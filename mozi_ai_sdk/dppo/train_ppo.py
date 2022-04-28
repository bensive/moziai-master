from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
from threading import Thread
import os
import multiprocessing
import random
import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath.partition('mozi_ai_sdk')[0]
sys.path.append(rootPath)
os.environ['MOZIPATH'] = 'D:\\mozi_server_个人版\\Mozi\\MoziServer\\bin'
from absl import app
from absl import flags
from absl import logging
import tensorflow as tf
from gym import spaces
import numpy as np

from mozi_ai_sdk.dppo.envs.spaces.mask_discrete import MaskDiscrete
from mozi_ai_sdk.dppo.agents.ppo_policies import LstmPolicy, MlpPolicy
from mozi_ai_sdk.dppo.agents.ppo_agent import PPOActor, PPOLearner
from mozi_ai_sdk.dppo.envs.env import Environment
from mozi_ai_sdk.dppo.envs import etc
from mozi_ai_sdk.dppo.envs.observations import Features
from mozi_ai_sdk.dppo.envs.tasks import Task

from mozi_ai_sdk.dppo.utils.utils import print_arguments

FLAGS = flags.FLAGS
flags.DEFINE_enum("job_name", 'actor', ['actor', 'learner'], "Job type.")
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


def create_env():
    env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME, etc.SIMULATE_COMPRESSION,
                      etc.DURATION_INTERVAL,
                      etc.SYNCHRONOUS)
    env.start()
    scenario = env.reset(FLAGS.side_name)
    env = Task(env, scenario, FLAGS.side_name)
    env = Features(env, scenario, FLAGS.side_name)
    return env


def start_actor():
    tf_config(ncpu=2)
    env = create_env()
    policy = {'lstm': LstmPolicy,
              'mlp': MlpPolicy}[FLAGS.policy]
    actor = PPOActor(env=env,
                     side_name=FLAGS.side_name,
                     policy=policy,
                     unroll_length=FLAGS.unroll_length,
                     gamma=FLAGS.discount_gamma,
                     lam=FLAGS.lambda_return,
                     learner_ip=FLAGS.learner_ip,
                     port_A=FLAGS.port_A,
                     port_B=FLAGS.port_B)
    actor.run()
    # env.close()


def start_learner():
    tf_config()

    # env = create_env()
    class Tempenv(object):
        def __init__(self):
            self.action_space = MaskDiscrete(71)
            self.observation_space = spaces.Tuple([spaces.Box(0.0, float('inf'), [740], dtype=np.float32),
                                                   spaces.Box(0.0, 1.0, [71], dtype=np.float32)])

    env = Tempenv()
    policy = {'lstm': LstmPolicy,
              'mlp': MlpPolicy}[FLAGS.policy]
    learner = PPOLearner(env=env,
                         policy=policy,
                         unroll_length=FLAGS.unroll_length,
                         lr=FLAGS.learning_rate,
                         clip_range=FLAGS.clip_range,
                         batch_size=FLAGS.batch_size,
                         ent_coef=FLAGS.ent_coef,
                         vf_coef=FLAGS.vf_coef,
                         max_grad_norm=0.5,
                         queue_size=FLAGS.learner_queue_size,
                         print_interval=FLAGS.print_interval,
                         save_interval=FLAGS.save_interval,
                         learn_act_speed_ratio=FLAGS.learn_act_speed_ratio,
                         save_dir=FLAGS.save_dir,
                         init_model_path=FLAGS.init_model_path,
                         port_A=FLAGS.port_A,
                         port_B=FLAGS.port_B)
    learner.run()


def main(argv):
    logging.set_verbosity(logging.ERROR)
    print_arguments(FLAGS)
    if FLAGS.job_name == 'actor':
        start_actor()
    else:
        start_learner()


if __name__ == '__main__':
    app.run(main)
