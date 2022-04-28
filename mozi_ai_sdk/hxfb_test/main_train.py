# 时间 : 2021/2/16 15:58 
# 作者 : Dixit
# 文件 : main_train.py 
# 说明 : 
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from ray.tune.schedulers import AsyncHyperBandScheduler
from ray.tune.suggest import ConcurrencyLimiter
from ray.tune.suggest.hyperopt import HyperOptSearch
from ray.rllib.utils.framework import try_import_tf, try_import_torch

import argparse
from gym.spaces import Discrete, Box, Dict
import zmq
import sys
import torch
import ray
from ray import tune
import os

from ray.remote_handle_docker import stop_docker
from mozi_ai_sdk.hxfb_test.envs.env_hxfb import HXFBEnv

file_dir = '/root/logs/'

tf1, tf, tfv = try_import_tf()
torch, nn = try_import_torch()

parser = argparse.ArgumentParser()

# 集群口令
parser.add_argument("--address", type=str, default='172.17.94.8:6379')
parser.add_argument("--redis_password", type=str, default='5241590000000000')

# 训练相关参数
parser.add_argument("--training_id", type=str, default='test_multi_trials')
parser.add_argument("--num_gpus", type=int, default=0)
parser.add_argument("--num_gpus_per_worker", type=int, default=0)
parser.add_argument("--training_iteration", type=int, default=50000)
parser.add_argument("--num_samples", type=int, default=1)
parser.add_argument("--checkpoint_freq", type=int, default=1)
parser.add_argument("--keep_checkpoints_num", type=int, default=10)
parser.add_argument("--num_workers", type=int, default=10)
parser.add_argument("--restore", type=str, default=None)

# 智能体相关参数
parser.add_argument("--agent_id", type=str, default='robot')
parser.add_argument("--framework", type=str, default="torch")
parser.add_argument("--vf_share_layers", type=bool, default=True)
parser.add_argument("--vf_loss_coeff", type=float, default=1.0)
parser.add_argument("--kl_coeff", type=float, default=0.2)
parser.add_argument("--clip_param", type=float, default=0.3)
parser.add_argument("--vf_clip_param", type=float, default=10)
parser.add_argument("--lr_min", type=float, default=5e-6)
parser.add_argument("--lr_max", type=float, default=5e-5)
parser.add_argument("--num_sgd_iter", type=int, default=100)
parser.add_argument("--sgd_minibatch_size", type=int, default=128)
parser.add_argument("--rollout_fragment_length", type=int, default=512)
parser.add_argument("--train_batch_size", type=int, default=-1)
parser.add_argument("--side", type=str, default="红方")

parser.add_argument("--Lambda", type=float, default=0.98)
parser.add_argument("--algorithm", type=str, default="DDPPO")

# 需确认
parser.add_argument("--torch", action="store_true")
parser.add_argument("--as-test", action="store_true")
parser.add_argument("--stop-iters", type=int, default=50000)
parser.add_argument("--stop-timesteps", type=int, default=1000000)
parser.add_argument("--stop-reward", type=float, default=1.5)
parser.add_argument("--platform_mode", type=str, default='development')

# zmq init
zmq_context = zmq.Context()

# 创建的docker个数应该是num_workers+1，比如num_workers=3，那么需要创建4个docker
SERVER_DOCKER_DICT = {'8.140.121.210': 11, }  # {'8.140.121.210': 2, '123.57.137.210': 2}


def reset_training_docker(_training_id):
    """
    功能：重启训练docker
    作者：张志高
    时间：2021-2-16
    """
    try:
        message = {}
        message['zmq_command'] = 'reset_training_docker'
        message['training_id'] = _training_id
        socket_to = g_zmq_manager.send_message_to_backend(message)
        recv_msg = socket_to.recv_pyobj()
        assert type(recv_msg) == str
        if 'OK' in recv_msg:
            print(f'重启训练docker成功，训练ID: {_training_id}')
        else:
            sys.exit(1)
    except Exception:
        print(f'重启训练docker失败，训练ID: {_training_id}')
        sys.exit(1)


def start_tune(training_id=None,
               num_gpus=None,
               num_gpus_per_worker=None,
               num_workers=10,
               training_iteration=None,
               num_samples=1,
               checkpoint_freq=None,
               keep_checkpoints_num=None,
               framework=None,
               model=None,
               vf_share_layers=None,
               vf_loss_coeff=1.0,
               kl_coeff=0.2,
               vf_clip_param=10.0,
               Lambda=None,
               clip_param=0.3,
               lr_min=5e-6,
               lr_max=5e-4,
               num_sgd_iter=100,
               sgd_minibatch_size=256,
               rollout_fragment_length=512,
               train_batch_size=-1,
               side_name=None,
               restore=None,
               platform_mode=None,
               # 内部参数
               algorithm_name='DDPPO',
               action_size=None,
               obs_size=None,
               log_to_file=file_dir,
               agent_id=None):
    act_space = Discrete(action_size)
    obs_space = Dict({"obs": Box(float("-inf"), float("inf"), shape=(obs_size,)),
                      # "action_mask": Box(0, 1, shape=(action_size,)),
                      })

    config = {"env": HXFBEnv,
              "env_config": {'mode': platform_mode,  # 'train'/'development'/'eval'
                             'sever_docker_dict': SERVER_DOCKER_DICT,  # {'8.140.121.210': 2, '123.57.81.172': 2}
                             'side_name': side_name,
                             'enemy_side_name': '蓝方',
                             'action_dim': action_size,
                             'obs_dim': obs_size,
                             'training_id': training_id,
                             },
              # "monitor": True,
              # "ignore_worker_failures": True,
              # "log_level": "DEBUG",
              "num_gpus": num_gpus,
              "num_gpus_per_worker": num_gpus_per_worker,
              # "queue_trials": True,
              "framework": framework,
              "model": {"use_lstm": True,
                        # "custom_model": "mask_model",
                        "max_seq_len": 64,
                        # Size of the LSTM cell.
                        "lstm_cell_size": 256,
                        # Whether to feed a_{t-1}, r_{t-1} to LSTM.
                        "lstm_use_prev_action_reward": True,
                        },
              'multiagent': {
                  'agent_0': (obs_space, act_space, {"gamma": 0.99}),
              },
              "lambda": 0.98,
              "vf_share_layers": True,
              "vf_loss_coeff": vf_loss_coeff,
              'entropy_coeff': 0.0,
              "kl_coeff": kl_coeff,
              "vf_clip_param": vf_clip_param,
              "clip_param": clip_param,
              "lr": tune.uniform(lr_min, lr_max), 
              "num_sgd_iter": num_sgd_iter,
              "sgd_minibatch_size": sgd_minibatch_size,
              "rollout_fragment_length": rollout_fragment_length,
              "num_envs_per_worker": 1,
              "train_batch_size": train_batch_size,
              "batch_mode": "truncate_episodes",
              "num_workers": num_workers,
              }
    if platform_mode == 'train':
        config['env_config']['schedule_addr'] = BACKEND_SERVER_IP
        config['env_config']['schedule_port'] = BACKEND_SERVER_PORT

    stop = {
        "training_iteration": training_iteration,
    }
    best_trial = None
    best_config = None
    try:
        algo = HyperOptSearch()
        algo = ConcurrencyLimiter(algo, max_concurrent=1)
        scheduler = AsyncHyperBandScheduler(max_t=1000)
        if platform_mode == 'train':
            result_dir = os.path.join(TRAINING_RESULT_PATH, agent_id, 'result')
        elif platform_mode == 'development':
            result_dir = None
        else:
            raise NotImplementedError
        results = tune.run(algorithm_name,
                           name=training_id,
                           metric="episode_reward_mean",
                           mode="max",
                           local_dir=result_dir,
                           search_alg=algo,
                           scheduler=scheduler,
                           num_samples=num_samples,
                           checkpoint_freq=checkpoint_freq,
                           keep_checkpoints_num=keep_checkpoints_num,
                           config=config,
                           # restore=restore,
                           # log_to_file=True,
                           # max_failures=3,
                           # resume=True,
                           # queue_trials=False,
                           # stop=stop
                           )

        best_trial = results.get_best_trial('episode_reward_mean')
        best_config = results.get_best_config('episode_reward_mean')
        print(best_trial)
        print(best_config)
    except Exception as e:
        print(f'训练时发生异常：{str(e)}')
        # 后续放开 张志高 2021-2-16
        # reset_training_docker(training_id)
        if platform_mode == 'development':
            stop_docker(SERVER_DOCKER_DICT)
    return best_trial, best_config


if __name__ == '__main__':

    args = parser.parse_args()
    if args.platform_mode == 'train':
        from ray.managers.config import *
        from ray.managers.utils import *
        from ray.managers.zmq_manager import g_zmq_manager
        g_zmq_manager.register_me(args.training_id)
        g_zmq_manager.start_listen_thread()
        ray.init(address=args.address, _redis_password=args.redis_password)
    elif args.platform_mode == 'development':
        ray.init(address="auto")
        # ray.init(local_mode=True)
    else:
        raise NotImplementedError

    start_tune(training_id=args.training_id,
               num_gpus=args.num_gpus,
               num_gpus_per_worker=args.num_gpus_per_worker,
               num_workers=args.num_workers,
               training_iteration=args.training_iteration,
               num_samples=args.num_samples,  # 警告, 该值为并行实验个数，当前只能传1，
               checkpoint_freq=args.checkpoint_freq,
               keep_checkpoints_num=args.keep_checkpoints_num,
               framework=args.framework,
               vf_share_layers=args.vf_share_layers,
               vf_loss_coeff=args.vf_loss_coeff,
               kl_coeff=args.kl_coeff,
               vf_clip_param=args.vf_clip_param,
               Lambda=args.Lambda,
               clip_param=args.clip_param,
               lr_min=args.lr_min,
               lr_max=args.lr_max,
               num_sgd_iter=args.num_sgd_iter,
               sgd_minibatch_size=args.sgd_minibatch_size,
               rollout_fragment_length=args.rollout_fragment_length,
               train_batch_size=args.train_batch_size,
               side_name=args.side,
               restore=args.restore,
               platform_mode=args.platform_mode,
               # 内部参数
               algorithm_name=args.algorithm,
               action_size=48,
               obs_size=350,
               log_to_file=file_dir,
               agent_id=args.agent_id)

    print('训练结束')
