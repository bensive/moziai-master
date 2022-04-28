# 时间 ： 2020/8/31 21:10
# 作者 ： Dixit
# 文件 ： observations.py
# 项目 ： moziAIBT2
# 版权 ： 北京华戍防务技术有限公司

import numpy as np
import re
from gym import spaces
from functools import reduce
from mozi_ai_sdk.dppo.utils.utils import *

# 单元类型、数量、在区域内在空的数量、空闲的数量、被击落、击沉的数量
# 在空所有飞机的武器类型和数量、消耗所有武器类型与数量
# 当前推演进度
# 任务类型、任务数量
# 探测信息（飞机、驱逐舰、航母、武器挂架）


# class Features(gym.Wrapper):
class Features(object):
    def __init__(self, env, scenario, sideName):
        self.sideName = sideName
        self.side = scenario.get_side_by_name(self.sideName)
        self._env = env
        self.reward = float(self.side.iTotalScore) / 4067
        self.mozi_server = scenario.mozi_server
        self.ships = self.side.ships
        self.aircrafts = self.side.aircrafts
        self.contacts = self.side.contacts
        self.asuw = 8
        self.asup = 8
        self.destroyer = 1
        self.aircarrier = 1
        self.toll = 384
        self.air2air_missile = 112
        self.antiship_missile = 48
        self.airdefense_missile = 80
        self.zones = {'saw_zone': ['Offensive_rp_1', 'Offensive_rp_2', 'Offensive_rp_3', 'Offensive_rp_4'],
                      'zone_1': ['AI-AO-1', 'rp2', 'rp3', 'rp4'],
                      'zone_2': ['rp2', 'AI-AO-2', 'rp5', 'rp3'],
                      'zone_3': ['rp3', 'rp5', 'AI-AO-3', 'rp6'],
                      'zone_4': ['rp4', 'rp3', 'rp6', 'AI-AO-4']}
        self.combact_units_type = {'asuw': '0001', 'asup': '0010', 'destroyer': '0100', 'aircarrier': '1000'}
        self.weapons_type = {'toll': '0001', 'air2air_missile': '0010', 'antiship_missile': '0100', 'airdefense_missile': '1000'}
        self.contacts_type = {'missile': '001', 'aircraft': '010', 'ship': '100'}
        self.top_category = {'unit_type': '001', 'weapon_type': '010', 'contact_type': '100'}
        self.second_category = {'idle_unit_type': self.top_category['unit_type']+'001',
                                'loss_unit_type': self.top_category['unit_type']+'010',
                                'busy_unit_type': self.top_category['unit_type']+'100',
                                'consumed_weapon_type': self.top_category['weapon_type']+'01',
                                'surplus_weapon_type': self.top_category['weapon_type']+'10',
                                'hostile_in_zone_1': self.top_category['contact_type'] + '0001',
                                'hostile_in_zone_2': self.top_category['contact_type'] + '0010',
                                'hostile_in_zone_3': self.top_category['contact_type'] + '0100',
                                'hostile_in_zone_4': self.top_category['contact_type'] + '1000'}
        self.third_category = {'saw_zone': self.second_category['busy_unit_type']+'00001',
                               'zone_1': self.second_category['busy_unit_type']+'00010',
                               'zone_2': self.second_category['busy_unit_type']+'00100',
                               'zone_3': self.second_category['busy_unit_type']+'01000',
                               'zone_4': self.second_category['busy_unit_type']+'10000'}
        self.stat_type = {
            # 空闲的单元类型stat_self_idle_unit_type
            'self_idle_asuw': self.second_category['idle_unit_type']+self.combact_units_type['asuw'],
            'self_idle_asup': self.second_category['idle_unit_type']+self.combact_units_type['asup'],
            'self_idle_destroyer': self.second_category['idle_unit_type']+self.combact_units_type['destroyer'],
            'self_idle_aircarrier': self.second_category['idle_unit_type']+self.combact_units_type['aircarrier'],
            # 损失的单元类型stat_self_loss_unit_type
            'self_loss_asuw': self.second_category['loss_unit_type']+self.combact_units_type['asuw'],
            'self_loss_asup': self.second_category['loss_unit_type']+self.combact_units_type['asup'],
            'self_loss_destroyer': self.second_category['loss_unit_type']+self.combact_units_type['destroyer'],
            'self_loss_aircarrier': self.second_category['loss_unit_type']+self.combact_units_type['aircarrier'],
            # 任务中的单元类型stat_self_busy_unit_type
            'self_busy_asuw': self.second_category['busy_unit_type'] + self.combact_units_type['asuw'],
            'self_busy_asup': self.second_category['busy_unit_type'] + self.combact_units_type['asup'],
            'self_busy_destroyer': self.second_category['busy_unit_type'] + self.combact_units_type['destroyer'],
            'self_busy_aircarrier': self.second_category['busy_unit_type'] + self.combact_units_type['aircarrier'],
            # 在区域saw_zone中的单元类型stat_self_saw_zone_unit_type
            'self_saw_zone_asuw': self.third_category['saw_zone'] + self.combact_units_type['asuw'],
            'self_saw_zone_asup': self.third_category['saw_zone'] + self.combact_units_type['asup'],
            'self_saw_zone_destroyer': self.third_category['saw_zone'] + self.combact_units_type['destroyer'],
            'self_saw_zone_aircarrier': self.third_category['saw_zone'] + self.combact_units_type['aircarrier'],
            # 在区域zone_1中的单元类型stat_self_zone_1_unit_type
            'self_zone_1_asuw': self.third_category['zone_1'] + self.combact_units_type['asuw'],
            'self_zone_1_asup': self.third_category['zone_1'] + self.combact_units_type['asup'],
            'self_zone_1_destroyer': self.third_category['zone_1'] + self.combact_units_type['destroyer'],
            'self_zone_1_aircarrier': self.third_category['zone_1'] + self.combact_units_type['aircarrier'],
            # 在区域zone_2中的单元类型stat_self_zone_2_unit_type
            'self_zone_2_asuw': self.third_category['zone_2'] + self.combact_units_type['asuw'],
            'self_zone_2_asup': self.third_category['zone_2'] + self.combact_units_type['asup'],
            'self_zone_2_destroyer': self.third_category['zone_2'] + self.combact_units_type['destroyer'],
            'self_zone_2_aircarrier': self.third_category['zone_2'] + self.combact_units_type['aircarrier'],
            # 在区域zone_3中的单元类型stat_self_zone_3_unit_type
            'self_zone_3_asuw': self.third_category['zone_3'] + self.combact_units_type['asuw'],
            'self_zone_3_asup': self.third_category['zone_3'] + self.combact_units_type['asup'],
            'self_zone_3_destroyer': self.third_category['zone_3'] + self.combact_units_type['destroyer'],
            'self_zone_3_aircarrier': self.third_category['zone_3'] + self.combact_units_type['aircarrier'],
            # 在区域zone_4中的单元类型stat_self_zone_4_unit_type
            'self_zone_4_asuw': self.third_category['zone_4'] + self.combact_units_type['asuw'],
            'self_zone_4_asup': self.third_category['zone_4'] + self.combact_units_type['asup'],
            'self_zone_4_destroyer': self.third_category['zone_4'] + self.combact_units_type['destroyer'],
            'self_zone_4_aircarrier': self.third_category['zone_4'] + self.combact_units_type['aircarrier'],
            # 消耗的武器类型stat_self_consumed_weapon_type
            'self_consumed_toll': self.second_category['consumed_weapon_type'] + self.weapons_type['toll'],
            'self_consumed_air2airmissile': self.second_category['consumed_weapon_type'] + self.weapons_type['air2air_missile'],
            'self_consumed_antishipmissile': self.second_category['consumed_weapon_type'] + self.weapons_type['antiship_missile'],
            'self_consumed_airdefensemissile': self.second_category['consumed_weapon_type'] + self.weapons_type['airdefense_missile'],
            # 任务中所有单元剩余武器类型stat_self_surplus_weapon_type
            'self_surplus_toll': self.second_category['surplus_weapon_type'] + self.weapons_type['toll'],
            'self_surplus_air2airmissile': self.second_category['surplus_weapon_type'] + self.weapons_type['air2air_missile'],
            'self_surplus_antishipmissile': self.second_category['surplus_weapon_type'] + self.weapons_type['antiship_missile'],
            'self_surplus_airdefensemissile': self.second_category['surplus_weapon_type'] + self.weapons_type['airdefense_missile'],
            # 探测到的敌方单元类型stat_hostile_unit_type
            # 'hostile_unknown': self.top_category['contact_type']+self.contacts_type['unknown'],
            'hostile_missile': self.top_category['contact_type'] + self.contacts_type['missile'],
            'hostile_aircraft': self.top_category['contact_type'] + self.contacts_type['aircraft'],
            'hostile_ship': self.top_category['contact_type'] + self.contacts_type['ship'],
            # 在区域zone_1中的敌方单元类型stat_hostile_zone_1_unit_type
            # 'hostile_zone_1_unknown': self.second_category['hostile_in_zone_1']+self.contacts_type['unknown'],
            'hostile_zone_1_missile': self.second_category['hostile_in_zone_1'] + self.contacts_type['missile'],
            'hostile_zone_1_aircraft': self.second_category['hostile_in_zone_1'] + self.contacts_type['aircraft'],
            'hostile_zone_1_ship': self.second_category['hostile_in_zone_1'] + self.contacts_type['ship'],
            # 在区域zone_2中的敌方单元类型stat_hostile_zone_2_unit_type
            # 'hostile_zone_2_unknown': self.second_category['hostile_in_zone_2'] + self.contacts_type['unknown'],
            'hostile_zone_2_missile': self.second_category['hostile_in_zone_2'] + self.contacts_type['missile'],
            'hostile_zone_2_aircraft': self.second_category['hostile_in_zone_2'] + self.contacts_type['aircraft'],
            'hostile_zone_2_ship': self.second_category['hostile_in_zone_2'] + self.contacts_type['ship'],
            # 在区域zone_3中的敌方单元类型stat_hostile_zone_3_unit_type
            # 'hostile_zone_3_unknown': self.second_category['hostile_in_zone_3'] + self.contacts_type['unknown'],
            'hostile_zone_3_missile': self.second_category['hostile_in_zone_3'] + self.contacts_type['missile'],
            'hostile_zone_3_aircraft': self.second_category['hostile_in_zone_3'] + self.contacts_type['aircraft'],
            'hostile_zone_3_ship': self.second_category['hostile_in_zone_3'] + self.contacts_type['ship'],
            # 在区域zone_4中的敌方单元类型stat_hostile_zone_4_unit_type
            # 'hostile_zone_4_unknown': self.second_category['hostile_in_zone_4'] + self.contacts_type['unknown'],
            'hostile_zone_4_missile': self.second_category['hostile_in_zone_4'] + self.contacts_type['missile'],
            'hostile_zone_4_aircraft': self.second_category['hostile_in_zone_4'] + self.contacts_type['aircraft'],
            'hostile_zone_4_ship': self.second_category['hostile_in_zone_4'] + self.contacts_type['ship']}
        n_dims = reduce(lambda x, y: x+len(list(y)), list(self.stat_type.values()), 0) + len(self.stat_type)*2
        self.action_space = self._env.action_space
        self.observation_space = spaces.Tuple([spaces.Box(0.0, float('inf'), [n_dims], dtype=np.float32),
                                               spaces.Box(0.0, 1.0, [self._env.action_space.n], dtype=np.float32)])

    def _update(self, scenario):
        self.side = scenario.get_side_by_name(self.sideName)
        self.reward = float(self.side.iTotalScore) / 4067
        self.mozi_server = scenario.mozi_server
        self.ships = self.side.ships
        self.aircrafts = self.side.aircrafts
        self.contacts = self.side.contacts

    def step(self, action):
        # pdb.set_trace()
        scenario, mask, done = self._env.step(action)
        self._update(scenario) # 无用
        reward = self.reward
        obs = self._features()
        info = {}
        return (obs, mask), reward, done, info

    def reset(self):
        scenario, mask = self._env.reset()
        self._update(scenario)
        obs = self._features()
        return (obs, mask)

    def _features(self):
        # 空闲的单元类型stat_self_idle_unit_type
        feat_self_idle_unit = self._generate_features('stat_self_idle_unit_type', 'self_idle_asuw', 'self_idle_asup',
                                                            'self_idle_destroyer', 'self_idle_aircarrier')
        # 损失的单元类型stat_self_loss_unit_type
        feat_self_loss_unit = self._generate_features('stat_self_loss_unit_type', 'self_loss_asuw', 'self_loss_asup',
                                                            'self_loss_destroyer', 'self_loss_aircarrier')
        # 任务中的单元类型stat_self_busy_unit_type
        feat_self_busy_unit = self._generate_features('stat_self_busy_unit_type',
                                                      'self_busy_asuw', 'self_busy_asup',
                                                       'self_busy_destroyer', 'self_busy_aircarrier')
        # 在区域saw_zone中的单元类型stat_self_saw_zone_unit_type
        feat_self_saw_zone_unit = self._generate_features('stat_self_saw_zone_unit_type',
                                                      'self_saw_zone_asuw', 'self_saw_zone_asup',
                                                       'self_saw_zone_destroyer', 'self_saw_zone_aircarrier')
        # 在区域zone_1中的单元类型stat_self_zone_1_unit_type
        feat_self_zone_1_unit = self._generate_features('stat_self_zone_1_unit_type',
                                                      'self_zone_1_asuw', 'self_zone_1_asup',
                                                       'self_zone_1_destroyer', 'self_zone_1_aircarrier')
        # 在区域zone_2中的单元类型stat_self_zone_2_unit_type
        feat_self_zone_2_unit = self._generate_features('stat_self_zone_2_unit_type',
                                                      'self_zone_2_asuw', 'self_zone_2_asup',
                                                       'self_zone_2_destroyer', 'self_zone_2_aircarrier')
        # 在区域zone_3中的单元类型stat_self_zone_3_unit_type
        feat_self_zone_3_unit = self._generate_features('stat_self_zone_3_unit_type',
                                                        'self_zone_3_asuw', 'self_zone_3_asup',
                                                         'self_zone_3_destroyer', 'self_zone_3_aircarrier')
        # 在区域zone_4中的单元类型stat_self_zone_4_unit_type
        feat_self_zone_4_unit = self._generate_features('stat_self_zone_4_unit_type',
                                                        'self_zone_4_asuw', 'self_zone_4_asup',
                                                         'self_zone_4_destroyer', 'self_zone_4_aircarrier')
        # 消耗的武器类型stat_self_consumed_weapon_type
        feat_self_consumed_weapon = self._generate_features('stat_self_consumed_weapon_type',
                                                        'self_consumed_toll', 'self_consumed_air2airmissile',
                                                         'self_consumed_antishipmissile', 'self_consumed_airdefensemissile')
        # 任务中所有单元剩余武器类型stat_self_surplus_weapon_type
        feat_self_surplus_weapon = self._generate_features('stat_self_surplus_weapon_type',
                                                            'self_surplus_toll', 'self_surplus_air2airmissile',
                                                             'self_surplus_antishipmissile','self_surplus_airdefensemissile')
        # 探测到的敌方单元类型stat_hostile_unit_type
        feat_hostile_unit = self._generate_features('stat_hostile_unit_type', 'hostile_unknown', 'hostile_missile',
                                                                               'hostile_aircraft', 'hostile_ship')
        # 在区域zone_1中的敌方单元类型stat_hostile_zone_1_unit_type
        feat_hostile_zone_1_unit = self._generate_features('stat_hostile_zone_1_unit_type',
                                                           'hostile_zone_1_unknown', 'hostile_zone_1_missile',
                                                            'hostile_zone_1_aircraft', 'hostile_zone_1_ship')
        # 在区域zone_2中的敌方单元类型stat_hostile_zone_2_unit_type
        feat_hostile_zone_2_unit = self._generate_features('stat_hostile_zone_2_unit_type',
                                                           'hostile_zone_2_unknown', 'hostile_zone_2_missile',
                                                            'hostile_zone_2_aircraft', 'hostile_zone_2_ship')
        # 在区域zone_3中的敌方单元类型stat_hostile_zone_3_unit_type
        feat_hostile_zone_3_unit = self._generate_features('stat_hostile_zone_3_unit_type',
                                                           'hostile_zone_3_unknown', 'hostile_zone_3_missile',
                                                            'hostile_zone_3_aircraft', 'hostile_zone_3_ship')
        # 在区域zone_4中的敌方单元类型stat_hostile_zone_4_unit_type
        feat_hostile_zone_4_unit = self._generate_features('stat_hostile_zone_4_unit_type',
                                                           'hostile_zone_4_unknown', 'hostile_zone_4_missile',
                                                            'hostile_zone_4_aircraft', 'hostile_zone_4_ship')

        features = np.concatenate([feat_self_idle_unit,
                                   feat_self_loss_unit,
                                   feat_self_busy_unit,
                                   feat_self_saw_zone_unit,
                                   feat_self_zone_1_unit,
                                   feat_self_zone_2_unit,
                                   feat_self_zone_3_unit,
                                   feat_self_zone_4_unit,
                                   feat_self_consumed_weapon,
                                   feat_self_surplus_weapon,
                                   feat_hostile_unit,
                                   feat_hostile_zone_1_unit,
                                   feat_hostile_zone_2_unit,
                                   feat_hostile_zone_3_unit,
                                   feat_hostile_zone_4_unit])
        return features

    @property
    def num_dims(self):
        pass

    def _generate_features(self, feat_type, *args):
        if len(args) != 4:
            raise ValueError
        if feat_type == 'stat_self_idle_unit_type':
            feat_self_idle_unit = np.array([])
            for key in ['self_idle_asuw', 'self_idle_asup', 'self_idle_destroyer', 'self_idle_aircarrier']:
                value = [int(i) for i in list(self.stat_type[key])]
                unit_type = key[key.rfind('_')+1:]
                num = self._get_self_idle_units(unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_self_idle_unit = np.concatenate((feat_self_idle_unit, value), axis=0)
            return feat_self_idle_unit
        elif feat_type == 'stat_self_loss_unit_type':
            feat_self_loss_unit = np.array([])
            for key in ['self_loss_asuw', 'self_loss_asup', 'self_loss_destroyer', 'self_loss_aircarrier']:
                value = [int(i) for i in list(self.stat_type[key])]
                unit_type = key[key.rfind('_') + 1:]
                num = self._get_self_loss_units(unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_self_loss_unit = np.concatenate((feat_self_loss_unit, value), axis=0)
            return feat_self_loss_unit
        elif feat_type == 'stat_self_busy_unit_type':
            feat_self_busy_unit = np.array([])
            for key in ['self_busy_asuw', 'self_busy_asup', 'self_busy_destroyer', 'self_busy_aircarrier']:
                value = [int(i) for i in list(self.stat_type[key])]
                unit_type = key[key.rfind('_') + 1:]
                num = self._get_self_busy_units(unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_self_busy_unit = np.concatenate((feat_self_busy_unit, value), axis=0)
            return feat_self_busy_unit
        elif feat_type == 'stat_self_saw_zone_unit_type':
            feat_self_saw_zone_unit = np.array([])
            for key in ['self_saw_zone_asuw', 'self_saw_zone_asup', 'self_saw_zone_destroyer', 'self_saw_zone_aircarrier']:
                value = [int(i) for i in list(self.stat_type[key])]
                unit_type = key[key.rfind('_') + 1:]
                num = self._get_zone_self_units('saw_zone', unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_self_saw_zone_unit = np.concatenate((feat_self_saw_zone_unit, value), axis=0)
            return feat_self_saw_zone_unit
        elif feat_type == 'stat_self_zone_1_unit_type':
            feat_self_zone_1_unit = np.array([])
            for key in ['self_zone_1_asuw', 'self_zone_1_asup', 'self_zone_1_destroyer', 'self_zone_1_aircarrier']:
                value = [int(i) for i in list(self.stat_type[key])]
                unit_type = key[key.rfind('_') + 1:]
                num = self._get_zone_self_units('zone_1', unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_self_zone_1_unit = np.concatenate((feat_self_zone_1_unit, value), axis=0)
            return feat_self_zone_1_unit
        elif feat_type == 'stat_self_zone_2_unit_type':
            feat_self_zone_2_unit = np.array([])
            for key in ['self_zone_2_asuw', 'self_zone_2_asup', 'self_zone_2_destroyer', 'self_zone_2_aircarrier']:
                value = [int(i) for i in list(self.stat_type[key])]
                unit_type = key[key.rfind('_') + 1:]
                num = self._get_zone_self_units('zone_2', unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_self_zone_2_unit = np.concatenate((feat_self_zone_2_unit, value), axis=0)
            return feat_self_zone_2_unit
        elif feat_type == 'stat_self_zone_3_unit_type':
            feat_self_zone_3_unit = np.array([])
            for key in ['self_zone_3_asuw', 'self_zone_3_asup', 'self_zone_3_destroyer', 'self_zone_3_aircarrier']:
                value = [int(i) for i in list(self.stat_type[key])]
                unit_type = key[key.rfind('_') + 1:]
                num = self._get_zone_self_units('zone_3', unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_self_zone_3_unit = np.concatenate((feat_self_zone_3_unit, value), axis=0)
            return feat_self_zone_3_unit
        elif feat_type == 'stat_self_zone_4_unit_type':
            feat_self_zone_4_unit = np.array([])
            for key in ['self_zone_4_asuw', 'self_zone_4_asup', 'self_zone_4_destroyer', 'self_zone_4_aircarrier']:
                value = [int(i) for i in list(self.stat_type[key])]
                unit_type = key[key.rfind('_') + 1:]
                num = self._get_zone_self_units('zone_4', unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_self_zone_4_unit = np.concatenate((feat_self_zone_4_unit, value), axis=0)
            return feat_self_zone_4_unit
        elif feat_type == 'stat_self_consumed_weapon_type':
            feat_self_consumed_weapon = np.array([])
            for key in ['self_consumed_toll', 'self_consumed_air2airmissile', 'self_consumed_antishipmissile', 'self_consumed_airdefensemissile']:
                value = [int(i) for i in list(self.stat_type[key])]
                weapon_type = key[key.rfind('_') + 1:]
                num = self._get_self_consumed_weapon(weapon_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_self_consumed_weapon = np.concatenate((feat_self_consumed_weapon, value), axis=0)
            return feat_self_consumed_weapon
        elif feat_type == 'stat_self_surplus_weapon_type':
            feat_self_surplus_weapon = np.array([])
            for key in ['self_surplus_toll', 'self_surplus_air2airmissile', 'self_surplus_antishipmissile', 'self_surplus_airdefensemissile']:
                value = [int(i) for i in list(self.stat_type[key])]
                weapon_type = key[key.rfind('_') + 1:]
                num = self._get_self_surplus_weapon(weapon_type)
                scaled_num = num / 600
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_self_surplus_weapon = np.concatenate((feat_self_surplus_weapon, value), axis=0)
            return feat_self_surplus_weapon
        elif feat_type == 'stat_hostile_unit_type':
            feat_hostile_unit = np.array([])
            for key in ['hostile_missile', 'hostile_aircraft', 'hostile_ship']:
                value = [int(i) for i in list(self.stat_type[key])]
                h_unit_type = key[key.rfind('_')+1:]
                num = self._get_hostile_units(h_unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_hostile_unit = np.concatenate((feat_hostile_unit, value), axis=0)
            return feat_hostile_unit
        elif feat_type == 'stat_hostile_zone_1_unit_type':
            feat_hostile_zone_1_unit = np.array([])
            for key in ['hostile_zone_1_missile', 'hostile_zone_1_aircraft', 'hostile_zone_1_ship']:
                value = [int(i) for i in list(self.stat_type[key])]
                h_unit_type = key[key.rfind('_') + 1:]
                num = self._get_zone_hostile_units('zone_1', h_unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_hostile_zone_1_unit = np.concatenate((feat_hostile_zone_1_unit, value), axis=0)
            return feat_hostile_zone_1_unit
        elif feat_type == 'stat_hostile_zone_2_unit_type':
            feat_hostile_zone_2_unit = np.array([])
            for key in ['hostile_zone_2_missile', 'hostile_zone_2_aircraft', 'hostile_zone_2_ship']:
                value = [int(i) for i in list(self.stat_type[key])]
                h_unit_type = key[key.rfind('_') + 1:]
                num = self._get_zone_hostile_units('zone_2', h_unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_hostile_zone_2_unit = np.concatenate((feat_hostile_zone_2_unit, value), axis=0)
            return feat_hostile_zone_2_unit
        elif feat_type == 'stat_hostile_zone_3_unit_type':
            feat_hostile_zone_3_unit = np.array([])
            for key in ['hostile_zone_3_missile', 'hostile_zone_3_aircraft', 'hostile_zone_3_ship']:
                value = [int(i) for i in list(self.stat_type[key])]
                h_unit_type = key[key.rfind('_') + 1:]
                num = self._get_zone_hostile_units('zone_3', h_unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_hostile_zone_3_unit = np.concatenate((feat_hostile_zone_3_unit, value), axis=0)
            return feat_hostile_zone_3_unit
        elif feat_type == 'stat_hostile_zone_4_unit_type':
            feat_hostile_zone_4_unit = np.array([])
            for key in ['hostile_zone_4_missile', 'hostile_zone_4_aircraft', 'hostile_zone_4_ship']:
                value = [int(i) for i in list(self.stat_type[key])]
                h_unit_type = key[key.rfind('_') + 1:]
                num = self._get_zone_hostile_units('zone_4', h_unit_type)
                scaled_num = num / 16
                value.append(scaled_num)
                log_num = np.log10(scaled_num + 1)
                value.append(log_num)
                feat_hostile_zone_4_unit = np.concatenate((feat_hostile_zone_4_unit, value), axis=0)
            return feat_hostile_zone_4_unit
        else:
            raise TypeError

        return []

    def _get_self_idle_units(self, unit_type):
        """
        :param unit_type: 'asuw'、'asup'、'destroyer'、'aircarrier'
        :return:
        """
        if unit_type == 'asuw':
            num = 0
            for k, v in self.aircrafts.items():
                if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 3004:
                    if len(v.m_MultipleMissionGUIDs) == 0 or v.strAirOpsConditionString not in [0, 19, 20, 21]:
                        num += 1
            return num
        elif unit_type == 'asup':
            num = 0
            for k, v in self.aircrafts.items():
                if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 19361:
                    if len(v.m_MultipleMissionGUIDs) == 0 or v.strAirOpsConditionString not in [0, 19, 20, 21]:
                        num += 1
            return num
        elif unit_type == 'destroyer':  # 驱逐舰
            num = 0
            for k, v in self.ships.items():
                if v.m_Type == 3203 and len(v.m_MultipleMissionGUIDs) == 0:
                    num += 1
            return num
        elif unit_type == 'aircarrier':  # 航母
            num = 0
            for k, v in self.ships.items():
                if v.m_Type == 2008 and len(v.m_MultipleMissionGUIDs) == 0:
                    num += 1
            return num
        else:
            raise TypeError

    def _get_self_busy_units(self, unit_type):
        """

        :param unit_type: 'asuw'、'asup'、'destroyer'、'aircarrier'
        :return:
        """
        if unit_type == 'asuw':
            num = 0
            for k, v in self.aircrafts.items():
                if v.strLoadoutDBGUID == '': continue
                if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 3004:
                    if len(v.m_MultipleMissionGUIDs) > 0 and v.strAirOpsConditionString in [0, 19, 20, 21]:
                        num += 1
            return num
        elif unit_type == 'asup':
            num = 0
            for k, v in self.aircrafts.items():
                if v.strLoadoutDBGUID == '': continue
                if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 19361:
                    if len(v.m_MultipleMissionGUIDs) > 0 or v.strAirOpsConditionString in [0, 19, 20, 21]:
                        num += 1
            return num
        elif unit_type == 'destroyer':  # 驱逐舰
            num = 0
            for k, v in self.ships.items():
                if v.m_Type == 3203 and len(v.m_MultipleMissionGUIDs) > 0:
                    num += 1
            return num
        elif unit_type == 'aircarrier':  # 航母
            num = 0
            for k, v in self.ships.items():
                if v.m_Type == 2008 and len(v.m_MultipleMissionGUIDs) > 0:
                    num += 1
            return num
        else:
            raise TypeError

    def _get_self_loss_units(self, unit_type):
        """

        :param unit_type: 'asuw'、'asup'、'destroyer'、'aircarrier'
        :return:
        """
        # self.side.m_Losses.split('@')
        if unit_type == 'asuw':
            surplus = 0
            for k, v in self.aircrafts.items():
                if v.strLoadoutDBGUID == '': continue
                if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 3004:
                    surplus += 1
            return 8 - surplus
        elif unit_type == 'asup':
            surplus = 0
            for k, v in self.aircrafts.items():
                if v.strLoadoutDBGUID == '': continue
                if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 19361:
                    surplus += 1
            return 8 - surplus
        elif unit_type == 'destroyer':  # 驱逐舰
            surplus = 0
            for k, v in self.ships.items():
                if v.m_Type == 3203:
                    surplus += 1
            return 1 - surplus
        elif unit_type == 'aircarrier':  # 航母
            surplus = 0
            for k, v in self.ships.items():
                if v.m_Type == 2008:
                    surplus += 1
            return 1 - surplus
        else:
            raise TypeError

    def _get_zone_self_units(self, zone_type, unit_type):
        """

        :param zone_type: {'saw_zone': ['Offensive_rp_1', 'Offensive_rp_2', 'Offensive_rp_3', 'Offensive_rp_4'],
                      'zone_1': ['AI-AO-1', 'rp2', 'rp3', 'rp4'],
                      'zone_2': ['rp5', 'AI-AO-2', 'rp7', 'rp8'],
                      'zone_3': ['rp9', 'rp10', 'AI-AO-3', 'rp12'],
                      'zone_4': ['rp13', 'rp14', 'rp15', 'AI-AO-4']}
        :param unit_type: 'asuw'、'asup'、'destroyer'、'aircarrier'
        :return:
        """
        if zone_type not in ['saw_zone', 'zone_1', 'zone_2', 'zone_3', 'zone_4']:
            raise TypeError

        zone_points = self.zones[zone_type]
        zone_ref = [{'latitude': v.dLatitude, 'longitude': v.dLongitude} for k, v in self.side.referencepnts.items()
                    if v.strName in zone_points]
        if len(zone_ref) == 0:
            return 0

        if unit_type == 'asuw':
            num = 0
            for k, v in self.aircrafts.items():
                unit = {}
                unit['latitude'] = v.dLatitude
                unit['longitude'] = v.dLongitude
                if zone_contain_unit(zone_ref, unit):
                    num += 1
            return num
        elif unit_type == 'asup':
            num = 0
            for k, v in self.aircrafts.items():
                unit = {}
                unit['latitude'] = v.dLatitude
                unit['longitude'] = v.dLongitude
                if zone_contain_unit(zone_ref, unit):
                    num += 1
            return num
        elif unit_type == 'destroyer':  # 驱逐舰
            num = 0
            for k, v in self.ships.items():
                unit = {}
                unit['latitude'] = v.dLatitude
                unit['longitude'] = v.dLongitude
                if zone_contain_unit(zone_ref, unit):
                    num += 1
            return num
        elif unit_type == 'aircarrier':  # 航母
            num = 0
            for k, v in self.ships.items():
                unit = {}
                unit['latitude'] = v.dLatitude
                unit['longitude'] = v.dLongitude
                if zone_contain_unit(zone_ref, unit):
                    num += 1
            return num
        else:
            raise TypeError

    def _get_self_consumed_weapon(self, weapon_type):
        """

        :param weapon_type: 'toll', 'air2air_missile', 'antiship_missile', 'airdefense_missile'
        :return:
        """
        expenditures = list(map(lambda x: x.split('$'), self.side.m_Expenditures.split('@')))
        if len(expenditures) == 0:
            return 0

        if weapon_type == 'toll':   # 诱饵弹 2051-通用红外干扰弹；564-通用箔条；3386-AN/ALE70
            num = 0
            for weapon in expenditures:
                if weapon[0] != '' and weapon[-1] != '':
                    if int(re.sub('\D', '', weapon[0])) in [564, 2051, 3386]:
                        num += int(weapon[-1])
            return num
        elif weapon_type == 'air2airmissile':  #   空空导弹  51-AIM120D;945-AIM9X
            num = 0
            for weapon in expenditures:
                if weapon[0] != '' and weapon[-1] != '':
                    if int(re.sub('\D', '', weapon[0])) in [51, 945]:
                        num += int(weapon[-1])
            return num
        elif weapon_type == 'antishipmissile':  #  反舰导弹  826-AGM154C
            num = 0
            for weapon in expenditures:
                if weapon[0] != '' and weapon[-1] != '':
                    if int(re.sub('\D', '', weapon[0])) == 826:
                        num += int(weapon[-1])
            return num
        elif weapon_type == 'airdefensemissile':  #    防空导弹 15-RIM162A
            num = 0
            for weapon in expenditures:
                if weapon[0] != '' and weapon[-1] != '':
                    if int(re.sub('\D', '', weapon[0])) == 15:
                        num += int(weapon[-1])
            return num
        else:
            raise TypeError

    def _get_self_surplus_weapon(self, weapon_type):
        """

        :param weapon_type: 'toll', 'air2air_missile', 'antiship_missile', 'airdefense_missile'
        :return:
        """

        total_busy_units = self._get_self_total_busy_units()
        if len(total_busy_units) == 0:
            return 0
        if weapon_type == 'toll':   # 诱饵弹 2051-通用红外干扰弹；564-通用箔条；3386-AN/ALE70
            num = 0
            for unit in total_busy_units:
                weapon_list = self._get_unit_weapon(unit)
                for weapon in weapon_list:
                    if weapon[0] != '' and weapon[-1] != '':
                        if int(re.sub('\D', '', weapon[-1])) in [564, 2051, 3386]:
                            num += int(weapon[0])
            return num
        elif weapon_type == 'air2airmissile':  #   空空导弹  51-AIM120D;945-AIM9X
            num = 0
            for unit in total_busy_units:
                weapon_list = self._get_unit_weapon(unit)
                for weapon in weapon_list:
                    if weapon[0] != '' and weapon[-1] != '':
                        if int(re.sub('\D', '', weapon[-1])) in [51, 945]:
                            num += int(weapon[0])
            return num
        elif weapon_type == 'antishipmissile':  #  反舰导弹  826-AGM154C
            num = 0
            for unit in total_busy_units:
                weapon_list = self._get_unit_weapon(unit)
                for weapon in weapon_list:
                    if weapon[0] != '' and weapon[-1] != '':
                        if int(re.sub('\D', '', weapon[-1])) == 826:
                            num += int(weapon[0])
            return num
        elif weapon_type == 'airdefensemissile':  #    防空导弹 15-RIM162A
            num = 0
            for unit in total_busy_units:
                weapon_list = self._get_unit_weapon(unit)
                for weapon in weapon_list:
                    if weapon[0] != '' and weapon[-1] != '':
                        if int(re.sub('\D', '', weapon[-1])) == 15:
                            num += int(weapon[0])
            return num
        else:
            raise TypeError

    def _get_self_total_busy_units(self):

        total_busy_units = []
        for k, v in self.aircrafts.items():
            if len(v.m_MultipleMissionGUIDs) > 0 and v.strAirOpsConditionString in [0, 19, 20, 21]:
                total_busy_units.append(v)
        for k, v in self.ships.items():
            if len(v.m_MultipleMissionGUIDs) > 0:
                total_busy_units.append(v)
        return total_busy_units

    def _get_unit_weapon(self, unit):
        """

        :param unit: aircraft, ship
        :return:
        """
        weapon = list(map(lambda x: x.split('$'), unit.m_UnitWeapons.split('@')))
        weapon_list = list(map(lambda x, y: x+[y[-1]], list(map(lambda x: x[0].split('x '), weapon)), weapon))
        return weapon_list

    def _get_hostile_units(self, h_unit_type):
        """

        :param h_unit_type: unknown、missile、aircraft、ship
        :return:
        """
        contacts = self.contacts
        if h_unit_type == 'missile':  # m_ContactType = 1
            num = 0
            for k, v in contacts.items():
                if v.m_ContactType == 1:
                    num += 1
            return num
        elif h_unit_type == 'aircraft': # m_ContactType = 0
            num = 0
            for k, v in contacts.items():
                if v.m_ContactType == 0:
                    num += 1
            return num
        elif h_unit_type == 'ship':  # m_ContactType = 2
            num = 0
            for k, v in contacts.items():
                if v.m_ContactType == 2:
                    num += 1
            return num
        else:
            raise TypeError

    def _get_zone_hostile_units(self, zone_type, h_unit_type):
        """

        :param zone_type: {'saw_zone': ['Offensive_rp_1', 'Offensive_rp_2', 'Offensive_rp_3', 'Offensive_rp_4'],
                      'zone_1': ['AI-AO-1', 'rp2', 'rp3', 'rp4'],
                      'zone_2': ['rp5', 'AI-AO-2', 'rp7', 'rp8'],
                      'zone_3': ['rp9', 'rp10', 'AI-AO-3', 'rp12'],
                      'zone_4': ['rp13', 'rp14', 'rp15', 'AI-AO-4']}
        :param h_unit_type: unknown、missile、aircraft、ship
        :return:
        """
        if zone_type not in ['saw_zone', 'zone_1', 'zone_2', 'zone_3', 'zone_4']:
            raise TypeError

        zone_points = self.zones[zone_type]
        zone_ref = [{'latitude': v.dLatitude, 'longitude': v.dLongitude} for k, v in self.side.referencepnts.items()
                    if v.strName in zone_points]

        contacts = self.contacts

        if h_unit_type == 'missile':
            num = 0
            for k, v in contacts.items():
                if v.m_ContactType == 1:
                    unit = {}
                    unit['latitude'] = v.dLatitude
                    unit['longitude'] = v.dLongitude
                    if zone_contain_unit(zone_ref, unit):
                        num += 1
            return num
        elif h_unit_type == 'aircraft':
            num = 0
            for k, v in contacts.items():
                if v.m_ContactType == 0:
                    unit = {}
                    unit['latitude'] = v.dLatitude
                    unit['longitude'] = v.dLongitude
                    if zone_contain_unit(zone_ref, unit):
                        num += 1
            return num
        elif h_unit_type == 'ship':
            num = 0
            for k, v in contacts.items():
                if v.m_ContactType == 2:
                    unit = {}
                    unit['latitude'] = v.dLatitude
                    unit['longitude'] = v.dLongitude
                    if zone_contain_unit(zone_ref, unit):
                        num += 1
            return num
        else:
            raise TypeError


