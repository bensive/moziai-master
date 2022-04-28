#!/usr/bin/env python3
# -*- coding:utf-8 -*-
##########################################################################################################
# File name : side.py
# Create date : 2020-1-8
# Modified date : 2020-05-08 16:22
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################

from mozi_simu_sdk.mssnpatrol import CPatrolMission
from mozi_simu_sdk.mssnstrike import CStrikeMission
from mozi_simu_sdk.mssnsupport import CSupportMission
from mozi_simu_sdk.mssncargo import CCargoMission
from mozi_simu_sdk.mssnferry import CFerryMission
from mozi_simu_sdk.mssnmining import CMiningMission
from mozi_simu_sdk.mssnmnclrng import CMineClearingMission

from mozi_simu_sdk.zonenonav import CNoNavZone
from mozi_simu_sdk.zonexclsn import CExclusionZone

from mozi_simu_sdk.submarine import CSubmarine
from mozi_simu_sdk.ship import CShip
from mozi_simu_sdk.aircraft import CAircraft
from mozi_simu_sdk.satellite import CSatellite
from mozi_simu_sdk.facility import CFacility
from mozi_simu_sdk.group import CGroup
from mozi_simu_sdk.referencepoint import CReferencePoint
from mozi_simu_sdk.args import is_in_domain
from mozi_simu_sdk.args import ArgsMission


########################################################################
class CSide:
    """方"""

    def __init__(self, strGuid, mozi_server, situation):
        # GUID
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 态势
        self.situation = situation
        self.__zone_index_increment = 1  # 创建封锁区或禁航区的自增命名序号
        self.__reference_point_index_increment = 1  # 创建参考点的自增命名序号
        self.missions = {}  # key:key:mission name, value: Mission instance 
        # 实体
        self.aircrafts = {}  # key:unit guid, value: Unit instance
        self.facilities = {}  # key:unit guid, value: Unit instance
        self.ships = {}
        self.submarines = {}
        self.weapons = {}
        self.satellites = {}
        # 目标
        self.contacts = {}  # key:contact guid, value, contact instance
        # 编组
        self.groups = {}
        # 点
        self.acrionPoints = {}
        # 参考点
        self.referencePoints = {}
        # 条令
        self.doctrine = None
        # 天气
        self.weather = None
        # 消息
        self.logged_messages = self.get_logged_messages()
        self.current_point = 0  # 当前得分
        self.point_record = []  # 得分记录
        self.simulate_time = ""  # 当前推演时间
        self.last_step_missing = {}  # 当前决策步损失的单元（我方），丢掉或击毁的单元（敌方）
        self.last_step_new = {}  # 当前决策步新增的单元（我方），新增的情报单元（敌方）
        self.all_units = {}
        self.activeunit = {}
        self.strName = ""  # 名称
        self.m_PosturesDictionary = []  # 获取针对其它推演方的立场
        self.m_Doctrine = ''  # 作战条令
        self.m_ProficiencyLevel = []
        self.m_AwarenessLevel = ''
        self.m_PosturesDictionary = ''
        self.iTotalScore = 0.0
        self.m_Expenditures = ''  # 战损
        self.m_Losses = ''  # 战耗
        self.iScoringDisaster = 0.0  # 完败阀值
        self.iScoringTriumph = 0.0  # 完胜阀值
        self.bCATC = False  # 自动跟踪非作战单元
        self.bCollectiveResponsibility = False  # 集体反应
        self.bAIOnly = False  # 只由计算机扮演
        self.strBriefing = ''  # 简要
        self.strCloseResult = ''  # 战斗结束后的结果
        self.fCamerAltitude = 0.0  # 中心点相机高度
        self.fCenterLatitude = 0.0  # 地图中心点纬度
        self.fCenterLongitude = 0.0  # 地图中心点经度
        self.strSideColorKey = ''  # 推演方颜色Key
        self.strFriendlyColorKey = ''  # 友方颜色Key
        self.strNeutralColorKey = ''  # 中立方颜色Key
        self.strUnfriendlyColorKey = ''  # 非友方颜色Key
        self.strHostileColorKey = ''  # 敌方颜色Key
        self.iSideStopCount = 0  # 推演方剩余停止次数
        self.m_ScoringLogs = ''
        self.m_ContactList = ''  # 所有的目标
        self.m_WarDamageOtherTotal = ''  # 战损的其它统计，包含但不限于(统计损失单元带来的经济和人员损失)
        self.pointname2location = {}  # 存放已命名的参考点的名称     #aie 20200408

    def static_construct(self):
        """
        将推演方准静态化
        by aie
        """
        self.doctrine = self.get_doctrine()
        self.groups = self.get_groups()
        self.submarines = self.get_submarines()
        self.ships = self.get_ships()
        self.facilities = self.get_facilities()
        self.aircrafts = self.get_aircrafts()
        self.satellites = self.get_satellites()
        self.weapons = self.get_weapons()
        self.unguidedwpns = self.get_unguided_weapons()
        self.sideways = self.get_sideways()
        self.contacts = self.get_contacts()
        self.loggedmssgs = self.get_logged_messages()
        self.patrolmssns = self.get_patrol_missions()
        self.strikemssns = self.get_strike_missions()
        self.supportmssns = self.get_support_missions()
        self.cargomssns = self.get_cargo_missions()
        self.ferrymssns = self.get_ferry_missions()
        self.miningmssns = self.get_mining_missions()
        self.mineclrngmssns = self.get_mine_clearing_missions()
        self.referencepnts = self.get_reference_points()
        self.nonavzones = self.get_no_nav_zones()
        self.excluzones = self.get_exclusion_zones()

        self.missions.update(self.patrolmssns)
        self.missions.update(self.strikemssns)
        self.missions.update(self.supportmssns)
        self.missions.update(self.cargomssns)
        self.missions.update(self.ferrymssns)
        self.missions.update(self.miningmssns)
        self.missions.update(self.mineclrngmssns)

    def static_update(self):
        """
        功能：静态更新推演方类下的关联类实例
        参数：无
        返回：无
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/9/20
        """
        self.static_add()
        self.static_delete()

    def static_delete(self):
        """
        将推演方删除的准静态化对象进行更新
        by aie
        """
        popped = []
        for k, v in self.situation.all_guid_delete_info.items():
            if v["side"] == self.strGuid:
                popped.append(k)
                if v["strType"] == 1005 and k in self.groups.keys():
                    self.groups.pop(k)
                    continue
                if v["strType"] == 2001 and k in self.submarines.keys():
                    self.submarines.pop(k)
                    continue
                if v["strType"] == 2002 and k in self.ships.keys():
                    self.ships.pop(k)
                    continue
                if v["strType"] == 2003 and k in self.facilities.keys():
                    self.facilities.pop(k)
                    continue
                if v["strType"] == 2004 and k in self.aircrafts.keys():
                    self.aircrafts.pop(k)
                    continue
                if v["strType"] == 2005 and k in self.satellites.keys():
                    self.satellites.pop(k)
                    continue
                if v["strType"] == 3005 and k in self.weapons.keys():
                    self.weapons.pop(k)
                    continue
                if v["strType"] == 3006 and k in self.unguidedwpns.keys():
                    self.unguidedwpns.pop(k)
                    continue
                if v["strType"] == 3008 and k in self.sideways.keys():
                    self.sideways.pop(k)
                    continue
                if v["strType"] == 4001 and k in self.contacts.keys():
                    self.contacts.pop(k)
                    continue
                if v["strType"] == 5001 and k in self.loggedmssgs.keys():
                    self.loggedmssgs.pop(k)
                    continue
                if v["strType"] == 10001 and k in self.missions.keys():
                    self.missions.pop(k)
                    continue
                if v["strType"] == 10001 and k in self.patrolmssns.keys():
                    self.patrolmssns.pop(k)
                    continue
                if v["strType"] == 10002 and k in self.strikemssns.keys():
                    self.strikemssns.pop(k)
                    continue
                if v["strType"] == 10003 and k in self.supportmssns.keys():
                    self.supportmssns.pop(k)
                    continue
                if v["strType"] == 10004 and k in self.cargomssns.keys():
                    self.cargomssns.pop(k)
                    continue
                if v["strType"] == 10005 and k in self.ferrymssns.keys():
                    self.ferrymssns.pop(k)
                    continue
                if v["strType"] == 10006 and k in self.miningmssns.keys():
                    self.miningmssns.pop(k)
                    continue
                if v["strType"] == 10007 and k in self.mineclrngmssns.keys():
                    self.mineclrngmssns.pop(k)
                    continue
                if v["strType"] == 11001 and k in self.referencepnts.keys():
                    self.referencepnts.pop(k)
                    continue
                if v["strType"] == 11002 and k in self.nonavzones.keys():
                    self.nonavzones.pop(k)
                    continue
                if v["strType"] == 11003 and k in self.excluzones.keys():
                    self.excluzones.pop(k)
        for k in popped:
            self.situation.all_guid_delete_info.pop(k)

    def static_add(self):
        """
        将推演方增加的准静态化对象进行更新
        by aie
        """
        for k, v in self.situation.all_guid_add_info.items():
            if v["side"] == self.strGuid:
                if v["strType"] == 1005:
                    self.groups.update({k: self.situation.group_dic[k]})
                    continue
                if v["strType"] == 2001:
                    self.submarines.update({k: self.situation.submarine_dic[k]})
                    continue
                if v["strType"] == 2002:
                    self.ships.update({k: self.situation.ship_dic[k]})
                    continue
                if v["strType"] == 2003:
                    self.facilities.update({k: self.situation.facility_dic[k]})
                    continue
                if v["strType"] == 2004:
                    self.aircrafts.update({k: self.situation.aircraft_dic[k]})
                    continue
                if v["strType"] == 2005:
                    self.satellites.update({k: self.situation.satellite_dic[k]})
                    continue
                if v["strType"] == 3005:
                    self.weapons.update({k: self.situation.weapon_dic[k]})
                    continue
                if v["strType"] == 3006:
                    self.unguidedwpns.update({k: self.situation.unguidedwpn_dic[k]})
                    continue
                if v["strType"] == 3008:
                    self.sideways.update({k: self.situation.sideway_dic[k]})
                    continue
                if v["strType"] == 4001:
                    self.contacts.update({k: self.situation.contact_dic[k]})
                    continue
                if v["strType"] == 5001:
                    self.loggedmssgs.update({k: self.situation.logged_messages[k]})
                    continue
                if v["strType"] == 10001:
                    self.patrolmssns.update({k: self.situation.mssnpatrol_dic[k]})
                    self.missions.update({k: self.situation.mssnpatrol_dic[k]})
                    continue
                if v["strType"] == 10002:
                    self.strikemssns.update({k: self.situation.mssnstrike_dic[k]})
                    self.missions.update({k: self.situation.mssnstrike_dic[k]})
                    continue
                if v["strType"] == 10003:
                    self.supportmssns.update({k: self.situation.mssnsupport_dic[k]})
                    self.missions.update({k: self.situation.mssnsupport_dic[k]})
                    continue
                if v["strType"] == 10004:
                    self.cargomssns.update({k: self.situation.mssncargo_dic[k]})
                    self.missions.update({k: self.situation.mssncargo_dic[k]})
                    continue
                if v["strType"] == 10005:
                    self.ferrymssns.update({k: self.situation.mssnferry_dic[k]})
                    self.missions.update({k: self.situation.mssnferry_dic[k]})
                    continue
                if v["strType"] == 10006:
                    self.miningmssns.update({k: self.situation.mssnmining_dic[k]})
                    self.missions.update({k: self.situation.mssnmining_dic[k]})
                    continue
                if v["strType"] == 10007:
                    self.mineclrngmssns.update({k: self.situation.mssnmnclrng_dic[k]})
                    self.missions.update({k: self.situation.mssnmnclrng_dic[k]})
                    continue
                if v["strType"] == 11001:
                    self.referencepnts.update({k: self.situation.referencept_dic[k]})
                    continue
                if v["strType"] == 11002:
                    self.nonavzones.update({k: self.situation.zonenonav_dic[k]})
                    continue
                if v["strType"] == 11003:
                    self.excluzones.update({k: self.situation.zonexclsn_dic[k]})

    def get_doctrine(self):
        """
        获取推演方条令
        by aie
        """
        if self.m_Doctrine in self.situation.doctrine_dic:
            doctrine = self.situation.doctrine_dic[self.m_Doctrine]
            doctrine.category = 'Side'  # 需求来源：20200331-2/2:Xy
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
        weapon_record = list({v.m_UnitWeapons: k for k, v in self.submarines.items()})
        weapon_record.extend(list({v.m_UnitWeapons: k for k, v in self.ships.items()}))
        weapon_record.extend(list({v.m_UnitWeapons: k for k, v in self.facilities.items()}))
        weapon_record.extend(list({v.m_UnitWeapons: k for k, v in self.aircrafts.items()}))
        weapon_record.extend(list({v.m_UnitWeapons: k for k, v in self.satellites.items()}))
        lst1 = []
        for unit_weapon_record in weapon_record:
            if unit_weapon_record:
                lst = unit_weapon_record.split('@')
                lst1.extend([k.split('$')[1] for k in lst])
        return lst1

    def get_weapon_infos(self):
        """
        功能：获取编组内所有武器的名称及数据库guid
        参数：无
        返回：编组内所有武器的名称及数据库guid组成的列表
        作者：aie
        张志高修改于2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        weapon_record = list({v.m_UnitWeapons: k for k, v in self.submarines.items()})
        weapon_record.extend(list({v.m_UnitWeapons: k for k, v in self.ships.items()}))
        weapon_record.extend(list({v.m_UnitWeapons: k for k, v in self.facilities.items()}))
        weapon_record.extend(list({v.m_UnitWeapons: k for k, v in self.aircrafts.items()}))
        weapon_record.extend(list({v.m_UnitWeapons: k for k, v in self.satellites.items()}))
        lst1 = []
        for unit_weapon_record in weapon_record:
            if unit_weapon_record:
                lst = unit_weapon_record.split('@')
                lst1.extend([k.split('$') for k in lst])
        return lst1

    def get_groups(self):
        """
        功能：获取本方编组
        参数：无
        返回：dict 格式 {unit_guid_1: unit_obj_1, unit_guid_2: unit_obj_2, ...}  CGroup
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        group_dic = {}
        for k, v in self.situation.group_dic.items():
            if v.m_Side == self.strGuid:
                group_dic[k] = v
        return group_dic

    def get_submarines(self):
        """
        功能：获取本方潜艇
        参数：无
        返回：dict 格式 {unit_guid_1: unit_obj_1, unit_guid_2: unit_obj_2, ...}  CSubmarine
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        submarine_dic = {}
        for k, v in self.situation.submarine_dic.items():
            if v.m_Side == self.strGuid:
                submarine_dic[k] = v
        return submarine_dic

    def get_ships(self):
        """
        功能：获取本方船
        参数：无
        返回：dict 格式 {unit_guid_1: unit_obj_1, unit_guid_2: unit_obj_2, ...}  CShip
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        ship_dic = {}
        for k, v in self.situation.ship_dic.items():
            if v.m_Side == self.strGuid:
                ship_dic[k] = v
        return ship_dic

    def get_facilities(self):
        """
        功能：获取本方地面单位
        参数：无
        返回：dict 格式 {unit_guid_1: unit_obj_1, unit_guid_2: unit_obj_2, ...}  CFacility
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        facility_dic = {}
        for k, v in self.situation.facility_dic.items():
            if v.m_Side == self.strGuid:
                facility_dic[k] = v
        return facility_dic

    def get_aircrafts(self):
        """
        功能：获取本方飞机
        参数：无
        返回：dict 格式 {unit_guid_1: unit_obj_1, unit_guid_2: unit_obj_2, ...}  CAircraft
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        air_dic = {}
        for k, v in self.situation.aircraft_dic.items():
            if v.m_Side == self.strGuid:
                air_dic[k] = v
        return air_dic

    def get_satellites(self):
        """
        功能：获取本方卫星
        参数：无
        返回：dict 格式 {unit_guid_1: unit_obj_1, unit_guid_2: unit_obj_2, ...}  CSatellite
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        satellite_dic = {}
        for k, v in self.situation.satellite_dic.items():
            if v.m_Side == self.strGuid:
                satellite_dic[k] = v
        return satellite_dic

    def get_weapons(self):
        """
        功能：获取本方武器
        参数：无
        返回：dict 格式 {unit_guid_1: unit_obj_1, unit_guid_2: unit_obj_2, ...}  CWeapon
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        weapon_dic = {}
        for k, v in self.situation.weapon_dic.items():
            if v.m_Side == self.strGuid:
                weapon_dic[k] = v
        return weapon_dic

    def get_unguided_weapons(self):
        """
        功能：获取本方非制导武器
        参数：无
        返回：dict 格式 {unit_guid_1: unit_obj_1, unit_guid_2: unit_obj_2, ...}
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        unguidedwpn_dic = {}
        for k, v in self.situation.unguidedwpn_dic.items():
            if v.m_Side == self.strGuid:
                unguidedwpn_dic[k] = v
        return unguidedwpn_dic

    def get_sideways(self):
        """
        功能：获取预定义航路
        参数：无
        返回：dict 格式 {unit_guid_1: unit_obj_1, unit_guid_2: unit_obj_2, ...}  CSideWay
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        return {k: v for k, v in self.situation.sideway_dic.items() if v.m_Side == self.strGuid}

    def get_contacts(self):
        """
        功能：获取本方目标
        参数：无
        返回：dict 格式 {contact_guid_1: contact_obj_1, contact_guid_2: contact_obj_2, ...}  CContact
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        contact_dic = {}
        for k, v in self.situation.contact_dic.items():
            if v.m_OriginalDetectorSide == self.strGuid:  # changed by aie
                contact_dic[k] = v
        return contact_dic

    def get_logged_messages(self):
        """
        功能：获取本方日志消息 # 接口暂不可用
        参数：无
        返回：dict 格式 {guid_1: _obj_1, guid_2: obj_2, ...}
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        logged_messages = {}
        for k, v in self.situation.logged_messages.items():
            if v.m_Side == self.strGuid:
                logged_messages[k] = v
        return logged_messages

    def get_patrol_missions(self):
        """
        功能：获取巡逻任务
        参数：无
        返回：dict 格式 {mission_guid_1: mission_obj_1, mission_guid_2: mission_obj_2, ...}  CPatrolMission
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        return {k: v for k, v in self.situation.mssnpatrol_dic.items() if v.m_Side == self.strGuid}

    def get_strike_missions(self):
        """
        功能：获取打击任务
        参数：无
        返回：dict 格式 {mission_guid_1: mission_obj_1, mission_guid_2: mission_obj_2, ...}  CStrikeMission
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        return {k: v for k, v in self.situation.mssnstrike_dic.items() if v.m_Side == self.strGuid}

    def get_support_missions(self):
        """
        功能：获取支援任务
        参数：无
        返回：dict 格式 {mission_guid_1: mission_obj_1, mission_guid_2: mission_obj_2, ...}  CSupportMission
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        return {k: v for k, v in self.situation.mssnsupport_dic.items() if v.m_Side == self.strGuid}

    def get_cargo_missions(self):
        """
        功能：获取运输任务
        参数：无
        返回：dict 格式 {mission_guid_1: mission_obj_1, mission_guid_2: mission_obj_2, ...}  CCargoMission
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        return {k: v for k, v in self.situation.mssncargo_dic.items() if v.m_Side == self.strGuid}

    def get_ferry_missions(self):
        """
        功能：获取转场任务
        参数：无
        返回：dict 格式 {mission_guid_1: mission_obj_1, mission_guid_2: mission_obj_2, ...}  CFerryMission
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        return {k: v for k, v in self.situation.mssnferry_dic.items() if v.m_Side == self.strGuid}

    def get_mining_missions(self):
        """
        功能：获取布雷任务 # 接口暂不可用
        参数：无
        返回：dict 格式 {mission_guid_1: mission_obj_1, mission_guid_2: mission_obj_2, ...}  CMiningMission
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        return {k: v for k, v in self.situation.mssnmining_dic.items() if v.m_Side == self.strGuid}

    def get_missions_by_name(self, name):
        """
        功能：根据任务名称获取任务
        参数：name {str: 任务名称}
        返回：任务对象
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        # 需求来源：20200331－1:Xy
        # return {k: v for k, v in self.missions.items() if v.strName == name}
        # 临时需改，by 赵俊义
        for k, v in self.missions.items():
            if v.strName == name:
                return v

    def get_mine_clearing_missions(self):
        """
        功能：获取扫雷任务 # 接口暂不可用
        参数：无
        返回：dict 格式 {mission_guid_1: mission_obj_1, mission_guid_2: mission_obj_2, ...}  CMineClearingMission
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        return {k: v for k, v in self.situation.mssnmnclrng_dic.items() if v.m_Side == self.strGuid}

    def get_reference_points(self):
        """
        功能：获取参考点
        参数：无
        返回：dict 格式 {item_guid_1: item_obj_1, item_guid_2: item_obj_2, ...}  CReferencePoint
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        referencept_dic = {}
        for k, v in self.situation.referencept_dic.items():
            if v.m_Side == self.strGuid:
                referencept_dic[k] = v
        return referencept_dic

    def get_no_nav_zones(self):
        """
        功能：获取禁航区
        参数：无
        返回：dict 格式 {item_guid_1: item_obj_1, item_guid_2: item_obj_2, ...}  CNoNavZone
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        zonenonav_dic = {}
        for k, v in self.situation.zonenonav_dic.items():
            if v.m_Side == self.strGuid:
                zonenonav_dic[k] = v
        return zonenonav_dic

    def set_reference_point(self, name, lat, lon):
        """
        功能：更新参考点坐标
        参数：
            name {str: 参考点名称}
            lat {float: 纬度}
            lon {float: 经度}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        # 传入int后，获取point经纬度为0，这里做下强制类型转换
        if isinstance(lat, int):
            lat = float(lat)
        if isinstance(lon, int):
            lon = float(lon)
        set_str = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
            self.strName, name, lat, lon)
        return self.mozi_server.send_and_recv(set_str)

    def get_exclusion_zones(self):
        """
        功能：获取封锁区
        参数：无
        返回：dict 格式 {item_guid_1: item_obj_1, item_guid_2: item_obj_2, ...}  CExclusionZone
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        zonexclsn_dic = {}
        for k, v in self.situation.zonexclsn_dic.items():
            if v.m_Side == self.strGuid:
                zonexclsn_dic[k] = v
        return zonexclsn_dic

    def get_score(self):
        """
        功能：获取本方分数
        参数：无
        返回：本方总分
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/21/20
        """
        return self.iTotalScore

    def get_unit_by_guid(self, guid):
        """
        功能：根据guid获取实体对象
        参数：guid {str: 实体guid}
        返回：活动单元对象
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        if guid in self.aircrafts:
            return self.aircrafts[guid]
        if guid in self.facilities:
            return self.facilities[guid]
        if guid in self.weapons:
            return self.weapons[guid]
        if guid in self.ships:
            return self.ships[guid]
        if guid in self.satellites:
            return self.satellites[guid]
        if guid in self.submarines:
            return self.submarines[guid]
        return None

    def get_contact_by_guid(self, contact_guid):
        """
        功能：根据情报对象guid获取情报对象
        参数：contact_guid {str: 情报对象guid}
        返回：情报对象
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-28
        """
        if contact_guid in self.contacts:
            return self.contacts[contact_guid]
        else:
            return None

    def get_identified_targets_by_name(self, name):
        """
        功能：从推演方用名称确认目标
        参数：name {str: 情报对象名称}
        返回：dict 格式 {item_guid_1: item_obj_1, item_guid_2: item_obj_2, ...}  CContact
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        # 需求来源：20200330-1.3/3:lzy
        return {k: v for k, v in self.contacts.items() if v.strName == name}

    def get_elevation(self, coord_point):
        """
        功能：获取某点的海拔高度
        参数：coord_point 经纬度元组 {tuple: (float, float) (lat, lon)}
        返回：该点的海拔高度，单位米
        作者：-
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        lua_cmd = "ReturnObj(World_GetElevation ({latitude='%lf',longitude='%lf'}))" % (coord_point[0], coord_point[1])
        return int(self.mozi_server.send_and_recv(lua_cmd))

    def add_mission_patrol(self, name, patrol_type_num, zone_points):
        """
        功能：添加巡逻任务
        参数：name:{str:任务名称}
             patrol_type_num: int 巡逻类型的编号 详见 args.py ArgsMission.patrol_type
                {int:0: 'AAW : 空战巡逻',
                    1: 'SUR_SEA : 反面(海)巡逻',
                    2: 'SUR_LAND : 反面(陆)巡逻',
                    3: 'SUR_MIXED : 反面(混)巡逻',
                    4: 'SUB : 反潜巡逻',
                    5: 'SEAD : 压制敌防空巡逻',
                    6: 'SEA : 海上控制巡逻'}
             zone_points:{list:参考点名称组成的列表}
        返回：
            创建的巡逻任务对象 或 None
        作者：aie
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/24/20,4/25/20
        """
        if not is_in_domain(patrol_type_num, ArgsMission.patrol_type):
            return "patrol_type_num不在域中", None
        patrol_type = ArgsMission.patrol_type[patrol_type_num].replace(' ', '').split(':')[0]
        area_str = str(zone_points).replace('[', '').replace(']', '')
        detail = f"{{type='{patrol_type}', Zone={{{area_str}}}}}"

        cmd = "ReturnObj(ScenEdit_AddMission('{}','{}','{}',{}))".format(self.strGuid, name, 'Patrol', detail)
        self.mozi_server.throw_into_pool(cmd)
        return_obj = self.mozi_server.send_and_recv(cmd)

        obj = None
        if name in return_obj:
            return_dict = self.__convert_lua_obj_to_dict(return_obj)
            self.situation.throw_into_pseudo_situ_all_guid(return_dict['guid'])
            obj = CPatrolMission(return_dict['guid'], self.mozi_server, self.situation)
            obj.strName = name
            obj.m_Side = self.strGuid
            obj.m_MissionClass = 2    # 巡逻
        return obj

    def add_mission_strike(self, name, strike_type_num):
        """
        功能：添加打击任务
        参数：name:{str:任务名称}
             strike_type_num:{int:打击类型的编号} 详见 args.py ArgsMission.strike_type
                {0: 'AIR : 空中拦截',
                    1: 'LAND : 对陆打击',
                    2: 'SEA : 对海打击',
                    3: 'SUB : 对潜打击'}
        返回：
            创建的打击任务对象 或 None
        作者：aie
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/24/20,4/25/20
        """
        if not is_in_domain(strike_type_num, ArgsMission.strike_type):
            return "strike_type_num不在域中"
        strike_type = ArgsMission.strike_type[strike_type_num].replace(' ', '').split(':')[0]
        detail = f"{{type='{strike_type}'}}"

        cmd = "ReturnObj(ScenEdit_AddMission('{}','{}','{}',{}))".format(self.strGuid, name, 'Strike', detail)
        self.mozi_server.throw_into_pool(cmd)
        return_obj = self.mozi_server.send_and_recv(cmd)

        obj = None
        if name in return_obj:
            return_dict = self.__convert_lua_obj_to_dict(return_obj)
            self.situation.throw_into_pseudo_situ_all_guid(return_dict['guid'])
            obj = CStrikeMission(return_dict['guid'], self.mozi_server, self.situation)
            obj.strName = name
            obj.m_Side = self.strGuid
            obj.m_MissionClass = 1    # 打击任务
            obj.m_StrikeType = strike_type_num  # 需确认是否一致
        return obj

    def add_mission_support(self, name, zone_points):
        """
        功能：添加支援任务
        参数：name:{str:任务名称}
             zone_points:{list:参考点名称组成的列表}
        返回：
            创建的支援任务对象 或 None
        作者：aie
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/25/20
        """
        area_str = str(zone_points).replace('[', '').replace(']', '')
        detail = f"{{Zone={{{area_str}}}}}"

        cmd = "ReturnObj(ScenEdit_AddMission('{}','{}','{}',{}))".format(self.strGuid, name, 'Support', detail)
        self.mozi_server.throw_into_pool(cmd)
        return_obj = self.mozi_server.send_and_recv(cmd)

        obj = None
        if name in return_obj:
            return_dict = self.__convert_lua_obj_to_dict(return_obj)
            self.situation.throw_into_pseudo_situ_all_guid(return_dict['guid'])
            obj = CSupportMission(return_dict['guid'], self.mozi_server, self.situation)
            obj.strName = name
            obj.m_Side = self.strGuid
            obj.m_MissionClass = 3    # 支援
        return obj

    def add_mission_ferry(self, name, destination):
        """
        功能：添加转场任务
        参数：name:{str:任务名称}
             destination:{str:目的地名称或guid}
        返回：
            创建的转场任务对象 或 None
        作者：aie
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/25/20
        """
        detail = f"{{destination='{destination}'}}"

        cmd = "ReturnObj(ScenEdit_AddMission('{}','{}','{}',{}))".format(self.strGuid, name, 'Ferry', detail)
        self.mozi_server.throw_into_pool(cmd)
        return_obj = self.mozi_server.send_and_recv(cmd)

        obj = None
        if name in return_obj:
            return_dict = self.__convert_lua_obj_to_dict(return_obj)
            self.situation.throw_into_pseudo_situ_all_guid(return_dict['guid'])
            obj = CFerryMission(return_dict['guid'], self.mozi_server, self.situation)
            obj.strName = name
            obj.m_Side = self.strGuid
            obj.m_MissionClass = 4    # 转场
        return obj

    def add_mission_mining(self, name, zone_points):
        """
        功能：添加布雷任务
        参数：name:{str:任务名称}
             zone_points:{list:参考点名称组成的列表}
        返回：
            创建的布雷任务对象 或 None
        作者：aie
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/25/20
        """
        area_str = str(zone_points).replace('[', '').replace(']', '')
        detail = f"{{Zone={{{area_str}}}}}"
        cmd = "ReturnObj(ScenEdit_AddMission('{}','{}','{}',{}))".format(self.strGuid, name, 'Mining', detail)
        self.mozi_server.throw_into_pool(cmd)
        return_obj = self.mozi_server.send_and_recv(cmd)

        obj = None
        if name in return_obj:
            return_dict = self.__convert_lua_obj_to_dict(return_obj)
            self.situation.throw_into_pseudo_situ_all_guid(return_dict['guid'])
            obj = CMiningMission(return_dict['guid'], self.mozi_server, self.situation)
            obj.strName = name
            obj.m_Side = self.strGuid
            obj.m_MissionClass = 5    # 布雷
        return obj

    def add_mission_mine_clearing(self, name, zone_points):
        """
        功能：添加扫雷任务
        参数：name:{str:任务名称}
             zone_points:{list:参考点名称组成的列表}
        返回：
            创建的扫雷任务对象 或 None
        作者：aie
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/25/20
        """
        area_str = str(zone_points).replace('[', '').replace(']', '')
        detail = f"{{Zone={{{area_str}}}}}"
        cmd = "ReturnObj(ScenEdit_AddMission('{}','{}','{}',{}))".format(self.strGuid, name, 'MineClearing', detail)
        self.mozi_server.throw_into_pool(cmd)
        return_obj = self.mozi_server.send_and_recv(cmd)

        obj = None
        if name in return_obj:
            return_dict = self.__convert_lua_obj_to_dict(return_obj)
            self.situation.throw_into_pseudo_situ_all_guid(return_dict['guid'])
            obj = CMineClearingMission(return_dict['guid'], self.mozi_server, self.situation)
            obj.strName = name
            obj.m_Side = self.strGuid
            obj.m_MissionClass = 6    # 扫雷
        return obj

    def add_mission_cargo(self, name, zone_points):
        """
        功能：添加投送任务
        参数：name:{str:任务名称}
             zone_points:{list:参考点名称组成的列表}
        返回：创建的投送任务对象 或 None
        作者：aie
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/25/20
        """
        area_str = str(zone_points).replace('[', '').replace(']', '')
        detail = f"{{Zone={{{area_str}}}}}"
        cmd = "ReturnObj(ScenEdit_AddMission('{}','{}','{}',{}))".format(self.strGuid, name, 'Cargo', detail)
        self.mozi_server.throw_into_pool(cmd)
        return_obj = self.mozi_server.send_and_recv(cmd)

        obj = None
        if name in return_obj:
            return_dict = self.__convert_lua_obj_to_dict(return_obj)
            self.situation.throw_into_pseudo_situ_all_guid(return_dict['guid'])
            obj = CCargoMission(return_dict['guid'], self.mozi_server, self.situation)
            obj.strName = name
            obj.m_Side = self.strGuid
            obj.m_MissionClass = 8    # 投送
        return obj

    def delete_mission(self, mission_name):
        """
        功能：删除任务
        参数：mission_name:{str:任务名称}
        返回：该任务不存在 或 lua执行成功 或 脚本执行出错
        作者：-
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/25/20
        """
        mission = self.get_missions_by_name(mission_name)
        if mission:
            lua = 'ScenEdit_DeleteMission("%s", "%s")' % (self.strName, mission_name)
            result = self.mozi_server.send_and_recv(lua)
            if result == 'lua执行成功':
                del self.missions[mission.strGuid]
            return result
        return '该任务不存在'

    def add_group(self, unit_guid_list):
        """
        功能：将同类型单元单元合并创建编队，暂不支持不同类型单元。
        参数：unit_guid_list:{list: 单元guid列表}
        返回：所添加单元的活动单元对象 或 None
        作者：-
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/25/20
        """
        table = str(unit_guid_list).replace('[', '{').replace(']', '}')
        return_str = self.mozi_server.send_and_recv("ReturnObj(Hs_ScenEdit_AddGroup({}))".format(table))
        if 'unit {' in return_str:
            # 将返回的字符串转换成字典
            return_dict = self.__convert_lua_obj_to_dict(return_str)
            self.situation.throw_into_pseudo_situ_all_guid(return_dict['guid'])
            obj = CGroup(return_dict['guid'], self.mozi_server, self.situation)
            obj.strName = return_dict['name']
            obj.m_Side = self.strGuid
            return obj
        return None

    def air_group_out(self, air_guid_list):
        """
        功能：飞机编组出动。
        参数：air_guid_list:{list: 单元guid列表}
            例子：['71136bf2-58ba-4013-92f5-2effc99d2wds','71136bf2-58ba-4013-92f5-2effc99d2fa0']
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/25/20
        """
        table = str(air_guid_list).replace('[', '{').replace(']', '}')
        lua_script = "Hs_LUA_AirOpsGroupOut('{}',{})".format(self.strName, table)
        return self.mozi_server.send_and_recv(lua_script)

    @staticmethod
    def __convert_lua_obj_to_dict(return_str):
        # 功能：将lua返回的对象，转化成python字典
        return_dict = {}
        if '\r\n' in return_str:
            return_list = return_str.split('\r\n')
        else:
            return_str = return_str.strip()[1:-1]
            return_list = return_str.split(',')
        for item in return_list:
            if '=' in item:
                item = item.strip()
                if item.endswith(','):
                    item = item[:-1]
                kv = item.split('=')
                return_dict[kv[0].strip()] = kv[1].strip().replace("'", '')
        return return_dict

    def set_ecom_status(self, object_type, object_name, emcon):
        """
        功能：设置选定对象的 EMCON
        参数：
            object_type 对象类型 {str: 'Side' / 'Mission' / 'Group' / 'Unit'}
            object_name {str: 对象名称或guid}
            emcon {str: 感器类型和传感器状态}
                Inherit 继承上级设置
                or Radar/Sonar/OECM=Active/Passive 设置开关
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/25/20
        """
        return self.mozi_server.send_and_recv("ScenEdit_SetEMCON('{}','{}','{}')".format(object_type, object_name,
                                                                                         emcon))

    def add_reference_point(self, name, lat, lon):
        """
        功能：添加参考点
        参数：
            name {str: 参考点名称}
            lat {float: 纬度}
            lon {float: 经度}
        返回：None 或 参考点对象
        作者：aie
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/24/20
        """
        cmd = "ReturnObj(ScenEdit_AddReferencePoint({side='%s', name='%s', lat=%s, lon=%s}))" % (self.strName, name, lat, lon)
        result_str = self.mozi_server.send_and_recv(cmd)
        pnt = None
        if name in result_str:
            result_dict = self.__convert_lua_obj_to_dict(result_str)
            self.mozi_server.throw_into_pool(cmd)
            pnt = CReferencePoint(result_dict['guid'], self.mozi_server, self.situation)
            pnt.strName = name
            pnt.dLatitude = lat
            pnt.dLongitude = lon
        return pnt

    def add_zone(self, zone_type, description, area, affects, is_active='true', mark_as=None):
        """
        功能：创建区域
        参数：
            zone_type: {int: 0 - 禁航区，1 - 封锁区}
            description: {str: 区域名称}
            area {list: 参考点名称列表}
            affects 应用于单元类型 {list: Aircraft Ship Submarine Facility 组成的列表}
                例子： ['Aircraft', 'Ship', 'Submarine']
            is_active 是否启用 {str: true - 是， false - 否}
            mark_as 封锁区闯入者立场 {str: Unfriendly - 不友好, Hostile - 敌对}
        返回：None 或 区域对象
        作者：-
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/24/20
        """
        area_str = str(area).replace('[', '{').replace(']', '}')
        affects_str = str(affects).replace('[', '{').replace(']', '}')
        mark_as_str = ''
        if zone_type == 1:
            if mark_as:
                mark_as_str = f", Markas='{mark_as}'"
            else:
                return "封锁区设置缺失参数mark_as"
        lua_script = f"ReturnObj(ScenEdit_AddZone('{self.strGuid}', {zone_type}, {{description='{description}', " \
                     f"Isactive={is_active}, Affects={affects_str}, Area={area_str}{mark_as_str}}}))"
        return_str = self.mozi_server.send_and_recv(lua_script)

        if description in return_str:
            # 将返回的字符串转换成字典
            return_dict = self.__convert_lua_obj_to_dict(return_str)
            self.situation.throw_into_pseudo_situ_all_guid(return_dict['guid'])
            type_selected = {0: CNoNavZone, 1: CExclusionZone}
            obj = type_selected[zone_type](return_dict['guid'], self.mozi_server, self.situation)
            obj.strName = description
            obj.strDescription = description
            obj.m_Side = self.strGuid
            return obj
        return None

    def set_zone(self, zone_guid, description=None, area=None, affects=None, is_active=None, mark_as=None,
                 rp_visible=None):
        """
        功能：设置区域
        参数：
            zone_guid: {str: 区域guid}
            description: {str: 区域名称}
            area {list: 参考点名称列表}
            affects 应用于单元类型 {list: Aircraft Ship Submarine Facility 组成的列表}
                例子： ['Aircraft', 'Ship', 'Submarine']
            is_active 是否启用 {str: true - 是， false - 否}
            mark_as 封锁区闯入者立场 {str: Unfriendly - 不友好, Hostile - 敌对}
            rp_visible 参考点是否可见 {str: true - 是， false - 否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/24/20
        """
        update_str = ''
        if description:
            update_str += f", description='{description}'"
        if area:
            area_str = str(area).replace('[', '{').replace(']', '}')
            update_str += f", Area={area_str}"
        if affects:
            affects_str = str(affects).replace('[', '{').replace(']', '}')
            update_str += f", Affects={affects_str}"
        if is_active:
            update_str += f", Isactive={is_active}"
        if mark_as:
            update_str += f", Markas='{mark_as}'"
        if rp_visible:
            update_str += f", RPVISIBLE={rp_visible}"
        if update_str:
            update_str = update_str[1:]

        lua_script = f"Hs_ScenEdit_SetZone('{self.strGuid}', '{zone_guid}', {{{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def get_reference_point_by_name(self, name):
        """
        功能：根据参考点名称获取参考点对象
        参数：
            name: {str: 参考点名称}
        返回：None 或 参考点对象
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-19
        """
        rp_points = self.get_reference_points()
        for k, v in rp_points.items():
            if v.strName == name:
                return v
        return None

    def assign_target_to_mission(self, contact_guid, mission_name_or_guid):
        """
        功能：将目标分配给一项打击任务
        参数：
            contact_guid: {str: 目标guid}
            mission_name_or_guid  {str: 任务名称或guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-20
        单位：北京华戍防务技术有限公司
        时间：4/24/20
        """
        lua = "ScenEdit_AssignUnitAsTarget({'%s'}, '%s')" % (contact_guid, mission_name_or_guid)
        self.mozi_server.send_and_recv(lua)

    def drop_contact(self, contact_guid):
        """
        功能：放弃目标, 不再将所选目标列为探测对象
        参数：
            contact_guid  {str: 探测目标guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-20
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        lua_script = "Hs_ContactDropTarget('%s','%s')" % (self.strGuid, contact_guid)
        self.mozi_server.send_and_recv(lua_script)

    def wcsfa_contact_types_all_unit(self, hold_tight_free_or_inherited):
        """
        功能：控制所有单元对所有目标类型的攻击状态。
        参数：
            hold_tight_free_or_inherited  {str: 'Hold'-禁止，'Tight'-限制，'Free'-自由，'Inherited'-按上级条令执行}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-20
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        lua = "Hs_WCSFAContactTypesAllUnit('%s','%s')" % (self.strGuid, hold_tight_free_or_inherited)
        self.mozi_server.send_and_recv(lua)

    def lpcw_attack_all_unit(self, yes_no_or_inherited):
        """
        功能：所有单元攻击时是否忽略计划航线。
        参数：
            yes_no_or_inherited  {str: 'Yes'-忽略，'No'-不忽略，'Inherited'-按上级条令执行}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-20
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        lua = "Hs_LPCWAttackAllUnit('{}','{}')".format(self.strGuid, yes_no_or_inherited)
        return self.mozi_server.send_and_recv(lua)

    def set_side_options(self, awareness=None, proficiency=None, is_ai_only=None, is_coll_response=None,
                         is_auto_track_civs=None):
        """
        功能：设置认知能力、训练水平、AI 操控、集体反应、自动跟踪非作战单元等组成的属性集合
        参数：
            awareness {str: Blind-一无所知，Normal-普通水平，AutoSideID-知其属方，AutoSideAndUnitID-知其属方与单元，
                        OMNI-无所不知}
            proficiency {str: Novice-新手，Cadet-初级，Regular-普通，Veteran-老手，Ace-顶级}
            is_ai_only 推演方是否由计算机扮演 {str: 'true'-是，'false'-否}
            is_coll_response 推演方是否集体反应 {str: 'true'-是，'false'-否}
            is_auto_track_civs 推演方是否自动跟踪非作战单元 {str: 'true'-是，'false'-否}
        返回：None, 'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修改：张志高 2021-8-21
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        update_str = ''
        if awareness:
            update_str += f", awareness='{awareness}'"
        if proficiency:
            update_str += f", proficiency='{proficiency}'"
        if is_ai_only:
            update_str += f", isAIOnly={is_ai_only}"
        if is_coll_response:
            update_str += f", isCollRespons={is_coll_response}"
        if is_auto_track_civs:
            update_str += f", isAutoTrackCivs='{is_auto_track_civs}'"
        if not update_str:
            return None
        lua_script = f"ScenEdit_SetSideOptions({{side='{self.strName}'{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def get_side_options(self):
        """
        功能：获取推演方属性
        参数：无
        返回：None 或 推演方属性字典
            example: {'proficiency': 'Regular', 'side': '红方',
                    'guid': 'f40500f8-dbde-4b02-9190-a8453a922c98', 'awareness': 'Normal'}
        作者：赵俊义
        修改：张志高 2021-8-21
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        lua_script = f"print(ScenEdit_GetSideOptions({{side='{self.strName}'}}))"
        return_str = self.mozi_server.send_and_recv(lua_script)
        if self.strName in return_str:
            return self.__convert_lua_obj_to_dict(return_str)
        return None

    def get_side_is_human(self):
        """
        功能：获取推演方操控属性，以便判断该推演方是人操控还是计算机操控
        参数：无
        返回：str:  Yes-推演方由人操控 or No-推演方只由计算机扮演
        作者：赵俊义
        修改：张志高 2021-8-21
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        lua_script = f"print(ScenEdit_GetSideIsHuman('{self.strName}'))"
        return_str = self.mozi_server.send_and_recv(lua_script)
        if 'Yes' in return_str:
            return 'Yes'
        if 'No' in return_str:
            return 'No'
        return return_str

    def remove_zone(self, zone_guid):
        """
        功能：删除指定推演方的指定禁航区或封锁区
        参数：
            zone_guid {str: 区域guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修改：张志高 2021-8-21
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        return self.mozi_server.send_and_recv("Hs_ScenEdit_RemoveZone('{}','{}')".format(self.strName, zone_guid))

    def delete_reference_point(self, pnt_guid):
        """
        功能：删除参考点
        参数：
            pnt_guid {str: 参考点guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        set_str = 'ScenEdit_DeleteReferencePoint({side="%s",guid="%s"})' % (self.strGuid, pnt_guid)
        return self.mozi_server.send_and_recv(set_str)

    def delete_reference_point_by_name(self, rp_name):
        """
        功能：按参考点名称删除参考点
        参数：
            rp_name {str: 参考点名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-21
        """
        set_str = 'ScenEdit_DeleteReferencePoint({side="%s",name="%s"})' % (self.strGuid, rp_name)
        return self.mozi_server.send_and_recv(set_str)

    def add_plan_way(self, way_type, way_name):
        """
        功能：为指定推演方添加一预设航线（待指定航路点）
        参数：
            way_type 航线类型 {int: 0-单元航线，1-武器航线}
            way_name {str: 航线名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        return self.mozi_server.send_and_recv("Hs_AddPlanWay('{}',{},'{}')".format(self.strName, way_type, way_name))

    def set_plan_way_showing_status(self, way_name_or_id, is_show):
        """
        功能：控制预设航线的显示或隐藏
        参数：
            way_name_or_id {str: 航线名称或guid}
            is_show 是否显示 {str: true-显示，false-隐藏}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        return self.mozi_server.send_and_recv(
            "Hs_PlanWayIsShow('{}','{}',{})".format(self.strGuid, way_name_or_id, is_show))

    def rename_plan_way(self, way_name_or_id, new_name):
        """
        功能：修改预设航线的名称
        参数：
            way_name_or_id {str: 航线名称或guid}
            new_name {str: 新的航线名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        return self.mozi_server.send_and_recv(
            "Hs_RenamePlanWay('{}','{}','{}')".format(self.strGuid, way_name_or_id, new_name))

    def add_plan_way_point(self, way_name_or_id, lon, lat):
        """
        功能：为预设航线添加航路点
        参数：
            way_name_or_id {str: 航线名称或guid}
            lon {float: 经度}
            lat {float: 纬度}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        return self.mozi_server.send_and_recv(
            "Hs_AddPlanWayPoint('{}','{}',{},{})".format(self.strGuid, way_name_or_id, lon,
                                                         lat))

    def update_plan_way_point(self, strWayNameOrID, strWayPointID, table):
        """
        作者: 赵俊义
        日期：2020-3-11
        函数功能：修改航路点信息  # 未找到航路点ID的获取方式
        函数类型：推演函数
        :param strWayNameOrID: 预设航线的名称或者GUID
        :param strWayPointID: 航路点的GUID
        :param table: 航路点的信息 {NAME='12',LONGITUDE = 12.01,LATITUDE=56.32,ALTITUDE=1(为0-7的数值)，THROTTLE = 1(为0-5
                      的数值)，RADAR= 1(为0-2的数值),SONAR=1(为0-2的数值) ,OECM=1(为0-2的数值)},可根据需要自己构造
        :return:
        """
        return self.mozi_server.send_and_recv(
            "Hs_UpDataPlanWayPoint('{}','{}','{}',{})".format(self.strGuid, strWayNameOrID, strWayPointID, table))

    def remove_plan_way_point(self, strWayNameOrID, strWayPointID):
        """
        作者: 赵俊义
        日期：2020-3-11
        函数功能：预设航线删除航路点  # 未找到航路点ID的获取方式
        函数类型：推演函数
        :param strWayNameOrID: 预设航线名称或者GUID
        :param strWayPointID: 航路点的ID
        :return:
        """
        return self.mozi_server.send_and_recv(
            "Hs_RemovePlanWayPoint('{}','{}','{}')".format(self.strGuid, strWayNameOrID, strWayPointID))

    def remove_plan_way(self, way_name_or_id):
        """
        功能：删除预设航线
        参数：
            way_name_or_id {str: 航线名称或guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        return self.mozi_server.send_and_recv("Hs_RemovePlanWay('{}','{}')".format(self.strGuid, way_name_or_id))

    def edit_brief(self, briefing):
        """
        功能：修改指定推演方的任务简报
        参数：
            briefing {str: 任务简报}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-12
        """
        return self.mozi_server.send_and_recv("Hs_EditBriefing('{}','{}')".format(self.strGuid, briefing))

    def is_target_existed(self, target_name):
        """
        功能：检查目标是否存在
        参数：
            target_name {str: 目标名称}
        返回：bool: True-存在，False-不存在
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-12
        """
        ret = self.get_guid_from_name(target_name, self.contacts)
        if ret:
            return True
        return False

    @staticmethod
    def get_guid_from_name(_name, _dic):
        """
        功能：通过名字查找guid
        参数：
            _name {str: 对象名称}
            _dic {字典：key为对象guid，value为对象实例}
        返回：对象guid
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-12
        """
        for key, value in _dic.items():
            if _name in value.strName:
                return key
        return None

    def hold_position_all_units(self, status):
        """
        功能：保持所有单元阵位，所有单元停止机动，留在原地
        参数：status: {str: 'true', 'false'}
        返回：执行成功与否
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/26/20
        """
        cmd = "Hs_HoldPositonAllUnit('%s', %s)" % (self.strGuid, status)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def launch_units_in_group(self, unitlist):
        """
        功能：停靠任务编队出航
        参数：unitlist {list: 活动单元对象列表}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        unitlist = [v.strGuid for v in unitlist]
        table = str(unitlist).replace('[', '{').replace(']', '}')
        cmd = "Hs_ScenEdit_DockingOpsGroupOut(%s)" % (table)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def launch_units_abort(self, unitlist):
        """
        功能：停靠任务终止出航
        参数：unitlist {list: 活动单元对象列表}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        unitlist = [v.strGuid for v in unitlist]
        table = str(unitlist).replace('[', '{').replace(']', '}')
        cmd = "Hs_ScenEdit_DockingOpsAbortLaunch(%s)" % (table)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_mark_contact(self, contact_guid, relation):
        """
        功能：设置目标对抗关系
        参数：
            contact_guid: {str: 目标guid}
            relation 目标立场类型 {str: 'F'-友方，'N'-中立，'U'-非友方，'H'-敌方}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/24/20
        """
        lua = "Hs_SetMarkContact('%s', '%s', '%s')" % (self.strName, contact_guid, relation)
        self.mozi_server.send_and_recv(lua)

    def delete_group(self, group_name, remove_child='false'):
        """
        功能：删除编组
        限制：专项赛禁用设置 remove_child='true'
        参数：
            group_name {str: 编组名称}
            remove_child 是否删除编组内子单元 {str: 'true' - 是   'false' - 否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-7-20
        """
        return self.mozi_server.send_and_recv(f"ScenEdit_DeleteUnit({{name='{group_name}', "
                                              f"Removechild={remove_child}}})")

    def add_unit(self, unit_type, name, dbid, latitude, longitude, heading):
        """
        功能：添加单元  # 朝向和高度设置不起作用
        限制：专项赛禁用
        参数：
            unit_type 单元类型 {str: SUB - 潜艇, ship - 舰船, facility - 地面兵力设施, air - 飞机}
            name {str: 单元名称}
            dbid {int: 单元数据库dbid}
            latitude {float: 纬度}
            longitude {float: 经度}
            heading {int, 朝向}
        返回：
            rslt：'lua执行成功' 或 '脚本执行出错'
            obj：创建的活动单元对象
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/26/20
        """
        guid = self.situation.generate_guid()
        cmd = ("HS_LUA_AddUnit({side = '%s', guid = '%s', type = '%s', name = '%s', dbid = %s, latitude = %s, "
               "longitude = %s, heading = %s})"
               % (self.strName, guid, unit_type, name, dbid, latitude, longitude, heading))
        rslt = self.mozi_server.send_and_recv(cmd)
        type_selected = {'SUB': CSubmarine, 'ship': CShip, 'facility': CFacility, 'air': CAircraft}
        obj = None
        if rslt == 'lua执行成功':
            self.mozi_server.throw_into_pool(cmd)
            self.situation.throw_into_pseudo_situ_all_guid(guid)
            obj = type_selected[unit_type](guid, self.mozi_server, self.situation)
            obj.strName = name
            obj.iDBID = dbid
            obj.dLatitude = latitude
            obj.dLongitude = longitude
            obj.fCurrentHeading = heading
        return rslt, obj

    def add_submarine(self, name, dbid, latitude, longitude, heading):
        """
        功能：添加潜艇  # 朝向和高度设置不起作用
        限制：专项赛禁用
        参数：
            name {str: 单元名称}
            dbid {int: 单元数据库dbid}
            latitude {float: 纬度}
            longitude {float: 经度}
            heading {int, 朝向}
        返回：
            rslt：'lua执行成功' 或 '脚本执行出错'
            obj：创建的活动单元对象
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/26/20
        """
        guid = self.situation.generate_guid()
        cmd = ("HS_LUA_AddUnit({type = 'SUB', name = '%s', guid = '%s', heading = %s, dbid = %s, "
               "side = '%s', latitude=%s, longitude=%s})"
               % (name, guid, heading, dbid, self.strName, latitude, longitude))
        rslt = self.mozi_server.send_and_recv(cmd)
        obj = None
        if rslt == 'lua执行成功':
            self.mozi_server.throw_into_pool(cmd)
            self.situation.throw_into_pseudo_situ_all_guid(guid)
            obj = CSubmarine(guid, self.mozi_server, self.situation)
            obj.strName = name
            obj.iDBID = dbid
            obj.dLatitude = latitude
            obj.dLongitude = longitude
            obj.fCurrentHeading = heading
        return rslt, obj

    def add_ship(self, name, dbid, latitude, longitude, heading):
        """
        功能：添加舰船 # 朝向和高度设置不起作用
        限制：专项赛禁用
        参数：
            name {str: 单元名称}
            dbid {int: 单元数据库dbid}
            latitude {float: 纬度}
            longitude {float: 经度}
            heading {int, 朝向}
        返回：
            rslt：'lua执行成功' 或 '脚本执行出错'
            obj：创建的活动单元对象
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/26/20
        """
        guid = self.situation.generate_guid()
        print(guid)
        cmd = ("HS_LUA_AddUnit({type = 'ship', name = '%s', guid = '%s', heading = %s, dbid = %s, "
               "side = '%s', latitude=%s, longitude=%s})"
               % (name, guid, heading, dbid, self.strName, latitude, longitude))
        rslt = self.mozi_server.send_and_recv(cmd)
        obj = None
        if rslt == 'lua执行成功':
            self.mozi_server.throw_into_pool(cmd)
            self.situation.throw_into_pseudo_situ_all_guid(guid)
            obj = CShip(guid, self.mozi_server, self.situation)
            obj.strName = name
            obj.iDBID = dbid
            obj.dLatitude = latitude
            obj.dLongitude = longitude
            obj.fCurrentHeading = heading
        return rslt, obj

    def add_facility(self, name, dbid, latitude, longitude, heading):
        """
        功能：添加地面兵力设施  # 朝向设置不起作用
        限制：专项赛禁用
        参数：
            name {str: 单元名称}
            dbid {int: 单元数据库dbid}
            latitude {float: 纬度}
            longitude {float: 经度}
            heading {int, 朝向}
        返回：
            rslt：'lua执行成功' 或 '脚本执行出错'
            obj：创建的活动单元对象
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/26/20
        """
        guid = self.situation.generate_guid()
        cmd = ("HS_LUA_AddUnit({type = 'facility', name = '%s', guid = '%s', heading = %s, dbid = %s, "
               "side = '%s', latitude=%s, longitude=%s})"
               % (name, guid, heading, dbid, self.strName, latitude, longitude))
        rslt = self.mozi_server.send_and_recv(cmd)
        obj = None
        if rslt == 'lua执行成功':
            self.mozi_server.throw_into_pool(cmd)
            self.situation.throw_into_pseudo_situ_all_guid(guid)
            obj = CFacility(guid, self.mozi_server, self.situation)
            obj.strName = name
            obj.iDBID = dbid
            obj.dLatitude = latitude
            obj.dLongitude = longitude
            obj.fCurrentHeading = heading
        return rslt, obj

    def add_aircraft(self, name, dbid, loadoutid, latitude, longitude, altitude, heading):
        """
        功能：添加飞机  # 高度和朝向设置不起作用
        限制：专项赛禁用
        参数：
            name {str: 单元名称}
            dbid {int: 单元数据库dbid}
            loadoutid {int: 挂载dbid}
            latitude {float: 纬度}
            longitude {float: 经度}
            altitude {float: 高度，单位：米}
            heading {int, 朝向}
        返回：
            rslt：'lua执行成功' 或 '脚本执行出错'
            创建的活动单元对象 或 None
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/26/20
        """
        guid = self.situation.generate_guid()
        cmd = ("HS_LUA_AddUnit({type = 'air', name = '%s', guid = '%s', loadoutid = %s, heading = %s, dbid = %s, "
               "side = '%s', latitude=%s, longitude=%s, altitude=%s})"
               % (name, guid, loadoutid, heading, dbid, self.strName, latitude, longitude, altitude))
        rslt = self.mozi_server.send_and_recv(cmd)
        obj = None
        if rslt == 'lua执行成功':
            self.mozi_server.throw_into_pool(cmd)
            self.situation.throw_into_pseudo_situ_all_guid(guid)
            obj = CAircraft(guid, self.mozi_server, self.situation)
            obj.strName = name
            obj.iDBID = dbid
            obj.loadout = loadoutid
            obj.dLatitude = latitude
            obj.dLongitude = longitude
            obj.fCurrentAltitude_ASL = altitude
            obj.fCurrentHeading = heading
        return rslt, obj

    def add_satellite(self, satellite_db_guid, orbital):
        """
        功能：添加卫星
        限制：专项赛禁用
        参数：
            satellite_db_guid {str: 卫星db guid}
            orbital {int: 卫星轨道编号}
        返回：
            rslt：'lua执行成功' 或 '脚本执行出错'
            obj：创建的活动单元对象
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：4/26/20
        """
        cmd = "Hs_AddSatellite('{}','{}',{})".format(self.strName, satellite_db_guid, orbital)
        rslt = self.mozi_server.send_and_recv(cmd)
        obj = None
        if rslt == 'lua执行成功':
            self.mozi_server.throw_into_pool(cmd)
            obj = CSatellite('generate-obj-for-cmd-operation', self.mozi_server, self.situation)
            obj.iDBID = satellite_db_guid
            obj.m_TracksPoints = orbital
        return rslt, obj

    def import_inst_file(self, filename):
        """
        导入 inst 文件  # 具体用法待确定
        限制：专项赛禁用
        side string 导入 inst 文件的阵营
        filename string inst 文件名
        """
        return self.mozi_server.send_and_recv("ScenEdit_ImportInst('{}','{}')".format(self.strName, filename))

    def import_mission(self, mission_name):
        """
        作者：赵俊义  # 具体用法待确定
        限制：专项赛禁用
        日期：2020-3-10
        函数功能：从 Defaults 文件夹中查找对应的任务，导入到想定中
        函数类型：推演函数
        :return:
        """
        return self.mozi_server.send_and_recv("ScenEdit_ImportMission('{}','{}')".format(self.strGuid, mission_name))

    def add_unit_to_facility(self, unit_type, name, dbid, base_unit_guid, loadout_id=None):
        """
        功能：往机场，码头添加单元
        限制：专项赛禁用
        参数：unit_type:{str: facility - 地面兵力设施，sub - 潜艇， ship - 水面舰艇, air - 飞机}
                    facility 当前不支持
            name {str: 单元名称}
            dbid {int: 单元数据库dbid}
            base_unit_guid: {str: 机场、码头单元guid}
            loadout_id 用于添加飞机 {int: 飞机的挂载方案dbid}
        返回：所添加单元的活动单元对象 或 None
        作者：-
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/25/20
        """
        loadout_str = ''
        if loadout_id:
            loadout_str = f", loadoutid={loadout_id}"
        lua_script = f"ReturnObj(ScenEdit_AddUnit({{type='{unit_type}', unitname='{name}',side='{self.strName}', " \
                     f"dbid={dbid}, base='{base_unit_guid}'{loadout_str}}}))"
        return_str = self.mozi_server.send_and_recv(lua_script)

        if 'unit {' in return_str:
            # 将返回的字符串转换成字典
            return_dict = self.__convert_lua_obj_to_dict(return_str)
            self.situation.throw_into_pseudo_situ_all_guid(return_dict['guid'])
            type_selected = {'sub': CSubmarine, 'ship': CShip, 'facility': CFacility, 'air': CAircraft}
            obj = type_selected[unit_type](return_dict['guid'], self.mozi_server, self.situation)
            obj.strName = name
            obj.m_Side = self.strGuid
            obj.m_HostActiveUnit = base_unit_guid
            return obj
        return None

    def delete_all_unit(self):
        """
        功能：删除本方所有单元
        限制：专项赛禁用
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/25/20
        """
        return self.mozi_server.send_and_recv("Hs_DeleteAllUnits('{}')".format(self.strName))

    def deploy_mine(self, mine_db_guid, mine_count, area):
        """
        功能：给某一方添加雷
        限制：专项赛禁用
        参数：
            mine_dbid: {int: 水雷数据库guid}
            mine_count: {int: 水雷数量}
            area {list: 参考点名称列表}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/24/20
        """
        area_str = ''
        for rp in area:
            rp_obj = self.get_reference_point_by_name(rp)
            if rp_obj:
                area_str += f", {{lat={rp_obj.dLatitude}, lon={rp_obj.dLongitude}}}"
        if area_str:
            area_str = area_str[1:]
        lua_script = f"Hs_DeployMine('{self.strName}', '{mine_db_guid}', {mine_count}, {{{area_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def set_new_name(self, new_name):
        """
        功能：推演方重命名
        限制：专项赛禁用
        参数：new_name: {str: 新的推演方名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-19
        单位：北京华戍防务技术有限公司
        时间：4/24/20
        """
        return self.mozi_server.send_and_recv("Hs_SetSideName('{}','{}')".format(self.strName, new_name))

    def set_score(self, score, reason_for_change=''):
        """
        功能：设置推演方总分
        限制：专项赛禁用
        类别：编辑所用函数
        参数：
            score: {int: 推演方总分}
            reason_for_change  {str: 总分变化原因}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-20
        单位：北京华戍防务技术有限公司
        时间：4/24/20
        """
        lua = "ScenEdit_SetScore('%s',%s,'%s')" % (self.strGuid, score, reason_for_change)
        self.mozi_server.send_and_recv(lua)

    def side_scoring(self, scoring_disaster, scoring_triumph):
        """
        功能：设置完胜完败阈值
        限制：专项赛禁用
        类别：编辑所用函数
        参数：
            scoring_disaster: {int: 完败分数线}
            scoring_triumph  {str: 完胜分数线}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修改：张志高 2021-8-20
        单位：北京华戍防务技术有限公司
        时间：2020-3-10
        """
        return self.mozi_server.send_and_recv(
            "Hs_SideScoring('{}','{}','{}')".format(self.strGuid, scoring_disaster, scoring_triumph))

    def copy_unit(self, unit_name, lon, lat):
        """
        功能：将想定中当前推演方中的已有单元复制到指定经纬度处
        限制：专项赛禁用
        参数：
            unit_name {str: 被复制的单元名称}
            lon {float: 经度}
            lat {float: 纬度}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修改：张志高 2021-8-21
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        lua_script = f"Hs_CopyUnit('{unit_name}',{lon},{lat})"
        return self.mozi_server.send_and_recv(lua_script)

    def delete_unit(self, unit_name):
        """
        功能：删除当前推演方中指定单元
        限制：专项赛禁用
        参数：
            unit_name {str: 单元名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        lua_script = f"ScenEdit_DeleteUnit({{name='{unit_name}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def kill_unit(self, unit_name):
        """
        功能：摧毁单元
             摧毁指定推演方的指定单元，并输出该摧毁事件的消息，并影响到战损统计
        限制：专项赛禁用
        参数：
            unit_name {str: 单元名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修改：张志高 2021-8-21
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        lua_script = f"ScenEdit_KillUnit({{side='{self.strName}',name='{unit_name}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_network(self, send_guid, recv_guid, MsgPassProbability, MsgDelayMin, MsgDelayMax):
        """
        功能：给两个单元添加网络
        :param send_guid: 发送方GUID
        :param recv_guid: 接收方GUID
        :param MsgPassProbability: 信息传递成功率 （0-1）之间
        :param MsgDelayMin: 信息最小延迟时间  1 标识 1分钟
        :param MsgDelayMax: 信息最大延迟时间
        :return: 'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-10-13
        """
        lua_script = f'NET_AddTwoUnitNet("{send_guid}","{recv_guid}",{{MsgPassProbability={MsgPassProbability},' \
                     f'MsgDelayMin={MsgDelayMin},MsgDelayMax={MsgDelayMax}}})'
        return self.mozi_server.send_and_recv(lua_script)

    def remove_network(self,send_guid, recv_guid):
        """
        功能：移除两个单元之间的网络
        :param send_guid: 发送方GUID
        :param recv_guid: 接收方GUID
        :return: 'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-10-13
        """
        lua_script = f'NET_RemoveNet("{send_guid}","{recv_guid}")'
        return self.mozi_server.send_and_recv(lua_script)

    def set_network(self,send_guid, recv_guid, MsgPassProbability=None, MsgDelayMin=None, MsgDelayMax=None):
        """
        功能：给两个单元之间的网络设置属性
        :param send_guid: 发送方GUID
        :param recv_guid: 接收方GUID
        :param MsgPassProbability: 信息传递成功率 （0-1）之间
        :param MsgDelayMin: 信息最小延迟时间  1 标识 1分钟
        :param MsgDelayMax: 信息最大延迟时间
        :return: 'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-10-13
        """
        update_str = ''
        if MsgPassProbability:
            update_str += f", MsgPassProbability={MsgPassProbability}"
        if MsgDelayMin:
            update_str += f", MsgDelayMin={MsgDelayMin}"
        if MsgDelayMax:
            update_str += f", MsgDelayMax={MsgDelayMax}"

        if not update_str:
            return None
        else:
            update_str = update_str[1:]
        lua_script = f'NET_ModifyProperty("{send_guid}", "{recv_guid}", {{{update_str}}})'
        return self.mozi_server.send_and_recv(lua_script)

    def set_network_core(self, guid, air_cycle=None,  ship_cycle=None, sub_cycle=None, fac_cycle=None):
        """
        功能：指定两个单元之间的网络哪一个单元为情报中心
        :param guid: 指定为情报中心单元的guid
        :param air_cycle: 情报中心对飞机的下传周期  例：60
        :param ship_cycle: 情报中心对舰艇的下传周期 例：300
        :param sub_cycle: 情报中心对潜艇的下传周期  例：7200
        :param fac_cycle: 情报中心对地面设施的下传周期 例：60
        :return: 'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-10-13
        """
        update_str = ''
        if air_cycle:
            update_str += f", AircraftDownloadCycle={air_cycle}"
        if ship_cycle:
            update_str += f", ShipDownloadCycle={ship_cycle}"
        if sub_cycle:
            update_str += f", SubmarineDownloadCycle={sub_cycle}"
        if fac_cycle:
            update_str +=  f", FacilityDownloadCycle={fac_cycle}"
        if not update_str:
            return None
        else:
            update_str = update_str[1:]
        lua_script = f'NET_SetInforCenter("{guid}", {{{update_str}}})'
        return self.mozi_server.send_and_recv(lua_script)

    def remove_network_core(self,guid):
        """
        功能：移除情报中心
        :param guid: 情报中心的单元guid
        :return: 'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-10-13
        """
        lua_script = f'NET_RemoveInforCenter("{guid}")'
        return self.mozi_server.send_and_recv(lua_script)

    def get_network_contact(self, num):
        """

        :param num: 通过网络获得的目标类型，int类型
         2：获得通过通信网络获得的目标数据
         4：获得本地雷达探测到的目标数据
         6：获得该实体探测到的所有目标数据 （2+4）
        :return:类似于side.contacts 获取所有探测到单元的字典
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-10-13
        """
        lua_script = f'NetWorkContacts({num})'
        return self.mozi_server.send_and_recv(lua_script)