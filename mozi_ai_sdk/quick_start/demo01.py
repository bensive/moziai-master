# 时间 : 2021/09/14 14:09
# 作者 : 张志高
# 文件 : main_versus.py
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment
from mozi_ai_sdk.quick_start.utils import common

# 设置墨子安装目录下bin目录为MOZIPATH，程序会跟进路径自动启动墨子
os.environ['MOZIPATH'] = etc.MOZI_PATH

# 创建环境类对象
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME_DEMO_01,
                  etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)

# 启动墨子服务端
# 通过gRPC连接墨子服务端，产生env.mozi_server对象
# 设置推进模式 SYNCHRONOUS
# 设置决策步长 DURATION_INTERVAL
env.start()

# 加载想定，产生env.scenario
# 设置推进速度 SIMULATE_COMPRESSION
# 初始化全局态势
env.scenario = env.reset()

red_side = env.scenario.get_side_by_name('红方')

flag = False
while not env.is_done():
    if env.step_count == 0 and not flag:
        flag = True
        # 获取本方地空导弹中队对象
        facilities = red_side.get_facilities()
        ground_to_air_missile_squadron = common.get_obj_by_name(facilities, '地空导弹中队')

        # 获取敌方单元苏-34 型“鸭嘴兽”攻击机的探测目标对象
        contacts = red_side.get_contacts()
        enemy_airplane = common.get_obj_by_name(contacts, '苏-34 型“鸭嘴兽”攻击机')
        enemy_airplane_guid = enemy_airplane.strGuid

        # 获取武器“MIM-104B型“爱国者-1”防空导弹”的数据库GUID
        weapon_db_guids = ground_to_air_missile_squadron.get_weapon_db_guids()
        weapon_db_guid = [j for j in weapon_db_guids if '1152' in j][0]

        # 手动攻击
        ground_to_air_missile_squadron.manual_attack(enemy_airplane.strGuid, weapon_db_guid, 1)
    else:
        # 下一步，更新态势
        env.step()
