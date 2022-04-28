#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name :sideway.py
# Create date : 2020-3-18
# Modified date : 2020-3-18
# Author : xy
# Describe : not set
# Email : yang_31296@163.com
#from ..entitys.activeunit import CActiveUnit
from .activeunit import CActiveUnit


class CSideWay:
    """
    预设航线类
    """

    def __init__(self, strGuid, mozi_server, situation):
        # GUID
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 态势
        self.situation = situation
        # 名称
        self.strName = ''
        # 推演方的GUID
        self.m_Side = ''
        # 是否显示航线
        self.m_bShow = False
        # 航线类型
        self.m_eSideWayType = 0
        # 所有航路点的集合
        self.m_WayPoints = ''
