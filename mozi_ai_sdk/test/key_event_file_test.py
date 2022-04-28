# 时间 : 2021/09/01 9:09
# 作者 : 张志高
# 文件 : key_event_file_test
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from mozi_ai_sdk.test.env.env import Environment
from mozi_ai_sdk.test.env import etc
import os
from mozi_ai_sdk.test.utils.test_framework import TestFramework


class TestKeyEventFile(TestFramework):
    """测试智能体关键事件写入功能"""

    def setUp(self):
        os.environ['MOZIPATH'] = etc.MOZI_PATH

    def test_key_event_file(self):
        """有文件的情况"""
        key_event_file = 'D:/event.txt'
        self.env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.SERVER_PLAT,
                               etc.SCENARIO_NAME_ACTIVE_UNIT_TEST, 6,
                               180, etc.SYNCHRONOUS, etc.app_mode, key_event_file, platform_mode='develop')

        self.env.start()
        self.scenario = self.env.reset()
        self.red_side = self.scenario.get_side_by_name("红方")

        while not self.env.is_done():
            self.env.step()
        # 结果验证
        # 文件D:/event.txt存在
        # 第一行为"成功连接墨子推演服务器！"
        # 中间行为"当前是第N步" N为10的倍数
        # 最后一行为"推演结束！"

    def test_key_event_file_2(self):
        """没有文件的情况"""
        self.env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.SERVER_PLAT,
                               etc.SCENARIO_NAME_ACTIVE_UNIT_TEST, 6,
                               180, etc.SYNCHRONOUS, etc.app_mode)

        self.env.start()
        self.scenario = self.env.reset()
        self.red_side = self.scenario.get_side_by_name("红方")

        # while not self.env.is_done():
        #     self.env.step()
        # 结果验证： 推演过程不报错"

    def test_platform_mode_versus(self):
        """测试比赛模式"""
        key_event_file = 'D:/event.txt'
        platform_mode = 'versus'
        # 推进速度由第三方指定
        self.env = Environment(etc.SERVER_IP, etc.SERVER_PORT, duration_interval=180, app_mode=2,
                               agent_key_event_file=key_event_file, platform_mode=platform_mode)

        self.env.start()
        self.scenario = self.env.reset()
        self.red_side = self.scenario.get_side_by_name("红方")

        while not self.env.is_done():
            self.env.step()
        # 结果验证： 推演过程不报错"
