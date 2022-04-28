# -*- coding:utf-8 -*-
##########################################################################################################
# File name : weather.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################


class CWeather:
    """天气"""

    def __init__(self, mozi_server, situation):
        # 态势
        self.situation = situation
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 类的名字
        self.ClassName = ""
        # 天气-云
        self.fSkyCloud = 0.0
        # 天气-下雨概率
        self.fRainFallRate = 0.0
        # 天气-温度
        self.dTemperature = 0.0
        # 天气-海上天气情况
        self.iSeaState = 0
