#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : base_agent.py
# Create date : 2020-03-22 23:43
# Modified date : 2020-04-03 09:43
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class BaseAgent(object):
    """A base agent to write custom scripted agents.

  It can also act as a passive agent that does nothing but no-ops.
  """

    def __init__(self):
        # 奖赏值
        self.reward = 0
        # 幕数
        self.episodes = 0
        # 步数
        self.steps = 0
        # 状态空间
        self.obs_spec = None
        # 动作空间
        self.action_spec = None

    def setup(self, obs_spec, action_spec):
        self.obs_spec = obs_spec
        self.action_spec = action_spec

    def reset(self):
        self.episodes += 1

    def step(self, obs):
        self.steps += 1
