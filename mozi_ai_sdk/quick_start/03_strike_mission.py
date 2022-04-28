# 时间 : 2021/09/18 14:25
# 作者 : 张志高
# 文件 : demo02
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

"""
本案例目标：
1、掌握打击任务的创建和常用设置
2、本案例相关接口文件
    side.py  CSide 推演方
    contacts.py CContacts 探测目标类
    sideway.py CSideWay预设航线类
    mission.py CMission 提供多数任务通用方法
    mssnstrike.py CStrikeMission 打击任务类
"""

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment
from mozi_ai_sdk.quick_start.utils import common


os.environ['MOZIPATH'] = etc.MOZI_PATH
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME_DEMO_03,
                  etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)
env.start()
env.scenario = env.reset()

red_side = env.scenario.get_side_by_name('红方')

flag = False
while not env.is_done():
    if env.step_count == 0 and not flag:
        flag = True

        # 创建对海突击任务
        sea_strike_mission = red_side.add_mission_strike('对海打击', 2)

        aircrafts = red_side.get_aircrafts()
        # 设置打击任务飞机
        for i in range(6, 11, 1):
            aircraft = common.get_obj_by_name(aircrafts, f'F-16A #{i}')
            sea_strike_mission.assign_unit(aircraft.strGuid)

        # 设置护航飞机
        for i in range(5):
            i += 1
            aircraft = common.get_obj_by_name(aircrafts, f'F-16A #{i}')
            sea_strike_mission.assign_unit(aircraft.strGuid, 'true')

        # 设置打击目标
        contacts = red_side.get_contacts()
        enemy_ship = common.get_obj_by_name(contacts, '舰船1')
        enemy_ship_guid = enemy_ship.strGuid
        sea_strike_mission.assign_unit_as_target(enemy_ship_guid)
        # 设置仅考虑计划目标
        sea_strike_mission.set_preplan('true')

        ############################################################

        # 任务是否激活
        sea_strike_mission.set_is_active('true')

        # 设置任务启用时间和失效时间
        sea_strike_mission.set_start_time('2021-09-23 9:30:00')
        sea_strike_mission.set_end_time('2021-09-23 13:10:00')

        # 设置打击任务触发条件, 探测目标至少为不明、非友、敌对
        sea_strike_mission.set_minimum_trigger(4)

        # 编队规模
        sea_strike_mission.set_flight_size(3)
        sea_strike_mission.set_flight_size_check('true')

        # 燃油、弹药设置
        # 设置如果不能打击目标，则带回空对地弹药
        sea_strike_mission.set_fuel_ammo(2)

        # 设置打击任务设置打击任务所需最少就绪飞机数（编队数）
        sea_strike_mission.set_min_aircrafts_required(1)

        # 设置任务细节：任务允许出动的最大飞行批次
        sea_strike_mission.set_strike_max(3)

        # 最小打击半径-单位海里
        sea_strike_mission.set_min_strike_radius(30)
        # 最大打击半径-单位海里
        sea_strike_mission.set_max_strike_radius(1000)

        # 雷达运用：从进入攻击航线段到武器消耗完毕状态点打开雷达
        sea_strike_mission.set_radar_usage(3)

        # 空中加油-设置不允许空中加油
        sea_strike_mission.set_use_refuel_unrep(1)

        # 出航航线
        sea_strike_mission.add_plan_way_to_mission(0, '单元航线出航')
        # 返航航线
        sea_strike_mission.add_plan_way_to_mission(2, '单元航线返航')
        # 武器航线-需要巡航导弹，且路径点数不为0
        # 墨子web查看
        sea_strike_mission.add_plan_way_to_mission(1, '武器航线')

        # 设置打击任务是否离轴攻击
        sea_strike_mission.set_auto_planner('true')

        # 设置打击任务是否仅限一次
        sea_strike_mission.set_strike_one_time_only('true')

        # 设置打击任务护航最大威胁响应半径
        sea_strike_mission.set_strike_escort_response_radius(100)
        # 设置护航飞机的编队规模
        sea_strike_mission.set_strike_escort_flight_size_shooter(3)
    else:
        # 下一步，更新态势
        env.step()

