
# 时间 : 2021/6/8 16:25
# 作者 : Dixit
# 文件 : hierarchical_trainer_workflow.py 
# 说明 : 
# 项目 : ncc_code
# 版权 : 北京华戍防务技术有限公司

import argparse
from gym.spaces import Tuple, Dict, Discrete, Box
import os

import ray
from ray import tune
from ray.tune.schedulers import AsyncHyperBandScheduler
from ray.tune.suggest import ConcurrencyLimiter
from ray.tune.suggest.hyperopt import HyperOptSearch

from ray.rllib.agents.trainer_template import build_trainer
from ray.rllib.agents.qmix.qmix import DEFAULT_CONFIG as QMIX_CONFIG
from ray.rllib.agents.qmix.qmix_policy import QMixTorchPolicy
from ray.rllib.agents.trainer import Trainer
from ray.rllib.agents.ppo.ppo import DEFAULT_CONFIG as PPO_CONFIG
from ray.rllib.agents.ppo.ppo_torch_policy import PPOTorchPolicy
from ray.rllib.evaluation.worker_set import WorkerSet
from ray.rllib.execution.common import _get_shared_metrics
from ray.rllib.execution.concurrency_ops import Concurrently
from ray.rllib.execution.metric_ops import StandardMetricsReporting
from ray.rllib.execution.rollout_ops import ParallelRollouts, ConcatBatches, \
    StandardizeFields, SelectExperiences
from ray.rllib.execution.replay_ops import SimpleReplayBuffer, Replay, \
    StoreToReplayBuffer
from ray.rllib.execution.train_ops import TrainOneStep, UpdateTargetNetwork
from ray.rllib.utils.test_utils import check_learning_achieved
from ray.rllib.env.multi_agent_env import ENV_STATE
from ray.rllib.examples.models.autoregressive_action_model import TorchAutoregressiveActionModel
from ray.rllib.examples.models.autoregressive_action_dist import TorchBinaryAutoregressiveDistribution
from ray.rllib.models import ModelCatalog

from mozi_ai_sdk.sc_code.envs.env_sc_new import SCEnv, LL_AGENTS_TO_OPERATION_GROUPS, LOW_LEVEL_OBS_SPACE,\
    STATE_SPACE, MID_LEVEL_OBS_SPACE, MID_LEVEL_STATE_SPACE, HIGH_LEVEL_OBS_SPACE, HIGH_LEVEL_STATE_SPACE, \
    LOW_LEVEL_ACT_SPACE, MID_LEVEL_ACT_SPACE, MID_LEVEL_ACTION_EMBED, HIGH_LEVEL_ACT_SPACE, HIGH_LEVEL_ACTION_EMBED

parser = argparse.ArgumentParser()
parser.add_argument("--as-test", action="store_true")
parser.add_argument("--torch", action="store_true")
parser.add_argument("--mixed-torch-tf", action="store_true")
parser.add_argument("--stop-iters", type=int, default=20)
parser.add_argument("--stop-reward", type=float, default=150.0)
parser.add_argument("--stop-timesteps", type=int, default=100000)

parser.add_argument("--mozi_server_path", type=str, default='D:\\mozi_server\\Mozi\\MoziServer\\bin')
parser.add_argument("--side", type=str, default="红方")
parser.add_argument("--platform_mode", type=str, default='eval')

# 创建的docker个数应该是num_workers+1，比如num_workers=3，那么需要创建4个docker
SERVER_DOCKER_DICT = {'8.140.121.210': 11, }  # {'8.140.121.210': 2, '123.57.137.210': 2}


def hierarchical_training_workflow(workers: WorkerSet, config: dict):

    def add_ppo_metrics(batch):
        print("PPO policy learning on samples from",
              batch.policy_batches.keys(), "env steps", batch.env_steps(),
              "agent steps", batch.env_steps())
        metrics = _get_shared_metrics()
        metrics.counters["agent_steps_trained_PPO"] += batch.env_steps()
        return batch

    def add_hl_qmix_metrics(batch):
        print("high level QMIX policy learning on samples from",
              batch.policy_batches.keys(), "env steps", batch.env_steps(),
              "agent steps", batch.env_steps())
        metrics = _get_shared_metrics()
        metrics.counters["agent_steps_trained_hl_QMIX"] += batch.env_steps()
        return batch

    def add_ml_qmix_metrics(batch):
        print("mid level QMIX policy learning on samples from",
              batch.policy_batches.keys(), "env steps", batch.env_steps(),
              "agent steps", batch.env_steps())
        metrics = _get_shared_metrics()
        metrics.counters["agent_steps_trained_ml_QMIX"] += batch.env_steps()
        return batch

    # Generate common experiences.
    rollouts = ParallelRollouts(workers, mode="bulk_sync")
    r1, r2, r3 = rollouts.duplicate(n=3)

    # high level QMIX sub-flow
    hl_replay_buffer = SimpleReplayBuffer(100)
    hl_qmix_store_op = r1.for_each(SelectExperiences(["high_level_qmix_policy"])) \
        .for_each(StoreToReplayBuffer(local_buffer=hl_replay_buffer))
    hl_qmix_replay_op = Replay(local_buffer=hl_replay_buffer) \
        .combine(ConcatBatches(min_batch_size=20)) \
        .for_each(add_hl_qmix_metrics) \
        .for_each(TrainOneStep(
            workers,
            policies=["high_level_qmix_policy"],
            num_sgd_iter=10,
            sgd_minibatch_size=8)) \
        .for_each(UpdateTargetNetwork(
            workers, 500, policies=["high_level_qmix_policy"]))
    hl_qmix_train_op = Concurrently(
        [hl_qmix_store_op, hl_qmix_replay_op], mode="round_robin", output_indexes=[1])

    # mid level QMIX sub-flow
    ml_replay_buffer = SimpleReplayBuffer(1000)
    ml_qmix_store_op = r2.for_each(SelectExperiences(["mid_level_qmix_policy"])) \
        .for_each(StoreToReplayBuffer(local_buffer=ml_replay_buffer))
    ml_qmix_replay_op = Replay(local_buffer=ml_replay_buffer) \
        .combine(ConcatBatches(min_batch_size=32)) \
        .for_each(add_ml_qmix_metrics) \
        .for_each(TrainOneStep(
            workers,
            policies=["mid_level_qmix_policy"],
            num_sgd_iter=10,
            sgd_minibatch_size=16)) \
        .for_each(UpdateTargetNetwork(
            workers, 500, policies=["mid_level_qmix_policy"]))
    ml_qmix_train_op = Concurrently(
        [ml_qmix_store_op, ml_qmix_replay_op], mode="round_robin", output_indexes=[1])

    # PPO sub-flow.
    low_level_ppo_train_op = r3.for_each(SelectExperiences(
        ["low_level_ppo_policy_a2a", "low_level_ppo_policy_a2s", "low_level_ppo_policy_ej"])) \
        .combine(ConcatBatches(min_batch_size=200)) \
        .for_each(add_ppo_metrics) \
        .for_each(StandardizeFields(["advantages"])) \
        .for_each(TrainOneStep(
            workers,
            policies=["low_level_ppo_policy_a2a", "low_level_ppo_policy_a2s", "low_level_ppo_policy_ej"],
            num_sgd_iter=10,
            sgd_minibatch_size=64))

    # Combined training flow
    train_op = Concurrently(
        [hl_qmix_train_op, ml_qmix_train_op, low_level_ppo_train_op], mode="async", output_indexes=[0, 1, 2])

    return StandardMetricsReporting(train_op, workers, config)


if __name__ == "__main__":
    args = parser.parse_args()
    assert not (args.torch and args.mixed_torch_tf),\
        "Use either --torch or --mixed-torch-tf, not both!"

    args = parser.parse_args()
    if args.platform_mode == 'train':
        pass
    elif args.platform_mode == 'development':
        ray.init(address="auto")
        # ray.init(local_mode=True)
    elif args.platform_mode == 'eval':
        os.environ['MOZIPATH'] = args.mozi_server_path
        ray.init(local_mode=True)
    else:
        raise NotImplementedError

    ModelCatalog.register_custom_model(
        "autoregressive_model", TorchAutoregressiveActionModel)
    ModelCatalog.register_custom_action_dist(
        "binary_autoreg_dist", TorchBinaryAutoregressiveDistribution)

    ppo_extra_config = {
        "model": {
            "custom_model": "autoregressive_model",
            "custom_action_dist": "binary_autoreg_dist",
        }
    }
    ppo_config = Trainer.merge_trainer_configs(PPO_CONFIG, ppo_extra_config, _allow_unknown_configs=True)

    high_level_qmix_obs_space = Tuple([
        Dict({
            "obs": Box(float("-inf"), float("inf"), shape=(HIGH_LEVEL_OBS_SPACE,)),
            ENV_STATE: Box(float("-inf"), float("inf"), shape=(HIGH_LEVEL_STATE_SPACE,)),
            # 上层智能体需要新增action_mask和avail_action
            "action_mask": Box(0, 1, shape=(HIGH_LEVEL_ACT_SPACE,)),
            "avail_actions": Box(-100, 100, shape=(HIGH_LEVEL_ACT_SPACE, HIGH_LEVEL_ACTION_EMBED)),
        }),
        Dict({
            "obs": Box(float("-inf"), float("inf"), shape=(HIGH_LEVEL_OBS_SPACE,)),
            ENV_STATE: Box(float("-inf"), float("inf"), shape=(HIGH_LEVEL_STATE_SPACE,)),
            # 上层智能体需要新增action_mask和avail_action
            "action_mask": Box(0, 1, shape=(HIGH_LEVEL_ACT_SPACE,)),
            "avail_actions": Box(-100, 100, shape=(HIGH_LEVEL_ACT_SPACE, HIGH_LEVEL_ACTION_EMBED)),
        }),
        Dict({
            "obs": Box(float("-inf"), float("inf"), shape=(HIGH_LEVEL_OBS_SPACE,)),
            ENV_STATE: Box(float("-inf"), float("inf"), shape=(HIGH_LEVEL_STATE_SPACE,)),
            # 上层智能体需要新增action_mask和avail_action
            "action_mask": Box(0, 1, shape=(HIGH_LEVEL_ACT_SPACE,)),
            "avail_actions": Box(-100, 100, shape=(HIGH_LEVEL_ACT_SPACE, HIGH_LEVEL_ACTION_EMBED)),
        }),
        Dict({
            "obs": Box(float("-inf"), float("inf"), shape=(HIGH_LEVEL_OBS_SPACE,)),
            ENV_STATE: Box(float("-inf"), float("inf"), shape=(HIGH_LEVEL_STATE_SPACE,)),
            # 上层智能体需要新增action_mask和avail_action
            "action_mask": Box(0, 1, shape=(HIGH_LEVEL_ACT_SPACE,)),
            "avail_actions": Box(-100, 100, shape=(HIGH_LEVEL_ACT_SPACE, HIGH_LEVEL_ACTION_EMBED)),
        }),
    ])
    high_level_qmix_act_space = Tuple([
        Discrete(HIGH_LEVEL_ACT_SPACE), Discrete(HIGH_LEVEL_ACT_SPACE),
        Discrete(HIGH_LEVEL_ACT_SPACE), Discrete(HIGH_LEVEL_ACT_SPACE)
    ])

    mid_level_qmix_obs_space = Tuple([
        Dict({
            "obs": Box(float("-inf"), float("inf"), shape=(MID_LEVEL_OBS_SPACE,)),
            ENV_STATE: Box(float("-inf"), float("inf"), shape=(MID_LEVEL_STATE_SPACE,)),
            # 中层智能体需要新增action_mask和avail_action
            "action_mask": Box(0, 1, shape=(MID_LEVEL_ACT_SPACE,)),
            "avail_actions": Box(-10, 10, shape=(MID_LEVEL_ACT_SPACE, MID_LEVEL_ACTION_EMBED)),
        }),
        Dict({
            "obs": Box(float("-inf"), float("inf"), shape=(MID_LEVEL_OBS_SPACE,)),
            ENV_STATE: Box(float("-inf"), float("inf"), shape=(MID_LEVEL_STATE_SPACE,)),
            # 中层智能体需要新增action_mask和avail_action
            "action_mask": Box(0, 1, shape=(MID_LEVEL_ACT_SPACE,)),
            "avail_actions": Box(-10, 10, shape=(MID_LEVEL_ACT_SPACE, MID_LEVEL_ACTION_EMBED)),
        }),
        Dict({
            "obs": Box(float("-inf"), float("inf"), shape=(MID_LEVEL_OBS_SPACE,)),
            ENV_STATE: Box(float("-inf"), float("inf"), shape=(MID_LEVEL_STATE_SPACE,)),
            # 中层智能体需要新增action_mask和avail_action
            "action_mask": Box(0, 1, shape=(MID_LEVEL_ACT_SPACE,)),
            "avail_actions": Box(-10, 10, shape=(MID_LEVEL_ACT_SPACE, MID_LEVEL_ACTION_EMBED)),
        }),
    ])
    mid_level_qmix_act_space = Tuple([
        Discrete(MID_LEVEL_ACT_SPACE), Discrete(MID_LEVEL_ACT_SPACE), Discrete(MID_LEVEL_ACT_SPACE)
    ])

    low_level_ppo_obs_space = Dict({
            "obs": Box(float("-inf"), float("inf"), shape=(LOW_LEVEL_OBS_SPACE,)),
            # "action_mask": Box(0, 1, shape=(self.action_size,)),
        })
    # auto-regressive 高度和速度
    low_level_ppo_act_space = Tuple([Discrete(LOW_LEVEL_ACT_SPACE[0]), Discrete(LOW_LEVEL_ACT_SPACE[1])])

    policies = {
        "high_level_qmix_policy": (QMixTorchPolicy, high_level_qmix_obs_space, high_level_qmix_act_space, QMIX_CONFIG),
        "mid_level_qmix_policy": (QMixTorchPolicy, mid_level_qmix_obs_space, mid_level_qmix_act_space, QMIX_CONFIG),
        "low_level_ppo_policy_a2a": (PPOTorchPolicy, low_level_ppo_obs_space, low_level_ppo_act_space, ppo_config),
        "low_level_ppo_policy_a2s": (PPOTorchPolicy, low_level_ppo_obs_space, low_level_ppo_act_space, ppo_config),
        "low_level_ppo_policy_ej": (PPOTorchPolicy, low_level_ppo_obs_space, low_level_ppo_act_space, ppo_config)
    }

    def policy_mapping_fn(agent_id):
        if agent_id == "group_0":
            return "high_level_qmix_policy"
        elif 'a2s_agent_group_' in agent_id:
            return "mid_level_qmix_policy"
        elif 'll_agent_' in agent_id:
            op_unit = LL_AGENTS_TO_OPERATION_GROUPS[agent_id]
            if "A2A_GROUP_" in op_unit:
                return "low_level_ppo_policy_a2a"
            elif "A2S_GROUP_" in op_unit:
                return "low_level_ppo_policy_a2s"
            elif "EJ_" in op_unit:
                return "low_level_ppo_policy_ej"
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    policies_to_train = ["high_level_qmix_policy", "mid_level_qmix_policy",
                         "low_level_ppo_policy_a2a", "low_level_ppo_policy_a2s", "low_level_ppo_policy_ej"]

    HierarchicalTrainer = build_trainer(
        name="PPO_QMIX_PPO_MultiAgent",
        default_policy=None,
        execution_plan=hierarchical_training_workflow)

    env_config = {'mode': 'eval',
                  'avail_docker_ip_port': ['127.0.0.1:6060', ],
                  # 'sever_docker_dict': SERVER_DOCKER_DICT,
                  'side_name': '蓝方',
                  'enemy_side_name': '红方'}

    config = {
        "env": SCEnv,
        "env_config": env_config,
        "rollout_fragment_length": 800,
        "num_workers": 0,
        # "model": {
        #     "custom_model": "autoregressive_model",
        #     "custom_action_dist": "binary_autoreg_dist",
        # },
        "lr": tune.uniform(5e-6, 5e-4),
        "multiagent": {
            "policies": policies,
            "policy_mapping_fn": policy_mapping_fn,
            "policies_to_train": policies_to_train,
        },
        "framework": "torch",
    }

    # stop = {
    #     "training_iteration": args.stop_iters,
    #     "timesteps_total": args.stop_timesteps,
    #     # "episode_reward_mean": args.stop_reward,
    # }
    algo = HyperOptSearch()
    algo = ConcurrencyLimiter(algo, max_concurrent=1)
    scheduler = AsyncHyperBandScheduler(max_t=1000)
    results = tune.run(HierarchicalTrainer,
                       metric="episode_reward_mean",
                       mode="max",
                       search_alg=algo,
                       scheduler=scheduler,
                       num_samples=1,
                       checkpoint_freq=1,
                       keep_checkpoints_num=10,
                       config=config,
                       # stop=stop
                       )

    if args.as_test:
        check_learning_achieved(results, args.stop_reward)

    ray.shutdown()
