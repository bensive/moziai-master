# 时间 : 2021/09/18 14:25
# 作者 : 张志高
# 文件 : demo02
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment
from mozi_ai_sdk.quick_start.utils import common

# 设置墨子安装目录下bin目录为MOZIPATH，程序会跟进路径自动启动墨子
os.environ['MOZIPATH'] = etc.MOZI_PATH

# 创建环境类对象
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME_DEMO_02,
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
    """
    决策
    """
    if env.step_count == 0 and not flag:
        flag = True

        # 获取本方地空导弹中队对象
        facilities = red_side.get_facilities()
        airport = common.get_obj_by_name(facilities, '机场1')

        # 根据机场经纬度添加参考点
        point_1 = red_side.add_reference_point('参考点1', airport.dLatitude + 0.8, airport.dLongitude + 0.4)
        point_2 = red_side.add_reference_point('参考点2', airport.dLatitude + 0.8, airport.dLongitude + 0.8)
        point_3 = red_side.add_reference_point('参考点3', airport.dLatitude + 0.4, airport.dLongitude + 0.8)
        point_4 = red_side.add_reference_point('参考点4', airport.dLatitude + 0.4, airport.dLongitude + 0.4)
        # 根据参考点创建巡逻任务
        point_list = ['参考点1', '参考点2', '参考点3', '参考点4']
        air_portal_mission = red_side.add_mission_patrol('空战巡逻', 0, point_list)

        # 设置警戒区
        point_5 = red_side.add_reference_point('参考点5', airport.dLatitude + 1.0, airport.dLongitude + 0.2)
        point_6 = red_side.add_reference_point('参考点6', airport.dLatitude + 1.0, airport.dLongitude + 1.0)
        point_7 = red_side.add_reference_point('参考点7', airport.dLatitude + 0.2, airport.dLongitude + 1.0)
        point_8 = red_side.add_reference_point('参考点8', airport.dLatitude + 0.2, airport.dLongitude + 0.2)
        # 根据参考点创建巡逻任务
        prosecution_point_list = ['参考点5', '参考点6', '参考点7', '参考点8']
        air_portal_mission.set_prosecution_zone(prosecution_point_list)

        # 设置巡逻任务单元
        aircrafts = red_side.get_aircrafts()
        aircraft_1 = common.get_obj_by_name(aircrafts, '米格 #1')
        aircraft_2 = common.get_obj_by_name(aircrafts, '米格 #2')
        air_portal_mission.assign_unit(aircraft_1.strGuid)
        air_portal_mission.assign_unit(aircraft_2.strGuid)

        # 设置任务不起用
        air_portal_mission.set_is_active('false')

        # 设置任务启动时间和失效时间
        air_portal_mission.set_start_time('2021-09-18 23:10:00')
        air_portal_mission.set_end_time('2021-09-19 2:10:00')

        # 设置阵位上每类平台保存作战单元数量
        air_portal_mission.set_maintain_unit_number(2)

        # 设置任务是否对巡逻区外的探测目标进行分析
        air_portal_mission.set_opa_check('true')

        # 设置任务是否仅在巡逻/警戒区内打开电磁辐射
        air_portal_mission.set_emcon_usage('true')

        # 设置打击任务编队规模
        air_portal_mission.set_flight_size(2)
        # 设置打击任务是否飞机数低于编组规模数要求就不能起飞
        air_portal_mission.set_flight_size_check('true')

        # # 设置航线
        # self.red_side.add_plan_way(0, '单元航线-新')
        # # 出航航线
        # mission.add_plan_way_to_mission(0, '单元航线-新')
        # # 返航航线
        # mission.add_plan_way_to_mission(2, '单元航线-新')
        # # 巡逻航线
        # mission.add_plan_way_to_mission(3, '单元航线-新')

        # 设置任务的攻击距离
        air_portal_mission.set_attack_distance(50)

        # 设置不允许空中加油
        air_portal_mission.set_use_refuel_unrep(1)

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

    else:
        # 下一步，更新态势
        env.step()

