# 时间 : 2021/08/18 9:18
# 作者 : 张志高
# 文件 : weapon_test
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import unittest
from mozi_ai_sdk.test.env.env import Environment
from mozi_ai_sdk.test.env import etc as config
import os


class TestWeapon(unittest.TestCase):
    """测试武器"""

    def setUp(self):
        print("--------------- CASE START ----------------------------")

        os.environ['MOZIPATH'] = config.MOZI_PATH
        self.env = Environment(config.SERVER_IP, config.SERVER_PORT, config.SERVER_PLAT,
                               config.SCENARIO_NAME_WEAPON_TEST,
                               config.SIMULATE_COMPRESSION, config.DURATION_INTERVAL, config.SYNCHRONOUS)

        self.env.start()
        self.scenario = self.env.reset()

        self.red_side = self.scenario.get_side_by_name("红方")

        self.weapon_1 = self.red_side.get_unit_by_guid('53c87315-c645-4a0d-abd6-0fd2cfaf07b5')

    def tearDown(self):
        print("--------------- CASE END ----------------------------")

    def test_get_summary_info(self):
        """获取精简信息, 提炼信息进行决策"""
        info = self.weapon_1.get_summary_info()
        self.env.step()

