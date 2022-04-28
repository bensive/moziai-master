
# 时间 : 2021/09/26 15:49
# 作者 : 张志高
# 文件 : 04_support_mission
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

"""
本案例目标：
1、掌握支援任务的创建和常用设置
2、本案例相关接口文件
    side.py  CSide 推演方
    sideway.py CSideWay预设航线类
    mission.py CMission 提供多数任务通用方法
    mssnsupport.py CSupportMission 支援任务类
3、其他任务接口文件
    mssncargo.py
    mssnferry.py
    mssnmining.py
    mssnmnclrng.py
"""

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment
from mozi_ai_sdk.quick_start.utils import common


os.environ['MOZIPATH'] = etc.MOZI_PATH
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME_DEMO_04,
                  etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)
env.start()
env.scenario = env.reset()

red_side = env.scenario.get_side_by_name('红方')

flag = False
while not env.is_done():
    if env.step_count == 0 and not flag:
        flag = True

        # 添加参考点
        point_1 = red_side.add_reference_point('RP-1', 37.482920555205, 123.362532042046)
        point_2 = red_side.add_reference_point('RP-2', 37.1244585650515, 123.211235946129)

        # 根据参考点创建支援任务
        point_list = ['RP-1', 'RP-2']
        mission_support = red_side.add_mission_support('支援任务', point_list)

        # 设置任务飞机
        aircrafts = red_side.get_aircrafts()
        for i in range(1, 4, 1):
            aircraft = common.get_obj_by_name(aircrafts, f'侦察机 #{i}')
            mission_support.assign_unit(aircraft.strGuid)

        # 任务是否激活
        mission_support.set_is_active('true')

        # 设置任务启用时间和失效时间
        mission_support.set_start_time('2021-09-26 15:55:00')
        mission_support.set_end_time('2021-09-26 19:55:00')

        # 阵位上每类平台保持几个作战单元
        mission_support.set_maintain_unit_number(2)

        # 设置遵循1/3规则
        mission_support.set_one_third_rule('true')

        # 设置仅一次
        mission_support.set_one_time_only('true')

        # 设置任务是否在阵位上打开电磁辐射
        mission_support.set_emcon_usage('true')

        # 设置导航类型-仅一次 -- 暂不可用
        mission_support.set_loop_type('onceRepeat')

        # 编队规模
        mission_support.set_flight_size(3)
        mission_support.set_flight_size_check('true')

        # 空中加油-设置不允许空中加油
        mission_support.set_use_refuel_unrep(1)

        # 设置出航返航航线
        # red_side.add_plan_way(0, '单元航线-出航')
        # red_side.add_plan_way(0, '单元航线-返航')
        # 出航航线
        mission_support.add_plan_way_to_mission(0, '单元航线-出航')
        # 返航航线
        mission_support.add_plan_way_to_mission(2, '单元航线-返航')

        # 出航油门-军用
        mission_support.set_throttle_transit('Full')
        # 阵位油门-巡航
        mission_support.set_throttle_station('Cruise')
        # 出航高度
        mission_support.set_transit_altitude(1000)
        # 阵位高度
        mission_support.set_station_altitude(2000)
    else:
        # 下一步，更新态势
        env.step()
