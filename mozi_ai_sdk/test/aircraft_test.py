
from mozi_ai_sdk.test.utils.test_framework import TestFramework


class TestAirCraft(TestFramework):
    """测试飞机"""

    def test_get_valid_weapons(self):
        """获取飞机有效的武器"""
        # TODO 接口暂不可用
        weapons = self.antisubmarine_aircraft.get_valid_weapons()
        print(weapons)

    def test_get_summary_info(self):
        """获取信息"""
        info = self.antisubmarine_aircraft.get_summary_info()
        self.assertEqual(info['guid'], self.antisubmarine_aircraft.strGuid)

    def test_get_status_type(self):
        """获取状态"""
        type_name = self.antisubmarine_aircraft.get_status_type()
        self.assertEqual(type_name, 'InAir')
        type_name = self.docked_f35_1.get_status_type()
        self.assertEqual(type_name, 'validToFly')

    def test_set_waypoint(self):
        """设置下一个航路点"""
        lat = 26.0728267704942
        lon = 125.582813973341
        self.antisubmarine_aircraft.set_waypoint(lon, lat)
        self.env.step()

        way_points_info = self.antisubmarine_aircraft.get_way_points_info()
        self.assertEqual(way_points_info[0]['latitude'], lat)
        self.assertEqual(way_points_info[0]['longitude'], lon)

    def test_ops_single_out(self):
        """单机出动"""
        self.docked_f35_1.ops_single_out()
        self.env.step()
        self.assertEqual(self.docked_f35_1.strActiveUnitStatus, '状态: 未分配任务 (正在滑行准备起飞)')

    def test_deploy_dipping_sonar(self):
        """投放吊放声呐"""
        # 部署吊放声呐
        self.aircraft_dipping_sonar.deploy_dipping_sonar()
        self.env.step()
        self.assertTrue('部署吊放声呐' in self.aircraft_dipping_sonar.strActiveUnitStatus)

    def test_set_airborne_time(self):
        """设置留空时间"""
        self.antisubmarine_aircraft.set_airborne_time(1, 40, 30)
        self.env.step()
        self.assertTrue('1小时40分飞行时间' in self.antisubmarine_aircraft.strFuelState)

    def test_time_to_ready(self):
        """设置飞机出动准备时间"""
        self.docked_f35_1.time_to_ready('01:02:03')
        self.env.step()
        int_seconds = 3 * 60 + 2 * 3600 + 1 * 3600 * 24
        int_time = int(self.docked_f35_1.strFinishPrepareTime)
        self.assertTrue(int_time < int_seconds)
        self.assertTrue(int_time > int_seconds - 60)

    def test_quick_turnaround(self):
        """设置飞机快速出动"""
        self.antisubmarine_aircraft.quick_turnaround('true', 0)
        self.env.step()
        self.assertEqual(self.antisubmarine_aircraft.strQuickTurnAroundInfo, '支持, 白天/夜间: 1 / 2波次, 0 / 4小时飞行时间, 无维修时间')

    def test_ready_immediately(self):
        """准备出动"""
        # 设置挂载方案为 Mk84低阻力通用炸弹, 外部挂载
        # 支持快速出动  EnableQuickTurnarour
        # 快速出动值    comboBox
        # 立即准备完毕  immediatelyGo
        # 是否不含可选武器  optionalWeapon
        # 是否不忽略弹药库  ignoreWeapon
        self.docked_f35_1.ready_immediately(loadout_dbid=2995, enable_quick_turnaround='true', combo_box=-1,
                                            immediately_go='true', optional_weapon='false', ignore_weapon='false')
        self.env.step()
        loadout = self.docked_f35_1.get_loadout()
        self.assertTrue('2995' in loadout.strDBGUID)

    def test_get_loadout(self):
        loadout = self.antisubmarine_aircraft.get_loadout()
        loadout_name = 'AGM-84C型“鱼叉”反舰导弹, “霍尼韦尔”Mk46 Mod 5 “尼尔蒂普”型鱼雷, AN/SSQ-53A型定向频率分析和记录被动' \
                       '声呐浮标, AN/SSQ-62A型定向指令主动声呐浮标, AN/SSQ-77A型垂直线列阵声呐浮标'
        self.assertEqual(loadout.strName, loadout_name)

    def test_ok_ready_mission(self):
        """飞机按对应的挂载方案所需准备时间完成出动准备"""
        self.docked_f35_1.ok_ready_mission('false', -1)
        self.env.step()
        self.assertTrue(int(self.docked_f35_1.strFinishPrepareTime) < 21600)
        self.assertTrue(int(self.docked_f35_1.strFinishPrepareTime) > 21500)

    def test_abort_launch(self):
        """让正在出动中的飞机立即终止出动"""
        self.docked_f35_1.ops_single_out()
        self.env.step()
        self.assertEqual(self.docked_f35_1.strActiveUnitStatus, '状态: 未分配任务 (正在滑行准备起飞)')

        self.docked_f35_1.abort_launch()
        self.env.step()
        self.assertEqual(self.docked_f35_1.strActiveUnitStatus, '状态: 未分配任务 (停放状态)')

    def test_refuel(self):
        """自动加油"""
        # 设置飞机剩余油量为2000公斤
        self.refuel_aircraft.set_fuel_qty(2000)
        self.refuel_aircraft.refuel()
        self.env.step()
        self.env.step()
        # 距离受油机2较近，选择受油机2加油
        self.assertEqual(self.refuel_aircraft.strActiveUnitStatus, '状态: 正赶赴加油点 (加油对象: 加油机2) (机动到加油阵位)')

    def test_refuel_manual(self):
        """手动加油"""
        # 设置飞机剩余油量为2000公斤
        self.refuel_aircraft.set_fuel_qty(2000)
        self.refuel_aircraft.refuel(self.refueling_tanker_aircraft_guid)
        self.env.step()
        self.env.step()
        # 选择了受油机加油
        self.assertEqual(self.refuel_aircraft.strActiveUnitStatus, '状态: 正赶赴加油点 (加油对象: 加油机) (机动到加油阵位)')


if __name__ == '__main__':
    TestAirCraft.main()
