#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name :cndscenhsstrtd.py
# Create date : 2020-3-18
# Modified date : 2020-4-11
# Author : xy
# Describe : not set
# Email : lzygzh@126.com

from .condition import CCondition


class CConditionScenHasStarted(CCondition):
    """
    判定想定启动的事件条件
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 名称
        self.strName = ''
        # 事件条件描述
        self.strDescription = ''
        # 事件条件类型
        self.m_EventConditionType = 0
        # 反选
        self.bModifier = False
