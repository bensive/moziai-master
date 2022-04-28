# 时间 ： 2020/8/29 20:34
# 作者 ： Dixit
# 文件 ： tasks.py
# 项目 ： moziAIBT2
# 版权 ： 北京华戍防务技术有限公司

from mozi_ai_sdk.btmodel.bt import utils
import re
import random
import itertools
import uuid
from collections import namedtuple
import datetime
import numpy as np
from itertools import chain
from mozi_simu_sdk.mssnpatrol import CPatrolMission
from mozi_simu_sdk.mssnstrike import CStrikeMission
from mozi_ai_sdk.dppo.envs.utils import *
from mozi_ai_sdk.dppo.envs.spaces.mask_discrete import MaskDiscrete

# mission_type = {0: 'NoneValue : 未知',
#                 1: 'Strike : 打击/截击任务',
#                 2: 'Patrol : 巡逻任务',
#                 3: 'Support : 支援任务',
#                 4: 'Ferry : 转场任务',
#                 5: 'Mining : 布雷任务',
#                 6: 'MineClearing : 扫雷任务',
#                 7: 'Escort : 护航任务',
#                 8: 'Cargo : 投送任务'}
#
# strike_type = {0: 'AIR : 空中拦截',
#                1: 'LAND : 对陆打击',
#                2: 'SEA : 对海打击',
#                3: 'SUB : 对陆潜打击'}
#
# patrol_type = {0: 'AAW : 空战巡逻',
#                1: 'SUR_SEA : 反面(海)巡逻',
#                2: 'SUR_LAND : 反面(陆)巡逻',
#                3: 'SUR_MIXED : 反面(混)巡逻',
#                4: 'SUB : 反潜巡逻',
#                5: 'SEAD : 压制敌防空巡逻',
#                6: 'SEA : 海上控制巡逻'}
Function = namedtuple('Function', ['type', 'function', 'is_valid'])


class Task(object):
    def __init__(self, env, scenario, sideName):
        self.scenario = scenario
        self.time = self.scenario.m_Duration.split('@')  # 想定总持续时间
        self.m_StartTime = self.scenario.m_StartTime  # 想定开始时间
        self.m_Time = self.scenario.m_Time  # 想定当前时间
        self._env = env
        self.sideName = sideName
        self.side = self.scenario.get_side_by_name(self.sideName)
        # self.defend_zones = [['AI-AO-1', 'rp2', 'rp3', 'rp4'],
        #                      ['rp2', 'AI-AO-2', 'rp5', 'rp3'],
        #                      ['rp3', 'rp5', 'AI-AO-3', 'rp6'],
        #                      ['rp4', 'rp3', 'rp6', 'AI-AO-4']]
        self.defend_zones = [['AI-AO-1', 'rp2', 'rp3', 'rp4'],
                             ['rp4', 'rp3', 'rp6', 'AI-AO-4']]
        self.times = 15
        self.delta = 2  # 时间间隔1分钟
        self.offend_zone = ['Offensive_rp_1', 'Offensive_rp_2', 'Offensive_rp_3', 'Offensive_rp_4']
        self.asuw = {k: v for k, v in self.side.aircrafts.items()
                     if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 3004
                     and (len(v.m_MultipleMissionGUIDs) == 0)}  # 剩余可用反舰空战飞机
        self.asup = {k: v for k, v in self.side.aircrafts.items()
                     if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 19361
                     and (len(v.m_MultipleMissionGUIDs) == 0)}  # 剩余可用空战飞机
        self.target = {k: v for k, v in self.side.contacts.items() if v.m_ContactType == 2 and 'DDG' in v.strName}
        self.time_zone_combine = list(
            itertools.product([x for x in range(self.times)], [y for y in range(len(self.defend_zones))]))

        self._actions = list(
            chain.from_iterable([self._Action('donothing', self._ActionDoNothing, self._DoNothingIsValid),
                                 self._Action('defensive', self._DefensiveAirMissionAction, self._PatrolMissionIsValid),
                                 self._Action('offensive', self._OffensiveAirMissionAction, self._PatrolMissionIsValid),
                                 self._Action('attack', self._AttackAntiSurfaceShipMissionAction,
                                              self._AttackMissionIsValid)]))
        self.action_space = MaskDiscrete(len(self._actions))

    def _Action(self, type, function, is_valid):
        if type == 'donothing':
            func_list = []
            func_list.append(Function(type=type, function=function(), is_valid=is_valid()))
            return func_list
        elif type == 'defensive':
            func_list = []
            for times, i in self.time_zone_combine:
                missionName = 'defensive-' + str(uuid.uuid1())
                # key = random.choice(list(self.asup.keys()))
                # missionUnit = {key: self.asup[key]}
                zone = self.defend_zones[i]
                func_list.append(Function(type=type, function=function(missionName, times, zone), is_valid=is_valid()))
            return func_list
        elif type == 'offensive':
            func_list = []
            for times in range(self.times):
                missionName = 'offensive-' + str(uuid.uuid1())
                # key = random.choice(list(self.asup.keys()))
                # missionUnit = {key: self.asup[key]}
                func_list.append(
                    Function(type=type, function=function(missionName, times, self.offend_zone), is_valid=is_valid()))
            return func_list
        elif type == 'attack':
            func_list = []
            for times in range(5, self.times * 2):
                missionName = 'attack-' + str(uuid.uuid1())
                # key = random.choice(list(self.asuw.keys()))
                # missionUnit = {key: self.asuw[key]}
                func_list.append(
                    Function(type=type, function=function(missionName, times, self.target), is_valid=is_valid()))
            return func_list
        else:
            raise NotImplementedError

    def _get_valid_action_mask(self):
        ids = [i for i, action in enumerate(self._actions) if action.is_valid()]
        mask = np.zeros(self.action_space.n)
        mask[ids] = 1
        return mask

    def _update(self, scenario):
        self.scenario = scenario
        self.side = self.scenario.get_side_by_name(self.sideName)
        self.asuw = {k: v for k, v in self.side.aircrafts.items()
                     if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 3004
                     and (len(v.m_MultipleMissionGUIDs) == 0)}  # 剩余可用反舰空战飞机
        self.asup = {k: v for k, v in self.side.aircrafts.items()
                     if int(re.sub('\D', '', v.strLoadoutDBGUID)) == 19361
                     and (len(v.m_MultipleMissionGUIDs) == 0)}  # 剩余可用空战飞机
        self.target = {k: v for k, v in self.side.contacts.items() if v.m_ContactType == 2 and 'DDG' in v.strName}
        self.m_StartTime = self.scenario.m_StartTime  # 想定开始时间
        self.m_Time = self.scenario.m_Time  # 想定当前时间
        self._create_or_update_battle_zone()
        self._CreateOrUpdateOffensivePatrolZone()
        self._CreateOrUpdateDenfensivePatrolZone()
        doctrine = self.side.get_doctrine()
        # pdb.set_trace()
        # if doctrine.m_WCS_Surface != 0:
        #     doctrine.set_weapon_control_status('weapon_control_status_surface', '0')
        # if doctrine.m_WCS_Air != 0:
        #     doctrine.set_weapon_control_status('weapon_control_status_air', '0')

    def _assign_available_unit(self, action):
        if self._actions[action].type == 'donothing':
            mission_unit = {}
            pass
        elif self._actions[action].type == 'defensive':
            if len(self.asup) == 0:
                print('action: ', action, '未分配单元')
                return None
            key = random.choice(list(self.asup.keys()))
            mission_unit = {key: self.asup[key]}
        elif self._actions[action].type == 'offensive':
            if len(self.asup) == 0:
                print('action: ', action, '未分配单元')
                return None
            key = random.choice(list(self.asup.keys()))
            mission_unit = {key: self.asup[key]}
        elif self._actions[action].type == 'attack':
            if len(self.asuw) == 0:
                print('action: ', action, '未分配单元')
                return None
            key = random.choice(list(self.asuw.keys()))
            mission_unit = {key: self.asuw[key]}
        else:
            raise NotImplementedError
        for k, v in mission_unit.items():
            print('k:', k, 'v:', v)
            # pdb.set_trace()
            print('action: ', action, 'unit_name: ', v.strName)
        return mission_unit

    def step(self, action):
        mission_unit = self._assign_available_unit(action)
        if mission_unit != None:
            self._actions[action].function(mission_unit)
        print('action:', action)
        scenario = self._env.step()  # 墨子环境step，无用
        self._update(scenario)
        mask = self._get_valid_action_mask()
        done = self._is_done()
        return scenario, mask, done

    def reset(self):
        scenario = self._env.reset(self.sideName)
        self._update(scenario)
        mask = self._get_valid_action_mask()
        return scenario, mask

    def _is_done(self):
        # pdb.set_trace()
        # duration = int(self.time[0]) * 86400 + int(self.time[1]) * 3600 + int(self.time[2]) * 60
        # if self.m_StartTime + duration <= self.m_Time + 30:
        #     return True
        # else:
        #     pass
        # if len(self.side.contacts) == 0 or len(self.side.aircrafts) == 0:
        #     return True
        # else:
        #     return False

        # 对战平台
        response_dic = self.scenario.get_responses()
        for _, v in response_dic.items():
            if v.Type == 'EndOfDeduction':
                print('打印出标记：EndOfDeduction')
                return True
        return False

    # 修改任务参数
    def _SetTaskParam(self, mission, kwargs):
        # kwargs = {'missionName': miss1, 'missionType': '空战巡逻', 'flightSize': 2, 'checkFlightSize': True, 'oneThirdRule': True,
        #           'chechOpa': False, 'checkWwr': True, 'startTime': '08/09/2020 00:00:00',
        #           'endTime': '08/09/2020 12:00:00', 'isActive': 'true', 'missionUnit': , 'targets': }
        kwargs_keys = kwargs.keys()
        # 设置编队规模
        if 'flightSize' in kwargs_keys:
            mission.set_flight_size(kwargs['flightSize'])
        # 检查编队规模
        if 'checkFlightSize' in kwargs_keys:
            mission.set_flight_size_check('true')  # True
        # 设置1/3规则
        if 'oneThirdRule' in kwargs_keys:
            mission.set_one_third_rule(kwargs['oneThirdRule'])
        # 是否对巡逻区外的探测目标进行分析
        if 'chechOpa' in kwargs_keys:
            mission.set_opa_check(str(kwargs['chechOpa']))
        # 是否对武器射程内探测目标进行分析
        if 'checkWwr' in kwargs_keys:
            mission.set_wwr_check(kwargs['checkWwr'])
        # 设置任务的开始和结束时间
        if 'startTime' in kwargs_keys:
            cmd_str = "ScenEdit_SetMission('" + self.sideName + "','" + kwargs['missionName'] + "',{starttime='" + \
                      kwargs['startTime'] + "'})"
            self.scenario.mozi_server.send_and_recv(cmd_str)
        if 'endTime' in kwargs_keys:
            cmd_str = "ScenEdit_SetMission('" + self.sideName + "','" + kwargs['missionName'] + "',{endtime='" + kwargs[
                'endTime'] + "'})"
            self.scenario.mozi_server.send_and_recv(cmd_str)
        # 设置是否启动任务
        # if 'isActive' in kwargs_keys:
        #     lua = "ScenEdit_SetMission('%s','%s',{isactive='%s'})" % (self.sideName, kwargs['missionName'], kwargs['isActive'])
        #     self.scenario.mozi_server.send_and_recv(lua)
        if 'missionUnit' in kwargs_keys:
            mission.assign_units(kwargs['missionUnit'])
        if 'targets' in kwargs_keys:
            # mission.assign_targets(kwargs['targets'])
            self.side.assign_target_to_mission(kwargs['targets'], mission.strName)

    # 修改任务条令、电磁管控
    def _SetTaskDoctrineAndEMC(self, doctrine, kwargs):
        # kwargs = {'emc_radar': 'Passive', 'evadeAuto': 'true', 'ignorePlottedCourse': 'yes', 'targetsEngaging': 'true',
        #           'ignoreEmcon': 'false', 'weaponControlAir': '0', 'weaponControlSurface': '0', 'fuelStateForAircraft': '0',
        #           'fuelStateForAirGroup': '3', 'weaponStateForAircraft': '2001', 'weaponStateForAirGroup': '3'}

        kwargs_keys = kwargs.keys()

        # 电磁管控
        # em_item: {str: 'Radar' - 雷达, 'Sonar' - 声呐, 'OECM' - 光电对抗}
        # status: {str: 'Passive' - 仅有被动设备工作, 'Active' - 另有主动设备工作
        if 'emc_radar' in kwargs_keys:
            doctrine.set_em_control_status(em_item='Radar', status=kwargs['emc_radar'])
        # 设置是否自动规避
        if 'evadeAuto' in kwargs_keys:
            doctrine.evade_automatically(kwargs['evadeAuto'])
        # 设置是否忽略计划航线
        if 'ignorePlottedCourse' in kwargs_keys:
            doctrine.ignore_plotted_course(kwargs['ignorePlottedCourse'])
        # 接战临机出现目标
        # opportunity_targets_engaging_status: {str: 'true' - 可与任何目标交战, 'false' - 只与任务相关目标交战}
        if 'targetsEngaging' in kwargs_keys:
            doctrine.set_opportunity_targets_engaging_status(kwargs['targetsEngaging'])
        # 受攻击时是否忽略电磁管控
        if 'ignoreEmcon' in kwargs_keys:
            doctrine.ignore_emcon_while_under_attack(kwargs['ignoreEmcon'])

        # 设置武器控制状态
        # domain: {str: 'weapon_control_status_subsurface' - 对潜,
        #               'weapon_control_status_surface' - 对面,
        #               'weapon_control_status_land' - 对陆,
        #               'weapon_control_status_air' - 对空}
        # fire_status: {str: '0' - 自由开火, '1' - 谨慎开火, '2' - 限制开火}
        if 'weaponControlAir' in kwargs_keys:
            doctrine.set_weapon_control_status(domain='weapon_control_status_air',
                                               fire_status=kwargs['weaponControlAir'])
        if 'weaponControlSurface' in kwargs_keys:
            doctrine.set_weapon_control_status(domain='weapon_control_status_surface',
                                               fire_status=kwargs['weaponControlSurface'])

        # 设置单架飞机返航的油料状态
        if 'fuelStateForAircraft' in kwargs_keys:
            doctrine.set_fuel_state_for_aircraft(kwargs['fuelStateForAircraft'])
        # 设置飞行编队返航的油料状态
        # fuel_state: {str:   'No'('0') - 无约束，编队不返航,
        #                     'YesLastUnit'('1') - 编队中所有飞机均因达到单机油料状态要返航时，编队才返航,
        #                     'YesFirstUnit'('2') - 编队中任意一架飞机达到单机油料状态要返航时，编队就返航,
        #                     'YesLeaveGroup'('3') - 编队中任意一架飞机达到单机油料状态要返航时，其可离队返航}
        if 'fuelStateForAirGroup' in kwargs_keys:
            doctrine.set_fuel_state_for_air_group(kwargs['fuelStateForAirGroup'])
        # 设置单架飞机的武器状态
        if 'weaponStateForAircraft' in kwargs_keys:
            doctrine.set_weapon_state_for_aircraft(kwargs['weaponStateForAircraft'])
        # 设置飞行编队的武器状态
        # weapon_state: {str: 'No'('0') - 无约束，编队不返航,
        #                     'YesLastUnit'('1') - 编队中所有飞机均因达到单机武器状态要返航时，编队才返航,
        #                     'YesFirstUnit'('2') - 编队中任意一架飞机达到单机武器状态要返航时，编队就返航,
        #                     'YesLeaveGroup'('3') - 编队中任意一架飞机达到单机武器状态要返航时，其可离队返航}
        if 'weaponStateForAirGroup' in kwargs_keys:
            doctrine.set_weapon_state_for_air_group(kwargs['weaponStateForAirGroup'])

    def _PatrolMissionIsValid(self):
        def is_valid():
            if len(self.asup) == 0:
                return False
            else:
                return True

        return is_valid

    def _AttackMissionIsValid(self):
        def is_valid():
            if len(self.asuw) == 0:
                return False
            else:
                return True

        return is_valid

    def _DoNothingIsValid(self):
        def is_valid():
            return True

        return is_valid

    def _ActionDoNothing(self):
        def act(mission_unit):
            pass

        return act

    # 防御性巡逻任务
    def _DefensiveAirMissionAction(self, missionName, times, zone):
        def act(missionUnit):
            side = self.side
            # zone = ['Offensive_rp_1', 'Offensive_rp_2', 'Offensive_rp_3', 'Offensive_rp_4']
            patrolmssn = [v for _, v in side.patrolmssns.items() if v.strName == missionName]
            if len(patrolmssn) != 0:
                return False
            scen_time = '04/16/2020 22:00:00'
            mission_time = datetime.datetime.strptime(scen_time, '%m/%d/%Y %H:%M:%S') + datetime.timedelta(
                minutes=self.delta * times)
            DefensiveAirMiss = side.add_mission_patrol(missionName, 0, zone)  # 空战巡逻
            # DefensiveAirMiss = CPatrolMission('T+1_mode', self.scenario.mozi_server, self.scenario.situation)
            DefensiveAirMiss.strName = missionName
            taskParam = {'missionName': missionName, 'missionType': '空战巡逻', 'flightSize': 1, 'checkFlightSize': True,
                         'oneThirdRule': True, 'chechOpa': True, 'checkWwr': True,
                         'startTime': '%s' % str(mission_time),
                         'endTime': '08/09/2020 12:00:00', 'isActive': 'true', 'missionUnit': missionUnit}
            self._SetTaskParam(DefensiveAirMiss, taskParam)
            print('missionName ', mission_time, '***', len(missionUnit))
            doctrine = DefensiveAirMiss.get_doctrine()
            doctrineParam = {'emc_radar': 'Passive', 'evadeAuto': 'true', 'ignorePlottedCourse': 'yes',
                             'targetsEngaging': 'true',
                             'ignoreEmcon': 'false', 'weaponControlAir': '0', 'weaponControlSurface': '0',
                             'fuelStateForAircraft': '0',
                             'fuelStateForAirGroup': '3', 'weaponStateForAircraft': '2001',
                             'weaponStateForAirGroup': '3'}
            # self._SetTaskDoctrineAndEMC(doctrine, doctrineParam)

        return act

    # 攻击性巡逻任务
    def _OffensiveAirMissionAction(self, missionName, times, zone):
        def act(missionUnit):
            side = self.side
            # zone = ['Offensive_rp_1', 'Offensive_rp_2', 'Offensive_rp_3', 'Offensive_rp_4']
            patrolmssn = [v for _, v in side.patrolmssns.items() if v.strName == missionName]
            if len(patrolmssn) != 0:
                return False
            scen_time = '04/16/2020 22:00:00'
            mission_time = datetime.datetime.strptime(scen_time, '%m/%d/%Y %H:%M:%S') + datetime.timedelta(
                minutes=self.delta * times)
            OffensiveAirMiss = side.add_mission_patrol(missionName, 0, zone)  # 空战巡逻
            # OffensiveAirMiss = CPatrolMission('T+1_mode', self.scenario.mozi_server, self.scenario.situation)
            OffensiveAirMiss.strName = missionName
            taskParam = {'missionName': missionName, 'missionType': '空战巡逻', 'flightSize': 1, 'checkFlightSize': True,
                         'oneThirdRule': True, 'chechOpa': True, 'checkWwr': True,
                         'startTime': '%s' % str(mission_time),
                         'endTime': '08/09/2020 12:00:00', 'isActive': 'true', 'missionUnit': missionUnit}
            self._SetTaskParam(OffensiveAirMiss, taskParam)
            print('missionName ', mission_time, '***', len(missionUnit))
            doctrine = OffensiveAirMiss.get_doctrine()
            doctrineParam = {'emc_radar': 'Passive', 'evadeAuto': 'true', 'ignorePlottedCourse': 'yes',
                             'targetsEngaging': 'true',
                             'ignoreEmcon': 'false', 'weaponControlAir': '0', 'weaponControlSurface': '0',
                             'fuelStateForAircraft': '0',
                             'fuelStateForAirGroup': '3', 'weaponStateForAircraft': '2001',
                             'weaponStateForAirGroup': '3'}
            # self._SetTaskDoctrineAndEMC(doctrine, doctrineParam)

        return act

    # missionName,
    # missionType: 'strike' = 2, 'patrol' = 0
    # zone:
    # target,
    # missionUnit,
    # startTime: 5,10,15,...,60
    # taskParam:
    # doctrineParam:

    # 对海打击任务
    def _AttackAntiSurfaceShipMissionAction(self, missionName, times, target):
        def act(missionUnit):
            side = self.side
            strikemssn = [v for _, v in side.strikemssns.items() if v.strName == missionName]
            if len(strikemssn) != 0:
                return False
            _target = target
            if len(_target) == 0:
                _target = {k: v for k, v in self.side.contacts.items()}

            scen_time = '04/16/2020 22:00:00'
            mission_time = datetime.datetime.strptime(scen_time, '%m/%d/%Y %H:%M:%S') + datetime.timedelta(
                minutes=self.delta * times)
            AntiSurface = side.add_mission_strike(missionName, 2)
            # AntiSurface = CStrikeMission('T+1_mode', self.scenario.mozi_server, self.scenario.situation)
            AntiSurface.strName = missionName
            taskParam = {'missionName': missionName, 'missionType': '对海打击', 'flightSize': 1, 'checkFlightSize': True,
                         'startTime': '%s' % str(mission_time),
                         'endTime': '08/09/2020 12:00:00', 'isActive': 'true', 'missionUnit': missionUnit,
                         'targets': _target}
            self._SetTaskParam(AntiSurface, taskParam)
            print('missionName ', mission_time, '***', len(missionUnit))
            doctrine = AntiSurface.get_doctrine()
            doctrineParam = {'emc_radar': 'Passive', 'evadeAuto': 'true', 'ignorePlottedCourse': 'yes',
                             'targetsEngaging': 'true',
                             'ignoreEmcon': 'false', 'weaponControlAir': '0', 'weaponControlSurface': '0',
                             'fuelStateForAircraft': '0',
                             'fuelStateForAirGroup': '3', 'weaponStateForAircraft': '2001',
                             'weaponStateForAirGroup': '3'}
            # self._SetTaskDoctrineAndEMC(doctrine, doctrineParam)

        return act

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
            side.add_reference_point(zone[0], patrolBoundingBox[0]['latitude'], patrolBoundingBox[0]['longitude'])
            side.add_reference_point(zone[1], patrolBoundingBox[1]['latitude'], patrolBoundingBox[1]['longitude'])
            side.add_reference_point(zone[2], patrolBoundingBox[2]['latitude'], patrolBoundingBox[2]['longitude'])
            side.add_reference_point(zone[3], patrolBoundingBox[3]['latitude'], patrolBoundingBox[3]['longitude'])
        else:
            for i in range(len(patrolBoundingBox)):
                cmd = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                    self.sideName, 'AI-AO-' + str(i + 1), patrolBoundingBox[i]['latitude'],
                    patrolBoundingBox[i]['longitude'])
                self.scenario.mozi_server.send_and_recv(cmd)

    # 生成或更新攻击性巡逻任务的巡逻区域
    def _CreateOrUpdateOffensivePatrolZone(self):
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
                self.sideName, zone[0], hostileContactBoundingBox[0]['latitude'],
                hostileContactBoundingBox[0]['longitude'])
            self.scenario.mozi_server.send_and_recv(set_str_1)
            set_str_2 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.sideName, zone[1], hostileContactBoundingBox[1]['latitude'],
                hostileContactBoundingBox[1]['longitude'])
            self.scenario.mozi_server.send_and_recv(set_str_2)
            set_str_3 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.sideName, zone[2], hostileContactBoundingBox[2]['latitude'],
                hostileContactBoundingBox[2]['longitude'])
            self.scenario.mozi_server.send_and_recv(set_str_3)
            set_str_4 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.sideName, zone[3], hostileContactBoundingBox[3]['latitude'],
                hostileContactBoundingBox[3]['longitude'])
            self.scenario.mozi_server.send_and_recv(set_str_4)

    # 生成或更新防御性巡逻区域
    def _CreateOrUpdateDenfensivePatrolZone(self):
        side = self.side
        zone = ['AI-AO-1', 'AI-AO-2', 'AI-AO-3', 'AI-AO-4']
        defaults = {v.strName: {'latitude': v.dLatitude, 'longitude': v.dLongitude} for k, v in
                    side.referencepnts.items() if v.strName in zone}

        # hostileContacts = side.contacts
        # # inventory = {**side.aircrafts, **side.ships}
        # inventory = side.ships
        #  Loop and Get Coordinates
        # coordinates = []
        # for k, v in hostileContacts.items():
        #     coordinates.append(MakeLatLong(v.dLatitude, v.dLongitude))
        # for k, v in inventory.items():
        #     coordinates.append(MakeLatLong(v.dLatitude, v.dLongitude))
        # # Create Defense Bounding Box
        # patrolBoundingBox = FindBoundingBoxForGivenLocations(coordinates, 2)

        # if len(defaults) < 4:
        #     # patrolBoundingBox = FindBoundingBoxForGivenLocations(coordinates, 3.0)
        #     side.add_reference_point(self.sideName, zone[0], patrolBoundingBox[0]['latitude'], patrolBoundingBox[0]['longitude'])
        #     side.add_reference_point(self.sideName, zone[1], patrolBoundingBox[1]['latitude'], patrolBoundingBox[1]['longitude'])
        #     side.add_reference_point(self.sideName, zone[2], patrolBoundingBox[2]['latitude'], patrolBoundingBox[2]['longitude'])
        #     side.add_reference_point(self.sideName, zone[3], patrolBoundingBox[3]['latitude'], patrolBoundingBox[3]['longitude'])
        # else:
        #     for i in range(len(patrolBoundingBox)):
        #         cmd = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
        #             self.sideName, 'AI-AO-' + str(i+1), patrolBoundingBox[i]['latitude'], patrolBoundingBox[i]['longitude'])
        #         self.scenario.mozi_server.send_and_recv(cmd)

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
                self.sideName, 'rp2', rp12mid['latitude'], rp12mid['longitude'])
            self.scenario.mozi_server.send_and_recv(cmd1)
            cmd2 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.sideName, 'rp3', rp13mid['latitude'], rp13mid['longitude'])
            self.scenario.mozi_server.send_and_recv(cmd2)
            cmd3 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.sideName, 'rp4', rp14mid['latitude'], rp14mid['longitude'])
            self.scenario.mozi_server.send_and_recv(cmd3)
            cmd5 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.sideName, 'rp5', rp23mid['latitude'], rp23mid['longitude'])
            self.scenario.mozi_server.send_and_recv(cmd5)
            cmd9 = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(
                self.sideName, 'rp6', rp34mid['latitude'], rp34mid['longitude'])
            self.scenario.mozi_server.send_and_recv(cmd9)
