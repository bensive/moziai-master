# 时间 : 2021/3/31 9:42 
# 作者 : Dixit
# 文件 : main_versus.py
# 说明 : 
# 项目 : hxfb_test
# 版权 : 北京华戍防务技术有限公司

import argparse
import collections
import gym
import json
import os
from pathlib import Path

import ray
from ray.rllib.env import MultiAgentEnv
from ray.rllib.env.base_env import _DUMMY_AGENT_ID
from ray.rllib.evaluation.worker_set import WorkerSet
from ray.rllib.policy.sample_batch import DEFAULT_POLICY_ID
from ray.rllib.utils.spaces.space_utils import flatten_to_single_ndarray
from mozi_ai_sdk.hxfb_test.envs.env_hxfb import HXFBEnv
from gym.spaces import Discrete, Box, Dict
from ray.rllib.agents.ppo import PPOTrainer

# from ray.managers.zmq_manager import g_zmq_manager
# from ray.managers.utils import *


parser = argparse.ArgumentParser()
parser.add_argument("--avail_ip_port", type=str, default='127.0.0.1:6060')
# 新传入对战相关参数，当前未用
# parser.add_argument("--versus_id", type=str, default='')
# parser.add_argument("--versus_room_id", type=str, default='')
# parser.add_argument("--room_game_number", type=int, default=10)
parser.add_argument("--platform_mode", type=str, default='eval')
parser.add_argument("--mozi_server_path", type=str, default='D:\\mozi_4p\\mozi\\Mozi\\MoziServer\\bin')


def run(checkpoint=None,
        evaluate_episodes=10,
        action_size=48,
        obs_size=350,
        avail_ip_port=None,
        _lambda=0.98,
        platform_mode='eval'):
    env = HXFBEnv
    act_space = Discrete(action_size)
    obs_space = Dict({"obs": Box(float("-inf"), float("inf"), shape=(obs_size,)),
                      # "action_mask": Box(0, 1, shape=(action_size,)),
                      })
    config = {"env_config": {'mode': platform_mode,
                             'avail_docker_ip_port': [avail_ip_port, ],
                             'side_name': '红方',
                             'enemy_side_name': '蓝方',
                             'action_dim': action_size,
                             'obs_dim': obs_size,
                             },
              # "log_level": "DEBUG",
              "framework": 'torch',
              "model": {"use_lstm": True,
                        # "custom_model": "mask_model",
                        "max_seq_len": 64,
                        # Size of the LSTM cell.
                        "lstm_cell_size": 256,
                        # Whether to feed a_{t-1}, r_{t-1} to LSTM.
                        "lstm_use_prev_action_reward": True,
                        },
              'multiagent': {'agent_0': (obs_space, act_space, {"gamma": 0.99}),
                             },
              "vf_share_layers": True,
              "batch_mode": 'truncate_episodes',  # 'truncate_episodes'
              "num_workers": 0,
              "num_envs_per_worker": 1,
              # 'vf_loss_coeff': vf_loss_coeff,
              # 'kl_coeff': kl_coeff,
              'lambda': _lambda,
              # 'vf_clip_param': vf_clip_param,
              # 'clip_param': clip_param,
              }

    agent = PPOTrainer(env=env, config=config)
    agent.restore(checkpoint)
    rollout(agent, env, evaluate_episodes, platform_mode)
    agent.stop()


class DefaultMapping(collections.defaultdict):
    """default_factory now takes as an argument the missing key."""

    def __missing__(self, key):
        self[key] = value = self.default_factory(key)
        return value


def default_policy_agent_mapping(unused_agent_id):
    return DEFAULT_POLICY_ID


def keep_going(episodes, num_episodes):
    """Determine whether we've collected enough data"""
    # if num_episodes is set, this overrides num_steps
    if num_episodes:
        return episodes < num_episodes
    return True


def rollout(agent,
            env_name,
            num_episodes=0,
            platform_mode=None
            ):
    policy_agent_mapping = default_policy_agent_mapping

    if hasattr(agent, "workers") and isinstance(agent.workers, WorkerSet):
        env = agent.workers.local_worker().env
        multiagent = isinstance(env, MultiAgentEnv)
        if agent.workers.local_worker().multiagent:
            policy_agent_mapping = agent.config["multiagent"][
                "policy_mapping_fn"]

        policy_map = agent.workers.local_worker().policy_map
        state_init = {p: m.get_initial_state() for p, m in policy_map.items()}
        use_lstm = {p: len(s) > 0 for p, s in state_init.items()}
    else:
        env = gym.make(env_name)
        multiagent = False
        try:
            policy_map = {DEFAULT_POLICY_ID: agent.policy}
        except AttributeError:
            raise AttributeError(
                "Agent ({}) does not have a `policy` property! This is needed "
                "for performing (trained) agent rollouts.".format(agent))
        use_lstm = {DEFAULT_POLICY_ID: False}

    # action_init = {
    #     p: flatten_to_single_ndarray(m.action_space.sample())
    #     for p, m in policy_map.items()
    # }
    action_init = {
        p: flatten_to_single_ndarray(0)
        for p, m in policy_map.items()
    }

    episodes = 0
    while keep_going(episodes, num_episodes):
        mapping_cache = {}  # in case policy_agent_mapping is stochastic
        obs = env.reset()
        agent_states = DefaultMapping(
            lambda agent_id: state_init[mapping_cache[agent_id]])
        prev_actions = DefaultMapping(
            lambda agent_id: action_init[mapping_cache[agent_id]])
        prev_rewards = collections.defaultdict(lambda: 0.)
        done = False
        reward_total = 0.0
        while not done and keep_going(episodes, num_episodes):
            multi_obs = obs if multiagent else {_DUMMY_AGENT_ID: obs}
            action_dict = {}
            for agent_id, a_obs in multi_obs.items():
                if a_obs is not None:
                    policy_id = mapping_cache.setdefault(
                        agent_id, policy_agent_mapping(agent_id))
                    p_use_lstm = use_lstm[policy_id]
                    if p_use_lstm:
                        a_action, p_state, _ = agent.compute_action(
                            a_obs,
                            state=agent_states[agent_id],
                            prev_action=prev_actions[agent_id],
                            prev_reward=prev_rewards[agent_id],
                            policy_id=policy_id,
                            # explore=False
                        )
                        agent_states[agent_id] = p_state
                    else:
                        a_action = agent.compute_action(
                            a_obs,
                            prev_action=prev_actions[agent_id],
                            prev_reward=prev_rewards[agent_id],
                            policy_id=policy_id)
                    a_action = flatten_to_single_ndarray(a_action)
                    action_dict[agent_id] = a_action
                    prev_actions[agent_id] = a_action
            action = action_dict

            action = action if multiagent else action[_DUMMY_AGENT_ID]
            next_obs, reward, done, info = env.step(action)
            if multiagent:
                for agent_id, r in reward.items():
                    prev_rewards[agent_id] = r
            else:
                prev_rewards[_DUMMY_AGENT_ID] = reward

            if multiagent:
                done = done["__all__"]
                reward_total += sum(reward.values())
            else:
                reward_total += reward
            obs = next_obs
        print("Episode #{}: reward: {}".format(episodes, reward_total))
        if platform_mode == 'versus':
            pass
            # if score is None:
            #     raise ValueError('对战分数获取失败！！')
            # message = {'zmq_command': 'report_versus_result_per_game', 'versus_id': versus_id,
            #            'versus_room_id': versus_room_id, 'rewards': score}
            # g_zmq_manager.send_message_to_backend(message)
        if done:
            episodes += 1


if __name__ == "__main__":
    args = parser.parse_args()

    if args.platform_mode == 'versus':
        pass
        # from ray.managers.zmq_manager import g_zmq_manager
        # from ray.managers.utils import *
    elif args.platform_mode == 'eval':
        # 设置墨子可执行程序的路径，用于代码启动墨子
        os.environ['MOZIPATH'] = args.mozi_server_path
    # ray.init(address=args.address, _redis_password=args.redis_password)
    ray.init()
    # checkpoint_path = os.path.join(Path(__file__).parent.parent, 'checkpoint/checkpoint_2/checkpoint-2')
    checkpoint_path = os.path.join(Path(__file__).parent, 'checkpoint')
    checkpoint_dir = None
    param_dir = None
    for root_dir, dirs, files in os.walk(checkpoint_path):
        if 'params.json' in files:
            param_dir = os.path.join(root_dir, 'params.json')
        for file in files:
            if 'checkpoint-' in file:
                checkpoint_dir = os.path.join(root_dir, file)
                print(checkpoint_dir)
                # by 张志高
                checkpoint_dir = checkpoint_dir.replace('.tune_metadata', '')
                break
        if checkpoint_dir:
            break
    if param_dir:
        with open(param_dir, 'r') as fp:
            params = json.load(fp)
    else:
        raise ValueError('参数路径为空')
    run(checkpoint=checkpoint_dir,
        evaluate_episodes=1,
        avail_ip_port=args.avail_ip_port,
        _lambda=params['lambda'],
        platform_mode=args.platform_mode
        )
