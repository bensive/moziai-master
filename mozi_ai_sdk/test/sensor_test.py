
from mozi_ai_sdk.test.utils.test_framework import TestFramework


class TestSensor(TestFramework):
    """测试传感器"""

    def test_switch(self):
        """设置单个传感器开关"""
        sensors = self.aircraft_dipping_sonar.get_sensor()
        self.aircraft_dipping_sonar.unit_obeys_emcon('false')

        sensor_test = None
        for k, sensor in sensors.items():
            if 'J/HPS-104型搜索雷达' == sensor.strName:
                sensor_test = sensor

        if not sensor_test:
            self.assertTrue(False, "未找到对应的传感器")

        sensor_test.switch('true')
        self.env.step()
        self.assertTrue(sensor_test.bActive)

