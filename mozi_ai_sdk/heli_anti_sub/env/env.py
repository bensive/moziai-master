#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import cos
from math import radians
from . import etc

from mozi_ai_sdk.base_env import BaseEnvironment as base_env
import numpy as np
from mozi_utils import pylog
from mozi_utils.geo import get_point_with_point_bearing_distance
from mozi_utils.geo import get_degree
from mozi_utils.geo import get_two_point_distance


def get_target_point():
    """
    获取目标点
    """
    lat2 = etc.task_end_point["latitude"]
    lon2 = etc.task_end_point["longitude"]
    return lat2, lon2


def get_target_distance(lat, lon):
    """
    获取目标距离
    """
    lat2, lon2 = get_target_point()
    distance = get_two_point_distance(lon, lat, lon2, lat2)
    return distance

def _get_reward_value(task_heading, current_heading, distance):
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

def get_distance_reward(lat, lon, last_heading, heading_change):
    """
    获取距离奖励值
    """
    lat2, lon2 = get_target_point()
    distance = get_two_point_distance(lon, lat, lon2, lat2)
    task_heading = get_degree(lat, lon, lat2, lon2)
    current_heading = last_heading + heading_change
    return _get_reward_value(task_heading, current_heading, distance)


class Env(base_env):
    """
    环境类
    """

    def __init__(self, IP, AIPort, agent_key_event_file, duration_interval, app_mode, synchronous=None,
                 simulate_compression=None, scenario_name=None, platform_mode=None, platform="windows"):
        super().__init__(IP, AIPort, platform, scenario_name, simulate_compression, duration_interval, synchronous,
                         app_mode, platform_mode)
        self.SERVER_PLAT = "windows"
        self.action_space = 2
        self.action_max = 1
        self.state_space = 3
        self.red_unit_list = None
        self.observation = None
        self.red_side_name = "美国海军"
        self.blue_side_name = "俄罗斯海军"
        self.agent_key_event_file = agent_key_event_file

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

        obs_lt = []
        for key in unit_list:
            aircraft_list_dic = self.redside.aircrafts
            unit = aircraft_list_dic.get(key)
            if unit:
                obs_lt.append(unit.dLongitude)
                obs_lt.append(unit.dLatitude)
                obs_lt.append(unit.fCurrentHeading)
            else:
                #pylog.info("unit do not exist")
                obs_lt.append(0.0)
                obs_lt.append(0.0)
                obs_lt.append(0.0)
        return obs_lt

    def _get_red_observation(self):
        """
        获取红方的观察
        """
        unit_list = self.red_unit_list
        obs_lt = self._get_a_side_observation(unit_list)
        return obs_lt

    def _get_waypoint_heading(self, last_heading, action_value):
        """
        获取航路点朝向
        """

        current_heading = last_heading + action_value
        if current_heading < 0:
            current_heading += 360
        if current_heading > 360:
            current_heading -= 360
        return current_heading

    def _get_new_waypoint(self, heading, lat, lon, distance=20.0):
        """
        获取新的航路点
        """
        dic = get_point_with_point_bearing_distance(lat, lon, heading, distance)
        return dic

    def _deal_point_data(self, waypoint):
        """
        处理航路点数据
        """
        lon = str(waypoint["longitude"])
        lat = str(waypoint["latitude"])
        return lon, lat

    def _get_aircraft_waypoint(self, action_value):
        """
        根据人工智能计算所得的动作值，计算飞机的目标航路点
        """
        obs = self.observation
        longitude = obs[0]
        latitude = obs[1]
        heading = obs[2]
        waypoint_heading = self._get_waypoint_heading(heading, action_value[0].item() * 90)
        waypoint = self._get_new_waypoint(waypoint_heading, latitude, longitude)
        distance = get_target_distance(latitude, longitude)
        return waypoint, distance

    def _check_done(self):
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
        检查飞机是否存在
        """
        obs = self.observation
        for i in range(len(obs)):
            if obs[i] != 0.0:
                return True
        return False

    def _check_target_exist(self):
        """
        检查目标是否存在
        """
        ret = self.scenario.get_units_by_name(etc.target_name)
        for key in ret:
            ret = self.scenario.unit_is_alive(key)
            if not ret:
                #pylog.info("target is not exist")
                pass
            return ret
        return False

    def _get_target_guid(self):
        """
        获取目标guid
        """
        target_name = etc.target_name
        for key in self.blueside.submarines:
            if etc.target_name == self.blueside.submarines[key].strName:
                target_guid = key
                return target_guid
        return None

    def _get_contact_target_guid(self):
        target_name = etc.target_name
        if self.redside.contacts:
            for key in self.redside.contacts:
                dic = self.redside.contacts[key].__dict__
                actual_guid = self.redside.contacts[key].m_ActualUnit
                for k in self.blueside.submarines:
                    if etc.target_name == self.blueside.submarines[k].strName:
                        return key

    def _check_is_contact_target(self):
        target_name = etc.target_name
        if self.redside.contacts:
            for key in self.redside.contacts:
                dic = self.redside.contacts[key].__dict__
                actual_guid = self.redside.contacts[key].m_ActualUnit
                for k in self.blueside.submarines:
                    if etc.target_name == self.blueside.submarines[k].strName:
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
            #pylog.info("find target and the guid is:%s" % target_guid)
            return True

        return False

    def _get_distance_reward(self, action_value):
        """
        获取距离奖励
        """
        obs = self.observation
        longitude = obs[0]
        latitude = obs[1]
        heading = obs[2]
        distance = get_target_distance(latitude, longitude)
        action_change_heading = action_value[0].item() * 90
        reward = get_distance_reward(latitude, longitude, heading, action_change_heading)
        return reward, distance

    def _get_reward(self, action_value):
        """
        获取奖励
        """
        reward = 0.0
        if action_value == []:
            return 0.0

        distance_reward, distance = self._get_distance_reward(action_value)
        reward += distance_reward

        if distance < etc.target_radius:
            if self._check_is_drop_sonobuoy(action_value):
                reward += 10.0
        else:
            if not self._check_aircraft_exist():
                reward += -100.0

        if self._check_is_find_target():
            reward += 10.0

        if not self._check_target_exist():
            #pylog.info("destroy target get 150.0 reward")
            reward += 150.0

        return reward

    def _check_is_drop_sonobuoy(self, action_value):
        if action_value[1].item() > 0:
            return True
        return False

    def _execute_action(self, action_value):
        """
        根据当前的动作值，执行动作
        """

        # 根据动作值计算飞机的下一路径点坐标，以及飞机到坦克的距离
        waypoint, distance = self._get_aircraft_waypoint(action_value)
        airs = self.redside.aircrafts
        for guid in airs:
            aircraft = airs[guid]
            print(aircraft.strName)

            if self._check_is_find_target():
                contact_target_guid = self._get_contact_target_guid()
                aircraft.auto_attack(contact_target_guid)
            else:
                if distance < etc.target_radius:
                    if self._check_is_drop_sonobuoy(action_value):
                        pylog.info("drop_sonobuoy")
                        aircraft.drop_sonobuoy("shallow", "active")

                lon, lat = self._deal_point_data(waypoint)
                aircraft.set_waypoint(lon, lat)

    def _update(self):
        """
        更新
        """
        # self.mozi_server.update_situation(self.scenario)
        self.redside.static_update()
        self.blueside.static_update()

    def _get_observation(self):
        """
        获取观察
        """
        red_obs_lt = self._get_red_observation()
        self.observation = red_obs_lt

        if self._check_aircraft_exist():
            if etc.TRANS_DATA:
                lt = []
                lt.append(red_obs_lt[0] - etc.task_end_point["longitude"])
                lt.append(red_obs_lt[1] - etc.task_end_point["latitude"])
                lt.append(red_obs_lt[2] / 360)
                return lt

        return  red_obs_lt

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
        obs = self._get_observation()
        reward = self._get_reward(action)
        done = self._check_done()
        info = ""
        return np.array(obs), reward, done, info

    def step(self, action):
        """
        输入动作
        执行动作
        更新态势
        获取观察
        获取reward
        检查是否结束
        """
        super(Env, self).step()
        self._execute_action(action)
        self._update()
        # self.mozi_server.run_grpc_simulate()
        return self._get_timesteps(action)

    def reset(self):
        """
        重置
        """
        super(Env, self).reset()
        self.scenario.set_cur_side_and_dir_view("美国海军", "false")    # 设置当前推演方及是否显示导演视图
        self._construct_side_entity()
        self._init_unit_list()
        return self._get_timesteps([])
