#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name :mssncargo.py
# Create date : 2020-3-18
# Modified date : 2020-3-18
# Author : xy
# Describe : not set
# All rights reserved:北京华戍防务技术有限公司
# Email : yang_31296@163.com

from .mission import CMission


class CCargoMission(CMission):
    """
    投送任务
    """
    def __init__(self, strGuid, mozi_server, situation):  # changed by aie
        super().__init__(strGuid, mozi_server, situation)
        # 母舰平台
        self.m_Motherships = ''
        # 要卸载的货物
        self.m_MountsToUnload = ''

    def add_mount_to_unload(self, mount_db_guid):
        """
        功能：设置投送任务的货物加1。
        参数：mount_db_guid: {str: 货物的数据库guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-6
        """
        cmd = "ScenEdit_SetMission('" + str(self.m_Side) + "','" + str(
            self.strGuid) + "', { AddMountToUnload='" + mount_db_guid + "'})"
        return self.mozi_server.send_and_recv(cmd)

    def remove_mount_to_unload(self, mount_db_guid):
        """
        功能：设置投送任务的货物减1。
        参数：mount_db_guid: {str: 货物的数据库guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-6
        """
        cmd = "ScenEdit_SetMission('" + str(self.m_Side) + "','" + str(
            self.strGuid) + "', { RemoveMountToUnload='" + mount_db_guid + "'})"
        return self.mozi_server.send_and_recv(cmd)

    def set_zone(self, point_list):
        """
        功能：设置投放区域
        参数：point_list {list: 参考点名称列表}
            example: ['RP1', 'RP2'，'RP3'，'RP4']
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        area_str = str(point_list).replace('[', '').replace(']', '')
        lua_script = f"ScenEdit_SetMission('{self.m_Side}','{self.strName}',{{zone={{{area_str}}}}})"
        self.mozi_server.throw_into_pool(lua_script)
        return self.mozi_server.send_and_recv(lua_script)

    def set_throttle_transit(self, throttle):
        """
        功能：设置任务的出航油门
        参数：throttle-油门: {str: Loiter-低速, Cruise-巡航, Full-军用 , Flank-加力}
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

    def set_throttle_transit_ship(self, throttle):
        """
        功能：设置任务的水面舰艇出航油门
        参数：throttle-油门: {str: Loiter-低速, Cruise-巡航, Full-军用 , Flank-加力}
        返回：'不在设值范围内，请重新设置。' 或 'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return super().set_throttle('transitThrottleShip', throttle)

    def set_throttle_station_ship(self, throttle):
        """
        功能：设置任务的水面舰艇阵位油门
        参数：throttle-油门: {str: Loiter-低速, Cruise：巡航, Full：军用 , Flank：加力}
        返回：'不在设值范围内，请重新设置。' 或 'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return super().set_throttle('stationThrottleShip', throttle)
