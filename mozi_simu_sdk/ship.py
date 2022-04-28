#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##########################################################################################################
# File name : ship.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################
# File name : ship.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################

from mozi_simu_sdk.activeunit import CActiveUnit


class CShip(CActiveUnit):
    """
    水面舰艇
    """

    # ----------------------------------------------------------------------
    def __init__(self, strGuid, mozi_server, situation):
        """飞机"""
        super().__init__(strGuid, mozi_server, situation)
        # 方位类型
        self.m_BearingType = 0
        # 方位
        self.m_Bearing = 0
        # 距离（转换为千米）
        self.m_Distance = 0
        # 高低速交替航行 
        self.bSprintAndDrift = False
        # 以下为 CShip 的属性
        # 类别
        self.m_Category = 0
        # 指挥部
        self.m_CommandPost = ''
        # 船舵
        self.m_Rudder = 0
        # 获取作战单元燃油信息
        # 显示燃油信息
        self.strFuelState = ''
        self.m_Type = 0  #
        # 空泡
        self.strCavitation = 0
        # 悬停
        self.fHoverSpeed = 0.0
        # 低速
        self.fLowSpeed = 0.0
        # 巡航
        self.fCruiseSpeed = 0.0
        # 军力
        self.fMilitarySpeed = 0.0
        # 加速
        self.fAddForceSpeed = 0.0
        # 载艇-信息
        # 毁伤
        self.strDamageInfo = 0
        # 武器
        self.strWeaponInfo = 0
        # 弹药库
        self.strMagazinesInfo = 0
        # 燃料
        self.strFuelInfo = 0
        # 状态
        self.strStatusInfo = 0
        # 就绪时间
        self.strTimeToReadyInfo = 0
        # 货物类型
        self.m_CargoType = None
        # 油门高度-航路点信息
        # 航路点名称至少一个航速指令为0公里/小时,不能估计剩余航行距离/时间/燃油量
        self.strWayPointName = 0
        self.bCanRefuelOrUNREP = 0
        # 补给队列header
        self.strShowTankerHeader = 0
        # 补给队列明显
        self.m_ShowTanker = 0
        self.ClassName = 'CShip'
