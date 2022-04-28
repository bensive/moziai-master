# 时间 : 2021/09/18 14:25
# 作者 : 张志高
# 文件 : demo02
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

"""
本案例目标：
1、掌握巡逻任务的创建和常用设置
2、掌握参考点的创建和设置
3、掌握航线的创建和设置
4、本案例相关接口文件
    side.py  CSide 推演方
    referencepoint.py CReferencePoint 参考点类
    mission.py CMission 提供多数任务通用方法
    mssnpatrol.py  CPatrolMission 提供巡逻任务的方法
    sideway.py CSideWay预设航线类
"""

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment
from mozi_ai_sdk.quick_start.utils import common

os.environ['MOZIPATH'] = etc.MOZI_PATH
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME_DEMO_02,
                  etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)
env.start()
env.scenario = env.reset()

red_side = env.scenario.get_side_by_name('红方')

flag = False
while not env.is_done():
    """
    决策
    """
    if env.step_count == 0 and not flag:
        flag = True

        # 获取本方机场
        facilities = red_side.get_facilities()
        airport = common.get_obj_by_name(facilities, '机场1')

        # 根据机场经纬度添加参考点
        point_1 = red_side.add_reference_point('参考点1', airport.dLatitude - 0.8, airport.dLongitude + 0.4)
        point_2 = red_side.add_reference_point('参考点2', airport.dLatitude - 0.8, airport.dLongitude + 0.8)
        point_3 = red_side.add_reference_point('参考点3', airport.dLatitude - 0.4, airport.dLongitude + 0.8)
        point_4 = red_side.add_reference_point('参考点4', airport.dLatitude - 0.4, airport.dLongitude + 0.4)

        # 根据参考点创建巡逻任务
        point_list = ['参考点1', '参考点2', '参考点3', '参考点4']
        # 返回的任务对象非态势获取，仅部分属性有效
        air_portal_mission = red_side.add_mission_patrol('空战巡逻', 0, point_list)
        # 新创建的任务，获取任务条令时返回None，需要更新态势后，重新从推演方对象中获取任务对象
        mission_doctrine = air_portal_mission.get_doctrine()
        env.step()
        air_portal_mission = red_side.get_missions_by_name('空战巡逻')
        mission_doctrine = air_portal_mission.get_doctrine()

        # 设置巡逻任务单元
        aircrafts = red_side.get_aircrafts()
        for i in range(4):
            i += 1
            aircraft = common.get_obj_by_name(aircrafts, f'米格 #{i}')
            air_portal_mission.assign_unit(aircraft.strGuid)

        ########################################################

        # 设置更新巡逻区，变更参考点列表
        point_list = ['参考点1', '参考点2', '参考点3']
        air_portal_mission.set_patrol_zone(point_list)

        # 修改参考点经纬度
        red_side.set_reference_point('参考点1', airport.dLatitude - 0.7, airport.dLongitude + 0.3)

        # 设置警戒区
        point_5 = red_side.add_reference_point('参考点5', airport.dLatitude - 1.0, airport.dLongitude + 0.2)
        point_6 = red_side.add_reference_point('参考点6', airport.dLatitude - 1.0, airport.dLongitude + 1.0)
        point_7 = red_side.add_reference_point('参考点7', airport.dLatitude - 0.2, airport.dLongitude + 1.0)
        point_8 = red_side.add_reference_point('参考点8', airport.dLatitude - 0.2, airport.dLongitude + 0.2)
        # 根据参考点创建巡逻任务
        prosecution_point_list = ['参考点5', '参考点6', '参考点7', '参考点8']
        air_portal_mission.set_prosecution_zone(prosecution_point_list)

        # 出航高度
        air_portal_mission.set_transit_altitude(1000)
        # 阵位高度
        air_portal_mission.set_station_altitude(2000)
        # 攻击高度
        air_portal_mission.set_attack_altitude(3000)

        # 出航油门-巡航
        air_portal_mission.set_throttle_transit('Full')
        # 阵位油门-全速
        air_portal_mission.set_throttle_station('Cruise')
        # 攻击油门-最大
        air_portal_mission.set_throttle_attack('Flank')

        # 设置任务的攻击距离，单位海里
        air_portal_mission.set_attack_distance(50)

        # 设置任务启用
        air_portal_mission.set_is_active('true')

        # 设置任务启动时间和失效时间
        air_portal_mission.set_start_time('2021-09-18 23:10:00')
        air_portal_mission.set_end_time('2021-09-19 3:50:00')

        # 设置打击任务编队规模
        air_portal_mission.set_flight_size(1)
        # 设置打击任务是否飞机数低于编组规模数要求就不能起飞
        air_portal_mission.set_flight_size_check('true')

        # 设置阵位上每类平台保存作战单元数量
        air_portal_mission.set_maintain_unit_number(1)

        # 设置遵循1/3规则，出动飞机数量为总飞机数/3，向上取整
        air_portal_mission.set_one_third_rule('true')

        # 设置任务是否对巡逻区外的探测目标进行分析
        air_portal_mission.set_opa_check('false')

        # 设置任务是否对武器射程内探测目标进行分析
        air_portal_mission.set_wwr_check('false')

        # 设置任务是否仅在巡逻/警戒区内打开电磁辐射
        air_portal_mission.set_emcon_usage('true')

        # 设置不允许空中加油
        # 该接口直接设置的任务条令
        air_portal_mission.set_use_refuel_unrep(1)

        # 设置航线
        # 添加航线：单元航线，武器航线
        red_side.add_plan_way(0, '出航航线')
        red_side.add_plan_way(0, '返航航线')
        red_side.add_plan_way(0, '巡逻航线')
        # 给航线添加航路点
        red_side.add_plan_way_point('出航航线', 128.465614876251, 26.671474736029)
        red_side.add_plan_way_point('出航航线', 128.887065012163, 26.5833293108848)
        red_side.add_plan_way_point('返航航线', 128.244808399628, 26.2561596899537)
        red_side.add_plan_way_point('返航航线', 128.117884730546, 26.644787386411)
        red_side.add_plan_way_point('巡逻航线', 128.714605112882, 26.0781801004785)
        red_side.add_plan_way_point('巡逻航线', 128.965734517005, 26.2415779306963)
        # 设置航线显隐
        red_side.set_plan_way_showing_status('出航航线', 'true')
        red_side.set_plan_way_showing_status('返航航线', 'true')
        red_side.set_plan_way_showing_status('巡逻航线', 'true')
        # 给任务添加出航航线
        air_portal_mission.add_plan_way_to_mission(0, '出航航线')
        # 给任务添加返航航线
        air_portal_mission.add_plan_way_to_mission(2, '返航航线')
        # 给任务添加巡逻航线
        air_portal_mission.add_plan_way_to_mission(3, '巡逻航线')
    else:
        # 下一步，更新态势
        env.step()

