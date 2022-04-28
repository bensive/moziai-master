
from mozi_ai_sdk.test.utils.test_framework import TestFramework


class TestAirFacility(TestFramework):
    """测试地面兵力设施"""

    def test_get_summary_info(self):
        """获取精简信息, 提炼信息进行决策"""
        info = self.ground_to_air_missile_squadron.get_summary_info()
        self.assertEqual(info['name'], self.ground_to_air_missile_squadron.strName)
