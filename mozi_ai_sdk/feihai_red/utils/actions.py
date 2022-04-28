# 时间 : 2021/09/29 12:23
# 作者 : 张志高
# 文件 : actions
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from mozi_ai_sdk.practical_operation_bt.utils import common


def create_support_mission_1(side):
    mission = side.get_missions_by_name('预警机支援')
    if not mission:
        latitude = 18.8523362636137
        longitude = 123.085123300477
        side.add_reference_point('预警机支援-1', latitude + 0.3, longitude - 0.3)
        side.add_reference_point('预警机支援-2', latitude + 0.3, longitude + 0.3)
        side.add_reference_point('预警机支援-3', latitude - 0.3, longitude + 0.3)
        side.add_reference_point('预警机支援-4', latitude - 0.3, longitude - 0.3)
        point_list = ['预警机支援-1', '预警机支援-2', '预警机支援-3', '预警机支援-4']
        mission = side.add_mission_support('预警机支援', point_list)

        # 设置支援任务飞机
        aircrafts = side.get_aircrafts()
        aircraft = common.get_obj_by_name(aircrafts, '卡-29 #7')
        mission.assign_unit(aircraft.strGuid)
        aircraft = common.get_obj_by_name(aircrafts, '卡-29 #8')
        mission.assign_unit(aircraft.strGuid)
        # 设置任务激活
        mission.set_is_active('true')
        # 设置遵循1/3规则
        mission.set_one_third_rule('false')
        # 设置仅一次
        mission.set_one_time_only('true')

        # 设置任务在阵位上打开电磁辐射
        mission.set_emcon_usage('true')

        # 编队规模
        mission.set_flight_size(1)
        mission.set_flight_size_check('false')

        # 出航油门-巡航
        mission.set_throttle_transit('Cruise')
        # 阵位油门-低速
        mission.set_throttle_station('Loiter')
    else:
        mission_doctrine = mission.get_doctrine()
        mission_doctrine.set_em_control_status('Radar', 'Active')


def create_support_mission_2(side):
    mission = side.get_missions_by_name('预警机支援二')
    if not mission:
        latitude = 20.2360321740537
        longitude = 124.785340974703
        side.add_reference_point('预警机支援-5', latitude + 0.3, longitude - 0.3)
        side.add_reference_point('预警机支援-6', latitude + 0.3, longitude + 0.3)
        side.add_reference_point('预警机支援-7', latitude - 0.3, longitude + 0.3)
        side.add_reference_point('预警机支援-8', latitude - 0.3, longitude - 0.3)
        point_list = ['预警机支援-5', '预警机支援-6', '预警机支援-7', '预警机支援-8']
        mission = side.add_mission_support('预警机支援二', point_list)

        # 设置支援任务飞机
        aircrafts = side.get_aircrafts()
        aircraft = common.get_obj_by_name(aircrafts, '卡-29 #9')
        mission.assign_unit(aircraft.strGuid)
        aircraft = common.get_obj_by_name(aircrafts, '卡-29 #10')
        mission.assign_unit(aircraft.strGuid)
        # 设置任务激活
        mission.set_is_active('true')
        # 设置遵循1/3规则
        mission.set_one_third_rule('false')
        # 设置仅一次
        mission.set_one_time_only('true')

        # 设置任务在阵位上打开电磁辐射
        mission.set_emcon_usage('true')

        # 编队规模
        mission.set_flight_size(1)
        mission.set_flight_size_check('false')

        # 出航油门-巡航
        mission.set_throttle_transit('Cruise')
        # 阵位油门-低速
        mission.set_throttle_station('Loiter')
    else:
        mission_doctrine = mission.get_doctrine()
        mission_doctrine.set_em_control_status('Radar', 'Active')


def create_patrol_mission(side):
    # 创建空战飞机巡逻任务
    mission = side.get_missions_by_name('空战飞机巡逻')
    if not mission:
        # 创建空战飞机巡逻任务
        # 添加参考点
        latitude = 19.8023794121797
        longitude = 123.939122860794
        side.add_reference_point('空战飞机巡逻-1', latitude + 0.6, longitude - 0.6)
        side.add_reference_point('空战飞机巡逻-2', latitude + 0.6, longitude + 0.6)
        side.add_reference_point('空战飞机巡逻-3', latitude - 0.6, longitude + 0.6)
        side.add_reference_point('空战飞机巡逻-4', latitude - 0.6, longitude - 0.6)
        point_list = ['空战飞机巡逻-1', '空战飞机巡逻-2', '空战飞机巡逻-3', '空战飞机巡逻-4']
        mission = side.add_mission_patrol('空战飞机巡逻', 0, point_list)

        # 设置任务单元
        aircrafts = side.get_aircrafts()
        for i in range(6):
            i += 1
            aircraft = common.get_obj_by_name(aircrafts, f'米格-29 #{i}')
            mission.assign_unit(aircraft.strGuid)

        # 设置任务激活
        mission.set_is_active('true')
        # 设置遵循1/3规则
        mission.set_one_third_rule('true')

        # 编队规模
        mission.set_flight_size(1)
        mission.set_flight_size_check('false')

        # 设置任务启动时间
        # patrol_mission.set_start_time('2021-05-26 11:25:00')

        # 设置任务是否对巡逻区外的探测目标进行分析
        mission.set_opa_check('false')

        # 设置任务是否对武器射程内探测目标进行分析
        mission.set_wwr_check('false')
    else:
        mission_doctrine = mission.get_doctrine()
        mission_doctrine.set_em_control_status('Radar', 'Active')
        mission_doctrine.set_em_control_status('OECM', 'Active')


def create_strike_mission(side):
    mission = side.get_missions_by_name('对空拦截')
    if not mission:
        # 对空拦截
        mission = side.add_mission_strike('对空拦截', 0)

        aircrafts = side.get_aircrafts()
        # 设置打击任务飞机
        for i in range(7, 11, 1):
            aircraft = common.get_obj_by_name(aircrafts, f'米格-29 #{i}')
            mission.assign_unit(aircraft.strGuid)

        # 设置仅考虑计划目标
        mission.set_preplan('false')

        # 编队规模
        mission.set_flight_size(2)
        mission.set_flight_size_check('false')

        # 设置打击任务仅限一次
        mission.set_strike_one_time_only('false')
    else:
        pass


def set_side_doctrine(side):
    doctrine = side.get_doctrine()
    # 设置对海对空自由开火
    doctrine.set_weapon_control_status_surface(0)
    doctrine.set_weapon_control_status_air(0)

    # 进攻忽略计划航线
    doctrine.ignore_plotted_course('yes')

    # Bingo燃油返航
    doctrine.set_fuel_state_for_aircraft('Bingo')
    # 编队中任意一架飞机达到单机油料状态要返航时，其可离队返航
    doctrine.set_fuel_state_for_air_group('YesLeaveGroup')

    # 武器状态
    # 所有超视距与防区外打击武器已经耗光.立即脱离战斗
    doctrine.set_weapon_state_for_aircraft(3001)
    doctrine.set_weapon_state_for_air_group('YesLeaveGroup')

    # 电磁管控
    doctrine.set_em_control_status('Radar', 'Active')
    doctrine.set_em_control_status('Sonar', 'Active')
    doctrine.set_em_control_status('OECM', 'Active')


