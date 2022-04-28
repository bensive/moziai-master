# 时间 : 2021/08/25 16:46
# 作者 : 张志高
# 文件 : support_mission_test
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from mozi_ai_sdk.test.utils.test_framework import TestFramework


class TestSupportMission(TestFramework):
    """测试支援任务类"""

    def test_add_plan_way_to_mission(self):
        """为任务分配预设航线"""
        self.red_side.add_plan_way(0, '单元航线-新')
        self.env.step()

        mission = self.red_side.get_missions_by_name('加油任务')
        # 出航航线
        mission.add_plan_way_to_mission(0, '单元航线-新')
        # 返航航线
        mission.add_plan_way_to_mission(2, '单元航线-新')
        self.env.step()

    def test_assign_unit(self):
        """设置作战单元及打击或护航角色"""
        mission = self.red_side.get_missions_by_name('加油任务')
        mission.assign_unit(self.antisubmarine_aircraft_guid)
        self.env.step()

    def test_set_maintain_unit_number(self):
        """阵位上每类平台保持几个作战单元"""
        mission = self.red_side.get_missions_by_name('加油任务')
        mission.set_maintain_unit_number(2)
        self.env.step()

    def test_get_doctrine(self):
        """获取任务条令"""
        mission = self.red_side.get_missions_by_name('加油任务')
        doctrine = mission.get_doctrine()
        self.assertEqual(doctrine.m_DoctrineOwner, mission.strGuid)

        # 设置对空限制开火
        doctrine.set_weapon_control_status('weapon_control_status_air', 2)
        self.env.step()
        self.assertEqual(2, doctrine.m_WCS_Air)

    def test_set_is_active(self):
        """设置是否启用任务"""
        mission = self.red_side.get_missions_by_name('加油任务')
        mission.set_is_active('true')
        self.env.step()
        self.assertEqual(0, mission.m_MissionStatus)
        mission.set_is_active('false')
        self.env.step()
        self.assertEqual(1, mission.m_MissionStatus)

    def test_set_time(self):
        """设置任务时间"""
        mission = self.red_side.get_missions_by_name('加油任务')
        mission.set_start_time('2021-07-19 22:10:00')
        mission.set_end_time('2021-07-19 23:10:00')
        self.env.step()

    def test_set_one_time_only(self):
        """是否仅一次"""
        mission = self.red_side.get_missions_by_name('加油任务')
        mission.set_one_time_only('true')
        self.env.step()
        mission.set_one_time_only('false')
        self.env.step()

    def test_set_loop_type(self):
        """导航类型"""
        mission = self.red_side.get_missions_by_name('加油任务')
        mission.set_loop_type('true')
        self.env.step()
        mission.set_loop_type('false')
        self.env.step()

    def test_set_flight_size(self):
        """编队规模"""
        mission = self.red_side.get_missions_by_name('加油任务')
        mission.set_flight_size(1)
        self.env.step()
        mission.set_flight_size(2)
        self.env.step()
        mission.set_flight_size(3)
        self.env.step()
        mission.set_flight_size(4)
        self.env.step()
        mission.set_flight_size(6)
        self.env.step()

    def test_set_flight_size_check(self):
        """是否低于编队规模不能起飞"""
        mission = self.red_side.get_missions_by_name('加油任务')
        mission.set_flight_size_check('true')
        self.env.step()
        mission.set_flight_size_check('false')
        self.env.step()

    def test_set_throttle_altitude(self):
        """设置油门和高度"""
        mission = self.red_side.get_missions_by_name('加油任务')
        # 出航-巡航
        mission.set_throttle_transit('Cruise')
        # 阵位 - 军用
        mission.set_throttle_station('Full')
        # 出航高度
        mission.set_transit_altitude(1000)
        # 阵位高度
        mission.set_station_altitude(2000)
        self.env.step()

    def test_set_emcon_usage(self):
        """设置任务是否在阵位上打开电磁辐射"""
        mission = self.red_side.get_missions_by_name('加油任务')
        mission.set_emcon_usage('true')
        self.env.step()

    def test_add_plan_way_to_mission(self):
        """为任务分配预设航线"""
        mission = self.red_side.get_missions_by_name('加油任务')
        self.red_side.add_plan_way(0, '单元航线-新')
        # 出航航线
        mission.add_plan_way_to_mission(0, '单元航线-新')
        # 返航航线
        mission.add_plan_way_to_mission(2, '单元航线-新')
        self.env.step()

    def test_set_flight_size(self):
        """飞机编队规模"""
        mission = self.red_side.get_missions_by_name('加油任务')
        mission.set_flight_size(4)
        self.env.step()

    def test_set_use_refuel_unrep(self):
        """空中加油"""
        mission = self.red_side.get_missions_by_name('加油任务')
        # 不允许加油
        mission.set_use_refuel_unrep(1)
        self.env.step()
        # 允许
        mission.set_use_refuel_unrep(2)
        self.env.step()
        # 0--允许但不允许给加油机加油
        mission.set_use_refuel_unrep(0)
        self.env.step()

    def test_set_throttle_ship(self):
        """设置任务的水面舰艇油门"""
        mission = self.red_side.get_missions_by_name('加油任务')
        # 出航-巡航
        mission.set_throttle_transit_ship('Cruise')
        # 阵位 - 全速
        mission.set_throttle_station_ship('Full')
        self.env.step()

    def test_set_throttle_submarine(self):
        """设置任务的潜艇油门"""
        mission = self.red_side.get_missions_by_name('加油任务')
        # 出航-巡航
        mission.set_throttle_transit_submarine('Cruise')
        # 阵位 - 全速
        mission.set_throttle_station_submarine('Full')
        self.env.step()

    def test_set_group_size(self):
        """设置任务水面舰艇/潜艇编队规模"""
        mission = self.red_side.get_missions_by_name('加油任务')
        mission.set_group_size(6)
        self.env.step()
        # 查看墨子， 空中巡逻任务水面舰艇/潜艇编队规模为6x艇

    def test_set_submarine_depth(self):
        mission = self.red_side.get_missions_by_name('加油任务')
        # 设置出航潜深
        mission.set_submarine_depth('transitDepthSubmarine', -100)
        # 设置阵位潜深
        mission.set_submarine_depth('stationDepthSubmarine', -50)
        self.env.step()


