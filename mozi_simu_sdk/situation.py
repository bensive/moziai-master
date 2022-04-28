# -*- coding:utf-8 -*-
##########################################################################################################
# File name : situation.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################8
import logging
import time

import random
import json

from .mozi_server import *
from .doctrine import CDoctrine
from .weather import CWeather
from .side import CSide
from .group import CGroup
from .submarine import CSubmarine
from .ship import CShip
from .facility import CFacility
from .aircraft import CAircraft
from .satellite import CSatellite
from .sensor import CSensor
from .loadout import CLoadout
from .mount import CMount
from .magazine import CMagazine
from .weapon import CWeapon
from .unguidedwpn import CUnguidedWeapon
from .wpnimpact import CWeaponImpact
from .sideway import CSideWay
from .waypoint import CWayPoint
from .contact import CContact
from .loggedmessage import CLoggedMessage
from .simevent import CSimEvent
from .trgunitdtcd import CTriggerUnitDetected
from .trgunitdmgd import CTriggerUnitDamaged
from .trgunitdstrd import CTriggerUnitDestroyed
from .trgpoints import CTriggerPoints
from .trgtime import CTriggerTime
from .trgrglrtime import CTriggerRegularTime
from .trgrndmtime import CTriggerRandomTime
from .trgscenldd import CTriggerScenLoaded
from .trgunitrmns import CTriggerUnitRemainsInArea
from .cndscenhsstrtd import CConditionScenHasStarted
from .cndsidepstr import CConditionSidePosture
from .cndluascrpt import CConditionLuaScript
from .actionmssg import CActionMessage
from .actionpnts import CActionPoints
from .actiontlprt import CActionTeleportInArea
from .actionchngms import CActionChangeMissionStatus
from .actionendscnr import CActionEndScenario
from .actionlscrpt import CActionLuaScript
from .mssnpatrol import CPatrolMission
from .mssnstrike import CStrikeMission
from .mssnsupport import CSupportMission
from .mssncargo import CCargoMission
from .mssnferry import CFerryMission
from .mssnmining import CMiningMission
from .mssnmnclrng import CMineClearingMission
from .referencepoint import CReferencePoint
from .zonenonav import CNoNavZone
from .zonexclsn import CExclusionZone
from .response import CResponse
import mozi_utils.pylog as pylog


class CSituation:
    """
    态势类  专项赛禁用
    """

    def __init__(self, mozi_server):
        """Constructor"""
        # 仿真服务类MoziServer实例
        self.all_guid_delete_info = {}
        self.mozi_server = mozi_server
        # 态势中所有guid
        self.all_guid = []
        # 态势中所有对象组成词典
        self.all_info_dict = {}
        # 态势中所有guid的简要信息
        self.all_guid_info = {}
        # 态势数据中所传各种对象所组成的词典
        self.doctrine_dic = {}
        self.weather = None
        self.side_dic = {}
        self.group_dic = {}
        self.submarine_dic = {}
        self.ship_dic = {}
        self.facility_dic = {}
        self.aircraft_dic = {}
        self.satellite_dic = {}
        self.sensor_dic = {}
        self.loadout_dic = {}
        self.mount_dic = {}
        self.magazine_dic = {}
        self.weapon_dic = {}
        self.unguidedwpn_dic = {}
        self.wpnimpact_dic = {}
        self.sideway_dic = {}
        self.waypoint_dic = {}
        self.contact_dic = {}
        self.logged_messages = {}
        self.simevent_dic = {}
        self.trgunitdtcd_dic = {}
        self.trgunitdmgd_dic = {}
        self.trgunitdstrd_dic = {}
        self.trgpoints_dic = {}
        self.trgtime_dic = {}
        self.trgrglrtime_dic = {}
        self.trgrndmtime_dic = {}
        self.trgscenldd_dic = {}
        self.trgunitrmns_dic = {}
        self.cndscenhsstrtd_dic = {}
        self.cndsidepstr_dic = {}
        self.cndluascrpt_dic = {}
        self.actionmssg_dic = {}
        self.actionpnts_dic = {}
        self.actiontlprt_dic = {}
        self.actionchngms_dic = {}
        self.actionendscnr_dic = {}
        self.actionlscrpt_dic = {}
        self.mssnpatrol_dic = {}
        self.mssnstrike_dic = {}  # by aie
        self.mssnsupport_dic = {}
        self.mssncargo_dic = {}
        self.mssnferry_dic = {}
        self.mssnmining_dic = {}
        self.mssnmnclrng_dic = {}
        self.referencept_dic = {}
        self.zonenonav_dic = {}
        self.zonexclsn_dic = {}
        self.response_dic = {}  # by aie
        # 更新态势标识
        self.update_start = False
        # 态势更新增加的对象guid
        self.all_guid_add_info = {}
        # 当前轮次下的伪态势：为方便仿真操控函数的关联而引入,只用当前一个轮次，每次态势更新要清除掉。
        self.pseudo_situ_all_guid = []
        self.pseudo_situ_all_name = []

    def init_situation(self, mozi_server, scenario, app_mode):
        """获取全局初始态势"""
        # dixit 2020/9/23 调试对战平台
        if app_mode not in [2, 3]:
            load_success = False
            for i in range(50):
                # 向服务器询问，是否想定已加载且打包完成，此处改为IsPacked
                load_result = mozi_server.send_and_recv("IsPacked")
                if load_result == "True":
                    # pylog.info("想定已加载且打包完成！")
                    print("%s：想定已加载且打包完成！" % (datetime.datetime.now()))
                    load_success = True
                    break
                else:
                    # pylog.info("”")
                    print("%s：想定未加载或打包未完成，再等一秒！" % (datetime.datetime.now()))
                    time.sleep(1)

            if not load_success:
                print("%s：服务端超过50秒没有完成打包!" % (datetime.datetime.now()))
                return False

            # 取想定初始态势
            situation_str = mozi_server.send_and_recv("GetAllState")
            print("%s：接收到初始态势数据!" % (datetime.datetime.now()))
            return self.parse_init_situation(situation_str, scenario)
        else:
            # 取想定初始态势
            for i in range(20):
                situation_str = mozi_server.send_and_recv("GetAllState")
                if situation_str != '数据错误':
                    print("%s：接收到初始态势数据!" % (datetime.datetime.now()))
                    print('初始态势数据大小%s' % len(situation_str))
                    return self.parse_init_situation(situation_str, scenario)
                else:
                    print('初始态势数据获取失败，稍等1s')
                    time.sleep(1)
            print(f'模式{app_mode}获取初始态势经过20s后，依然失败')
            return False

    def parse_init_situation(self, situation_str, scenario):
        """
        传入初始获取全局态势字符串，构建本地对象体系框架
        :param situation_str:  str, 初始全局态势字符串
        :return:
        """
        print("%s：开始解析初始态势数据!" % (datetime.datetime.now()))
        try:
            situation_dict = json.loads(situation_str)
            # print(situation_dict)
            self.all_guid = list(situation_dict.keys())
            self.all_info_dict = situation_dict
        except Exception as e:
            pylog.error("Failed to json initial situation' return %s" % e)
            return False
        for key, value in situation_dict.items():
            if value["ClassName"] == "CCurrentScenario":
                self.parse_scenario(value, scenario)
            elif value["ClassName"] == "CDoctrine":  # added by aie
                self.parse_Doctrine(value)
            elif value["ClassName"] == "CWeather":
                self.parse_weather(value)
            elif value["ClassName"] == "CSide":
                self.parse_side(value)
            elif value["ClassName"] == "CGroup":
                self.parse_group(value)
            elif value["ClassName"] == "CSubmarine":
                self.parse_submarine(value)
            elif value["ClassName"] == "CShip":
                self.parse_ship(value)
            elif value["ClassName"] == "CFacility":
                self.parse_facility(value)
            elif value["ClassName"] == "CAircraft":
                self.parse_aircraft(value)
            elif value["ClassName"] == "CSatellite":
                self.parse_satellite(value)
            elif value["ClassName"] == "CSensor":
                self.parse_sensor(value)
            elif value["ClassName"] == "CLoadout":
                self.parse_loadout(value)
            elif value["ClassName"] == "CMount":
                self.parse_mount(value)
            elif value["ClassName"] == "CMagazine":
                self.parse_magazine(value)
            elif value["ClassName"] == "CWeapon":
                self.parse_weapon(value)
            elif value["ClassName"] == "CUnguidedWeapon":
                self.parse_unguidedwpn(value)
            elif value["ClassName"] == "CWeaponImpact":
                self.parse_wpnimpact(value)
            elif value["ClassName"] == "CSideWay":
                self.parse_sideway(value)
            elif value["ClassName"] == "CWayPoint":  # added by aie
                self.parse_waypoint(value)
            elif value["ClassName"] == "CContact":
                self.parse_contact(value)
            elif value["ClassName"] == "CLoggedMessage":
                self.parse_loggedmessage(value)
            elif value["ClassName"] == "CSimEvent":
                self.parse_simEvent(value)
            elif value["ClassName"] == "CTriggerUnitDetected":
                self.parse_trgUnitDtctd(value)
            elif value["ClassName"] == "CTriggerUnitDamaged":
                self.parse_trgUnitDmgd(value)
            elif value["ClassName"] == "CTriggerUnitDestroyed":
                self.parse_trgUnitDstrd(value)
            elif value["ClassName"] == "CTriggerPoints":
                self.parse_trgPoints(value)
            elif value["ClassName"] == "CTriggerTime":
                self.parse_trgTime(value)
            elif value["ClassName"] == "CTriggerRegularTime":
                self.parse_trgRegTime(value)
            elif value["ClassName"] == "CTriggerRandomTime":
                self.parse_trgRndmTime(value)
            elif value["ClassName"] == "CTriggerScenLoaded":
                self.parse_trgScenLdd(value)
            elif value["ClassName"] == "CTriggerUnitRemainsInArea":
                self.parse_trgUnitRmnsInArea(value)
            elif value["ClassName"] == "CConditionScenHasStarted":
                self.parse_cndScenHasStarted(value)
            elif value["ClassName"] == "CConditionSidePosture":
                self.parse_cndSidePosture(value)
            elif value["ClassName"] == "CConditionLuaScript":
                self.parse_cndLuaScript(value)
            elif value["ClassName"] == "CActionMessage":
                self.parse_actnMessage(value)
            elif value["ClassName"] == "CActionPoints":
                self.parse_actnPoints(value)
            elif value["ClassName"] == "CActionTeleportInArea":
                self.parse_actnTlptInArea(value)
            elif value["ClassName"] == "CActionChangeMissionStatus":
                self.parse_actnChngMssnStts(value)
            elif value["ClassName"] == "CActionEndScenario":
                self.parse_actnEndScenario(value)
            elif value["ClassName"] == "CActionLuaScript":
                self.parse_actnLuaScript(value)
            elif value["ClassName"] == "CPatrolMission":
                self.parse_patrolmission(value)
            elif value["ClassName"] == "CStrikeMission":
                self.parse_strikemission(value)
            elif value["ClassName"] == "CSupportMission":
                self.parse_supportmission(value)
            elif value["ClassName"] == "CCargoMission":
                self.parse_cargomission(value)
            elif value["ClassName"] == "CFerryMission":
                self.parse_ferrymission(value)
            elif value["ClassName"] == "CMiningMission":
                self.parse_mnngmission(value)
            elif value["ClassName"] == "CMineClearingMission":
                self.parse_mnclrngmission(value)
            elif value["ClassName"] == "CReferencePoint":
                self.parse_referencePoint(value)
            elif value["ClassName"] == "CNoNavZone":
                self.parse_nonavzone(value)
            elif value["ClassName"] == "CExclusionZone":
                self.parse_xclsnzone(value)
            elif value["ClassName"] == "CResponse":  # by aie
                self.parse_response(value)

        print("%s：完成解析初始态势数据!" % (datetime.datetime.now()))

    def update_situation(self, mozi_server, scenario, app_mode):
        """
        获取更新态势
        :return:
        """
        if app_mode == 3:
            # 此线程接收数据
            from mozi_simu_sdk import mozi_server as mozi
            q = mozi.q
            start_time = time.time()
            while q.qsize() == 0:
                time.sleep(0.01)
                end_time = time.time()
                if end_time - start_time > 60:
                    print('获取更新态势数据超时')
                    raise Exception('获取更新态势数据超时')
            while q.qsize() > 0:
                # print('更新开始')
                self.update_start = True
                self.all_guid_add_info = {}
                self.pseudo_situ_all_guid = []
                self.pseudo_situ_all_name = []
                # print(f'获取到态势数据, {q.qsize()}个')
                update_data = q.get()
                # print(f'get后的队列大小, {q.qsize()}个')
                if not update_data == 'Blank info from MZ':
                    # print(f"更新的态势数据{update_data}")
                    self.parse_update_situation(update_data, scenario)
                    # print(f"更新完成")
                    self.update_start = False
                    # 态势更新完成
                    for k, side in self.side_dic.items():
                        side.static_update()
            # print(f'解析态势数据完成')
        else:
            self.update_start = True
            self.all_guid_add_info = {}
            self.pseudo_situ_all_guid = []
            self.pseudo_situ_all_name = []
            update_data = mozi_server.send_and_recv("UpdateState")
            situation_data = self.parse_update_situation(update_data, scenario)
            self.update_start = False
            return situation_data

    def parse_update_situation(self, update_data, scenario):
        """
        传入更新的态势字符串，解析后更新到本地框架对象中
        :param update_data: str, 更新的态势字符串
        :param scenario: 想定文件
        :return:
        """
        if isinstance(update_data, str):
            try:
                situation_data = json.loads(update_data.strip())
            except Exception as e:
                pylog.error("Failed to json update situation's resturn:%s" % e)
                return
        else:
            situation_data = update_data
        for key, value in situation_data.items():
            if value["ClassName"] == "CCurrentScenario":
                self.parse_scenario(value, scenario)
            elif value["ClassName"] == "CDoctrine":  # added by aie
                self.parse_Doctrine(value)
            elif value["ClassName"] == "CWeather":
                self.parse_weather(value)
            elif value["ClassName"] == "CSide":
                self.parse_side(value)
            elif value["ClassName"] == "CGroup":
                self.parse_group(value)
            elif value["ClassName"] == "CSubmarine":
                self.parse_submarine(value)
            elif value["ClassName"] == "CShip":
                self.parse_ship(value)
            elif value["ClassName"] == "CFacility":
                self.parse_facility(value)
            elif value["ClassName"] == "CAircraft":
                self.parse_aircraft(value)
            elif value["ClassName"] == "CSatellite":
                self.parse_satellite(value)
            elif value["ClassName"] == "CSensor":
                self.parse_sensor(value)
            elif value["ClassName"] == "CLoadout":
                self.parse_loadout(value)
            elif value["ClassName"] == "CMount":
                self.parse_mount(value)
            elif value["ClassName"] == "CMagazine":
                self.parse_magazine(value)
            elif value["ClassName"] == "CWeapon":
                self.parse_weapon(value)
            elif value["ClassName"] == "CUnguidedWeapon":
                self.parse_unguidedwpn(value)
            elif value["ClassName"] == "CWeaponImpact":
                self.parse_wpnimpact(value)
            elif value["ClassName"] == "CSideWay":
                self.parse_sideway(value)
            elif value["ClassName"] == "CWayPoint":  # added by aie
                self.parse_waypoint(value)
            elif value["ClassName"] == "CContact":
                self.parse_contact(value)
            elif value["ClassName"] == "CLoggedMessage":
                self.parse_loggedmessage(value)
            elif value["ClassName"] == "CSimEvent":
                self.parse_simEvent(value)
            elif value["ClassName"] == "CTriggerUnitDetected":
                self.parse_trgUnitDtctd(value)
            elif value["ClassName"] == "CTriggerUnitDamaged":
                self.parse_trgUnitDmgd(value)
            elif value["ClassName"] == "CTriggerUnitDestroyed":
                self.parse_trgUnitDstrd(value)
            elif value["ClassName"] == "CTriggerPoints":
                self.parse_trgPoints(value)
            elif value["ClassName"] == "CTriggerTime":
                self.parse_trgTime(value)
            elif value["ClassName"] == "CTriggerRegularTime":
                self.parse_trgRegTime(value)
            elif value["ClassName"] == "CTriggerRandomTime":
                self.parse_trgRndmTime(value)
            elif value["ClassName"] == "CTriggerScenLoaded":
                self.parse_trgScenLdd(value)
            elif value["ClassName"] == "CTriggerUnitRemainsInArea":
                self.parse_trgUnitRmnsInArea(value)
            elif value["ClassName"] == "CConditionScenHasStarted":
                self.parse_cndScenHasStarted(value)
            elif value["ClassName"] == "CConditionSidePosture":
                self.parse_cndSidePosture(value)
            elif value["ClassName"] == "CConditionLuaScript":
                self.parse_cndLuaScript(value)
            elif value["ClassName"] == "CActionMessage":
                self.parse_actnMessage(value)
            elif value["ClassName"] == "CActionPoints":
                self.parse_actnPoints(value)
            elif value["ClassName"] == "CActionTeleportInArea":
                self.parse_actnTlptInArea(value)
            elif value["ClassName"] == "CActionChangeMissionStatus":
                self.parse_actnChngMssnStts(value)
            elif value["ClassName"] == "CActionEndScenario":
                self.parse_actnEndScenario(value)
            elif value["ClassName"] == "CActionLuaScript":
                self.parse_actnLuaScript(value)
            elif value["ClassName"] == "CPatrolMission":
                self.parse_patrolmission(value)
            elif value["ClassName"] == "CStrikeMission":
                self.parse_strikemission(value)
            elif value["ClassName"] == "CSupportMission":
                self.parse_supportmission(value)
            elif value["ClassName"] == "CCargoMission":
                self.parse_cargomission(value)
            elif value["ClassName"] == "CFerryMission":
                self.parse_ferrymission(value)
            elif value["ClassName"] == "CMiningMission":
                self.parse_mnngmission(value)
            elif value["ClassName"] == "CMineClearingMission":
                self.parse_mnclrngmission(value)
            elif value["ClassName"] == "CReferencePoint":
                self.parse_referencePoint(value)
            elif value["ClassName"] == "CNoNavZone":
                self.parse_nonavzone(value)
            elif value["ClassName"] == "CExclusionZone":
                self.parse_xclsnzone(value)
            elif value["ClassName"] == "CResponse":  # by aie
                self.parse_response(value)
            elif value["ClassName"] == "Delete":
                self.parse_delete(value)

        return situation_data

    # 以下为各态势对象的解析函数parse_XXX

    def parse_scenario(self, scenario_json, scenario):
        scenario.__dict__.update(scenario_json)  # changed by aie

    def parse_Doctrine(self, doctrine_json):
        # reconstructed by aie
        strGuid = doctrine_json['strGuid']
        if strGuid not in self.all_guid_info:
            doctrine = CDoctrine(strGuid, self.mozi_server, self)
            doctrine.__dict__.update(doctrine_json)  # changed by aie
            self.all_guid_info[strGuid] = {"strType": 1002}
            self.all_guid.append(strGuid)
            self.doctrine_dic[strGuid] = doctrine
        else:
            self.doctrine_dic[strGuid].__dict__.update(doctrine_json)

    def parse_weather(self, weather_json):
        weather = CWeather(self.mozi_server, self)
        weather.__dict__.update(weather_json)  # changed by aie
        self.weather = weather

    def parse_side(self, side_json):
        # reconstructed by aie
        strGuid = side_json["strGuid"]
        if strGuid not in self.all_guid_info:
            side = CSide(strGuid, self.mozi_server, self)
            side.__dict__.update(side_json)
            self.all_guid_info[strGuid] = {"strType": 1004}
            self.all_guid.append(strGuid)
            self.side_dic[strGuid] = side
        else:
            self.side_dic[strGuid].__dict__.update(side_json)

    def parse_group(self, group_json):
        # reconstructed by aie
        strGuid = group_json["strGuid"]
        if strGuid not in self.all_guid_info:
            group = CGroup(strGuid, self.mozi_server, self)
            group.__dict__.update(group_json)
            self.all_guid_info[strGuid] = {"strType": 1005, "side": group.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.group_dic[strGuid] = group
        else:
            self.group_dic[strGuid].__dict__.update(group_json)

    def parse_submarine(self, submarine_json):
        # reconstructed by aie
        strGuid = submarine_json["strGuid"]
        if strGuid not in self.all_guid_info:
            submarine = CSubmarine(strGuid, self.mozi_server, self)
            submarine.__dict__.update(submarine_json)
            self.all_guid_info[strGuid] = {"strType": 2001, "side": submarine.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.submarine_dic[strGuid] = submarine
        else:
            self.submarine_dic[strGuid].__dict__.update(submarine_json)

    def parse_ship(self, ship_json):
        # reconstructed by aie
        strGuid = ship_json["strGuid"]
        if strGuid not in self.all_guid_info:
            ship = CShip(strGuid, self.mozi_server, self)
            ship.__dict__.update(ship_json)
            self.all_guid_info[strGuid] = {"strType": 2002, "side": ship.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.ship_dic[strGuid] = ship
        else:
            self.ship_dic[strGuid].__dict__.update(ship_json)

    def parse_facility(self, facility_json):
        # reconstructed by aie
        strGuid = facility_json["strGuid"]
        if strGuid not in self.all_guid_info:
            facility = CFacility(strGuid, self.mozi_server, self)
            facility.__dict__.update(facility_json)
            self.all_guid_info[strGuid] = {"strType": 2003, "side": facility.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.facility_dic[strGuid] = facility
        else:
            self.facility_dic[strGuid].__dict__.update(facility_json)

    def parse_aircraft(self, aircraft_json):
        # reconstructed by aie
        strGuid = aircraft_json["strGuid"]
        if strGuid not in self.all_guid_info:
            aircraft = CAircraft(strGuid, self.mozi_server, self)
            aircraft.__dict__.update(aircraft_json)
            self.all_guid_info[strGuid] = {"strType": 2004, "side": aircraft.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.aircraft_dic[strGuid] = aircraft
        else:
            self.aircraft_dic[strGuid].__dict__.update(aircraft_json)

    def parse_satellite(self, satellite_json):
        # reconstructed by aie
        strGuid = satellite_json["strGuid"]
        if strGuid not in self.all_guid_info:
            satellite = CSatellite(strGuid, self.mozi_server, self)
            satellite.__dict__.update(satellite_json)
            self.all_guid_info[strGuid] = {"strType": 2005, "side": satellite.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.satellite_dic[strGuid] = satellite
        else:
            self.satellite_dic[strGuid].__dict__.update(satellite_json)

    def parse_sensor(self, sensor_json):
        # reconstructed by aie
        strGuid = sensor_json["strGuid"]
        if strGuid not in self.all_guid_info:
            sensor = CSensor(strGuid, self.mozi_server, self)
            sensor.__dict__.update(sensor_json)
            self.all_guid_info[strGuid] = {"strType": 3001}
            self.all_guid.append(strGuid)
            self.sensor_dic[strGuid] = sensor
        else:
            self.sensor_dic[strGuid].__dict__.update(sensor_json)

    def parse_loadout(self, loadout_json):
        # reconstructed by aie
        strGuid = loadout_json["strGuid"]
        if strGuid not in self.all_guid_info:
            loadout = CLoadout(strGuid, self.mozi_server, self)
            loadout.__dict__.update(loadout_json)
            self.all_guid_info[strGuid] = {"strType": 3002}
            self.all_guid.append(strGuid)
            self.loadout_dic[strGuid] = loadout
        else:
            self.loadout_dic[strGuid].__dict__.update(loadout_json)

    def parse_mount(self, mount_json):
        # reconstructed by aie
        strGuid = mount_json["strGuid"]
        if strGuid not in self.all_guid_info:
            mount = CMount(strGuid, self.mozi_server, self)
            mount.__dict__.update(mount_json)
            self.all_guid_info[strGuid] = {"strType": 3003}
            self.all_guid.append(strGuid)
            self.mount_dic[strGuid] = mount
        else:
            self.mount_dic[strGuid].__dict__.update(mount_json)

    def parse_magazine(self, magazine_json):
        # reconstructed by aie
        strGuid = magazine_json["strGuid"]
        if strGuid not in self.all_guid_info:
            magazine = CMagazine(strGuid, self.mozi_server, self)
            magazine.__dict__.update(magazine_json)
            self.all_guid_info[strGuid] = {"strType": 3004}
            self.all_guid.append(strGuid)
            self.magazine_dic[strGuid] = magazine
        else:
            self.magazine_dic[strGuid].__dict__.update(magazine_json)

    def parse_weapon(self, weapon_json):
        # reconstructed by aie
        strGuid = weapon_json["strGuid"]
        if strGuid not in self.all_guid_info:
            weapon = CWeapon(strGuid, self.mozi_server, self)
            weapon.__dict__.update(weapon_json)
            self.all_guid_info[strGuid] = {"strType": 3005, "side": weapon.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.weapon_dic[strGuid] = weapon
        else:
            self.weapon_dic[strGuid].__dict__.update(weapon_json)

    def parse_unguidedwpn(self, unguidedwpn_json):
        # constructed by aie
        strGuid = unguidedwpn_json["strGuid"]
        if strGuid not in self.all_guid_info:
            unguidedwpn = CUnguidedWeapon(strGuid, self.mozi_server, self)
            unguidedwpn.__dict__.update(unguidedwpn_json)
            self.all_guid_info[strGuid] = {"strType": 3006, "side": unguidedwpn.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.unguidedwpn_dic[strGuid] = unguidedwpn
        else:
            self.unguidedwpn_dic[strGuid].__dict__.update(unguidedwpn_json)

    def parse_wpnimpact(self, wpnimpact_json):
        # constructed by aie
        strGuid = wpnimpact_json["strGuid"]
        if strGuid not in self.all_guid_info:
            wpnimpact = CWeaponImpact(strGuid, self.mozi_server, self)
            wpnimpact.__dict__.update(wpnimpact_json)
            self.all_guid_info[strGuid] = {"strType": 3007}
            self.all_guid.append(strGuid)
            self.wpnimpact_dic[strGuid] = wpnimpact
        else:
            self.wpnimpact_dic[strGuid].__dict__.update(wpnimpact_json)

    def parse_sideway(self, sideway_json):
        # constructed by aie
        strGuid = sideway_json["strGuid"]
        if strGuid not in self.all_guid_info:
            sideway = CSideWay(strGuid, self.mozi_server, self)
            sideway.__dict__.update(sideway_json)
            self.all_guid_info[strGuid] = {"strType": 3008, "side": sideway.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.sideway_dic[strGuid] = sideway
        else:
            self.sideway_dic[strGuid].__dict__.update(sideway_json)

    def parse_waypoint(self, waypoint_json):
        # reconstructed by aie
        strGuid = waypoint_json["strGuid"]
        if strGuid not in self.all_guid_info:
            waypoint = CWayPoint(strGuid, self.mozi_server, self)
            waypoint.__dict__.update(waypoint_json)
            self.all_guid_info[strGuid] = {"strType": 3009}
            self.all_guid.append(strGuid)
            self.waypoint_dic[strGuid] = waypoint
        else:
            # m_ActiveUnit = waypoint_json["m_ActiveUnit"]
            self.waypoint_dic[strGuid].__dict__.update(waypoint_json)

    def parse_contact(self, contact_json):
        # reconstructed by aie
        strGuid = contact_json["strGuid"]
        if strGuid not in self.all_guid_info:
            contact = CContact(strGuid, self.mozi_server, self)
            contact.__dict__.update(contact_json)  # changed by aie
            self.all_guid_info[strGuid] = {"strType": 4001, "side": contact.m_OriginalDetectorSide}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.contact_dic[strGuid] = contact
        else:
            self.contact_dic[strGuid].__dict__.update(contact_json)

    def parse_loggedmessage(self, loggedmessage_json):
        # reconstructed by aie
        strGuid = loggedmessage_json["strGuid"]
        if strGuid not in self.all_guid_info:
            loggedmessage = CLoggedMessage(strGuid)
            loggedmessage.__dict__.update(loggedmessage_json)
            self.all_guid_info[strGuid] = {"strType": 5001, "side": loggedmessage.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.logged_messages[strGuid] = loggedmessage
        else:
            self.logged_messages[strGuid].__dict__.update(loggedmessage_json)

    def parse_simEvent(self, simEvent_json):
        # reconstructed by aie
        strGuid = simEvent_json["strGuid"]
        if strGuid not in self.all_guid_info:
            simEvent = CSimEvent(strGuid, self.mozi_server, self)
            simEvent.__dict__.update(simEvent_json)
            self.all_guid_info[strGuid] = {"strType": 6001}
            self.all_guid.append(strGuid)
            self.simevent_dic[strGuid] = simEvent
        else:
            self.simevent_dic[strGuid].__dict__.update(simEvent_json)

    def parse_trgUnitDtctd(self, trgunitdtcd_json):
        # reconstructed by aie
        strGuid = trgunitdtcd_json["strGuid"]
        if strGuid not in self.all_guid_info:
            trgunitdtcd = CTriggerUnitDetected(strGuid, self.mozi_server, self)
            trgunitdtcd.__dict__.update(trgunitdtcd_json)
            self.all_guid_info[strGuid] = {"strType": 7001}
            self.all_guid.append(strGuid)
            self.trgunitdtcd_dic[strGuid] = trgunitdtcd
        else:
            self.trgunitdtcd_dic[strGuid].__dict__.update(trgunitdtcd_json)

    def parse_trgUnitDmgd(self, trgunitdmgd_json):
        # reconstructed by aie
        strGuid = trgunitdmgd_json["strGuid"]
        if strGuid not in self.all_guid_info:
            trgunitdmgd = CTriggerUnitDamaged(strGuid, self.mozi_server, self)
            trgunitdmgd.__dict__.update(trgunitdmgd_json)
            self.all_guid_info[strGuid] = {"strType": 7002}
            self.all_guid.append(strGuid)
            self.trgunitdmgd_dic[strGuid] = trgunitdmgd
        else:
            self.trgunitdmgd_dic[strGuid].__dict__.update(trgunitdmgd_json)

    def parse_trgUnitDstrd(self, trgunitdstrd_json):
        # reconstructed by aie
        strGuid = trgunitdstrd_json["strGuid"]
        if strGuid not in self.all_guid_info:
            trgunitdstrd = CTriggerUnitDestroyed(strGuid, self.mozi_server, self)
            trgunitdstrd.__dict__.update(trgunitdstrd_json)
            self.all_guid_info[strGuid] = {"strType": 7003}
            self.all_guid.append(strGuid)
            self.trgunitdstrd_dic[strGuid] = trgunitdstrd
        else:
            self.trgunitdstrd_dic[strGuid].__dict__.update(trgunitdstrd_json)

    def parse_trgPoints(self, trgpoints_json):
        # reconstructed by aie
        strGuid = trgpoints_json["strGuid"]
        if strGuid not in self.all_guid_info:
            trgpoints = CTriggerPoints(strGuid, self.mozi_server, self)
            trgpoints.__dict__.update(trgpoints_json)
            self.all_guid_info[strGuid] = {"strType": 7004}
            self.all_guid.append(strGuid)
            self.trgpoints_dic[strGuid] = trgpoints
        else:
            self.trgpoints_dic[strGuid].__dict__.update(trgpoints_json)

    def parse_trgTime(self, trgtime_json):
        # reconstructed by aie
        strGuid = trgtime_json["strGuid"]
        if strGuid not in self.all_guid_info:
            trgtime = CTriggerTime(strGuid, self.mozi_server, self)
            trgtime.__dict__.update(trgtime_json)
            self.all_guid_info[strGuid] = {"strType": 7005}
            self.all_guid.append(strGuid)
            self.trgtime_dic[strGuid] = trgtime
        else:
            self.trgtime_dic[strGuid].__dict__.update(trgtime_json)

    def parse_trgRegTime(self, trgrglrtime_json):
        # reconstructed by aie
        strGuid = trgrglrtime_json["strGuid"]
        if strGuid not in self.all_guid_info:
            trgrglrtime = CTriggerRegularTime(strGuid, self.mozi_server, self)
            trgrglrtime.__dict__.update(trgrglrtime_json)
            self.all_guid_info[strGuid] = {"strType": 7006}
            self.all_guid.append(strGuid)
            self.trgrglrtime_dic[strGuid] = trgrglrtime
        else:
            self.trgrglrtime_dic[strGuid].__dict__.update(trgrglrtime_json)

    def parse_trgRndmTime(self, trgrndmtime_json):
        # reconstructed by aie
        strGuid = trgrndmtime_json["strGuid"]
        if strGuid not in self.all_guid_info:
            trgrndmtime = CTriggerRandomTime(strGuid, self.mozi_server, self)
            trgrndmtime.__dict__.update(trgrndmtime_json)
            self.all_guid_info[strGuid] = {"strType": 7007}
            self.all_guid.append(strGuid)
            self.trgrndmtime_dic[strGuid] = trgrndmtime
        else:
            self.trgrndmtime_dic[strGuid].__dict__.update(trgrndmtime_json)

    def parse_trgScenLdd(self, trgscenldd_json):
        # reconstructed by aie
        strGuid = trgscenldd_json["strGuid"]
        if strGuid not in self.all_guid_info:
            trgscenldd = CTriggerScenLoaded(strGuid, self.mozi_server, self)
            trgscenldd.__dict__.update(trgscenldd_json)
            self.all_guid_info[strGuid] = {"strType": 7008}
            self.all_guid.append(strGuid)
            self.trgscenldd_dic[strGuid] = trgscenldd
        else:
            self.trgscenldd_dic[strGuid].__dict__.update(trgscenldd_json)

    def parse_trgUnitRmnsInArea(self, trgunitrmns_json):
        # reconstructed by aie
        strGuid = trgunitrmns_json["strGuid"]
        if strGuid not in self.all_guid_info:
            trgunitrmns = CTriggerUnitRemainsInArea(strGuid, self.mozi_server, self)
            trgunitrmns.__dict__.update(trgunitrmns_json)
            self.all_guid_info[strGuid] = {"strType": 7009}
            self.all_guid.append(strGuid)
            self.trgunitrmns_dic[strGuid] = trgunitrmns
        else:
            self.trgunitrmns_dic[strGuid].__dict__.update(trgunitrmns_json)

    def parse_cndScenHasStarted(self, cndscenhsstrtd_json):
        # reconstructed by aie
        strGuid = cndscenhsstrtd_json["strGuid"]
        if strGuid not in self.all_guid_info:
            cndscenhsstrtd = CConditionScenHasStarted(strGuid, self.mozi_server, self)
            cndscenhsstrtd.__dict__.update(cndscenhsstrtd_json)
            self.all_guid_info[strGuid] = {"strType": 8001}
            self.all_guid.append(strGuid)
            self.cndscenhsstrtd_dic[strGuid] = cndscenhsstrtd
        else:
            self.cndscenhsstrtd_dic[strGuid].__dict__.update(cndscenhsstrtd_json)

    def parse_cndSidePosture(self, cndsidepstr_json):
        # reconstructed by aie
        strGuid = cndsidepstr_json["strGuid"]
        if strGuid not in self.all_guid_info:
            cndsidepstr = CConditionSidePosture(strGuid, self.mozi_server, self)
            cndsidepstr.__dict__.update(cndsidepstr_json)
            self.all_guid_info[strGuid] = {"strType": 8002}
            self.all_guid.append(strGuid)
            self.cndsidepstr_dic[strGuid] = cndsidepstr
        else:
            self.cndsidepstr_dic[strGuid].__dict__.update(cndsidepstr_json)

    def parse_cndLuaScript(self, cndluascrpt_json):
        # reconstructed by aie
        strGuid = cndluascrpt_json["strGuid"]
        if strGuid not in self.all_guid_info:
            cndluascrpt = CConditionLuaScript(strGuid, self.mozi_server, self)
            cndluascrpt.__dict__.update(cndluascrpt_json)
            self.all_guid_info[strGuid] = {"strType": 8003}
            self.all_guid.append(strGuid)
            self.cndluascrpt_dic[strGuid] = cndluascrpt
        else:
            self.cndluascrpt_dic[strGuid].__dict__.update(cndluascrpt_json)

    def parse_actnMessage(self, actionmssg_json):
        # reconstructed by aie
        strGuid = actionmssg_json["strGuid"]
        if strGuid not in self.all_guid_info:
            actionmssg = CActionMessage(strGuid, self.mozi_server, self)
            actionmssg.__dict__.update(actionmssg_json)
            self.all_guid_info[strGuid] = {"strType": 9001}
            self.all_guid.append(strGuid)
            self.actionmssg_dic[strGuid] = actionmssg
        else:
            self.actionmssg_dic[strGuid].__dict__.update(actionmssg_json)

    def parse_actnPoints(self, actionpnts_json):
        # reconstructed by aie
        strGuid = actionpnts_json["strGuid"]
        if strGuid not in self.all_guid_info:
            actionpnts = CActionPoints(strGuid, self.mozi_server, self)
            actionpnts.__dict__.update(actionpnts_json)
            self.all_guid_info[strGuid] = {"strType": 9002}
            self.all_guid.append(strGuid)
            self.actionpnts_dic[strGuid] = actionpnts
        else:
            self.actionpnts_dic[strGuid].__dict__.update(actionpnts_json)

    def parse_actnTlptInArea(self, actiontlprt_json):
        # reconstructed by aie
        strGuid = actiontlprt_json["strGuid"]
        if strGuid not in self.all_guid_info:
            actiontlprt = CActionTeleportInArea(strGuid, self.mozi_server, self)
            actiontlprt.__dict__.update(actiontlprt_json)
            self.all_guid_info[strGuid] = {"strType": 9003}
            self.all_guid.append(strGuid)
            self.actiontlprt_dic[strGuid] = actiontlprt
        else:
            self.actiontlprt_dic[strGuid].__dict__.update(actiontlprt_json)

    def parse_actnChngMssnStts(self, actionchngms_json):
        # reconstructed by aie
        strGuid = actionchngms_json["strGuid"]
        if strGuid not in self.all_guid_info:
            actionchngms = CActionChangeMissionStatus(strGuid, self.mozi_server, self)
            actionchngms.__dict__.update(actionchngms_json)
            self.all_guid_info[strGuid] = {"strType": 9004}
            self.all_guid.append(strGuid)
            self.actionchngms_dic[strGuid] = actionchngms
        else:
            self.actionchngms_dic[strGuid].__dict__.update(actionchngms_json)

    def parse_actnEndScenario(self, actionendscnr_json):
        # reconstructed by aie
        strGuid = actionendscnr_json["strGuid"]
        if strGuid not in self.all_guid_info:
            actionendscnr = CActionEndScenario(strGuid, self.mozi_server, self)
            actionendscnr.__dict__.update(actionendscnr_json)
            self.all_guid_info[strGuid] = {"strType": 9005}
            self.all_guid.append(strGuid)
            self.actionendscnr_dic[strGuid] = actionendscnr
        else:
            self.actionendscnr_dic[strGuid].__dict__.update(actionendscnr_json)

    def parse_actnLuaScript(self, actionlscrpt_json):
        # reconstructed by aie
        strGuid = actionlscrpt_json["strGuid"]
        if strGuid not in self.all_guid_info:
            actionlscrpt = CActionLuaScript(strGuid, self.mozi_server, self)
            actionlscrpt.__dict__.update(actionlscrpt_json)
            self.all_guid_info[strGuid] = {"strType": 9006}
            self.all_guid.append(strGuid)
            self.actionlscrpt_dic[strGuid] = actionlscrpt
        else:
            self.actionlscrpt_dic[strGuid].__dict__.update(actionlscrpt_json)

    def parse_patrolmission(self, mssnpatrol_json):
        # reconstructed by aie
        strGuid = mssnpatrol_json["strGuid"]
        if strGuid not in self.all_guid_info:
            mssnpatrol = CPatrolMission(strGuid, self.mozi_server, self)
            mssnpatrol.__dict__.update(mssnpatrol_json)
            self.all_guid_info[strGuid] = {"strType": 10001, "side": mssnpatrol.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.mssnpatrol_dic[strGuid] = mssnpatrol
        else:
            self.mssnpatrol_dic[strGuid].__dict__.update(mssnpatrol_json)

    def parse_strikemission(self, mssnstrike_json):
        # reconstructed by aie
        strGuid = mssnstrike_json["strGuid"]
        if strGuid not in self.all_guid_info:
            mssnstrike = CStrikeMission(strGuid, self.mozi_server, self)
            mssnstrike.__dict__.update(mssnstrike_json)
            self.all_guid_info[strGuid] = {"strType": 10002, "side": mssnstrike.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.mssnstrike_dic[strGuid] = mssnstrike
        else:
            self.mssnstrike_dic[strGuid].__dict__.update(mssnstrike_json)

    def parse_supportmission(self, mssnsupport_json):
        # reconstructed by aie
        strGuid = mssnsupport_json["strGuid"]
        if strGuid not in self.all_guid_info:
            mssnsupport = CSupportMission(strGuid, self.mozi_server, self)
            mssnsupport.__dict__.update(mssnsupport_json)
            self.all_guid_info[strGuid] = {"strType": 10003, "side": mssnsupport.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.mssnsupport_dic[strGuid] = mssnsupport
        else:
            self.mssnsupport_dic[strGuid].__dict__.update(mssnsupport_json)

    def parse_cargomission(self, mssncargo_json):
        # reconstructed by aie
        strGuid = mssncargo_json["strGuid"]
        if strGuid not in self.all_guid_info:
            mssncargo = CCargoMission(strGuid, self.mozi_server, self)
            mssncargo.__dict__.update(mssncargo_json)
            self.all_guid_info[strGuid] = {"strType": 10004, "side": mssncargo.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.mssncargo_dic[strGuid] = mssncargo
        else:
            self.mssncargo_dic[strGuid].__dict__.update(mssncargo_json)

    def parse_ferrymission(self, mssnferry_json):
        # reconstructed by aie
        strGuid = mssnferry_json["strGuid"]
        if strGuid not in self.all_guid_info:
            mssnferry = CFerryMission(strGuid, self.mozi_server, self)
            mssnferry.__dict__.update(mssnferry_json)
            self.all_guid_info[strGuid] = {"strType": 10005, "side": mssnferry.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.mssnferry_dic[strGuid] = mssnferry
        else:
            self.mssnferry_dic[strGuid].__dict__.update(mssnferry_json)

    def parse_mnngmission(self, mssnmining_json):
        # reconstructed by aie
        strGuid = mssnmining_json["strGuid"]
        if strGuid not in self.all_guid_info:
            mssnmining = CMiningMission(strGuid, self.mozi_server, self)
            mssnmining.__dict__.update(mssnmining_json)
            self.all_guid_info[strGuid] = {"strType": 10006, "side": mssnmining.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.mssnmining_dic[strGuid] = mssnmining
        else:
            self.mssnmining_dic[strGuid].__dict__.update(mssnmining_json)

    def parse_mnclrngmission(self, mssnmnclrng_json):
        # reconstructed by aie
        strGuid = mssnmnclrng_json["strGuid"]
        if strGuid not in self.all_guid_info:
            mssnmnclrng = CMineClearingMission(strGuid, self.mozi_server, self)
            mssnmnclrng.__dict__.update(mssnmnclrng_json)
            self.all_guid_info[strGuid] = {"strType": 10007, "side": mssnmnclrng.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.mssnmnclrng_dic[strGuid] = mssnmnclrng
        else:
            self.mssnmnclrng_dic[strGuid].__dict__.update(mssnmnclrng_json)

    def parse_referencePoint(self, referencePoint_json):
        # reconstructed by aie
        strGuid = referencePoint_json["strGuid"]
        if strGuid not in self.all_guid_info:
            referencePoint = CReferencePoint(strGuid, self.mozi_server, self)
            referencePoint.__dict__.update(referencePoint_json)
            self.all_guid_info[strGuid] = {"strType": 11001, "side": referencePoint.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.referencept_dic[strGuid] = referencePoint
        else:
            self.referencept_dic[strGuid].__dict__.update(referencePoint_json)

    def parse_nonavzone(self, zonenonav_json):
        # reconstructed by aie
        strGuid = zonenonav_json["strGuid"]
        if strGuid not in self.all_guid_info:
            zonenonav = CNoNavZone(strGuid, self.mozi_server, self)
            zonenonav.__dict__.update(zonenonav_json)
            self.all_guid_info[strGuid] = {"strType": 11002, "side": zonenonav.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.zonenonav_dic[strGuid] = zonenonav
        else:
            self.zonenonav_dic[strGuid].__dict__.update(zonenonav_json)

    def parse_xclsnzone(self, zonexclsn_json):
        # reconstructed by aie
        strGuid = zonexclsn_json["strGuid"]
        if strGuid not in self.all_guid_info:
            zonexclsn = CExclusionZone(strGuid, self.mozi_server, self)
            zonexclsn.__dict__.update(zonexclsn_json)
            self.all_guid_info[strGuid] = {"strType": 11003, "side": zonexclsn.m_Side}
            if self.update_start:
                self.all_guid_add_info[strGuid] = self.all_guid_info[strGuid]
            self.all_guid.append(strGuid)
            self.zonexclsn_dic[strGuid] = zonexclsn
        else:
            self.zonexclsn_dic[strGuid].__dict__.update(zonexclsn_json)

    #  by aie
    def parse_response(self, response_json):
        # reconstructed by aie
        ID = response_json["ID"]
        if ID not in self.response_dic:
            response = CResponse(ID)
            response.__dict__.update(response_json)
            self.all_guid_info[ID] = {"strType": 11004}
            self.all_guid.append(ID)
            self.response_dic[ID] = response
        else:
            self.response_dic[ID].__dict__.update(response_json)

    def parse_delete(self, delete_json):
        """
        删除对象
        添加了side准静态成员的删除机制 by aie
        """
        guid = delete_json["strGuid"]
        if guid in self.all_guid_info:
            guid_info = self.all_guid_info[guid]
            self.all_guid_info.pop(guid)
            if guid in self.all_guid:
                self.all_guid.remove(guid)
            strType = guid_info["strType"]
            if strType == 1002:
                self.doctrine_dic.pop(guid)
                return
            if strType == 1004:
                self.side_dic.pop(guid)
                return
            if strType == 1005:
                self.all_guid_delete_info[guid] = {"strType": 1005, "side": self.group_dic[guid].m_Side}
                self.group_dic.pop(guid)
                return
            if strType == 2001:
                self.all_guid_delete_info[guid] = {"strType": 2001, "side": self.submarine_dic[guid].m_Side}
                self.submarine_dic.pop(guid)
                return
            if strType == 2002:
                self.all_guid_delete_info[guid] = {"strType": 2002, "side": self.ship_dic[guid].m_Side}
                self.ship_dic.pop(guid)
                return
            if strType == 2003:
                self.all_guid_delete_info[guid] = {"strType": 2003, "side": self.facility_dic[guid].m_Side}
                self.facility_dic.pop(guid)
                return
            if strType == 2004:
                self.all_guid_delete_info[guid] = {"strType": 2004, "side": self.aircraft_dic[guid].m_Side}
                self.aircraft_dic.pop(guid)
                return
            if strType == 2005:
                self.all_guid_delete_info[guid] = {"strType": 2005, "side": self.satellite_dic[guid].m_Side}
                self.satellite_dic.pop(guid)
                return
            if strType == 3001:
                self.sensor_dic.pop(guid)
                return
            if strType == 3002:
                self.loadout_dic.pop(guid)
                return
            if strType == 3003:
                self.mount_dic.pop(guid)
                return
            if strType == 3004:
                self.magazine_dic.pop(guid)
                return
            if strType == 3005:
                self.all_guid_delete_info[guid] = {"strType": 3005, "side": self.weapon_dic[guid].m_Side}
                self.weapon_dic.pop(guid)
                return
            if strType == 3006:
                self.all_guid_delete_info[guid] = {"strType": 3006, "side": self.unguidedwpn_dic[guid].m_Side}
                self.unguidedwpn_dic.pop(guid)
                return
            if strType == 3007:
                self.wpnimpact_dic.pop(guid)
                return
            if strType == 3008:
                self.all_guid_delete_info[guid] = {"strType": 3008, "side": self.sideway_dic[guid].m_Side}
                self.sideway_dic.pop(guid)
                return
            if strType == 3009:
                self.waypoint_dic.pop(guid)
                return
            if strType == 4001:
                self.all_guid_delete_info[guid] = {"strType": 4001,
                                                   "side": self.contact_dic[guid].m_OriginalDetectorSide}
                self.contact_dic.pop(guid)
                return
            if strType == 5001:
                self.all_guid_delete_info[guid] = {"strType": 5001, "side": self.logged_messages[guid].m_Side}
                self.logged_messages.pop(guid)
                return
            if strType == 6001:
                self.simevent_dic.pop(guid)
                return
            if strType == 7001:
                self.trgunitdtcd_dic.pop(guid)
                return
            if strType == 7002:
                self.trgunitdmgd_dic.pop(guid)
                return
            if strType == 7003:
                self.trgunitdstrd_dic.pop(guid)
                return
            if strType == 7004:
                self.trgpoints_dic.pop(guid)
                return
            if strType == 7005:
                self.trgtime_dic.pop(guid)
                return
            if strType == 7006:
                self.trgrglrtime_dic.pop(guid)
                return
            if strType == 7007:
                self.trgrndmtime_dic.pop(guid)
                return
            if strType == 7008:
                self.trgscenldd_dic.pop(guid)
                return
            if strType == 7009:
                self.trgunitrmns_dic.pop(guid)
                return
            if strType == 8001:
                self.cndscenhsstrtd_dic.pop(guid)
                return
            if strType == 8002:
                self.cndsidepstr_dic.pop(guid)
                return
            if strType == 8003:
                self.cndluascrpt_dic.pop(guid)
                return
            if strType == 9001:
                self.actionmssg_dic.pop(guid)
                return
            if strType == 9002:
                self.actionpnts_dic.pop(guid)
                return
            if strType == 9003:
                self.actiontlprt_dic.pop(guid)
                return
            if strType == 9004:
                self.actionchngms_dic.pop(guid)
                return
            if strType == 9005:
                self.actionendscnr_dic.pop(guid)
                return
            if strType == 9006:
                self.actionlscrpt_dic.pop(guid)
                return
            if strType == 10001:
                self.all_guid_delete_info[guid] = {"strType": 10001, "side": self.mssnpatrol_dic[guid].m_Side}
                self.mssnpatrol_dic.pop(guid)
                return
            if strType == 10002:
                self.all_guid_delete_info[guid] = {"strType": 10002, "side": self.mssnstrike_dic[guid].m_Side}
                self.mssnstrike_dic.pop(guid)
                return
            if strType == 10003:
                self.all_guid_delete_info[guid] = {"strType": 10003, "side": self.mssnsupport_dic[guid].m_Side}
                self.mssnsupport_dic.pop(guid)
                return
            if strType == 10004:
                self.all_guid_delete_info[guid] = {"strType": 10004, "side": self.mssncargo_dic[guid].m_Side}
                self.mssncargo_dic.pop(guid)
                return
            if strType == 10005:
                self.all_guid_delete_info[guid] = {"strType": 10005, "side": self.mssnferry_dic[guid].m_Side}
                self.mssnferry_dic.pop(guid)
                return
            if strType == 10006:
                self.all_guid_delete_info[guid] = {"strType": 10006, "side": self.mssnmining_dic[guid].m_Side}
                self.mssnmining_dic.pop(guid)
                return
            if strType == 10007:
                self.all_guid_delete_info[guid] = {"strType": 10007, "side": self.mssnmnclrng_dic[guid].m_Side}
                self.mssnmnclrng_dic.pop(guid)
                return
            if strType == 11001:
                self.all_guid_delete_info[guid] = {"strType": 11001, "side": self.referencept_dic[guid].m_Side}
                self.referencept_dic.pop(guid)
                return
            if strType == 11002:
                self.all_guid_delete_info[guid] = {"strType": 11002, "side": self.zonenonav_dic[guid].m_Side}
                self.zonenonav_dic.pop(guid)
                return
            if strType == 11003:
                self.all_guid_delete_info[guid] = {"strType": 11003, "side": self.zonexclsn_dic[guid].m_Side}
                self.zonexclsn_dic.pop(guid)
                return
            if strType == 11004:
                self.response_dic.pop(guid)
                return

    def get_obj_by_guid(self, guid):
        """
        通过guid获取对象
        :param guid:实体的guid
        :return:
        """
        if guid in self.all_guid_info:
            guid_info = self.all_guid_info[guid]
            strType = guid_info["strType"]
            if strType == 1002:
                return self.doctrine_dic[guid]
            if strType == 1004:
                return self.side_dic[guid]
            if strType == 1005:
                return self.group_dic[guid]
            if strType == 2001:
                return self.submarine_dic[guid]
            if strType == 2002:
                return self.ship_dic[guid]
            if strType == 2003:
                return self.facility_dic[guid]
            if strType == 2004:
                return self.aircraft_dic[guid]
            if strType == 2005:
                return self.satellite_dic[guid]
            if strType == 3001:
                return self.sensor_dic[guid]
            if strType == 3002:
                return self.loadout_dic[guid]
            if strType == 3003:
                return self.mount_dic[guid]
            if strType == 3004:
                return self.magazine_dic.pop(guid)
            if strType == 3005:
                return self.weapon_dic[guid]
            if strType == 3006:
                return self.unguidedwpn_dic[guid]
            if strType == 3007:
                return self.wpnimpact_dic[guid]
            if strType == 3008:
                return self.sideway_dic[guid]
            if strType == 3009:
                return self.waypoint_dic[guid]
            if strType == 4001:
                return self.contact_dic[guid]
            if strType == 5001:
                return self.logged_messages[guid]
            if strType == 6001:
                return self.simevent_dic[guid]
            if strType == 7001:
                return self.trgunitdtcd_dic[guid]
            if strType == 7002:
                return self.trgunitdmgd_dic[guid]
            if strType == 7003:
                return self.trgunitdstrd_dic[guid]
            if strType == 7004:
                return self.trgpoints_dic[guid]
            if strType == 7005:
                return self.trgtime_dic[guid]
            if strType == 7006:
                return self.trgrglrtime_dic[guid]
            if strType == 7007:
                return self.trgrndmtime_dic[guid]
            if strType == 7008:
                return self.trgscenldd_dic[guid]
            if strType == 7009:
                return self.trgunitrmns_dic[guid]
            if strType == 8001:
                return self.cndscenhsstrtd_dic[guid]
            if strType == 8002:
                return self.cndsidepstr_dic[guid]
            if strType == 8003:
                return self.cndluascrpt_dic[guid]
            if strType == 9001:
                return self.actionmssg_dic[guid]
            if strType == 9002:
                return self.actionpnts_dic[guid]
            if strType == 9003:
                return self.actiontlprt_dic[guid]
            if strType == 9004:
                return self.actionchngms_dic[guid]
            if strType == 9005:
                return self.actionendscnr_dic[guid]
            if strType == 9006:
                return self.actionlscrpt_dic[guid]
            if strType == 10001:
                return self.mssnpatrol_dic[guid]
            if strType == 10002:
                return self.mssnstrike_dic[guid]
            if strType == 10003:
                return self.mssnsupport_dic[guid]
            if strType == 10004:
                return self.mssncargo_dic[guid]
            if strType == 10005:
                return self.mssnferry_dic[guid]
            if strType == 10006:
                return self.mssnmining_dic[guid]
            if strType == 10007:
                return self.mssnmnclrng_dic[guid]
            if strType == 11001:
                return self.referencept_dic[guid]
            if strType == 11002:
                return self.zonenonav_dic[guid]
            if strType == 11003:
                return self.zonexclsn_dic[guid]
            if strType == 11004:
                return self.response_dic[guid]

    def generate_guid(self):
        """
        功能：
        参数：
        返回：
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/24/20,4/25/20
        """
        hyphen_order = [9, 14, 19, 24]
        s = []
        continuing = True
        while continuing:
            for i in range(1, 37):
                if i in hyphen_order:
                    s.extend('-')
                else:
                    num = random.randint(0, 9)
                    letter = chr(random.randint(97, 102))  # 102-f (MoziServer), 122-z (wider)
                    s.extend(str(random.choice([num, letter])))
            if (s not in self.all_guid) and (s not in self.pseudo_situ_all_guid):
                continuing = False
        return ''.join(s)

    def throw_into_pseudo_situ_all_guid(self, guid):
        """
        功能：伪态势管理:all_guid
        参数：
        返回：
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/26/20
        """
        self.pseudo_situ_all_guid.append(guid)

    def throw_into_pseudo_situ_all_name(self, name):
        """
        功能：伪态势管理:all_guid
        参数：
        返回：
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/26/20
        """
        self.pseudo_situ_all_name.append(name)

    def is_name_existed(self, name):
        if name in self.pseudo_situ_all_name:
            raise Exception('存在相同名称，请重新命名。')
        else:
            self.throw_into_pseudo_situ_all_name(name)
