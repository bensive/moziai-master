#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : actionpnts.py
# Create date : 2020-3-18
# Modified date : 2020-4-11
# Author : xy
# Describe : not set
# Email : lzygzh@126.com
#####################################

from .action import CAction


class CActionPoints(CAction):
    """
    设置得分的事件动作类
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 名称
        self.strName = ''
        # 事件动作描述
        self.strDescription = ''
        # 事件动作类型
        self.m_EventActionType = 0
        # 推演方GUID
        self.m_strSideID = ''
        # 变化评分
        self.iPointChange = 0
