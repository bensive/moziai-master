# 时间 : 2021/09/14 14:09
# 作者 : 张志高
# 文件 : main_versus.py
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

"""
本案例目标：
1、熟悉智能体代码的一般结构
2、熟悉环境类，以及智能体客户端与墨子交互运行的一般流程
3、了解相关参数配置以及设置方法
4、了解仿真服务类MoziServer （mozi_server.py）, 熟悉该类中的send_and_recv、set_key_value、get_key_value方法
"""

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment
from mozi_ai_sdk.quick_start.utils import common

# 设置墨子安装目录下bin目录为MOZIPATH，程序会跟进路径自动启动墨子
os.environ['MOZIPATH'] = etc.MOZI_PATH

# ①创建环境类对象
# 环境类对象将仿真服务类中定义的方法串联起来，
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME_DEMO_01,
                  etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)

# ②
# 启动墨子服务端
# 通过gRPC连接墨子服务端，产生env.mozi_server对象
# 连接上墨子后，可以通过send_and_recv方法，发送指令
# 设置推进模式 SYNCHRONOUS
# 设置决策步长 DURATION_INTERVAL
env.start()

# ③
# 加载想定，产生env.scenario
# 设置推进速度 SIMULATE_COMPRESSION
# 初始化全局态势
# 将所有推演方对象静态化
env.scenario = env.reset()

red_side = env.scenario.get_side_by_name('红方')

flag = False

# env.is_done, 判断推演是否结束
while not env.is_done():
    if env.step_count == 0 and not flag:
        flag = True
        # 获取本方地空导弹中队对象
        facilities = red_side.get_facilities()
        ground_to_air_missile_squadron = common.get_obj_by_name(facilities, '地空导弹中队')

        # 获取敌方单元苏-34 型“鸭嘴兽”攻击机的探测目标对象
        # 获取所有探测目标对象字典
        contacts = red_side.get_contacts()
        # 从探测目标字典，通过探测目标名称获取探测目标对象
        enemy_airplane = common.get_obj_by_name(contacts, '苏-34 型“鸭嘴兽”攻击机')
        # 探测目标属性，strGuid
        enemy_airplane_guid = enemy_airplane.strGuid

        # 获取武器“MIM-104B型“爱国者-1”防空导弹”的数据库GUID
        # 获取单元的所有武器的guid列表
        weapon_db_guids = ground_to_air_missile_squadron.get_weapon_db_guids()
        # 通过武器dbid, 得到武器的db guid
        # 1152为“MIM-104B型“爱国者-1”防空导弹”的dbid
        # 可以通过数据库浏览获取
        weapon_db_guid = [j for j in weapon_db_guids if '1152' in j][0]

        # 手动攻击
        ground_to_air_missile_squadron.manual_attack(enemy_airplane.strGuid, weapon_db_guid, 4)
    else:
        # ④
        # 下一步，更新态势
        # 仿真向前推进一个决策步长
        # 更新态势信息
        # 所有推演方对象静态更新
        env.step()

