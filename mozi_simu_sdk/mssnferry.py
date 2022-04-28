#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name :mssnferry.py
# Create date : 2020-3-18
# Modified date : 2020-3-18
# Author : xy
# Describe : not set
# Email : yang_31296@163.com

from .mission import CMission


class CFerryMission(CMission):
    """
    转场任务
    """

    def __init__(self, strGuid, mozi_server, situation):  # changed by aie
        super().__init__(strGuid, mozi_server, situation)
        # 转场任务行为
        self.m_FerryMissionBehavior = ''
        # 转场飞机数量
        self.m_FlightSize = ''

    def set_ferry_behavior(self, ferry_behavior):
        """
        功能：设置转场规则
        参数：ferry_behavior: {str: OneWay--单程，Cycle--循环 ，Random--随机}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-7
        """
        cmd = "ScenEdit_SetMission('%s','%s', {ferryBehavior='%s'}) " % (self.m_Side, self.strGuid, ferry_behavior)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_ferry_throttle_aircraft(self, throttle):
        """
        功能：设置转场油门
        参数：throttle-油门: {str: Loiter-低速, Cruise：巡航, Full：军用 , Flank：加力}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        cmd = "ScenEdit_SetMission('%s','%s', {ferryThrottleAircraft='%s'}) " % (self.m_Side, self.strGuid, throttle)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_ferry_altitude_aircraft(self, altitude):
        """
        功能：设置转场高度
        参数：altitude: {float: 转场高度，单位米}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        cmd = "ScenEdit_SetMission('%s','%s', {ferryAltitudeAircraft=%s}) " % (self.m_Side, self.strGuid, altitude)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)
