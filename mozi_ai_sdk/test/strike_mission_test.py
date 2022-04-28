# 时间 : 2021/08/25 11:24
# 作者 : 张志高
# 文件 : strike_mission_test
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from mozi_ai_sdk.test.utils.test_framework import TestFramework


class TestStrikeMission(TestFramework):
    """测试打击任务类"""

    def test_assign_unit(self):
        """设置作战单元及打击或护航角色"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.assign_unit_as_target(self.enemy_airplane_guid)
        mission.assign_unit(self.antisubmarine_aircraft_guid)
        mission.assign_unit(self.antisubmarine_aircraft_2_guid, True)
        self.env.step()

    def test_assign_unit_as_target(self):
        """分配目标"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.assign_unit_as_target(self.enemy_airplane_guid)
        self.env.step()

    def test_get_doctrine(self):
        """获取任务条令"""
        mission = self.red_side.get_missions_by_name('空中打击')
        doctrine = mission.get_doctrine()
        self.assertEqual(doctrine.m_DoctrineOwner, mission.strGuid)

        # 设置对空限制开火
        doctrine.set_weapon_control_status('weapon_control_status_air', 2)
        self.env.step()
        self.assertEqual(2, doctrine.m_WCS_Air)

    def test_set_is_active(self):
        """设置是否启用任务"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.set_is_active('true')
        self.env.step()
        self.assertEqual(0, mission.m_MissionStatus)
        mission.set_is_active('false')
        self.env.step()
        self.assertEqual(1, mission.m_MissionStatus)

    def test_set_time(self):
        """设置任务时间"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.set_start_time('2021-07-19 22:10:00')
        mission.set_end_time('2021-07-19 23:10:00')
        self.env.step()

    def test_add_plan_way_to_mission(self):
        """为任务分配预设航线"""
        self.red_side.add_plan_way(0, '单元航线-新')
        self.red_side.add_plan_way(1, '武器航线-新')
        self.env.step()

        mission = self.red_side.get_missions_by_name('空中打击')
        # 出航航线
        mission.add_plan_way_to_mission(0, '单元航线-新')
        # 返航航线
        mission.add_plan_way_to_mission(2, '单元航线-新')
        # 武器航线
        mission.add_plan_way_to_mission(1, '武器航线-新')
        self.env.step()

    def test_get_targets(self):
        """返回任务打击目标"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.assign_unit_as_target(self.enemy_airplane_guid)
        self.env.step()
        targets = mission.get_targets()
        self.assertTrue(targets)
        for k, v in targets.items():
            self.assertEqual(k, self.enemy_airplane_guid)

    def test_set_preplan(self):
        """设置任务细节：是否仅考虑计划目标（在目标清单）"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.set_preplan(True)
        self.env.step()
        mission.set_preplan(False)
        self.env.step()

    def test_set_minimum_trigger(self):
        """设置打击任务触发条件, 探测目标至少为不明、非友、敌对"""
        mission = self.red_side.get_missions_by_name('空中打击')
        # 空
        mission.set_minimum_trigger(1)
        self.env.step()
        # 非友
        mission.set_minimum_trigger(2)
        self.env.step()
        # 敌对
        mission.set_minimum_trigger(3)
        self.env.step()
        # 不明
        mission.set_minimum_trigger(4)
        self.env.step()

    def test_set_strike_max(self):
        """设置任务细节：任务允许出动的最大飞行批次"""
        mission = self.red_side.get_missions_by_name('空中打击')
        # 空
        mission.set_strike_max(0)
        self.env.step()
        mission.set_strike_max(1)
        self.env.step()
        mission.set_strike_max(2)
        self.env.step()
        mission.set_strike_max(3)
        self.env.step()
        mission.set_strike_max(4)
        self.env.step()
        mission.set_strike_max(6)
        self.env.step()
        mission.set_strike_max(8)
        self.env.step()
        mission.set_strike_max(12)
        self.env.step()
        mission.set_strike_max('all')
        self.env.step()

    def test_set_flight_size(self):
        """飞机编队规模"""
        mission = self.red_side.get_missions_by_name('空中打击')
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

    def test_set_min_aircrafts_required(self):
        """设置打击任务设置打击任务所需最少就绪飞机数"""
        mission = self.red_side.get_missions_by_name('空中打击')
        # 空
        mission.set_min_aircrafts_required(0)
        self.env.step()
        mission.set_min_aircrafts_required(1)
        self.env.step()
        mission.set_min_aircrafts_required(2)
        self.env.step()
        mission.set_min_aircrafts_required(3)
        self.env.step()
        mission.set_min_aircrafts_required(4)
        self.env.step()
        mission.set_min_aircrafts_required(6)
        self.env.step()
        mission.set_min_aircrafts_required(8)
        self.env.step()
        mission.set_min_aircrafts_required(12)
        self.env.step()
        mission.set_min_aircrafts_required('all')
        self.env.step()

    def test_set_radar_usage(self):
        """设置打击任务雷达运用规则"""
        mission = self.red_side.get_missions_by_name('空中打击')
        # 从初始点到武器消耗光打开雷达
        mission.set_radar_usage(2)
        self.env.step()
        # 整个飞行计划遵循任务电磁管控规则
        mission.set_radar_usage(1)
        self.env.step()
        # 从进入攻击航线段到武器消耗完毕状态点打开雷达
        mission.set_radar_usage(3)
        self.env.step()

    def test_set_fuel_ammo(self):
        """设置打击任务燃油弹药规则"""
        mission = self.red_side.get_missions_by_name('空中打击')
        # 根据每个挂载方案的设置决定是消耗/抛弃还是带回空地弹药，
        mission.set_fuel_ammo(0)
        self.env.step()
        # 在最远距离上抛弃空对地弹药，以获取最大打击
        mission.set_fuel_ammo(1)
        self.env.step()
        # 如果不能打击目标，则带回空对地弹药
        mission.set_fuel_ammo(2)
        self.env.step()

    def test_strike_radius(self):
        """设置打击任务最小/大打击半径"""
        mission = self.red_side.get_missions_by_name('空中打击')
        # 最小打击半径
        mission.set_min_strike_radius(200)
        self.env.step()
        # 最大打击半径
        mission.set_max_strike_radius(300)
        self.env.step()

    def test_set_flight_size_check(self):
        """设置打击任务是否飞机数低于编组规模数要求就不能起飞"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.set_flight_size_check('true')
        self.env.step()
        mission.set_flight_size_check('false')
        self.env.step()

    def test_set_auto_planner(self):
        """设置打击任务是否离轴攻击"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.set_auto_planner('true')
        self.env.step()
        mission.set_auto_planner('false')
        self.env.step()

    def test_set_auto_planner(self):
        """设置打击任务是否仅限一次"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.set_strike_one_time_only('true')
        self.env.step()
        mission.set_strike_one_time_only('false')
        self.env.step()

    def test_set_use_refuel_unrep(self):
        """空中加油"""
        mission = self.red_side.get_missions_by_name('空中打击')
        # 不允许加油
        mission.set_use_refuel_unrep(1)
        self.env.step()
        # 允许
        mission.set_use_refuel_unrep(2)
        self.env.step()
        # 0--允许但不允许给加油机加油
        mission.set_use_refuel_unrep(0)
        self.env.step()

    def test_set_strike_escort_flight_size_shooter(self):
        """设置打击任务护航飞机设置编队规模"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.set_strike_escort_flight_size_shooter(4)
        self.env.step()
        # 查看墨子, 护航编队规模为4机编队

    def test_set_strike_escort_flight_size_shooter(self):
        """设置打击任务护航最大威胁响应半径"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.set_strike_escort_response_radius(200)
        self.env.step()
        # 查看墨子， 空中打击任务护航最大威胁响应半径370.4公里

    def test_set_strike_group_size(self):
        """设置打击任务水面舰艇/潜艇编队规模"""
        mission = self.red_side.get_missions_by_name('空中打击')
        mission.set_strike_group_size(6)
        self.env.step()
        # 查看墨子， 空中打击任务水面舰艇/潜艇编队规模为6x艇


if __name__ == '__main__':
    TestStrikeMission.main()
