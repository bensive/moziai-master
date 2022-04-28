#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : aircraft.py
# Create date : 2019-11-06 19:38
# Modified date : 2019-12-25 16:09
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from .commonfunction import parse_weapons_record
from .activeunit import CActiveUnit
from . import database as db


class CAircraft(CActiveUnit):
    """飞机"""

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 方位类型
        self.m_BearingType = 0
        # 方位
        self.m_Bearing = 0.0
        # 距离（转换为千米）
        self.m_Distance = 0.0
        # 高低速交替航行
        self.bSprintAndDrift = False
        # 载机按钮的文本描述
        self.strDockAircraft = ""
        # 类别
        self.m_Category = 0
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
        # 机型（战斗机，多用途，加油机...)
        self.m_Type = 0
        # 宿主单元对象
        self.m_CurrentHostUnit = ""
        # 挂载方案的DBID
        self.iLoadoutDBID = 0
        # 挂载方案的GUid
        self.m_LoadoutGuid = ""
        # 获取当前行动状态
        self.strAirOpsConditionString = 0
        # 完成准备时间
        self.strFinishPrepareTime = ""
        # 快速出动信息
        self.strQuickTurnAroundInfo = ""
        # 显示燃油信息
        self.strFuelState = ""
        # 期望高度
        self.fDesiredAltitude = 0.0
        # 维护状态
        self.m_MaintenanceLevel = 0
        self.fFuelConsumptionCruise = 0.0
        self.fAbnTime = 0.0
        self.iFuelRecsMaxQuantity = 0
        # 当前油量
        self.iCurrentFuelQuantity = 0
        # 是否快速出动
        self.bQuickTurnaround_Enabled = False
        # 是否有空中加油能力
        self.bIsAirRefuelingCapable = False
        # 加油队列header
        self.strShowTankerHeader = ""
        # 加油队列明细
        self.m_ShowTanker = ""
        # 可受油探管加油
        self.m_bProbeRefuelling = False
        # 可输油管加油
        self.m_bBoomRefuelling = False
        # from dong:
        # 航路点名称
        self.strWayPointName = ""
        # 航路点描述
        self.strWayPointDescription = ""
        # 航路点剩余航行距离
        self.strWayPointDTG = ""
        # 航路点剩余航行时间
        self.WayPointTTG = ""
        # 航路点需要燃油数
        self.strWayPointFuel = ""
        self.ClassName = 'CAircraft'
        self.fMaxRange = '0.0'

    def get_loadout(self):
        """
        功能：获取挂载
        参数：无
        返回：CLoadout对象
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-17
        """
        return self.situation.loadout_dic[self.m_LoadoutGuid]

    def get_valid_weapons(self):
        """
        获取飞机有效的武器，暂时不可用接口
        :return:
        """
        info = {}
        # mount.values 可能是不同的mount，mount_obj.strWeapon,说明mount_obj 是一个对象
        for mount_obj in self.mounts.values():
            if (mount_obj.strWeaponFireState == "就绪" or "秒" in mount_obj.strWeaponFireState) \
                    and mount_obj.m_ComponentStatus <= 1:
                mount_weapons = parse_weapons_record(mount_obj.m_LoadRatio)
                for w_record in mount_weapons:
                    w_dbid = w_record['wpn_dbid']
                    if db.check_weapon_attack(w_dbid):
                        if w_dbid in info:
                            info[w_dbid] += w_record['wpn_current']
                        else:
                            info[w_dbid] = w_record['wpn_current']
        if self.loadout is not None:
            mount_weapons = parse_weapons_record(self.loadout.m_LoadRatio)
            for w_record in mount_weapons:
                w_dbid = w_record['wpn_dbid']
                if db.check_weapon_attack(w_dbid):
                    if w_dbid in info:
                        info[w_dbid] += w_record['wpn_current']
                    else:
                        info[w_dbid] = w_record['wpn_current']
        return info

    def get_summary_info(self):
        """
        功能：获取精简信息, 提炼信息进行决策
        参数：无
        返回：dict
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        info_dict = {
            "guid": self.strGuid,
            "DBID": self.iDBID,
            "subtype": str(self.m_Type),
            "facilityTypeID": "",
            "name": self.strName,
            "proficiency": self.m_ProficiencyLevel,
            "latitude": self.dLatitude,
            "longitude": self.dLongitude,
            "altitude": self.fAltitude_AGL,
            "altitude_asl": self.iAltitude_ASL,
            "heading": self.fCurrentHeading,
            "speed": self.fCurrentSpeed,
            "throttle": self.m_CurrentThrottle,
            "autodetectable": self.bAutoDetectable,
            "unitstate": self.strActiveUnitStatus,
            "fuelstate": self.strFuelState,
            "weaponstate": -1,
            "mounts": self.get_mounts(),
            "targetedBy": self.get_ai_targets(),
            "pitch": self.fPitch,
            "roll": self.fRoll,
            "yaw": self.fCurrentHeading,
            "loadout": self.get_loadout(),
            "type": "Aircraft",
            "fuel": self.iCurrentFuelQuantity,
            "damage": self.strDamageState,
            "sensors": self.get_sensor(),
            "weaponsValid": self.get_weapon_infos()
        }
        return info_dict

    def get_status_type(self):
        """
        功能：获取飞机状态
        参数：无
        返回：str   {'validToFly' - 在基地可马上部署飞行任务,
                    'InAir' - 在空中可部署巡逻，进攻，航路规划,
                    'InAirRTB' - 在空中返航或降落,
                    'WaitReady' - 其他}
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        if self.strAirOpsConditionString in (1, 2, 4, 8, 9, 18, 23, 24, 26):
            # 在基地可马上部署飞行任务
            return 'validToFly'
        elif self.strAirOpsConditionString in (0, 13, 14, 15, 16, 19, 20, 21, 22):
            # 在空中可部署巡逻，进攻，航路规划
            return 'InAir'
        elif self.strAirOpsConditionString in (5, 10, 11, 17, 25):
            # 在空中返航或降落
            return 'InAirRTB'
        else:
            return 'WaitReady'

    def set_waypoint(self, longitude, latitude):
        """
        功能：设置飞机下一个航路点
        参数：
            longitude {float - 经度}
            latitude {float - 纬度}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        lua_str = "ScenEdit_SetUnit({side= '%s', guid='%s', course={ { Description = ' ', TypeOf = " \
                  "'ManualPlottedCourseWaypoint', longitude = %s, latitude = %s } } })" % (
                      self.m_Side, self.strGuid, longitude, latitude)
        return self.mozi_server.send_and_recv(lua_str)

    def ops_single_out(self):
        """
        功能：设置在基地内飞机单机出动
        类别：推演所用函数
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        if self.m_HostActiveUnit:
            return super().set_single_out()
        return False

    def deploy_dipping_sonar(self):
        """
        功能：部署吊放声呐
        类别：推演所用函数
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        return self.mozi_server.send_and_recv("Hs_DeployDippingSonar('{}')".format(self.strGuid))

    def quick_turnaround(self, true_or_false, sorties_total):
        """
        功能：让指定飞机快速出动
        类别：推演所用函数
        参数：
            true_or_false: 是否快速出动 {str：true - 是， false - 否}
            sorties_total： {int - 出动架次总数} 序号？？？
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        lua = "Hs_QuickTurnaround('%s',%s,%s)" % (self.strGuid, true_or_false, sorties_total)
        self.mozi_server.send_and_recv(lua)

    def ok_ready_mission(self, enable_quick_turnaround, combo_box):
        """
        功能：飞机按对应的挂载方案所需准备时间完成出动准备
        类别：编辑所用函数
        参数：
            enable_quick_turnaround： 是否支持快速出动 {str: true - 支持, false - 不支持}
            combo_box 为快速出动值 {int: 不支持时填-1，支持填 0}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修改：张志高 2021-8-17
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        loadout_db_guid = self.get_loadout().strDBGUID
        lua_script = "Hs_OKReadyMission('{}','{}',{},{})".format(self.strGuid,
                                                                 loadout_db_guid, enable_quick_turnaround, combo_box)
        return self.mozi_server.send_and_recv(lua_script)

    def abort_launch(self):
        """
        功能：让正在出动中的飞机立即终止出动。
        类别：推演函数
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修改：张志高 2021-8-17
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        lua_script = f"Hs_ScenEdit_AirOpsAbortLaunch({{'{self.strGuid}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def refuel(self, tanker_guid=''):
        """
        功能：命令单元多种方式寻找加油机（自动寻找加油机、指定加油机、
        指定加油任务执行单元）进行加油。它与 ScenEdit_RefuelUnit 功能相同，只是它
        的参数是单元或任务的 GUID、后者的参数是单元或任务的名称。
        类别：推演函数
        参数：tanker_guid {str: 加油机guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        if tanker_guid == '':
            lua = "Hs_ScenEdit_AirRefuel({guid='%s'})" % self.strGuid
        else:
            lua = "Hs_ScenEdit_AirRefuel({guid='%s',tanker_guid = '%s'})" % (self.strGuid, tanker_guid)
        return self.mozi_server.send_and_recv(lua)

    def set_airborne_time(self, hour, minute, second):
        """
        功能：设置留空时间
        类别：编辑所用函数
        参数：
            hour: {int - 小时}
            minute: {int - 分钟}
            second: {int - 秒}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        lua_script = "Hs_SetAirborneTime('{}','{}','{}','{}')".format(self.strGuid, hour, minute, second)
        return self.mozi_server.send_and_recv(lua_script)

    def time_to_ready(self, time):
        """
        功能：设置飞机出动准备时间
        限制：专项赛禁用
        类别：编辑所用函数
        参数：
            time: 出动准备时间 {str - 00:00:02 格式'天:小时:分'}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        return self.mozi_server.send_and_recv("Hs_ScenEdit_TimeToReady('%s',{'%s'})" % (time, self.strGuid))

    def ready_immediately(self, loadout_dbid, enable_quick_turnaround, combo_box, immediately_go, optional_weapon,
                          ignore_weapon):
        """
        功能：飞机立即完成出动准备
        限制：专项赛禁用
        类别：编辑所用函数
        参数：
            loadout_dbid:  {int：挂载方案数据库dbid}
            enable_quick_turnaround： 是否支持快速出动 {str: true - 支持, false - 不支持}
            combo_box 为快速出动值 {int: 不支持时填-1，支持填 0}
            immediately_go 是否立即出动  {str: true - 是, false - 否}
            optional_weapon 是否不含可选武器 {str: true - 不包含, false - 包含}
            ignore_weapon   是否不忽略武器  {str: true - 不忽略, false - 忽略}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修改：张志高 2021-8-17
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        lua_script = "Hs_ReadyImmediately('{}',{},{},{},{},{},{})".format(self.strGuid, loadout_dbid,
                                                                          enable_quick_turnaround, combo_box,
                                                                          immediately_go,
                                                                          optional_weapon, ignore_weapon)
        return self.mozi_server.send_and_recv(lua_script)