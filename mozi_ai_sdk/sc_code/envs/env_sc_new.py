# 时间 : 2021/6/16 16:43 
# 作者 : Dixit
# 文件 : env_ncc_new.py 
# 说明 : 
# 项目 : ncc_code
# 版权 : 北京华戍防务技术有限公司

from collections import namedtuple, OrderedDict
from ray.rllib.env.multi_agent_env import MultiAgentEnv, ENV_STATE
from ray.rllib.policy.sample_batch import SampleBatch
from ray.rllib.env.constants import GROUP_REWARDS, GROUP_INFO
import numpy as np

from mozi_ai_sdk.sc_code.envs.env import Environment
from mozi_ai_sdk.sc_code.envs import etc
from mozi_ai_sdk.sc_code.envs.utils.geo import plot_square, get_two_point_distance, get_cell, get_sudoku, \
    convert_coordinate_to_lat_lon, convert_lua_obj_to_dict
from mozi_ai_sdk.sc_code.envs.utils.train_data_utils import AgentCollector
from ray.remote_handle_docker import restart_mozi_container

import sys
import copy
import re
import random
import zmq
import time
from bidict import bidict
from datetime import datetime
import heapq

# zmq init
zmq_context = zmq.Context()
# ray request port
restart_requestor = zmq_context.socket(zmq.REQ)
Function = namedtuple('Function', ['type', 'function'])
FEATS_MAX_LEN = 350
MAX_DOCKER_RETRIES = 3
# 作战区域左上和右下点经纬度
RP_1 = (23.3131320340466, 119.038643031331)
# RP_2 = (15.0952995675627, 128.551360051763)
RP_2 = (14.0538827130597, 130.229734675437)
# 作战区域网格维度
OPERATION_AREA_GRID_DIM = 30
B_1_2 = (14, 0)
B_2_3 = (14, 8)
B_3_4 = (29, 8)
B_4_5 = (29, 29)
B_5_6 = (0, 29)
B_1_6 = (0, 0)
EXTERNAL_BOUNDARY = {'boundary_1': [(i, B_1_2[1]) for i in range(B_1_2[0] + 1)],  # (0->14, 0)
                     'boundary_2': [(B_1_2[0], i) for i in range(B_1_2[1] + 1, B_2_3[1] + 1)],  # (14, 1->8)
                     'boundary_1_2': [B_1_2],  # 属于边界1
                     'boundary_3': [(i, B_2_3[1]) for i in range(B_2_3[0] + 1, B_3_4[0] + 1)],  # (15->29, 8)
                     'boundary_2_3': [(B_2_3[0], B_2_3[1]), (B_2_3[0], B_2_3[1] + 1),
                                      (B_2_3[0] + 1, B_2_3[1] + 1), (B_2_3[0] + 1, B_2_3[1])],
                     'boundary_4': [(B_3_4[0], i) for i in range(B_3_4[1] + 1, B_4_5[1] + 1)],  # (29, 9->29)
                     'boundary_3_4': [B_3_4],  # 属于边界3
                     'boundary_5': [(i, B_4_5[1]) for i in range(B_4_5[0])],  # (0->28, 29)
                     'boundary_4_5': [B_4_5],  # 属于边界4
                     'boundary_6': [(B_5_6[0], i) for i in range(B_1_6[1], B_5_6[1])],  # (0, 1->28)
                     'boundary_5_6': [B_5_6],  # 属于边界5
                     'boundary_1_6': [B_1_6],  # 属于边界1
                     }

DESTROYER_NAME = '驱逐舰'
CARRIER_NAME = '航空母舰'
FIGHTER_NAME = '苏-33'
# 卫星过顶时间（分钟）
SATELLITE_ZENITH_TIME = 30

CARRIER_LOC = (18, 19)

# [(6, 7), (9, 10), (12, 13), (15, 16)]
ANCHOR_POINTS = [(CARRIER_LOC[0] - 12, CARRIER_LOC[1] - 12),
                 (CARRIER_LOC[0] - 9, CARRIER_LOC[1] - 9),
                 (CARRIER_LOC[0] - 6, CARRIER_LOC[1] - 6),
                 (CARRIER_LOC[0] - 3, CARRIER_LOC[1] - 3)]
ATTACK_CHAINS = len(ANCHOR_POINTS)
ATTACK_CHAIN_POINT_NUMS = 7
ATTACK_POINTS = sum(map(lambda x: list(zip(range(x[0] - 3, x[0] + 4), range(x[1] + 3, x[1] - 4, -1))), ANCHOR_POINTS),
                    [])

DEFENSE_RULE_UNITS_NAME = ['F-16V #19', 'F-16V #20']
TOP_RULE_UNITS_NAME = ['F-16A #21', 'F-16A #22']
BOT_RULE_UNITS_NAME = ['F-16A #23', 'F-16A #24']
EWR_NAME = ['E-2K #1']
EWR_SUPPORT_MISSION_NAME = "E-2K patrol"
# RULE_OPERATION_UNITS_NAME = TOP_RULE_UNITS_NAME + BOT_RULE_UNITS_NAME + EWR_NAME + DEFENSE_RULE_UNITS_NAME
RULE_OPERATION_UNITS_NAME = TOP_RULE_UNITS_NAME + BOT_RULE_UNITS_NAME + EWR_NAME
# EWR_PATROL_AREA = ['rp:7:6', 'rp:5:8']
EWR_PATROL_AREA = [(2, 3), (4, 4), (6, 7), (9, 10), (12, 13)]
SCOUT_POINT_LIST = [(4, 12), (10, 18), (9, 8), (15, 13), (15, 18)]

RULE_OPERATION_UNITS_TASK_STATUS = {'F-16A #21': {'first_stage': {'point': SCOUT_POINT_LIST[0], 'status': False},
                                                  'second_stage': {'point': SCOUT_POINT_LIST[1], 'status': False}},
                                    'F-16A #22': {'first_stage': {'point': SCOUT_POINT_LIST[0], 'status': False},
                                                  'second_stage': {'point': SCOUT_POINT_LIST[1], 'status': False}},
                                    'F-16A #23': {'first_stage': {'point': SCOUT_POINT_LIST[2], 'status': False},
                                                  'second_stage': {'point': SCOUT_POINT_LIST[3], 'status': False}},
                                    'F-16A #24': {'first_stage': {'point': SCOUT_POINT_LIST[2], 'status': False},
                                                  'second_stage': {'point': SCOUT_POINT_LIST[3], 'status': False}},
                                    }

EVADE_NUMS = 10  # 规避次数
# 规避进攻的距离
# rule_bot
AVOID_ATTACK_DISTANCE = 30
SCOUT_DETECT_DISTANCE = 50
EWR_DETECT_DISTANCE = 260
# 歼轰飞机自动攻击敌方舰船的距离
AUTO_ATTACK_SHIP_DISTANCE = 280
# 空战飞机自动攻击敌方飞机的距离
AUTO_ATTACK_AIR_DISTANCE = 150
# 风险度量距离
POINT_RISK_DISTANCE = 120  # 120
RISK_DISTANCE = 180
# 构造局部状态的距离
UNITS_DISTANCE = 80  # 统计附近的本方单元
ENEMY_DISTANCE = 200  # 统计附近的敌方单元

# 分层模型启动时间（分钟）
MODEL_START_TIME = random.randrange(10, 150, 5)  # 180
FIRST_STAGE_DURATION_TIME = MODEL_START_TIME / 4  # 45
# 基准停留时间(秒)
BASE_DWELL_TIME = 3
# 分数归一
SCORE_BOUND = 3000.
"""
建立作战单元编组、底层智能体、中层智能体与高层智能体的对应关系。
"""
# 空战飞机编组
AIR_TO_AIR_GROUP = {'UNIT_TYPE': 'F-16A', 'NUM': 2, 'WEAPON_TYPE': 'AIM'}  # 两机编队
AIR_TO_AIR_GROUPS = ['A2A_GROUP_1', 'A2A_GROUP_2', 'A2A_GROUP_3', 'A2A_GROUP_4']
# 歼轰飞机编组
AIR_TO_SURFACE_GROUP = {'UNIT_TYPE': 'F-16A', 'NUM': 6, 'WEAPON_TYPE': 'AGM'}  # 六机编队
AIR_TO_SURFACE_GROUPS = ['A2S_GROUP_1', 'A2S_GROUP_2', 'A2S_GROUP_3', 'A2S_GROUP_4']
# 电子干扰机
ELECTRONIC_JAMMER = {'UNIT_TYPE': 'EC-130H', 'NUM': 1}  # 单机编队
ELECTRONIC_JAMMER_GROUPS = ['EJ_1', 'EJ_2', 'EJ_3', 'EJ_4']

LOW_LEVEL_AGENT_NUM = len(AIR_TO_AIR_GROUPS) + len(AIR_TO_SURFACE_GROUPS) + \
                      len(ELECTRONIC_JAMMER_GROUPS)
LOW_LEVEL_AGENT_IDs = [f'll_agent_{i}' for i in range(LOW_LEVEL_AGENT_NUM)]
OPERATION_GROUPS = AIR_TO_AIR_GROUPS + AIR_TO_SURFACE_GROUPS + ELECTRONIC_JAMMER_GROUPS
LL_AGENTS_TO_OPERATION_GROUPS = dict(zip(LOW_LEVEL_AGENT_IDs, OPERATION_GROUPS))
OPERATION_GROUPS_TO_LL_AGENTS = dict(zip(OPERATION_GROUPS, LOW_LEVEL_AGENT_IDs))

MID_LEVEL_AGENT_IDs = [f'ml_agent_{i}' for i in range(LOW_LEVEL_AGENT_NUM)]
MID_LEVEL_AGENT_GROUPS = ['a2s_agent_group_1', 'a2s_agent_group_2', 'a2s_agent_group_3',
                          'a2s_agent_group_4']  # for qmix group
assert len(AIR_TO_AIR_GROUPS) == len(AIR_TO_SURFACE_GROUPS) == len(ELECTRONIC_JAMMER_GROUPS) == len(
    MID_LEVEL_AGENT_GROUPS)
MID_LEVEL_AGENT_GROUPS_TO_OPERATION_GROUPS = {MID_LEVEL_AGENT_GROUPS[i]:
                                                  [AIR_TO_AIR_GROUPS[i], AIR_TO_SURFACE_GROUPS[i],
                                                   ELECTRONIC_JAMMER_GROUPS[i]]
                                              for i in range(len(MID_LEVEL_AGENT_GROUPS))}

assert len(MID_LEVEL_AGENT_IDs) == len(LOW_LEVEL_AGENT_IDs)
ML_AGENTS_TO_LL_AGENTS = bidict(zip(MID_LEVEL_AGENT_IDs, LOW_LEVEL_AGENT_IDs))


def ml_agent_groups_to_ml_agent_id():
    ml_agent_groups_to_agent_id = {}
    for agent_group, op_groups in MID_LEVEL_AGENT_GROUPS_TO_OPERATION_GROUPS.items():
        ml_agent_groups_to_agent_id[agent_group] = \
            [ML_AGENTS_TO_LL_AGENTS.inverse[OPERATION_GROUPS_TO_LL_AGENTS[op_group]] for op_group in op_groups]
    return ml_agent_groups_to_agent_id


HIGH_LEVEL_AGENT_IDs = [f'hl_agent_{i}' for i in range(len(MID_LEVEL_AGENT_GROUPS))]
HL_AGENT_ID_TO_ML_AGENT_GROUPS = {HIGH_LEVEL_AGENT_IDs[i]: MID_LEVEL_AGENT_GROUPS[i]
                                  for i in range(len(MID_LEVEL_AGENT_GROUPS))}
HL_AGENTS_TO_ML_AGENTS = {HIGH_LEVEL_AGENT_IDs[i]: ml_agent_groups_to_ml_agent_id()[MID_LEVEL_AGENT_GROUPS[i]]
                          for i in range(len(MID_LEVEL_AGENT_GROUPS))}
HIGH_LEVEL_GROUP_AGENT_IDs = 'group_0'  # for qmix group
# groups = {'group_0': ['hl_agent_0', 'hl_agent_1', 'hl_agent_2', 'hl_agent_3'],
#           'a2s_agent_group_1': ['ml_agent_0', 'ml_agent_1', 'ml_agent_2'],
#           'a2s_agent_group_2': ['ml_agent_3', 'ml_agent_4', 'ml_agent_5'],
#           'a2s_agent_group_3': ['ml_agent_6', 'ml_agent_7', 'ml_agent_8'],
#           'a2s_agent_group_4': ['ml_agent_9', 'ml_agent_10', 'ml_agent_11']}
GROUPS = {HIGH_LEVEL_GROUP_AGENT_IDs: HIGH_LEVEL_AGENT_IDs}
GROUPS.update(ml_agent_groups_to_ml_agent_id())


def ml_agent_to_hl_agent(ml_agent_id):  # 通过mid level的agent_id找到对应的high level的agent_id
    for hl_agent_id, ml_agent_ids in HL_AGENTS_TO_ML_AGENTS.items():
        if ml_agent_id in ml_agent_ids:
            return hl_agent_id


# AGENT_IDs = LOW_LEVEL_AGENT_IDs + MID_LEVEL_AGENT_IDs + HIGH_LEVEL_AGENT_IDs
LL_DATA_COLLECTOR = {
    agent_id: AgentCollector()
    for agent_id in LOW_LEVEL_AGENT_IDs
}
HL_ML_AGENT_IDs = MID_LEVEL_AGENT_IDs + HIGH_LEVEL_AGENT_IDs
LAST_HL_ML_AGENTS_ACTION = {
    agent_id: None
    for agent_id in HL_ML_AGENT_IDs
}
LAST_ML_AGENTS_OBS_REWARD_DONE = {
    agent_id: {}
    for agent_id in MID_LEVEL_AGENT_IDs
}
HL_DATA_COLLECTOR = {
    agent_id: AgentCollector()
    for agent_id in HIGH_LEVEL_AGENT_IDs
}

LOW_LEVEL_OBS_SPACE = 21
STATE_SPACE = 19
LOW_LEVEL_ACT_SPACE = (3, 2)  # 高度(0:保持原高度；1:降高；2：升高)和速度(0: 保持原速度；1：加速)

MID_LEVEL_OBS_SPACE = LOW_LEVEL_OBS_SPACE * 8  # 取最近10步的数据
MID_LEVEL_STATE_SPACE = STATE_SPACE * 5  # 取最近10步的数据
MID_LEVEL_ACT_SPACE = 9
MID_LEVEL_ACTION_EMBED = 6

HIGH_LEVEL_OBS_SPACE = MID_LEVEL_OBS_SPACE * 3 * 6
HIGH_LEVEL_STATE_SPACE = MID_LEVEL_STATE_SPACE * 3 * 5
HIGH_LEVEL_ACT_SPACE = 28  # 5
HIGH_LEVEL_ACTION_EMBED = 6


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


class MoziEnv(object):

    def __init__(self, env_config):
        self.steps = None
        self.env_config = env_config
        self.env_config['avail_docker_ip_port'] = ['127.0.0.1:6060', ]
        self.reset_nums = 0
        self._get_env()
        self.side_name = env_config['side_name']
        print('开始mozi reset!!!')
        self.scenario = self.env.reset()
        print('结束mozi reset!!!')

        self.time = self.scenario.m_Duration.split('@')  # 想定总持续时间
        self.m_StartTime = self.scenario.m_StartTime  # 想定开始时间
        self.m_Time = self.scenario.m_Time  # 想定当前时间

        self.side = self.scenario.get_side_by_name(self.side_name)
        self.enemy_side = self.scenario.get_side_by_name(env_config['enemy_side_name'])
        self._init_data_structure()
        # 中层智能体的action_mask和avail_actions
        local_seed = np.random.RandomState(0)
        self.mid_level_action_embed = {agent_id: local_seed.rand(MID_LEVEL_ACT_SPACE, MID_LEVEL_ACTION_EMBED)
                                       for agent_id in MID_LEVEL_AGENT_IDs}
        self.high_level_action_embed = {agent_id: local_seed.rand(HIGH_LEVEL_ACT_SPACE, HIGH_LEVEL_ACTION_EMBED)
                                        for agent_id in HIGH_LEVEL_AGENT_IDs}
        self.high_level_init_avail_action = list(range(ATTACK_CHAIN_POINT_NUMS))

        self.no_nav_area_info = {}

    def _init_data_structure(self):
        self.ll_reward = {agent_id: 0.0 for agent_id in LOW_LEVEL_AGENT_IDs}
        self.ml_reward = {agent_id: 0.0 for agent_id in MID_LEVEL_AGENT_IDs}
        self.hl_reward = {agent_id: 0.0 for agent_id in HIGH_LEVEL_AGENT_IDs}

        # 对分层模型所需的空战、歼轰、电子干扰机进行分组
        self.air_to_air_groups = {AIR_TO_AIR_GROUPS[i]: {} for i in range(len(AIR_TO_AIR_GROUPS))}
        self.air_to_air_group_name_to_guid = {AIR_TO_AIR_GROUPS[i]: None for i in range(len(AIR_TO_AIR_GROUPS))}
        self.air_to_surface_groups = {AIR_TO_SURFACE_GROUPS[i]: {} for i in range(len(AIR_TO_SURFACE_GROUPS))}
        self.air_to_surface_group_name_to_guid = \
            {AIR_TO_SURFACE_GROUPS[i]: None for i in range(len(AIR_TO_SURFACE_GROUPS))}
        self.electronic_jammer_groups = {ELECTRONIC_JAMMER_GROUPS[i]: {} for i in range(len(ELECTRONIC_JAMMER_GROUPS))}
        self.electronic_jammer_group_name_to_guid = \
            {ELECTRONIC_JAMMER_GROUPS[i]: None for i in range(len(ELECTRONIC_JAMMER_GROUPS))}
        self.operation_groups_name_to_guid = {}
        self.operation_groups = {}
        self.operation_groups_status = {op: False for op in OPERATION_GROUPS}
        self.operation_groups_class = {}
        self.dwell_time = {"start_time": None, "dwell_time": None}
        self.update_next_point = False
        self.update_next_attack_point = False
        self.operation_groups_last_area = {op: [] for op in OPERATION_GROUPS}

        self.mid_level_avail_action_action_mask = {agent_id: {"action_mask": None, "avail_actions": None}
                                                   for agent_id in MID_LEVEL_AGENT_IDs}
        self.high_level_avail_action_action_mask = {agent_id: {"action_mask": None, "avail_actions": None}
                                                    for agent_id in HIGH_LEVEL_AGENT_IDs}
        self.auto_attack_ships = {}
        self.hl_last_attack_points = {hl_agent_id: None for hl_agent_id in HIGH_LEVEL_AGENT_IDs}

    def _get_win_score(self):
        if self.steps % 10 == 0:
            print(f'step: {self.steps} redside total score is {self.side.iTotalScore}')
        return float(self.side.iTotalScore)

    def _update(self, scenario):
        self.side = scenario.get_side_by_name(self.side_name)
        self.agent_operation_units = {k: v for k, v in self.side.aircrafts.items()
                                      if v.strName not in RULE_OPERATION_UNITS_NAME}
        self.rule_operation_units = {k: v for k, v in self.side.aircrafts.items()
                                     if v.strName in RULE_OPERATION_UNITS_NAME}

        self.operation_groups_class = {v.strName: v
                                       for _, v in self.side.groups.items()}
        self.operation_groups_class.update({v.strName: v
                                            for _, v in self.side.aircrafts.items()
                                            if 'EJ' in v.strName})
        self._update_operation_groups()
        self._update_operation_groups_status()

        self.attack_ships = {k: v
                             for k, v in self.side.contacts.items() if v.m_ContactType == 2}
        if self.steps % 10 == 0:
            self.update_ships_no_nav_area()
        self.attack_airs = {k: v
                            for k, v in self.side.contacts.items() if v.m_ContactType == 0}

        self.m_Time = self.scenario.m_Time  # 想定当前时间
        # 所有单元规避进攻
        # self.all_unit_avoid_attack()
        # 更新预警飞机的位置
        self.update_ewr_location()
        # 返回基地
        self.return_to_base()

    def step(self, action, ml_status, hl_status):
        self.steps += 1
        self.ll_reward = {agent_id: 0.0 for agent_id in LOW_LEVEL_AGENT_IDs}
        self.ml_reward = {agent_id: 0.0 for agent_id in MID_LEVEL_AGENT_IDs}
        self.hl_reward = {agent_id: 0.0 for agent_id in HIGH_LEVEL_AGENT_IDs}
        self.update_next_point = ml_status
        self.update_next_attack_point = hl_status
        self.low_level_agent_execute_action(action)
        # self.get_reward(action)

        done = False
        if self.env_config['mode'] in ['train', 'development']:
            force_done = self.safe_step()
            if force_done:
                done = force_done
                self.reset_nums = 4  # 下一局会重启墨子docker(每5局重启一次docker)
                print(f"{time.strftime('%H:%M:%S')} 在第{self.steps}步，强制重启墨子！！！")
            else:
                self._update(self.scenario)
                done = self._is_done()
        elif self.env_config['mode'] in ['versus', 'eval']:
            self.scenario = self.env.step()  # 墨子环境step
            self._update(self.scenario)
            done = self._is_done()
        dones, ret_ml, ret_hl, infos = self._generate_dones_rets_masks_infos(action)
        if ret_ml["__all__"]:
            self.update_ml_agent_reward(action, dones["__all__"])
        if ret_hl["__all__"]:
            self.update_hl_agent_reward(action, dones["__all__"])
        self.update_ll_agent_reward(action, dones["__all__"])

        global_obs = self._generate_global_features()
        low_level_agent_obs = self._generate_local_features()

        if self.steps % 10 == 0:
            print(self.ip_port + '-' + f'reward is {self.ll_reward}' + '-' + f'action is {action}')
        if done:
            print('++++Score:', self._get_win_score(), 'step:', self.steps)
        return (low_level_agent_obs, global_obs,
                self.ll_reward, self.ml_reward, self.hl_reward,
                ret_ml, ret_hl, dones, infos,
                self.mid_level_avail_action_action_mask, self.high_level_avail_action_action_mask)

    def safe_step(self):
        force_done = False
        # noinspection PyBroadException
        try:
            pass
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
        global MODEL_START_TIME, FIRST_STAGE_DURATION_TIME
        MODEL_START_TIME = random.randrange(50, 150, 5)  # 180
        FIRST_STAGE_DURATION_TIME = MODEL_START_TIME / 4  # 45
        self.last_t_score = 0.0

        self.ewr_last_point = ()
        self._get_initial_state()
        self.steps = 0
        self._init_data_structure()
        self._update(self.scenario)

        # 画出战场区域网格图
        plot_square(OPERATION_AREA_GRID_DIM, self.side, RP_1, RP_2)

        self.no_nav_area_info = {}

        self.scenario = self.env.step()  # 墨子环境step
        self._update(self.scenario)
        self._set_side_doctrine()  # 设置推演方条令
        self._set_simulate_speed(etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL)  # 设置推演倍速为30倍速

        # 启动规则智能体
        self.rule_bot()
        self._set_simulate_speed(etc.SIMULATE_COMPRESSION_2, etc.DURATION_INTERVAL_2)  # 设置推演倍速为5倍速

        # 创建编组，让墨子中作战单元按编组出动
        self.create_operation_groups()
        # 作战单元出动
        self.operation_group_out()
        self.scenario = self.env.step()  # 墨子环境step
        self._update(self.scenario)
        self.operation_group_name_to_guid()  # python中的作战单元编组名，与墨子中实际的作战单元编组唯一guid，建立映射关系。
        self.scenario = self.env.step()  # 墨子环境step
        self._update(self.scenario)
        # 获取作战编组的初始位置和区域
        self.get_operation_groups_init_area()
        global_obs = self._generate_global_features()
        multi_agent_obs = self._generate_local_features()
        return multi_agent_obs, global_obs

    # 《《《《《《《《《《《《《 rule_bot 》》》》》》》》》》》》》》

    def get_bear_point(self, point_name_prefix, lat, lon, bearing_list, distance):
        points_dict = {}
        for i, bearing in enumerate(bearing_list):
            point_name = point_name_prefix + f"{i}"
            cmd = "print(World_GetPointFromBearing({" + \
                  f"latitude=\'{lat}\', longitude=\'{lon}\', BEARING=\'{bearing}\', DISTANCE=\'{distance}\'" + "}))"
            ret = self.scenario.mozi_server.send_and_recv(cmd)
            ret = convert_lua_obj_to_dict(ret)
            point = (ret['Latitude'], ret['Longitude'])
            points_dict[point_name] = point
        return points_dict

    def set_ref_points(self, points_dict):
        for point_name, p in points_dict.items():
            cmd = "ScenEdit_AddReferencePoint({" + \
                  f"side='{self.side_name}', name='{point_name}', lat={p[0]}, lon={p[1]}" + "})"
            self.scenario.mozi_server.send_and_recv(cmd)

    def delete_ref_points(self, points_name):
        for point_name in points_name:
            cmd = "ScenEdit_DeleteReferencePoint({" + f"side='{self.side_name}',name='{point_name}'" + "})"
            self.scenario.mozi_server.send_and_recv(cmd)

    def update_ref_points(self, area_name, latitude, longitude, outer_distance=20, inner_distance=19.8):
        # 根据新的中心坐标点更新环形区域
        # 正北方向为0度，顺时针方向每30度设置一个参考点
        bearing_list = [i for i in range(0, 361, 30)]  # 331
        # outer_distance = 20  # 海里
        point_name_prefix = f"{area_name}-outer-no-nav-"
        outer_points_dict = self.get_bear_point(point_name_prefix, latitude, longitude, bearing_list, outer_distance)
        self.no_nav_area_info[area_name].update(outer_points_dict)

        # 正北方向为0度，逆时针方向每30度设置一个参考点
        bearing_list = [i for i in range(360, -1, -30)]
        # inner_distance = 10  # 海里
        point_name_prefix = f"{area_name}-inner-no-nav-"
        inner_points_dict = self.get_bear_point(point_name_prefix, latitude, longitude, bearing_list, inner_distance)
        self.no_nav_area_info[area_name].update(inner_points_dict)

        for point_name, point in self.no_nav_area_info[area_name].items():
            cmd = "ScenEdit_SetReferencePoint({" + \
                  f"side='{self.side_name}',name='{point_name}', lat={point[0]}, lon={point[1]}" + "})"
            self.scenario.mozi_server.send_and_recv(cmd)

    def set_no_nav_area(self, area_center_name, center_lat, center_lon, outer_distance=20, inner_distance=19.8):
        # 正北方向为0度，顺时针方向每30度设置一个参考点
        bearing_list = [i for i in range(0, 361, 30)]   # 331
        # outer_distance = 20  # 海里
        point_name_prefix = f"{area_center_name}-outer-no-nav-"
        outer_points_dict = self.get_bear_point(point_name_prefix, center_lat, center_lon, bearing_list, outer_distance)
        self.no_nav_area_info[area_center_name] = outer_points_dict
        self.set_ref_points(outer_points_dict)

        # 正北方向为0度，逆时针方向每30度设置一个参考点
        bearing_list = [i for i in range(360, -1, -30)]
        # inner_distance = 10  # 海里
        point_name_prefix = f"{area_center_name}-inner-no-nav-"
        inner_points_dict = self.get_bear_point(point_name_prefix, center_lat, center_lon, bearing_list, inner_distance)
        self.no_nav_area_info[area_center_name].update(inner_points_dict)
        self.set_ref_points(inner_points_dict)

        if not self.no_nav_area_info[area_center_name]:
            raise ValueError

        cmd = f"ScenEdit_AddZone('{self.side_name}', 0, " + \
              "{" + f"description='{area_center_name}', " + "Isactive=true, Affects={'Aircraft'}, Area={"
        for point_name in self.no_nav_area_info[area_center_name].keys():
            cmd += f"'{point_name}', "
        cmd = cmd + "}})"
        self.scenario.mozi_server.send_and_recv(cmd)

    def update_ships_no_nav_area(self):
        for ship_name, ship_value in self.attack_ships.items():
            if ship_name in self.no_nav_area_info:
                self.update_ref_points(ship_name, ship_value.dLatitude, ship_value.dLongitude)
            else:
                self.set_no_nav_area(ship_name, ship_value.dLatitude, ship_value.dLongitude)
        # 删除多余禁航区参考点
        points_name = []
        areas_name = []
        for area_name in self.no_nav_area_info.keys():
            if area_name not in self.attack_ships:
                areas_name.append(area_name)
        for area_name in areas_name:
            points_dict = self.no_nav_area_info.pop(area_name)
            points_name += points_dict.keys()

        if points_name:
            self.delete_ref_points(points_name)

    def _high_level_mask(self, last_area_coord_points, hl_action, ret_hl):
        attack_point = ATTACK_POINTS[hl_action]
        hl_avail_action = []
        # if attack_point:
        delta_x = attack_point[0] - last_area_coord_points[0][0]
        delta_y = attack_point[1] - last_area_coord_points[0][1]
        chain_index = int(hl_action / ATTACK_CHAIN_POINT_NUMS)
        if delta_x + delta_y > 0:
            lower_index = chain_index * ATTACK_CHAIN_POINT_NUMS if chain_index > 0 else 0
            upper_index = (chain_index + 1) * ATTACK_CHAIN_POINT_NUMS
            hl_avail_action = list(range(lower_index, upper_index))
            return chain_index, hl_avail_action
        else:
            ret_hl["__all__"] = True
            if chain_index < ATTACK_CHAINS - 1:
                # 到达打击点，更新下一步可用打击点
                lower_index = (chain_index + 1) * ATTACK_CHAIN_POINT_NUMS
                upper_index = (chain_index + 2) * ATTACK_CHAIN_POINT_NUMS
                # hl_avail_action = list(range(lower_index, upper_index))
                for ap in ATTACK_POINTS[lower_index:upper_index]:
                    delta = abs(attack_point[0] - ap[0]) + abs(attack_point[1] - ap[1])
                    if delta == 6:
                        hl_avail_action.append(ATTACK_POINTS.index(ap))
                return chain_index + 1, hl_avail_action
            elif chain_index == ATTACK_CHAINS - 1:
                lower_index = chain_index * ATTACK_CHAIN_POINT_NUMS
                upper_index = (chain_index + 1) * ATTACK_CHAIN_POINT_NUMS
                hl_avail_action = list(range(lower_index, upper_index))
                return chain_index, hl_avail_action

    def _mid_level_mask(self, last_area_coord_points, hl_action, ml_avail_action):
        """

        :param last_area_coord_points:
        :param hl_action:
        :param ml_avail_action:
        :return: 中层智能体当前可用动作
        """

        attack_point = ATTACK_POINTS[hl_action]

        # self.avail_attack_points = {hl_agent_id: [] for hl_agent_id in HIGH_LEVEL_AGENT_IDs}  # 智能体编队可用打击点列表
        ml_avail_action = self.mid_level_agent_move_mask(last_area_coord_points, ml_avail_action, attack_point)
        return ml_avail_action

    @staticmethod
    def mid_level_agent_move_mask(last_area_coord_points, avail_action, attack_point):
        y_delta = last_area_coord_points[0][0] - attack_point[0]
        x_delta = last_area_coord_points[0][1] - attack_point[1]
        if y_delta < 0 and x_delta < 0:
            avail_action = list(set(avail_action).intersection(('0', '4', '5', '6')))
        elif y_delta > 0 and x_delta < 0:
            avail_action = list(set(avail_action).intersection(('0', '3', '4')))
        elif y_delta < 0 and x_delta > 0:
            avail_action = list(set(avail_action).intersection(('0', '7', '8')))
        elif y_delta > 0 and x_delta > 0:
            avail_action = list(set(avail_action).intersection(('0', '1',)))
        elif y_delta < 0 and x_delta == 0:
            avail_action = list(set(avail_action).intersection(('0', '6',)))
        elif y_delta > 0 and x_delta == 0:
            avail_action = list(set(avail_action).intersection(('0', '2',)))
        elif y_delta == 0 and x_delta < 0:
            avail_action = list(set(avail_action).intersection(('0', '4',)))
        elif y_delta == 0 and x_delta > 0:
            avail_action = list(set(avail_action).intersection(('0', '8',)))
        elif y_delta == 0 and x_delta == 0:
            avail_action = ['0']
        return avail_action

    def _action_mask(self, action_dict, ret_hl):
        for op_group_name, last_area_coord_points in self.operation_groups_last_area.items():
            agent_id = OPERATION_GROUPS_TO_LL_AGENTS[op_group_name]
            ml_agent_id = ML_AGENTS_TO_LL_AGENTS.inverse[agent_id]
            _, ml_avail_action = get_sudoku(EXTERNAL_BOUNDARY, last_area_coord_points)
            hl_action = action_dict[agent_id][-1]
            ml_avail_action = self._mid_level_mask(last_area_coord_points, hl_action, ml_avail_action)

            # 中层智能体的mask
            ml_action_mask = [0 for _ in range(MID_LEVEL_ACT_SPACE)]
            ml_action_embed = np.zeros([MID_LEVEL_ACT_SPACE, MID_LEVEL_ACTION_EMBED])
            ml_action_embed[0] = self.mid_level_action_embed[ml_agent_id][0]
            for aac in ml_avail_action:
                ml_action_mask[int(aac)] = 1
                ml_action_embed[int(aac)] = self.mid_level_action_embed[ml_agent_id][int(aac)]
            self.mid_level_avail_action_action_mask[ml_agent_id]["action_mask"] = ml_action_mask
            self.mid_level_avail_action_action_mask[ml_agent_id]["avail_actions"] = ml_action_embed

        temp_avail_action = []
        max_chain_index = 0
        for hl_agent_id in HIGH_LEVEL_AGENT_IDs:
            for ml_agent_id in HL_AGENTS_TO_ML_AGENTS[hl_agent_id]:
                ll_agent_id = ML_AGENTS_TO_LL_AGENTS[ml_agent_id]
                hl_action = action_dict[ll_agent_id][-1]
                group_name = LL_AGENTS_TO_OPERATION_GROUPS[ll_agent_id]
                last_area_coord_points = self.operation_groups_last_area[group_name]
                chain_index, hl_avail_action = self._high_level_mask(last_area_coord_points, hl_action, ret_hl)
                if chain_index > max_chain_index:
                    max_chain_index = chain_index
                    temp_avail_action = hl_avail_action
        for hl_agent_id in HIGH_LEVEL_AGENT_IDs:
            # 上层智能体的mask
            hl_action_mask = [0 for _ in range(HIGH_LEVEL_ACT_SPACE)]
            hl_action_embed = np.zeros([HIGH_LEVEL_ACT_SPACE, HIGH_LEVEL_ACTION_EMBED])
            # hl_action_embed[0] = self.high_level_action_embed[hl_agent_id][0]
            for aac in temp_avail_action:
                hl_action_mask[int(aac)] = 1
                hl_action_embed[int(aac)] = self.high_level_action_embed[hl_agent_id][int(aac)]
            self.high_level_avail_action_action_mask[hl_agent_id]["action_mask"] = hl_action_mask
            self.high_level_avail_action_action_mask[hl_agent_id]["avail_actions"] = hl_action_embed

    def update_ewr_location(self):
        duration_time = self.m_Time - self.m_StartTime

        # EWR_PATROL_AREA = [(2, 3), (4, 4), (6, 7), (9, 10), (11, 12)]
        if self.ewr_last_point:
            point_index = None
            for index, p in enumerate(EWR_PATROL_AREA):
                if self.ewr_last_point == p:
                    point_index = index
            assert point_index is not None
            current_point_detect_status = self.detect_point_distance(self.ewr_last_point, EWR_DETECT_DISTANCE)
            ewr_unit = [v for k, v in self.rule_operation_units.items() if v.m_Type == 4002]
            if not ewr_unit:
                return
            # 向后退
            if current_point_detect_status:
                if point_index == 0:
                    # 返航
                    assert ewr_unit is not []
                    ewr_unit[0].return_to_base()
                else:
                    self.ewr_last_point = EWR_PATROL_AREA[point_index - 1]
                    self.set_ewr_location(self.ewr_last_point, status_code="update")
            # 前进
            else:
                if duration_time / 60.0 > MODEL_START_TIME:
                    if point_index == 4:
                        pass
                    else:
                        next_point_detect_status = self.detect_point_distance(EWR_PATROL_AREA[point_index + 1],
                                                                              EWR_DETECT_DISTANCE)
                        if next_point_detect_status:
                            pass
                        else:
                            self.ewr_last_point = EWR_PATROL_AREA[point_index + 1]
                            self.set_ewr_location(self.ewr_last_point, status_code="update")

    def set_ewr_location(self, point, status_code=None):
        """
        :param point: (2, 3)
        :param status_code: "init", "update"
        :return:
        """

        assert point is not None
        ewr_unit = {k: v for k, v in self.rule_operation_units.items() if v.m_Type == 4002}
        assert ewr_unit is not {}
        if status_code is "init":
            self.unit_out_to_next_point(list(ewr_unit.keys())[0], list(ewr_unit.values())[0].strName, point)
            self.ewr_last_point = point
        elif status_code is "update":
            lat, lon = \
                convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2, point)
            self.control_operation_group_next_point(list(ewr_unit.values())[0].strName, lat, lon)
            self.ewr_last_point = point

    def rule_bot(self):
        # 还原数据结构
        for _, v in RULE_OPERATION_UNITS_TASK_STATUS.items():
            v['first_stage']['status'] = False
            v['second_stage']['status'] = False
        # 创建预警任务
        self.set_ewr_location(EWR_PATROL_AREA[2], status_code="init")

        # 第一阶段单机出动
        for k, v in self.rule_operation_units.items():
            if v.strName in [TOP_RULE_UNITS_NAME[0], BOT_RULE_UNITS_NAME[0]]:
                RULE_OPERATION_UNITS_TASK_STATUS[v.strName]['first_stage']['status'] = True
                self.unit_out_to_next_point(k, v.strName,
                                            RULE_OPERATION_UNITS_TASK_STATUS[v.strName]['first_stage']['point'])

        scout_units_name = TOP_RULE_UNITS_NAME + BOT_RULE_UNITS_NAME
        first_wave_scout_units_name = [TOP_RULE_UNITS_NAME[0], BOT_RULE_UNITS_NAME[0]]
        second_wave_scout_units_name = [TOP_RULE_UNITS_NAME[1], BOT_RULE_UNITS_NAME[1]]
        scout_rule_unit_survival_status = {scout_units_name[i]: True for i in range(len(scout_units_name))}
        while True:
            self.scenario = self.env.step()  # 墨子环境step
            self._update(self.scenario)
            rule_operation_units_name_to_guid = {v.strName: k for k, v in self.rule_operation_units.items()}
            duration_time = self.m_Time - self.m_StartTime
            # 更新判断执行侦察任务的单元存活状态
            for name in scout_units_name:
                if name not in rule_operation_units_name_to_guid:
                    scout_rule_unit_survival_status[name] = False

            if duration_time / 60.0 >= MODEL_START_TIME:
                # 侦察任务结束，剩余的侦察任务飞机向前突进
                for scout_rule_unit_name, survival_status in scout_rule_unit_survival_status.items():
                    if survival_status:
                        guid = rule_operation_units_name_to_guid[scout_rule_unit_name]
                        if self.rule_operation_units[guid].strAirOpsConditionString == 1:  # 飞机处于停泊状态
                            self.unit_out_to_next_point(guid, scout_rule_unit_name, SCOUT_POINT_LIST[4])
                        else:
                            lat, lon = \
                                convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2, SCOUT_POINT_LIST[4])
                            self.control_operation_group_next_point(scout_rule_unit_name, lat, lon)
                break

            # 更新判断四个侦察点附近是否存在敌方单元
            detect_status = {SCOUT_POINT_LIST[i]: self.detect_point_distance(SCOUT_POINT_LIST[i], SCOUT_DETECT_DISTANCE)
                             for i in range(len(SCOUT_POINT_LIST))}
            # 更新判断执行侦察任务的单元存活状态
            for name in scout_units_name:
                if name not in rule_operation_units_name_to_guid:
                    scout_rule_unit_survival_status[name] = False

            for scout_rule_unit_name, survival_status in scout_rule_unit_survival_status.items():
                if survival_status:
                    # 是否需要规避进攻
                    self.avoid_attack(rule_operation_units_name_to_guid[scout_rule_unit_name], scout_rule_unit_name)

                    # 第一波侦察单元(第一阶段任务已启动)
                    if scout_rule_unit_name in first_wave_scout_units_name:
                        # 如果第二阶段任务已启动
                        if RULE_OPERATION_UNITS_TASK_STATUS[scout_rule_unit_name]['second_stage']['status']:
                            pass
                        # 如果第二阶段任务未启动，择时启动第二阶段任务
                        else:
                            # 启动时间超过30分钟
                            if duration_time / 60.0 >= FIRST_STAGE_DURATION_TIME:
                                # 两阶段侦察任务点附近是否存在敌方单元
                                fs_detect_status = \
                                    detect_status[
                                        RULE_OPERATION_UNITS_TASK_STATUS[scout_rule_unit_name]['first_stage']['point']]
                                ss_detect_status = \
                                    detect_status[
                                        RULE_OPERATION_UNITS_TASK_STATUS[scout_rule_unit_name]['second_stage']['point']]

                                # 两阶段侦察任务点附近都不存在敌方单元，启动第二阶段任务
                                if not fs_detect_status and not ss_detect_status:
                                    lat, lon = \
                                        convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2,
                                                                      RULE_OPERATION_UNITS_TASK_STATUS[
                                                                          scout_rule_unit_name]['second_stage'][
                                                                          'point'])
                                    RULE_OPERATION_UNITS_TASK_STATUS[
                                        scout_rule_unit_name]['second_stage']['status'] = True
                                    self.control_operation_group_next_point(scout_rule_unit_name, lat, lon)
                    # 第二波侦察单元
                    elif scout_rule_unit_name in second_wave_scout_units_name:
                        # 是否第一阶段任务已启动
                        if RULE_OPERATION_UNITS_TASK_STATUS[scout_rule_unit_name]['first_stage']['status']:
                            # 如果第二阶段任务已启动
                            if RULE_OPERATION_UNITS_TASK_STATUS[scout_rule_unit_name]['second_stage']['status']:
                                pass
                            # 如果第二阶段任务未启动，择时启动第二阶段任务
                            else:
                                # 启动时间超过90分钟
                                if duration_time / 60.0 >= FIRST_STAGE_DURATION_TIME * 3:
                                    # 两阶段侦察任务点附近是否存在敌方单元
                                    fs_detect_status = \
                                        detect_status[
                                            RULE_OPERATION_UNITS_TASK_STATUS[scout_rule_unit_name]['first_stage'][
                                                'point']]
                                    ss_detect_status = \
                                        detect_status[
                                            RULE_OPERATION_UNITS_TASK_STATUS[scout_rule_unit_name]['second_stage'][
                                                'point']]

                                    # 两阶段侦察任务点附近都不存在敌方单元，启动第二阶段任务
                                    if not fs_detect_status and not ss_detect_status:
                                        lat, lon = \
                                            convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2,
                                                                          RULE_OPERATION_UNITS_TASK_STATUS[
                                                                              scout_rule_unit_name]['second_stage'][
                                                                              'point'])
                                        RULE_OPERATION_UNITS_TASK_STATUS[
                                            scout_rule_unit_name]['second_stage']['status'] = True
                                        self.control_operation_group_next_point(scout_rule_unit_name, lat, lon)
                        # 第一阶段任务未启动
                        else:
                            # 判断单元是哪路任务单元
                            if scout_rule_unit_name in TOP_RULE_UNITS_NAME:
                                # 第一波单元未存活，立即启动第二波侦察单元
                                guid = rule_operation_units_name_to_guid[scout_rule_unit_name]
                                if not scout_rule_unit_survival_status[TOP_RULE_UNITS_NAME[0]]:
                                    RULE_OPERATION_UNITS_TASK_STATUS[
                                        scout_rule_unit_name]['first_stage']['status'] = True
                                    self.unit_out_to_next_point(guid, scout_rule_unit_name,
                                                                RULE_OPERATION_UNITS_TASK_STATUS[
                                                                    scout_rule_unit_name]['first_stage']['point'])
                                else:
                                    guid_2 = rule_operation_units_name_to_guid[TOP_RULE_UNITS_NAME[0]]
                                    if self.rule_operation_units[guid_2].strAirOpsConditionString in [7,
                                                                                                      11]:  # 飞机处于返航状态
                                        RULE_OPERATION_UNITS_TASK_STATUS[
                                            scout_rule_unit_name]['first_stage']['status'] = True
                                        self.unit_out_to_next_point(guid, scout_rule_unit_name,
                                                                    RULE_OPERATION_UNITS_TASK_STATUS[
                                                                        scout_rule_unit_name]['first_stage']['point'])
                            elif scout_rule_unit_name in BOT_RULE_UNITS_NAME:
                                # 第一波单元未存活，立即启动第二波侦察单元
                                guid = rule_operation_units_name_to_guid[scout_rule_unit_name]
                                if not scout_rule_unit_survival_status[BOT_RULE_UNITS_NAME[0]]:
                                    RULE_OPERATION_UNITS_TASK_STATUS[
                                        scout_rule_unit_name]['first_stage']['status'] = True
                                    self.unit_out_to_next_point(guid, scout_rule_unit_name,
                                                                RULE_OPERATION_UNITS_TASK_STATUS[
                                                                    scout_rule_unit_name]['first_stage']['point'])
                                else:
                                    guid_2 = rule_operation_units_name_to_guid[BOT_RULE_UNITS_NAME[0]]
                                    if self.rule_operation_units[guid_2].strAirOpsConditionString in [7,
                                                                                                      11]:  # 飞机处于返航状态
                                        RULE_OPERATION_UNITS_TASK_STATUS[
                                            scout_rule_unit_name]['first_stage']['status'] = True
                                        self.unit_out_to_next_point(guid, scout_rule_unit_name,
                                                                    RULE_OPERATION_UNITS_TASK_STATUS[
                                                                        scout_rule_unit_name]['first_stage']['point'])
                            else:
                                raise ValueError
                    else:
                        raise ValueError
                else:
                    pass

    def unit_out_to_next_point(self, guid, scout_rule_unit_name, point):
        cmd = "Hs_ScenEdit_AirOpsSingleOut({" + f"\'{guid}\'" + "})"
        self.scenario.mozi_server.send_and_recv(cmd)

        lat, lon = \
            convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2, point)
        self.control_operation_group_next_point(scout_rule_unit_name, lat, lon)

    def avoid_attack(self, unit_guid, unit_name):
        # guid = rule_operation_units_name_to_guid[unit_name]
        unit = self.rule_operation_units[unit_guid]
        detect_status = self.compute_point_distance(unit.dLongitude, unit.dLatitude, AVOID_ATTACK_DISTANCE)
        # 附近30公里存在敌方单元，启动规避
        if detect_status:
            for _ in range(EVADE_NUMS):
                altitude, speed, heading = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
                self.control_operation_unit(unit_name, altitude * 20000, speed * 1000, heading * 360)

    def all_unit_avoid_attack(self):
        t = []
        ewr = {k: v for k, v in self.rule_operation_units.items() if v.m_Type == 4002}
        ou = {**self.agent_operation_units, **ewr}

        for _, unit_class in ou.items():
            detect_status = self.compute_point_distance(unit_class.dLongitude,
                                                        unit_class.dLatitude, AVOID_ATTACK_DISTANCE)
            if detect_status:
                t.append(unit_class.strName)
        if t:
            for _ in range(EVADE_NUMS):
                for name in t:
                    # 附近30公里存在敌方单元，启动规避
                    altitude, speed, heading = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
                    self.control_operation_unit(name, altitude * 20000, speed * 1000, heading * 360)

    def compute_point_distance(self, lon, lat, distance):
        """
        功能：判断探测的单元与某个点的距离是否超过特定distance
        point:tuple,某个点的经纬度
        distance：距离，km
        contact：探测到的单元字典
        """
        for v in self.side.contacts.values():
            dis = get_two_point_distance(lon, lat, v.dLongitude, v.dLatitude)
            if dis < distance * 1000:
                return True
        return False

    def control_operation_unit(self, unit_name, altitude, speed, heading):
        """
            设置作战编队高度、速度、航向
            :param unit_name: 作战单元名称
            :param altitude:（米） 作战编队高度（100，20000）
            :param speed:（海里） 作战编队速度（0, 1000） speed单位是海里，转化为公里为speed*1.852
                            speed = 1000海里/小时（1852公里/小时）
                            低速度：350海里/小时（648.2公里/小时）
                            巡航速度：480海里/小时（888.96公里/小时）
                            军用速度：520海里/小时（963.04公里/小时）
                            加力速度：920海里/小时（1703.84公里/小时）
            :param heading: 作战编队航向（0，360）
            :return:
            """

        cmd = "ScenEdit_SetUnit({Unitname=" + f"\'{unit_name}\'," + f"Altitude={altitude}," \
              + f"Speed={speed}," + f"Heading={heading}" + "})"
        self.scenario.mozi_server.send_and_recv(cmd)

    def detect_point_distance(self, point, distance):
        """
        功能：判断探测的单元与某个点的距离是否超过特定distance
        point:tuple,某个点的经纬度
        distance：距离，km
        contact：探测到的单元字典
        """
        lat, lon = \
            convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2, point)
        for v in self.side.contacts.values():
            if FIGHTER_NAME not in v.strName:
                continue
            dis = get_two_point_distance(lon, lat, v.dLongitude, v.dLatitude)
            if dis < distance * 1000:
                return True
        return False

    def return_to_base(self):
        # 如果歼轰飞机全部返航，那么其余飞机应返航
        a2s_status = []
        for name, status in self.operation_groups_status.items():
            if 'A2S' in name:
                a2s_status.append(status)
        if all(a2s_status):
            for _, unit_class in self.agent_operation_units.items():
                unit_class.return_to_base()
            for _, unit_class in self.rule_operation_units.items():
                unit_class.return_to_base()

    def _set_side_doctrine(self):
        """
        设置推演方条令
        """
        doctrine = self.side.get_doctrine()

        # 设置武器控制状态
        # domain: {str: 'weapon_control_status_subsurface' - 对潜,
        #               'weapon_control_status_surface' - 对面,
        #               'weapon_control_status_land' - 对陆,
        #               'weapon_control_status_air' - 对空}
        # fire_status: {str: '0' - 自由开火, '1' - 谨慎开火, '2' - 限制开火}
        # 对空自由开火
        # doctrine.set_weapon_control_status(domain='weapon_control_status_air', fire_status='0')
        # 对面自由开火
        doctrine.set_weapon_control_status(domain='weapon_control_status_surface', fire_status='0')
        # 电磁管控
        # em_item: {str: 'Radar' - 雷达, 'Sonar' - 声呐, 'OECM' - 光电对抗}
        # status: {str: 'Passive' - 仅有被动设备工作, 'Active' - 另有主动设备工作
        doctrine.set_em_control_status(em_item='Radar', status='Active')
        doctrine.set_em_control_status(em_item='OECM', status='Active')
        # 设置是否自动规避
        doctrine.evade_automatically('true')
        # 设置是否进攻时忽略计划航线
        doctrine.ignore_plotted_course('yes')

        # 设置飞行编队返航的油料状态
        # fuel_state: {str:   'No'('0') - 无约束，编队不返航,
        #                     'YesLastUnit'('1') - 编队中所有飞机均因达到单机油料状态要返航时，编队才返航,
        #                     'YesFirstUnit'('2') - 编队中任意一架飞机达到单机油料状态要返航时，编队就返航,
        #                     'YesLeaveGroup'('3') - 编队中任意一架飞机达到单机油料状态要返航时，其可离队返航}
        doctrine.set_fuel_state_for_air_group('3')
        # 设置飞行编队的武器状态
        # weapon_state: {str: 'No'('0') - 无约束，编队不返航,
        #                     'YesLastUnit'('1') - 编队中所有飞机均因达到单机武器状态要返航时，编队才返航,
        #                     'YesFirstUnit'('2') - 编队中任意一架飞机达到单机武器状态要返航时，编队就返航,
        #                     'YesLeaveGroup'('3') - 编队中任意一架飞机达到单机武器状态要返航时，其可离队返航}
        doctrine.set_weapon_state_for_air_group('3')

        # 设置武器使用规则 AIM-120C-7 目标：直升机-未指明
        doctrine.set_weapon_release_authority(weapon_dbid='718', target_type='2100',
                                              quantity_salvo=1, shooter_salvo='max',
                                              firing_range=35, self_defense='max', escort='')
        # 设置武器使用规则 AGM-84L 目标：水面目标-未知类型
        doctrine.set_weapon_release_authority(weapon_dbid='816', target_type='2999',
                                              quantity_salvo=12, shooter_salvo='max',
                                              firing_range='max', self_defense='max', escort='')
        # 设置武器使用规则 AGM-84L 目标：水面舰艇-未指明
        doctrine.set_weapon_release_authority(weapon_dbid='816', target_type='3000',
                                              quantity_salvo=12, shooter_salvo='max',
                                              firing_range='max', self_defense='max', escort='')

    @staticmethod
    def modify_unit_doctrine(unit_class, radar_status, fire_status=False):
        """

        :param unit_class:
        :param radar_status: 'Passive' - 仅有被动设备工作, 'Active' - 另有主动设备工作
        :param fire_status：bool
        :return:
        """
        doctrine = unit_class.get_doctrine()
        # 对空自由开火
        if fire_status:
            doctrine.set_weapon_control_status(domain='weapon_control_status_air', fire_status='0')
        doctrine.set_em_control_status(em_item='Radar', status=radar_status)
        doctrine.set_em_control_status(em_item='OECM', status='Active')

    # 《《《《《《《《《《《《《 rule_bot 》》》》》》》》》》》》》》

    # 《《《《《《《《《《《《《 状态空间 》》》》》》》》》》》》》》

    def _generate_dones_rets_masks_infos(self, action):
        ret_ml = {"__all__": False}
        ret_hl = {hl_agent_id: False for hl_agent_id in HIGH_LEVEL_AGENT_IDs}
        ret_hl["__all__"] = False
        if self.dwell_time["start_time"]:
            now_time = datetime.now()
            delta = now_time - self.dwell_time["start_time"]
            delta = str(delta).split(':')
            delta = float(delta[1]) * 60 + float(delta[2])
            if delta >= self.dwell_time["dwell_time"]:
                ret_ml["__all__"] = True
                self.dwell_time["start_time"] = None
                self.dwell_time["dwell_time"] = None

        dones = {"__all__": self._is_done()}
        if dones["__all__"]:
            ret_ml["__all__"] = True
            ret_hl["__all__"] = True

        if ret_ml["__all__"]:
            self._action_mask(action, ret_hl)

        infos = {}
        for operation_group_name, agent_id in OPERATION_GROUPS_TO_LL_AGENTS.items():
            infos[agent_id] = {}
            ret_ml[agent_id] = False
            if dones["__all__"]:
                dones[agent_id] = True
            else:
                dones[agent_id] = False
        return dones, ret_ml, ret_hl, infos

    def _generate_global_features(self):
        feats = []

        if all(self.operation_groups_status.values()):
            feats = [0.0 for _ in range(STATE_SPACE)]
            return feats

        contacts = {k: v for k, v in self.side.contacts.items()}
        # s_contacts = sorted(contacts.items(), key=lambda value: value[1].dLongitude)
        h_feats = [0.0 for _ in range(7)]
        div = 0.0
        for k, v in contacts.items():
            div += 1.0
            temp_feats = [0.0 for _ in range(7)]
            if v.m_ContactType:
                temp_feats[0] = v.m_ContactType / 22.0
            if v.m_IdentificationStatus:
                temp_feats[1] = v.m_IdentificationStatus / 4.0
            if v.fCurrentHeading:
                temp_feats[2] = v.fCurrentHeading / 180.0
            if v.fCurrentSpeed:
                temp_feats[3] = v.fCurrentSpeed / 1000.0
            if v.dLongitude and v.dLatitude:
                temp_feats[4] = v.dLongitude / 180.0
                temp_feats[5] = v.dLatitude / 180.0
            h_feats = map(lambda x, y: x + y, h_feats, temp_feats)
        if div == 0.0:
            feats.extend(h_feats)
        else:
            h_feats = [i / div for i in h_feats]
            h_feats[-1] = div
            feats.extend(h_feats)

        # aircraft = sorted(self.side.aircrafts.items(), key=lambda value: value[1].dLongitude)
        air_feats = [0.0 for _ in range(9)]
        div = 0.0
        for k, v in self.side.aircrafts.items():
            div += 1.0
            temp_air_feats = [0.0 for _ in range(9)]
            if v.iFireIntensityLevel:
                temp_air_feats[0] = v.iFireIntensityLevel / 4.0
            if v.iFloodingIntensityLevel:
                temp_air_feats[1] = v.iFloodingIntensityLevel / 4.0
            if v.strAirOpsConditionString:
                temp_air_feats[2] = v.strAirOpsConditionString / 26.0
            if v.dLongitude and v.dLatitude:
                temp_air_feats[3] = v.dLongitude / 180.0
                temp_air_feats[4] = v.dLatitude / 180.0

            weapon_list = self._get_unit_weapon(v)
            # 诱饵弹 2051-通用红外干扰弹；564-通用箔条；
            temp_air_feats[5] = self._get_weapon_num(weapon_list, [564, 2051]) / 10.0
            # 空空导弹  718-AIM-120C;1129-AIM-2000A
            temp_air_feats[6] = self._get_weapon_num(weapon_list, [718, 1129]) / 10.0
            # 反舰导弹  816-AGM-84L
            temp_air_feats[7] = self._get_weapon_num(weapon_list, [816]) / 10.0

            air_feats = map(lambda x, y: x + y, air_feats, temp_air_feats)

        if div == 0.0:
            feats.extend(air_feats)
        else:
            air_feats = [i / div for i in air_feats]
            air_feats[-1] = div
            feats.extend(air_feats)

        time_delta = self.m_Time - self.m_StartTime
        feats.append(time_delta / 3600.0)
        feats.append(time_delta / 7200.0)
        feats.append(time_delta / 14400.0)

        return feats

    def _generate_local_features(self):
        """
        :return:
        """
        low_level_multi_agent_obs = {}
        for operation_group_name, agent_id in OPERATION_GROUPS_TO_LL_AGENTS.items():
            agent_obs = {}
            obs = self._generate_operation_group_features(operation_group_name)
            agent_obs[SampleBatch.OBS] = obs  # np.array(obs)
            low_level_multi_agent_obs[agent_id] = agent_obs
        return low_level_multi_agent_obs

    def _update_operation_groups(self):
        temp_operation_groups = {}
        for group_name in self.operation_groups:
            temp_operation_groups[group_name] = {}
        for unit_guid, unit_class in self.agent_operation_units.items():
            for group_name, units in self.operation_groups.items():
                if unit_guid in units:
                    temp_operation_groups[group_name][unit_guid] = unit_class
        self.operation_groups = temp_operation_groups

    def _generate_operation_group_features(self, operation_group_name):
        in_group_units = self.operation_groups[operation_group_name]

        feats = []
        if self.operation_groups_status[operation_group_name]:
            feats = [0.0 for _ in range(LOW_LEVEL_OBS_SPACE - 2)]
            return feats

        # TODO 找出与作战编组单元距离200公里内的敌方单元
        local_contacts = {}
        contacts = {k: v for k, v in self.side.contacts.items()}
        for unit_guid, unit_value in in_group_units.items():
            for contact_guid, contact_value in contacts.items():
                dis = get_two_point_distance(unit_value.dLongitude, unit_value.dLatitude,
                                             contact_value.dLongitude, contact_value.dLatitude)
                if dis <= ENEMY_DISTANCE * 1000:
                    local_contacts[contact_guid] = contact_value

        h_feats = [0.0 for _ in range(7)]
        div = 0.0
        for k, v in local_contacts.items():
            div += 1.0
            temp_feats = [0.0 for _ in range(7)]
            if v.m_ContactType:
                temp_feats[0] = v.m_ContactType / 22.0
            if v.m_IdentificationStatus:
                temp_feats[1] = v.m_IdentificationStatus / 4.0
            if v.fCurrentHeading:
                temp_feats[2] = v.fCurrentHeading / 180.0
            if v.fCurrentSpeed:
                temp_feats[3] = v.fCurrentSpeed / 1000.0
            if v.dLongitude and v.dLatitude:
                temp_feats[4] = v.dLongitude / 180.0
                temp_feats[5] = v.dLatitude / 180.0
            h_feats = map(lambda x, y: x + y, h_feats, temp_feats)
        if div == 0.0:
            feats.extend(h_feats)
        else:
            h_feats = [i / div for i in h_feats]
            h_feats[-1] = div
            feats.extend(h_feats)

        # TODO 找出与作战编组单元距离80公里内的我方单元
        local_units = {}
        for unit_guid, unit_value in in_group_units.items():
            for local_unit_guid, local_unit_value in self.agent_operation_units.items():
                dis = get_two_point_distance(unit_value.dLongitude, unit_value.dLatitude,
                                             local_unit_value.dLongitude, local_unit_value.dLatitude)
                if dis <= UNITS_DISTANCE * 1000:
                    local_units[local_unit_guid] = local_unit_value

        air_feats = [0.0 for _ in range(9)]
        div = 0.0
        for k, v in local_units.items():
            div += 1.0
            temp_air_feats = [0.0 for _ in range(9)]
            if v.iFireIntensityLevel:
                temp_air_feats[0] = v.iFireIntensityLevel / 4.0
            if v.iFloodingIntensityLevel:
                temp_air_feats[1] = v.iFloodingIntensityLevel / 4.0
            if v.strAirOpsConditionString:
                temp_air_feats[2] = v.strAirOpsConditionString / 26.0
            if v.dLongitude and v.dLatitude:
                temp_air_feats[3] = v.dLongitude / 180.0
                temp_air_feats[4] = v.dLatitude / 180.0

            weapon_list = self._get_unit_weapon(v)
            # 诱饵弹 2051-通用红外干扰弹；564-通用箔条；
            temp_air_feats[5] = self._get_weapon_num(weapon_list, [564, 2051]) / 10.0
            # 空空导弹  718-AIM-120C;1129-AIM-2000A
            temp_air_feats[6] = self._get_weapon_num(weapon_list, [718, 1129]) / 10.0
            # 反舰导弹  816-AGM-84L
            temp_air_feats[7] = self._get_weapon_num(weapon_list, [816]) / 10.0

            air_feats = map(lambda x, y: x + y, air_feats, temp_air_feats)

        if div == 0.0:
            feats.extend(air_feats)
        else:
            air_feats = [i / div for i in air_feats]
            air_feats[-1] = div
            feats.extend(air_feats)

        time_delta = self.m_Time - self.m_StartTime
        feats.append(time_delta / 3600.0)
        feats.append(time_delta / 7200.0)
        feats.append(time_delta / 14400.0)

        return feats

    @staticmethod
    def _get_contact_area(contact_unit):
        """
        :param contact_unit: ship
        :return:
        """
        if contact_unit.m_UncertaintyArea:
            uncertainty_area = list(map(lambda x: x.split('$'), contact_unit.m_UncertaintyArea.split('$0@')))
            ua = []
            for lon_lat in uncertainty_area:
                if lon_lat.__len__() < 2:
                    raise ValueError
                else:
                    ua.append([float(lon_lat[0]), float(lon_lat[1])])
            return ua
        else:
            return [[contact_unit.dLongitude, contact_unit.dLatitude]]

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
    def _get_weapon_info(weapon_list, weapon_name):
        for weapon in weapon_list:
            if weapon_name in weapon[1]:
                return True
        return False

    @staticmethod
    def _get_weapon_num(weapon_list, weapon_type):
        num = 0
        for weapon in weapon_list:
            if weapon[0] != '' and weapon[-1] != '':
                if int(re.sub('\D', '', weapon[-1])) in weapon_type:
                    num += int(weapon[0])
        return num

    # 《《《《《《《《《《《《《 状态空间 》》》》》》》》》》》》》》

    # 《《《《《《《《《《《《《 环境 》》》》》》》》》》》》》》

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
                self.scenario = self.env.reset()
                print('结束mozi reset!!!')
            else:
                print('开始mozi reset!!!')
                self.scenario = self.env.reset()
                print('结束mozi reset!!!')
        else:
            self.scenario = self.env.reset()

    def _is_done(self):
        """
        数值：0, 空中
            1, 停泊
            2, 正在滑行准备起飞
            3, 正在滑行到停机位
            4, 正在起飞过程中
            5, 最终进场
            6, 正在完成降落
            7, 正在进行出动准备
            8, 等待可用的滑行道/升降机
            9, 等待跑道空闲
            10, 处于降落队列中
            11, 返回基地
            12, 准备出动
            13, 机动到加油阵位
            14, 正在加油
            15, 卸载燃油
            16, 准备部署吊放式声纳，尚未到达部署点
            17, 紧急着陆
            18, 到飞行甲板
            19,正在执行超视距攻击任务
            20, 超视距攻击往复运动？远距离攻击往复运动？
            21, 近距空中格斗
            22, 投送货物
            23,滑行至加油区
            24,滑行
            25,通过跑道滑行降落（用于演示功能）
            26,通过跑道滑行起飞（用于演示功能）
        :return:
        """
        # 对战平台
        response_dic = self.scenario.get_responses()
        for _, v in response_dic.items():
            if v.Type == 'EndOfDeduction':
                print('打印出标记：EndOfDeduction')
                return True

        # TODO 增加如果3.5小时后空中没有作战单元，则返回true
        duration_time = self.m_Time - self.m_StartTime

        if duration_time / 3600.0 >= 4.0:
            status = []
            for u, v in self.agent_operation_units.items():
                if v.strAirOpsConditionString == 7:  # [1, 5, 6, 7, 10, 11]
                    status.append(True)
                else:
                    status.append(False)
            if status:
                return all(status)
            else:
                pass
        return False

    # 《《《《《《《《《《《《《 环境 》》》》》》》》》》》》》》

    # 《《《《《《《《《《《《《 奖励机制 》》》》》》》》》》》》》》

    def _detect_point_fighter_nums(self, point):
        """
        功能：判断探测的单元与某个点的距离是否超过特定distance
        point:tuple,某个点的经纬度
        distance：距离，km
        contact：探测到的单元字典
        """
        lat, lon = \
            convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2, point)
        contacts = {k: v
                    for k, v in self.side.contacts.items()
                    if int(v.m_ContactType) == 1 and FIGHTER_NAME in v.strName}
        fighter_nums = 0
        risk_status = False
        if not contacts:
            return risk_status, fighter_nums
        for v in contacts.values():
            dis = get_two_point_distance(lon, lat, v.dLongitude, v.dLatitude)
            if dis <= POINT_RISK_DISTANCE * 1000:
                fighter_nums += 1
        if fighter_nums:
            risk_status = True
        return risk_status, fighter_nums

    def _detect_fighter_nums(self, operation_group_name):
        """
        获取距离作战单元编队某一范围的敌方空战飞机的数量
        m_IdentificationStatus: 0--未知
                                1--已知空域（如空中、地面）
                                2--已知类型（如飞机、导弹）
                                3--已知级别
                                4--确认对象
        m_ContactType: 0--空中目标
                       1--导弹
                       2--水面/地面
                       ...
        :return:
        """
        in_group_units = self.operation_groups[operation_group_name]
        contacts = {k: v
                    for k, v in self.side.contacts.items()
                    if int(v.m_ContactType) == 0 and FIGHTER_NAME in v.strName}
        fighter_nums = 0
        risk_status = False
        if not contacts or not in_group_units:
            return risk_status, fighter_nums
        for unit_guid, unit_value in in_group_units.items():
            for contact_guid, contact_value in contacts.items():
                dis = get_two_point_distance(unit_value.dLongitude, unit_value.dLatitude,
                                             contact_value.dLongitude, contact_value.dLatitude)
                if dis <= RISK_DISTANCE * 1000:
                    fighter_nums += 1
        if fighter_nums:
            risk_status = True
        return risk_status, fighter_nums

    def _update_operation_groups_status(self):
        """
        判断作战编队（成员）的返航状态，是否被击毁
        strAirOpsConditionString  11-返回基地
        :return:
        """
        for group_name, units in self.operation_groups.items():
            if units:
                if self.operation_groups_status[group_name]:
                    continue
                temp_status = []
                for unit_guid, unit_class in units.items():
                    if int(unit_class.strAirOpsConditionString) is 11:
                        temp_status.append(True)
                    else:
                        temp_status.append(False)
                self.operation_groups_status[group_name] = all(temp_status)
            else:
                self.operation_groups_status[group_name] = True

    def update_hl_agent_reward(self, action_dict, is_done):
        anchor_attack_point_index = None
        reward_bound = 100.0
        for hl_agent_id in HIGH_LEVEL_AGENT_IDs:
            if is_done:
                self.hl_reward[hl_agent_id] += self._get_win_score()/SCORE_BOUND
            attack_point_list = []
            if hl_agent_id == 'hl_agent_0':
                for ml_agent_id in HL_AGENTS_TO_ML_AGENTS[hl_agent_id]:
                    ll_agent_id = ML_AGENTS_TO_LL_AGENTS[ml_agent_id]
                    group_name = LL_AGENTS_TO_OPERATION_GROUPS[ll_agent_id]
                    # 作战编队返航、编组内单元全部被击毁，不做任何处理
                    if self.operation_groups_status[group_name]:
                        continue
                    _, _, _, attack_point_index = action_dict[ll_agent_id]
                    attack_point_list.append(attack_point_index)
                # 如果在中途智能体编队0的作战编队全部被击毁，指定默认编队配合打击点。
                if not attack_point_list:
                    # for k, v in self.hl_last_attack_points.items():
                    anchor_attack_point_index = 24
                    continue
                if len(set(attack_point_list)) > 1:
                    raise ValueError("同一个智能体编队的打击点不同！！！")
                anchor_attack_point_index = attack_point_list[0]
                self.hl_last_attack_points[hl_agent_id] = anchor_attack_point_index
                # 在没有到达最后一道打击点之前应该远离风险区域
                # 获取打击点附近100公里的对方单元
                chain_index = int(anchor_attack_point_index / ATTACK_CHAIN_POINT_NUMS)
                # lower_index = chain_index * ATTACK_CHAIN_POINT_NUMS if chain_index > 0 else 0
                # upper_index = (chain_index + 1) * ATTACK_CHAIN_POINT_NUMS
                # simple_chain_points = ATTACK_POINTS[lower_index:upper_index]
                if 0 < chain_index < ATTACK_CHAINS - 1:
                    attack_point = ATTACK_POINTS[anchor_attack_point_index]
                    _, fighter_nums = self._detect_point_fighter_nums(attack_point)
                    self.hl_reward[hl_agent_id] -= fighter_nums / reward_bound
                    continue
                elif chain_index == ATTACK_CHAINS - 1:
                    pass

            for ml_agent_id in HL_AGENTS_TO_ML_AGENTS[hl_agent_id]:
                ll_agent_id = ML_AGENTS_TO_LL_AGENTS[ml_agent_id]
                _, _, _, attack_point_index = action_dict[ll_agent_id]
                attack_point_list.append(attack_point_index)
            if len(set(attack_point_list)) > 1:
                raise ValueError("同一个智能体编队的打击点不同！！！")
            attack_point_index = attack_point_list[0]
            self.hl_last_attack_points[hl_agent_id] = attack_point_index
            if anchor_attack_point_index:
                self.hl_reward[hl_agent_id] -= abs(attack_point_index - anchor_attack_point_index) / reward_bound
                # chain_index = int(anchor_attack_point_index / ATTACK_CHAIN_POINT_NUMS)
                # if 0 < chain_index < ATTACK_CHAINS - 1:
                #     attack_point = ATTACK_POINTS[attack_point_index]
                #     _, fighter_nums = self._detect_point_fighter_nums(attack_point)
                #     self.hl_reward[hl_agent_id] -= fighter_nums / reward_bound

            # TODO 两个high level step打击点之间的距离尽可能短

    def update_ml_agent_reward(self, action_dict, is_done):
        reward_bound = 100.0
        for agent_id in LOW_LEVEL_AGENT_IDs:
            _, _, next_area_index, _ = action_dict[agent_id]
            group_name = LL_AGENTS_TO_OPERATION_GROUPS[agent_id]
            ml_agent_id = ML_AGENTS_TO_LL_AGENTS.inverse[agent_id]
            if is_done:
                self.ml_reward[ml_agent_id] += self._get_win_score()/SCORE_BOUND
            # 作战编队返航、编组内单元全部被击毁，不做任何处理
            if self.operation_groups_status[group_name]:
                continue
            exist_near_contact, fighter_nums = self._detect_fighter_nums(group_name)

            if "A2S_GROUP_" in group_name:
                if next_area_index == 0:
                    # 作战单元在原地巡逻观察，如果周边没有敌方单元，给出负奖励；如果周边有作战单元，给出奖励；
                    if exist_near_contact:
                        self.ml_reward[ml_agent_id] += fighter_nums / reward_bound
                    else:
                        self.ml_reward[ml_agent_id] -= fighter_nums / reward_bound
                    # 统计单元的油量，如果油量不足，那么应尽快向前推进
                else:
                    if exist_near_contact:
                        self.ml_reward[ml_agent_id] -= fighter_nums / reward_bound
                    else:
                        self.ml_reward[ml_agent_id] += fighter_nums / reward_bound

            elif "A2A_GROUP_" in group_name:
                pass
            elif "EJ_" in group_name:
                pass

    def update_ll_agent_reward(self, action_dict, is_done):
        for agent_id in LOW_LEVEL_AGENT_IDs:
            altitude, radar_status, _, _ = action_dict[agent_id]
            group_name = LL_AGENTS_TO_OPERATION_GROUPS[agent_id]
            if is_done:
                self.ll_reward[agent_id] += self._get_win_score()/SCORE_BOUND
            # 作战编队返航、编组内单元全部被击毁，不做任何处理
            if self.operation_groups_status[group_name]:
                continue

    # 《《《《《《《《《《《《《 动作空间 》》》》》》》》》》》》》》

    def get_operation_groups_init_area(self):
        for operation_group_name in OPERATION_GROUPS:
            group_class = self.operation_groups_class[operation_group_name]
            group_lat, group_lon = group_class.dLatitude, group_class.dLongitude
            coordinate_points = get_cell(OPERATION_AREA_GRID_DIM, RP_1, RP_2, (group_lat, group_lon))
            self.operation_groups_last_area[operation_group_name] = coordinate_points

    def compute_next_point(self, next_area_index, operation_group_name):
        # if self.steps == 1:
        #     # 获取作战编队的初始区域
        #     group_class = self.operation_groups_class[operation_group_name]
        #     group_lat, group_lon = group_class.dLatitude, group_class.dLongitude
        #     coordinate_points = get_cell(OPERATION_AREA_GRID_DIM, RP_1, RP_2, (group_lat, group_lon))
        #     next_area, _ = get_sudoku(EXTERNAL_BOUNDARY, coordinate_points)
        #     if next_area[str(next_point_index)]:
        #         # 更新作战编队最新区域
        #         self.operation_groups_last_area[operation_group_name] = next_area[str(next_point_index)]
        #         coordinate_index = next_area[str(next_point_index)]
        #         if 'A2A' in operation_group_name:
        #             lat, lon = convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2, coordinate_index[0])
        #             return lat, lon
        #         elif 'A2S' in operation_group_name:
        #             lat, lon = convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2, coordinate_index[2])
        #             return lat, lon
        #         elif 'EJ' in operation_group_name:
        #             lat, lon = convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2, coordinate_index[1])
        #             return lat, lon
        #         else:
        #             raise ValueError
        #     else:
        #         raise ValueError("区域错误！！！")
        # else:
        last_area_coord_points = self.operation_groups_last_area[operation_group_name]
        if last_area_coord_points:
            next_area, _ = get_sudoku(EXTERNAL_BOUNDARY, last_area_coord_points)
            if next_area[str(next_area_index)]:
                # 更新作战编队最新区域
                self.operation_groups_last_area[operation_group_name] = next_area[str(next_area_index)]
                coordinate_index = next_area[str(next_area_index)]
                if 'A2A' in operation_group_name:
                    lat, lon = convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2,
                                                             coordinate_index[2])
                    return lat, lon, coordinate_index[2], last_area_coord_points
                elif 'A2S' in operation_group_name:
                    lat, lon = convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2,
                                                             coordinate_index[0])
                    return lat, lon, coordinate_index[0], last_area_coord_points
                elif 'EJ' in operation_group_name:
                    # ci = (coordinate_index[0][0] - 1, coordinate_index[0][1])
                    lat, lon = convert_coordinate_to_lat_lon(OPERATION_AREA_GRID_DIM, RP_1, RP_2,
                                                             coordinate_index[0])
                    return lat, lon, coordinate_index[1], last_area_coord_points
                else:
                    raise ValueError
            else:
                raise ValueError("区域错误！！！")
        else:
            raise ValueError("没有找到作战单元所在的区域！！！")

    def control_operation_group_space(self, action_dict):
        # 把同一个智能体编队的作战编队下一个区域统一修改为歼轰机编队的下一个区域
        # temp_ac_dict = copy.deepcopy(action_dict)
        # for _, groups in HL_AGENTS_TO_ML_AGENTS.items():
        #     temp_ac = None
        #     temp_area = None
        #     for agent_id, ac in action_dict.items():
        #         group_name = LL_AGENTS_TO_OPERATION_GROUPS[agent_id]
        #         ml_agent_id = ML_AGENTS_TO_LL_AGENTS.inverse[agent_id]
        #         if ml_agent_id in groups:
        #             if "A2S_GROUP_" in group_name:
        #                 temp_ac = ac
        #                 temp_area = self.operation_groups_last_area[group_name]
        #                 break
        #     for agent_id, ac in action_dict.items():
        #         group_name = LL_AGENTS_TO_OPERATION_GROUPS[agent_id]
        #         ml_agent_id = ML_AGENTS_TO_LL_AGENTS.inverse[agent_id]
        #         if ml_agent_id in groups:
        #             if "A2S_GROUP_" not in group_name:
        #                 self.ml_reward[ml_agent_id] += -abs(temp_ac_dict[agent_id][-2] - temp_ac[-2])
        #                 # 把同一个智能体编队的下的非歼轰作战编队的下一个区域统一修改为歼轰机编队的下一个区域
        #                 temp_ac_dict[agent_id][-2] = temp_ac[-2]
        #                 self.operation_groups_last_area[group_name] = temp_area

        temp_ac_dict = copy.deepcopy(action_dict)
        for agent_id, ac in temp_ac_dict.items():
            _, _, next_area_index, attack_point_index = ac
            group_name = LL_AGENTS_TO_OPERATION_GROUPS[agent_id]
            # 作战编队返航、编组内单元全部被击毁，不做任何处理
            if self.operation_groups_status[group_name]:
                continue
            if next_area_index:  # 0 为保持不动
                lat, lon, ci, last_cp = self.compute_next_point(next_area_index, group_name)
                # 控制作战编队去下一个点
                self.control_operation_group_next_point(group_name, lat, lon)

                # if "A2S_GROUP_" in group_name:
                #     attack_point = ATTACK_POINTS[attack_point_index]
                #     ml_agent_id = ML_AGENTS_TO_LL_AGENTS.inverse[agent_id]
                #     self.ml_reward[ml_agent_id] += ((last_cp[0][0] - attack_point[0]) ** 2 +
                #                                     (last_cp[0][1] - attack_point[1]) ** 2) ** 0.5 - \
                #                                    ((ci[0] - attack_point[0]) ** 2 +
                #                                     (ci[1] - attack_point[1]) ** 2) ** 0.5

        self.dwell_time["start_time"] = datetime.now()
        self.dwell_time["dwell_time"] = BASE_DWELL_TIME

    def _nearest_ships_info(self, operation_group_name):
        """
        获取距离作战单元编队最近的舰船
        :return:
        """
        in_group_units = self.operation_groups[operation_group_name]

        auto_attack_status = False
        attack_target_guids = []
        carrier = None
        carrier_guid = None
        for ship_guid, ship_value in self.attack_ships.items():
            if CARRIER_NAME in ship_value.strName:
                carrier = ship_value
                carrier_guid = ship_guid
                break
        if carrier and carrier_guid:
            for unit_guid, unit_value in in_group_units.items():
                dis = get_two_point_distance(unit_value.dLongitude, unit_value.dLatitude,
                                             carrier.dLongitude, carrier.dLatitude)
                if dis <= AUTO_ATTACK_SHIP_DISTANCE * 1000:
                    auto_attack_status = True
            if auto_attack_status:
                ship_dis = []
                ship_guids = []
                for ship_guid, ship_value in self.attack_ships.items():
                    if CARRIER_NAME in ship_value.strName:
                        continue
                    distance = 0.0
                    for unit_guid, unit_value in in_group_units.items():
                        dis = get_two_point_distance(unit_value.dLongitude, unit_value.dLatitude,
                                                     ship_value.dLongitude, ship_value.dLatitude)
                        distance += dis
                    ship_dis.append(distance)
                    ship_guids.append(ship_guid)
                # 距离最近的两艘舰
                index = heapq.nsmallest(2, range(len(ship_dis)), ship_dis.__getitem__)
                attack_target_guids = [ship_guids[i] for i in index]

        return auto_attack_status, attack_target_guids
        # return auto_attack_status, carrier_guid

    def _near_airs_info(self, operation_group_name):
        """
        获取作战编队附近的敌方飞机
        :return:
        """
        in_group_units = self.operation_groups[operation_group_name]

        auto_attack_status = False
        attack_target_guids = []

        for air_guid, air_value in self.attack_airs.items():
            for unit_guid, unit_value in in_group_units.items():
                dis = get_two_point_distance(unit_value.dLongitude, unit_value.dLatitude,
                                             air_value.dLongitude, air_value.dLatitude)
                if dis <= AUTO_ATTACK_AIR_DISTANCE * 1000:
                    attack_target_guids.append(air_guid)
        if attack_target_guids:
            auto_attack_status = True

        return auto_attack_status, attack_target_guids

    def _auto_attack(self, group_name):
        if 'A2S' in group_name:
            # 编组内任何一个作战单元与任何一艘舰在160公里以内
            ret, target_guids = self._nearest_ships_info(group_name)
            if ret and target_guids:
                # 攻击驱逐舰或航母
                self.auto_attack_target(self.operation_groups_name_to_guid[group_name], target_guids)
        elif 'A2A' in group_name:
            ret, target_guids = self._near_airs_info(group_name)
            if ret and target_guids:
                # 攻击飞机
                self.auto_attack_target(self.operation_groups_name_to_guid[group_name], target_guids)

    def auto_attack_target(self, ops_group_guid, attack_guid_list):
        for attack_guid in attack_guid_list:
            cmd = f"ScenEdit_AttackContact(\'{ops_group_guid}\', \'{attack_guid}\'," + "{mode = 0})"
            ret = self.scenario.mozi_server.send_and_recv(cmd)

    def set_radar_status(self, group_name, radar_status):
        if radar_status:
            radar_status = 'Active'
        else:
            radar_status = 'Passive'
        fire_status = False
        if "A2A" in group_name:
            fire_status = True
        units = self.operation_groups[group_name]
        for unit_name, unit_class in units.items():
            self.modify_unit_doctrine(unit_class, radar_status, fire_status)

    def low_level_agent_execute_action(self, action_dict):
        """
        :param action_dict: 智能体的高度、速度
        :return:
        """
        if self.update_next_point:
            self.control_operation_group_space(action_dict)
        for agent_id, action_tuple in action_dict.items():
            group_name = LL_AGENTS_TO_OPERATION_GROUPS[agent_id]
            # 作战编队返航、编组内单元全部被击毁，不做任何处理
            if self.operation_groups_status[group_name]:
                continue
            altitude, radar_status, _, _ = action_tuple
            # self.control_operation_group(group_name, altitude)
            self.set_radar_status(group_name, radar_status)
            # TODO 自动攻击的启动时机
            self._auto_attack(group_name)
            # self._auto_attack_target(group_name)

    def control_operation_group(self, group_name, altitude, speed=None, heading=None):
        """
        设置作战编队高度、速度、航向
        :param group_name: 作战编队名称
        :param altitude: 作战编队高度（100，20000）
        :param speed:（海里） 作战编队速度（0, 1000） speed单位是海里，转化为公里为speed*1.852
                            speed = 1000海里/小时（1852公里/小时）
                            低速度：350海里/小时（648.2公里/小时）
                            巡航速度：480海里/小时（888.96公里/小时）
                            军用速度：520海里/小时（963.04公里/小时）
                            加力速度：920海里/小时（1703.84公里/小时）
        :param heading: 作战编队航向（0，360）
        :return:
        """
        if altitude == 0:  # 保持高度
            altitude = 10000
            cmd = "ScenEdit_SetUnit({Unitname=" + f"\'{group_name}\'," + f"Altitude={altitude}" + "})"
            self.scenario.mozi_server.send_and_recv(cmd)
        elif altitude == 1:  # 降低高度
            altitude = 10000
            cmd = "ScenEdit_SetUnit({Unitname=" + f"\'{group_name}\'," + f"Altitude={altitude}" + "})"
            self.scenario.mozi_server.send_and_recv(cmd)
        else:  # 提升高度
            altitude = 20000
            cmd = "ScenEdit_SetUnit({Unitname=" + f"\'{group_name}\'," + f"Altitude={altitude}" + "})"
            self.scenario.mozi_server.send_and_recv(cmd)
        # if altitude == 0:  # 保持高度
        #     if speed == 0:  # 保持速度
        #         speed = 480
        #         cmd = "ScenEdit_SetUnit({Unitname=" + f"\'{group_name}\'," + f"Speed={speed}" + "})"
        #         self.scenario.mozi_server.send_and_recv(cmd)
        #     else:
        #         speed = 1000
        #         cmd = "ScenEdit_SetUnit({Unitname=" + f"\'{group_name}\'," + f"Speed={speed}" + "})"
        #         self.scenario.mozi_server.send_and_recv(cmd)
        # elif altitude == 1:  # 降低高度
        #     altitude = 0
        #     if speed == 0:  # 保持速度
        #         speed = 480
        #         cmd = "ScenEdit_SetUnit({Unitname=" + f"\'{group_name}\'," + f"Altitude={altitude}," \
        #               + f"Speed={speed}" + "})"
        #         self.scenario.mozi_server.send_and_recv(cmd)
        #     else:
        #         speed = 1000
        #         cmd = "ScenEdit_SetUnit({Unitname=" + f"\'{group_name}\'," + f"Altitude={altitude}," \
        #               + f"Speed={speed}" + "})"
        #         self.scenario.mozi_server.send_and_recv(cmd)
        # else:
        #     altitude = altitude * 20000
        #     if speed == 0:  # 保持速度
        #         speed = 480
        #         cmd = "ScenEdit_SetUnit({Unitname=" + f"\'{group_name}\'," + f"Altitude={altitude}," \
        #               + f"Speed={speed}" + "})"
        #         self.scenario.mozi_server.send_and_recv(cmd)
        #     else:
        #         speed = 1000
        #         cmd = "ScenEdit_SetUnit({Unitname=" + f"\'{group_name}\'," + f"Altitude={altitude}," \
        #               + f"Speed={speed}" + "})"
        #         self.scenario.mozi_server.send_and_recv(cmd)

    def control_operation_group_next_point(self, group_name, lat, lon):
        """
        设置作战编队下一个航路点
        :param group_name: 作战编队名称
        :param lat: 下一个航路点纬度
        :param lon: 下一个航路点经度
        :return:
        """

        cmd = "ScenEdit_SetUnit({Unitname=" + f"\'{group_name}\'," + "course={{" \
              + f"latitude=\'{lat}\'," + f"longitude=\'{lon}\'" + "}}})"
        ret = self.scenario.mozi_server.send_and_recv(cmd)

    def create_operation_groups(self):
        air_to_air = {}
        air_to_surface = {}
        electronic_jammer = {}
        # 获取分层模型所需的空战、歼轰、电子干扰机
        for op_unit_key, op_unit_value in self.agent_operation_units.items():
            weapon_list = self._get_unit_weapon(op_unit_value)
            if AIR_TO_SURFACE_GROUP['UNIT_TYPE'] in op_unit_value.strName and \
                    self._get_weapon_info(weapon_list, AIR_TO_SURFACE_GROUP['WEAPON_TYPE']):
                air_to_surface[op_unit_key] = op_unit_value
            if AIR_TO_AIR_GROUP['UNIT_TYPE'] in op_unit_value.strName and \
                    self._get_weapon_info(weapon_list, AIR_TO_AIR_GROUP['WEAPON_TYPE']) and not \
                    self._get_weapon_info(weapon_list, AIR_TO_SURFACE_GROUP['WEAPON_TYPE']):
                air_to_air[op_unit_key] = op_unit_value
            if ELECTRONIC_JAMMER['UNIT_TYPE'] in op_unit_value.strName:
                electronic_jammer[op_unit_key] = op_unit_value

        # 对分层模型所需的空战、歼轰、电子干扰机进行分组
        assert air_to_air.__len__() >= self.air_to_air_groups.__len__() * AIR_TO_AIR_GROUP['NUM']
        for name in AIR_TO_AIR_GROUPS:
            for _ in range(AIR_TO_AIR_GROUP['NUM']):
                k = random.choice(list(air_to_air.keys()))
                self.air_to_air_groups[name][k] = air_to_air.pop(k)

        assert air_to_surface.__len__() >= self.air_to_surface_groups.__len__() * AIR_TO_SURFACE_GROUP['NUM']
        for name in AIR_TO_SURFACE_GROUPS:
            for _ in range(AIR_TO_SURFACE_GROUP['NUM']):
                k = random.choice(list(air_to_surface.keys()))
                self.air_to_surface_groups[name][k] = air_to_surface.pop(k)

        assert electronic_jammer.__len__() >= self.electronic_jammer_groups.__len__() * ELECTRONIC_JAMMER['NUM']
        for name in ELECTRONIC_JAMMER_GROUPS:
            for _ in range(ELECTRONIC_JAMMER['NUM']):
                k = random.choice(list(electronic_jammer.keys()))
                self.electronic_jammer_groups[name][k] = electronic_jammer.pop(k)

    def operation_group_out(self):
        for k, v in self.air_to_air_groups.items():
            cmd = "Hs_ScenEdit_AirOpsGroupOut(" + "{"
            for guid in v.keys():
                cmd += f"\'{guid}\'" + ","
            cmd += "})"  # 按编队出动
            self.scenario.mozi_server.send_and_recv(cmd)

        for k, v in self.air_to_surface_groups.items():
            cmd = "Hs_ScenEdit_AirOpsGroupOut(" + "{"
            for guid in v.keys():
                cmd += f"\'{guid}\'" + ","
            cmd += "})"  # 按编队出动
            self.scenario.mozi_server.send_and_recv(cmd)

        for k, v in self.electronic_jammer_groups.items():
            guid = list(v.keys())[0]
            cmd = "Hs_ScenEdit_AirOpsSingleOut({" + f"\'{guid}\'" + "})"  # 电子干扰机单机出动
            self.scenario.mozi_server.send_and_recv(cmd)

    def operation_group_name_to_guid(self):
        """
        python中的作战单元编组名，与墨子中实际的作战单元编组唯一guid，建立映射关系。
        :return:
        """
        for k, v in self.side.groups.items():
            for group_name, units in self.air_to_air_groups.items():
                if v.m_GroupLead in units.keys():
                    self.air_to_air_group_name_to_guid[group_name] = k
                    # 编对命名
                    cmd = "ScenEdit_SetUnit({" + f"Unitname='{v.strName}'," + f"Newname='{group_name}'" + "})"
                    self.scenario.mozi_server.send_and_recv(cmd)
                    break
            for group_name, units in self.air_to_surface_groups.items():
                if v.m_GroupLead in units.keys():
                    self.air_to_surface_group_name_to_guid[group_name] = k
                    # 编对命名
                    cmd = "ScenEdit_SetUnit({" + f"Unitname='{v.strName}'," + f"Newname='{group_name}'" + "})"
                    self.scenario.mozi_server.send_and_recv(cmd)
                    break

        for group_name, unit in self.electronic_jammer_groups.items():
            guid = list(unit.keys())[0]
            self.electronic_jammer_group_name_to_guid[group_name] = guid
            # 编对命名
            value = list(unit.values())[0]
            cmd = "ScenEdit_SetUnit({" + f"Unitname='{value.strName}'," + f"Newname='{group_name}'" + "})"
            self.scenario.mozi_server.send_and_recv(cmd)

        self.operation_groups = dict(self.air_to_air_groups,
                                     **self.air_to_surface_groups, **self.electronic_jammer_groups)
        self.operation_groups_name_to_guid = dict(self.air_to_air_group_name_to_guid,
                                                  **self.air_to_surface_group_name_to_guid,
                                                  **self.electronic_jammer_group_name_to_guid)
        assert self.operation_groups.keys() == self.operation_groups_name_to_guid.keys()

    def _set_simulate_speed(self, sc, di):
        """
        加速推演
        """
        # Hs_SetSimCompression(3)
        self.scenario.mozi_server.set_simulate_compression(sc)
        self.scenario.mozi_server.set_decision_step_length(di)


class HighLevelEnv(MultiAgentEnv):
    def __init__(self, mozi_env):
        self.high_level_steps = 0
        self.mozi_env = mozi_env
        # 是否更新了智能体的下一个区域
        self.update_next_point = False
        # 是否更新了智能体的下一个打击点
        self.update_next_attack_point = False
        self.mid_level_action_embed = self.mozi_env.mid_level_action_embed
        self.high_level_action_embed = self.mozi_env.high_level_action_embed
        self.high_level_init_avail_action = self.mozi_env.high_level_init_avail_action

    def step(self, action_dict):
        self.high_level_steps += 1
        ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info = {}, {}, {}, {}
        low_level_action_dict = {}
        mid_level_action_dict = {}
        high_level_action_dict = {}
        multi_agent_action_dict = {}
        for agent_id, action in action_dict.items():
            if 'll_agent_' in agent_id:
                low_level_action_dict[agent_id] = action
                multi_agent_action_dict[agent_id] = list(action)
            if 'ml_agent_' in agent_id:
                mid_level_action_dict[agent_id] = action
                # 更新LAST_HL_ML_AGENTS_ACTION
                LAST_HL_ML_AGENTS_ACTION[agent_id] = action
            if 'hl_agent_' in agent_id:
                high_level_action_dict[agent_id] = action
                # 更新LAST_HL_ML_AGENTS_ACTION
                LAST_HL_ML_AGENTS_ACTION[agent_id] = action
        ll_action_ret = low_level_action_dict.__len__() > 0
        ml_action_ret = mid_level_action_dict.__len__() > 0
        hl_action_ret = high_level_action_dict.__len__() > 0

        # 上、中、底层都有动作返回，构造底层智能体的状态空间、奖励等，并存入数据单元，用于后续构造中上层智能体的输入数据。
        # 下一步ray只返回底层智能体的动作。
        if self.high_level_steps == 1:
            assert low_level_action_dict.__len__() == LOW_LEVEL_AGENT_IDs.__len__()
            assert mid_level_action_dict.__len__() == MID_LEVEL_AGENT_IDs.__len__()
            assert high_level_action_dict.__len__() == HIGH_LEVEL_AGENT_IDs.__len__()

            # 通过高、中、底层智能体的动作，构造底层智能体的动作（航向、航速、高度、下一个区域点、停留时间）
            for agent_id, _ in multi_agent_action_dict.items():
                # 添加下一个区域点
                ml_agent_id = ML_AGENTS_TO_LL_AGENTS.inverse[agent_id]
                mid_level_action = LAST_HL_ML_AGENTS_ACTION[ml_agent_id]
                multi_agent_action_dict[agent_id].append(mid_level_action)
                # 添加停留时间
                hl_agent_id = ml_agent_to_hl_agent(ml_agent_id)
                high_level_action = LAST_HL_ML_AGENTS_ACTION[hl_agent_id]
                multi_agent_action_dict[agent_id].append(high_level_action)

            self.update_next_point = True
            self.update_next_attack_point = True
            (low_level_agent_obs, global_obs, ll_reward, ml_reward, hl_reward, ret_ml, ret_hl, done, info,
             ml_avail_action_action_mask, hl_avail_action_action_mask) = \
                self.mozi_env.step(multi_agent_action_dict, self.update_next_point, self.update_next_attack_point)
            self.update_next_point = False
            self.update_next_attack_point = False
            t_low_level_agent_obs = copy.deepcopy(low_level_agent_obs)

            for low_level_agent_id, obs in low_level_agent_obs.items():
                # 找出对应的中层智能体的动作
                ml_agent_id = ML_AGENTS_TO_LL_AGENTS.inverse[low_level_agent_id]
                mid_level_action = LAST_HL_ML_AGENTS_ACTION[ml_agent_id]
                hl_agent_id = ml_agent_to_hl_agent(ml_agent_id)
                high_level_action = LAST_HL_ML_AGENTS_ACTION[hl_agent_id]

                if not ret_ml["__all__"]:
                    # 构造底层智能体的obs、reward、done、info
                    t_low_level_agent_obs[low_level_agent_id][SampleBatch.OBS].append(mid_level_action)
                    t_low_level_agent_obs[low_level_agent_id][SampleBatch.OBS].append(high_level_action)

                    # 更新ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info
                    ret_ray_obs.update(t_low_level_agent_obs)
                    ret_ray_reward.update(ll_reward)
                    ret_ray_done.update(done)
                    ret_ray_info.update(info)

                    # 把底层智能体的obs添加进数据存储单元，用于后面构造中、上层智能体的输入数据
                    t_obs = copy.deepcopy(obs)
                    t_obs[SampleBatch.OBS].append(mid_level_action)
                    t_obs[SampleBatch.OBS].append(high_level_action)
                    low_level_values_dict = {
                        SampleBatch.OBS: t_obs[SampleBatch.OBS],
                        SampleBatch.REWARDS: ll_reward[low_level_agent_id],
                        SampleBatch.DONES: done[low_level_agent_id],
                        ENV_STATE: global_obs,
                        "t": self.high_level_steps,
                        "ret_ml": ret_ml[low_level_agent_id]
                    }
                    LL_DATA_COLLECTOR[low_level_agent_id].add_values(low_level_values_dict)
                else:
                    # 把底层智能体的obs添加进数据存储单元
                    t_obs = copy.deepcopy(obs)
                    t_obs[SampleBatch.OBS].append(mid_level_action)
                    t_obs[SampleBatch.OBS].append(high_level_action)
                    low_level_values_dict = {SampleBatch.OBS: t_obs[SampleBatch.OBS],
                                             SampleBatch.REWARDS: ll_reward[low_level_agent_id],
                                             SampleBatch.DONES: done[low_level_agent_id],
                                             ENV_STATE: global_obs,
                                             "t": self.high_level_steps,
                                             "ret_ml": ret_ml[low_level_agent_id]}
                    LL_DATA_COLLECTOR[low_level_agent_id].add_values(low_level_values_dict)

                    temp_ml_agent_state = []
                    for s in LL_DATA_COLLECTOR[low_level_agent_id].buffers[ENV_STATE]:
                        temp_ml_agent_state += s  # 拼接全局state向量
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][ENV_STATE] = temp_ml_agent_state

                    temp_ml_agent_obs = []
                    for o in LL_DATA_COLLECTOR[low_level_agent_id].buffers[SampleBatch.OBS]:
                        temp_ml_agent_obs += o  # 拼接局部obs向量
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.OBS] = temp_ml_agent_obs

                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id]["action_mask"] = \
                        ml_avail_action_action_mask[ml_agent_id]["action_mask"]
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id]["avail_actions"] = \
                        ml_avail_action_action_mask[ml_agent_id]["avail_actions"]

                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.REWARDS] = ml_reward[ml_agent_id]
                    # for r in LL_DATA_COLLECTOR[low_level_agent_id].buffers[SampleBatch.REWARDS]:
                    #     # 累加对应底层智能体的奖励作为中层智能体的奖励
                    #     LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.REWARDS] += r
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.DONES] = done[low_level_agent_id]
                    LAST_ML_AGENTS_OBS_REWARD_DONE["__all__"] = done["__all__"]

            if ret_ml["__all__"]:
                # ret_hl["__all__"]为true时，ret_ml["__all__"]一定为true.
                if not ret_hl["__all__"]:
                    # 返回中层智能体的状态空间
                    ml_agent_obs = {ml_agent_id: {} for ml_agent_id in MID_LEVEL_AGENT_IDs}
                    ml_agent_reward, ml_agent_done, ml_agent_info = {}, {}, {}
                    for ml_agent_id in MID_LEVEL_AGENT_IDs:
                        ml_agent_obs[ml_agent_id][SampleBatch.OBS] = \
                            LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.OBS]

                        ml_agent_obs[ml_agent_id]["action_mask"] = \
                            LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id]["action_mask"]
                        ml_agent_obs[ml_agent_id]["avail_actions"] = \
                            LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id]["avail_actions"]

                        ml_agent_obs[ml_agent_id][ENV_STATE] = LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][
                            ENV_STATE]
                        ml_agent_reward[ml_agent_id] = \
                            LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.REWARDS]
                        ml_agent_done[ml_agent_id] = \
                            LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.DONES]
                        ml_agent_info[ml_agent_id] = {}

                    # 更新ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info
                    ret_ray_obs.update(ml_agent_obs)
                    ret_ray_reward.update(ml_agent_reward)
                    ret_ray_done.update(ml_agent_done)
                    ret_ray_info.update(ml_agent_info)

                # 更新上层智能体的数据存储单元
                for hl_agent_id in HIGH_LEVEL_AGENT_IDs:
                    temp_hl_agent_obs = []
                    for ml_agent_id in HL_AGENTS_TO_ML_AGENTS[hl_agent_id]:
                        temp_hl_agent_obs += LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.OBS]

                    high_level_values_dict = {SampleBatch.OBS: temp_hl_agent_obs,
                                              ENV_STATE: LAST_ML_AGENTS_OBS_REWARD_DONE['ml_agent_0'][ENV_STATE]}
                    HL_DATA_COLLECTOR[hl_agent_id].add_values(high_level_values_dict)

            # ret_hl["__all__"]为true时，ret_ml["__all__"]一定为true.
            if ret_hl["__all__"]:
                hl_agent_obs = {hl_agent_id: {SampleBatch.OBS: [], ENV_STATE: []} for hl_agent_id in
                                HIGH_LEVEL_AGENT_IDs}
                hl_agent_reward = hl_reward
                hl_agent_done = {hl_agent_id: False for hl_agent_id in HIGH_LEVEL_AGENT_IDs}
                hl_agent_info = {hl_agent_id: {} for hl_agent_id in HIGH_LEVEL_AGENT_IDs}

                for hl_agent_id in HIGH_LEVEL_AGENT_IDs:
                    # temp_hl_agent_obs = []
                    # for ml_agent_id in HL_AGENTS_TO_ML_AGENTS[hl_agent_id]:
                    #     temp_hl_agent_obs += LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.OBS]
                    # hl_agent_obs[hl_agent_id][SampleBatch.OBS] = temp_hl_agent_obs
                    # hl_agent_obs[hl_agent_id][ENV_STATE] = LAST_ML_AGENTS_OBS_REWARD_DONE['ml_agent_0'][ENV_STATE]

                    temp_hl_agent_state = []
                    for s in HL_DATA_COLLECTOR[hl_agent_id].buffers[ENV_STATE]:
                        temp_hl_agent_state += s  # 拼接全局state向量
                    hl_agent_obs[hl_agent_id][ENV_STATE] = temp_hl_agent_state

                    temp_hl_agent_obs = []
                    for o in HL_DATA_COLLECTOR[hl_agent_id].buffers[SampleBatch.OBS]:
                        temp_hl_agent_obs += o  # 拼接局部obs向量
                    hl_agent_obs[hl_agent_id][SampleBatch.OBS] = temp_hl_agent_obs

                    HL_DATA_COLLECTOR[hl_agent_id] = AgentCollector()

                    hl_agent_obs[hl_agent_id]["action_mask"] = hl_avail_action_action_mask[hl_agent_id]["action_mask"]
                    hl_agent_obs[hl_agent_id]["avail_actions"] = \
                        hl_avail_action_action_mask[hl_agent_id]["avail_actions"]

                    hl_agent_done[hl_agent_id] = LAST_ML_AGENTS_OBS_REWARD_DONE['ml_agent_0'][SampleBatch.DONES]

                # 更新ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info
                ret_ray_obs.update(hl_agent_obs)
                ret_ray_reward.update(hl_agent_reward)
                ret_ray_done.update(hl_agent_done)
                ret_ray_info.update(hl_agent_info)

            ret_ray_done['__all__'] = done['__all__']
            # print(f"1208: {ret_ray_obs}")
            return ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info

        # 只有底层智能体返回动作，
        # 如果底层智能体全部执行完中上层给的目标，那么返回给ray的是上层的状态空间、奖励，下一步ray只返回上层的动作；清空数据单元？
        # 如果底层智能体没有执行完中上层给的目标，那么返回给ray的是底层的状态空间、奖励，
        elif ll_action_ret and not ml_action_ret and not hl_action_ret:
            assert low_level_action_dict.__len__() == LOW_LEVEL_AGENT_IDs.__len__()

            # 通过高、中、底层智能体的动作，构造底层智能体的动作（航向、航速、高度、下一个区域点、停留时间）
            for agent_id, _ in multi_agent_action_dict.items():
                # 添加下一个区域点
                ml_agent_id = ML_AGENTS_TO_LL_AGENTS.inverse[agent_id]
                mid_level_action = LAST_HL_ML_AGENTS_ACTION[ml_agent_id]
                multi_agent_action_dict[agent_id].append(mid_level_action)
                # 添加停留时间
                hl_agent_id = ml_agent_to_hl_agent(ml_agent_id)
                high_level_action = LAST_HL_ML_AGENTS_ACTION[hl_agent_id]
                multi_agent_action_dict[agent_id].append(high_level_action)

            (low_level_agent_obs, global_obs, ll_reward, ml_reward, hl_reward, ret_ml, ret_hl, done, info,
             ml_avail_action_action_mask, hl_avail_action_action_mask) = \
                self.mozi_env.step(multi_agent_action_dict, self.update_next_point, self.update_next_attack_point)
            self.update_next_point = False
            self.update_next_attack_point = False
            t_low_level_agent_obs = copy.deepcopy(low_level_agent_obs)

            for low_level_agent_id, obs in low_level_agent_obs.items():
                # 找出对应的中层智能体的动作
                ml_agent_id = ML_AGENTS_TO_LL_AGENTS.inverse[low_level_agent_id]
                mid_level_action = LAST_HL_ML_AGENTS_ACTION[ml_agent_id]
                hl_agent_id = ml_agent_to_hl_agent(ml_agent_id)
                high_level_action = LAST_HL_ML_AGENTS_ACTION[hl_agent_id]

                # 构造底层智能体的obs、reward、done、info
                t_low_level_agent_obs[low_level_agent_id][SampleBatch.OBS].append(mid_level_action)
                t_low_level_agent_obs[low_level_agent_id][SampleBatch.OBS].append(high_level_action)

                # 如果done['__all__']为true，那么ret["__all__"]一定为true.
                # done['__all__']为true，ret["__all__"]为true时，返回底层智能体的obs，更新LL_DATA_COLLECTOR.
                if done['__all__']:
                    assert ret_ml["__all__"] is True
                    # 更新ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info
                    ret_ray_obs.update(t_low_level_agent_obs)
                    ret_ray_reward.update(ll_reward)
                    ret_ray_done.update(done)
                    ret_ray_info.update(info)

                    # 把底层智能体的obs添加进数据存储单元
                    t_obs = copy.deepcopy(obs)
                    t_obs[SampleBatch.OBS].append(mid_level_action)
                    t_obs[SampleBatch.OBS].append(high_level_action)
                    low_level_values_dict = {SampleBatch.OBS: t_obs[SampleBatch.OBS],
                                             SampleBatch.REWARDS: ll_reward[low_level_agent_id],
                                             SampleBatch.DONES: done[low_level_agent_id],
                                             ENV_STATE: global_obs,
                                             "t": self.high_level_steps,
                                             "ret_ml": ret_ml[low_level_agent_id]}
                    LL_DATA_COLLECTOR[low_level_agent_id].add_values(low_level_values_dict)
                # 如果ret['__all__']为false，那么done["__all__"]一定为false.
                # ret_ml["__all__"]为false时，ret_hl["__all__"]一定为false.
                # ret['__all__']为false，done["__all__"]为false时，返回底层智能体的obs，更新LL_DATA_COLLECTOR.
                if not ret_ml["__all__"]:
                    assert done["__all__"] is False
                    # 更新ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info
                    ret_ray_obs.update(t_low_level_agent_obs)
                    ret_ray_reward.update(ll_reward)
                    ret_ray_done.update(done)
                    ret_ray_info.update(info)

                    # 把底层智能体的obs添加进数据存储单元
                    t_obs = copy.deepcopy(obs)
                    t_obs[SampleBatch.OBS].append(mid_level_action)
                    t_obs[SampleBatch.OBS].append(high_level_action)
                    low_level_values_dict = {SampleBatch.OBS: t_obs[SampleBatch.OBS],
                                             SampleBatch.REWARDS: ll_reward[low_level_agent_id],
                                             SampleBatch.DONES: done[low_level_agent_id],
                                             ENV_STATE: global_obs,
                                             "t": self.high_level_steps,
                                             "ret_ml": ret_ml[low_level_agent_id]}
                    LL_DATA_COLLECTOR[low_level_agent_id].add_values(low_level_values_dict)
                else:
                    # done['__all__']为true时，上面已经把底层智能体数据存到数据存储单元，勿重复存放.
                    # ret['__all__']为true，done["__all__"]为false时，更新LL_DATA_COLLECTOR.
                    if not done['__all__']:
                        # 把底层智能体的obs添加进数据存储单元
                        t_obs = copy.deepcopy(obs)
                        t_obs[SampleBatch.OBS].append(mid_level_action)
                        t_obs[SampleBatch.OBS].append(high_level_action)
                        low_level_values_dict = {SampleBatch.OBS: t_obs[SampleBatch.OBS],
                                                 SampleBatch.REWARDS: ll_reward[low_level_agent_id],
                                                 SampleBatch.DONES: done[low_level_agent_id],
                                                 ENV_STATE: global_obs,
                                                 "t": self.high_level_steps,
                                                 "ret_ml": ret_ml[low_level_agent_id]}
                        LL_DATA_COLLECTOR[low_level_agent_id].add_values(low_level_values_dict)

                    temp_ml_agent_state = []
                    for s in LL_DATA_COLLECTOR[low_level_agent_id].buffers[ENV_STATE]:
                        temp_ml_agent_state += s  # 拼接全局state向量
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][ENV_STATE] = temp_ml_agent_state

                    temp_ml_agent_obs = []
                    for o in LL_DATA_COLLECTOR[low_level_agent_id].buffers[SampleBatch.OBS]:
                        temp_ml_agent_obs += o  # 拼接局部obs向量
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.OBS] = temp_ml_agent_obs

                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id]["action_mask"] = \
                        ml_avail_action_action_mask[ml_agent_id]["action_mask"]
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id]["avail_actions"] = \
                        ml_avail_action_action_mask[ml_agent_id]["avail_actions"]

                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.REWARDS] = ml_reward[ml_agent_id]
                    # for r in LL_DATA_COLLECTOR[low_level_agent_id].buffers[SampleBatch.REWARDS]:
                    #     # 累加对应底层智能体的奖励作为中层智能体的奖励
                    #     LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.REWARDS] += r
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.DONES] = done[low_level_agent_id]
                    LAST_ML_AGENTS_OBS_REWARD_DONE["__all__"] = done["__all__"]

            # 如果done['__all__']为true，那么ret["__all__"]一定为true.
            # ret_hl["__all__"]为true时，ret_ml["__all__"]一定为true.
            # ret_ml["__all__"]为true，ret_hl["__all__"]为false时.
            # 除reset和done=true时同时返回上中下三层智能体的状态，其余状态下只允许返回一层智能体的状态。
            if ret_ml["__all__"]:
                if not ret_hl["__all__"] or done['__all__']:
                    # 返回中层智能体的状态
                    ml_agent_obs = {ml_agent_id: {} for ml_agent_id in MID_LEVEL_AGENT_IDs}
                    ml_agent_reward, ml_agent_done, ml_agent_info = {}, {}, {}
                    for ml_agent_id in MID_LEVEL_AGENT_IDs:
                        ml_agent_obs[ml_agent_id][SampleBatch.OBS] = \
                            LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.OBS]

                        ml_agent_obs[ml_agent_id]["action_mask"] = \
                            LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id]["action_mask"]
                        ml_agent_obs[ml_agent_id]["avail_actions"] = \
                            LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id]["avail_actions"]

                        ml_agent_obs[ml_agent_id][ENV_STATE] = LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][
                            ENV_STATE]
                        ml_agent_reward[ml_agent_id] = \
                            LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.REWARDS]
                        ml_agent_done[ml_agent_id] = \
                            LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.DONES]
                        ml_agent_info[ml_agent_id] = {}

                    # 更新ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info
                    ret_ray_obs.update(ml_agent_obs)
                    ret_ray_reward.update(ml_agent_reward)
                    ret_ray_done.update(ml_agent_done)
                    ret_ray_info.update(ml_agent_info)

                # 更新上层智能体的数据存储单元
                for hl_agent_id in HIGH_LEVEL_AGENT_IDs:
                    temp_hl_agent_obs = []
                    for ml_agent_id in HL_AGENTS_TO_ML_AGENTS[hl_agent_id]:
                        temp_hl_agent_obs += LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.OBS]

                    high_level_values_dict = {SampleBatch.OBS: temp_hl_agent_obs,
                                              ENV_STATE: LAST_ML_AGENTS_OBS_REWARD_DONE['ml_agent_0'][
                                                  ENV_STATE]}
                    HL_DATA_COLLECTOR[hl_agent_id].add_values(high_level_values_dict)

            # ret_hl["__all__"]为true时，ret_ml["__all__"]一定为true.
            # 反过来，ret_ml["__all__"]为false时，ret_hl["__all__"]一定为false.
            if ret_hl["__all__"]:
                hl_agent_obs = {hl_agent_id: {SampleBatch.OBS: [], ENV_STATE: []} for hl_agent_id in
                                HIGH_LEVEL_AGENT_IDs}
                hl_agent_reward = hl_reward
                hl_agent_done = {hl_agent_id: False for hl_agent_id in HIGH_LEVEL_AGENT_IDs}
                hl_agent_info = {hl_agent_id: {} for hl_agent_id in HIGH_LEVEL_AGENT_IDs}

                for hl_agent_id in HIGH_LEVEL_AGENT_IDs:
                    # temp_hl_agent_obs = []
                    # for ml_agent_id in HL_AGENTS_TO_ML_AGENTS[hl_agent_id]:
                    #     temp_hl_agent_obs += LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.OBS]
                    # hl_agent_obs[hl_agent_id][SampleBatch.OBS] = temp_hl_agent_obs
                    # hl_agent_obs[hl_agent_id][ENV_STATE] = LAST_ML_AGENTS_OBS_REWARD_DONE['ml_agent_0'][ENV_STATE]

                    temp_hl_agent_state = []
                    for s in HL_DATA_COLLECTOR[hl_agent_id].buffers[ENV_STATE]:
                        temp_hl_agent_state += s  # 拼接全局state向量
                    hl_agent_obs[hl_agent_id][ENV_STATE] = temp_hl_agent_state

                    temp_hl_agent_obs = []
                    for o in HL_DATA_COLLECTOR[hl_agent_id].buffers[SampleBatch.OBS]:
                        temp_hl_agent_obs += o  # 拼接局部obs向量
                    hl_agent_obs[hl_agent_id][SampleBatch.OBS] = temp_hl_agent_obs

                    HL_DATA_COLLECTOR[hl_agent_id] = AgentCollector()

                    hl_agent_obs[hl_agent_id]["action_mask"] = hl_avail_action_action_mask[hl_agent_id]["action_mask"]
                    hl_agent_obs[hl_agent_id]["avail_actions"] = \
                        hl_avail_action_action_mask[hl_agent_id]["avail_actions"]

                    hl_agent_done[hl_agent_id] = LAST_ML_AGENTS_OBS_REWARD_DONE['ml_agent_0'][SampleBatch.DONES]

                # 更新ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info
                ret_ray_obs.update(hl_agent_obs)
                ret_ray_reward.update(hl_agent_reward)
                ret_ray_done.update(hl_agent_done)
                ret_ray_info.update(hl_agent_info)

            if done['__all__']:
                # 清空LAST_HL_ML_AGENTS_ACTION
                for agent_id in HL_ML_AGENT_IDs:
                    LAST_HL_ML_AGENTS_ACTION[agent_id] = None
                # 清空LAST_ML_AGENTS_OBS_REWARD_DONE
                for agent_id in HL_ML_AGENT_IDs:
                    LAST_ML_AGENTS_OBS_REWARD_DONE[agent_id] = {}
                # 清空底层智能体的数据存储单元
                for low_level_agent_id in LOW_LEVEL_AGENT_IDs:
                    LL_DATA_COLLECTOR[low_level_agent_id] = AgentCollector()
                # 清空上层智能体的数据存储单元
                for high_level_agent_id in HIGH_LEVEL_AGENT_IDs:
                    HL_DATA_COLLECTOR[high_level_agent_id] = AgentCollector()

            ret_ray_done['__all__'] = done['__all__']
            # print(f"1378: {ret_ray_obs}")
            return ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info

        # 只有上层智能体返回动作，更新LAST_HL_ML_AGENTS_ACTION，
        # 把上层智能体的动作，拼接到中层智能体的状态空间LAST_ML_AGENTS_OBS_REWARD_DONE，
        # 返回给ray，下一步ray只返回中层智能体的动作。
        elif not ll_action_ret and not ml_action_ret and hl_action_ret:
            assert high_level_action_dict.__len__() == HIGH_LEVEL_AGENT_IDs.__len__()
            for hl_agent_id, ac in high_level_action_dict.items():
                LAST_HL_ML_AGENTS_ACTION[hl_agent_id] = ac
                # 找到对应的中层智能体，并替换掉LAST_ML_AGENTS_OBS_REWARD_DONE中的mid_level_action
                for ml_agent_id in HL_AGENTS_TO_ML_AGENTS[hl_agent_id]:
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.OBS][-1] = ac
            # 返回中层智能体的状态空间
            ml_agent_obs = {ml_agent_id: {} for ml_agent_id in MID_LEVEL_AGENT_IDs}
            ml_agent_reward, ml_agent_done, ml_agent_info = {}, {}, {}
            for ml_agent_id in MID_LEVEL_AGENT_IDs:
                ml_agent_obs[ml_agent_id][SampleBatch.OBS] = \
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.OBS]
                ml_agent_obs[ml_agent_id][ENV_STATE] = LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][ENV_STATE]

                ml_agent_obs[ml_agent_id]["action_mask"] = \
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id]["action_mask"]
                ml_agent_obs[ml_agent_id]["avail_actions"] = \
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id]["avail_actions"]

                ml_agent_reward[ml_agent_id] = \
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.REWARDS]
                ml_agent_done[ml_agent_id] = \
                    LAST_ML_AGENTS_OBS_REWARD_DONE[ml_agent_id][SampleBatch.DONES]
                ml_agent_info[ml_agent_id] = {}

            # 更新ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info
            ret_ray_obs.update(ml_agent_obs)
            ret_ray_reward.update(ml_agent_reward)
            ret_ray_done.update(ml_agent_done)
            ret_ray_info.update(ml_agent_info)

            self.update_next_attack_point = True
            ret_ray_done['__all__'] = LAST_ML_AGENTS_OBS_REWARD_DONE["__all__"]
            # print(f"1417: {ret_ray_obs}")
            return ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info

        # 只有中层智能体返回动作，更新LAST_HL_ML_AGENTS_ACTION，
        # 把中层智能体的动作，拼接到底层智能体的状态空间，返回给ray，下一步ray只返回底层智能体的动作。
        elif not ll_action_ret and ml_action_ret and not hl_action_ret:
            assert mid_level_action_dict.__len__() == MID_LEVEL_AGENT_IDs.__len__()

            ll_agent_obs = {ll_agent_id: {} for ll_agent_id in LOW_LEVEL_AGENT_IDs}
            ll_agent_reward, ll_agent_done, ll_agent_info = {}, {}, {}
            for ml_agent_id, ac in mid_level_action_dict.items():
                LAST_HL_ML_AGENTS_ACTION[ml_agent_id] = ac

                ll_agent_id = ML_AGENTS_TO_LL_AGENTS[ml_agent_id]
                hl_agent_id = ml_agent_to_hl_agent(ml_agent_id)
                # 取出底层智能体最近一次的obs、reward、done
                ll_agent_obs[ll_agent_id][SampleBatch.OBS] = LL_DATA_COLLECTOR[ll_agent_id].buffers[SampleBatch.OBS][-1]
                # 用新的上层和中层的动作替换掉底层智能体最近一次的obs中的旧的上层和中层的动作
                ll_agent_obs[ll_agent_id][SampleBatch.OBS][-1] = LAST_HL_ML_AGENTS_ACTION[hl_agent_id]
                ll_agent_obs[ll_agent_id][SampleBatch.OBS][-2] = ac

                ll_agent_obs[ll_agent_id][ENV_STATE] = LL_DATA_COLLECTOR[ll_agent_id].buffers[ENV_STATE][-1]
                ll_agent_reward[ll_agent_id] = LL_DATA_COLLECTOR[ll_agent_id].buffers[SampleBatch.REWARDS][-1]
                ll_agent_done[ll_agent_id] = LL_DATA_COLLECTOR[ll_agent_id].buffers[SampleBatch.DONES][-1]
                ll_agent_info[ll_agent_id] = {}
                # 清空相应底层智能体的数据存储单元
                LL_DATA_COLLECTOR[ll_agent_id] = AgentCollector()

                # 把底层智能体的init_obs添加进数据存储单元
                LL_DATA_COLLECTOR[ll_agent_id].add_init_obs(ll_agent_obs[ll_agent_id][ENV_STATE],
                                                            self.high_level_steps,
                                                            False,
                                                            ll_agent_obs[ll_agent_id][SampleBatch.OBS])
            # 更新ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info
            ret_ray_obs.update(ll_agent_obs)
            ret_ray_reward.update(ll_agent_reward)
            ret_ray_done.update(ll_agent_done)
            ret_ray_info.update(ll_agent_info)

            self.update_next_point = True
            ret_ray_done['__all__'] = all(ll_agent_done.values())
            # print(f"1458: {ret_ray_obs}")
            return ret_ray_obs, ret_ray_reward, ret_ray_done, ret_ray_info

    def reset(self):
        self.high_level_steps = 0
        self.update_next_point = False
        self.update_next_attack_point = False
        # 清空LAST_HL_ML_AGENTS_ACTION
        for agent_id in HL_ML_AGENT_IDs:
            LAST_HL_ML_AGENTS_ACTION[agent_id] = None
        # 清空LAST_ML_AGENTS_OBS_REWARD_DONE
        for agent_id in HL_ML_AGENT_IDs:
            LAST_ML_AGENTS_OBS_REWARD_DONE[agent_id] = {}

        global HL_DATA_COLLECTOR
        HL_DATA_COLLECTOR = {
            agent_id: AgentCollector()
            for agent_id in HIGH_LEVEL_AGENT_IDs
        }

        low_level_agent_obs, global_obs = self.mozi_env.reset()
        hl_agent_obs = {hl_agent_id: {SampleBatch.OBS: [], ENV_STATE: global_obs} for hl_agent_id in
                        HIGH_LEVEL_AGENT_IDs}
        ml_agent_obs = {ml_agent_id: {SampleBatch.OBS: None, ENV_STATE: global_obs} for ml_agent_id in
                        MID_LEVEL_AGENT_IDs}
        ret_ml = False  # 是否返回上一层
        high_level_action, mid_level_action = 0, 0
        for low_level_agent_id, obs in low_level_agent_obs.items():
            # 清空相应底层智能体的数据存储单元
            LL_DATA_COLLECTOR[low_level_agent_id] = AgentCollector()
            # 把底层智能体的init_obs添加进数据存储单元
            t_obs = copy.deepcopy(obs)
            t_obs[SampleBatch.OBS].append(mid_level_action)
            t_obs[SampleBatch.OBS].append(high_level_action)
            LL_DATA_COLLECTOR[low_level_agent_id].add_init_obs(global_obs,
                                                               self.high_level_steps,
                                                               ret_ml,
                                                               t_obs[SampleBatch.OBS])

            low_level_agent_obs[low_level_agent_id][SampleBatch.OBS].append(mid_level_action)
            low_level_agent_obs[low_level_agent_id][SampleBatch.OBS].append(high_level_action)

            # 把中层智能体的init_obs添加进数据存储单元
            ml_agent_id = ML_AGENTS_TO_LL_AGENTS.inverse[low_level_agent_id]
            # LL_DATA_COLLECTOR[ml_agent_id].add_init_obs(global_obs,
            #                                           self.high_level_steps,
            #                                           ret_ml, obs.append(high_level_action))
            ml_agent_obs[ml_agent_id][SampleBatch.OBS] = t_obs[SampleBatch.OBS]
            # ml_agent_obs[ml_agent_id][SampleBatch.OBS].append(high_level_action)
            ml_action_mask = [1 for _ in range(MID_LEVEL_ACT_SPACE)]
            ml_agent_obs[ml_agent_id]["action_mask"] = ml_action_mask
            ml_agent_obs[ml_agent_id]["avail_actions"] = self.mid_level_action_embed[ml_agent_id]

            # 把高层智能体对应的中层智能体obs拼接形成高层智能体的obs
            hl_agent_id = ml_agent_to_hl_agent(ml_agent_id)
            hl_agent_obs[hl_agent_id][SampleBatch.OBS] += t_obs[SampleBatch.OBS]
            # 上层智能体的初始mask
            hl_action_mask = [0 for _ in range(HIGH_LEVEL_ACT_SPACE)]
            hl_action_embed = np.zeros([HIGH_LEVEL_ACT_SPACE, HIGH_LEVEL_ACTION_EMBED])
            # hl_action_embed[0] = self.high_level_action_embed[hl_agent_id][0]
            for aac in self.high_level_init_avail_action:
                hl_action_mask[int(aac)] = 1
                hl_action_embed[int(aac)] = self.high_level_action_embed[hl_agent_id][int(aac)]
            hl_agent_obs[hl_agent_id]["action_mask"] = hl_action_mask
            hl_agent_obs[hl_agent_id]["avail_actions"] = hl_action_embed

        # 把高层智能体的init_obs添加进数据存储单元
        # for hl_agent_id, obs_dict in hl_agent_obs.items():
        #     LL_DATA_COLLECTOR[hl_agent_id].add_init_obs(obs_dict[ENV_STATE],
        #                                               self.high_level_steps,
        #                                               ret_ml, obs_dict[SampleBatch.OBS])
        obs = {}
        obs.update(low_level_agent_obs)
        obs.update(ml_agent_obs)
        obs.update(hl_agent_obs)

        return obs


class SCEnv(MultiAgentEnv):
    def __init__(self, env_config):
        self.steps = 0
        self.mozi_env = MoziEnv(env_config)  # 直接和墨子交互
        self.high_level_qmix_env = HighLevelEnv(self.mozi_env)

        self.groups = GROUPS
        self.agent_id_to_group = {}
        for group_id, agent_ids in self.groups.items():
            for agent_id in agent_ids:
                if agent_id in self.agent_id_to_group:
                    raise ValueError(
                        "Agent id {} is in multiple groups".format(
                            agent_id, self.groups))
                self.agent_id_to_group[agent_id] = group_id

    def step(self, action_dict):
        self.steps += 1
        # print(f'NCCEnv: {action_dict}')
        # Ungroup and send actions
        action_dict = self._ungroup_items(action_dict)
        obs, rewards, dones, infos = self.high_level_qmix_env.step(action_dict)
        obs = self._padding(obs)

        # Apply grouping transforms to the env outputs
        obs = self._group_items(obs)
        rewards = self._group_items(
            rewards, agg_fn=lambda gvals: list(gvals.values()))
        dones = self._group_items(
            dones, agg_fn=lambda gvals: all(gvals.values()))
        infos = self._group_items(
            infos, agg_fn=lambda gvals: {GROUP_INFO: list(gvals.values())})

        # Aggregate rewards, but preserve the original values in infos
        for agent_id, rew in rewards.items():
            if isinstance(rew, list):
                rewards[agent_id] = sum(rew)
                if agent_id not in infos:
                    infos[agent_id] = {}
                infos[agent_id][GROUP_REWARDS] = rew

        return obs, rewards, dones, infos

    def reset(self):
        self.steps = 0
        # TODO 刚开局启动规则智能体，感知态势；之后再启动RL智能体。
        obs = self.high_level_qmix_env.reset()
        obs = self._padding(obs)
        grouped_obs = self._group_items(obs)
        return grouped_obs

    def _padding(self, obs):
        np_obs = {}
        for agent_id, item in obs.items():
            if 'hl_agent_' in agent_id:
                o = self._pad(item, SampleBatch.OBS, HIGH_LEVEL_OBS_SPACE)
                np_obs[agent_id] = {}
                np_obs[agent_id][SampleBatch.OBS] = o
                s = self._pad(item, ENV_STATE, HIGH_LEVEL_STATE_SPACE)
                np_obs[agent_id][ENV_STATE] = s

                np_obs[agent_id]["action_mask"] = np.array(item["action_mask"])
                np_obs[agent_id]["avail_actions"] = np.array(item["avail_actions"])
            elif 'ml_agent_' in agent_id:
                o = self._pad(item, SampleBatch.OBS, MID_LEVEL_OBS_SPACE)
                np_obs[agent_id] = {}
                np_obs[agent_id][SampleBatch.OBS] = o
                s = self._pad(item, ENV_STATE, MID_LEVEL_STATE_SPACE)
                np_obs[agent_id][ENV_STATE] = s

                np_obs[agent_id]["action_mask"] = np.array(item["action_mask"])
                np_obs[agent_id]["avail_actions"] = np.array(item["avail_actions"])

            elif 'll_agent_' in agent_id:
                np_obs[agent_id] = {}
                np_obs[agent_id][SampleBatch.OBS] = np.array(item[SampleBatch.OBS])
        return np_obs

    @staticmethod
    def _pad(item, index, space_len):
        if len(item[index]) < space_len:
            pad_len = space_len - len(item[index])
            i = np.array(item[index])
            # (1,2)表示在一维数组array前面填充1位，最后面填充2位
            #  constant_values=(0,2) 表示前面填充0，后面填充2
            i = np.pad(i, (0, pad_len), 'constant', constant_values=0.0)
            # np_obs[agent_id][SampleBatch.OBS] = i
            return i
        elif len(item[index]) == space_len:
            i = np.array(item[index])
            # np_obs[agent_id][SampleBatch.OBS] = i
            return i
        else:
            clip_len = len(item[index]) - space_len
            i = item[index][clip_len:]  # 取最近的几个obs和state
            # np_obs[agent_id][SampleBatch.OBS] = np.array(i)
            return np.array(i)

    def _ungroup_items(self, items):
        out = {}
        for agent_id, value in items.items():
            if agent_id in self.groups:
                assert len(value) == len(self.groups[agent_id]), \
                    (agent_id, value, self.groups)
                for a, v in zip(self.groups[agent_id], value):
                    out[a] = v
            else:
                out[agent_id] = value
        return out

    def _group_items(self, items, agg_fn=lambda gvals: list(gvals.values())):
        grouped_items = {}
        for agent_id, item in items.items():
            if agent_id in self.agent_id_to_group:
                group_id = self.agent_id_to_group[agent_id]
                if group_id in grouped_items:
                    continue  # already added
                group_out = OrderedDict()
                for a in self.groups[group_id]:
                    if a in items:
                        group_out[a] = items[a]
                    else:
                        raise ValueError(
                            "Missing member of group {}: {}: {}".format(
                                group_id, a, items))
                grouped_items[group_id] = agg_fn(group_out)
            else:
                grouped_items[agent_id] = item
        return grouped_items
