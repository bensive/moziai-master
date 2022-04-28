#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name :trgpoints.py
# Create date : 2020-3-18self.
# Modified date : 2020-4-11
# Author : xy
# Describe : not set
# Email : yang_31296@163.com

from .trigger import CTrigger


class CTriggerPoints(CTrigger):
    """
    推演方得分
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 名称
        self.strName = ''
        # 事件触发器描述
        self.strDescription = ''
        # 事件触发器类型
        self.m_EventTriggerType = 0
        # 推演方的GUID
        self.m_strSideID = ''
        # 得分类型
        self.m_reachDirection = 0
        # 得分
        self.iPointValue = 0
