#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name :trgrglrtime.py
# Create date : 2020-3-18
# Modified date : 2020-3-18
# Author : xy
# Describe : not set
# Email : yang_31296@163.com

from .trigger import CTrigger


class CTriggerRegularTime(CTrigger):
    """
    规则时间
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 名称
        self.strName = ''
        # 事件触发器描述
        self.strDescription = ''
        # 事件触发器类型
        self.m_EventTriggerType = 0
        # 触发器每几秒将会触发
        self.m_Interval = 0
