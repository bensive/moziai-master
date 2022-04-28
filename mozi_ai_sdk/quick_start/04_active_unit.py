# 时间 : 2021/09/26 16:40
# 作者 : 张志高
# 文件 : 05_active_unit
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment
from mozi_ai_sdk.quick_start.utils import common

"""
本案例目标：
1、掌握活动单元对象的使用
2、本案例相关接口文件
    activeunit.py CActiveUnit
    aircraft.py CAircraft
    facility.py CFacility
    satellite.py CSatellite
    ship.py CShip
    submarine.py CSubmarine
"""

os.environ['MOZIPATH'] = etc.MOZI_PATH
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME_DEMO_05,
                  etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)
env.start()
env.scenario = env.reset()
red_side = env.scenario.get_side_by_name('红方')

# 获取机场内飞机对象
aircrafts = red_side.get_aircrafts()
aircraft_6 = common.get_obj_by_name(aircrafts, f'F-16A #6')
aircraft_7 = common.get_obj_by_name(aircrafts, f'F-16A #7')
aircraft_8 = common.get_obj_by_name(aircrafts, f'F-16A #8')

# 设置F16A #6单机出动
aircraft_6.set_single_out()
# 编组出动
unit_list = [aircraft_7.strGuid, aircraft_8.strGuid]
red_side.air_group_out(unit_list)
# 终止出动
aircraft_7.abort_launch()
aircraft_8.abort_launch()

while not aircraft_6.strActiveUnitStatus == '状态: 未分配任务 (在空)':
    # '状态: 未分配任务 (正在滑行准备起飞)'
    # '状态: 未分配任务 (正在起飞)'
    # '状态: 未分配任务 (在空)'
    env.step()

# 航线规划
course_list = [(37.0398991935271, 122.958786299026), (37.3926884324471, 123.618312576662),
               (37.6447756693682, 124.107738263721)]
aircraft_6.plot_course(course_list)

# 删除第2个航路点(从0开始计数)
aircraft_6.delete_coursed_point([2])


# 设置单元雷达、声纳、干扰机开机
aircraft_6.switch_sensor(radar='true', sonar='true', oecm='true')

# 设置单元是否遵循电磁管控
aircraft_6.unit_obeys_emcon('false')
# 设置雷达开机
aircraft_6.set_radar_shutdown('false')
# 设置声纳开机
aircraft_6.set_sonar_shutdown('false')
# 设置干扰机开机
aircraft_6.set_oecm_shutdown('false')

# 航路点设置雷达、声纳、主动ECM开机
aircraft_6.set_way_point_sensor(0, 'CB_radar', 'Checked')
aircraft_6.set_way_point_sensor(0, 'CB_Sonar', 'Checked')
aircraft_6.set_way_point_sensor(0, 'CB_ECM', 'Checked')

env.step()

# 设置期望速度
aircraft_6.set_desired_speed(900)
# # 设置单元期望高度
aircraft_6.set_desired_height(8000, 'true')

for i in range(17):
    env.step()

# 手动攻击
weapon_db_guid = 'hsfw-dataweapon-00000000000816'
contacts = red_side.get_contacts()
enemy_ship = common.get_obj_by_name(contacts, '舰船1')
enemy_ship_guid = enemy_ship.strGuid
aircraft_6.allocate_weapon_to_target(enemy_ship_guid, weapon_db_guid, 1)

while not red_side.get_weapons():
    env.step()

# 选择新基地
facilities = red_side.get_facilities()
airport = common.get_obj_by_name(facilities, '机场2')
aircraft_6.select_new_base(airport.strGuid)
# 返回基地
aircraft_6.return_to_base()

while not env.is_done():
    env.step()





