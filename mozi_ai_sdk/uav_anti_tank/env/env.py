#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import numpy as np
from math import cos
from math import radians

from mozi_utils import pylog
from mozi_utils.geo import get_point_with_point_bearing_distance
from mozi_utils.geo import get_degree
from mozi_utils.geo import get_two_point_distance

from mozi_ai_sdk.base_env import BaseEnvironment
from . import etc

'''
作者：刘占勇
日期：2020.05.04
功能：无人机反坦克想定环境类，UAT=UAV Anti Tank
'''


def _get_waypoint_heading(last_heading, action_value):
    """
    获取航路点朝向
    """

    current_heading = last_heading + action_value
    if current_heading < 0:
        current_heading += 360
    if current_heading > 360:
        current_heading -= 360
    return current_heading


class EnvUavAntiTank(BaseEnvironment):
    """
    作者：刘占勇
    日期：2020.05.04
    功能：构造函数
    参数：无
    返回：无
    """

    def __init__(self, IP, AIPort, agent_key_event_file, duration_interval, app_mode, synchronous=None,
                 simulate_compression=None, scenario_name=None, platform_mode=None, platform="windows"):
        super().__init__(IP, AIPort, platform, scenario_name, simulate_compression, duration_interval, synchronous,
                         app_mode, platform_mode)

        self.SERVER_PLAT = platform
        self.state_space_dim = 3  # 状态空间维度
        self.action_space_dim = 1
        self.action_max = 1

        self.state_space_dim = 3
        self.red_unit_list = None
        self.observation = None
        self.red_side_name = "红方"
        self.blue_side_name = "蓝方"
        self.agent_key_event_file = agent_key_event_file

    def reset(self, app_mode=None):
        """
        重置    Signature of method ‘ret()’ does not match signature of base method in class ‘base_env.reset()’
        返回：当前状体及回报值
        """
        # 调用父类的重置函数
        super(EnvUavAntiTank, self).reset()

        # 构建各方实体
        self._construct_side_entity()
        self._init_unit_list()

        state_now = self.get_observation()
        reward_now = self.get_reward(None)
        return state_now, reward_now

    '''
    作者：刘占勇
    日期：2020.05.04
    功能：环境的执行动作函数
    流程： 
        输入动作
        执行动作
        更新态势
        获取观察
        获取reward
        检查是否结束        
    参数：无
    返回： 1）state：状态；
           2）reward：回报值 
    '''

    def execute_action(self, action_value):
        super(EnvUavAntiTank, self).step()

        waypoint = self._get_aircraft_waypoint(action_value)  # 根据动作计算飞机的期望路径点

        longitude = self.observation[0]  # 当前的位置
        latitude = self.observation[1]
        distance = self.get_target_distance(latitude, longitude)

        airs = self.redside.aircrafts
        for guid in airs:
            aircraft = airs[guid]
            if distance < etc.target_radius:
                # 如果目标距离小于打击距离，且已发现目标，则自动攻击之
                if self._check_is_find_target():
                    target_guid = self._get_target_guid()
                    target_guid = self._get_contact_target_guid()
                    print("%s：自动攻击目标" % datetime.time())
                    aircraft.auto_attack(target_guid)
            else:
                # 如果目标距离大于打击距离，则继续机动
                lon, lat = self._deal_point_data(waypoint)
                # print("set waypoint:%s %s" % (lon, lat))
                aircraft.set_waypoint(lon, lat)

        # 动作下达了，该仿真程序运行，以便执行指令（），许怀阳 2020050716:58
        self.mozi_server.run_grpc_simulate()

        # 更新数据时，会被阻塞，实现与仿真的同步
        self._update()

        # # 动作执行完了，该继续仿真了
        # self.mozi_server.run_simulate()

        obs = self.get_observation()
        reward = self.get_reward(action_value)
        done = self.check_done()

        return np.array(obs), reward

    def get_reward(self, action_value):
        """
        获取奖励
        """
        reward = 0.0
        if action_value is not None:
            # 距离目标越近，奖励值越大
            distance_reward, distance = self._get_distance_reward(action_value)
            reward += distance_reward

            if distance < etc.target_radius:  # 如果进入了一个距离范围
                reward += 10.0
            else:
                if not self._check_aircraft_exist():  # 飞机被打死，则降低奖赏值
                    reward += -100.0
            if not self._check_target_exist():  # 目标被打死，则增加奖赏值
                reward += 150.0
        return reward

    def _get_distance_reward(self, action_value):
        """
        获取距离奖励
        """
        obs = self.observation
        longitude = obs[0]
        latitude = obs[1]
        heading = obs[2]
        distance = self.get_target_distance(latitude, longitude)
        action_change_heading = action_value[0].item() * 10  # 许怀阳 202005062308，由90改为20
        reward = self.get_distance_reward(latitude, longitude, heading, action_change_heading)
        return reward, distance

    def _init_red_unit_list(self):
        """
        初始化红方单元列表
        """
        ret_lt = []
        aircraft_list_dic = self.redside.aircrafts
        for key in aircraft_list_dic:
            ret_lt.append(key)
        return ret_lt

    def _get_a_side_observation(self, unit_list):
        """
        获取一方的观察
        """
        obs_lt = [0.0 for x in range(0, self.state_space_dim)]
        for key in unit_list:
            aircraft_list_dic = self.redside.aircrafts
            unit = aircraft_list_dic.get(key)
            if unit:
                obs_lt[0] = unit.dLongitude
                obs_lt[1] = unit.dLatitude
                obs_lt[2] = unit.fCurrentHeading
        return obs_lt

    def _get_red_observation(self):
        """
        获取红方的观察
        """
        unit_list = self.red_unit_list
        obs_lt = self._get_a_side_observation(unit_list)
        return obs_lt

    def _get_new_waypoint(self, heading, lat, lon, distance=20.0):
        """
        根據朝向，設置飛機的下一個路徑點
        """
        dic = get_point_with_point_bearing_distance(lat, lon, heading, distance)
        return dic

    def _deal_point_data(self, waypoint):
        """
        处理航路店数据
        """
        lon = str(waypoint["longitude"])
        lat = str(waypoint["latitude"])
        return lon, lat

    '''
    作者：刘占勇
    日期：2020.05.04
    功能：检查飞机是否存在，用于判断是否结束推演，如果飞机没有了，就不用再推演了
    参数：无
    返回：无
    '''

    def _get_aircraft_waypoint(self, action_value):
        """
        根据智能体的动作指令，获取飞机的期望的航路点
        """
        obs = self.observation
        longitude = obs[0]  # 当前的位置
        latitude = obs[1]
        heading = obs[2]  # 朝向
        waypoint_heading = _get_waypoint_heading(heading, action_value[0].item() * 10)  # 许怀阳 20200505 2306 由90改为20
        waypoint = self._get_new_waypoint(waypoint_heading, latitude, longitude)

        return waypoint

    def check_done(self):
        """
        检查是否可以结束
        """
        if not self._check_aircraft_exist():
            return True
        if not self._check_target_exist():
            return True
        return False

    def _check_aircraft_exist(self):
        """
        作者：刘占勇
        日期：2020.05.04
        功能：检查飞机是否存在，用于判断是否结束推演，如果飞机没有了，就不用再推演了
        """
        obs = self.observation
        for i in range(len(obs)):
            if obs[i] != 0.0:
                return True
        return False

    def _check_target_exist(self):
        """
        作者：刘占勇
        日期：2020.05.04
        功能：检查是否还有目标存在
        """
        ret = self.scenario.get_units_by_name(etc.target_name)
        for key in ret:
            ret = self.scenario.unit_is_alive(key)
            if not ret:
                # pylog.info("target is not exist")
                pass
            else:
                # pylog.info("target is exist")
                pass
            return ret
        return False

    def _get_target_guid(self):
        """
        获取目标guid
        """
        target_name = etc.target_name
        for key in self.blueside.facilities:
            pylog.info("%s" % self.blueside.facilities[key])
            if etc.target_name == self.blueside.facilities[key].strName:
                target_guid = key
                return target_guid
        return None

    def _get_contact_target_guid(self):
        target_name = etc.target_name
        if self.redside.contacts:
            for key in self.redside.contacts:
                pylog.info("contact guid:%s" % key)
                dic = self.redside.contacts[key].__dict__
                actual_guid = self.redside.contacts[key].m_ActualUnit
                if etc.target_name == self.blueside.facilities[actual_guid].strName:
                    return key

    def _check_is_contact_target(self):
        """
        作者：刘占勇
        日期：2020.05.04
        功能：检查是否还有目标存在
        """
        target_name = etc.target_name
        if self.redside.contacts:
            for key in self.redside.contacts:
                dic = self.redside.contacts[key].__dict__
                actual_guid = self.redside.contacts[key].m_ActualUnit
                for k in self.blueside.facilities:
                    if etc.target_name == self.blueside.facilities[k].strName:
                        target_guid = k
                        return target_guid
        return False

    def _check_is_find_target(self):
        """
        检查是否发现目标
        """
        target_name = etc.target_name
        target_guid = self._check_is_contact_target()
        if target_guid:
            pylog.info("find target and the guid is:%s" % target_guid)
            return True

        return False

    def _update(self):
        """
        更新
        """
        self.mozi_server.update_situation(self.scenario, self.app_mode)
        self.redside.static_update()
        self.blueside.static_update()

    def get_observation(self):
        """
        获取观察
        """
        red_obs_lt = self._get_red_observation()
        self.observation = red_obs_lt
        return red_obs_lt

    def _construct_side_entity(self):
        """
        构造各方实体
        """
        self.redside = self.scenario.get_side_by_name(self.red_side_name)
        self.redside.static_construct()
        self.blueside = self.scenario.get_side_by_name(self.blue_side_name)
        self.blueside.static_construct()

    def _init_unit_list(self):
        """
        初始化单元列表
        """
        self.red_unit_list = self._init_red_unit_list()

    def _get_timesteps(self, action):
        """
        获取单步数据
        """
        obs = self.get_observation()
        reward = self.get_reward(action)
        done = self.check_done()
        info = ""
        return np.array(obs), reward, done, info

    def get_target_point(self):
        """
        获取目标点
        """
        lat2 = etc.task_end_point["latitude"]
        lon2 = etc.task_end_point["longitude"]
        return lat2, lon2

    def get_target_distance(self, lat, lon):
        """
        获取目标距离
        """
        lat2, lon2 = self.get_target_point()
        distance = get_two_point_distance(lon, lat, lon2, lat2)
        return distance

    def get_reward_value(self, task_heading, current_heading, distance):
        """
        获取奖励值
        """
        angel = abs(task_heading - current_heading)
        cos_value = cos(radians(angel))
        if cos_value >= 0:
            reward = (10000 * cos(radians(angel))) / distance
            return reward
        else:
            neg_reward = (distance * cos(radians(angel))) / 10000
            return neg_reward

    def get_distance_reward(self, lat, lon, last_heading, heading_change):
        """
        获取距离奖励值
        """
        lat2, lon2 = self.get_target_point()
        distance = get_two_point_distance(lon, lat, lon2, lat2)
        task_heading = get_degree(lat, lon, lat2, lon2)
        current_heading = last_heading + heading_change
        return self.get_reward_value(task_heading, current_heading, distance)
