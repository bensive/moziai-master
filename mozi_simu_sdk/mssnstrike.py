#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name :mssnstrike.py
# Create date : 2020-3-18
# Modified date : 2020-3-18
# Author : xy
# Describe : not set
# Email : yang_31296@163.com


from .mission import CMission


class CStrikeMission(CMission):
    """
    打击任务
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        self.strName = None
        self.m_Category = None
        self.m_MissionClass = None
        self.m_StartTime = None
        self.m_EndTime = None
        self.m_MissionStatus = None
        self.m_AssignedUnits = None
        self.m_UnassignedUnits = None
        self.m_StrikeType = None
        self.m_MinimumContactStanceToTrigger = None
        self.m_FlightSize = None
        self.m_Bingo = None
        self.m_MinAircraftReq_Strikers = None
        self.iMinResponseRadius = None
        self.iMaxResponseRadius = None
        self.m_RadarBehaviour = None
        self.bUseRefuel = None
        self.m_UseRefuel = None
        self.bUseFlightSizeHardLimit = None
        self.bUseAutoPlanner = None
        self.bOneTimeOnly = None
        self.m_GroupSize = None
        self.bUseGroupSizeHardLimit = None
        self.bPrePlannedOnly = None
        self.m_Doctrine = None
        self.m_SpecificTargets = None
        self.m_strSideWayGUID = None
        self.m_strSideWeaponWayGUID = None
        self.m_EscortFlightSize = None
        self.m_MinAircraftReqEscorts = None
        self.m_MaxAircraftToFlyEscort = None
        self.iEscortResponseRadius = None
        self.m_EscortFlightSizeNo = None
        self.m_MinAircraftReqEscortsNo = None
        self.m_MaxAircraftToFlyEscortNo = None
        self.bUseFlightSizeHardLimitEscort = None
        self.m_EscortGroupSize = None
        self.bUseGroupSizeHardLimitEscort = None
        self.m_Doctrine_Escorts = None
        self.m_strContactWeaponWayGuid = None
        self.iEmptySlots = None

    def get_targets(self):
        """
        功能：返回任务打击目标
        参数：无
        返回：目标单元组成的词典 {key: 探测目标guid, value: 探测目标对象}
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/11/20
        """
        target_guids = self.m_SpecificTargets.split('@')
        targets = {k: v for k, v in self.situation.side_dic[self.m_Side].contacts.items() if k in target_guids}
        return targets

    def assign_unit_as_target(self, target_name_or_guid):
        """
        功能：分配目标
        参数：target_name_or_guid: {str: 目标名称或guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：张志高 2021-8-25
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = f"ScenEdit_AssignUnitAsTarget({{'{target_name_or_guid}'}}, '{self.strName}')"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def remove_target(self, target_name_or_guid):
        """
        功能：删除打击任务目标
        参数：target_name_or_guid: {str: 目标名称或guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：张志高 2021-8-25
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = f"ScenEdit_RemoveUnitAsTarget('{target_name_or_guid}', '{self.strName}')"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_preplan(self, b_preplan):
        """
        功能：设置任务细节：是否仅考虑计划目标（在目标清单）
        参数：b_preplan: 是否仅考虑计划目标 {bool: True-是，False-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {strikePreplan = " + str(
            b_preplan).lower() + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_minimum_trigger(self, strike_minimum_trigger):
        """
        功能：设置打击任务触发条件, 探测目标至少为不明、非友、敌对
        参数：strike_minimum_trigger: 任务触发，如果探测目标至少为 {int: 1-空, 2-非友方, 3-敌对方, 4-不明}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {StrikeMinimumTrigger = " + str(
            strike_minimum_trigger) + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_strike_max(self, strike_max):
        """
        功能：设置任务细节：任务允许出动的最大飞行批次
        参数：strike_max: 任务所需的最低飞机数 {str: 0-无偏好、1-1机编队、2-2机编队、3-3机编队、4-4机编队、
                                                6-6机编队、8-8机编队、12-12机编队}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {strikeMax = '" + str(
            strike_max) + "'})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_min_aircrafts_required(self, min_aircraft_req):
        """
        功能：设置打击任务所需最少就绪飞机数
            min_aircraft_req 编队规模 {str: 0-无偏好、1-1编队、2-2编队、3-3编队、4-4编队、
                                                6-6编队、8-8编队、12-12编队、all-所有编队}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {strikeMinAircraftReq = '" + str(
            min_aircraft_req) + "'})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_flight_size(self, flight_size):
        """
        功能：设置打击任务编队规模
        参数：flight_size 编队规模 {str: 1-单机, 2-2机编队, 3-3机编队, 4-4机编队, 6-6机编队}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {strikeFlightSize = '" + str(
            flight_size) + "'})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_radar_usage(self, radar_usage):
        """
        功能：设置打击任务雷达运用规则
        参数：radar_usage 编队规模 {int: 1：整个飞行计划遵循任务电磁管控规则，
                                    2：从初始点到武器消耗光打开雷达，
                                    3：从进入攻击航线段到武器消耗完毕状态点打开雷达}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie, 张志高：2021-8-25
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', { strikeRadarUasge = " + str(
            radar_usage) + "} )"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_fuel_ammo(self, fuel_ammo):
        """
        功能：设置打击任务燃油弹药规则
        参数：fuel_ammo 燃油弹药规则 {int: 0-根据每个挂载方案的设置决定是消耗/抛弃还是带回空地弹药，
                                        1-在最远距离上抛弃空对地弹药，以获取最大打击，
                                        2-如果不能打击目标，则带回空对地弹药}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {StrikeFuleAmmo = " + str(
            fuel_ammo) + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_min_strike_radius(self, min_distance):
        """
        功能：设置打击任务最小打击半径
        参数：min_distance {float: 最小打击半径，单位：海里}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {StrikeMinDist=" + str(
            min_distance) + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_max_strike_radius(self, max_distance):
        """
        功能：设置打击任务最大打击半径
        参数：max_distance {float: 最大打击半径。 单位：海里}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {StrikeMaxDist=" + str(
            max_distance) + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_flight_size_check(self, use_flight_size_check):
        """
        功能：设置打击任务是否飞机数低于编组规模数要求就不能起飞
        参数：use_flight_size_check 飞机数低于编队规模要求不能起飞 {str: true-是，false-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie 张志高-2021-8-25
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = 'ScenEdit_SetMission("' + self.m_Side + '","' + self.strGuid + '", {''strikeUseFlightSize =' + str(
            use_flight_size_check).lower() + '})'
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_auto_planner(self, use_auto_planner):
        """
        功能：设置打击任务是否离轴攻击
        参数：use_auto_planner 是否多扇面攻击 {str: true-是，false-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {StrikeUseAutoPlanner = " + str(
            use_auto_planner).lower() + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_strike_one_time_only(self, one_time_only):
        """
        功能：设置打击任务是否仅限一次
        参数：one_time_only 是否仅限一次 {str: true-是，false-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {strikeOneTimeOnly = " + str(
            one_time_only) + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_strike_escort_flight_size_shooter(self, flight_size):
        """
        功能：设置打击任务护航飞机编队规模
        参数：flight_size 编队规模 {int: 1-单机, 2-2机编队, 3-3机编队, 4-4机编队, 6-6机编队}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {escortFlightSizeShooter=" + str(
            flight_size) + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_strike_escort_response_radius(self, escort_response_radius):
        """
        功能：设置打击任务护航最大威胁响应半径
        参数：escort_response_radius {float: 最大威胁响应半径，单位海里}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {escortResponseRadius=" + str(
            escort_response_radius) + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_strike_group_size(self, group_size):
        """
        功能：设置打击任务水面舰艇/潜艇编队规模
        参数：group_size 编队规模 {int: 1-单艇, 2-2x艇, 3-3x艇, 4-4x艇, 6-6x艇}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-8
        """
        cmd = "ScenEdit_SetMission('" + self.m_Side + "', '" + self.strName + "', {strikeGroupSize=" + str(
            group_size) + "})"
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)
