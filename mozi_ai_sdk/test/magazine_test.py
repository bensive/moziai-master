from mozi_ai_sdk.test.utils.test_framework import TestFramework
from mozi_ai_sdk.test.utils import common


class TestMagazine(TestFramework):
    """测试弹药库"""

    def test_set_magazine_state(self):
        """设置弹药库状态"""
        magazines = self.ground_to_air_missile_squadron.get_magazines()
        magazine = common.get_obj_by_name(magazines, '“毒刺”肩射地空导弹')

        # 设置弹药库状态为已被摧毁
        magazine.set_magazine_state('摧毁')
        self.env.step()
        self.assertEqual(magazine.m_ComponentStatus, 2)

    def test_remove_weapon(self):
        """设置弹药库状态"""
        magazines = self.ground_to_air_missile_squadron.get_magazines()
        magazine = common.get_obj_by_name(magazines, '“毒刺”肩射地空导弹')
        weapon_guid = magazine.m_LoadRatio.split('$')[0]
        magazine.remove_weapon(weapon_guid)
        self.env.step()
        self.assertTrue(weapon_guid not in magazine.m_LoadRatio)
