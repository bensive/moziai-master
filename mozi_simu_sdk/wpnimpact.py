#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name " wpnimpact.py
# Create date : 2020-3-18
# Modified date : 2020-3-18
# Author : xy
# Describe : not set
# Email : yang_31296@163.com


class CWeaponImpact:
    """
    武器碰撞
    """

    def __init__(self, strGuid, mozi_server, situation):
        # guid
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 态势
        self.situation = situation
        # 名称
        self.strName = ''

        # 爆炸经度
        self.dLatitude = ''
        # 爆炸纬度
        self.dLongitude = ''
        # 海拔高度
        self.iAltitude_ASL = ''
        # 碰撞类型
        self.m_ImpactType = ''
