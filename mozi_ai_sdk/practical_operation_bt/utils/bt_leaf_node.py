# 时间 : 2021/10/08 9:37
# 作者 : 张志高
# 文件 : bt_leaf_node
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from mozi_ai_sdk.practical_operation_bt.utils import common
from mozi_utils import geo
from mozi_ai_sdk.practical_operation_bt.env import etc


def create_support_mission(side_name, scenario):
    side = scenario.get_side_by_name(side_name)
    support_mission = side.get_missions_by_name('预警机支援任务')
    if not support_mission:
        # 创建预警机支援任务
        # 添加参考点
        side.add_reference_point('预警机支援-1', 21.4930884112519, 121.427690179311)
        side.add_reference_point('预警机支援-2', 21.8231037592407, 121.908977165728)
        point_list = ['预警机支援-1', '预警机支援-2']
        mission_support = side.add_mission_support('预警机支援任务', point_list)

        # 设置支援任务飞机
        aircrafts = side.get_aircrafts()
        aircraft = common.get_obj_by_name(aircrafts, 'E-2K #1')
        mission_support.assign_unit(aircraft.strGuid)
        # 设置任务激活
        mission_support.set_is_active('true')
        # 设置遵循1/3规则
        mission_support.set_one_third_rule('false')
        # 设置仅一次
        mission_support.set_one_time_only('true')

        # 设置任务在阵位上打开电磁辐射
        mission_support.set_emcon_usage('true')

        # 编队规模
        mission_support.set_flight_size(1)
        mission_support.set_flight_size_check('false')

        # 出航油门-巡航
        mission_support.set_throttle_transit('Cruise')
        # 阵位油门-低速
        mission_support.set_throttle_station('Loiter')
    else:
        mission_support_doctrine = support_mission.get_doctrine()
        mission_support_doctrine.set_em_control_status('Radar', 'Active')
    return True


def update_support_mission(side_name, scenario):
    side = scenario.get_side_by_name(side_name)
    # 设置支援任务飞机
    aircrafts = side.get_aircrafts()
    aircraft_ea = common.get_obj_by_name(aircrafts, 'EC-130H #1')
    aircraft_ew = common.get_obj_by_name(aircrafts, 'E-2K #1')

    contacts = side.get_contacts()
    enemy_fight_aircraft = common.get_obj_by_name_in(contacts, '米格')
    # 如果本方电子战飞机存活
    if aircraft_ea:
        # 如果没有探测到对方米格
        if not enemy_fight_aircraft:
            if int(scenario.m_Time) - etc.SCENARIO_START_TIME > 120 * 60:
                side.set_reference_point('预警机支援-1', 21.1895046301962, 122.507983623636)
                side.set_reference_point('预警机支援-2', 21.1895046301962, 122.557983623636)
    else:
        if aircraft_ew:
            aircraft_ew.set_throttle(3)
            aircraft_ew_doctrine = aircraft_ew.get_doctrine()
            aircraft_ew_doctrine.set_em_control_status('Radar', 'Passive')
            aircraft_ew.return_to_base()
    return True


def create_patrol_mission(side_name, scenario):
    side = scenario.get_side_by_name(side_name)
    # 创建电子战机巡逻任务
    patrol_mission = side.get_missions_by_name('电子战机巡逻')
    if not patrol_mission:
        # 创建电子战机巡逻任务
        # 添加参考点
        latitude = 20.7183754855534
        longitude = 123.037810838717
        side.add_reference_point('电子战机巡逻-1', latitude + 0.3, longitude - 0.3)
        side.add_reference_point('电子战机巡逻-2', latitude + 0.3, longitude + 0.3)
        side.add_reference_point('电子战机巡逻-3', latitude - 0.3, longitude + 0.3)
        side.add_reference_point('电子战机巡逻-4', latitude - 0.3, longitude - 0.3)
        point_list = ['电子战机巡逻-1', '电子战机巡逻-2', '电子战机巡逻-3', '电子战机巡逻-4']
        patrol_mission = side.add_mission_patrol('电子战机巡逻', 0, point_list)

        # 设置任务单元
        aircrafts = side.get_aircrafts()
        aircraft = common.get_obj_by_name(aircrafts, 'EC-130H #1')
        patrol_mission.assign_unit(aircraft.strGuid)
        # aircraft_2 = common.get_obj_by_name(aircrafts, 'EC-130H #2')
        # patrol_mission.assign_unit(aircraft_2.strGuid)

        # 设置任务激活
        patrol_mission.set_is_active('true')
        # 设置遵循1/3规则
        patrol_mission.set_one_third_rule('false')

        # 编队规模
        patrol_mission.set_flight_size(1)
        patrol_mission.set_flight_size_check('false')

        # 设置任务启动时间
        patrol_mission.set_start_time('2021-05-26 11:25:00')

        # 设置任务是否对巡逻区外的探测目标进行分析
        patrol_mission.set_opa_check('false')

        # 设置任务是否对武器射程内探测目标进行分析
        patrol_mission.set_wwr_check('false')
    else:
        patrol_mission_doctrine = patrol_mission.get_doctrine()
        patrol_mission_doctrine.set_em_control_status('Radar', 'Passive')
        patrol_mission_doctrine.set_em_control_status('OECM', 'Active')
    return True


def create_strike_mission_1(side_name, scenario):
    side = scenario.get_side_by_name(side_name)
    sea_strike_mission = side.get_missions_by_name('对海打击_1')
    if not sea_strike_mission:
        # 延迟2小时打击任务
        # 创建对海突击任务
        sea_strike_mission = side.add_mission_strike('对海打击_1', 2)

        aircrafts = side.get_aircrafts()
        # 设置打击任务飞机
        for i in range(1, 7, 1):
            aircraft = common.get_obj_by_name(aircrafts, f'F-16A #0{i}')
            sea_strike_mission.assign_unit(aircraft.strGuid)

        # 设置仅考虑计划目标
        sea_strike_mission.set_preplan('false')

        # 设置任务启用时间
        sea_strike_mission.set_start_time('2021-05-26 12:55:00')

        # 编队规模
        sea_strike_mission.set_flight_size(6)
        sea_strike_mission.set_flight_size_check('false')

        # 出航航线
        sea_strike_mission.add_plan_way_to_mission(0, '航线3')
        # 返航航线
        sea_strike_mission.add_plan_way_to_mission(2, '航线3')

        # 设置打击任务仅限一次
        sea_strike_mission.set_strike_one_time_only('true')
    else:
        if not len(sea_strike_mission.get_targets()) == 2:
            # 设置打击目标
            contacts = side.get_contacts()
            enemy_ship = common.get_obj_by_name_in(contacts, '护卫舰')
            enemy_ship_2 = common.get_obj_by_name_in(contacts, '航空母舰')
            if enemy_ship:
                enemy_ship_guid = enemy_ship.strGuid
                sea_strike_mission.assign_unit_as_target(enemy_ship_guid)
            if enemy_ship_2:
                enemy_ship_2_guid = enemy_ship_2.strGuid
                sea_strike_mission.assign_unit_as_target(enemy_ship_2_guid)
    return True


def create_strike_mission_2(side_name, scenario):
    side = scenario.get_side_by_name(side_name)
    sea_strike_mission = side.get_missions_by_name('对海打击_2')
    if not sea_strike_mission:
        # 延迟2小时打击任务
        # 创建对海突击任务
        sea_strike_mission = side.add_mission_strike('对海打击_2', 2)

        aircrafts = side.get_aircrafts()
        # 设置打击任务飞机
        for i in range(1, 7, 1):
            aircraft = common.get_obj_by_name(aircrafts, f'F-16A #{i}')
            sea_strike_mission.assign_unit(aircraft.strGuid)

        # 设置仅考虑计划目标
        sea_strike_mission.set_preplan('false')

        # 设置任务启用时间
        sea_strike_mission.set_start_time('2021-05-26 12:55:00')

        # 编队规模
        sea_strike_mission.set_flight_size(6)
        sea_strike_mission.set_flight_size_check('false')

        # 出航航线
        sea_strike_mission.add_plan_way_to_mission(0, '航线3')
        # 返航航线
        sea_strike_mission.add_plan_way_to_mission(2, '航线3')

        # 设置打击任务仅限一次
        sea_strike_mission.set_strike_one_time_only('true')
    else:
        if not len(sea_strike_mission.get_targets()) == 2:
            # 设置打击目标
            contacts = side.get_contacts()
            enemy_ship = common.get_obj_by_name_in(contacts, '护卫舰')
            enemy_ship_2 = common.get_obj_by_name_in(contacts, '航空母舰')
            if enemy_ship:
                enemy_ship_guid = enemy_ship.strGuid
                sea_strike_mission.assign_unit_as_target(enemy_ship_guid)
            if enemy_ship_2:
                enemy_ship_2_guid = enemy_ship_2.strGuid
                sea_strike_mission.assign_unit_as_target(enemy_ship_2_guid)
    return True


def set_side_doctrine(side_name, scenario):
    side = scenario.get_side_by_name(side_name)
    doctrine = side.get_doctrine()
    # 如果推演方条令已设置，返回True
    if doctrine.m_WCS_Surface == 0:
        return True

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
    doctrine.set_em_control_status('Radar', 'Passive')
    doctrine.set_em_control_status('Sonar', 'Passive')
    doctrine.set_em_control_status('OECM', 'Passive')

    # AGM-84L 反舰
    # 未知类型
    doctrine.set_weapon_release_authority('816', '2999', 'max', 'max', 'max', 'none', 'false')
    # 未指明
    doctrine.set_weapon_release_authority('816', '3000', 'max', 'max', 'max', 'none', 'false')
    # 航母
    doctrine.set_weapon_release_authority('816', '3001', 'max', 'max', 'max', 'none', 'false')
    doctrine.set_weapon_release_authority('816', '3002', 'max', 'max', 'max', 'none', 'false')
    doctrine.set_weapon_release_authority('816', '3003', 'max', 'max', 'max', 'none', 'false')
    doctrine.set_weapon_release_authority('816', '3004', 'max', 'max', 'max', 'none', 'false')

    # 护卫舰
    doctrine.set_weapon_release_authority('816', '3103', 'none', 'none', 'max', 'none', 'false')
    # 驱逐舰
    doctrine.set_weapon_release_authority('816', '3104', 'none', 'none', 'max', 'none', 'false')

    # AIM-120C 中程空空导弹
    # 不明
    doctrine.set_weapon_release_authority('718', '1999', '1', '1', 'max', 'none', 'false')
    # 飞机
    doctrine.set_weapon_release_authority('718', '2000', '2', '1', 'max', 'none', 'false')
    # 五代机
    doctrine.set_weapon_release_authority('718', '2001', '2', '1', 'max', 'none', 'false')
    # 四代机
    doctrine.set_weapon_release_authority('718', '2002', '2', '1', 'max', 'none', 'false')
    # 电子战机
    doctrine.set_weapon_release_authority('718', '2021', '1', '1', 'max', 'none', 'false')
    # 预警机
    doctrine.set_weapon_release_authority('718', '2031', '1', '1', 'max', 'none', 'false')
    # 直升机
    doctrine.set_weapon_release_authority('718', '2100', '1', '1', 'max', 'none', 'false')
    # 导弹
    doctrine.set_weapon_release_authority('718', '2200', 'none', '1', 'max', 'none', 'false')

    return True


def ecm(side_name, scenario):
    # 伴随干扰
    side = scenario.get_side_by_name(side_name)
    aircrafts = side.get_aircrafts()
    ea_1 = common.get_obj_by_name(aircrafts, 'EC-130H #1')
    if ea_1:
        ea_1_status = ea_1.get_status_type()
        f_16A_1_name_list = ['F-16A #7', 'F-16A #8', 'F-16A #9']
        group_1 = common.get_group(side, f_16A_1_name_list)
        f_16A_2_name_list = ['F-16A #07', 'F-16A #08', 'F-16A #09']
        group_2 = common.get_group(side, f_16A_2_name_list)
        if group_1:
            etc.flag_3 = True
        if not group_1 and not group_2 and etc.flag_1 and etc.flag_2 and etc.flag_3:
            ea_1.set_throttle(3)
            ea_1.return_to_base()
            ea_1_doctrine = ea_1.get_doctrine()
            ea_1_doctrine.set_em_control_status('OECM', 'Active')
        if group_1:
            group_1.plot_course([(ea_1.dLatitude - 0.4, ea_1.dLongitude + 0.3)])
        if ea_1_status == 'InAir' and not etc.flag_1:
            etc.flag_1 = True
            air_group_out(side, f_16A_1_name_list)
        if group_2:
            group_2.plot_course([(ea_1.dLatitude - 0.4, ea_1.dLongitude + 0.3)])
        if ea_1_status == 'InAir' and not etc.flag_2:
            etc.flag_2 = True
            air_group_out(side, f_16A_2_name_list)
    return False


def air_group_out(side, unit_name_list):
    guid_list = []
    aircrafts = side.aircrafts
    for name in unit_name_list:
        aircraft = common.get_obj_by_name(aircrafts, name)
        guid_list.append(aircraft.strGuid)
    if guid_list:
        side.air_group_out(guid_list)

