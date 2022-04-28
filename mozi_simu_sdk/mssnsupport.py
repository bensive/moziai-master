#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name :mssnsupport.py
# Create date : 2020-3-18
# Modified date : 2020-3-18
# Author : xy
# Describe : not set
# Email : yang_31296@163.com

from .mission import CMission


class CSupportMission(CMission):
    """
    支援任务
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)

    def set_maintain_unit_number(self, support_maintain_count):
        """
        功能：阵位上每类平台保持几个作战单元
        参数：support_maintain_count {int: 保持阵位的数量}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = 'ScenEdit_SetMission("' + self.m_Side + '","' + self.strName + '",{SupportMaintainUN=' + str(
                support_maintain_count) + '})'
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_one_time_only(self, is_one_time_only):
        """
        功能：设置仅一次
        参数：is_one_time_only 是否仅一次 {str: true-是，false-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = 'ScenEdit_SetMission("' + self.m_Side + '","' + self.strName + '", {oneTimeOnly=' + str(
                is_one_time_only).lower() + '})'
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_emcon_usage(self, is_active_emcon):
        """
        功能：仅在阵位上打开电磁辐射
        参数：is_active_emcon 是否仅在阵位上打开电磁辐射 {str: true-是，false-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = 'ScenEdit_SetMission("' + self.m_Side + '","' + self.strName + '", {activeEMCON =' + str(
                is_active_emcon).lower() + '})'
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_loop_type(self, loop_type):
        """
        功能：导航类型 接口暂不可用
        参数：is_loop_type 导航类型 {str: onceRepeat-仅一次；continuation-连续循环}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = 'ScenEdit_SetMission("' + self.m_Side + '","' + self.strName + '", {loopType ="' + loop_type + '"})'
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_flight_size(self, flight_size):
        """
        功能：设置打击任务编队规模
            flight_size 编队规模 {str: 1-单机, 2-2机编队, 3-3机编队, 4-4机编队, 6-6机编队}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = 'ScenEdit_SetMission("' + self.m_Side + '","' + self.strName + '",{flightSize=' + str(
                flight_size) + '})'
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_flight_size_check(self, use_flight_size_check):
        """
        功能：是否飞机数低于编队规模不允许起飞
        参数：use_flight_size_check 飞机数低于编队规模要求不能起飞 {str: true-是，false-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie 张志高-2021-8-25
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = 'ScenEdit_SetMission("' + self.m_Side + '","' + self.strGuid + '", {''useFlightSize =' + str(
            use_flight_size_check).lower() + '})'
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_throttle_transit(self, throttle):
        """
        功能：设置任务的出航油门
        参数：throttle-油门: {str: Loiter-低速, Cruise：巡航, Full：军用 , Flank：加力}
        返回：'不在设值范围内，请重新设置。' 或 'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return super().set_throttle('transitThrottleAircraft', throttle)

    def set_throttle_station(self, throttle):
        """
        功能：设置任务的阵位油门
        参数：throttle-油门: {str: Loiter-低速, Cruise：巡航, Full：军用 , Flank：加力}
        返回：'不在设值范围内，请重新设置。' 或 'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return super().set_throttle('stationThrottleAircraft', throttle)

    def set_transit_altitude(self, altitude):
        """
        功能：设置任务的出航高度
        参数：altitude-高度: {float: 单位：米，最多6位字符，例：99999.9， 888888}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return super().set_altitude('transitAltitudeAircraft', altitude)

    def set_station_altitude(self, altitude):
        """
        功能：设置任务的阵位高度
        参数：altitude-高度: {float: 单位：米，最多6位字符，例：99999.9， 888888}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return super().set_altitude('stationAltitudeAircraft', altitude)

    def set_emcon_usage(self, is_active_emcon):
        """
        功能：设置任务是否在阵位上打开电磁辐射
        参数：is_active_emcon {str: true-打开，false-不打开}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        cmd = "ScenEdit_SetMission('" + str(self.m_Side) + "', '" + str(
            self.strGuid) + "', { activeEMCON = " + str(is_active_emcon).lower() + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_throttle_transit_ship(self, throttle):
        """
        功能：设置任务的水面舰艇出航油门
        参数：throttle-油门: {str: Loiter-低速, Cruise-巡航, Full-军用 , Flank-加力}
        返回：'不在设值范围内，请重新设置。' 或 'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        return super().set_throttle('transitThrottleShip', throttle)

    def set_throttle_station_ship(self, throttle):
        """
        功能：设置任务的水面舰艇阵位油门
        参数：throttle-油门: {str: Loiter-低速, Cruise：巡航, Full：军用 , Flank：加力}
        返回：'不在设值范围内，请重新设置。' 或 'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        return super().set_throttle('stationThrottleShip', throttle)

    def set_group_size(self, group_size):
        """
        功能：设置任务水面舰艇/潜艇编队规模
        参数：group_size 编队规模 {int: 1-单艇, 2-2x艇, 3-3x艇, 4-4x艇, 6-6x艇}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {groupSize=" + str(
            group_size) + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_throttle_transit_submarine(self, throttle):
        """
        功能：设置任务的潜艇出航油门
        参数：throttle-油门: {str: Loiter-低速, Cruise-巡航, Full-军用 , Flank-加力}
        返回：'不在设值范围内，请重新设置。' 或 'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        return super().set_throttle('transitThrottleSubmarine', throttle)

    def set_throttle_station_submarine(self, throttle):
        """
        功能：设置任务的潜艇阵位油门
        参数：throttle-油门: {str: Loiter-低速, Cruise：巡航, Full：军用 , Flank：加力}
        返回：'不在设值范围内，请重新设置。' 或 'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        return super().set_throttle('stationThrottleSubmarine', throttle)


