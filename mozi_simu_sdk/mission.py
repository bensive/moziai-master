# -*- coding:utf-8 -*-
##########################################################################################################
# File name : mission.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################


class CMission:
    """任务"""

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
        # 推演方
        self.m_Side = ''
        # 推演方名称
        self.side_name = ""
        # 任务类别
        self.m_Category = 0
        # 任务类型
        self.m_MissionClass = 0
        # 任务状态
        self.m_MissionStatus = 0
        # 飞机设置-编队规模
        self.m_FlightSize = 0
        # 空中加油任务设置-任务执行设置 -加油机遵循受油机的飞行计划是否选中
        self.bTankerFollowsReceivers = False
        # 任务描述
        self.strDescription = ""
        # 空中加油任务设置-任务规划设置 加油机没到位的情况下启动任务
        self.bLaunchMissionWithoutTankersInPlace = False
        # 水面舰艇/潜艇设置-水面舰艇/潜艇树低于编队规模要求,不能出击(根据基地编组)
        self.bUseGroupSizeHardLimit = False
        # 已分配单元的集合
        self.m_AssignedUnits = ""
        # 空中加油任务设置-任务执行设置 - 每架加油机允许加油队列最大长度
        self.strMaxReceiversInQueuePerTanker_Airborne = ""
        # 水面舰艇/潜艇设置-编队规模
        self.m_GroupSize = 0
        # 空中加油-  点击配置  显示如下两个选项： 返回选中的值1.使用优良充足的最近加油机加油2.使用已分配特定任务的加油机加油
        self.m_TankerUsage = 0
        # 条令
        self.m_Doctrine = ""
        # 空中加油任务设置-任务规划设置 阵位上加油机最小数量
        self.strTankerMinNumber_Station = ""
        # 未分配单元的集合
        self.m_UnassignedUnits = ""
        # 单元航线
        self.m_strSideWayGUID = ""
        # 空中加油任务设置-任务执行设置 -受油机寻找加油机的时机条件
        self.strFuelQtyToStartLookingForTanker_Airborne = ""
        # 空中加油选项是否与上级保持一致
        self.bUseRefuel = False
        # 飞机数低于编队规模要求,不能起飞
        self.bUseFlightSizeHardLimit = False
        # 飞机设置-空中加油
        self.m_UseRefuel = 0
        # 行动预案
        self.bUseActionPlan = False
        # 空中加油任务设置-任务规划设置 留空的加油机最小数量
        self.strTankerMinNumber_Airborne = ""
        # 空中加油任务设置-任务规划设置1.需要加油机的最小数量
        self.strTankerMinNumber_Total = ""
        self.m_TransitThrottle_Aircraft = ''  # 飞机航速与高度-出航油门
        self.m_StationThrottle_Aircraft = ''  # 飞机航速与高度-阵位油门
        self.strTransitAltitude_Aircraft = ''  # 飞机航速与高度-出航高度
        self.strStationAltitude_Aircraft = ''  # 飞机航速与高度-阵位高度
        self.m_TransitThrottle_Submarine = ''  # 潜艇航速与潜深-出航油门
        self.m_StationThrottle_Submarine = ''  # 潜艇航速与潜深-阵位油门
        self.strTransitDepth_Submarine = ''  # 潜艇航速与潜深-出航潜深
        self.strStationDepth_Submarine = ''  # 潜艇航速与潜深-阵位潜深
        self.m_TransitThrottle_Ship = ''  # 水面舰艇航速-出航油门
        self.m_StationThrottle_Ship = ''  # 水面舰艇航速-阵位油门

    def get_assigned_units(self):
        """
        功能：获取已分配任务的单元
        参数：无
        返回：dict: key为单元guid, value为单元对象
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        guid_list = self.m_AssignedUnits.split('@')
        units = {}
        for guid in guid_list:
            units[guid] = self.situation.get_obj_by_guid(guid)
        return units

    def get_unassigned_units(self):
        """
        功能：获取未分配任务的单元
        参数：无
        返回：dict: key为单元guid, value为单元对象
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        guid_list = self.m_UnassignedUnits.split('@')
        units = {}
        for guid in guid_list:
            units[guid] = self.situation.get_obj_by_guid(guid)
        return units

    def get_doctrine(self):
        """
        功能：获取条令
        参数：无
        返回：条令对象
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        if self.m_Doctrine in self.situation.doctrine_dic:
            doctrine = self.situation.doctrine_dic[self.m_Doctrine]
            doctrine.category = 'Mission'  # 需求来源：20200331-2/2:Xy
            return doctrine
        return None

    def get_weapon_db_guids(self):
        """
        功能：获取编组内所有武器的数据库guid
        参数：无
        返回：编组内所有武器的guid组成的列表
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        张志高修改于2021-8-18
        """
        side = self.situation.side_dic[self.m_Side]
        unit_guids = self.m_AssignedUnits.split('@')
        # 考虑了编组作为执行单位时的情况。
        groups = self.situation.side_dic[self.m_Side].groups
        assigned_groups = {k: v for k, v in groups.items() if k in unit_guids}
        lst = []
        if len(assigned_groups) > 0:
            gg = [k.get_weapon_db_guids() for k in assigned_groups.values()]
            for n in gg:
                lst.extend(n)
        assigned_units_guids = [k for k in unit_guids if k not in groups.keys()]
        weapon_record = []
        lst02 = []
        if len(assigned_units_guids) > 0:
            weapon_record.extend(
                list({v.m_UnitWeapons: k for k, v in side.submarines.items() if k in assigned_units_guids}))
            weapon_record.extend(
                list({v.m_UnitWeapons: k for k, v in side.ships.items() if k in assigned_units_guids}))
            weapon_record.extend(
                list({v.m_UnitWeapons: k for k, v in side.facilities.items() if k in assigned_units_guids}))
            weapon_record.extend(
                list({v.m_UnitWeapons: k for k, v in side.aircrafts.items() if k in assigned_units_guids}))
            weapon_record.extend(
                list({v.m_UnitWeapons: k for k, v in side.satellites.items() if k in assigned_units_guids}))
            for unit_weapon_record in weapon_record:
                if unit_weapon_record:
                    lst01 = unit_weapon_record.split('@')
                    lst02.extend([k.split('$')[1] for k in lst01])
        lst.extend(lst02)
        return lst

    def get_weapon_infos(self):
        """
        功能：获取编组内所有武器的名称及db_guid
        参数：无
        返回：编组内所有武器的名称及db_guid组成的列表
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        side = self.situation.side_dic[self.m_Side]
        unit_guids = self.m_AssignedUnits.split('@')
        # 考虑了编组作为执行单位时的情况。
        groups = self.situation.side_dic[self.m_Side].groups
        assigned_groups = {k: v for k, v in groups.items() if k in unit_guids}
        lst = []
        if len(assigned_groups) > 0:
            gg = [k.get_weapon_infos() for k in assigned_groups.values()]
            for n in gg:
                lst.extend(n)
        assigned_units_guids = [k for k in unit_guids if k not in groups.keys()]
        weapon_record = []
        lst04 = []
        if len(assigned_units_guids) > 0:
            weapon_record.extend(
                list({v.m_UnitWeapons: k for k, v in side.submarines.items() if k in assigned_units_guids}))
            weapon_record.extend(
                list({v.m_UnitWeapons: k for k, v in side.ships.items() if k in assigned_units_guids}))
            weapon_record.extend(
                list({v.m_UnitWeapons: k for k, v in side.facilities.items() if k in assigned_units_guids}))
            weapon_record.extend(
                list({v.m_UnitWeapons: k for k, v in side.aircrafts.items() if k in assigned_units_guids}))
            weapon_record.extend(
                list({v.m_UnitWeapons: k for k, v in side.satellites.items() if k in assigned_units_guids}))
            for unit_weapon_record in weapon_record:
                if unit_weapon_record:
                    lst01 = unit_weapon_record.split('@')
                    lst04.extend([k.split('$') for k in lst01])
        lst.extend(lst04)
        return lst

    def get_side(self):
        """
        功能：获取任务所在方
        参数：无
        返回：任务所在方对象
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        return self.situation.side_dic[self.m_Side]

    def set_is_active(self, is_active):
        """
        功能：设置是否启用任务
        参数：is_active 是否启用 {str: true -是， false - 否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: 张志高 2021-8-23
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        str_set = str(is_active).lower()
        lua = "ScenEdit_SetMission('%s','%s',{isactive='%s'})" % (self.m_Side, self.strName, str_set)
        return self.mozi_server.send_and_recv(lua)

    def set_start_time(self, start_time):
        """
        功能：设置任务开始时间
        参数：start_time {str: 格式 '2020-04-16 22:10:00'}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd_str = "ScenEdit_SetMission('" + self.m_Side + "','" + self.strName + "',{starttime='" + start_time + "'})"
        return self.mozi_server.send_and_recv(cmd_str)

    def set_end_time(self, end_time):
        """
        功能：设置任务结束时间
        参数：end_time {str: 格式 '2020-04-16 22:10:00'}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd_str = "ScenEdit_SetMission('" + self.m_Side + "','" + self.strName + "',{endtime='" + end_time + "'})"
        return self.mozi_server.send_and_recv(cmd_str)

    def set_one_third_rule(self, is_one_third):
        """
        功能：设置任务是否遵循1/3原则
        参数：is_one_third 是否遵循1/3原则 {str: true -是， false - 否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = 'ScenEdit_SetMission("%s","%s", {oneThirdRule=%s})' % \
              (self.m_Side, self.strName, str(is_one_third).lower())
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def switch_radar(self, switch_on):
        """
        功能：设置任务雷达是否打开
        参数：switch_on 雷达打开或者静默 {bool: True - 打开， False - 不打开}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        if switch_on:
            set_str = 'Radar=Active'
        else:
            set_str = 'Radar=Passive'
        return self.situation.side_dic[self.m_Side].set_ecom_status("Mission", self.strName, set_str)  # amended by aie

    def assign_unit(self, unit_guid, is_escort=False):
        """
        功能：分配单元
        参数：
            unit_guid {str: 单元guid}
            is_escort 是否护航任务 {bool: True-是，False-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: 张志高 2021-8-23
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd_str = "ScenEdit_AssignUnitToMission('" + unit_guid + "', '" + self.strName + "', " + str(
            is_escort).lower() + ")"
        return self.mozi_server.send_and_recv(cmd_str)

    def assign_units(self, units):
        """
        功能：分配多个单元
        参数：units {dict: key-单元guid, value-单元对象}
        返回：'lua执行成功' 或 '脚本执行出错' 组成的字符串
            example: lua执行成功,lua执行成功,脚本执行出错
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        results = ''
        for k, v in units.items():
            cmd = "ScenEdit_AssignUnitToMission('{}', '{}')".format(v.strGuid, self.strName)
            self.mozi_server.throw_into_pool(cmd)
            ret = self.mozi_server.send_and_recv(cmd)
            results = results + ',' + ret
        return results

    def is_area_valid(self):
        """
        功能：验证区域角点连线是否存在交叉现象
        参数：无
        返回：验证结果状态标识（'Yes'：正常，'No'：异常）
        作者：-
        修改: 张志高 2021-8-24
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        lua_script = "print(Hs_IsValidArea('%s'))" % self.strName
        return self.mozi_server.send_and_recv(lua_script).replace("'", '')

    def unassign_unit(self, active_unit_name_guid):
        """
        功能：单元从任务中移除
        参数：active_unit_name_guid {str: 活动单元guid或名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: 张志高 2021-8-24
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        lua_script = "ScenEdit_UnAssignUnitFromMission('%s','%s')" % (active_unit_name_guid, self.strName)
        return self.mozi_server.send_and_recv(lua_script)

    def set_throttle(self, throttle_type, throttle):
        """
        功能：设置任务油门类型及值
        参数：throttle_type-油门类型: {str: 'transitThrottleAircraft'-飞机出航油门,
                                  'stationThrottleAircraft'-飞机阵位油门,
                                  'attackThrottleAircraft'-飞机攻击油门,
                                  'transitThrottleShip'-水面舰艇出航油门,
                                  'stationThrottleShip'-水面舰艇阵位油门,
                                  'attackThrottleShip'-水面舰艇攻击油门,
                                  'transitThrottleSubmarine'-潜艇出航油门,
                                  'stationThrottleSubmarine'-潜艇阵位油门}
             throttle-油门: {str: Loiter-低速, Cruise：巡航, Full：军用 , Flank：加力}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        修改: 张志高 2021-8-24
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('%s','%s', {%s = '%s'}) " % (self.m_Side, self.strGuid, throttle_type, throttle)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_speed(self, speed_type, speed):
        """
        功能：设置任务速度类型及值
        参数：speed_type-速度类型: {str: 'transitSpeedAircraft'-飞机出航速度,
                                  'stationSpeedAircraft'-飞机阵位速度,
                                  'attackSpeedAircraft'-飞机攻击速度,
                                  'transitSpeedShip'-水面舰艇出航速度,
                                  'stationSpeedShip'-水面舰艇阵位速度,
                                  'attackSpeedShip'-水面舰艇攻击速度,
                                  'transitSpeedSubmarine'-潜艇出航速度,
                                  'stationSpeedSubmarine'-潜艇阵位速度,
                                  'attackSpeedSubmarine'-水面舰艇攻击速度,}
             speed-速度: {float: 速度, 单位海里}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者: 张志高
        单位：北京华戍防务技术有限公司
        时间：2021-10-23
        """
        cmd = "ScenEdit_SetMission('%s','%s', {%s=%s}) " % (self.m_Side, self.strGuid, speed_type, speed)
        return self.mozi_server.send_and_recv(cmd)

    def set_altitude(self, altitude_type, altitude):
        """
        功能：设置任务高度类型及值
        参数：altitude_type-高度类型: {str: 'transitAltitudeAircraft'-出航高度,
                                         'stationAltitudeAircraft'-阵位高度,
                                         'attackAltitudeAircraft'-攻击高度}
             altitude-高度值: {float: 单位：米，最多6位字符，例：99999.9， 888888}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        cmd = "ScenEdit_SetMission('%s','%s', {%s=%s})"%(self.m_Side, self.strGuid, altitude_type, altitude)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def add_plan_way_to_mission(self, way_type, way_name_or_id):
        """
        功能：为任务分配预设航线
        参数：way_type-航线类型: {int: 0-单元出航航线，1-武器航线, 2-返航航线，3-巡逻航线}
             way_name_or_id: {str: 航线名称或guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: 张志高 2021-8-24
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return self.mozi_server.send_and_recv("Hs_AddPlanWayToMission('%s',%d,'%s')"
                                              % (self.strName, way_type, way_name_or_id))

    def add_plan_way_to_target(self, way_name_or_id, target_name_or_id):
        """
        功能：武器打击目标预设航线
        参数：
             way_name_or_id {str: 武器航线名称或guid}
             target_name_or_id {str: 目标名称或guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改: 张志高 2021-8-24
        单位：北京华戍防务技术有限公司
        时间：4/10/20
        """
        return self.mozi_server.send_and_recv(
            "Hs_AddPlanWayToMissionTarget('{}','{}','{}')".format(self.strName, way_name_or_id,
                                                                  target_name_or_id))

    def set_use_refuel_unrep(self, use_refuel_unrep):
        """
        功能：设置空中加油
        参数：use_refuel_unrep: {int: 0--允许但不允许给加油机加油，1--不允许，2--允许}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-7
        """
        cmd = "ScenEdit_SetMission('%s','%s', {use_refuel_unrep=%s})" % (self.m_Side, self.strGuid, use_refuel_unrep)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_submarine_depth(self, depth_type, depth):
        """
        功能：设置潜艇潜深 - 仅支持扫雷、布雷、支援和巡逻任务
        参数：depth_type: {str: transitDepthSubmarine--出航潜深，stationDepthSubmarine--阵位潜深}
            depth: {float: 深度 单位米}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-7
        """
        cmd = "ScenEdit_SetMission('%s','%s', {%s = %s}) " % (self.m_Side, self.strGuid, depth_type, depth)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def export_mission(self):
        """
        功能：将相应的任务导出到 Defaults 文件夹中
            Mozi/MoziServer/bin/Defaults
        限制：专项赛禁用
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        日期：2020-3-10
        """
        return self.mozi_server.send_and_recv("ScenEdit_ExportMission('{}','{}')".format(self.m_Side, self.strGuid))
