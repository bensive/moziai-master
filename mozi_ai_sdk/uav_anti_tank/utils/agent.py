#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : agent.py
# Create date : 2020-03-23 00:56
# Modified date : 2020-05-06 14:37
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

from mozi_ai_sdk.uav_anti_tank.utils import base_agent
from mozi_ai_sdk.uav_anti_tank.rlmodel.ddpg import train
from mozi_ai_sdk.uav_anti_tank.rlmodel.ddpg import buffer
from mozi_ai_sdk.uav_anti_tank.env import etc as etc
import numpy as np
from mozi_ai_sdk.uav_anti_tank.utils.pic import write_loss


class AgentUavAntiTank(base_agent.BaseAgent):
    """
    无人机攻击坦克案例的智能体
    """

    def __init__(self, env, start_epoch=0):
        super(AgentUavAntiTank, self).__init__()
        '''创建训练器'''

        self.episodes = start_epoch
        self.ram = buffer.MemoryBuffer(etc.MAX_BUFFER)  # 算法缓存大小
        self.trainer = train.Trainer(
            env.state_space_dim,  # 状态空间维度
            env.action_space_dim,  # 动作空间维度
            env.action_max,  # ？？？？？
            self.ram,
            etc.device,  # CPU or GPU
            write_loss,
            int(start_epoch),
            etc.MODELS_PATH)

        self.env = env
        self.train_step = 0  # 当前决策步数

        # 设置状态空间维度及动作空间维度
        self.setup(env.state_space_dim, env.action_space_dim)

    def reset(self):
        """
        重置
        """
        self.trainer.save_model(self.episodes, etc.MODELS_PATH)  # 保存一下已经训练的轮数
        self.episodes += 1

    def setup(self, state_space, action_space):
        """
        设置
        """
        self.state_space = state_space  # 为什么不叫state_space
        self.action_space = action_space

    def make_decision(self, state_now, reward_now):
        """
        功能说明：智能体的决策函数，该函数根据从环境所得的状态及回报值来决定下一步该执行什么动作。
        执行流程：训练器生成动作
        参数：state_now:当前状态空间；
              reward_now:当前的回报值
        """
        super(AgentUavAntiTank, self).step(state_now)
        state = np.float32(state_now)  # 强制转化为浮点类型

        # 4/5的动作随机生成，1/5的动作由模型生成
        if self.episodes % 5 == 0:
            action = self.trainer.get_exploitation_action(state)  # 通过模型来生成动作，利用，
        else:
            action = self.trainer.get_exploration_action(state)  # 随机生成动作。

        # 返回动作
        return action

    def train(self, state_last, action_last, reward_now, state_new, cur_step):
        """
        功能说明：根据动作执行结果，训练一次智能体
        作者：许怀阳
        时间：2020.05.05 17:20
        执行流程：
        参数：state_now:当前状态空间；
              reward_now:当前的回报值
        """
        # 添加最新经验，并优化训练一把，再做决策
        self.ram.add(state_last, action_last, reward_now, state_new)
        self.trainer.optimize(cur_step)
        self.train_step += 1

        # 返回动作
        return True
