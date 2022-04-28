# -*- coding:utf-8 -*-
##########################################################################################################
# File name : CReferencePoint.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################


class CReferencePoint:
    """
    参考点
    """

    def __init__(self, strGuid, mozi_server, situation):
        # GUID
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 态势
        self.situation = situation
        # 类名
        self.ClassName = ""
        # 名称
        self.strName = ''
        # 方
        self.m_Side = ''
        # 经度
        self.dLongitude = 0.0
        # 纬度
        self.dLatitude = 0.0
        # 高度
        self.fAltitude = 0.0
        # 相对单元guid
        self.m_RelativeToUnit = ""
        # 相对方位角
        self.fRelativeBearing = 0.0
        # 相对距离
        self.fRelativeDistance = 0.0
        # 方向类型
        # 0 固定的，不随领队朝向变化而变化
        # 1 旋转的，随领队朝向改变旋转
        self.m_BearingType = 0
        # 是否锁定
        self.bIsLocked = False
