# 时间 : 2021/08/24 16:35
# 作者 : 张志高
# 文件 : patrol_mission
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from mozi_ai_sdk.test.utils.test_framework import TestFramework
from mozi_ai_sdk.test.utils import common


class TestPatrolMission(TestFramework):
    """测试巡逻任务类"""

    def test_set_prosecution_zone(self):
        """设置巡逻任务的警戒区"""
        point_list = ['RP-74', 'RP-75', 'RP-76', 'RP-77']
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.set_prosecution_zone(point_list)
        point_list = ['RP-74', 'RP-75', 'RP-76']
        mission.set_prosecution_zone(point_list)
        self.env.step()

        rps = mission.m_ProsecutionAreaVertices.split('@')
        points = self.red_side.get_reference_points()
        count = 0
        for item in rps:
            if item != "":
                count += 1
                rp = points.get(item)
                self.assertTrue(rp.strName in point_list)
        self.assertEqual(count, 3)

    def test_set_patrol_zone(self):
        """设置巡逻任务的巡逻区"""
        point_list = ['RP-74', 'RP-76', 'RP-77']
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.set_patrol_zone(point_list)
        point_list = ['RP-74', 'RP-75', 'RP-76']
        mission.set_patrol_zone(point_list)
        self.env.step()

        rps = mission.m_PatrolAreaVertices.split('@')
        points = self.red_side.get_reference_points()
        count = 0
        for item in rps:
            if item != "":
                count += 1
                rp = points.get(item)
                self.assertTrue(rp.strName in point_list)
        self.assertEqual(count, 3)

    def test_assign_unit(self):
        """分配单元"""
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.assign_unit(self.antisubmarine_aircraft_guid)
        self.env.step()
        units = mission.get_assigned_units()
        count = 0
        for k, v in units.items():
            count += 1
            self.assertEqual(v.strGuid, self.antisubmarine_aircraft_guid)
        self.assertEqual(count, 1)

    def test_get_doctrine(self):
        """获取任务条令"""
        mission = self.red_side.get_missions_by_name('空中巡逻')
        doctrine = mission.get_doctrine()
        self.assertEqual(doctrine.m_DoctrineOwner, mission.strGuid)

        # 设置对空限制开火
        doctrine.set_weapon_control_status('weapon_control_status_air', 2)
        self.env.step()
        self.assertEqual(2, doctrine.m_WCS_Air)

    def test_set_is_active(self):
        """设置是否启用任务"""
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.set_is_active('true')
        self.env.step()
        self.assertEqual(0, mission.m_MissionStatus)
        mission.set_is_active('false')
        self.env.step()
        self.assertEqual(1, mission.m_MissionStatus)

    def test_set_time(self):
        """设置任务时间"""
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.set_start_time('2021-07-19 22:10:00')
        mission.set_end_time('2021-07-19 23:10:00')
        self.env.step()
        self.assertEqual(mission.m_StartTime, 1626703800)
        self.assertEqual(mission.m_EndTime, 1626707400)

    def test_set_maintain_unit_number(self):
        """巡逻任务阵位上每类平台保存作战单元数量"""
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        # 阵位上没类平台保持2个单元
        mission.set_maintain_unit_number(2)
        self.env.step()
        self.assertEqual(mission.iMNOS, 2)

    def test_set_opa_check(self):
        """设置任务是否对巡逻区外的探测目标进行分析"""
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.set_opa_check('false')
        self.env.step()
        self.assertFalse(mission.bIOPA)
        mission.set_opa_check('true')
        self.env.step()
        self.assertTrue(mission.bIOPA)

    def test_set_emcon_usage(self):
        """设置任务是否仅在巡逻/警戒区内打开电磁辐射"""
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.set_emcon_usage('true')
        self.env.step()
        self.assertTrue(mission.bAEOIPA)

        mission.set_emcon_usage('false')
        self.env.step()
        self.assertFalse(mission.bAEOIPA)

    def test_set_wwr_check(self):
        """设置任务是否对武器射程内探测目标进行分析"""
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.set_wwr_check('false')
        self.env.step()
        self.assertFalse(mission.bIWWR)
        mission.set_wwr_check('true')
        self.env.step()
        self.assertTrue(mission.bIWWR)

    def test_set_flight_size(self):
        """设置任务编队规模"""
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.set_flight_size(1)
        self.env.step()
        self.assertEqual(mission.m_FlightSize, 1)
        mission.set_flight_size(2)
        self.env.step()
        self.assertEqual(mission.m_FlightSize, 2)
        mission.set_flight_size(3)
        self.env.step()
        self.assertEqual(mission.m_FlightSize, 3)
        mission.set_flight_size(4)
        self.env.step()
        self.assertEqual(mission.m_FlightSize, 4)
        mission.set_flight_size(6)
        self.env.step()
        self.assertEqual(mission.m_FlightSize, 6)

    def test_set_flight_size_check(self):
        """设置打击任务是否飞机数低于编组规模数要求就不能起飞"""
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.set_flight_size_check('true')
        self.env.step()
        self.assertTrue(mission.bUseFlightSizeHardLimit)
        mission.set_flight_size_check('false')
        self.env.step()
        self.assertFalse(mission.bUseFlightSizeHardLimit)

    def test_set_throttle(self):
        """设置任务的油门"""
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        # 出航-巡航
        mission.set_throttle_transit('Cruise')
        # 阵位 - 军用
        mission.set_throttle_station('Full')
        # 攻击 - 加力
        mission.set_throttle_attack('Flank')
        self.env.step()
        self.assertEqual(mission.m_AttackThrottle_Aircraft, 4)
        self.assertEqual(mission.m_StationThrottle_Aircraft, 3)
        self.assertEqual(mission.m_TransitThrottle_Aircraft, 2)

    def test_set_throttle_ship(self):
        """设置任务的水面舰艇油门"""
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        # 出航-巡航
        mission.set_throttle_transit_ship('Cruise')
        # 阵位 - 全速
        mission.set_throttle_station_ship('Full')
        # 攻击 - 最大
        mission.set_throttle_attack_ship('Flank')
        self.env.step()
        self.env.step()
        self.assertEqual(mission.m_AttackThrottle_Ship, 4)
        self.assertEqual(mission.m_StationThrottle_Ship, 3)
        self.assertEqual(mission.m_TransitThrottle_Ship, 2)

    def test_set_speed(self):
        """设置任务的速度"""
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        # 飞机出航
        mission.set_speed('transitSpeedAircraft', 200)
        # 飞机阵位
        mission.set_speed('stationSpeedAircraft', 300)
        # 飞机攻击
        mission.set_speed('attackSpeedAircraft', 400)
        # 舰船出航
        mission.set_speed('transitSpeedShip', 20)
        # 舰船阵位
        mission.set_speed('stationSpeedShip', 30)
        # 舰船攻击
        mission.set_speed('attackSpeedShip', 40)
        # 潜艇出航
        mission.set_speed('transitSpeedSubmarine', 10)
        # 潜艇阵位
        mission.set_speed('stationSpeedSubmarine', 15)
        # 潜艇攻击
        mission.set_speed('attackSpeedSubmarine', 20)
        self.env.step()
        self.assertEqual(mission.strAttackSpeed_Aircraft, '400')
        self.assertEqual(mission.strAttackSpeed_Ship, '40')
        self.assertEqual(mission.strAttackSpeed_Submarine, '20')

        self.assertEqual(mission.strStationSpeed_Aircraft, '300')
        self.assertEqual(mission.strStationSpeed_Ship, '30')
        self.assertEqual(mission.strStationSpeed_Submarine, '15')

        self.assertEqual(mission.strTransitSpeed_Aircraft, '200')
        self.assertEqual(mission.strTransitSpeed_Ship, '20')
        self.assertEqual(mission.strTransitSpeed_Submarine, '10')

    def test_set_altitude(self):
        """设置任务的出航/阵位/攻击高度"""
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        # 出航高度
        mission.set_transit_altitude(1000)
        # 阵位高度
        mission.set_station_altitude(2000)
        # 攻击高度
        mission.set_attack_altitude(3000)
        self.env.step()
        self.assertEqual(mission.strAttackAltitude_Aircraft, '3000')
        self.assertEqual(mission.strStationAltitude_Aircraft, '2000')
        self.assertEqual(mission.strTransitAltitude_Aircraft, '1000')

    def test_set_attack_distance(self):
        """设置任务的攻击距离"""
        # 空战巡逻
        mission = self.red_side.get_missions_by_name('空中巡逻')
        # 攻击距离
        mission.set_attack_distance(500)
        self.env.step()
        self.assertEqual(mission.strAttackDistance_Aircraft, '500')

    def test_set_patrol_sonobuoys_cover(self):
        """反潜巡逻任务设置声呐浮标在巡逻区域内的覆盖密度和深浅类型"""
        # 反潜巡逻
        point_list = ['RP-74', 'RP-75', 'RP-76', 'RP-77']
        mission = self.red_side.add_mission_patrol('反潜巡逻', 4, point_list)
        # 投放声呐覆盖3倍半径，声呐浮标深度温跃层之下
        mission.set_patrol_sonobuoys_cover(3.0, 2)
        self.env.step()
        # TODO 没有下面两个属性
        self.assertEqual(mission.m_cboSonobuoysType, 2)
        self.assertEqual(mission.fnudSonobuoysCoverMul, 3.0)

    def test_add_plan_way_to_mission(self):
        """为任务分配预设航线"""
        mission = self.red_side.get_missions_by_name('空中巡逻')
        self.red_side.add_plan_way(0, '单元航线-新')
        # 出航航线
        mission.add_plan_way_to_mission(0, '单元航线-新')
        # 返航航线
        mission.add_plan_way_to_mission(2, '单元航线-新')
        # 巡逻航线
        mission.add_plan_way_to_mission(3, '单元航线-新')
        self.env.step()
        sideways = self.red_side.get_sideways()
        side_way_unit = common.get_obj_by_name(sideways, '单元航线-新')
        self.assertEqual(mission.m_strSidePatrolWayGUID, side_way_unit.strGuid)
        self.assertEqual(mission.m_strSideRTBWayGUID, side_way_unit.strGuid)
        self.assertEqual(mission.m_strSideWayGUID, side_way_unit.strGuid)

    def test_set_flight_size_aircraft(self):
        """飞机编队规模"""
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.set_flight_size(4)
        self.env.step()
        self.assertEqual(mission.m_FlightSize, 4)

    def test_set_use_refuel_unrep(self):
        """空中加油"""
        mission = self.red_side.get_missions_by_name('空中巡逻')
        doctrine = mission.get_doctrine()
        # 不允许加油
        mission.set_use_refuel_unrep(1)
        self.env.step()
        self.assertEqual(1, doctrine.m_UseRefuel)
        # 允许
        mission.set_use_refuel_unrep(2)
        self.env.step()
        self.assertEqual(2, doctrine.m_UseRefuel)
        # 0--允许但不允许给加油机加油
        mission.set_use_refuel_unrep(0)
        self.env.step()
        self.assertEqual(0, doctrine.m_UseRefuel)

    def test_set_group_size(self):
        """设置巡逻任务水面舰艇/潜艇编队规模"""
        mission = self.red_side.get_missions_by_name('空中巡逻')
        mission.set_group_size(6)
        self.env.step()
        self.assertEqual(mission.m_GroupSize, 6)


if __name__ == '__main__':
    TestPatrolMission.main()


