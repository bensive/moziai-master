
# 时间 : 2021/07/27 17:59
# 作者 : 张志高
# 文件 : active_unit_test
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from mozi_ai_sdk.test.utils.test_framework import TestFramework
from mozi_ai_sdk.test.utils import common


class TestActiveUnit(TestFramework):
    """测试活动单元"""

    def test_get_assigned_mission(self):
        """获取分配的任务"""
        mission = self.refueling_tanker_aircraft.get_assigned_mission()
        self.assertEqual(mission.strName, '加油任务')

    def test_get_original_detector_side(self):
        """获取单元所在方"""
        side = self.refueling_tanker_aircraft.get_original_detector_side()
        self.assertEqual(side.strName, '红方')

    def test_get_par_group(self):
        """获取父级编组"""
        group = self.refueling_tanker_aircraft.get_par_group()
        self.assertEqual(group.strName, '飞行编队 59')

    def test_get_docked_units(self):
        """获取停靠单元（舰船或潜艇）"""
        unit_dict = self.wharf_1.get_docked_units()
        self.assertTrue(unit_dict)
        for k, v in unit_dict.items():
            self.assertTrue('舰船' in v.strName)

    def test_get_doctrine(self):
        """获取单元条令"""
        doctrine = self.antisubmarine_aircraft.get_doctrine()
        self.assertEqual(self.antisubmarine_aircraft, doctrine.get_doctrine_owner())

        # 设置对地自由开火
        doctrine.set_weapon_control_status_land(0)
        self.env.step()
        self.assertEqual(0, doctrine.m_WCS_Land)

    def test_doctrine_docked_ship(self):
        """获取停靠舰船条令设置"""
        doctrine = self.docked_ship_1.get_doctrine()
        self.assertEqual(self.docked_ship_1, doctrine.get_doctrine_owner())

        # 设置对地自由开火
        doctrine.set_weapon_control_status_land(0)
        self.env.step()
        self.assertEqual(0, doctrine.m_WCS_Land)

    def test_get_weapon_db_guids(self):
        """获取单元所有武器的db_guid"""
        db_guids = self.ground_to_air_missile_squadron.get_weapon_db_guids()
        self.assertTrue('hsfw-dataweapon-00000000001152' in db_guids)
        self.assertTrue('hsfw-dataweapon-00000000000735' in db_guids)

    def test_get_weapon_infos(self):
        """获取编组内所有武器的名称及db guid"""
        weapon_infos = self.ground_to_air_missile_squadron.get_weapon_infos()
        self.assertTrue(['48x MIM-104B型“爱国者-1”防空导弹', 'hsfw-dataweapon-00000000001152'] in weapon_infos)
        self.assertTrue(['6x FIM-92B型“毒刺”防空导弹[POST]', 'hsfw-dataweapon-00000000000735'] in weapon_infos)

    def test_get_mounts(self):
        """获取挂架信息"""
        mounts_infos = self.ground_to_air_missile_squadron.get_mounts()
        self.assertEqual(9, len(mounts_infos))

    def test_get_loadout(self):
        """获取挂载"""
        loadout_info = self.refueling_tanker_aircraft.get_loadout()
        print(loadout_info)
        self.assertEqual('CLoadout', loadout_info.ClassName)

    def test_get_magazines(self):
        """获取弹药库"""
        magazine_infos = self.ground_to_air_missile_squadron.get_magazines()
        self.assertEqual(2, len(magazine_infos))

    def test_get_sensor(self):
        """获取传感器"""
        sensor_infos = self.ground_to_air_missile_squadron.get_sensor()
        self.assertEqual(2, len(sensor_infos))

    def test_get_range_to_contact(self):
        """获取与目标的距离"""
        distance = self.ground_to_air_missile_squadron.get_range_to_contact(self.enemy_airplane_guid)
        self.assertEqual(21, int(distance.split('.')[0]))

    def test_plot_course(self):
        """航线规划"""
        # 反潜机1
        course_list = [(26.0728267704942, 125.582813973341), (26.410343165174, 125.857575579442)]
        self.antisubmarine_aircraft.plot_course(course_list)
        self.env.step()
        way_points_info = self.antisubmarine_aircraft.get_way_points_info()
        self.assertEqual(way_points_info[0]['latitude'], 26.0728267704942)
        self.assertEqual(way_points_info[0]['longitude'], 125.582813973341)
        self.assertEqual(way_points_info[1]['latitude'], 26.410343165174)
        self.assertEqual(way_points_info[1]['longitude'], 125.857575579442)

    def test_get_way_points_info(self):
        """获取本单元航路点信息"""
        # 与航线规划测试步骤相同
        # 反潜机1
        course_list = [(26.0728267704942, 125.582813973341), (26.410343165174, 125.857575579442)]
        self.antisubmarine_aircraft.plot_course(course_list)
        self.env.step()
        way_points_info = self.antisubmarine_aircraft.get_way_points_info()
        self.assertEqual(way_points_info[0]['latitude'], 26.0728267704942)
        self.assertEqual(way_points_info[0]['longitude'], 125.582813973341)
        self.assertEqual(way_points_info[1]['latitude'], 26.410343165174)
        self.assertEqual(way_points_info[1]['longitude'], 125.857575579442)

    def test_get_ai_targets(self):
        # 想定0时，返回值为空
        contacts_dic = self.ground_to_air_missile_squadron.get_ai_targets()
        self.env.step()
        contacts_dic = self.ground_to_air_missile_squadron.get_ai_targets()
        # 验证contacts_dic不为空
        self.assertTrue(contacts_dic)
        # 验证探测目标名称
        for k, v in contacts_dic.items():
            self.assertTrue(v.strName.strip() in ['苏-34 型“鸭嘴兽”攻击机', 'F-14E型“超级雄猫”战斗机'])

    def test_unit_obeys_emcon(self):
        """设置单元是否遵循电磁管控"""
        # 设置单元遵循电磁管控条令
        self.ground_to_air_missile_squadron.unit_obeys_emcon('true')
        self.env.step()
        self.assertEqual(True, self.ground_to_air_missile_squadron.bObeysEMCON)

        # 设置单元不遵循电磁管控条令
        self.ground_to_air_missile_squadron.unit_obeys_emcon('false')
        self.env.step()
        self.assertEqual(False, self.ground_to_air_missile_squadron.bObeysEMCON)

    def test_allocate_weapon_to_target_manual(self):
        """手动攻击"""
        weapon_guid = 'hsfw-dataweapon-00000000001152'
        # 向敌机1发射一枚 MIM-104B型“爱国者-1”防空导弹
        self.ground_to_air_missile_squadron.allocate_weapon_to_target(self.enemy_airplane_guid, weapon_guid, 1)
        # 查看墨子服务端, "地空导弹中队"发射了一枚 MIM-104B型“爱国者-1”防空导弹
        self.env.step()
        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if 'MIM-104B型“爱国者-1”防空导弹' in v.strName:
                flag = True
                break
        self.assertEqual(True, flag)

    def test_allocate_weapon_to_target_position(self):
        """纯方位攻击"""
        target = (28.8441089193402, 125.996683806863)
        # 向target对应的方位发射一枚RGM-84G “鱼叉”反舰导弹
        weapon_guid = 'hsfw-dataweapon-00000000000591'
        self.ship.allocate_weapon_to_target(target, weapon_guid, 1)
        self.env.step()
        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if '鱼叉' in v.strName:
                flag = True
                break
        self.assertEqual(True, flag)

    def test_unit_auto_detectable(self):
        """单元自动探测到"""
        self.ship.unit_auto_detectable('true')
        self.env.step()
        self.assertTrue(self.ship.bAutoDetectable)
        self.ship.unit_auto_detectable('false')
        self.env.step()
        self.assertFalse(self.ship.bAutoDetectable)

    def test_unit_drop_target_contact(self):
        """单元放弃目标"""
        # 设置对空限制开火
        side_doctrine = self.red_side.get_doctrine()
        side_doctrine.set_weapon_control_status('weapon_control_status_air', 2)

        # 向敌机1发射一枚 MIM-104B型“爱国者-1”防空导弹
        weapon_guid = 'hsfw-dataweapon-00000000001152'
        self.ground_to_air_missile_squadron.allocate_weapon_to_target(self.enemy_airplane_guid, weapon_guid, 1)

        # 单元放弃目标
        self.ground_to_air_missile_squadron.unit_drop_target_contact(self.enemy_airplane_guid)

        self.env.step()
        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if 'MIM-104B型“爱国者-1”防空导弹' in v.strName:
                flag = True
                break
        self.assertEqual(False, flag)

    def test_unit_drop_target_all_contact(self):
        """单元放弃所有目标"""

        # 设置对空限制开火
        side_doctrine = self.red_side.get_doctrine()
        side_doctrine.set_weapon_control_status('weapon_control_status_air', 2)

        # 向敌机1发射一枚 MIM-104B型“爱国者-1”防空导弹
        weapon_guid = 'hsfw-dataweapon-00000000001152'
        self.ground_to_air_missile_squadron.allocate_weapon_to_target(self.enemy_airplane_guid, weapon_guid, 1)
        self.ground_to_air_missile_squadron.allocate_weapon_to_target(self.enemy_airplane_guid_2, weapon_guid, 1)

        # 单元放弃目标
        self.ground_to_air_missile_squadron.unit_drop_target_all_contact()

        self.env.step()
        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if 'MIM-104B型“爱国者-1”防空导弹' in v.strName:
                flag = True
                break
        self.assertEqual(False, flag)

    def test_ignore_plotted_course_when_attacking(self):
        """攻击时忽略计划航线"""
        # 设置攻击时忽略计划航线
        self.ground_to_air_missile_squadron.ignore_plotted_course_when_attacking('Yes')
        self.env.step()
        self.assertEqual(1, self.ground_to_air_missile_squadron.get_doctrine().m_IgnorePlottedCourseWhenAttacking)
        # 设置攻击时不忽略计划航线
        self.ground_to_air_missile_squadron.ignore_plotted_course_when_attacking('No')
        self.env.step()
        self.assertEqual(0, self.ground_to_air_missile_squadron.get_doctrine().m_IgnorePlottedCourseWhenAttacking)
        # 设置攻击时忽略计划航线设定与上级保持一致
        self.ground_to_air_missile_squadron.ignore_plotted_course_when_attacking('Inherited')
        self.env.step()
        self.assertEqual(-1, self.ground_to_air_missile_squadron.get_doctrine().m_IgnorePlottedCourseWhenAttacking)

    def test_follow_terrain(self):
        """设置当前单元（飞机）的飞行高度跟随地形"""
        # 设置地形跟随
        self.refueling_tanker_aircraft.follow_terrain('true')
        self.env.step()
        self.assertTrue(self.refueling_tanker_aircraft.bTerrainFollowing)
        # 设置地形不跟随
        self.refueling_tanker_aircraft.follow_terrain('false')
        self.env.step()
        self.assertFalse(self.refueling_tanker_aircraft.bTerrainFollowing)

    def test_delete_coursed_point(self):
        """单元删除航路点"""
        # 验证清空航路点的情况
        course_list = [(26.0728267704942, 125.582813973341), (26.410343165174, 125.857575579442)]
        self.antisubmarine_aircraft.plot_course(course_list)
        self.env.step()
        # 清空所有航路点
        self.antisubmarine_aircraft.delete_coursed_point(clear=True)
        self.env.step()
        way_points_info = self.antisubmarine_aircraft.get_way_points_info()
        self.assertFalse(way_points_info)

        # 以index列表删除航路点
        course_list = [(26.0728267704942, 125.582813973341), (26.410343165174, 125.857575579442)]
        self.antisubmarine_aircraft.plot_course(course_list)
        self.env.step()
        # 删除第1，2个航路点
        self.antisubmarine_aircraft.delete_coursed_point([0, 1])
        self.env.step()
        way_points_info = self.antisubmarine_aircraft.get_way_points_info()
        self.assertFalse(way_points_info)

        # 以index删除航路点
        course_list = [(26.0728267704942, 125.582813973341), (26.410343165174, 125.857575579442)]
        self.antisubmarine_aircraft.plot_course(course_list)
        self.env.step()
        # 删除第2个航路点
        self.antisubmarine_aircraft.delete_coursed_point(1)
        self.env.step()
        way_points_info = self.antisubmarine_aircraft.get_way_points_info()
        self.assertEqual(len(way_points_info), 1)
        self.assertEqual(way_points_info[0]['latitude'], 26.0728267704942)
        self.assertEqual(way_points_info[0]['longitude'], 125.582813973341)

    def test_return_to_base(self):
        """单元返回基地"""
        self.antisubmarine_aircraft.return_to_base()
        self.env.step()
        self.env.step()
        self.env.step()
        self.assertEqual(self.antisubmarine_aircraft.strActiveUnitStatus, '状态: 返回基地(受命)')

    def test_select_new_base(self):
        """单元选择新基地/新港口"""
        self.antisubmarine_aircraft.select_new_base(self.airport_2.strGuid)
        self.env.step()
        self.env.step()
        self.env.step()
        self.assertEqual(self.antisubmarine_aircraft.m_HostActiveUnit, self.airport_2.strGuid)

    def test_hold_position(self):
        """命令面上指定单元设置是否保持阵位"""
        # TODO C# 脚本执行出错
        self.ship_japan_1.hold_position('true')
        self.env.step()
        self.assertTrue(self.ship_japan_1.bHoldPosition)
        self.ship_japan_1.hold_position('false')
        self.env.step()
        self.assertFalse(self.ship_japan_1.bHoldPosition)

    def test_leave_dock_alone(self):
        """单独出航"""
        self.docked_ship_1.leave_dock_alone()
        self.env.step()
        self.assertEqual(self.docked_ship_1.strStatusInfo, '部署出动')

    def test_assign_unit_to_mission(self):
        """分配任务"""
        missing_name = '空中打击'
        self.docked_f35_1.assign_unit_to_mission(missing_name)
        self.env.step()
        self.assertEqual(self.red_side.get_missions_by_name(missing_name).strGuid, self.docked_f35_1.m_AssignedMission)

    def test_assign_unit_to_mission_docked_ship(self):
        """分配任务"""
        missing_name = '水上巡逻'
        self.docked_ship_1.assign_unit_to_mission(missing_name)
        self.env.step()
        self.assertEqual(self.red_side.get_missions_by_name(missing_name).strGuid, self.docked_ship_1.m_AssignedMission)

    def test_assign_unit_to_mission_escort(self):
        """将单元分配为某打击任务的护航任务"""
        missing_name = '空中打击'
        self.docked_f35_1.assign_unit_to_mission_escort(missing_name)
        self.env.step()
        self.assertEqual(self.red_side.get_missions_by_name(missing_name).strGuid, self.docked_f35_1.m_AssignedMission)

    def test_cancel_assign_unit_to_mission(self):
        """将单元分配为某打击任务的护航任务"""
        missing_name = '空中打击'
        self.docked_f35_1.assign_unit_to_mission(missing_name)
        self.env.step()
        self.docked_f35_1.cancel_assign_unit_to_mission()
        self.env.step()
        self.assertEqual('', self.docked_f35_1.m_AssignedMission)

    def test_set_fuel_qty(self):
        """设置单元燃油量"""
        self.env.step()
        self.antisubmarine_aircraft.set_fuel_qty(5000)
        self.env.step()
        self.assertTrue(self.antisubmarine_aircraft.iCurrentFuelQuantity < 5000)

    def test_set_unit_heading(self):
        """设置单元朝向"""
        # TODO 设置单元朝向对舰船不起作用
        self.ship.set_unit_heading(60)
        self.env.step()
        self.assertEqual(self.ship.fCurrentHeading, 60)

    def test_auto_attack(self):
        """自动攻击"""
        self.ground_to_air_missile_squadron.auto_attack(self.enemy_airplane_guid)

        self.env.step()
        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if 'MIM-104B型“爱国者-1”防空导弹' in v.strName:
                flag = True
                break
        self.assertEqual(True, flag)

    def test_set_desired_speed(self):
        """设置单元期望速度"""
        # 若要使设定生效，飞机不能是盘旋状态
        course_list = [(26.0728267704942, 125.582813973341), (26.410343165174, 125.857575579442)]
        self.antisubmarine_aircraft.plot_course(course_list)
        self.env.step()
        # 设置期望速度
        self.antisubmarine_aircraft.set_desired_speed(555.6)
        self.env.step()
        self.env.step()
        self.assertEqual(self.antisubmarine_aircraft.fDesiredSpeed * 1.852, 555.6)

    def test_set_throttle(self):
        """设置单元油门"""
        # 若要使设定生效，飞机不能是盘旋状态
        course_list = [(26.0728267704942, 125.582813973341), (26.410343165174, 125.857575579442)]
        self.aircraft_dipping_sonar.plot_course(course_list)
        self.env.step()
        # 设置单元油门
        # TODO 低速 - 测试失败
        # self.aircraft_dipping_sonar.set_throttle(1)
        # self.env.step()
        # self.assertEqual(1, self.aircraft_dipping_sonar.m_CurrentThrottle)
        # 巡航
        self.aircraft_dipping_sonar.set_throttle(2)
        self.env.step()
        self.assertEqual(2, self.aircraft_dipping_sonar.m_CurrentThrottle)
        # 全速
        self.aircraft_dipping_sonar.set_throttle(3)
        self.env.step()
        self.assertEqual(3, self.aircraft_dipping_sonar.m_CurrentThrottle)
        # TODO 军用- 测试失败
        # self.aircraft_dipping_sonar.set_throttle(4)
        # self.env.step()
        # self.assertEqual(4, self.aircraft_dipping_sonar.m_CurrentThrottle)

    def test_set_desired_height(self):
        """设置期望高度"""
        # 给飞机设置航线
        course_list = [(26.0728267704942, 125.582813973341), (26.410343165174, 125.857575579442)]
        self.aircraft_dipping_sonar.plot_course(course_list)
        self.env.step()
        # 设置单元期望高度
        self.aircraft_dipping_sonar.set_desired_height(3000, 'true')
        self.env.step()
        self.assertEqual(3000, self.aircraft_dipping_sonar.fDesiredAltitude)

    def test_set_desired_height_submarine(self):
        """设置期望高度"""
        # TODO 对潜艇不起作用
        # 给潜艇设置航线
        course_list = [(26.0728267704942, 125.582813973341), (26.410343165174, 125.857575579442)]
        self.submarine.plot_course(course_list)
        self.env.step()
        # 设置单元期望高度
        self.aircraft_dipping_sonar.set_desired_height(-50.1, 'true')
        self.env.step()
        self.assertEqual(-50.1, self.aircraft_dipping_sonar.fDesiredAltitude)

    def test_set_radar_shutdown(self):
        # 设置舰船不遵循电磁管控
        self.ship.unit_obeys_emcon('false')
        self.env.step()

        # 设置雷达开机
        self.ship.set_radar_shutdown('true')
        self.env.step()
        flag = False
        sensors = self.ship.get_sensor()
        for k, v in sensors.items():
            if '雷达' in v.strName:
                self.assertEqual(v.bActive, True)
                flag = True
        self.assertEqual(flag, True)

        # 设置雷达关机
        self.ship.set_radar_shutdown('false')
        self.env.step()
        flag = False
        sensors = self.ship.get_sensor()
        for k, v in sensors.items():
            if '雷达' in v.strName:
                self.assertEqual(v.bActive, False)
                flag = True
        self.assertEqual(flag, True)

    def test_set_sonar_shutdown(self):
        # 设置 舰船-纯方位发射 不遵循电磁管控
        self.ship.unit_obeys_emcon('false')
        self.env.step()
        # 设置声纳开机
        self.ship.set_sonar_shutdown('true')
        self.env.step()
        flag = False
        sensors = self.ship.get_sensor()
        for k, v in sensors.items():
            if '声纳' in v.strName and '主' in v.strName:
                self.assertEqual(v.bActive, True)
                flag = True
        self.assertEqual(flag, True)

        # 设置声纳关机
        self.ship.set_sonar_shutdown('false')
        self.env.step()
        flag = False
        sensors = self.ship.get_sensor()
        for k, v in sensors.items():
            if '声纳' in v.strName and '主' in v.strName:
                self.assertEqual(v.bActive, False)
                flag = True
        self.assertEqual(flag, True)

    def test_set_oecm_shutdown(self):
        # 设置 舰船-纯方位发射 不遵循电磁管控
        self.ship.unit_obeys_emcon('false')
        self.env.step()

        # 设置干扰机开机
        self.ship.set_oecm_shutdown('true')
        self.env.step()
        flag = False
        sensors = self.ship.get_sensor()
        for k, v in sensors.items():
            if 'ECM' in v.strName:
                self.assertEqual(v.bActive, True)
                flag = True
        self.assertEqual(flag, True)

        # 设置干扰机关机
        self.ship.set_oecm_shutdown('false')
        self.env.step()
        sensors = self.ship.get_sensor()
        for k, v in sensors.items():
            if 'ECM' in v.strName:
                self.assertEqual(v.bActive, False)
                flag = True
        self.assertEqual(flag, True)

    def test_manual_attack(self):
        """手动攻击"""
        weapon_guid = 'hsfw-dataweapon-00000000001152'
        # 向敌机1发射一枚 MIM-104B型“爱国者-1”防空导弹
        self.ground_to_air_missile_squadron.manual_attack(self.enemy_airplane_guid, weapon_guid, 1)
        self.env.step()
        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if 'MIM-104B型“爱国者-1”防空导弹' in v.strName:
                flag = True
                break
        self.assertEqual(True, flag)

    def test_set_single_out(self):
        """飞机单机出动"""
        # 设置F35 #1单机出动
        self.docked_f35_1.set_single_out()
        self.env.step()
        self.assertEqual(self.docked_f35_1.strActiveUnitStatus, '状态: 未分配任务 (正在滑行准备起飞)')

    def test_drop_active_sonobuoy(self):
        """投放主动声纳"""
        # 投放主动声纳，深
        self.aircraft_drop_sonar.drop_active_sonobuoy('deep')
        self.env.step()
        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        name_1 = ''
        for k, v in weapons.items():
            if '主动声呐浮标' in v.strName:
                name_1 = v.strName
                self.assertTrue(v.fAltitude_AGL < -50)
                flag = True
                break
        self.assertEqual(True, flag)

        # 投放主动声纳，浅
        self.aircraft_drop_sonar.drop_active_sonobuoy('shallow')
        self.env.step()
        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if '主动声呐浮标' in v.strName and v.strName != name_1:
                self.assertTrue(v.fAltitude_AGL > -50)
                flag = True
                break
        self.assertEqual(True, flag)

    def test_drop_passive_sonobuoy(self):
        """投放被动声纳"""
        # 投放被动声纳，深
        self.aircraft_drop_sonar.drop_passive_sonobuoy('deep')
        self.env.step()

        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        name_1 = ''
        for k, v in weapons.items():
            if '被动声呐浮标' in v.strName:
                name_1 = v.strName
                self.assertTrue(v.fAltitude_AGL < -50)
                flag = True
                break
        self.assertEqual(True, flag)

        # 投放被动声纳，浅
        self.aircraft_drop_sonar.drop_passive_sonobuoy('shallow')
        self.env.step()

        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if '被动声呐浮标' in v.strName and v.strName != name_1:
                self.assertTrue(v.fAltitude_AGL > -50)
                flag = True
                break
        self.assertEqual(True, flag)

    def test_drop_sonobuoy(self):
        """投放声纳"""
        self.aircraft_drop_sonar.drop_sonobuoy('deep', 'active')
        self.env.step()
        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        name_1 = ''
        for k, v in weapons.items():
            if '主动声呐浮标' in v.strName:
                name_1 = v.strName
                self.assertTrue(v.fAltitude_AGL < -50)
                flag = True
                break
        self.assertEqual(True, flag)

        self.aircraft_drop_sonar.drop_sonobuoy('shallow', 'active')
        self.env.step()
        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if '主动声呐浮标' in v.strName and v.strName != name_1:
                self.assertTrue(v.fAltitude_AGL > -50)
                flag = True
                break
        self.assertEqual(True, flag)

        self.aircraft_drop_sonar.drop_sonobuoy('deep', 'passive')
        self.env.step()
        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        name_1 = ''
        for k, v in weapons.items():
            if '被动声呐浮标' in v.strName:
                name_1 = v.strName
                self.assertTrue(v.fAltitude_AGL < -50)
                flag = True
                break
        self.assertEqual(True, flag)

        self.aircraft_drop_sonar.drop_sonobuoy('shallow', 'passive')
        self.env.step()
        # 获取所有武器
        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if '被动声呐浮标' in v.strName and v.strName != name_1:
                self.assertTrue(v.fAltitude_AGL > -50)
                flag = True
                break
        self.assertEqual(True, flag)

    def test_set_own_side(self):
        self.aircraft_drop_sonar.set_own_side('蓝方')
        self.env.step()
        blue_side = self.scenario.get_side_by_name("蓝方")
        self.assertEqual(self.aircraft_drop_sonar.m_Side, blue_side.strGuid)
        # 问题，更改后blue_side中获取不到这个单元
        aircrafts = blue_side.get_aircrafts()
        flag = False
        for k, v in aircrafts.items():
            if "飞机-投放声纳" in v.strName:
                flag = True
        self.assertTrue(flag)

        aircrafts = self.red_side.get_aircrafts()
        flag = False
        for k, v in aircrafts.items():
            if "飞机-投放声纳" in v.strName:
                flag = True
        self.assertFalse(flag)

    def test_set_loadout(self):
        # 包含可选武器
        self.docked_f35_1.set_loadout(loadout_id=2995, time_to_ready_minutes=10, ignore_magazines='true',
                                      exclude_optional_weapons='false')
        self.env.step()
        loadout = self.docked_f35_1.get_loadout()
        self.assertTrue('hsfw-dataloadout-0000000002995' in loadout.strDBGUID)
        self.assertTrue('hsfw-dataweapon-00000000000051' in loadout.m_LoadRatio)
        self.assertTrue('hsfw-dataweapon-00000000000945' in loadout.m_LoadRatio)
        self.assertTrue('hsfw-dataweapon-00000000001839' in loadout.m_LoadRatio)

        # 不包含可选武器
        self.docked_f35_1.set_loadout(loadout_id=2995, time_to_ready_minutes=10, ignore_magazines='true',
                                      exclude_optional_weapons='true')
        self.env.step()
        loadout = self.docked_f35_1.get_loadout()
        self.assertTrue('hsfw-dataloadout-0000000002995' in loadout.strDBGUID)
        self.assertTrue('hsfw-dataweapon-00000000000051' not in loadout.m_LoadRatio)
        self.assertTrue('hsfw-dataweapon-00000000000945' in loadout.m_LoadRatio)
        self.assertTrue('hsfw-dataweapon-00000000001839' in loadout.m_LoadRatio)

    def test_reload_weapon(self):
        self.ground_to_air_missile_squadron.auto_attack(self.enemy_airplane_guid)
        self.env.step()
        weapon_db_guid = 'hsfw-dataweapon-00000000001152'
        # 装填1个MIM-104B型“爱国者-1”防空导弹
        self.ground_to_air_missile_squadron.reload_weapon(weapon_db_guid, 1)
        self.env.step()
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        flag = False
        for k, v in mounts.items():
            if v.strName == 'M901式爱国者导弹':
                if v.strLoadWeaponCount == '(3/4)':
                    flag = True
        self.assertTrue(flag)

        # 填满MIM-104B型“爱国者-1”防空导弹
        self.ground_to_air_missile_squadron.reload_weapon(weapon_db_guid, 3, 'true')
        self.env.step()
        # 地空导弹营填充了3发 MIM-104B型“爱国者-1”防空导弹
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        flag = False
        for k, v in mounts.items():
            if v.strName == 'M901式爱国者导弹':
                print(v.strLoadWeaponCount)
                if v.strLoadWeaponCount != '(4/4)':
                    flag = True
        self.assertFalse(flag)

    def test_load_cargo(self):
        """装载货物"""
        # 机场1装载货物
        self.airport_1.load_cargo(469)
        self.env.step()
        cargo = self.airport_1.m_Cargo.split('$')
        self.assertTrue(cargo[0].endswith('469'))
        self.assertEqual(cargo[1], '1')

    def test_remove_cargo(self):
        """卸载货物"""
        # 机场1装载货物
        self.airport_1.load_cargo(469)
        self.env.step()
        # 机场1卸载货物
        self.airport_1.remove_cargo(469)
        self.env.step()
        self.assertFalse(self.airport_1.m_Cargo)

    def test_set_magazine_weapon_current_load(self):
        """设置弹药库武器数量"""
        # 获取地空导弹中队最后一个弹药库的第一个武器记录guid
        magazines = self.ground_to_air_missile_squadron.get_magazines()
        magazine = common.get_obj_by_name(magazines, '爱国者导弹')
        # 'a2db1331-e223-4b1f-8d86-d000aa0bb8cc$hsfw-dataweapon-00000000001152$10$24'
        weapon_record_guid = magazine.m_LoadRatio.split('$')[0]
        self.ground_to_air_missile_squadron.set_magazine_weapon_current_load(weapon_record_guid, 10)
        self.env.step()
        # 查看地空导弹中队弹药库，爱国者导弹数量变为10
        magazines = self.ground_to_air_missile_squadron.get_magazines()
        magazine = common.get_obj_by_name(magazines, '爱国者导弹')
        # 'a2db1331-e223-4b1f-8d86-d000aa0bb8cc$hsfw-dataweapon-00000000001152$10$24'
        number = int(magazine.m_LoadRatio.split('$')[2])
        self.assertEqual(number, 10)

    def test_remove_magazine(self):
        """删除弹药库"""
        # 获取地空导弹中队最后一个弹药库
        magazines = self.ground_to_air_missile_squadron.get_magazines()
        magazine = common.get_obj_by_name(magazines, '爱国者导弹')
        # 删除弹药库
        self.ground_to_air_missile_squadron.remove_magazine(magazine.strGuid)
        self.env.step()
        # 验证弹药库是否被删除
        magazines = self.ground_to_air_missile_squadron.get_magazines()
        self.assertFalse(magazine.strGuid in magazines.keys())

    def test_set_magazine_state(self):
        """设置弹药库状态"""
        # 获取地空导弹中队最后一个弹药库
        magazines = self.ground_to_air_missile_squadron.get_magazines()
        print(magazines)
        magazine = common.get_obj_by_name(magazines, '爱国者导弹')
        magazine_guid = magazine.strGuid
        print(magazine_guid)
        # 设置弹药库被摧毁
        self.ground_to_air_missile_squadron.set_magazine_state(magazine_guid, '摧毁')
        self.env.step()
        self.assertEqual(magazine.m_ComponentStatus, 2)
        # 设置重度毁伤 TODO  m_ComponentStatus没有区分三种毁伤
        self.ground_to_air_missile_squadron.set_magazine_state(magazine_guid, '重度毁伤')
        self.env.step()
        self.assertEqual(magazine.m_ComponentStatus, 1)
        # 设置中度毁伤 TODO m_ComponentStatus没有区分三种毁伤
        self.ground_to_air_missile_squadron.set_magazine_state(magazine_guid, '中度毁伤')
        self.env.step()
        self.assertEqual(magazine.m_ComponentStatus, 1)
        # 设置轻度毁伤 TODO m_ComponentStatus没有区分三种毁伤
        self.ground_to_air_missile_squadron.set_magazine_state(magazine_guid, '轻度毁伤')
        self.env.step()
        self.assertEqual(magazine.m_ComponentStatus, 1)
        # 设置正常运转
        self.ground_to_air_missile_squadron.set_magazine_state(magazine_guid, '正常运转')
        self.env.step()
        self.assertEqual(magazine.m_ComponentStatus, 0)

    def test_set_weapon_current_load(self):
        """设置挂架武器数量"""
        # 获取地空导弹中队第一个名称为‘M901式爱国者导弹’的挂架
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        mount = common.get_obj_by_name(mounts, 'M901式爱国者导弹')
        weapon_record_guid = mount.m_LoadRatio.split('$')[0]
        mount_guid = mount.strGuid
        # 设置挂架武器数量为1
        self.ground_to_air_missile_squadron.set_weapon_current_load(weapon_record_guid, 1)
        self.env.step()
        # 验证
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        mount = mounts.get(mount_guid)
        self.assertEqual(mount.strLoadWeaponCount, '(1/4)')

    def test_set_weapon_reload_priority(self):
        # TODO Lua执行后不起作用
        """设置武器重新装载优先级"""
        # 获取地空导弹中队第一个名称为‘M901式爱国者导弹’的挂架
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        mount = common.get_obj_by_name(mounts, 'M901式爱国者导弹')
        mount_guid = mount.strGuid
        weapon_record_guid = mount.m_LoadRatio.split('$')[0]
        self.ground_to_air_missile_squadron.set_weapon_reload_priority(weapon_record_guid, 'true')
        self.env.step()
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        mount = mounts.get(mount_guid)
        self.assertEqual(mount.m_ReloadPrioritySet, 'hsfw-dataweapon-00000000001152')

        self.ground_to_air_missile_squadron.set_weapon_reload_priority(weapon_record_guid, 'false')
        self.env.step()
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        mount = mounts.get(mount_guid)
        self.assertEqual(mount.m_ReloadPrioritySet, '')

    def test_add_weapon_to_unit_magazine(self):
        # TODO Lua未调通
        """往弹药库内添加武器"""
        # 获取地空导弹中队最后一个弹药库
        magazines = self.ground_to_air_missile_squadron.get_magazines()
        print(magazines)
        magazine_guid = ''
        for k, v in magazines.items():
            magazine_guid = k
        print(magazine_guid)
        # 添加5个105毫米M68A1型高爆火炮
        weapon_db_guid = 'hsfw-dataweaponrecord-00000000004'
        self.ground_to_air_missile_squadron.add_weapon_to_unit_magazine(magazine_guid, weapon_db_guid, 3)
        self.env.step()
        pass

    def test_switch_sensor(self):
        """同时设置单元上多种类型传感器的开关状态。"""
        # 设置单元不遵循电磁管控
        self.ship.unit_obeys_emcon('false')
        # 设置单元雷达、声纳、干扰机开机
        self.ship.switch_sensor(radar='true', sonar='true', oecm='true')
        self.env.step()
        sensors = self.ship.get_sensor()
        radar = common.get_obj_by_name(sensors, 'AN/SPG-62型目标照射雷达')
        self.assertEqual(radar.bActive, True)
        sonar = common.get_obj_by_name(sensors, 'AN/SQS-53C型舰壳主/被动声纳')
        self.assertEqual(sonar.bActive, True)
        ecm = common.get_obj_by_name(sensors, 'AN/SLQ-32(V)6型电子战系统[ECM]')
        self.assertEqual(ecm.bActive, True)

        # 设置单元雷达、声纳、干扰机关机
        self.ship.switch_sensor(radar='false', sonar='false', oecm='false')
        self.env.step()
        sensors = self.ship.get_sensor()
        radar = common.get_obj_by_name(sensors, 'AN/SPG-62型目标照射雷达')
        self.assertEqual(radar.bActive, False)
        sonar = common.get_obj_by_name(sensors, 'AN/SQS-53C型舰壳主/被动声纳')
        self.assertEqual(sonar.bActive, False)
        ecm = common.get_obj_by_name(sensors, 'AN/SLQ-32(V)6型电子战系统[ECM]')
        self.assertEqual(ecm.bActive, False)

    def test_wcsf_contact_types_unit(self):
        """控制指定单元对所有目标类型的攻击状态。"""
        # 设置限制开火
        self.ship.wcsf_contact_types_unit('Hold')
        self.env.step()
        self.assertEqual(self.ship.get_doctrine().m_WCS_Air, 2)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Surface, 2)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Submarine, 2)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Land, 2)
        # 设置谨慎开火
        self.ship.wcsf_contact_types_unit('Tight')
        self.env.step()
        self.assertEqual(self.ship.get_doctrine().m_WCS_Air, 1)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Surface, 1)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Submarine, 1)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Land, 1)
        # 设置自由开火
        self.ship.wcsf_contact_types_unit('Free')
        self.env.step()
        self.assertEqual(self.ship.get_doctrine().m_WCS_Air, 0)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Surface, 0)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Submarine, 0)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Land, 0)
        # 设置与上级一致
        self.ship.wcsf_contact_types_unit('Inherited')
        self.env.step()
        self.assertEqual(self.ship.get_doctrine().m_WCS_Air, -1)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Surface, -1)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Submarine, -1)
        self.assertEqual(self.ship.get_doctrine().m_WCS_Land, -1)

    def test_allocate_all_weapons_to_target(self):
        """为手动交战分配同类型所有武器。"""
        self.ground_to_air_missile_squadron.wcsf_contact_types_unit('Hold')
        self.ground_to_air_missile_squadron.allocate_all_weapons_to_target(self.enemy_airplane_guid, 1152)
        self.env.step()
        self.env.step()
        # 验证地空导弹中队向目标敌机1发射所有武器，因传感器限制（最大照射目标数），只能发射9发
        weapons = self.red_side.get_weapons()
        count = 0
        for k, v in weapons.items():
            if 'MIM-104B型“爱国者-1”防空导弹' in v.strName:
                count += 1
        self.assertEqual(count, 9)

    def test_remove_salvo_target(self):
        # TODO salvo_guid不知道如何获取
        """取消手动交战时齐射攻击目标"""
        salvo_guid = self.ground_to_air_missile_squadron.allocate_salvo_to_target(self.enemy_airplane_guid, 1152)
        self.env.step()
        self.ground_to_air_missile_squadron.remove_salvo_target(salvo_guid)
        self.env.step()
        # 验证地空导弹中队向目标敌机1发射所有武器
        self.assertTrue(False)
        count = 0

    def test_set_salvo_timeout(self):
        """控制手动交战是否设置齐射间隔  or 超时自动取消齐射？？？"""
        # TODO 设置后未找到对应的态势
        self.ground_to_air_missile_squadron.set_salvo_timeout('false')
        self.env.step()
        # 选中单元，右键，手动接战目标，超时自动取消齐射取消勾选
        self.ground_to_air_missile_squadron.set_salvo_timeout('true')
        self.env.step()
        # 选中单元，右键，手动接战目标，超时自动取消齐射勾选

    def test_allocate_weapon_to_target(self):
        """手动攻击"""
        self.ground_to_air_missile_squadron.wcsf_contact_types_unit('Hold')
        # 手动攻击
        self.ground_to_air_missile_squadron.allocate_weapon_to_target(self.enemy_airplane_guid,
                                                                      'hsfw-dataweapon-00000000001152', 1)
        self.env.step()

        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if 'MIM-104B型“爱国者-1”防空导弹' in v.strName:
                flag = True
        self.assertEqual(flag, True)

    def test_allocate_weapon_to_target_2(self):
        """纯方位发射"""
        self.ship.wcsf_contact_types_unit('Hold')
        target = (28.8528630608011, 125.946422322959)
        # 发射一枚RGM-84G “鱼叉”反舰导弹
        self.ship.allocate_weapon_to_target(target, 'hsfw-dataweapon-00000000000591', 1)
        # 查看墨子服务端发射了一枚 RGM-84G “鱼叉”反舰导弹
        self.env.step()

        weapons = self.red_side.get_weapons()
        flag = False
        for k, v in weapons.items():
            if 'RGM-84G “鱼叉”反舰导弹' in v.strName:
                flag = True
        self.assertEqual(flag, True)

    def test_allocate_weapon_auto_targeted(self):
        """为自动交战进行弹目匹配。此时自动交战意义在于不用指定对多个目标的攻击顺序。"""
        # TODO 限制开火时，只发一枚导弹
        # TODO 不限制开火时，发射10枚
        # self.ground_to_air_missile_squadron.wcsf_contact_types_unit('Hold')
        target_guid_list = [self.enemy_airplane_guid, self.enemy_airplane_guid_2]
        # weapon_db_guid = 'hsfw-dataweapon-00000000001152'
        self.ground_to_air_missile_squadron.allocate_weapon_auto_targeted(target_guid_list, 1152, 4)
        self.env.step()
        count = 0
        while True:
            self.env.step()
            count = count + 1
            if count > 100:
                break

    def test_auto_target(self):
        # TODO 并没有发射武器 设置后目标从自动变成手动主要
        """让单元自动进行弹目匹配并攻击目标。"""
        target_guid_list = [self.enemy_airplane_guid]
        self.ground_to_air_missile_squadron.auto_target(target_guid_list)
        count = 0
        while True:
            self.env.step()
            count = count + 1
            if count > 100:
                break

    def test_add_to_host(self):
        """将单元部署进基地"""
        self.aircraft_drop_sonar.add_to_host(self.airport_1_guid)
        self.env.step()
        self.assertEqual(self.aircraft_drop_sonar.m_HostActiveUnit, self.airport_1_guid)

    def test_add_mount(self):
        """添加挂架"""
        heading_dict = {'PS1': 'true', 'PMA1': 'true'}
        # 添加挂架 20毫米 M39型机炮 [280 发备弹]
        self.ground_to_air_missile_squadron.add_mount(227, heading_dict)
        self.env.step()
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        mount_exist = False
        for k, v in mounts.items():
            if v.strName == '20毫米 M39型机炮 [280 发备弹]':
                mount_exist = True
        self.assertTrue(mount_exist)

    def test_remove_mount(self):
        """删除挂架"""
        heading_dict = {'PS1': 'true'}
        # 添加挂架 20毫米 M39型机炮 [280 发备弹]
        self.ground_to_air_missile_squadron.add_mount(227, heading_dict)
        self.env.step()
        # 获取所添加挂架的guid
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        mount_guid = ''
        for k, v in mounts.items():
            if v.strName == '20毫米 M39型机炮 [280 发备弹]':
                mount_guid = k
        self.assertTrue(mount_guid)
        # 删除挂架
        self.ground_to_air_missile_squadron.remove_mount(mount_guid)
        self.env.step()
        # 验证挂架已被移除
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        mount_exist = False
        for k, v in mounts.items():
            if v.strName == '20毫米 M39型机炮 [280 发备弹]':
                mount_exist = True
        self.assertFalse(mount_exist)

    def test_add_weapon(self):
        """挂架添加武器"""
        # TODO 插入的武器ID实际为武器记录ID
        heading_dict = {'PS1': 'true'}
        self.ground_to_air_missile_squadron.add_mount(227, heading_dict)
        self.env.step()
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        mount_guid = ''
        for k, v in mounts.items():
            if v.strName == '20毫米 M39型机炮 [280 发备弹]':
                mount_guid = k
        # 挂架中添加武器 "AIM-26B 型“猎鹰”空空导弹"
        self.ground_to_air_missile_squadron.add_weapon(1727, mount_guid)
        self.env.step()
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        flag = False
        mount = common.get_obj_by_name(mounts, '20毫米 M39型机炮 [280 发备弹]')
        self.assertTrue('hsfw-dataweapon-00000000000783' in mount.m_LoadRatio)
        self.assertTrue(False)

    def test_remove_weapon(self):
        """挂架删除武器"""
        heading_dict = {'PS1': 'true'}
        self.ground_to_air_missile_squadron.add_mount(227, heading_dict)
        self.env.step()
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        mount = common.get_obj_by_name(mounts, '20毫米 M39型机炮 [280 发备弹]')
        weapon_id = mount.m_LoadRatio.split('$')[0]

        self.env.step()
        self.ground_to_air_missile_squadron.remove_weapon(weapon_id)
        self.env.step()
        self.assertEqual(mount.m_LoadRatio, '')

    def test_update_way_point(self):
        # 设置航路点
        course_list = [(26.0728267704942, 125.582813973341), (26.410343165174, 125.857575579442)]
        self.antisubmarine_aircraft.plot_course(course_list)
        self.env.step()
        self.antisubmarine_aircraft.update_way_point(0, 27.0728267704942, 126.582813973341)
        self.env.step()
        way_points_info = self.antisubmarine_aircraft.get_way_points_info()
        self.assertEqual(way_points_info[0]['latitude'], 27.0728267704942)
        self.assertEqual(way_points_info[0]['longitude'], 126.582813973341)

    def test_set_way_point_sensor(self):
        """设置航路点传感器的开关状态"""
        # 设置航路点
        course_list = [(26.0728267704942, 125.582813973341), (26.410343165174, 125.857575579442)]
        self.antisubmarine_aircraft.plot_course(course_list)
        self.env.step()
        # 设置雷达、声纳、主动ECM开机
        self.antisubmarine_aircraft.set_way_point_sensor(0, 'CB_radar', 'Checked')
        self.antisubmarine_aircraft.set_way_point_sensor(0, 'CB_Sonar', 'Checked')
        self.antisubmarine_aircraft.set_way_point_sensor(0, 'CB_ECM', 'Checked')
        self.env.step()
        # 设置雷达、声纳、主动ECM关机
        self.antisubmarine_aircraft.set_way_point_sensor(0, 'CB_radar', 'Unchecked')
        self.antisubmarine_aircraft.set_way_point_sensor(0, 'CB_Sonar', 'Unchecked')
        self.antisubmarine_aircraft.set_way_point_sensor(0, 'CB_ECM', 'Unchecked')
        self.env.step()
        # 设置雷达、声纳、主动ECM未配置
        self.antisubmarine_aircraft.set_way_point_sensor(0, 'CB_radar', 'Indeterminate')
        self.antisubmarine_aircraft.set_way_point_sensor(0, 'CB_Sonar', 'Indeterminate')
        self.antisubmarine_aircraft.set_way_point_sensor(0, 'CB_ECM', 'Indeterminate')
        self.env.step()

    def test_set_unit_damage(self):
        """设置单元毁伤值"""
        # 设置航空设施毁伤  --- 被摧毁
        component_guid = self.airport_1.m_AirFacilitiesComponent.split('$0$0$@')[0].split('$')[0]
        # 设置总体毁伤为10%，设置第1个组件为完全摧毁
        self.airport_1.set_unit_damage(10, component_guid, 4)
        self.env.step()

        # 设置挂架毁伤 --- 重度毁伤 -- TODO 地空导弹中队不显示毁伤百分比
        mounts = self.ground_to_air_missile_squadron.get_mounts()
        mount_guid = ''
        for k, v in mounts.items():
            mount_guid = k
            break
        self.ground_to_air_missile_squadron.set_unit_damage(11, mount_guid, 3)

        # 设置弹药库毁伤 --- 中度毁伤
        magazines = self.ground_to_air_missile_squadron.get_magazines()
        magazine_guid = ''
        for k, v in magazines.items():
            magazine_guid = k
            break
        self.ground_to_air_missile_squadron.set_unit_damage(50, magazine_guid, 2)

        # 设置传感器毁伤  --- 轻度毁伤
        sensors = self.ground_to_air_missile_squadron.get_sensor()
        sensor_guid = ''
        for k, v in sensors.items():
            sensor_guid = k
            break
        self.ground_to_air_missile_squadron.set_unit_damage(50, sensor_guid, 1)
        self.env.step()
        # 设置正常工作
        self.ground_to_air_missile_squadron.set_unit_damage(50, sensor_guid, 0)
        self.env.step()

    def test_set_magazine_weapon_number(self):
        magazines = self.ground_to_air_missile_squadron.get_magazines()
        magazine_guid = ''
        magazine = None
        for k, v in magazines.items():
            magazine_guid = k
            magazine = v
            break
        weapon_db_guid = 'hsfw-dataweapon-00000000001397'       # 黄貂鱼 Mod 0型鱼雷
        # 添加两个"黄貂鱼 Mod 0型鱼雷"鱼雷到弹药库
        self.ground_to_air_missile_squadron.set_magazine_weapon_number(magazine_guid, weapon_db_guid, 2)
        self.env.step()
        self.assertTrue('hsfw-dataweapon-00000000001397$2$4' in magazine.m_LoadRatio)

    def test_set_side_proficiency(self):
        """设置单元训练水平"""
        # 新手
        self.antisubmarine_aircraft.set_proficiency('Novice')
        self.env.step()
        self.assertEqual(self.antisubmarine_aircraft.m_ProficiencyLevel, 0)
        # 初级
        self.antisubmarine_aircraft.set_proficiency('Cadet')
        self.env.step()
        self.assertEqual(self.antisubmarine_aircraft.m_ProficiencyLevel, 1)
        # 普通
        self.antisubmarine_aircraft.set_proficiency('Regular')
        self.env.step()
        self.assertEqual(self.antisubmarine_aircraft.m_ProficiencyLevel, 2)
        # 老手
        self.antisubmarine_aircraft.set_proficiency('Veteran')
        self.env.step()
        self.assertEqual(self.antisubmarine_aircraft.m_ProficiencyLevel, 3)
        # 顶级
        self.antisubmarine_aircraft.set_proficiency('Ace')
        self.env.step()
        self.assertEqual(self.antisubmarine_aircraft.m_ProficiencyLevel, 4)

    def test_set_side_proficiency_group(self):
        """设置编组训练水平"""
        # 新手
        self.air_group.set_proficiency('Novice')
        self.env.step()
        self.assertEqual(self.air_group.m_ProficiencyLevel, 0)

    def test_set_longitude_latitude(self):
        """移动单元，设置单元的经纬度"""
        # 新手
        self.airport_1.set_longitude_latitude(100.0, 50.0)
        self.env.step()
        self.assertEqual(self.airport_1.dLatitude, 50.0)
        self.assertEqual(self.airport_1.dLongitude, 100.0)


if __name__ == '__main__':
    TestActiveUnit.main()








