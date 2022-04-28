#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : train.py
# Create date : 2019-10-20 19:59
# Modified date : 2020-03-23 01:23
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

from __future__ import division


import datetime
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from . import utils
from . import model

BATCH_SIZE = 128  #
LEARNING_RATE = 0.001  # 训练学习率
GAMMA = 0.99  # 奖励随时间步的衰减因子
TAU = 0.001


class Trainer:
    """训练器"""
    def __init__(self, state_dim, action_dim, action_lim, ram, dev, write_loss, epoch=0, model_save_path=None):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.action_lim = action_lim
        self.ram = ram
        self.iter = 0
        self.noise = utils.OrnsteinUhlenbeckActionNoise(self.action_dim)
        self.device = dev
        self.write_loss = write_loss

        # 策略网络（在线和目标）及其优化器--(online policy和 target policy )
        self.actor = model.Actor(self.state_dim, self.action_dim, self.action_lim).to(self.device)
        self.target_actor = model.Actor(self.state_dim, self.action_dim, self.action_lim).to(self.device)
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), LEARNING_RATE)

        # 价值网络（在线和目标）及其优化器
        self.critic = model.Critic(self.state_dim, self.action_dim).to(self.device)
        self.target_critic = model.Critic(self.state_dim, self.action_dim).to(self.device)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), LEARNING_RATE)

        # 如果当前轮数大于0，则表示以前训练过，则载入训练过的模型
        if epoch > 0:
            print("load models")
            self.load_models(epoch, model_save_path)

        # 用在线网络更新目标网络，
        utils.hard_update(self.target_actor, self.actor)
        utils.hard_update(self.target_critic, self.critic)  # 貌似和load_Models里重复了。（许怀阳，2020.05.05 17:13）

    def get_exploitation_action(self, state):
        """利用模型产生动作"""
        state = Variable(torch.from_numpy(state).to(self.device))
        action = self.target_actor.forward(state).detach()
        return action.data.cpu().numpy()

    def get_exploration_action(self, state):
        """随机探索产生动作"""
        state = Variable(torch.from_numpy(state).to(self.device))
        action = self.actor.forward(state).detach()
        new_action = action.data.cpu().numpy() + (self.noise.sample() * self.action_lim)
        return new_action

    def optimize(self, step):
        """'优化"""
        s1, a1, r1, s2 = self.ram.sample(BATCH_SIZE)
        s1 = Variable(torch.from_numpy(s1).to(self.device))
        a1 = Variable(torch.from_numpy(a1).to(self.device))
        r1 = Variable(torch.from_numpy(r1).to(self.device))
        s2 = Variable(torch.from_numpy(s2).to(self.device))

        a2 = self.target_actor.forward(s2).detach()  # 根据S2得出的下一个动作a2
        next_val = torch.squeeze(self.target_critic.forward(s2, a2).detach())  # 根据s2和a2得出的目标值
        y_expectd = r1 + GAMMA * next_val  # 目标回报值

        y_predicted = torch.squeeze(self.critic.forward(s1, a1))  # 主价值网络得到的回报值

        loss_critic = F.smooth_l1_loss(y_predicted, y_expectd)  # 价值损失（回报值的损失）
        self.critic_optimizer.zero_grad()   # 优化器参数置为零
        if self.write_loss:
            self.write_loss(step, loss_critic.item(), "loss_critic")  # 将损失值保存到文件中
        loss_critic.backward()  # 反向传播，
        self.critic_optimizer.step()  # 修改价值网络参数

        pred_a1 = self.actor.forward(s1)
        loss_actor = -1 * torch.sum(self.critic.forward(s1, pred_a1))
        self.actor_optimizer.zero_grad()
        if self.write_loss:
            self.write_loss(step, loss_actor.item(), "loss_actor")
        loss_actor.backward()
        self.actor_optimizer.step()

        utils.soft_update(self.target_actor, self.actor, TAU)
        utils.soft_update(self.target_critic, self.critic, TAU)

    def get_models_path(self):
        return "./"

    def save_model(self, episode_count, model_save_path=None):
        """保存模型"""
        # torch.save(self.target_actor.state_dict(), './Models/' + str(episode_count) + '_actor.pt')
        if model_save_path is None:
            model_save_path = self.get_models_path()
        torch.save(self.target_actor.state_dict(), model_save_path + str(episode_count) + '_actor.pt')
        torch.save(self.target_critic.state_dict(), model_save_path + str(episode_count) + '_critic.pt')
        print("%s：%s Models saved successfully" % (datetime.datetime.now(), episode_count))
        # print("%s：轮数:%s 决策步数:%s  Reward:%.2f" % (datetime.now(), _ep, step, reward_now))

    def load_models(self, episode, model_save_path=None):
        """载入以前训练过的模型, 包括策略网络和价值网络"""
        if model_save_path is None:
            model_save_path = self.get_models_path()
        # self.critic.load_state_dict(torch.load(self.get_models_path() + str(episode) + '_critic.pt'))
        self.critic.load_state_dict(torch.load(model_save_path + str(episode) + '_critic.pt'))
        # self.actor.load_state_dict(torch.load(self.get_models_path() + str(episode) + '_actor.pt'))
        self.actor.load_state_dict(torch.load(model_save_path + str(episode) + '_actor.pt'))
        utils.hard_update(self.target_actor, self.actor)
        utils.hard_update(self.target_critic, self.critic)
        print("Models loaded successfully")
