#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name " trgunitdtcd.py
# Create date : 2020-3-18
# Modified date : 2020-4-11
# Author : xy
# Describe : not set
# Email : yang_31296@163.com

from .trigger import CTrigger


class CTriggerUnitDetected(CTrigger):
    """
    单元被探测到
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 名称
        self.strName = ''
        # 事件触发器描述
        self.strDescription = ''
        # 事件触发器类型
        self.m_EventTriggerType = 0
        # 目标推演方GUID
        self.strTargetSide = ''
        # 目标类型
        self.m_TargetType = 0
        # 目标子类型
        self.iTargetSubType = 0
        # 目标等级
        self.iSpecificUnitClass = 0
        # 特殊单元GUID
        self.m_SpecificUnit = ''
        # 探测器推演方GUID
        self.strDetectorSideID = ''
        # 最小等级分类
        self.m_identificationStatus = 0
