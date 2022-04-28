# 时间 : 2021/08/26 11:59
# 作者 : 张志高
# 文件 : mozi_server_test
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from mozi_ai_sdk.test.utils.test_framework import TestFramework


class TestMoziServer(TestFramework):
    """测试推演类"""

    def test_set_simulate_compression(self):
        """设置想定推演倍速"""
        # 0-1倍速，1-2倍速，2-5倍速，3-15倍速，4-30倍速，5-60倍速，6-300倍速，7-900倍速，8-1800倍速
        self.scenario.mozi_server.set_simulate_compression(0)
        self.scenario.mozi_server.set_simulate_compression(1)
        self.scenario.mozi_server.set_simulate_compression(2)
        self.scenario.mozi_server.set_simulate_compression(3)
        self.scenario.mozi_server.set_simulate_compression(4)
        self.scenario.mozi_server.set_simulate_compression(5)
        self.scenario.mozi_server.set_simulate_compression(6)
        self.scenario.mozi_server.set_simulate_compression(7)
        self.scenario.mozi_server.set_simulate_compression(8)
        pass

    def test_set_run_mode(self):
        """设置python端与墨子服务端的交互模式"""
        # true 同步模式,false 异步模式
        self.scenario.mozi_server.set_run_mode(True)    # 一般用于训练
        self.scenario.mozi_server.set_run_mode(False)   # 一般用于对战
        print(1234)

    def test_set_simulate_mode(self):
        """设置想定推演模式"""
        # True：非脉冲式推进（尽快），False:脉冲式推进（一般）
        self.scenario.mozi_server.set_simulate_mode(False)
        self.scenario.mozi_server.set_simulate_mode(True)
        print(1234)

    def test_set_decision_step_length(self):
        """设置决策间隔"""
        # 决策步长
        self.scenario.mozi_server.set_decision_step_length(20)
        self.env.step()
        time_1 = self.scenario.get_current_time()
        self.env.step()
        time_2 = self.scenario.get_current_time()
        self.assertEqual(int(time_2) - int(time_1), 20)

    def test_in_de_crease_simulate_compression(self):
        """推演时间步长提高/降低"""
        # 推演步长
        self.scenario.mozi_server.increase_simulate_compression()
        self.scenario.mozi_server.decrease_simulate_compression()
        self.env.step()

    def test_creat_new_scenario(self):
        """新建想定"""
        # 新建想定
        self.scenario.mozi_server.creat_new_scenario()
        self.env.step()

    def test_key_value(self):
        """添加、获取预设的“键-值”表"""
        self.scenario.mozi_server.set_key_value('test_key', 'test_value')
        value = self.scenario.mozi_server.get_value_by_key('test_key')
        self.env.step()
        self.assertEqual(value, 'test_value')
