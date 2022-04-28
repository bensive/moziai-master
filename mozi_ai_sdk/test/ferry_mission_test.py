# 时间 : 2021/09/08 15:30
# 作者 : 张志高
# 文件 : ferry_mission_test
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from mozi_ai_sdk.test.utils.test_framework import TestFramework
from mozi_ai_sdk.test.utils import common


class TestFerryMission(TestFramework):
    """测试转场任务类"""

    def test_add_plan_way_to_mission(self):
        """为任务分配预设航线"""
        self.red_side.add_plan_way(0, '单元航线-新')
        mission = self.red_side.get_missions_by_name('转场')
        # 出航航线
        mission.add_plan_way_to_mission(0, '单元航线-新')
        self.env.step()
        sideways = self.red_side.get_sideways()
        side_way = common.get_obj_by_name(sideways, '单元航线-新')
        self.assertEqual(mission.m_strSideWayGUID, side_way.strGuid)

    def test_set_ferry_behavior(self):
        mission = self.red_side.get_missions_by_name('转场')
        mission.set_ferry_behavior('Cycle')
        self.env.step()
        self.assertEqual(mission.m_FerryMissionBehavior, 1)
        mission.set_ferry_behavior('OneWay')
        self.env.step()
        self.assertEqual(mission.m_FerryMissionBehavior, 0)
        mission.set_ferry_behavior('Random')
        self.env.step()
        self.assertEqual(mission.m_FerryMissionBehavior, 2)

    def test_get_doctrine(self):
        """获取任务条令"""
        # TODO 转场任务属性中条令为空
        mission = self.red_side.get_missions_by_name('转场')
        doctrine = mission.get_doctrine()
        self.assertEqual(doctrine.m_DoctrineOwner, mission.strGuid)

        # 设置对空限制开火
        doctrine.set_weapon_control_status('weapon_control_status_air', 2)
        self.env.step()
        self.assertEqual(2, doctrine.m_WCS_Air)

    def test_set_is_active(self):
        """设置是否启用任务"""
        mission = self.red_side.get_missions_by_name('转场')
        mission.set_is_active('true')
        self.env.step()
        self.assertEqual(0, mission.m_MissionStatus)
        mission.set_is_active('false')
        self.env.step()
        self.assertEqual(1, mission.m_MissionStatus)

    def test_set_time(self):
        """设置任务时间"""
        mission = self.red_side.get_missions_by_name('转场')
        mission.set_start_time('2021-07-19 22:10:00')
        mission.set_end_time('2021-07-19 23:10:00')
        self.env.step()
        self.env.step()
        self.assertEqual(mission.m_EndTime, 1626707400)
        self.assertEqual(mission.m_StartTime, 1626703800)
        self.assertEqual(mission.m_EndTime - mission.m_StartTime, 3600)

    def test_set_ferry_throttle_altitude(self):
        """设置转场任务油门和高度"""
        mission = self.red_side.get_missions_by_name('转场')
        # 军用
        mission.set_ferry_throttle_aircraft('Full')
        mission.set_ferry_altitude_aircraft(6000.1)
        self.env.step()
        self.assertEqual(mission.m_FerryThrottle_Aircraft, 3)
        self.assertEqual(mission.strTransitAltitude_Aircraft, '6000.1')

