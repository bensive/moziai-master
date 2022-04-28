# -*- coding:utf-8 -*-
##########################################################################################################
# File name : scenario.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################

from mozi_simu_sdk.situation import CSituation


class CScenario:
    """想定"""

    def __init__(self, mozi_server):
        self.mozi_server = mozi_server
        # 类名
        self.ClassName = "CCurrentScenario"
        # GUID
        self.strGuid = ""
        # 标题
        self.strTitle = ""
        # 想定文件名
        self.strScenFileName = ""
        # 描述
        self.strDescription = ""
        # 当前时间
        self.m_Time = ""
        # 是否是夏令时
        self.bDaylightSavingTime = False
        # 当前想定第一次启动的开始时间
        self.m_FirstTimeRunDateTime = ""
        # 用不上
        self.m_FirstTimeLastProcessed = 0.0
        # 用不上
        self.m_grandTimeLastProcessed = 0.0
        # 夏令时开始时间（基本不用）
        self.strDaylightSavingTime_Start = 0.0
        # 夏令结束时间（基本不用）
        self.strDaylightSavingTime_End = 0.0
        # 想定开始时间
        self.m_StartTime = ""
        # 想定持续时间
        self.m_Duration = ""
        # 想定精细度
        self.sMeta_Complexity = 1
        # 想定困难度
        self.sMeta_Difficulty = 1
        # 想定发生地
        self.strMeta_ScenSetting = ""
        # 想定精细度的枚举类集合
        self.strDeclaredFeatures = ""
        # 想定的名称
        self.strCustomFileName = ""
        # 编辑模式剩余时间
        self.iEditCountDown = 0
        # 推演模式剩余时间
        self.iStartCountDown = 0
        # 暂停剩余时间
        self.iSuspendCountDown = 0
        # 获取推演的阶段模式
        self.m_CurrentStage = 0
        # 态势
        self.situation = CSituation(mozi_server)
        self.sides = self.get_sides()  # by aie

    def get_sides(self):
        """
        功能：获取所有推演方
        参数：无
        返回：所有推演方（类型：dict, {side_guid:side_obj, side_guid2:side_obj2, ...}）
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        return self.situation.side_dic

    def get_title(self):
        """
        功能：获取想定标题
        函数类别：推演所用的函数
        参数：无
        返回：str - 想定标题
        作者：赵俊义;  amended by aie
        单位：北京华戍防务技术有限公司
        时间：2020-3-7 ;amended on 2020-4-26
        """
        return self.strTitle

    def get_weather(self):
        """
        功能：获取天气条件
        函数类别：推演所用的函数
        参数：无
        返回：CWeather对象 （天气条件）
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：20200401
        """
        return self.situation.weather

    def get_responses(self):
        """
        功能：获取仿真响应信息。
        函数类别：推演所用的函数
        参数：无
        返回：仿真响应信息（类型：dict）格式 {response_guid:response_obj,response_guid_2:response_obj_2, ...}
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：20200401
        """
        return self.situation.response_dic

    def get_weapon_impacts(self):
        """
        功能：获取所有武器冲击。
        函数类别：推演所用的函数
        参数：无
        返回：所有武器冲击（类型：dict） 格式 {weapon_impact_guid:weapon_impact_obj,weapon_impact_guid_2:weapon_impact_obj_2, ...}
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：20200401
        """
        return self.situation.wpnimpact_dic

    def get_events(self):
        """
        功能：获取所有事件。
        函数类别：推演所用的函数
        参数：无
        返回：所有事件（类型：dict） 格式 {event_guid:event_obj,event_guid_2:event_obj_2, ...}
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：20200401
        """
        return self.situation.simevent_dic

    def get_side_by_name(self, name):
        """
        功能：根据名字获取推演方信息
        函数类别：推演所用的函数
        参数：
            name {str: 推演方名字}
        返回：CSide对象
        作者：-
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        for k, v in self.situation.side_dic.items():
            if v.strName == name:
                return v

    def get_current_time(self):
        """
        功能：获得当前想定时间
        函数类别：推演使用函数
        参数：无
        返回：当前时间戳 example: 1626657722
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-7
        """
        lua = "ReturnObj(ScenEdit_CurrentTime())"
        ret_time = self.mozi_server.send_and_recv(lua)
        return ret_time

    def get_player_name(self):
        """
        功能：获得当前推演方的名称
        函数类别：推演使用函数
        参数：无
        返回：str - 当前推演方名称
        作者：赵俊义
        修改：张志高 2021-8-17
        单位：北京华戍防务技术有限公司
        时间：2020-3-7
        """
        return self.mozi_server.send_and_recv("ReturnObj(ScenEdit_PlayerSide())")

    def get_side_posture(self, side_a, side_b):
        """
        功能：获取一方side_a对另一方side_b的立场
        函数类别：推演使用函数
        参数：
            side_a: {str: 推演方名称}
            side_b: {str: 推演方名称}
        返回：立场编码 {str: 'F'-友好，'H'-敌对，'N'-中立，'U'-非友}
        作者：赵俊义
        修改：张志高 2021-8-17
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        return self.mozi_server.send_and_recv("ReturnObj(ScenEdit_GetSidePosture('{}','{}'))".format(side_a, side_b))

    def get_units_by_name(self, name):
        """
        功能：从上帝视角用名称获取单元。
        限制：专项赛禁用
        函数类别：推演所用的函数
        参数：
            name {str: 单元名称}
        返回：活动单元字典 格式 {active_unit_guid:active_unit_obj,active_unit_guid_2:active_unit_obj_2...}
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        # 需求来源：20200330-1.1/3:lzy
        units = {}
        sbmrns = {k: v for k, v in self.situation.submarine_dic.items() if v.strName == name}
        shps = {k: v for k, v in self.situation.ship_dic.items() if v.strName == name}
        fclts = {k: v for k, v in self.situation.facility_dic.items() if v.strName == name}
        airs = {k: v for k, v in self.situation.aircraft_dic.items() if v.strName == name}
        stllts = {k: v for k, v in self.situation.satellite_dic.items() if v.strName == name}
        wpns = {k: v for k, v in self.situation.weapon_dic.items() if v.strName == name}
        ungddwpns = {k: v for k, v in self.situation.unguidedwpn_dic.items() if v.strName == name}
        units.update(sbmrns)
        units.update(shps)
        units.update(fclts)
        units.update(airs)
        units.update(stllts)
        units.update(wpns)
        units.update(ungddwpns)
        return units

    def unit_is_alive(self, guid):
        """
        功能：从上帝视角用guid判断实体单元是否存在
        限制：专项赛禁用
        函数类别：推演所用的函数
        参数：
            guid {str: 单元guid}
        返回：bool:{True-是，False-否}
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        # 需求来源：20200330-1.2/3:lzy
        if guid in self.situation.all_guid:
            return True
        else:
            return False

    def add_side(self, side_name):
        """
        功能：添加方
        限制：专项赛禁用
        函数类别：编辑使用函数
        参数：
            side_name {str: 推演方名字}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        return self.mozi_server.send_and_recv("HS_LUA_AddSide({side='%s'})" % side_name)

    def remove_side(self, side):
        """
        功能：移除推演方
        限制：专项赛禁用
        函数类别：编辑使用函数
        参数：
            side {str: 推演方名字}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        return self.mozi_server.send_and_recv("ScenEdit_RemoveSide({side='%s'})" % side)

    def set_side_posture(self, side_a, side_b, relation):
        """
        功能：设置一方对另一方的立场
        限制：专项赛禁用
        函数类别：编辑使用函数
        参数：
            side_a {str: 推演方名字}
            side_b {str: 推演方名字}
            relation 立场编码 {str: 'F'-友好，'H'-敌对，'N'-中立，'U'-非友}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        return self.mozi_server.send_and_recv(
            "ScenEdit_SetSidePosture('{}','{}','{}')".format(side_a, side_b, relation))

    def reset_all_sides_scores(self):
        """
        功能：重置所有推演方分数
        限制：专项赛禁用
        函数类别：编辑使用函数
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        return self.mozi_server.send_and_recv("Hs_ResetAllSideScores()")

    def reset_all_losses_expenditures(self):
        """
        功能：将各推演方所有战斗损失、战斗消耗、单元损伤等均清零。
        限制：专项赛禁用
        函数类别：编辑使用函数
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        return self.mozi_server.send_and_recv("Hs_ResetAllLossesExpenditures()")

    def set_scenario_time(self, scenario_current_time=None, scenario_start_time=None, scenario_set_duration=None,
                          scenario_complexity=None, scenario_difficulty=None, scenario_address_setting=None):
        """
        功能：设置当前想定的起始时间，当前时间，持续事时间、想定复杂度、想定难度，想定地点等
        限制：专项赛禁用
        函数类别：编辑使用函数
        参数：
            scenario_current_time 想定当前时间 {str: 格式'2020/8/10 10:12:2'}
            scenario_start_time 想定起始时间 {str: 格式'2020/8/10 10:12:2'} 开始时间不能晚于当前时间
            scenario_set_duration 想定持续时间 {str: '1-10-16' 表示1天10小时16分钟}
            scenario_complexity 想定复杂度 {int: 1-5 5个复杂等级}
            scenario_difficulty 想定难度 {int: 1-5 5个难度等级}
            scenario_address_setting  {str: 想定发生地点}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：20200330
        """
        update_str = ''
        if scenario_current_time:
            update_str += f", ScenarioTime='{scenario_current_time}'"
        if scenario_start_time:
            update_str += f", ScenarioStartTime='{scenario_start_time}'"
        if scenario_set_duration:
            update_str += f", ScenarioSetDuration='{scenario_set_duration}'"
        if scenario_complexity:
            update_str += f", ScenarioComplexity={scenario_complexity}"
        if scenario_difficulty:
            update_str += f", ScenarioDifficulty={scenario_difficulty}"
        if scenario_address_setting:
            update_str += f", ScenarioScenSetting='{scenario_address_setting}'"
        if update_str:
            update_str = update_str[1:]
        lua_script = f"Hs_SetScenarioTime({{{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def change_unit_side(self, unit_name, side_a, side_b):
        """
        功能：改变单元的方
        限制：专项赛禁用
        函数类别：编辑使用函数
        参数：
            unit_name: {str: 单元名称}
            side_a: {str: 推演方名称}
            side_b: {str: 推演方名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        return self.mozi_server.send_and_recv(
            "ScenEdit_SetUnitSide({{name='{}',side='{}',newside='{}'}})".format(unit_name, side_a,
                                                                                side_b))  # ammended by aie

    def dump_rules(self):
        """
        功能：向系统安装目录下想定默认文件夹以 xml 文件的方式导出事件、条件、触发器、动作、特殊动作。
        限制：专项赛禁用
        函数类别：推演使用函数
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        return self.mozi_server.send_and_recv("Tool_DumpEvents()")

    def set_description(self, scenario_title, description):
        """
        功能：设置想定标题和描述
        限制：专项赛禁用
        函数类别：编辑使用函数
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修改：张志高 2021-8-17
        单位：北京华戍防务技术有限公司
        时间：2020-3-7
        """
        lua_script = f"Hs_SetScenarioDescribe({{ScenarioTitle='{scenario_title}',SetDescription='{description}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def set_fineness(self, detailed_gun_fire_control=None, unlimited_base_mags=None, aircraft_damage=None,
                     comms_jamming=None, comms_disruption=None, ballistic_missile=None):
        """
        功能：设置想定精细度
        限制：专项赛禁用
        函数类别：编辑使用函数
        参数：
            detailed_gun_fire_control 是否使用高精度火控算法 {str: true - 是，false - 否}
            unlimited_base_mags 是否海/空弹药库不受限 {str: true - 是，false - 否}
            aircraft_damage 是否使用飞机高精度毁伤模型   {str: true - 是，false - 否}
            comms_jamming 是否使用通信干扰  {str: true - 是，false - 否}
            comms_disruption 是否使用通信摧毁   {str: true - 是，false - 否}
            ballistic_missile 是否使用弹道导弹精细模型  {str: true - 是，false - 否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-17
        """
        update_str = ''
        if detailed_gun_fire_control:
            update_str += f", DetailedGunFirControl={detailed_gun_fire_control}"
        if unlimited_base_mags:
            update_str += f", UnlimitedBaseMags={unlimited_base_mags}"
        if aircraft_damage:
            update_str += f", AircraftDamage={aircraft_damage}"
        if comms_jamming:
            update_str += f", CommsJamming={comms_jamming}"
        if comms_disruption:
            update_str += f", CommsDisruption={comms_disruption}"
        if ballistic_missile:
            update_str += f", BallisticMissile={ballistic_missile}"

        if update_str:
            update_str = update_str[1:]

        lua_script = f"Hs_FeaturesReakismSet({{{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def set_cur_side_and_dir_view(self, side_name_or_guid, open_or_close_dir_view):
        """
        功能：设置服务端当前推演方,便于用户观察态势。
        限制：专项赛禁用
        函数类别：推演所用的函数
        参数：
            side_name_or_guid {str: 推演方名称或guid}
            open_or_close_dir_view 是否开启导演视图 {str: true - 是，false - 否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：董卓
        单位：北京华戍防务技术有限公司
        时间：2020-5-3
        """
        return self.mozi_server.send_and_recv(
            "ScenEdit_SetCurSideAndDirView('%s',%s)" % (side_name_or_guid, open_or_close_dir_view))

    def end_scenario(self):
        """
        功能：终止当前想定，进入参演方评估并给出评估结果
        限制：专项赛禁用
        函数类别：推演所用的函数
        参数：无
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-5-3
        """
        return self.mozi_server.send_and_recv("ScenEdit_EndScenario()")

    def save_scenario(self):
        """
        功能：保存当前已经加载的想定
        限制：专项赛禁用
        函数类别：推演所用的函数
        参数：无
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-7
        """
        return self.mozi_server.send_and_recv("Hs_ScenEdit_SaveScenario()")

    def save_as(self, scenario_name):
        """
        功能：另存当前已经加载的想定
        限制：专项赛禁用
        函数类别：推演所用的函数
        参数：无
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-7
        """
        return self.mozi_server.send_and_recv("Hs_ScenEdit_SaveAsScenario('{}')".format(scenario_name))

    def set_weather(self, avg_temp, rainfall_rate, fraction_under_rain, sea_state):
        """
        功能：设置当前天气条件
        限制：专项赛禁用
        参数：avg_temp 平均气温 {float: -50 ~ 50}
            rainfall_rate 降水量 {float: 0 ~ 50 无雨~暴雨}
            fraction_under_rain 天空云量 {float: 0 ~ 1.0 晴朗~多云}
            sea_state 风力/海况 {int: 0 ~ 9 无风~飓风}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-9
        """
        lua_script = f"ScenEdit_SetWeather({avg_temp}, {rainfall_rate}, {fraction_under_rain}, {sea_state})"
        return self.mozi_server.send_and_recv(lua_script)

    @staticmethod
    def __generate_target_filter_str(target_filter_dict):
        """
        功能：私有函数，将target_filter_dict转换成target_filter_str
        参数：target_filter_dict {dict}
            example: {TARGETSIDE='红方',TARGETTYPE=3,TARGETSUBTYPE=3204,SPECIFICUNITCLASS=1573,
                SPECIFICUNIT='016b72ba-2ab2-464a-a340-3cfbfb133ed1'}
        返回：target_filter_str {str}
            example: TARGETSIDE='红方',TARGETTYPE=3,TARGETSUBTYPE=3204,SPECIFICUNITCLASS=1573,
                SPECIFICUNIT='016b72ba-2ab2-464a-a340-3cfbfb133ed1'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        target_filter_str = ''
        target_filter_list = []
        for k, v in target_filter_dict.items():
            if k in ['TARGETSIDE', 'SPECIFICUNIT']:
                target_filter_list.append(f"{k}='{v}'")
            if k in ['TARGETSUBTYPE', 'SPECIFICUNITCLASS']:
                target_filter_list.append(f"{k}={v}")
            if k in ['TARGETTYPE']:
                if isinstance(v, int):
                    target_filter_list.append(f"{k}={v}")
                else:
                    target_filter_list.append(f"{k}='{v}'")
        if target_filter_list:
            target_filter_str = ','.join(target_filter_list)
        return target_filter_str

    def add_trigger_unit_destroyed(self, name, target_filter_dict):
        """
        功能：添加单元被摧毁触发器
        限制：专项赛禁用
        参数：name:{str:触发器名称}
            target_filter_dict {dict:
                TARGETSIDE-str-推演方名称，
                TARGETTYPE-int-类型ID，
                    0 = NoneValue
                    1 = AircraftType
                    2 = ShipType
                    3 = SubmarineType
                    4 = FacilityType
                    5 = Aimpoint
                    6 = WeaponType
                    7 = SatelliteType
                  或 str
                    	Aircraft：飞机
                    	Ship：水面舰艇
                    	Submarine：潜艇
                    	Facility：地面兵力与设施
                TARGETSUBTYPE-int-数据库中的类型ID，
                SPECIFICUNITCLASS-目标数据库DBID，
                SPECIFICUNIT-实际单元名称或GUID}
                例子：{'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
        返回：'lua执行成功' 或 '脚本执行出错' 或 'target_filter_dict不合法'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-11
        """
        target_filter_str = self.__generate_target_filter_str(target_filter_dict)
        if not target_filter_str:
            return "target_filter_dict不合法"

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='unitdestroyed'," \
                     f"TargetFilter={{{target_filter_str}}}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_trigger_unit_destroyed(self, name, rename=None, target_filter_dict=None):
        """
        功能：更新单元被摧毁触发器
        限制：专项赛禁用
        参数：name:{str:触发器名称}
            rename:{str:新的触发器名称}
            target_filter_dict {dict:
                TARGETSIDE-str-推演方名称，
                TARGETTYPE-int-类型ID，
                    0 = NoneValue
                    1 = AircraftType
                    2 = ShipType
                    3 = SubmarineType
                    4 = FacilityType
                    5 = Aimpoint
                    6 = WeaponType
                    7 = SatelliteType
                  或 str
                    	Aircraft：飞机
                    	Ship：水面舰艇
                    	Submarine：潜艇
                    	Facility：地面兵力与设施
                TARGETSUBTYPE-int-数据库中的类型ID，
                SPECIFICUNITCLASS-目标数据库DBID，
                SPECIFICUNIT-实际单元名称或GUID}
                例子：{'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
        返回：'lua执行成功' 或 '脚本执行出错' 或 'target_filter_dict不合法'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-13
        """
        update_str = ''
        if target_filter_dict:
            target_filter_str = self.__generate_target_filter_str(target_filter_dict)
            if not target_filter_str:
                return "target_filter_dict不合法"
            update_str += f", TargetFilter={{{target_filter_str}}}"
        if rename:
            update_str += f", rename='{rename}'"

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='update',Type='unitdestroyed'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_trigger_unit_damaged(self, name, target_filter_dict, damage_percent):
        """
        功能：添加单元被毁伤触发器
        限制：专项赛禁用
        参数：name:{str:触发器名称}
            target_filter_dict {dict:
                TARGETSIDE-str-推演方名称，
                TARGETTYPE-int-类型ID，
                    0 = NoneValue
                    1 = AircraftType
                    2 = ShipType
                    3 = SubmarineType
                    4 = FacilityType
                    5 = Aimpoint
                    6 = WeaponType
                    7 = SatelliteType
                  或 str
                    	Aircraft：飞机
                    	Ship：水面舰艇
                    	Submarine：潜艇
                    	Facility：地面兵力与设施
                TARGETSUBTYPE-int-数据库中的类型ID，
                SPECIFICUNITCLASS-目标数据库DBID，
                SPECIFICUNIT-实际单元名称或GUID}
                例子：{'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
            damage_percent: int - 毁伤百分比
        返回：'lua执行成功' 或 '脚本执行出错' 或 'target_filter_dict不合法'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-11
        """
        target_filter_str = self.__generate_target_filter_str(target_filter_dict)
        if not target_filter_str:
            return "target_filter_dict不合法"

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='UnitDamaged'," \
                     f"TargetFilter={{{target_filter_str}}},DamagePercent={damage_percent}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_trigger_unit_damaged(self, name, rename=None, target_filter_dict=None, damage_percent=None):
        """
        功能：更新单元被毁伤触发器
        限制：专项赛禁用
        参数：name:{str:触发器名称}
            rename:{str:新的触发器名称}
            target_filter_dict {dict:
                TARGETSIDE-str-推演方名称，
                TARGETTYPE-int-类型ID，
                    0 = NoneValue
                    1 = AircraftType
                    2 = ShipType
                    3 = SubmarineType
                    4 = FacilityType
                    5 = Aimpoint
                    6 = WeaponType
                    7 = SatelliteType
                  或 str
                    	Aircraft：飞机
                    	Ship：水面舰艇
                    	Submarine：潜艇
                    	Facility：地面兵力与设施
                TARGETSUBTYPE-int-数据库中的类型ID，
                SPECIFICUNITCLASS-目标数据库DBID，
                SPECIFICUNIT-实际单元名称或GUID}
                例子：{'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
            damage_percent: int - 毁伤百分比
        返回：'lua执行成功' 或 '脚本执行出错' 或 'target_filter_dict不合法'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        update_str = ''
        if target_filter_dict:
            target_filter_str = self.__generate_target_filter_str(target_filter_dict)
            if not target_filter_str:
                return "target_filter_dict不合法"
            update_str += f", TargetFilter={{{target_filter_str}}}"
        if rename:
            update_str += f", rename='{rename}'"
        if damage_percent:
            update_str += f", DamagePercent={damage_percent}"

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='update',Type='UnitDamaged'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_trigger_points(self, name, side, point_value, reach_direction):
        """
        功能：添加推演方得分触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            side:{str:推演方名称}
            point_value:{int:推演方分数}
            reach_direction:{int:0-超过，1-刚好达到，2-低于}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='Points'," \
                     f"SideID='{side}', PointValue={point_value}, ReachDirection={reach_direction}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_trigger_points(self, name, rename=None, side=None, point_value=None, reach_direction=None):
        """
        功能：编辑推演方得分触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            rename:{str:新的触发器名称}
            side:{str:推演方名称}
            point_value:{int:推演方分数}
            reach_direction:{int:0-超过，1-刚好达到，2-低于}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if side:
            update_str += f", SideID='{side}'"
        if point_value:
            update_str += f", PointValue={point_value}"
        if reach_direction:
            update_str += f", ReachDirection={reach_direction}"
        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='update',Type='Points'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_trigger_time(self, name, time):
        """
        功能：添加时间触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            time:{str:格式 2019/8/10 10:1:21}，实际设置的时间为设置时间+8小时
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-13
        """
        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='time'," \
                     f"Time='{time}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_trigger_time(self, name, rename=None, time=None):
        """
        功能：更新时间触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            rename:{str:新的触发器名称}
            time:{str:格式 2019/8/10 10:1:21} 实际设置的时间为设置时间
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if time:
            update_str += f", Time='{time}'"

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='update',Type='time'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_trigger_unit_remains_in_area(self, name, target_filter_dict, area, stay_time):
        """
        功能：添加单元停留在区域内触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            target_filter_dict {dict:
                TARGETSIDE-str-推演方名称，
                TARGETTYPE-int-类型ID，
                    0 = NoneValue
                    1 = AircraftType
                    2 = ShipType
                    3 = SubmarineType
                    4 = FacilityType
                    5 = Aimpoint
                    6 = WeaponType
                    7 = SatelliteType
                  或 str
                    	Aircraft：飞机
                    	Ship：水面舰艇
                    	Submarine：潜艇
                    	Facility：地面兵力与设施
                TARGETSUBTYPE-int-数据库中的类型ID，
                SPECIFICUNITCLASS-目标数据库DBID，
                SPECIFICUNIT-实际单元名称或GUID}
                例子：{'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
            area：{list: 参考点名称列表}
            stay_time 停留时间 {str: 格式'1:2:3:4' （'天:小时:分:秒'）}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        target_filter_str = self.__generate_target_filter_str(target_filter_dict)
        if not target_filter_str:
            return "target_filter_dict不合法"

        area_str = str(area).replace('[', '').replace(']', '')

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='UnitRemainsInArea'," \
                     f"TargetFilter={{{target_filter_str}}}, Area={{{area_str}}}, TD='{stay_time}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_trigger_unit_remains_in_area(self, name, rename=None, target_filter_dict=None, area=None,
                                            stay_time=None):
        """
        功能：编辑单元停留在区域内触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            rename:{str:新的触发器名称}
            target_filter_dict {dict:
                TARGETSIDE-str-推演方名称，
                TARGETTYPE-int-类型ID，
                    0 = NoneValue
                    1 = AircraftType
                    2 = ShipType
                    3 = SubmarineType
                    4 = FacilityType
                    5 = Aimpoint
                    6 = WeaponType
                    7 = SatelliteType
                  或 str
                    	Aircraft：飞机
                    	Ship：水面舰艇
                    	Submarine：潜艇
                    	Facility：地面兵力与设施
                TARGETSUBTYPE-int-数据库中的类型ID，
                SPECIFICUNITCLASS-目标数据库DBID，
                SPECIFICUNIT-实际单元名称或GUID}
                例子：{'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
            area：{list: 参考点名称列表}
            stay_time 停留时间 {str: 格式'1:2:3:4' （'天:小时:分:秒'）}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        update_str = ''
        if target_filter_dict:
            target_filter_str = self.__generate_target_filter_str(target_filter_dict)
            if not target_filter_str:
                return "target_filter_dict不合法"
            update_str += f", TargetFilter={{{target_filter_str}}}"
        if rename:
            update_str += f", rename='{rename}'"
        if area:
            area_str = str(area).replace('[', '').replace(']', '')
            update_str += f", Area={{{area_str}}}"
        if stay_time:
            update_str += f", TD='{stay_time}'"

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='update',Type='UnitRemainsInArea'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_trigger_unit_enters_area(self, name, target_filter_dict, area, ETOA, LTOA, trigger_if_not_in_area):
        """
        功能：添加单元进入区域触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            target_filter_dict {dict:
                TARGETSIDE-str-推演方名称，
                TARGETTYPE-int-类型ID，
                    0 = NoneValue
                    1 = AircraftType
                    2 = ShipType
                    3 = SubmarineType
                    4 = FacilityType
                    5 = Aimpoint
                    6 = WeaponType
                    7 = SatelliteType
                  或 str
                    	Aircraft：飞机
                    	Ship：水面舰艇
                    	Submarine：潜艇
                    	Facility：地面兵力与设施
                TARGETSUBTYPE-int-数据库中的类型ID，
                SPECIFICUNITCLASS-目标数据库DBID，
                SPECIFICUNIT-实际单元名称或GUID}
                例子：{'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
            area：{list: 参考点名称列表}
            ETOA 最早到达日期/时间 {str: 格式'2020/8/10 10:12:2'}
            LTOA 最晚到达日期/时间 {str: 格式'2019/8/1 9:1:21'}
            trigger_when_not_in_area {str: 'true'- 若单元不在区域内则触发, 'false'-若单元在区域内则触发}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-13
        """
        target_filter_str = self.__generate_target_filter_str(target_filter_dict)
        if not target_filter_str:
            return "target_filter_dict不合法"

        area_str = str(area).replace('[', '').replace(']', '')

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='unitentersarea'," \
                     f"TargetFilter={{{target_filter_str}}}, Area={{{area_str}}}," \
                     f"ETOA='{ETOA}', LTOA='{LTOA}', NOT={trigger_if_not_in_area}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_trigger_unit_enters_area(self, name, rename=None, target_filter_dict=None, area=None, ETOA=None,
                                        LTOA=None, trigger_if_not_in_area=None):
        """
        功能：更新单元进入区域触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            rename:{str:新的触发器名称}
            target_filter_dict {dict:
                TARGETSIDE-str-推演方名称，
                TARGETTYPE-int-类型ID，
                    0 = NoneValue
                    1 = AircraftType
                    2 = ShipType
                    3 = SubmarineType
                    4 = FacilityType
                    5 = Aimpoint
                    6 = WeaponType
                    7 = SatelliteType
                  或 str
                    	Aircraft：飞机
                    	Ship：水面舰艇
                    	Submarine：潜艇
                    	Facility：地面兵力与设施
                TARGETSUBTYPE-int-数据库中的类型ID，
                SPECIFICUNITCLASS-目标数据库DBID，
                SPECIFICUNIT-实际单元名称或GUID}
                例子：{'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
            area：{list: 参考点名称列表}
            ETOA 最早到达日期/时间 {str: 格式'2020/8/10 10:12:2'}
            LTOA 最晚到达日期/时间 {str: 格式'2019/8/1 9:1:21'}
            trigger_when_not_in_area {str: 'true'- 若单元不在区域内则触发, 'false'-若单元在区域内则触发}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        update_str = ''
        if target_filter_dict:
            target_filter_str = self.__generate_target_filter_str(target_filter_dict)
            if not target_filter_str:
                return "target_filter_dict不合法"
            update_str += f", TargetFilter={{{target_filter_str}}}"
        if rename:
            update_str += f", rename='{rename}'"
        if area:
            area_str = str(area).replace('[', '').replace(']', '')
            update_str += f", Area={{{area_str}}}"
        if ETOA:
            update_str += f", ETOA='{ETOA}'"
        if LTOA:
            update_str += f", LTOA='{LTOA}'"
        if trigger_if_not_in_area:
            update_str += f", NOT={trigger_if_not_in_area}"

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='update',Type='unitentersarea'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_trigger_random_time(self, name, earliest_time, latest_time):
        """
        功能：添加随机时间触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            earliest_time 开始检查的最早日期/时间 :{str: 格式 2019/8/2 9:31:21}
            latest_time 停止检查的最晚日期/时间 :{str: 格式 2019/8/9 10:31:21}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='RandomTime'," \
                     f"EarliestTime='{earliest_time}', LatestTime='{latest_time}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_trigger_random_time(self, name, rename=None, earliest_time=None, latest_time=None):
        """
        功能：编辑随机时间触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            rename:{str:新的触发器名称}
            earliest_time 开始检查的最早日期/时间 :{str: 格式 2019/8/2 9:31:21}  # 显示时间-设置时间=4小时
            latest_time 停止检查的最晚日期/时间 :{str: 格式 2019/8/9 10:31:21}   # 显示时间-设置时间=4小时
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if earliest_time:
            update_str += f", EarliestTime='{earliest_time}'"
        if latest_time:
            update_str += f", LatestTime='{latest_time}'"

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='update',Type='RandomTime'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_trigger_scen_loaded(self, name):
        """
        功能：添加想定被加载触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='scenloaded'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_trigger_scen_loaded(self, name, rename):
        """
        功能：编辑想定被加载触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            rename:{str:新的触发器名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='update',Type='scenloaded', rename='{rename}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_trigger_regular_time(self, name, interval):
        """
        功能：添加规律时间触发器
        参数：
            name:{str:触发器名称}
            interval:{int:秒 0-1秒，1-5秒，2-15秒，3-30秒, 4-1分钟，
                            5-5分钟，6-15分钟，7-30分钟，8-1小时, 9-6小时，
                            10-6小时，11-24小时，12-0.1秒（高精度模式可用），13-0.5秒（高经度模式可用）}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='regulartime'," \
                     f"Interval={interval}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_trigger_regular_time(self, name, rename=None, interval=None):
        """
        功能：编辑规律时间触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            rename:{str:新的触发器名称}
            interval:{int:秒 0-1秒，1-5秒，2-15秒，3-30秒, 4-1分钟，
                            5-5分钟，6-15分钟，7-30分钟，8-1小时, 9-6小时，
                            10-6小时，11-24小时，12-0.1秒（高精度模式可用），13-0.5秒（高经度模式可用）}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if interval:
            update_str += f", Interval={interval}"

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='update',Type='regulartime'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_trigger_unit_detected(self, name, target_filter_dict, detector_side, MCL):
        """
        功能：添加单元被探测到触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            target_filter_dict {dict:
                TARGETSIDE-str-推演方名称，
                TARGETTYPE-int-类型ID，
                    0 = NoneValue
                    1 = AircraftType
                    2 = ShipType
                    3 = SubmarineType
                    4 = FacilityType
                    5 = Aimpoint
                    6 = WeaponType
                    7 = SatelliteType
                  或 str
                    	Aircraft：飞机
                    	Ship：水面舰艇
                    	Submarine：潜艇
                    	Facility：地面兵力与设施
                TARGETSUBTYPE-int-数据库中的类型ID，
                SPECIFICUNITCLASS-目标数据库DBID，
                SPECIFICUNIT-实际单元名称或GUID}
                例子：{'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
            detector_side：{str: 探测推演方}
            MCL 最小分类级别 {int: 0-不明，1-知道领域(舰艇、飞机)，2-知道类型（护卫舰，轰炸机），3-知道型号（F-16）， 4-具体ID}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-13
        """
        target_filter_str = self.__generate_target_filter_str(target_filter_dict)
        if not target_filter_str:
            return "target_filter_dict不合法"

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='UnitDetected'," \
                     f"TargetFilter={{{target_filter_str}}}, DetectorSideID='{detector_side}'," \
                     f"MCL={MCL}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_trigger_unit_detected(self, name, rename=None, target_filter_dict=None, detector_side=None, MCL=None):
        """
        功能：更新单元被探测到触发器
        限制：专项赛禁用
        参数：
            name:{str:触发器名称}
            rename:{str:新的触发器名称}
            target_filter_dict {dict:
                TARGETSIDE-str-推演方名称，
                TARGETTYPE-int-类型ID，
                    0 = NoneValue
                    1 = AircraftType
                    2 = ShipType
                    3 = SubmarineType
                    4 = FacilityType
                    5 = Aimpoint
                    6 = WeaponType
                    7 = SatelliteType
                  或 str
                    	Aircraft：飞机
                    	Ship：水面舰艇
                    	Submarine：潜艇
                    	Facility：地面兵力与设施
                TARGETSUBTYPE-int-数据库中的类型ID，
                SPECIFICUNITCLASS-目标数据库DBID，
                SPECIFICUNIT-实际单元名称或GUID}
                例子：{'TARGETSIDE': '红方', 'TARGETTYPE': 1, 'TARGETSUBTYPE': 6002, 'SPECIFICUNITCLASS': 2802}
            detector_side：{str: 探测推演方}
            MCL 最小分类级别 {int: 0-不明，1-知道领域(舰艇、飞机)，2-知道类型（护卫舰，轰炸机），3-知道型号（F-16）， 4-具体ID}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        update_str = ''
        if target_filter_dict:
            target_filter_str = self.__generate_target_filter_str(target_filter_dict)
            if not target_filter_str:
                return "target_filter_dict不合法"
            update_str += f", TargetFilter={{{target_filter_str}}}"
        if rename:
            update_str += f", rename='{rename}'"
        if detector_side:
            update_str += f", DetectorSideID='{detector_side}'"
        if MCL:
            update_str += f", MCL={MCL}"

        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='update',Type='UnitDetected'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def remove_trigger(self, name):
        """
        功能：删除触发器
        限制：专项赛禁用
        其他信息：如果触发器分配给了某事件，必须移除该事件才能移除该触发器
        参数：
            name:{str:触发器名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='remove'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_action_points(self, name, side_name, point_change):
        """
        功能：添加推演方得分动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
            side:{str:推演方名称}
            point_change:{int:推演方得分变化}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='add',Type='Points'," \
                     f"SideID='{side_name}', PointChange={point_change}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_action_points(self, name, rename=None, side_name=None, point_change=None):
        """
        功能：编辑推演方得分动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
            rename:{str:新的动作名称}
            side:{str:推演方名称}
            point_change:{int:推演方得分变化}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if side_name:
            update_str += f", SideID='{side_name}'"
        if point_change:
            update_str += f", PointChange={point_change}"
        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='update',Type='Points'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_action_end_scenario(self, name):
        """
        功能：添加终止想定动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='add',Type='EndScenario'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_action_end_scenario(self, name, rename):
        """
        功能：编辑终止想定动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
            rename:{str:新的动作名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetAction({{name='{name}', rename='{rename}', Mode='update',Type='EndScenario'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_action_teleport_in_area(self, name, unit_list, area):
        """
        功能：添加单元瞬时移动动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
            unit_list:{list: 单元名称或单元guid列表}
            area：{list: 参考点名称列表}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        area_str = str(area).replace('[', '').replace(']', '')
        unit_list_str = str(unit_list).replace('[', '').replace(']', '')
        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='add',Type='TeleportInArea'," \
                     f"UnitIDs={{{unit_list_str}}}, Area={{{area_str}}}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_action_teleport_in_area(self, name, rename=None, unit_list=None, area=None):
        """
        功能：编辑单元瞬时移动动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
            rename:{str:新的动作名称}
            unit_list:{list: 单元名称或单元guid列表}
            area：{list: 参考点名称列表}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if unit_list:
            unit_list_str = str(unit_list).replace('[', '').replace(']', '')
            update_str += f", UnitIDs={{{unit_list_str}}}"
        if area:
            area_str = str(area).replace('[', '').replace(']', '')
            update_str += f", Area={{{area_str}}}"

        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='update',Type='TeleportInArea'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_action_message(self, name, side, text):
        """
        功能：添加消息动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
            side:{str: 推演方名称}
            text：{str: 消息内容}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='add',Type='Message'," \
                     f"SideID='{side}', text='{text}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_action_message(self, name, rename=None, side=None, text=None):
        """
        功能：编辑消息动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
            rename:{str:新的动作名称}
            side:{str: 推演方名称}
            text：{str: 消息内容}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if side:
            update_str += f", SideID='{side}'"
        if text:
            update_str += f", text='{text}'"
        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='update',Type='Message'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_action_change_mission_status(self, name, side, mission, new_status):
        """
        功能：添加改变任务状态动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
            side:{str: 推演方名称}
            mission：{str: 任务名称}
            new_status：{int: 0-激活，1-不激活}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='add',Type='ChangeMissionStatus'," \
                     f"MissionID='{mission}', NewStatus={new_status}, SideID='{side}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_action_change_mission_status(self, name, rename=None, side=None, mission=None, new_status=None):
        """
        功能：编辑改变任务状态动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
            rename:{str:新的动作名称}
            side:{str: 推演方名称}
            mission：{str: 任务名称}
            new_status：{int: 0-激活，1-不激活}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if side:
            update_str += f", SideID='{side}'"
        if mission:
            update_str += f", MissionID='{mission}'"
        if new_status:
            update_str += f", NewStatus={new_status}"
        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='update',Type='ChangeMissionStatus'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_action_lua_script(self, name, script_text):
        """
        功能：添加执行lua脚本动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
            script_text:{str: lua脚本}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='add',Type='LuaScript'," \
                     f"ScriptText=\"{script_text}\"}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_action_lua_script(self, name, rename=None, script_text=None):
        """
        功能：编辑执行lua脚本动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
            rename:{str:新的动作名称}
            script_text:{str: lua脚本}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if script_text:
            update_str += f", ScriptText=\"{script_text}\""

        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='update',Type='LuaScript'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def remove_action(self, name):
        """
        功能：删除动作
        限制：专项赛禁用
        参数：
            name:{str:动作名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetAction({{name='{name}',Mode='remove'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_event(self, name):
        """
        功能：添加事件
        限制：专项赛禁用
        参数：
            name:{str:事件名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetEvent('{name}', {{Mode='add'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def remove_event(self, name):
        """
        功能：删除事件
        限制：专项赛禁用
        参数：
            name:{str:事件名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetEvent('{name}', {{Mode='remove'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def set_event_trigger(self, event_name, trigger_name):
        """
        功能：添加事件的触发器
        限制：专项赛禁用
        参数：
            event_name:{str:事件名称}
            trigger_name:{str:触发器名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetEventTrigger('{event_name}', {{Mode='add', name='{trigger_name}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def replace_event_trigger(self, event_name, trigger_name, new_trigger_name):
        """
        功能：替换事件的触发器
        限制：专项赛禁用
        参数：
            event_name:{str:事件名称}
            trigger_name:{str:触发器名称}
            new_trigger_name:{str:新的触发器名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetEventTrigger('{event_name}', {{Mode='replace', name='{trigger_name}', " \
                     f"replacedby='{new_trigger_name}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def set_event_action(self, event_name, action_name):
        """
        功能：添加事件的动作
        限制：专项赛禁用
        参数：
            event_name:{str:事件名称}
            action_name:{str:动作名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetEventAction('{event_name}', {{Mode='add', name='{action_name}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def replace_event_action(self, event_name, action_name, new_action_name):
        """
        功能：替换事件的动作
        限制：专项赛禁用
        参数：
            event_name:{str:事件名称}
            action_name:{str:动作名称}
            new_action_name:{str:新的动作名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-14
        """
        lua_script = f"ScenEdit_SetEventAction('{event_name}', {{Mode='replace', name='{action_name}', " \
                     f"replacedby='{new_action_name}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def set_event_condition(self, event_name, condition_name):
        """
        功能：添加事件的条件
        限制：专项赛禁用
        参数：
            event_name:{str:事件名称}
            condition_name:{str:条件名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        lua_script = f"ScenEdit_SetEventCondition('{event_name}', {{Mode='add', name='{condition_name}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def replace_event_condition(self, event_name, condition_name, new_condition_name):
        """
        功能：替换事件的条件
        限制：专项赛禁用
        参数：
            event_name:{str:事件名称}
            condition_name:{str:条件名称}
            new_condition_name:{str:新的条件名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        lua_script = f"ScenEdit_SetEventCondition('{event_name}', {{Mode='replace', name='{condition_name}', " \
                     f"replacedby='{new_condition_name}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_event_attribute(self, event_name, new_event_name=None, is_active=None, is_shown=None,
                               is_repeatable=None, probability=None):
        """
        功能：更新事件的属性
        限制：专项赛禁用
        参数：
            event_name:{str:事件名称}
            new_event_name:{str:新的事件名称}
            is_active 是否启用:{str:'true'-是，'false'-否}
            is_shown 是否显示：{str:'true'-是，'false'-否}
            is_repeatable 是否可重复{str:'true'-是，'false'-否}
            probability:{int:发生概率%}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        update_str = ''
        if new_event_name:
            update_str += f", Description='{new_event_name}'"
        if is_active:
            update_str += f", IsActive='{is_active}'"
        if is_shown:
            update_str += f", IsShown={is_shown}"
        if is_repeatable:
            update_str += f", IsRepeatable={is_repeatable}"
        if probability:
            update_str += f", Probability={probability}"

        if update_str:
            update_str = update_str[1:]
        lua_script = f"ScenEdit_UpdateEvent('{event_name}', {{{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_condition_side_posture(self, name, observer_side, target_side, target_posture, is_reverse):
        """
        功能：添加推演方立场条件
        限制：专项赛禁用
        参数：
            name:{str:条件名称}
            observer_side:{str: 推演方名称}
            target_side:{str: 考虑推演方名称}
            target_posture： observer_side视作target_side的关系:
                {int: 0-中立方，1-友方，2-非友方，3-敌方， 4-不明}
            is_reverse 条件是否取反 {str: true-是，false-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        lua_script = f"ScenEdit_SetCondition({{name='{name}',Mode='add',Type='sideposture'," \
                     f"ObserverSideID='{observer_side}',TargetSideID='{target_side}'," \
                     f"TargetPosture='{target_posture}', NOT={is_reverse}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_condition_side_posture(self, name, rename=None, observer_side=None, target_side=None,
                                      target_posture=None, is_reverse=None):
        """
        功能：编辑推演方立场条件
        限制：专项赛禁用
        参数：
            name:{str:条件名称}
            rename:{str:新的条件名称}
            observer_side:{str: 推演方名称}
            target_side:{str: 考虑推演方名称}
            target_posture observer_side视作target_side的关系:
                {int: 0-中立方，1-友方，2-非友方，3-敌方， 4-不明}
            is_reverse 条件是否取反 {str: true-是，false-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if observer_side:
            update_str += f", ObserverSideID='{observer_side}'"
        if target_side:
            update_str += f", TargetSideID='{target_side}'"
        if target_posture:
            update_str += f", TargetPosture={target_posture}"
        if is_reverse:
            update_str += f", NOT={is_reverse}"

        lua_script = f"ScenEdit_SetCondition({{name='{name}',Mode='update',Type='sideposture'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_condition_scen_has_started(self, name, is_reverse):
        """
        功能：添加想定已经开始条件
        限制：专项赛禁用
        参数：
            name:{str:条件名称}
            is_reverse 条件是否取反 {str: true-是，false-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        lua_script = f"ScenEdit_SetCondition({{name='{name}',Mode='add',Type='scenhasstarted', NOT={is_reverse}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_condition_scen_has_started(self, name, rename=None, is_reverse=None):
        """
        功能：编辑想定已经开始条件
        限制：专项赛禁用
        参数：
            name:{str:条件名称}
            rename:{str:新的条件名称}
            is_reverse 条件是否取反 {str: true-是，false-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if is_reverse:
            update_str += f", NOT={is_reverse}"
        lua_script = f"ScenEdit_SetCondition({{name='{name}',Mode='update',Type='scenhasstarted'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_condition_lua_script(self, name, script_text):
        """
        功能：添加lua脚本条件
        限制：专项赛禁用
        参数：
            name:{str:条件名称}
            script_text {str: lua脚本}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        lua_script = f"ScenEdit_SetCondition({{name='{name}',Mode='add',Type='LuaScript', " \
                     f"ScriptText=\"{script_text}\"}})"
        return self.mozi_server.send_and_recv(lua_script)

    def update_condition_lua_script(self, name, rename=None, script_text=None):
        """
        功能：编辑lua脚本条件
        限制：专项赛禁用
        参数：
            name:{str:条件名称}
            rename:{str:新的条件名称}
            script_text {str: lua脚本}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        update_str = ''
        if rename:
            update_str += f", rename='{rename}'"
        if script_text:
            update_str += f", ScriptText=\"{script_text}\""
        lua_script = f"ScenEdit_SetCondition({{name='{name}',Mode='update',Type='LuaScript'" \
                     f"{update_str}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def remove_condition(self, name):
        """
        功能：删除条件
        限制：专项赛禁用
        参数：
            name:{str:条件名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-16
        """
        lua_script = f"ScenEdit_SetCondition({{name='{name}',Mode='remove'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_trigger_aircraft_take_off(self, name, side_guid):
        """
        功能：添加飞机起飞触发器 10006版本墨子不可用
        限制：专项赛禁用
        参数：name:{str:触发器名称}
            side_guid {str: 推演方guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-7
        """
        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='AircraftTakeOff'," \
                     f"DetectorSideID='{side_guid}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def add_trigger_aircraft_landing(self, name, side_guid):
        """
        功能：添加飞机降落触发器 10006版本墨子不可用
        限制：专项赛禁用
        参数：name:{str:触发器名称}
            side_guid {str: 推演方guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-7
        """
        lua_script = f"ScenEdit_SetTrigger({{name='{name}',Mode='add',Type='AircraftLanding'," \
                     f"DetectorSideID='{side_guid}'}})"
        return self.mozi_server.send_and_recv(lua_script)
