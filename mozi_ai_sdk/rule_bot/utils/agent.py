# 时间 : 2021/4/12 11:33 
# 作者 :
# 文件 : agent.py 
# 说明 : 
# 项目 : moziai
# 版权 : 北京华戍防务技术有限公司
from mozi_simu_sdk.args import Throttle


def edit_side_doctrine(doctrine):
    # 对空自由攻击
    doctrine.set_weapon_control_status('weapon_control_status_air', 0)

    # 燃油规划bingo
    doctrine.set_fuel_state_for_aircraft('Bingo')

    # 燃油返航离开编队
    doctrine.set_fuel_state_for_air_group('YesLeaveGroup')

    # 武器规划超视距耗尽返航
    doctrine.set_weapon_state_for_aircraft('3001')

    # 武器返航离开编队
    doctrine.set_weapon_state_for_air_group('YesLeaveGroup')

    """
    总电磁
    """
    # 雷达静默
    doctrine.unit_obeys_emcon('false')  # 单元不遵循电磁管控，然后修改雷达，干扰等。
    doctrine.set_em_control_status('Radar', 'Active')

    # 干扰器静默
    doctrine.set_em_control_status('Sonar', 'Passive')

    # 声呐静默
    doctrine.set_em_control_status('OECM', 'Passive')

    """
    总武器
    """

    doctrine.set_weapon_release_authority('3413', '1999', '1', '1', '70', 'none', 'false')

    # 飞机
    doctrine.set_weapon_release_authority('3413', '2000', '1', '1', '70', 'none', 'false')

    # 五代机
    doctrine.set_weapon_release_authority('3413', '2001', '1', '1', '70', 'none', 'false')

    # 四代机
    doctrine.set_weapon_release_authority('3413', '2002', '1', '1', '70', 'none', 'false')

    # 预警机
    doctrine.set_weapon_release_authority('3413', '2031', '1', '1', '80', 'none', 'false')

    # 直升机
    doctrine.set_weapon_release_authority('3413', '2100', '0', '1', 'none', 'none', 'false')

    # 导弹
    doctrine.set_weapon_release_authority('3413', '2200', '0', '1', 'none', 'none', 'false')


def add_rp(side):
    # 画参考点，必须用浮点数，矩形
    patrol_area = []
    cordon_area = []
    reference_point1 = [(17.0, 111.0), (17.1, 113.0), (15.0, 113.0), (15.1, 111.0)]
    reference_point2 = [(18.0, 110.0), (18.1, 114.0), (14.0, 114.0), (14.1, 110.0)]
    name = 1
    while name < 5:
        for k in reference_point1:
            side.add_reference_point(str(name), k[0], k[1])
            patrol_area.append(str(name))
            name += 1
    while 4 < name < 9:
        for h in reference_point2:
            side.add_reference_point(str(name), h[0], h[1])
            cordon_area.append(str(name))
            name += 1
    return patrol_area, cordon_area


def edit_mission(patrol_mission, cordon_area):
    # 加警戒区
    patrol_mission.set_prosecution_zone(cordon_area)

    # 分配兵力
    patrol_mission.assign_unit('歼-16 #1', 'true')

    # 取消1/3规则
    patrol_mission.set_one_third_rule('true')

    # 对巡逻区外探测
    patrol_mission.set_opa_check('true')

    # 取消区内电磁
    patrol_mission.set_emcon_usage('true')

    # 射程内分析
    patrol_mission.set_wwr_check('true')

    # 编队规模单机
    patrol_mission.set_flight_size('1')

    # 低于规模起飞
    patrol_mission.set_flight_size_check(False)

    # 出航油门巡航,新版接口只需要输入相应的数字编号即可。
    patrol_mission.set_throttle_transit(Throttle.Cruise)

    # 阵位油门低速
    patrol_mission.set_throttle_station(Throttle.Loiter)

    # 攻击油门军用
    patrol_mission.set_throttle_attack(Throttle.Full)

    # 出航高度13000
    patrol_mission.set_transit_altitude(13000.1)

    # 阵位高度13000
    patrol_mission.set_station_altitude(13000.1)

    # 攻击高度默认


def edit_mission_doctrine(doctrine):
    # 交战规则
    doctrine.set_weapon_state_for_air_group('3')  # m_WeaponStateRTB
    doctrine.gun_strafe_for_aircraft('1')  # m_GunStrafeGroundTargets
    doctrine.set_fuel_state_for_air_group('0')  # m_BingoJokerRTB
    doctrine.set_weapon_control_status('weapon_control_status_subsurface', '0')
    doctrine.set_weapon_control_status('weapon_control_status_surface', '0')
    doctrine.set_weapon_control_status('weapon_control_status_land', '0')
    doctrine.set_weapon_control_status('weapon_control_status_air', '0')
    # 燃油返航一致
    doctrine.set_fuel_state_for_air_group('YesLeaveGroup')

    # 武器返航一致
    doctrine.set_weapon_state_for_air_group('YesLeaveGroup')

    """
    任务电磁
    """
    # 与上级一致
    doctrine.set_emcon_according_to_superiors('yes', 'false')


# 巡逻区域经纬度的生成
def create_patrol_zone(scenario):
    side = scenario.get_side_by_name('红方')
    contacts = side.contacts
    ships = side.ships
    point_list = []
    # 根据本方航空母舰的位置创建巡逻区xl1，xl2
    for k, v in ships.items():
        # lat: 纬度， lon：经度
        if '驱逐舰' in v.strName:
            lat, lon = v.dLatitude, v.dLongitude
            # xl1
            rp1 = side.add_reference_point('rp1', lat + 1.2, lon + 1)
            rp2 = side.add_reference_point('rp2', lat + 1, lon + 1.5)
            rp3 = side.add_reference_point('rp3', lat + 0.6, lon + 1)
            rp4 = side.add_reference_point('rp4', lat + 1, lon + 0.5)
            point_list.append([rp1, rp2, rp3, rp4])
    for k, v in contacts.items():
        # lat: 纬度， lon：经度
        if 'CVN' in v.strName:
            lat, lon = v.dLatitude, v.dLongitude
            # xl1
            rp11 = side.add_reference_point('rp11', lat + 1.2, lon + 1)
            rp21 = side.add_reference_point('rp21', lat + 1, lon + 1.5)
            rp31 = side.add_reference_point('rp31', lat + 0.6, lon + 1)
            rp41 = side.add_reference_point('rp41', lat + 1, lon + 0.5)
            point_list.append([rp11, rp21, rp31, rp41])


def update(scenario):
    pass
