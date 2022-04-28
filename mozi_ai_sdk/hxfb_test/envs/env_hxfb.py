#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 10:33:22 2020

@author: dixit
"""

import random
import itertools
import uuid
from collections import namedtuple
from itertools import chain
from mozi_simu_sdk.mssnpatrol import CPatrolMission
from mozi_simu_sdk.mssnstrike import CStrikeMission
# from mozi_ai_sdk.test.dppo.envs.common.utils import *
from mozi_ai_sdk.hxfb_test.envs.common.utils import *
from mozi_ai_sdk.hxfb_test.envs.env import Environment
from mozi_ai_sdk.hxfb_test.envs import etc

from ray.rllib.env.multi_agent_env import MultiAgentEnv
from gym.spaces import Discrete, Box, Dict
from ray.remote_handle_docker import restart_mozi_container

import sys
import re
import zmq
import time

# zmq init
zmq_context = zmq.Context()
# ray request port
restart_requestor = zmq_context.socket(zmq.REQ)
Function = namedtuple('Function', ['type', 'function'])
FEATS_MAX_LEN = 350
MAX_DOCKER_RETRIES = 3


def restart_container(schedule_addr, schedule_port, _training_id, docker_ip_port):
    # 训练5轮后，重启docker
    try:
        message = {}
        message['zmq_command'] = 'restart_training_container'
        message['docker_ip_port'] = docker_ip_port
        message['training_id'] = _training_id
        restart_requestor.connect("tcp://%s:%s" % (str(schedule_addr), str(schedule_port)))
        restart_requestor.send_pyobj(message)
        recv_msg = restart_requestor.recv_pyobj()
        assert type(recv_msg) == str
        if 'OK' in recv_msg:
            pass
        else:
            sys.exit(1)
        return docker_ip_port
    except Exception:
        print('fail restart mozi docker!')
        sys.exit(1)


class HXFBEnv(MultiAgentEnv):
    def __init__(self, env_config):
        self.steps = None
        self.reward_accum = None
        self.env_config = env_config
        self.reset_nums = 0
        self._get_env()
        self.side_name = env_config['side_name']
        print('开始mozi reset!!!')
        self.scenario = self.env.reset(self.side_name)
        print('结束mozi reset!!!')

        self.time = self.scenario.m_Duration.split('@')  # 想定总持续时间
        self.m_StartTime = self.scenario.m_StartTime  # 想定开始时间
        self.m_Time = self.scenario.m_Time  # 想定当前时间

        self.side = self.scenario.get_side_by_name(self.side_name)
        self.enemy_side = self.scenario.get_side_by_name(env_config['enemy_side_name'])
        self.reward = float(self.side.iTotalScore) / 4067
        self.temp_reward = 0

        # self.defend_zones = [['AI-AO-1', 'rp2', 'rp3', 'rp4'],
        #                      ['rp2', 'AI-AO-2', 'rp5', 'rp3'],
        #                      ['rp3', 'rp5', 'AI-AO-3', 'rp6'],
        #                      ['rp4', 'rp3', 'rp6', 'AI-AO-4']]
        self.defend_zones = [['AI-AO-1', 'rp2', 'rp3', 'rp4'],
                             ['rp4', 'rp3', 'rp6', 'AI-AO-4']]
        # self.offend_zone = ['Offensive_rp_1', 'Offensive_rp_2', 'Offensive_rp_3', 'Offensive_rp_4']

        self.asuw = {k: v for k, v in self.side.aircrafts.items()
                     if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 3004
                     and (len(v.m_MultipleMissionGUIDs) == 0)}  # 可用反舰空战飞机
        self.s_asuw = dict(sorted(self.asuw.items(), key=lambda value: value[1].dLongitude))
        self.asup = {k: v for k, v in self.side.aircrafts.items()
                     if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 19361
                     and (len(v.m_MultipleMissionGUIDs) == 0)}  # 可用空战飞机
        self.target = {k: v for k, v in self.side.contacts.items() if v.m_ContactType == 2 and 'DDG' in v.strName}
        self.s_asup = dict(sorted(self.asup.items(), key=lambda value: value[1].dLongitude))

        self.action_atom_list = list(chain.from_iterable([
            [0 for _ in range(24)],
            list(itertools.product([x for x in self.s_asup.keys()], [y for y in self.defend_zones])),
            self.s_asuw.keys(),
        ]))
        self._action_func_list = list(
            chain.from_iterable([self._action('do-nothing', self._action_do_nothing),
                                 self._action('defensive', self._defensive_air_mission_action),
                                 # self._action('offensive', self._offensive_air_mission_action),
                                 self._action('attack', self._attack_anti_surface_ship_mission_action)]))
        self.action_space = Discrete(len(self._action_func_list))

        self.observation_space = Dict({
            "obs": Box(float("-inf"), float("inf"), shape=(23,)),
            # "action_mask": Box(0, 1, shape=(self.action_size,)),
        })

    def _get_win_score(self):
        if self.steps % 10 == 0:
            print(f'redside total score is {self.side.iTotalScore}')
        return float(self.side.iTotalScore) / 4067

    def _update(self, scenario):
        self.side = scenario.get_side_by_name(self.side_name)
        self.reward = self._get_win_score() - self.reward_accum + self.temp_reward
        self.reward_accum = self._get_win_score() + self.temp_reward
        self.temp_reward = 0
        self.m_Time = self.scenario.m_Time  # 想定当前时间
        self.asuw = {k: v for k, v in self.side.aircrafts.items()
                     if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 3004}  # 可用反舰空战飞机
        self.asup = {k: v for k, v in self.side.aircrafts.items()
                     if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 19361}  # 可用空战飞机
        self.target = {k: v for k, v in self.side.contacts.items() if v.m_ContactType == 2 and 'DDG' in v.strName}

        # 更新巡逻区域
        self._create_or_update_battle_zone()
        self._create_or_update_offensive_patrol_zone()
        self._create_or_update_defensive_patrol_zone()

    def step(self, action):
        done = False
        mission_unit = self._assign_available_unit(action['agent_0'])
        if self.env_config['mode'] in ['train', 'development']: 
            force_done = self.safe_step(action, mission_unit)
            if force_done:
                done = force_done
                self.reset_nums = 4  # 下一局会重启墨子docker(每5局重启一次docker)
                print(f"{time.strftime('%H:%M:%S')} 在第{self.steps}步，强制重启墨子！！！")
            else:
                self._update(self.scenario)
                done = self._is_done()
        elif self.env_config['mode'] in ['versus', 'eval']:
            if mission_unit:
                self._action_func_list[action['agent_0']].function(self.side, mission_unit)
            self.scenario = self.env.step()  # 墨子环境step
            self._update(self.scenario)
            done = self._is_done()
        reward = {'agent_0': self.reward}
        obs = {'agent_0': {"obs": self._generate_features()}}
        self.steps += 1
        if self.steps % 10 == 0:
            print(self.ip_port + '-' + f'reward is {self.reward}' + '-' + f'action is {action}')
        if done:
            print('++++Score:', self.reward_accum, 'step:', self.steps)
        return obs, reward, {'__all__': done, 'agent_0': done}, {'agent_0': {'score': self.side.iTotalScore}}

    def safe_step(self, action, mission_unit):
        force_done = False
        # noinspection PyBroadException
        try:
            if mission_unit:
                self._action_func_list[action['agent_0']].function(self.side, mission_unit)
        except Exception:
            print(f"{time.strftime('%H:%M:%S')} 在第{self.steps}步，执行lua超时！！！")
            force_done = True
            return force_done
        # noinspection PyBroadException
        try:
            self.scenario = self.env.step()  # 墨子环境step
        except Exception:
            print(f"{time.strftime('%H:%M:%S')} 在第{self.steps}步，更新态势超时！！！")
            force_done = True
            return force_done
        if self.scenario and self.scenario.get_side_by_name(self.side_name):
            return force_done
        else:
            # 态势更新失败会抛出异常
            print(f"{time.strftime('%H:%M:%S')} 在第{self.steps}步，更新态势失败！！！")
            force_done = True
            return force_done                       

    def reset(self):
        self._get_initial_state()
        self.steps = 0
        self.reward_accum = self._get_win_score()
        self._update(self.scenario)
        obs = {'agent_0': {
            "obs": self._generate_features()
        }}
        print('env_reset finished!!!')
        return obs

    def _generate_features(self):
        feats = []

        contacts = {k: v for k, v in self.side.contacts.items() if v.m_ContactType != 1}
        # s_contacts = sorted(contacts.items(), key=lambda value: value[1].dLongitude)
        h_feats = [0.0 for _ in range(6)]
        div = 0.0
        for k, v in contacts.items():
            div += 1.0
            temp_feats = [0.0 for _ in range(6)]
            if v.m_ContactType:
                temp_feats[0] = v.m_ContactType/22.0
            if v.m_IdentificationStatus:
                temp_feats[1] = v.m_IdentificationStatus/4.0
            if v.fCurrentHeading:
                temp_feats[2] = v.fCurrentHeading/180.0
            if v.fCurrentSpeed:
                temp_feats[3] = v.fCurrentSpeed/1000.0
            if v.dLongitude and v.dLatitude:
                temp_feats[4] = v.dLongitude/180.0
                temp_feats[5] = v.dLatitude/180.0
            h_feats = map(lambda x, y: x + y, h_feats, temp_feats)
        if div == 0.0:
            feats.extend(h_feats)
        else:
            h_feats = [i/div for i in h_feats]
            feats.extend(h_feats)

        # aircraft = sorted(self.side.aircrafts.items(), key=lambda value: value[1].dLongitude)
        red_air_feats = [0.0 for _ in range(9)]
        div = 0.0
        for k, v in self.side.aircrafts.items():
            div += 1.0
            temp_red_air_feats = [0.0 for _ in range(9)]
            if v.iFireIntensityLevel:
                temp_red_air_feats[0] = v.iFireIntensityLevel/4.0
            if v.iFloodingIntensityLevel:
                temp_red_air_feats[1] = v.iFloodingIntensityLevel/4.0
            if v.strAirOpsConditionString:
                temp_red_air_feats[2] = v.strAirOpsConditionString/26.0
            if v.dLongitude and v.dLatitude:
                temp_red_air_feats[3] = v.dLongitude/180.0
                temp_red_air_feats[4] = v.dLatitude/180.0

            weapon_list = self._get_unit_weapon(v)
            # 诱饵弹 2051-通用红外干扰弹；564-通用箔条；3386-AN/ALE70
            temp_red_air_feats[5] = self._get_weapon_num(weapon_list, [564, 2051, 3386])/10.0
            # 空空导弹  51-AIM120D;945-AIM9X
            temp_red_air_feats[6] = self._get_weapon_num(weapon_list, [51, 945])/10.0
            # 反舰导弹  826-AGM154C
            temp_red_air_feats[7] = self._get_weapon_num(weapon_list, [826, ])/10.0
            # 防空导弹 15-RIM162A
            temp_red_air_feats[8] = self._get_weapon_num(weapon_list, [15, ])/10.0

            red_air_feats = map(lambda x, y: x + y, red_air_feats, temp_red_air_feats)

        if div == 0.0:
            feats.extend(red_air_feats)
        else:
            red_air_feats = [i/div for i in red_air_feats]
            feats.extend(red_air_feats)

        # ships = sorted(self.side.ships.items(), key=lambda value: value[1].dLongitude)
        red_ship_feats = [0.0 for _ in range(3)]
        div = 0.0
        for k, v in self.side.ships.items():
            div += 1.0
            temp_red_ship_feats = [0.0 for _ in range(3)]
            if v.dFuelPercentage:
                temp_red_ship_feats[0] = v.dFuelPercentage/100.0
            if v.dLongitude and v.dLatitude:
                temp_red_ship_feats[1] = v.dLatitude/180.0
                temp_red_ship_feats[2] = v.dLongitude/180.0

            red_ship_feats = map(lambda x, y: x + y, red_ship_feats, temp_red_ship_feats)

        if div == 0.0:
            feats.extend(red_ship_feats)
        else:
            red_ship_feats = [i/div for i in red_ship_feats]
            feats.extend(red_ship_feats)

        red_patrol_mission_feats = [self.side.patrolmssns.__len__()/10.0, ]
        feats.extend(red_patrol_mission_feats)
        red_strike_mission_feats = [self.side.strikemssns.__len__()/10.0, ]
        feats.extend(red_strike_mission_feats)

        time_delta = self.m_Time - self.m_StartTime
        feats.append(time_delta / 3600.0)
        feats.append(time_delta / 7200.0)
        feats.append(time_delta / 14400.0)
        # print(f'+++feats:{feats}')
        # if feats.__len__() > FEATS_MAX_LEN:
        #     feats = feats[:FEATS_MAX_LEN]
        # else:
        #     feats.extend([0.0 for _ in range(FEATS_MAX_LEN - feats.__len__())])
        return feats

    @staticmethod
    def _get_unit_weapon(unit):
        """
        :param unit: aircraft, ship
        :return:
        """
        weapon = list(map(lambda x: x.split('$'), unit.m_UnitWeapons.split('@')))
        weapon_list = list(map(lambda x, y: x + [y[-1]], list(map(lambda x: x[0].split('x '), weapon)), weapon))
        return weapon_list

    @staticmethod
    def _get_weapon_num(weapon_list, weapon_type):
        num = 0
        for weapon in weapon_list:
            if weapon[0] != '' and weapon[-1] != '':
                if int(re.sub('\D', '', weapon[-1])) in weapon_type:
                    num += int(weapon[0])
        return num

    def _get_env(self):
        if self.env_config['mode'] == 'train':
            self.schedule_addr = self.env_config['schedule_addr']
            self.schedule_port = self.env_config['schedule_port']
            scenario_name = etc.SCENARIO_NAME
            platform = 'linux'
            self._create_env(platform, scenario_name=scenario_name)
        elif self.env_config['mode'] == 'development':
            scenario_name = etc.SCENARIO_NAME
            platform = 'linux'
            self._create_env(platform, scenario_name=scenario_name)
        elif self.env_config['mode'] == 'versus':
            scenario_name = etc.SCENARIO_NAME
            platform = 'linux'
            self._create_env(platform, scenario_name=scenario_name)
        elif self.env_config['mode'] == 'eval':
            scenario_name = etc.EVAL_SCENARIO_NAME
            platform = 'windows'
            self._create_env(platform, scenario_name=scenario_name)

            # platform = 'linux'
            # self._create_env(platform)
        else:
            raise NotImplementedError

    def _create_env(self, platform, scenario_name=None):
        for _ in range(MAX_DOCKER_RETRIES):
            # noinspection PyBroadException
            try:
                self.env = Environment(etc.SERVER_IP,
                                       etc.SERVER_PORT,
                                       platform,
                                       scenario_name,
                                       etc.SIMULATE_COMPRESSION,
                                       etc.DURATION_INTERVAL,
                                       etc.SYNCHRONOUS)
                # by dixit
                if self.env_config['avail_docker_ip_port']:
                    self.avail_ip_port_list = self.env_config['avail_docker_ip_port']
                else:
                    raise Exception('no avail port!')
                # self.self.reset_nums = 0
                self.ip_port = self.avail_ip_port_list[0]
                print(self.ip_port)
                self.ip = self.avail_ip_port_list[0].split(":")[0]
                self.port = self.avail_ip_port_list[0].split(":")[1]
                self.ip_port = f'{self.ip}:{self.port}'
                self.env.start(self.ip, self.port)
                break
            except Exception:
                continue

    def _get_initial_state(self):
        """
        dixit 2021/3/22
        每5局重启墨子，获取初始态势
        """

        self.reset_nums += 1
        if self.env_config['mode'] in ['train', 'development']:
            if self.reset_nums % 5 == 0:
                docker_ip_port = self.avail_ip_port_list[0]
                for _ in range(MAX_DOCKER_RETRIES):
                    # noinspection PyBroadException
                    try:
                        if self.env_config['mode'] == 'train':
                            restart_container(self.schedule_addr,
                                              self.schedule_port,
                                              self.env_config['training_id'],
                                              docker_ip_port)
                        else:
                            restart_mozi_container(docker_ip_port)
                        self.env = Environment(etc.SERVER_IP,
                                               etc.SERVER_PORT,
                                               'linux',
                                               etc.SCENARIO_NAME,
                                               etc.SIMULATE_COMPRESSION,
                                               etc.DURATION_INTERVAL,
                                               etc.SYNCHRONOUS)
                        self.env.start(self.ip, self.port)
                        break
                    except Exception:
                        print(f"{time.strftime('%H:%M:%S')} 在第{self.steps}步，第{_}次重启docker失败！！！")
                        continue
                print('开始mozi reset!!!')
                self.scenario = self.env.reset(self.side_name)
                print('结束mozi reset!!!')
            else:
                print('开始mozi reset!!!')
                self.scenario = self.env.reset(self.side_name)
                print('结束mozi reset!!!')
        else:
            self.scenario = self.env.reset(self.side_name)

    def _is_done(self):
        # 对战平台
        response_dic = self.scenario.get_responses()
        for _, v in response_dic.items():
            if v.Type == 'EndOfDeduction':
                print('打印出标记：EndOfDeduction')
                return True
        return False

    # 《《《《《《《《《《《《《 动作空间 》》》》》》》》》》》》》》

    def _action(self, action_type, function):
        if action_type == 'do-nothing':
            func_list = []
            for _ in range(24):
                func_list.append(Function(type=action_type, function=function()))
            return func_list
        elif action_type == 'defensive':
            func_list = []
            for atom in self.action_atom_list[24:-8]:
                # mission_name = 'defensive-' + str(uuid.uuid1())
                patrol_zone = atom[1]
                func_list.append(Function(type=action_type, function=function(patrol_zone)))
            return func_list
        elif action_type == 'attack':
            func_list = []
            for _ in self.action_atom_list[-8:]:
                # mission_name = 'attack-' + str(uuid.uuid1())
                func_list.append(
                    Function(type=action_type, function=function(self.target)))
            return func_list
        else:
            raise NotImplementedError

    def _assign_available_unit(self, action):
        if self._action_func_list[action].type == 'do-nothing':
            if (self.m_Time - self.m_StartTime) / 60.0 <= 10.0:
                self.temp_reward += 0.02  # 抑制agent频繁切换任务
            elif 10 < (self.m_Time - self.m_StartTime) / 60.0 <= 60.0:
                self.temp_reward += 0.01  # 抑制agent频繁切换任务
            else:
                self.temp_reward += 0.02  # 抑制agent频繁切换任务
            print(f'{self.steps}执行>>>>do-nothing!')
            return {}
        elif self._action_func_list[action].type == 'defensive':
            action_unit_key = self.action_atom_list[action][0]
            if action_unit_key in self.asup.keys():  # 当前任务的战机是否存活
                action_unit_class = self.asup[action_unit_key]
                if action_unit_class.m_AssignedMission == '':
                    self.temp_reward += 0.1
                    self.busy_asuw = {k: v for k, v in self.asuw.items()
                                      if (v.strAirOpsConditionString in [0, 11, 19, 20, 21]
                                          or v.m_AssignedMission != '')}
                    if self.busy_asuw.__len__() == 0:  # 在任务中的反舰飞机等于0架创建巡逻任务
                        self.temp_reward += 0.5
                    elif 0 < self.busy_asuw.__len__() <= 2:
                        self.temp_reward -= 0.2
                    elif 2 < self.busy_asuw.__len__() <= 4:
                        self.temp_reward -= 0.3
                    elif 4 < self.busy_asuw.__len__() <= 6:
                        self.temp_reward -= 0.4
                    else:
                        self.temp_reward -= 0.5

                    # if 0 <= (self.m_Time - self.m_StartTime)/60.0 <= 50.0:
                    #     self.temp_reward += 0.1
                    # elif 50 < (self.m_Time - self.m_StartTime)/60.0 <= 70.0:
                    #     self.temp_reward -= 0.1
                    # else:
                    #     self.temp_reward -= 0.5

                    if (self.m_Time - self.m_StartTime) / 60.0 <= 10.0:
                        self.temp_reward -= 0.1
                    elif 10 < (self.m_Time - self.m_StartTime) / 60.0 <= 40.0:
                        self.temp_reward += 0.2
                    elif 40 < (self.m_Time - self.m_StartTime) / 60.0 <= 60.0:
                        self.temp_reward -= 0.1
                    else:
                        self.temp_reward -= 0.2

                if action_unit_class.strAirOpsConditionString not in [11, 19, 20, 21]:  # 不为接站中的飞机切换任务
                    mission_unit = {action_unit_key: action_unit_class}
                else:
                    self.temp_reward -= 0.02
                    return {}
            else:
                self.temp_reward -= 0.02
                return {}
        elif self._action_func_list[action].type == 'attack':
            action_unit_key = self.action_atom_list[action]
            if action_unit_key in self.asuw.keys():  # 当前任务的战机是否存活
                action_unit_class = self.asuw[action_unit_key]
                if action_unit_class.m_AssignedMission == '':
                    self.temp_reward += 0.2
                    self.busy_asup = {k: v for k, v in self.asup.items()
                                      if (v.strAirOpsConditionString in [0, 11, 19, 20, 21])
                                      or v.m_AssignedMission != ''}
                    if self.busy_asup.__len__() == 0:  # 在任务中的巡逻飞机等于0架创建反舰任务
                        self.temp_reward -= 0.5
                    elif 0 < self.busy_asup.__len__() <= 2:
                        self.temp_reward -= 0.4
                    elif 2 < self.busy_asup.__len__() <= 4:
                        self.temp_reward -= 0.3
                    elif 4 < self.busy_asup.__len__() <= 6:
                        self.temp_reward -= 0.2
                    else:
                        self.temp_reward += 0.6

                    # if (self.m_Time - self.m_StartTime)/60.0 <= 25.0:
                    #     self.temp_reward -= 0.2
                    # elif 25 < (self.m_Time - self.m_StartTime)/60.0 <= 60.0:
                    #     self.temp_reward += 0.2
                    # elif 60 < (self.m_Time - self.m_StartTime)/60.0 <= 70.0:
                    #     self.temp_reward += 0.1
                    # else:
                    #     self.temp_reward -= 0.2

                    if (self.m_Time - self.m_StartTime) / 60.0 <= 30.0:
                        self.temp_reward -= 0.2
                    elif 30 < (self.m_Time - self.m_StartTime) / 60.0 <= 60.0:
                        self.temp_reward += 0.2
                    elif 60 < (self.m_Time - self.m_StartTime) / 60.0 <= 70.0:
                        self.temp_reward += 0.1
                    else:
                        self.temp_reward -= 0.2

                if action_unit_class.strAirOpsConditionString not in [11, 19, 20, 21]:  # 不为接站中的飞机切换任务
                    mission_unit = {action_unit_key: action_unit_class}
                else:
                    self.temp_reward -= 0.02
                    return {}
            else:
                self.temp_reward -= 0.02
                return {}
        else:
            raise NotImplementedError
        '''
        for k, v in mission_unit.items():
            print('k:', k, 'v:', v)
            # pdb.set_trace()
            print('action: ', action, 'unit_name: ', v.strName)
        '''
        return mission_unit

    def _action_do_nothing(self):
        def act(mission_unit):
            print(f'当前step：{self.steps}不执行任何动作！')
            pass

        return act

    # 防御性巡逻任务
    def _defensive_air_mission_action(self, zone):
        def act(side, mission_unit):
            mission_name = 'defensive-' + str(uuid.uuid1())
            
            for unit_key, unit_value in mission_unit.items():
                weapon_list = HXFBEnv._get_unit_weapon(unit_value)
                num = HXFBEnv._get_weapon_num(weapon_list, [51, 945])
                if num == 0:
                    print(f'单元{unit_value.strName}没有空战导弹，无法执行空战任务，应返航！')
                    return
                if unit_value.m_AssignedMission == '':
                    print(f'单元{unit_value.strName}执行防御性巡逻任务：{mission_name}')
                else:
                    for mission_key, mission_value in side.patrolmssns.items():
                        if mission_key == unit_value.m_AssignedMission:
                            mission_value.unassign_unit(unit_key)
                            print(f'取消单元{unit_value.strName}分配的任务！')
                            time.sleep(1)
                            # 删除旧任务
                            lua = 'ScenEdit_DeleteMission("%s", "%s")' % (self.side_name, mission_value.strName)
                            self.scenario.mozi_server.send_and_recv(lua)
                            time.sleep(1)
                            print(f'单元{unit_value.strName}执行防御性巡逻任务：{mission_name}')

            DefensiveAirMiss = side.add_mission_patrol(mission_name, 0, zone)  # 空战巡逻
            # DefensiveAirMiss = CPatrolMission('T+1_mode', self.scenario.mozi_server, self.scenario.situation)
            # DefensiveAirMiss.strName = mission_name
            taskParam = {'mission_name': mission_name,
                         'missionType': '空战巡逻',
                         'flightSize': 1,
                         'checkFlightSize': True,
                         'oneThirdRule': True,
                         'chechOpa': True,
                         'checkWwr': True,
                         'isActive': 'true',
                         'mission_unit': mission_unit}
            time.sleep(1)
            self._set_task_param(DefensiveAirMiss, taskParam)
            # print('mission_name ', mission_time, '***', len(mission_unit))

        return act

    # 攻击性巡逻任务
    def _offensive_air_mission_action(self, zone):
        def act(side, mission_unit):
            mission_name = 'offensive-' + str(uuid.uuid1())
                
            for unit_key, unit_value in mission_unit.items():
                weapon_list = HXFBEnv._get_unit_weapon(unit_value)
                num = HXFBEnv._get_weapon_num(weapon_list, [51, 945])
                if num == 0:
                    print(f'单元{unit_value.strName}没有空战导弹，无法执行空战任务，应返航！')
                    return

                if unit_value.m_AssignedMission == '':
                    print(f'单元{unit_value.strName}执行攻击性巡逻任务：{mission_name}')
                    
                else:
                    for mission_key, mission_value in side.patrolmssns.items():
                        if mission_key == unit_value.m_AssignedMission:
                            mission_value.unassign_unit(unit_key)
                            print(f'取消单元{unit_value.strName}分配的任务！')
                            time.sleep(1)
                            # 删除旧任务
                            lua = 'ScenEdit_DeleteMission("%s", "%s")' % (self.side_name, mission_value.strName)
                            self.scenario.mozi_server.send_and_recv(lua)
                            time.sleep(1)
                            print(f'单元{unit_value.strName}执行攻击性巡逻任务：{mission_name}')
                            self.temp_reward -= 0.005  # 抑制agent频繁切换任务
            OffensiveAirMiss = self.side.add_mission_patrol(mission_name, 0, zone)  # 空战巡逻
            # OffensiveAirMiss = CPatrolMission('T+1_mode', self.scenario.mozi_server, self.scenario.situation)
            # OffensiveAirMiss.strName = mission_name
            taskParam = {'mission_name': mission_name,
                         'missionType': '空战巡逻',
                         'flightSize': 1,
                         'checkFlightSize': True,
                         'oneThirdRule': True,
                         'chechOpa': True,
                         'checkWwr': True,
                         'isActive': 'true',
                         'mission_unit': mission_unit}
            time.sleep(1)
            self._set_task_param(OffensiveAirMiss, taskParam)
            # print('mission_name ', mission_time, '***', len(mission_unit))

        return act

    # 对海打击任务
    def _attack_anti_surface_ship_mission_action(self, target):
        def act(side, mission_unit):
            mission_name = 'attack-' + str(uuid.uuid1())
            
            for unit_key, unit_value in mission_unit.items():
                weapon_list = HXFBEnv._get_unit_weapon(unit_value)
                num = HXFBEnv._get_weapon_num(weapon_list, [826, ])
                if num == 0:
                    print(f'单元{unit_value.strName}没有反舰导弹，无法执行反舰任务，应返航！')
                    return
                if unit_value.m_AssignedMission == '':
                    print(f'单元{unit_value.strName}执行对海打击任务：{mission_name}')
                else:
                    for mission_key, mission_value in side.strikemssns.items():
                        if mission_key == unit_value.m_AssignedMission:
                            mission_value.unassign_unit(unit_key)
                            print(f'取消单元{unit_value.strName}分配的任务！')
                            time.sleep(1)
                            # 删除旧任务
                            lua = 'ScenEdit_DeleteMission("%s", "%s")' % (self.side_name, mission_value.strName)
                            self.scenario.mozi_server.send_and_recv(lua)
                            time.sleep(1)
                            print(f'单元{unit_value.strName}执行对海打击任务：{mission_name}')

            _target = target
            if len(_target) == 0:
                _target = {k: v for k, v in side.contacts.items()}
            AntiSurface = side.add_mission_strike(mission_name, 2)
            # AntiSurface = CStrikeMission('T+1_mode', self.scenario.mozi_server, self.scenario.situation)
            # AntiSurface.strName = mission_name
            taskParam = {'mission_name': mission_name,
                         'missionType': '对海打击',
                         'flightSize': 1,
                         'checkFlightSize': True,
                         'isActive': 'true',
                         'mission_unit': mission_unit,
                         'targets': _target}
            time.sleep(1)
            self._set_task_param(AntiSurface, taskParam)
            # print('mission_name ', mission_time, '***', len(mission_unit))

        return act

    def _set_task_param(self, mission, kwargs):
        kwargs_keys = kwargs.keys()
        # 设置编队规模
        if 'flightSize' in kwargs_keys:
            # mission.set_flight_size(self.side_name, kwargs['mission_name'], kwargs['flightSize'])
            mission.set_flight_size(kwargs['flightSize'])
        # 检查编队规模
        if 'checkFlightSize' in kwargs_keys:
            # mission.set_flight_size_check(self.side_name, kwargs['mission_name'], True)
            mission.set_flight_size_check(True)
        # 设置1/3规则
        if 'oneThirdRule' in kwargs_keys:
            # mission.set_one_third_rule(self.side_name, kwargs['mission_name'], kwargs['oneThirdRule'])
            mission.set_one_third_rule(kwargs['oneThirdRule'])
        # 是否对巡逻区外的探测目标进行分析
        if 'chechOpa' in kwargs_keys:
            # mission.set_opa_check(self.side_name, kwargs['mission_name'], kwargs['chechOpa'])
            mission.set_opa_check(str(kwargs['chechOpa']).lower())
        # 是否对武器射程内探测目标进行分析
        if 'checkWwr' in kwargs_keys:
            # mission.set_wwr_check(self.side_name, kwargs['mission_name'], kwargs['checkWwr'])
            mission.set_wwr_check(kwargs['checkWwr'])
        # 设置任务的开始和结束时间
        if 'startTime' in kwargs_keys:
            cmd_str = "ScenEdit_SetMission('" + self.side_name + "','" + kwargs['mission_name'] + "',{starttime='" + \
                      kwargs['startTime'] + "'})"
            self.scenario.mozi_server.send_and_recv(cmd_str)
        if 'endTime' in kwargs_keys:
            cmd_str = "ScenEdit_SetMission('" + self.side_name + "','" + kwargs['mission_name'] + "',{endtime='" + \
                      kwargs[
                          'endTime'] + "'})"
            self.scenario.mozi_server.send_and_recv(cmd_str)
        if 'mission_unit' in kwargs_keys:
            mission.assign_units(kwargs['mission_unit'])
        if 'targets' in kwargs_keys:
            mission.assign_unit_as_target(kwargs['targets'])

    def _create_or_update_battle_zone(self):
        side = self.side
        zone = ['AI-AO-1', 'AI-AO-2', 'AI-AO-3', 'AI-AO-4']
        defaults = {v.strName: {'latitude': v.dLatitude, 'longitude': v.dLongitude} for k, v in
                    side.referencepnts.items() if v.strName in zone}

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
        patrolBoundingBox = FindBoundingBoxForGivenLocations(coordinates, 1.2)
        if len(defaults) < 4:
            # patrolBoundingBox = FindBoundingBoxForGivenLocations(coordinates, 3.0)
            side.add_reference_point(zone[0], patrolBoundingBox[0]['latitude'],
                                     patrolBoundingBox[0]['longitude'])
            side.add_reference_point(zone[1], patrolBoundingBox[1]['latitude'],
                                     patrolBoundingBox[1]['longitude'])
            side.add_reference_point(zone[2], patrolBoundingBox[2]['latitude'],
                                     patrolBoundingBox[2]['longitude'])
            side.add_reference_point(zone[3], patrolBoundingBox[3]['latitude'],
                                     patrolBoundingBox[3]['longitude'])
        else:
            for i in range(len(patrolBoundingBox)):
                cmd = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                    self.side_name, 'AI-AO-' + str(i + 1), patrolBoundingBox[i]['latitude'],
                    patrolBoundingBox[i]['longitude'])
                self.scenario.mozi_server.send_and_recv(cmd)

    # 生成或更新攻击性巡逻任务的巡逻区域
    def _create_or_update_offensive_patrol_zone(self):
        side = self.side
        defaultRef = ['AI-AO-1', 'AI-AO-2', 'AI-AO-3', 'AI-AO-4']
        zone = ['Offensive_rp_1', 'Offensive_rp_2', 'Offensive_rp_3', 'Offensive_rp_4']
        defaults = {v.strName: {'latitude': v.dLatitude, 'longitude': v.dLongitude} for k, v in
                    side.referencepnts.items()
                    if v.strName in defaultRef}
        Offensive_rp = {v.strName: {'latitude': v.dLatitude, 'longitude': v.dLongitude} for k, v in
                        side.referencepnts.items()
                        if v.strName in zone}
        airContacts_dic = {k: v for k, v in side.contacts.items() if v.m_ContactType == 0}  # 探测到的敌方飞机
        if len(defaults) != 4:
            return

        hostileContactBoundingBox = FindBoundingBoxForGivenContacts(airContacts_dic, defaults, 1)

        if len(Offensive_rp) == 0:
            side.add_reference_point(zone[0], hostileContactBoundingBox[0]['latitude'],
                                     hostileContactBoundingBox[0]['longitude'])
            side.add_reference_point(zone[1], hostileContactBoundingBox[1]['latitude'],
                                     hostileContactBoundingBox[1]['longitude'])
            side.add_reference_point(zone[2], hostileContactBoundingBox[2]['latitude'],
                                     hostileContactBoundingBox[2]['longitude'])
            side.add_reference_point(zone[3], hostileContactBoundingBox[3]['latitude'],
                                     hostileContactBoundingBox[3]['longitude'])
        else:
            set_str_1 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.side_name, zone[0], hostileContactBoundingBox[0]['latitude'],
                hostileContactBoundingBox[0]['longitude'])
            self.scenario.mozi_server.send_and_recv(set_str_1)
            set_str_2 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.side_name, zone[1], hostileContactBoundingBox[1]['latitude'],
                hostileContactBoundingBox[1]['longitude'])
            self.scenario.mozi_server.send_and_recv(set_str_2)
            set_str_3 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.side_name, zone[2], hostileContactBoundingBox[2]['latitude'],
                hostileContactBoundingBox[2]['longitude'])
            self.scenario.mozi_server.send_and_recv(set_str_3)
            set_str_4 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.side_name, zone[3], hostileContactBoundingBox[3]['latitude'],
                hostileContactBoundingBox[3]['longitude'])
            self.scenario.mozi_server.send_and_recv(set_str_4)

    # 生成或更新防御性巡逻区域
    def _create_or_update_defensive_patrol_zone(self):
        side = self.side
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
        rps = [k for k, v in side.referencepnts.items() if v.strName in zones]

        if len(rps) != 5:
            # 巡逻任务1
            side.add_reference_point('rp2', rp12mid['latitude'], rp12mid['longitude'])
            side.add_reference_point('rp3', rp13mid['latitude'], rp13mid['longitude'])
            side.add_reference_point('rp4', rp14mid['latitude'], rp14mid['longitude'])
            side.add_reference_point('rp5', rp23mid['latitude'], rp23mid['longitude'])
            side.add_reference_point('rp6', rp34mid['latitude'], rp34mid['longitude'])
        elif len(rps) == 5:
            # 巡逻任务1
            cmd1 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.side_name, 'rp2', rp12mid['latitude'], rp12mid['longitude'])
            self.scenario.mozi_server.send_and_recv(cmd1)
            cmd2 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.side_name, 'rp3', rp13mid['latitude'], rp13mid['longitude'])
            self.scenario.mozi_server.send_and_recv(cmd2)
            cmd3 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.side_name, 'rp4', rp14mid['latitude'], rp14mid['longitude'])
            self.scenario.mozi_server.send_and_recv(cmd3)
            cmd5 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.side_name, 'rp5', rp23mid['latitude'], rp23mid['longitude'])
            self.scenario.mozi_server.send_and_recv(cmd5)
            cmd9 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.side_name, 'rp6', rp34mid['latitude'], rp34mid['longitude'])
            self.scenario.mozi_server.send_and_recv(cmd9)
