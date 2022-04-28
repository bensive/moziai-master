#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : actionendscnr.py
# Create date : 2020-3-18
# Modified date : 2020-4-11
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

from .action import CAction


class CActionEndScenario(CAction):
    """
    终止想定的事件动作类
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 名称
        self.strName = ''
        # 事件动作描述
        self.strDescription = ''
        # 事件动作类型
        self.m_EventActionType = 0
        self.ClassName = 'CActionEndScenario'
