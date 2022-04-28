#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : actionchngms.py
# Create date : 2020-3-18
# Modified date : 2020-4-11
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

from .action import CAction


class CActionChangeMissionStatus(CAction):
    """
    改变任务状态的事件动作类
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 名称
        self.strName = ''
        # 事件动作描述
        self.strDescription = ''
        # 事件动作类型
        self.m_EventActionType = ''
        # 推演方GUID
        self.m_strSideID = ''
        # 任务GUID
        self.strMissionID = ''
        # 是否启动
        self.m_newmissionStatus = 0
        self.ClassName = 'CActionChangeMissionStatus'
