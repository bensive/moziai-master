# 时间 : 2021/08/09 15:46
# 作者 : 张志高
# 文件 : scenario_test
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from mozi_ai_sdk.test.utils.test_framework import TestFramework


class TestScenario(TestFramework):
    """测试想定类"""

    def test_set_weather(self):
        """设置天气"""
        self.env.step()
        self.scenario.set_weather(50, 50, 1.0, 9)
        self.env.step()
        weather = self.scenario.get_weather()
        self.assertEqual(weather.dTemperature, 50.0)
        self.assertEqual(weather.fRainFallRate, 50.0)
        self.assertEqual(weather.fSkyCloud, 1.0)
        self.assertEqual(weather.iSeaState, 9)

        self.scenario.set_weather(-40, 25, 0.5, 4)
        self.env.step()
        weather = self.scenario.get_weather()
        self.assertEqual(weather.dTemperature, -40.0)
        self.assertEqual(weather.fRainFallRate, 25.0)
        self.assertEqual(weather.fSkyCloud, 0.5)
        self.assertEqual(weather.iSeaState, 4)

        self.scenario.set_weather(-50, 0, 0, 0)
        self.env.step()
        weather = self.scenario.get_weather()
        self.assertEqual(weather.dTemperature, -50.0)
        self.assertEqual(weather.fRainFallRate, 0)
        self.assertEqual(weather.fSkyCloud, 0)
        self.assertEqual(weather.iSeaState, 0)

    def test_add_trigger_unit_destroyed(self):
        """添加单元被摧毁触发器"""
        # 设置触发器推演方单元被摧毁
        target_filter_dict = {'TARGETSIDE': '红方'}
        self.scenario.add_trigger_unit_destroyed('红方单元被摧毁', target_filter_dict)

        # 设置触发器红方飞机被摧毁
        target_filter_dict = {'TARGETSIDE': '红方', 'TARGETTYPE': 1}
        self.scenario.add_trigger_unit_destroyed('飞机被摧毁', target_filter_dict)

        # 设置触发器红方潜艇被摧毁
        target_filter_dict = {'TARGETSIDE': '红方', 'TARGETTYPE': 'Submarine'}
        self.scenario.add_trigger_unit_destroyed('潜艇被摧毁', target_filter_dict)

        # 设置触发器红方类型为海上巡逻机的飞机被摧毁
        target_filter_dict = {'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002}
        self.scenario.add_trigger_unit_destroyed('海上巡逻机被摧毁', target_filter_dict)

        # 设置红方数据库名称为P-3C型“猎户座” II反潜机的单元被摧毁
        target_filter_dict = {'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
        self.scenario.add_trigger_unit_destroyed('P-3C型“猎户座” II反潜机被摧毁', target_filter_dict)

        # 设置触发器反潜机1被摧毁
        target_filter_dict = {'SPECIFICUNIT': self.antisubmarine_aircraft.strGuid}
        self.scenario.add_trigger_unit_destroyed('反潜机1被摧毁', target_filter_dict)

        # 设置触发器反潜机2被摧毁
        target_filter_dict = {'SPECIFICUNIT': '反潜机2'}
        self.scenario.add_trigger_unit_destroyed('反潜机2被摧毁', target_filter_dict)
        self.env.step()

    def test_update_trigger_unit_destroyed(self):
        """更新单元被摧毁触发器"""
        # 设置触发器推演方单元被摧毁
        target_filter_dict = {'TARGETSIDE': '红方'}
        self.scenario.add_trigger_unit_destroyed('红方单元被摧毁', target_filter_dict)
        self.env.step()

        # 修改名称和目标
        target_filter_dict = {'TARGETSIDE': '红方', 'TARGETTYPE': 1}
        self.scenario.update_trigger_unit_destroyed('红方单元被摧毁', '飞机被摧毁', target_filter_dict)
        self.env.step()
        # 只修改名称
        self.scenario.update_trigger_unit_destroyed('飞机被摧毁', rename='飞机被摧毁2')
        self.env.step()
        # 只修改目标
        target_filter_dict = {'SPECIFICUNIT': '反潜机2'}
        self.scenario.update_trigger_unit_destroyed('飞机被摧毁2', target_filter_dict=target_filter_dict)
        self.env.step()

    def test_add_trigger_unit_damaged(self):
        """添加单元被毁伤触发器"""
        # 设置触发器推演方单元被摧毁
        target_filter_dict = {'TARGETSIDE': '红方'}
        self.scenario.add_trigger_unit_damaged('红方单元被毁伤10%', target_filter_dict, 10)

        # 设置触发器红方飞机被摧毁
        target_filter_dict = {'TARGETSIDE': '红方', 'TARGETTYPE': 1}
        self.scenario.add_trigger_unit_damaged('飞机被毁伤20%', target_filter_dict, 20)

        # 设置触发器红方潜艇被摧毁
        target_filter_dict = {'TARGETSIDE': '红方', 'TARGETTYPE': 'Submarine'}
        self.scenario.add_trigger_unit_damaged('潜艇被毁伤30%', target_filter_dict, 30)

        # 设置触发器红方类型为海上巡逻机的飞机被摧毁
        target_filter_dict = {'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002}
        self.scenario.add_trigger_unit_damaged('海上巡逻机被毁伤40%', target_filter_dict, 40)

        # 设置红方数据库名称为P-3C型“猎户座” II反潜机的单元被摧毁
        target_filter_dict = {'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
        self.scenario.add_trigger_unit_damaged('P-3C型“猎户座” II反潜机被毁伤50%', target_filter_dict, 50)

        # 设置触发器反潜机1被摧毁
        target_filter_dict = {'SPECIFICUNIT': self.antisubmarine_aircraft.strGuid}
        self.scenario.add_trigger_unit_damaged('反潜机1被毁伤60%', target_filter_dict, 60)

        # 设置触发器反潜机2被摧毁
        target_filter_dict = {'SPECIFICUNIT': '反潜机2'}
        self.scenario.add_trigger_unit_damaged('反潜机2被毁伤100%', target_filter_dict, 100)
        self.env.step()

    def test_update_trigger_unit_damaged(self):
        """编辑单元被毁伤触发器"""
        # 设置触发器推演方单元被摧毁
        target_filter_dict = {'TARGETSIDE': '红方'}
        self.scenario.add_trigger_unit_damaged('红方单元被毁伤10%', target_filter_dict, 10)

        # 设置触发器红方飞机被摧毁
        target_filter_dict = {'TARGETSIDE': '红方', 'TARGETTYPE': 1}
        rename = '飞机被毁伤20%'
        damage_percent = 20
        self.scenario.update_trigger_unit_damaged('红方单元被毁伤10%', rename=rename,
                                                  target_filter_dict=target_filter_dict, damage_percent=damage_percent)
        self.env.step()

    def test_add_trigger_points(self):
        """添加推演方得分触发器"""
        self.scenario.add_trigger_points('推演方得分触发器', '红方', 100, 0)
        self.env.step()

    def test_update_trigger_points(self):
        """编辑推演方得分触发器"""
        # 高于100分
        self.scenario.add_trigger_points('推演方得分触发器', '红方', 100, 0)
        self.env.step()

        rename = '推演方得分触发器-改1'
        # 刚好抵达200分
        self.scenario.update_trigger_points('推演方得分触发器', rename=rename, side='蓝方', point_value=200, reach_direction=1)
        self.env.step()
        rename = '推演方得分触发器-改2'
        # 低于200分
        self.scenario.update_trigger_points('推演方得分触发器-改1', rename=rename, side='蓝方', point_value=200, reach_direction=2)
        self.env.step()

    def test_add_trigger_time(self):
        """添加时间触发器"""
        self.scenario.add_trigger_time('时间触发器', '2021/7/19 10:1:21')
        self.env.step()
        # 实际设置时间为2021/7/19 10:1:21 + 8小时

    def test_update_trigger_time(self):
        """编辑时间触发器"""
        self.scenario.add_trigger_time('时间触发器', '2021/7/19 10:1:21')
        self.env.step()
        # 实际设置时间为2021/7/19 10:1:21 + 8小时
        rename = '时间触发器-新'
        self.scenario.update_trigger_time('时间触发器', rename=rename, time='2021/7/19 11:1:21')
        self.env.step()
        # 更新的时间为为实际时间，没有+8小时

    def test_add_trigger_unit_remains_in_area(self):
        """添加单元区域停留触发器"""
        target_filter_dict = {'SPECIFICUNIT': '反潜机2'}
        area = ['RP-16', 'RP-17', 'RP-18', 'RP-19']
        stay_time = '0:1:2:3'
        self.scenario.add_trigger_unit_remains_in_area('单元区域停留', target_filter_dict, area, stay_time)
        self.env.step()

    def test_update_trigger_unit_remains_in_area(self):
        """编辑单元区域停留触发器"""
        target_filter_dict = {'SPECIFICUNIT': '反潜机2'}
        area = ['RP-16', 'RP-17', 'RP-18', 'RP-19']
        stay_time = '0:1:2:3'
        self.scenario.add_trigger_unit_remains_in_area('单元区域停留', target_filter_dict, area, stay_time)
        self.env.step()

        target_filter_dict = {'SPECIFICUNIT': '反潜机1'}
        area = ['RP-16', 'RP-17', 'RP-18']
        stay_time = '1:2:3:4'
        rename = '单元区域停留-改'
        self.scenario.update_trigger_unit_remains_in_area('单元区域停留', rename=rename,
                                                          target_filter_dict=target_filter_dict,
                                                          area=area, stay_time=stay_time)
        self.env.step()

    def test_add_trigger_unit_enters_area(self):
        """添加单元进入区域触发器"""
        target_filter_dict = {'SPECIFICUNIT': '反潜机2'}
        area = ['RP-16', 'RP-17', 'RP-18', 'RP-19']
        ETOA = '2021/7/19 10:1:21'
        LTOA = '2021/7/19 11:1:21'
        trigger_if_not_in_area = 'true'
        self.scenario.add_trigger_unit_enters_area('单元进入区域', target_filter_dict, area, ETOA, LTOA,
                                                   trigger_if_not_in_area)
        self.env.step()
        # 实际设置时间为2021/7/19 10:1:21 + 8小时

    def test_update_trigger_unit_enters_area(self):
        """编辑单元进入区域触发器"""
        target_filter_dict = {'SPECIFICUNIT': '反潜机2'}
        area = ['RP-16', 'RP-17', 'RP-18', 'RP-19']
        ETOA = '2021/7/19 10:1:21'
        LTOA = '2021/7/19 11:1:21'
        trigger_if_not_in_area = 'true'
        self.scenario.add_trigger_unit_enters_area('单元进入区域', target_filter_dict, area, ETOA, LTOA,
                                                   trigger_if_not_in_area)
        self.env.step()
        # 实际设置时间为2021/7/19 10:1:21 + 8小时
        rename = '单元进入区域-改'
        target_filter_dict = {'SPECIFICUNIT': '反潜机1'}
        area = ['RP-16', 'RP-17', 'RP-18']
        ETOA = '2021/7/19 11:1:21'
        LTOA = '2021/7/19 12:1:21'
        trigger_if_not_in_area = 'false'
        self.scenario.update_trigger_unit_enters_area('单元进入区域', rename=rename, target_filter_dict=target_filter_dict,
                                                      area=area, ETOA=ETOA, LTOA=LTOA,
                                                      trigger_if_not_in_area=trigger_if_not_in_area)
        self.env.step()
        # 实际设置时间为2021/7/19 11:1:21，没有+8小时

    def test_add_trigger_scen_loaded(self):
        """添加想定被加载触发器"""
        self.scenario.add_trigger_scen_loaded('想定被加载')
        self.env.step()

    def test_update_trigger_scen_loaded(self):
        """编辑想定被加载触发器"""
        self.scenario.add_trigger_scen_loaded('想定被加载')
        self.env.step()

        rename = '想定被加载-改'
        self.scenario.update_trigger_scen_loaded('想定被加载', rename)
        self.env.step()

    def test_add_trigger_random_time(self):
        """添加随机时间触发器"""
        earliest_time = '2021/7/19 10:1:21'
        latest_time = '2021/7/19 11:1:21'
        self.scenario.add_trigger_random_time('随机时间', earliest_time, latest_time)
        self.env.step()

    def test_update_trigger_random_time(self):
        """编辑随机时间触发器"""
        earliest_time = '2021/7/19 10:1:21'
        latest_time = '2021/7/19 11:1:21'
        self.scenario.add_trigger_random_time('随机时间', earliest_time, latest_time)
        self.env.step()

        earliest_time = '2021/7/19 11:1:21'
        latest_time = '2021/7/19 12:1:21'
        rename = '随机时间-改'
        self.scenario.update_trigger_random_time('随机时间', rename=rename, earliest_time=earliest_time,
                                                 latest_time=latest_time)
        self.env.step()

    def test_add_trigger_regular_time(self):
        """添加规律时间触发器"""
        self.scenario.add_trigger_regular_time('规律时间1秒', 0)
        self.scenario.add_trigger_regular_time('规律时间5秒', 1)
        self.scenario.add_trigger_regular_time('规律时间15秒', 2)
        self.scenario.add_trigger_regular_time('规律时间30秒', 3)
        self.scenario.add_trigger_regular_time('规律时间1分钟', 4)
        self.scenario.add_trigger_regular_time('规律时间5分钟', 5)
        self.scenario.add_trigger_regular_time('规律时间15分钟', 6)
        self.scenario.add_trigger_regular_time('规律时间30分钟', 7)
        self.scenario.add_trigger_regular_time('规律时间1小时', 8)
        self.scenario.add_trigger_regular_time('规律时间6小时', 9)
        self.scenario.add_trigger_regular_time('规律时间12小时', 10)
        self.scenario.add_trigger_regular_time('规律时间24小时', 11)
        self.scenario.add_trigger_regular_time('规律时间0.1秒', 12)
        self.scenario.add_trigger_regular_time('规律时间0.5秒', 13)
        self.env.step()

    def test_update_trigger_regular_time(self):
        """编辑规律时间触发器"""
        self.scenario.add_trigger_regular_time('规律时间', 1)
        self.env.step()

        rename = '规律时间-改'
        self.scenario.update_trigger_regular_time('规律时间', rename=rename, interval=5)
        self.env.step()

    def test_add_trigger_unit_detected(self):
        """添加单元被探测到触发器"""
        target_filter_dict = {'SPECIFICUNIT': '反潜机2'}
        detector_side = '蓝方'
        # 不明
        self.scenario.add_trigger_unit_detected('单元被探测到0', target_filter_dict, detector_side, 0)
        # 知道领域
        self.scenario.add_trigger_unit_detected('单元被探测到1', target_filter_dict, detector_side, 1)
        # 知道类型
        self.scenario.add_trigger_unit_detected('单元被探测到2', target_filter_dict, detector_side, 2)
        # 知道型号
        self.scenario.add_trigger_unit_detected('单元被探测到3', target_filter_dict, detector_side, 3)
        # 知道具体ID
        self.scenario.add_trigger_unit_detected('单元被探测到4', target_filter_dict, detector_side, 4)
        self.env.step()

    def test_update_trigger_unit_detected(self):
        """编辑单元被探测到触发器"""
        target_filter_dict = {'SPECIFICUNIT': '反潜机2'}
        detector_side = '蓝方'
        # 不明
        self.scenario.add_trigger_unit_detected('单元被探测到0', target_filter_dict, detector_side, 0)
        self.env.step()
        target_filter_dict = {'SPECIFICUNIT': '反潜机1'}
        detector_side = '蓝方'
        # 知道领域
        self.scenario.update_trigger_unit_detected('单元被探测到0', rename='单元被探测到1',
                                                   target_filter_dict=target_filter_dict, detector_side=detector_side,
                                                   MCL=1)
        self.env.step()

    def test_remove_trigger(self):
        """编辑单元被探测到触发器"""
        target_filter_dict = {'SPECIFICUNIT': '反潜机2'}
        detector_side = '蓝方'
        # 不明
        self.scenario.add_trigger_unit_detected('单元被探测到0', target_filter_dict, detector_side, 0)
        self.env.step()
        self.scenario.remove_trigger('单元被探测到0')
        self.env.step()

    def test_add_action_points(self):
        """添加动作推演方得分"""
        detector_side = '红方'
        self.scenario.add_action_points('红方得分100', detector_side, 100)
        self.env.step()

    def test_update_action_points(self):
        """编辑动作推演方得分"""
        detector_side = '红方'
        self.scenario.add_action_points('红方得分100', detector_side, 100)
        self.env.step()
        detector_side = '蓝方'
        rename = '蓝方得分-100'
        # 不明
        self.scenario.update_action_points('红方得分100', rename=rename, side_name=detector_side, point_change=-100)
        self.env.step()

    def test_add_action_end_scenario(self):
        """添加动作终止想定"""
        self.scenario.add_action_end_scenario('想定终止')
        self.env.step()

    def test_update_action_end_scenario(self):
        """编辑动作终止想定"""
        self.scenario.add_action_end_scenario('想定终止')
        self.env.step()
        self.scenario.update_action_end_scenario('想定终止', '想定终止改')
        self.env.step()

    def test_add_action_teleport_in_area(self):
        """添加动作单元瞬时移动"""
        area = ['RP-16', 'RP-17', 'RP-18', 'RP-19']
        unit_list = ['反潜机1', '反潜机2']
        self.scenario.add_action_teleport_in_area('单元瞬时移动', unit_list, area)
        self.env.step()

    def test_update_action_end_scenario(self):
        """编辑动作单元瞬时移动"""
        area = ['RP-16', 'RP-17', 'RP-18', 'RP-19']
        unit_list = ['反潜机1', '反潜机2']
        self.scenario.add_action_teleport_in_area('单元瞬时移动', unit_list, area)
        self.env.step()

        area = ['RP-16', 'RP-17', 'RP-18']
        unit_list = [self.antisubmarine_aircraft_guid, self.aircraft_drop_sonar_guid]
        rename = '单元瞬时移动-改'
        self.scenario.update_action_teleport_in_area('单元瞬时移动', rename=rename, unit_list=unit_list, area=area)
        self.env.step()

    def test_add_action_message(self):
        """添加消息动作"""
        self.scenario.add_action_message('消息', '红方', '消息测试')
        self.env.step()

    def test_update_action_message(self):
        """编辑消息动作"""
        self.scenario.add_action_message('消息', '红方', '消息测试')
        self.env.step()
        rename = '消息-改'
        self.scenario.update_action_message('消息', rename=rename, side='蓝方', text='消息测试-改')
        self.env.step()

    def test_add_action_change_mission_status(self):
        """添加改变任务状态动作"""
        self.scenario.add_action_change_mission_status('改变任务状态', '红方', '投送', 0)
        self.env.step()

    def test_update_action_change_mission_status(self):
        """编辑改变任务状态动作"""
        self.scenario.add_action_change_mission_status('改变任务状态', '红方', '投送', 0)
        self.env.step()

        rename = '改变任务状态-改'
        self.scenario.update_action_change_mission_status('改变任务状态', rename=rename, side='蓝方',
                                                          mission='水上巡逻', new_status=1)
        self.env.step()

    def test_add_action_lua_script(self):
        """添加lua脚本动作"""
        self.scenario.add_action_lua_script('lua脚本执行', 'ScenEdit_SetAction()')
        self.env.step()

    def test_update_action_lua_script(self):
        """编辑lua脚本动作"""
        self.scenario.add_action_lua_script('lua脚本执行', 'ScenEdit_SetAction()')
        self.env.step()

        rename = 'lua脚本执行-改'
        self.scenario.update_action_lua_script('lua脚本执行', rename=rename, script_text='ScenEdit_SetTrigger()')
        self.env.step()

    def test_remove_action(self):
        """删除动作"""
        self.scenario.add_action_change_mission_status('改变任务状态', '红方', '投送', 0)
        self.env.step()
        self.scenario.remove_action('改变任务状态')
        self.env.step()

    def test_add_event(self):
        """添加事件"""
        self.scenario.add_event('事件1')
        self.env.step()

        self.scenario.add_action_change_mission_status('改变任务状态', '红方', '投送', 0)
        self.env.step()

    def test_remove_event(self):
        """删除事件"""
        self.scenario.add_event('事件1')
        self.env.step()
        self.scenario.remove_event('事件1')
        self.env.step()

    def test_set_event_trigger_action_condition(self):
        """设置事件触发器、条件、动作"""
        self.scenario.add_event('事件1')
        self.env.step()

        self.scenario.add_trigger_time('时间触发器', '2021/7/19 10:1:21')
        self.scenario.add_action_change_mission_status('改变任务状态', '红方', '投送', 0)
        self.scenario.add_condition_side_posture('推演方立场', '红方', '蓝方', 0, 'true')

        self.scenario.set_event_trigger('事件1', '时间触发器')
        self.scenario.set_event_action('事件1', '改变任务状态')
        self.scenario.set_event_condition('事件1', '推演方立场')
        self.env.step()

    def test_replace_event_trigger_action_condition(self):
        """替换事件触发器、条件、动作"""
        self.scenario.add_event('事件1')
        self.env.step()

        self.scenario.add_trigger_time('时间触发器', '2021/7/19 10:1:21')
        self.scenario.add_trigger_time('时间触发器-改', '2021/7/19 11:1:21')
        self.scenario.add_action_change_mission_status('改变任务状态', '红方', '投送', 0)
        self.scenario.add_action_change_mission_status('改变任务状态-改', '红方', '投送', 0)
        self.scenario.add_condition_side_posture('推演方立场', '红方', '蓝方', 0, 'true')
        self.scenario.add_condition_side_posture('推演方立场-改', '红方', '蓝方', 0, 'true')

        self.scenario.set_event_trigger('事件1', '时间触发器')
        self.scenario.set_event_action('事件1', '改变任务状态')
        self.scenario.set_event_condition('事件1', '推演方立场')
        self.env.step()
        self.scenario.replace_event_trigger('事件1', '时间触发器', '时间触发器-改')
        self.scenario.replace_event_condition('事件1', '推演方立场', '推演方立场-改')
        self.scenario.replace_event_action('事件1', '改变任务状态', '改变任务状态-改')
        self.env.step()

    def test_update_event_attribute(self):
        """设置事件属性"""
        self.scenario.add_event('事件1')
        self.scenario.add_trigger_time('时间触发器', '2021/7/19 10:1:21')
        self.scenario.add_action_change_mission_status('改变任务状态', '红方', '投送', 0)
        self.scenario.add_condition_side_posture('推演方立场', '红方', '蓝方', 0, 'true')
        self.scenario.set_event_trigger('事件1', '时间触发器')
        self.scenario.set_event_action('事件1', '改变任务状态')
        self.scenario.set_event_condition('事件1', '推演方立场')
        self.env.step()

        new_event_name = '事件1-改'
        description = '事件1-改2'
        is_active = 'false'
        is_shown = 'false'
        is_repeatable = 'true'
        probability = 90
        self.scenario.update_event_attribute('事件1', new_event_name=new_event_name, is_active=is_active,
                                             is_shown=is_shown, is_repeatable=is_repeatable, probability=probability)
        self.env.step()

    def test_add_condition_side_posture(self):
        """添加条件，推演方立场"""
        self.scenario.add_condition_side_posture('推演方立场-中立方', '红方', '蓝方', 0, 'true')
        self.env.step()
        self.scenario.add_condition_side_posture('推演方立场-友方', '红方', '蓝方', 1, 'true')
        self.scenario.add_condition_side_posture('推演方立场-非友方', '红方', '蓝方', 2, 'true')
        self.scenario.add_condition_side_posture('推演方立场-敌方', '红方', '蓝方', 3, 'true')
        self.scenario.add_condition_side_posture('推演方立场-不明', '红方', '蓝方', 4, 'true')
        self.env.step()

    def test_update_condition_side_posture(self):
        """更新条件，推演方立场"""
        self.scenario.add_condition_side_posture('推演方立场', '红方', '蓝方', 1, 'true')
        self.env.step()

        rename = '推演方立场-改'
        self.scenario.update_condition_side_posture('推演方立场', rename=rename, observer_side='蓝方', target_side='红方',
                                                    target_posture=2, is_reverse='false')
        self.env.step()

    def test_add_condition_scen_has_started(self):
        """添加条件，想定已加载"""
        self.scenario.add_condition_scen_has_started('想定已加载', 'true')
        self.env.step()

    def test_update_condition_scen_has_started(self):
        """更新条件，想定已加载"""
        self.scenario.add_condition_scen_has_started('想定已加载', 'true')
        self.env.step()

        rename = '想定已加载-改'
        self.scenario.update_condition_scen_has_started('想定已加载', rename=rename, is_reverse='false')
        self.env.step()

    def test_add_condition_lua_script(self):
        """添加条件lua script"""
        script_text = 'ScenEdit_SetAction()'
        self.scenario.add_condition_lua_script('lua脚本', script_text)
        self.env.step()

    def test_update_condition_lua_script(self):
        """更新条件lua script"""
        script_text = 'ScenEdit_SetAction()'
        self.scenario.add_condition_lua_script('lua脚本', script_text)
        self.env.step()

        script_text = 'ScenEdit_SetTrigger()'
        rename = 'lua脚本-改'
        self.scenario.update_condition_lua_script('lua脚本', rename=rename, script_text=script_text)
        self.env.step()

    def test_remove_condition(self):
        """删除条件"""
        script_text = 'ScenEdit_SetAction()'
        self.scenario.add_condition_lua_script('lua脚本', script_text)
        self.env.step()

        self.scenario.remove_condition('lua脚本')
        self.env.step()

    def test_get_sides(self):
        """获取推演方"""
        sides = self.scenario.get_sides()
        for k, v in sides.items():
            if k == self.red_side.strGuid:
                self.assertEqual(v, self.red_side)
            elif k == self.blue_side.strGuid:
                self.assertEqual(v, self.blue_side)
            else:
                self.assertTrue(False)
        self.env.step()

    def test_get_title(self):
        """获取标题"""
        title = self.scenario.get_title()
        self.assertEqual(title, 'active_unit_test')

    def test_get_weather(self):
        """获取天气"""
        weather = self.scenario.get_weather()
        self.assertEqual(weather.dTemperature, 15.0)
        self.assertEqual(weather.fRainFallRate, 0.0)
        self.assertEqual(weather.fSkyCloud, 0.0)
        self.assertEqual(weather.iSeaState, 0)

    def test_get_responses(self):
        """获取仿真响应信息"""
        response = self.scenario.get_responses()
        self.assertTrue(response)
        for k, v in response.items():
            self.assertEqual(v.ClassName, 'CResponse')

    def test_get_weapon_impacts(self):
        """获取所有武器冲击"""
        # TODO 接口作用不明
        self.red_side.get_doctrine().set_weapon_control_status_air(0)
        for i in range(10):
            self.env.step()
        weapon_impacts = self.scenario.get_weapon_impacts()
        self.env.step()

    def test_get_events(self):
        """获取所有事件"""
        self.scenario.add_event('事件2')
        self.scenario.add_trigger_time('时间触发器1', '2021/7/19 10:1:21')
        self.scenario.add_action_change_mission_status('改变任务状态1', '红方', '投送', 0)
        self.scenario.add_condition_side_posture('推演方立场1', '红方', '蓝方', 0, 'true')
        self.scenario.set_event_trigger('事件2', '时间触发器1')
        self.scenario.set_event_action('事件2', '改变任务状态1')
        self.scenario.set_event_condition('事件2', '推演方立场1')
        self.env.step()

        events = self.scenario.get_events()
        for k, v in events.items():
            self.assertEqual(v.strDescription, '事件2')

    def test_get_units_by_name(self):
        """获取根据名称获取单元列表"""
        aircraft_dict = self.scenario.get_units_by_name('反潜机1')
        for k, v in aircraft_dict.items():
            self.assertEqual(v.strName, '反潜机1')

    def test_unit_is_alive(self):
        """从上帝视角用uid判断实体单元是否存在"""
        is_alive = self.scenario.unit_is_alive(self.antisubmarine_aircraft_guid)
        self.assertTrue(is_alive)

    def test_get_side_by_name(self):
        """根据名字获取推演方信息"""
        side = self.scenario.get_side_by_name('红方')
        self.assertEqual(side.strName, '红方')

    def test_add_side(self):
        """添加方"""
        self.scenario.add_side('绿方')
        self.env.step()
        side = self.scenario.get_side_by_name('绿方')
        self.assertEqual(side.strName, '绿方')

    def test_remove_side(self):
        """移除推演方"""
        self.scenario.add_side('绿方')
        self.env.step()
        self.scenario.remove_side('绿方')
        self.env.step()
        side = self.scenario.get_side_by_name('绿方')
        self.assertFalse(side)

    def test_set_side_posture(self):
        """设置一方对另一方的立场"""
        # 友好
        self.scenario.set_side_posture('红方', '蓝方', 'F')
        # 敌对
        self.scenario.set_side_posture('红方', '蓝方', 'H')
        # 中立
        self.scenario.set_side_posture('红方', '蓝方', 'N')
        # 非友
        self.scenario.set_side_posture('红方', '蓝方', 'U')
        self.env.step()

    def test_reset_all_sides_scores(self):
        """重置所有推演方分数"""
        pass
        # TODO 手动测试lua通过，可能需要换个想定

    def test_reset_all_losses_expenditures(self):
        """将各推演方所有战斗损失、战斗消耗、单元损伤等均清零。"""
        pass
        # TODO 手动测试lua通过，可能需要换个想定

    def test_set_scenario_time(self):
        """设置当前想定的起始时间，当前时间，持续事时间、想定复杂度、想定难度，想定地点等"""
        scenario_current_time = '2021/7/19 10:12:2'
        scenario_start_time = '2021/7/19 10:10:2'
        scenario_set_duration = '1-10-16'
        scenario_complexity = 3
        scenario_difficulty = 4
        scenario_address_setting = '南海'
        self.scenario.set_scenario_time(scenario_current_time=scenario_current_time,
                                        scenario_start_time=scenario_start_time,
                                        scenario_set_duration=scenario_set_duration,
                                        scenario_complexity=scenario_complexity,
                                        scenario_difficulty=scenario_difficulty,
                                        scenario_address_setting=scenario_address_setting)
        self.env.step()

    def test_get_current_time(self):
        """获得当前想定时间"""
        current_time = self.scenario.get_current_time()
        print(current_time)

    def test_get_player_name(self):
        """获得当前推演方的名称"""
        player_name = self.scenario.get_player_name()
        self.assertEqual(player_name, '红方')

    def test_get_side_posture(self):
        """获取一方side_a对另一方side_b的立场"""
        posture = self.scenario.get_side_posture('红方', '蓝方')
        self.assertEqual(posture, 'U')

    def test_change_unit_side(self):
        """改变单元的方"""
        self.scenario.change_unit_side('反潜机1', '红方', '蓝方')
        self.env.step()
        self.assertEqual(self.antisubmarine_aircraft.m_Side, self.blue_side.strGuid)

    def test_dump_rules(self):
        """向系统安装目录下想定默认文件夹以 xml 文件的方式导出事件、条件、触发器、动作、特殊动作"""
        self.scenario.add_event('事件2')
        self.scenario.add_trigger_time('时间触发器1', '2021/7/19 10:1:21')
        self.scenario.add_action_change_mission_status('改变任务状态1', '红方', '投送', 0)
        self.scenario.add_condition_side_posture('推演方立场1', '红方', '蓝方', 0, 'true')
        self.scenario.set_event_trigger('事件2', '时间触发器1')
        self.scenario.set_event_action('事件2', '改变任务状态1')
        self.scenario.set_event_condition('事件2', '推演方立场1')
        self.env.step()

        self.scenario.dump_rules()
        self.env.step()

    def test_set_description(self):
        """设置想定标题和描述"""
        self.scenario.set_description('新标题', '新描述')
        self.env.step()
        self.env.step()

    def test_set_fineness(self):
        """设置想定精细度"""
        detailed_gun_fire_control = 'true'
        unlimited_base_mags = 'true'
        aircraft_damage = 'true'
        comms_jamming = 'true'
        comms_disruption = 'true'
        ballistic_missile = 'true'
        self.scenario.set_fineness(detailed_gun_fire_control=detailed_gun_fire_control,
                                   unlimited_base_mags=unlimited_base_mags,
                                   aircraft_damage=aircraft_damage,
                                   comms_jamming=comms_jamming,
                                   comms_disruption=comms_disruption,
                                   ballistic_missile=ballistic_missile)
        self.env.step()

    def test_set_cur_side_and_dir_view(self):
        """设置服务端当前推演方"""
        self.scenario.set_cur_side_and_dir_view('蓝方', 'true')
        self.env.step()

    def test_end_scenario(self):
        """终止当前想定"""
        self.env.step()
        self.env.step()
        self.scenario.end_scenario()
        # 查看消息输出
        self.env.step()

    def test_save_scenario(self):
        """保存当前已经加载的想定"""
        self.env.step()
        self.env.step()
        self.scenario.save_scenario()
        self.env.step()

    def test_save_as(self):
        """另存当前已经加载的想定"""
        self.env.step()
        self.env.step()
        self.scenario.save_as('想定-新.scen')
        self.env.step()

    def test_add_trigger_aircraft_take_off(self):
        """添加飞机起飞触发器"""
        self.scenario.add_trigger_aircraft_take_off('飞机起飞', self.red_side.strGuid)
        self.env.step()

    def test_add_trigger_aircraft_landing(self):
        """添加飞机降落触发器"""
        self.scenario.add_trigger_aircraft_landing('飞机降落', self.red_side.strGuid)
        self.env.step()


if __name__ == '__main__':
    TestScenario.main()
