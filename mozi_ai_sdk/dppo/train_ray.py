from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
from threading import Thread
import os
import multiprocessing
import random
import time

# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = curPath.partition('mozi_ai_sdk')[0]
# sys.path.append(rootPath)

from absl import app
from absl import flags
from absl import logging
import tensorflow as tf
from gym import spaces
import numpy as np

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath.partition('mozi_ai_sdk')[0]
sys.path.append(rootPath)

from mozi_ai_sdk.dppo.envs.spaces.mask_discrete import MaskDiscrete
from mozi_ai_sdk.dppo.agents.ppo_policies import LstmPolicy, MlpPolicy
from mozi_ai_sdk.dppo.agents.ppo_agent import PPOActor, PPOLearner
from mozi_ai_sdk.dppo.envs.env import Environment
from mozi_ai_sdk.dppo.envs import etc
from mozi_ai_sdk.dppo.envs.observations import Features
from mozi_ai_sdk.dppo.envs.tasks import Task
from mozi_ai_sdk.dppo.envs.env_qc import HXFBEnv


from mozi_ai_sdk.dppo.utils.utils import print_arguments

import ray
from ray.rllib.agents.ppo import PPOTrainer
from ray.tune.logger import pretty_print

FLAGS = flags.FLAGS
flags.DEFINE_enum("job_name", 'learner', ['actor', 'learner'], "Job type.")
flags.DEFINE_enum("policy", 'mlp', ['mlp', 'lstm'], "Job type.")
flags.DEFINE_integer("unroll_length", 128, "Length of rollout steps.")
flags.DEFINE_string("learner_ip", "localhost", "Learner IP address.")
flags.DEFINE_string("port_A", "5700", "Port for transporting model.")
flags.DEFINE_string("port_B", "5701", "Port for transporting data.")
flags.DEFINE_string("side_name", "红方", "side info.")
flags.DEFINE_float("discount_gamma", 0.998, "Discount factor.")
flags.DEFINE_float("lambda_return", 0.95, "Lambda return factor.")
flags.DEFINE_float("clip_range", 0.1, "Clip range for PPO.")
flags.DEFINE_float("ent_coef", 0.01, "Coefficient for the entropy term.")
flags.DEFINE_float("vf_coef", 0.5, "Coefficient for the value loss.")
flags.DEFINE_float("learn_act_speed_ratio", 0, "Maximum learner/actor ratio.")
flags.DEFINE_integer("batch_size", 32, "Batch size.")
flags.DEFINE_integer("game_steps_per_episode", 43200, "Maximum steps per episode.")
flags.DEFINE_integer("learner_queue_size", 1024, "Size of learner's unroll queue.")
flags.DEFINE_float("learning_rate", 1e-5, "Learning rate.")
flags.DEFINE_string("init_model_path", None, "Initial model path.")
flags.DEFINE_string("save_dir", "./checkpoints/", "Dir to save models to")
# flags.DEFINE_integer("save_interval", 50000, "Model saving frequency.")
# flags.DEFINE_integer("print_interval", 1000, "Print train cost frequency.")
flags.DEFINE_integer("save_interval", 5000, "Model saving frequency.")
flags.DEFINE_integer("print_interval", 5000, "Print train cost frequency.")
flags.FLAGS(sys.argv)


def tf_config(ncpu=None):
  if ncpu is None:
    ncpu = multiprocessing.cpu_count()
    if sys.platform == 'darwin': ncpu //= 2
  config = tf.ConfigProto(allow_soft_placement=True,
                          intra_op_parallelism_threads=ncpu,
                          inter_op_parallelism_threads=ncpu)
  config.gpu_options.allow_growth = True
  tf.Session(config=config).__enter__()


# def create_env(env_config):
    # env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME, etc.SIMULATE_COMPRESSION,
    #                   etc.DURATION_INTERVAL,
    #                   etc.SYNCHRONOUS)
    # env.start()
    # scenario = env.reset("红方")#(FLAGS.side_name)
    # env = Task(env, scenario, "红方")
    # env = Features(env, scenario, "红方")
#     return env

def prepare_ray_agent():
    env_config = {}
    # env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME, etc.SIMULATE_COMPRESSION,
    #                   etc.DURATION_INTERVAL,
    #                   etc.SYNCHRONOUS)
    # print('agents connected')
    # env.start()
    # scenario = env.reset('红方')
    # env = Task(env, scenario, '红方')
    # print('agent prepared')

    env = HXFBEnv(env_config)
    obs_space = env.observation_space
    act_space = env.action_space
    # register_env("mozi_env", lambda _: env)
    agent=PPOTrainer(env=HXFBEnv,
                     config={"num_workers": 1,
                            "env_config": {},
                            # "num_gpus": 1,
                            "vf_clip_param": 1e3,
                            # "model": {
                            #         "use_lstm": True,
                            #     }, 
                            #"lr":1e-3,
                            "sgd_minibatch_size": 256,
                            #"framework":'tf',
                            "framework":'torch',
                            #"model":{"custom_model": args.CNNs_name},
                            'multiagent': {
                                'agent_0': (obs_space, act_space, {"gamma": 0.99}),
                                #'fighter_1': (obs_space, act_space, {"gamma": 0.99}),
                                #'fighter_2': (obs_space, act_space, {"gamma": 0.99}),
                            },
                            "vf_share_layers": True,
                            "vf_loss_coeff": 1e-5, #1e-2, 5e-4,
                            #"lr": grid_search([1e-2]),#, 1e-4, 1e-6]),  # try different lrs
                            "batch_mode": "complete_episodes", #'truncate_episodes'
                            #"num_workers": 2,
                            })
    return agent



def train():
    agent = prepare_ray_agent()
    #agent.restore('/home/ben/ray_results/PPO_UGSEnv_2020-10-13_11-56-33we52a5kr/checkpoint_4502/checkpoint-4502')
    for i in range(10000):
        result = agent.train()
        print (pretty_print(result))
        if i % 100==1:
            state1 = agent.save()
    agent.save()



if __name__ == '__main__':
  # ray.init(num_gpus=1, _memory = 4000*1024*1024, object_store_memory = 800*1024*1024)
  ray.init(address='auto', _redis_password='5241590000000000')
  import os
  print(os.getpid())
  train()
