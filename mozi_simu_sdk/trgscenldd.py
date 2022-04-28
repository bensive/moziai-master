#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name :trgscenldd.py
# Create date : 2020-3-18
# Modified date : 2020-3-18
# Author : xy
# Describe : not set
# Email : yang_31296@163.com

from .trigger import CTrigger


class CTriggerScenLoaded(CTrigger):
    """
    想定已经加载
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 名称
        self.strName = ''
        # 事件触发器描述
        self.strDescription = ''
        # 事件触发器类型
        self.m_EventTriggerType = 0
