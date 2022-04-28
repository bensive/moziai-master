# -*- coding:utf-8 -*-
##########################################################################################################
# File name : satellite.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################

from .activeunit import CActiveUnit


class CSatellite(CActiveUnit):
    """
    卫星类
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 卫星类别
        self.m_SatelliteCategory = None
        # 卫星航迹线 航迹是根据卫星算法得出的
        self.m_TracksPoints = None
        self.ClassName = 'CSatellite'

