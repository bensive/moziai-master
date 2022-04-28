#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name :mssnpatrol.py
# Create date : 2020-3-18
# Modified date : 2020-3-18
# Author : xy
# Describe : not set
# Email : yang_31296@163.com

from .mission import CMission


class CPatrolMission(CMission):
    """
    巡逻任务
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)

    @staticmethod
    def __get_zone_str(point_list):
        """
        功能：构造区域点集形成的字符串
        参数：point_list-参考点列表: {list: 例:[(40, 39.0), (41, 39.0), (41, 40.0), (40, 40.0)]，其中纬度值在前，经度值在后，(40, 39.0)中,
                                        latitude = 40, longitude = 39.0
                                        或者[(40, 39.0, 'RP1'), (41, 39.0, 'RP2'), (41, 40.0, 'RP3'), (40, 40.0, 'RP4')]
                                        或者['RP1', 'RP2'，'RP3'，'RP4']，传入参考点名称要求提前创建好参考点
        返回：区域点集形成的字符串
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        zone_str = ''
        if type(point_list[0]) == str:
            zone_str = "Zone={'%s'}" % ("','".join(point_list))
        elif type(point_list[0]) == tuple:
            if type(point_list[0][-1]) == str:
                t = [k[-1] for k in point_list]
                zone_str = "Zone={'%s'}" % ("','".join(t))
            else:
                t = ['latitude=%s,longitude=%s' % (k[0], k[1]) for k in point_list]
                zone_str = "Zone={{%s}}" % ("},{".join(t))
        return zone_str

    def set_prosecution_zone(self, point_list):
        """
        功能：设置巡逻任务的警戒区
        参数：point_list {list: 参考点名称列表}
            example: ['RP1', 'RP2'，'RP3'，'RP4']
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: 张志高 2021-8-24
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        area_str = str(point_list).replace('[', '').replace(']', '')
        lua_script = f"ScenEdit_SetMission('{self.m_Side}','{self.strName}',{{prosecutionZone={{{area_str}}}}})"
        self.mozi_server.throw_into_pool(lua_script)
        return self.mozi_server.send_and_recv(lua_script)

    def set_patrol_zone(self, point_list):
        """
        功能：设置巡逻任务的巡逻区
        参数：point_list {list: 参考点名称列表}
            example: ['RP1', 'RP2'，'RP3'，'RP4']
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: 张志高 2021-8-24
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        area_str = str(point_list).replace('[', '').replace(']', '')
        lua_script = f"ScenEdit_SetMission('{self.m_Side}','{self.strName}',{{patrolZone={{{area_str}}}}})"
        self.mozi_server.throw_into_pool(lua_script)
        return self.mozi_server.send_and_recv(lua_script)

    def set_maintain_unit_number(self, unit_number):
        """
        功能：巡逻任务阵位上每类平台保存作战单元数量
        参数：unit_number {int: 阵位上每类平台保存单元数量}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = 'ScenEdit_SetMission("%s","%s",{PatrolMaintainUnitNumber=%d})' % (
            self.m_Side, self.strName, unit_number)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_opa_check(self, is_check_opa):
        """
        功能：设置任务是否对巡逻区外的探测目标进行分析
        参数：is_check_opa {str: true-分析，false-不分析}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie 张志高-2021-8-24
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', { checkOPA = " + is_check_opa + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_emcon_usage(self, is_active_emcon):
        """
        功能：设置任务是否仅在巡逻/警戒区内打开电磁辐射
        参数：is_active_emcon {str: true-打开，false-不打开}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie 张志高-2021-8-24
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = "ScenEdit_SetMission('" + str(self.m_Side) + "', '" + str(
            self.strGuid) + "', { activeEMCON = " + str(is_active_emcon).lower() + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_wwr_check(self, is_check_wwr):
        """
        功能：设置任务是否对武器射程内探测目标进行分析
        参数：is_check_wwr {str: true-打开，false-不打开}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie 张志高-2021-8-24
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strGuid\
              + "', { checkWWR = " + str(is_check_wwr).lower() + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_flight_size(self, flight_size):
        """
        功能：设置任务编队规模
        参数：flight_size 编队规模 {str: 1-1机编队,
                            2-2机编队,
                            3-3机编队,
                            4-4机编队,
                            6-6机编队}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie 张志高-2021-8-24
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strGuid + "', { flightSize = " \
              + str(flight_size) + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_flight_size_check(self, use_flight_size_check):
        """
        功能：是否飞机数低于编队规模不允许起飞
        参数：use_flight_size_check 飞机数低于编队规模要求不能起飞 {str: true-是，false-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie 张志高-2021-8-24
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
        参数：throttle-油门: {str: Loiter-低速, Cruise-巡航, Full-军用 , Flank-加力}
        返回：'不在设值范围内，请重新设置。' 或 'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return super().set_throttle('transitThrottleAircraft', throttle)

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

    def set_throttle_attack(self, throttle):
        """
        功能：设置任务的攻击油门
        参数：throttle-油门: {str: Loiter-低速, Cruise：巡航, Full：军用 , Flank：加力}
        返回：'不在设值范围内，请重新设置。' 或 'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return super().set_throttle('attackThrottleAircraft', throttle)

    def set_throttle_attack_ship(self, throttle):
        """
        功能：设置任务的水面舰艇攻击油门
        参数：throttle-油门: {str: Loiter-低速, Cruise：巡航, Full：军用 , Flank：加力}
        返回：'不在设值范围内，请重新设置。' 或 'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return super().set_throttle('attackThrottleShip', throttle)

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

    def set_attack_altitude(self, altitude):
        """
        功能：设置任务的攻击高度
        参数：altitude-高度: {float: 单位：米，最多6位字符，例：99999.9， 888888}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return super().set_altitude('attackAltitudeAircraft', altitude)

    def set_attack_distance(self, distance):
        """
        功能：设置任务的攻击距离
        参数：distance: {float: 单位：海里}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('" + str(self.m_Side) + "','" + str(
            self.strGuid) + "', { attackDistanceAircraft = " + str(distance) + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_patrol_sonobuoys_cover(self, sonobuoys_cover, drop_sonobuoys_type):
        """
        功能：为反潜巡逻任务设置声呐浮标在巡逻区域内的覆盖密度和深浅类型。
        参数：sonobuoys_cover: 倍 {float: 覆盖密度（1-5之间的数，保留小数点后两位）}
            drop_sonobuoys_type 深度类型 {int: （0：随机、1：温跃层之上、2：温跃层之下）}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return self.mozi_server.send_and_recv(
            "Hs_SetPatrolSonobuoysCover('{}',{},{})".format(self.strGuid, sonobuoys_cover, drop_sonobuoys_type))

    def set_group_size(self, group_size):
        """
        功能：设置巡逻任务水面舰艇/潜艇编队规模
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
