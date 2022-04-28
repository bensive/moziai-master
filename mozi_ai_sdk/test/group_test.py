
from mozi_ai_sdk.test.utils.test_framework import TestFramework
from mozi_ai_sdk.test.utils import common


class TestGroup(TestFramework):
    """测试编组"""

    def test_get_units(self):
        """获取编组下单元"""
        units = self.air_group.get_units()
        count = 0
        for k, v in units.items():
            count += 1
            self.assertTrue(k in [self.air_group_unit_guid_1, self.air_group_unit_guid_2])
            self.assertTrue(v in [self.antisubmarine_aircraft_3, self.antisubmarine_aircraft_4])
        self.assertEqual(count, 2)

    def test_add_unit(self):
        """编队添加一个单元"""
        # 将反潜机1加入编组
        self.air_group.add_unit(self.antisubmarine_aircraft_guid)
        self.env.step()
        units = self.air_group.get_units()
        count = 0
        for k, v in units.items():
            count += 1
            self.assertTrue(k in [self.air_group_unit_guid_1, self.air_group_unit_guid_2,
                                  self.antisubmarine_aircraft_guid])
        self.assertEqual(count, 3)

    def test_remove_unit(self):
        """将单元移除编组"""
        # 将反潜机4移除编组
        self.air_group.remove_unit(self.air_group_unit_guid_2)
        self.env.step()
        units = self.air_group.get_units()
        count = 0
        for k, v in units.items():
            count += 1
            self.assertTrue(k in [self.air_group_unit_guid_1])
            self.assertTrue(v in [self.antisubmarine_aircraft_3])
        self.assertEqual(count, 1)

    def test_set_formation_group_lead(self):
        """设置编队领队"""
        self.ship_group.set_formation_group_lead('日本舰船2')
        self.env.step()
        self.assertEqual(self.red_side.get_ships()[self.ship_group.m_GroupLead].strName, '日本舰船2')

    def test_set_formation_group_member(self):
        """设置编队队形"""
        self.ship_group.set_formation_group_member('日本舰船2', 'Rotating', 60, 2)
        self.env.step()
        ships = self.red_side.get_ships()
        ship = common.get_obj_by_name(ships, '日本舰船2')
        while True:
            self.env.step()

    def test_set_unit_sprint_and_drift(self):
        """控制编队内非领队单元相对于编队是否进行高低速交替航行"""
        self.ship_group.set_unit_sprint_and_drift(self.ship_japan_1_guid, 'true')
        self.env.step()


if __name__ == '__main__':
    TestGroup.main()


