#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mozi_simu_sdk.mozi_server import MoziServer
import time
from mozi_ai_sdk.dppo.utils.utils import *
from mozi_ai_sdk.dppo.envs import etc
from mozi_ai_sdk.base_env import BaseEnvironment

def override(cls):
    """Annotation for documenting method overrides.

    Arguments:
        cls (type): The superclass that provides the overriden method. If this
            cls does not actually have the method, an error is raised.
    """

    def check_override(method):
        if method.__name__ not in dir(cls):
            raise NameError("{} does not override any method of {}".format(
                method, cls))
        return method

    return check_override


class Environment(BaseEnvironment):
    """
    环境
    """

    # def __init__(self, IP, AIPort, platform, scenario_name, simulate_compression, duration_interval, synchronous):
    #     self.server_ip = IP
    #     self.aiPort = AIPort
    #     self.platform = platform
    #     self.scenario_name = scenario_name
    #     self.websocker_conn = None
    #     self.mozi_server = None
    #     self.scenario = None
    #     self.connect_mode = 1
    #     self.num = 1
    #     self.simulate_compression = simulate_compression
    #     self.duration_interval = duration_interval
    #     self.synchronous = synchronous
    @override(BaseEnvironment)
    def step(self):
        """
        步长
        主要用途：单步决策的方法,根据环境态势数据改变战场环境
        """
        self.situation = self.mozi_server.update_situation(self.scenario, self.app_mode)
        self.redside.static_update()
        self.blueside.static_update()
        self.mozi_server.run_grpc_simulate()
        return self.scenario

    @override(BaseEnvironment)
    def reset(self, side_name):
        """
        重置函数
        主要用途：加载想定，
        """
        self.mozi_server.send_and_recv("IsMasterControl")
        self.create_scenario()
        # self.scenario = self.mozi_server.load_scenario()
        self.mozi_server.set_simulate_compression(self.simulate_compression)
        self.mozi_server.init_situation(self.scenario, etc.app_mode)
        self.redside = self.scenario.get_side_by_name('红方')
        self.redside.static_construct()
        self.blueside = self.scenario.get_side_by_name('蓝方')
        self.blueside.static_construct()
        self.mozi_server.run_simulate()

        side = self.scenario.get_side_by_name(side_name)
        self.create_battle_zone(side, side_name)
        self.scenario = self.step()
        side = self.scenario.get_side_by_name(side_name)
        self.create_offensive_patrol_zone(side, side_name)
        self.create_defensive_patrol_zone(side, side_name)
        self.scenario = self.step()

        return self.scenario

    # def create_scenario(self):
    #     """
    #     建立一个想定对象
    #     """
    #     self.scenario = self.mozi_server.load_scenario()
    #
    # def connect_mozi_server(self, ip=None, port=None):
    #     """
    #     功能：连接墨子服务器
    #     参数：
    #     返回：
    #     作者：aie
    #     单位：北京华戍防务技术有限公司
    #     时间：4/28/20
    #     """
    #     if ip is None and port is None:
    #         self.mozi_server = MoziServer(etc.SERVER_IP, etc.SERVER_PORT, self.platform, self.scenario_name,
    #                                       self.simulate_compression, self.synchronous)
    #     elif ip is not None and port is not None:
    #         self.mozi_server = MoziServer(ip, str(port), self.platform, self.scenario_name,
    #                                       self.simulate_compression, self.synchronous)
    #     time.sleep(4.0)
    #
    # def start(self, ip=None, port=None):
    #     """
    #     开始函数
    #     主要用途：
    #         1.连接服务器端
    #         2.设置运行模式
    #         3.设置步长参数
    #     """
    #     if ip is None and port is None:
    #         self.connect_mozi_server()
    #     elif ip is not None and port is not None:
    #         self.connect_mozi_server(ip, port)
    #     else:
    #         raise ValueError('请正确配置墨子IP与端口！！！')
    #
    #     self.mozi_server.set_run_mode(self.synchronous)
    #     self.mozi_server.set_decision_step_length(self.duration_interval)

    @staticmethod
    def create_battle_zone(side, side_name):
        zone = ['AI-AO-1', 'AI-AO-2', 'AI-AO-3', 'AI-AO-4']
        hostileContacts = side.contacts
        # inventory = {**side.aircrafts, **side.ships}
        inventory = side.ships
        #  Loop and Get Coordinates
        coordinates = []
        for k, v in hostileContacts.items():
            coordinates.append(MakeLatLong(v.dLatitude, v.dLongitude))
        for k, v in inventory.items():
            coordinates.append(MakeLatLong(v.dLatitude, v.dLongitude))
        # Create Defense Bounding Box
        patrolBoundingBox = FindBoundingBoxForGivenLocations(coordinates, 1.2)  # 2
        # patrolBoundingBox = FindBoundingBoxForGivenLocations(coordinates, 3.0)
        side.add_reference_point(zone[0], patrolBoundingBox[0]['latitude'], patrolBoundingBox[0]['longitude'])
        side.add_reference_point(zone[1], patrolBoundingBox[1]['latitude'], patrolBoundingBox[1]['longitude'])
        side.add_reference_point(zone[2], patrolBoundingBox[2]['latitude'], patrolBoundingBox[2]['longitude'])
        side.add_reference_point(zone[3], patrolBoundingBox[3]['latitude'], patrolBoundingBox[3]['longitude'])

    # 生成或更新攻击性巡逻任务的巡逻区域
    @staticmethod
    def create_offensive_patrol_zone(side, side_name):
        defaultRef = ['AI-AO-1', 'AI-AO-2', 'AI-AO-3', 'AI-AO-4']
        zone = ['Offensive_rp_1', 'Offensive_rp_2', 'Offensive_rp_3', 'Offensive_rp_4']
        defaults = {v.strName: {'latitude': v.dLatitude, 'longitude': v.dLongitude} for k, v in side.referencepnts.items()
                    if v.strName in defaultRef}
        airContacts_dic = {k: v for k, v in side.contacts.items() if v.m_ContactType == 0}      # 探测到的敌方飞机
        if len(defaults) != 4:
            return

        hostileContactBoundingBox = FindBoundingBoxForGivenContacts(airContacts_dic, defaults, 1)   # 2
        side.add_reference_point(zone[0], hostileContactBoundingBox[0]['latitude'], hostileContactBoundingBox[0]['longitude'])
        side.add_reference_point(zone[1], hostileContactBoundingBox[1]['latitude'], hostileContactBoundingBox[1]['longitude'])
        side.add_reference_point(zone[2], hostileContactBoundingBox[2]['latitude'], hostileContactBoundingBox[2]['longitude'])
        side.add_reference_point(zone[3], hostileContactBoundingBox[3]['latitude'], hostileContactBoundingBox[3]['longitude'])

    @staticmethod
    def create_defensive_patrol_zone(side, side_name):
        zone = ['AI-AO-1', 'AI-AO-2', 'AI-AO-3', 'AI-AO-4']
        defaults = {v.strName: {'latitude': v.dLatitude, 'longitude': v.dLongitude} for k, v in
                    side.referencepnts.items() if v.strName in zone}

        if len(defaults) != 4:
            return
        key_order = sorted(defaults.keys())
        aoPoints = [defaults[key] for key in key_order]
        # 生成大四边形的四个中点
        rp12mid = MidPointCoordinate(aoPoints[0]['latitude'], aoPoints[0]['longitude'], aoPoints[1]['latitude'],
                                     aoPoints[1]['longitude'])
        rp13mid = MidPointCoordinate(aoPoints[0]['latitude'], aoPoints[0]['longitude'], aoPoints[2]['latitude'],
                                     aoPoints[2]['longitude'])
        rp14mid = MidPointCoordinate(aoPoints[0]['latitude'], aoPoints[0]['longitude'], aoPoints[3]['latitude'],
                                     aoPoints[3]['longitude'])
        rp23mid = MidPointCoordinate(aoPoints[1]['latitude'], aoPoints[1]['longitude'], aoPoints[2]['latitude'],
                                     aoPoints[2]['longitude'])
        rp34mid = MidPointCoordinate(aoPoints[2]['latitude'], aoPoints[2]['longitude'], aoPoints[3]['latitude'],
                                     aoPoints[3]['longitude'])

        zones = ['rp2', 'rp3', 'rp4', 'rp5', 'rp6']

        side.add_reference_point('rp2', rp12mid['latitude'], rp12mid['longitude'])
        side.add_reference_point('rp3', rp13mid['latitude'], rp13mid['longitude'])
        side.add_reference_point('rp4', rp14mid['latitude'], rp14mid['longitude'])
        side.add_reference_point('rp5', rp23mid['latitude'], rp23mid['longitude'])
        side.add_reference_point('rp6', rp34mid['latitude'], rp34mid['longitude'])

