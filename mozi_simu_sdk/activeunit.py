# -*- coding:utf-8 -*-
##########################################################################################################
# File name : activeunit.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################
import re


class CActiveUnit:
    """
    活动单元（潜艇、水面舰艇、地面兵力及设施、飞机、卫星、离开平台射向目标的武器，不包含目标、传感器等）的父类
    """

    def __init__(self, strGuid, mozi_server, situation):
        # GUID
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 态势
        self.situation = situation
        # 活动单元传感器列表
        self.sensors = {}
        # 活动单元挂架
        self.mounts = {}
        # 活动单元挂载
        self.loadout = {}
        # 挂载方案的GUid
        self.m_LoadoutGuid = ""
        # 活动单元弹药库
        self.magazines = {}
        # 航路点
        self.way_points = {}
        # 对象类名
        self.ClassName = ""
        # 名称
        self.strName = ""
        # 地理高度
        self.fAltitude_AGL = 0.0
        # 海拔高度
        self.iAltitude_ASL = 0
        # 所在推演方ID
        self.m_Side = ""
        # 单元类别
        self.strUnitClass = ""
        # 当前纬度
        self.dLatitude = 0.0
        # 当前经度
        self.dLongitude = 0.0
        # 当前朝向
        self.fCurrentHeading = 0.0
        # 当前速度
        self.fCurrentSpeed = 0.0
        # 当前海拔高度
        self.fCurrentAltitude_ASL = 0.0
        # 倾斜角
        self.fPitch = 0.0
        # 翻转角
        self.fRoll = 0.0
        # 获取期望速度
        self.fDesiredSpeed = 0.0
        # 获取最大油门
        self.m_MaxThrottle = 0
        # 最大速度
        self.fMaxSpeed = 0.0
        # 最小速度
        self.fMinSpeed = 0.0
        # 当前高度
        self.fCurrentAlt = 0.0
        # 期望高度
        self.fDesiredAlt = 0.0
        # 最大高度
        self.fMaxAltitude = 0.0
        # 最小高度
        self.fMinAltitude = 0.0
        # 军标ID
        self.strIconType = ""
        # 普通军标
        self.strCommonIcon = ""
        # 数据库ID
        self.iDBID = 0
        # 是否可操作
        self.bIsOperating = False
        # 编组ID
        self.m_ParentGroup = ""
        # 停靠的设施的ID(关系)
        self.m_DockedUnits = ""
        # 单元的停靠设施(部件)
        self.m_DockFacilitiesComponent = ""
        # 停靠的飞机的ID(关系)
        self.m_DockAircrafts = ""
        # 单元的航空设施(部件)
        self.m_AirFacilitiesComponent = ""
        # 单元的通信设备及数据链(部件)
        self.m_CommDevices = ""
        # 单元的引擎(部件)
        self.m_Engines = ""
        # 传感器，需要构建对象类,所以只传ID
        self.m_Sensors = ""
        # 挂架
        self.m_Mounts = ""
        # 毁伤状态
        self.strDamageState = ""
        # 失火
        self.iFireIntensityLevel = 0
        # 进水
        self.iFloodingIntensityLevel = 0
        # 分配的任务
        self.m_AssignedMission = ""
        # 作战条令
        self.m_Doctrine = None
        # 系统右栏->对象信息->作战单元武器
        self.m_UnitWeapons = ""
        # 路径点
        self.m_WayPoints = ""
        # 训练水平
        self.m_ProficiencyLevel = 0
        # 是否是护卫角色
        self.bIsEscortRole = False
        # 当前油门
        self.m_CurrentThrottle = 0
        # 通讯设备是否断开
        self.bIsCommsOnLine = False
        self.bIsIsolatedPOVObject = False
        # 地形跟随
        self.bTerrainFollowing = False
        self.bIsRegroupNeeded = False
        # 保持阵位
        self.bHoldPosition = False
        # 是否可自动探测
        self.bAutoDetectable = False
        # 当前货物
        self.m_Cargo = ""
        # 燃油百分比，作战单元燃油栏第一个进度条的值
        self.dFuelPercentage = 0.0
        # 获取AI对象的目标集合# 获取活动单元AI对象的每个目标对应显示不同的颜色集合
        self.m_AITargets = ""
        # 获取活动单元AI对象的每个目标对应显示不同的颜色集合
        self.m_AITargetsCanFiretheTargetByWCSAndWeaponQty = ""
        # 获取单元的通讯链集合
        self.m_CommLink = ""
        # 获取传感器
        self.m_NoneMCMSensors = ""
        # 获取显示"干扰"或"被干扰"
        self.iDisturbState = 0
        # 单元所属多个任务数量
        self.iMultipleMissionCount = 0
        # 单元所属多个任务guid拼接
        self.m_MultipleMissionGUIDs = ""
        # 是否遵守电磁管控
        self.bObeysEMCON = False
        # 武器预设的打击航线
        self.m_strContactWeaponWayGuid = ""
        # 停靠参数是否包含码头
        self.bDockingOpsHasPier = False
        # 弹药库
        self.m_Magazines = ""
        # 被摧毁
        self.dPBComponentsDestroyedWidth = 0.0
        # 轻度
        self.dPBComponentsLightDamageWidth = 0.0
        # 中度
        self.dPBComponentsMediumDamageWidth = 0.0
        # 重度
        self.dPBComponentsHeavyDamageWidth = 0.0
        # 正常
        self.dPBComponentsOKWidth = 0.0
        # 配属基地
        self.m_HostActiveUnit = ""
        # 状态
        self.strActiveUnitStatus = ""
        # 精简
        self.doctrine = None

    def get_assigned_mission(self):
        """
        功能：获取分配的任务
        参数：无
        返回：任务对象
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2021-7-28
        """
        return self.situation.get_obj_by_guid(self.m_AssignedMission)

    def get_original_detector_side(self):
        """
        功能：获取单元所在方
        参数：无
        返回：CSide对象
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2021-7-28
        """
        return self.situation.side_dic[self.m_Side]

    def get_par_group(self):
        """
        功能：获取父级编组
        参数：无
        返回：CGroup对象
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2021-7-28
        """
        return self.situation.group_dic[self.m_ParentGroup]

    def get_docked_units(self):
        """
        功能：获取停靠单元
        参数：无
        返回：单元字典，{guid1: unit_obj1, guid2: unit_obj2, ...}
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2021-7-28
        张志高修改于2021-7-28
        """
        docked_units = {}
        docked_units_guid = self.m_DockedUnits.split("@")
        for guid in docked_units_guid:
            if guid in self.situation.submarine_dic:
                docked_units[guid] = self.situation.submarine_dic[guid]
            elif guid in self.situation.ship_dic:
                docked_units[guid] = self.situation.ship_dic[guid]
            elif guid in self.situation.facility_dic:
                docked_units[guid] = self.situation.facility_dic[guid]
            elif guid in self.situation.aircraft_dic:
                docked_units[guid] = self.situation.aircraft_dic[guid]
            elif guid in self.situation.satellite_dic:
                docked_units[guid] = self.situation.satellite_dic[guid]
        return docked_units

    def get_doctrine(self):
        """
        功能：获取单元条令
        参数：无
        返回：CDoctrine对象
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：2021-7-28
        """
        if self.m_Doctrine in self.situation.doctrine_dic:
            doctrine = self.situation.doctrine_dic[self.m_Doctrine]
            doctrine.category = 'Unit'  # 需求来源：20200331-2/2:Xy
            return doctrine
        return None

    def get_weapon_db_guids(self):
        """
        功能：获取编组内所有武器的数据库guid
        参数：无
        返回：编组内所有武器的guid组成的列表
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        张志高修改于2021-7-28
        """
        weapon_record = self.m_UnitWeapons
        lst1 = []
        if weapon_record:
            lst = weapon_record.split('@')
            lst1 = [k.split('$')[1] for k in lst]
        return lst1

    def get_weapon_infos(self):
        """
        功能：获取编组内所有武器的名称及数据库guid
        参数：无
        返回：编组内所有武器的名称及dbid组成的列表
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        kinds = ['CWeapon', 'CUnguidedWeapon', 'CWeaponImpact']
        if self.ClassName in kinds:
            return '本身是武器实体'
        weapon_record = self.m_UnitWeapons
        lst = weapon_record.split('@')
        lst1 = [k.split('$') for k in lst]
        return [x for x in lst1 if x != ['']]

    def get_mounts(self):
        """
        功能：获取挂架信息
        参数：无
        返回：挂架字典，格式{mount_guid1: mount_obj1, mount_guid2: mount_obj2, ...}
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        mounts_guid = self.m_Mounts.split('@')
        mounts_dic = {}
        for guid in mounts_guid:
            if guid in self.situation.mount_dic:
                mounts_dic[guid] = self.situation.mount_dic[guid]
        return mounts_dic

    def get_loadout(self):
        """
        功能：获取挂载
        参数：无
        返回：挂载字典，格式{loadout_guid1: loadout_obj1, loadout_guid2: loadout_obj2, ...}
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        loadout_dic = {}
        loadout_guid = self.m_LoadoutGuid.split('@')
        for guid in loadout_guid:
            if guid in self.situation.loadout_dic:
                loadout_dic[guid] = self.situation.loadout_dic[guid]
        return loadout_dic

    def get_magazines(self):
        """
        功能：获取弹药库
        参数：无
        返回：弹药库字典，格式{magazine_guid1: magazine_obj1, magazine_guid2: magazine_obj2, ...}
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        magazines_dic = {}
        magazines_guid = self.m_Magazines.split('@')
        for guid in magazines_guid:
            if guid in self.situation.magazine_dic:
                magazines_dic[guid] = self.situation.magazine_dic[guid]
        return magazines_dic

    def get_sensor(self):
        """
        功能：获取传感器
        参数：无
        返回：传感器字典，格式{sensor_guid1: sensor_obj1, sensor_guid2: sensor_obj2, ...}
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        sensors_guid = self.m_NoneMCMSensors.split('@')
        sensors_dic = {}
        for guid in sensors_guid:
            if guid in self.situation.sensor_dic:
                sensors_dic[guid] = self.situation.sensor_dic[guid]
        return sensors_dic

    def get_range_to_contact(self, contact_guid):
        """
        功能：获取单元与目标的距离（单位海里）
        参数：无
        返回：数字型字符串 - 单位海里
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        cmd = "print(Tool_Range('{}','{}'))".format(self.strGuid, contact_guid)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def plot_course(self, course_list):
        """
        功能：规划单元航线
        参数：course_list: list, [(lat, lon)]
        例子：[(40, 39.0), (41, 39.0)]
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        if not course_list:
            return
        course_para = "{ longitude=" + str(course_list[0][1]) + ",latitude=" + str(course_list[0][0]) + "}"
        for point in course_list[1:]:
            latitude = point[0]
            longitude = point[1]
            course_para = course_para + ",{ longitude=" + str(longitude) + ",latitude=" + str(latitude) + "}"
        cmd_str = "HS_LUA_SetUnit({side='" + self.m_Side + "', guid='" + self.strGuid + "', course={" + course_para + \
                  "}})"
        return self.mozi_server.send_and_recv(cmd_str)

    def get_way_points_info(self):
        """
        功能：获取本单元航路点信息
        参数：无
        返回：单元航路点列表
        例子：[{'latitude': 26.0728267704942, 'longitude': 125.582813973341, 'Description': ' '},
              {'latitude': 26.410343165174, 'longitude': 125.857575579442, 'Description': ' '}]
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        way_points = []
        if self.m_WayPoints != "":
            guid_list = self.m_WayPoints.split("@")
            for guid in guid_list:
                point_obj = self.situation.waypoint_dic[guid]
                way_points.append({
                    "latitude": point_obj.dLatitude,
                    "longitude": point_obj.dLongitude,
                    "Description": point_obj.strWayPointDescription
                })
        return way_points

    def get_ai_targets(self):
        """
        功能：获取活动单元的Ai目标集合
        参数：无
        返回：AI目标字典，格式{guid1: contact_obj, guid2: contact_obj}
        例子：{'801ea534-a57c-4d3b-ba5d-0f77e909506c': <mozi_simu_sdk.contact.CContact object at 0x000002C27BFCBCF8>,
               '781cc773-30e3-440d-8750-1b5cddb90249': <mozi_simu_sdk.contact.CContact object at 0x000002C27BFEDB00>}
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        contacts_dic = {}
        tar_guid_list = self.m_AITargets.split('@')
        for tar_guid in tar_guid_list:
            if tar_guid in self.situation.contact_dic:
                contacts_dic[tar_guid] = self.situation.contact_dic[tar_guid]
        return contacts_dic

    def unit_obeys_emcon(self, is_obey):
        """
        功能：单元传感器面板， 单元是否遵循电磁管控条令
        参数：is_obey:{str:'true'-遵守，'false'-不遵守}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        state = str(is_obey).lower()
        return self.mozi_server.send_and_recv("Hs_UnitObeysEMCON('{}', {})".format(self.strGuid, state))

    def allocate_weapon_to_target(self, target, weapon_db_guid, weapon_count):
        """
        功能：单元手动攻击(打击情报目标), 或者纯方位攻击(打击一个位置)
        参数：target:{str: 情报目标guid} 或 {tuple(lat, lon)：坐标}
            weapon_db_guid {str: 武器型号数据库guid}
            weapon_count {int: 分配数量}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        if type(target) == str:
            table = "{TargetGUID ='" + target + "'}"
        elif type(target) == tuple:
            table = "{TargetLatitude =" + str(target[0]) + ", TargetLongitude = " + str(target[1]) + "}"
        else:
            raise Exception("target 参数错误")
        return self.mozi_server.send_and_recv("Hs_ScenEdit_AllocateWeaponToTarget('{}',{},'{}',{})".format(
            self.strGuid, table, str(weapon_db_guid), str(weapon_count)))

    def unit_drop_target_contact(self, contact_guid):
        """
        功能： 放弃对指定目标进行攻击。
        参数：ContactID:{str: 目标GUID}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        修订：aie
        时间：4/8/20
        """
        lua_script = "Hs_UnitDropTargetContact('{}','{}','{}')".format(self.m_Side, self.strGuid, contact_guid)
        return self.mozi_server.send_and_recv(lua_script)

    def unit_drop_target_all_contact(self):
        """
        功能： 放弃对所有目标进行攻击。
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv("Hs_UnitDropTargetAllContact('{}')".format(self.strGuid))

    def ignore_plotted_course_when_attacking(self, ignore_plotted):
        """
        功能： 指定单元攻击时是否忽略计划航线。
        参数：ignore_plotted:{str:'Yes'-忽略，'No'-不忽略, 'Inherited'-按上级条令执行}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv(
            "Hs_LPCWAttackSUnit('{}','{}','{}')".format(self.m_Side, self.strGuid, ignore_plotted))

    def follow_terrain(self, is_followed):
        """
        功能： 设置当前单元（飞机）的飞行高度跟随地形
        参数：is_followed:{str:'true'-是，'false'-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        set_str = str(is_followed).lower()
        lua_script = "ScenEdit_SetUnit({guid='%s',TEEEAINFOLLOWING=%s})" % (str(self.strGuid), set_str)
        return self.mozi_server.send_and_recv(lua_script)

    def delete_coursed_point(self, point_index=None, clear=False):
        """
        功能： 单元删除航路点
        参数：clear:{bool:True-是,清空所有航路点，False-否, 按point_index删除航路点}
            point_index:{int:航路点index, 删除航路点的序号，从0开始，0代表离单元最近的航路点}
                        or {int list:[0, 1], 删除航路点的序号列表}}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        lua_script = ""
        if clear:
            if self.m_WayPoints != "":
                point_count = len(self.m_WayPoints.split("@"))
                for point in range(point_count - 1, -1, -1):
                    lua_script += ('Hs_UnitOperateCourse("%s",%d,0.0,0.0,"Delete")' % (self.strGuid, point))
        else:
            if isinstance(point_index, list):
                if len(point_index) > 1 and point_index[-1] > point_index[0]:
                    point_index.reverse()
                for point in point_index:
                    lua_script += ('Hs_UnitOperateCourse("%s",%d,0.0,0.0,"Delete")' % (self.strGuid, point))
            elif isinstance(point_index, int):
                lua_script = "Hs_UnitOperateCourse('%s',%d,0.0,0.0,'Delete')" % (self.strGuid, point_index)
        return self.mozi_server.send_and_recv(lua_script)

    def return_to_base(self):
        """
        功能： 单元返航
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv("HS_ReturnToBase('{}')".format(self.strGuid))

    def select_new_base(self, base_guid):
        """
        功能： 单元选择新基地/新港口
        参数：base_guid {str: 新基地的guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        lua_script = "ScenEdit_SetUnit({guid='%s',base='%s'})" % (self.strGuid, base_guid)
        return self.mozi_server.send_and_recv(lua_script)

    def hold_position(self, is_hold):
        """
        功能： 命令面上指定单元设置是否保持阵位。 该接口暂不可用
        参数： is_hold {str:true-是，false-否}
        返回： 'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv("Hs_HoldPositonSelectedUnit('{}',{})".format(self.strGuid, is_hold))

    def leave_dock_alone(self):
        """
        功能：单独出航
        参数：
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        cmd = "Hs_ScenEdit_DockingOpsGroupOut({'%s'})" % (self.strGuid)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def assign_unit_to_mission(self, mission_name):
        """
        功能：分配加入到任务中
        参数：mission_name {str - 任务名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        lua_script = "ScenEdit_AssignUnitToMission('{}', '{}')".format(self.strGuid, mission_name)
        return self.mozi_server.send_and_recv(lua_script)

    def assign_unit_to_mission_escort(self, mission_name):
        """
        功能：将单元分配为某打击任务的护航任务
        参数：mission_name {str - 任务名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        lua_script = "ScenEdit_AssignUnitToMission('{}', '{}', true)".format(self.strGuid, mission_name)
        return self.mozi_server.send_and_recv(lua_script)

    def cancel_assign_unit_to_mission(self):
        """
        功能：将单元取消分配任务
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        lua_script = "ScenEdit_AssignUnitToMission('{}', 'none')".format(self.strGuid)
        return self.mozi_server.send_and_recv(lua_script)

    def set_unit_heading(self, heading):
        """
        功能：设置朝向
        参数：heading {int - 朝向}
        返回：'lua执行成功' 或 '脚本执行出错'
        example: set_unit_heading('016b72ba-2ab2-464a-a340-3cfbfb133ed1',30)
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        lua_script = "ScenEdit_SetUnit({guid ='%s' ,heading = %s})" % (self.strGuid, heading)
        return self.mozi_server.send_and_recv(lua_script)

    def auto_attack(self, contact_guid):
        """
        功能：自动攻击目标
        参数：contact_guid {str - 目标guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        return self.mozi_server.send_and_recv(
            "ScenEdit_AttackContact('%s', '%s', {mode=%s})" % (self.strGuid, contact_guid, 0))

    def set_desired_speed(self, desired_speed):
        """
        功能：设置单元的期望速度
        参数：desired_speed {int or float - 单元期望速度，单位千米/小时}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        if isinstance(desired_speed, int) or isinstance(desired_speed, float):
            lua_script = "ScenEdit_SetUnit({guid='" + str(self.strGuid) + "', manualSpeed=" + str(
                desired_speed / 1.852) + "})"
            return self.mozi_server.send_and_recv(lua_script)

    def set_throttle(self, enum_throttle):
        """
        功能：设置单元油门
        参数：enum_throttle {int, 1-低速，2-巡航，3-全速， 4-军用}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        lua_script = "ScenEdit_SetUnit({guid='%s', throttle=%s})" % (self.strGuid, enum_throttle)
        return self.mozi_server.send_and_recv(lua_script)

    def set_radar_shutdown(self, on_off):
        """
        功能：设置雷达开关机
        参数：on_off {str, 'true'-开机, 'false'-关机}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        lua_script = "Hs_ScenEdit_SetUnitSensorSwitch({guid ='%s',rader=%s})" % (self.strGuid, on_off)
        return self.mozi_server.send_and_recv(lua_script)

    def set_sonar_shutdown(self, on_off):
        """
        功能：设置声纳开关机
        参数：on_off {str, 'true'-开机, 'false'-关机}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        lua_script = "Hs_ScenEdit_SetUnitSensorSwitch({guid ='%s',SONAR=%s })" % (self.strGuid, on_off)
        return self.mozi_server.send_and_recv(lua_script)

    def set_oecm_shutdown(self, on_off):
        """
        功能：设置干扰机开关机
        参数：on_off {str, 'true'-开机, 'false'-关机}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        lua_script = "Hs_ScenEdit_SetUnitSensorSwitch({guid = '%s',OECM=%s})" % (self.strGuid, on_off)
        return self.mozi_server.send_and_recv(lua_script)

    def manual_attack(self, target_guid, weapon_db_guid, weapon_num):
        """
        功能：手动开火函数
        参数：target_guid {str: 目标guid}
            weapon_db_guid {int: 武器的数据库guid}
            weapon_num {int: 武器数量}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：解洋
        修订：张志高 2021-8-3
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        manual_lua = 'Hs_ScenEdit_AllocateWeaponToTarget(\'%s\',{TargetGUID=\'%s\'},\'%s\',%s)' % (
            self.strGuid, target_guid, weapon_db_guid, weapon_num)
        return self.mozi_server.send_and_recv(manual_lua)

    def set_single_out(self):
        """
        功能：设置飞机在基地内单机出动
        参数：无
        返回：'lua执行成功' 或 '脚本执行出错' 或 '不是飞机'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        if self.ClassName == 'CAircraft':
            lua_script = "Hs_ScenEdit_AirOpsSingleOut({'%s'})" % self.strGuid
        else:
            return "不是飞机"
        return self.mozi_server.send_and_recv(lua_script)

    def drop_active_sonobuoy(self, deep_or_shallow):
        """
        功能：投放主动声呐
        参数：deep_or_shallow {str: 'deep'-深-温跃层之下， 'shallow'-浅-温跃层之上}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        side = self.situation.side_dic[self.m_Side]
        cmd = "Hs_DropActiveSonobuoy('{}','{}','{}')".format(side.strName, self.strGuid, deep_or_shallow)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def drop_passive_sonobuoy(self, deep_or_shallow):
        """
        功能：投放被动声呐
        参数：deep_or_shallow {str: 'deep'-深-温跃层之下， 'shallow'-浅-温跃层之上}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        side = self.situation.side_dic[self.m_Side]
        cmd = "Hs_DropPassiveSonobuoy('{}','{}','{}')".format(side.strName, self.strGuid, deep_or_shallow)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def drop_sonobuoy(self, deep_or_shallow, passive_or_active):
        """
        功能：投放声呐,目前只能飞机投放声纳
        参数：deep_or_shallow {str: 'deep'-深-温跃层之下， 'shallow'-浅-温跃层之上}
            passive_or_active {str: 'active'-主动声呐， 'passive'-被动声呐}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        side = self.situation.side_dic[self.m_Side]
        return self.mozi_server.send_and_recv(
            "Hs_DropSonobuoy('{}','{}','{}','{}')".format(side.strName, self.strGuid, deep_or_shallow,
                                                          passive_or_active))

    def set_weapon_reload_priority(self, wpnrec_guid, priority):
        """
        功能：设置武器重新装载优先级 # 接口暂不可用
        参数：wpnrec_guid {str: 武器记录guid}
            priority {str: 'true'-优先，'false'-不优先}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv(
            "Hs_ScenEdit_SetWeaponReloadPriority({guid='%s',WPNREC_GUID='%s',IsReloadPriority=%s})" % (
                self.strGuid, wpnrec_guid, priority))

    def add_weapon_to_unit_magazine(self, mag_guid, wpn_dbid, number):
        """
        功能：往弹药库内添加武器 # 接口暂不可用
        限制：专项赛禁用
        参数：mag_guid {str: 弹药库guid}
            wpn_dbid {int: 武器dbid}
            number {int: 武器数量}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv(
            "Hs_AddWeaponToUnitMagazine({side='%s',guid='%s',mag_guid='%s',wpn_dbid=%s,number=%s})" % (
                self.m_Side, self.strGuid, mag_guid, wpn_dbid, number))

    def switch_sensor(self, radar='false', sonar='false', oecm='false'):
        """
        功能：同时设置单元上多种类型传感器的开关状态。
        参数：radar {str: 'true'-开，'false'-关}   雷达
            sonar {str: 'true'-开，'false'-关}    声呐
            oecm {str: 'true'-开，'false'-关}     攻击性电子对抗手段
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        lua = "Hs_ScenEdit_SetUnitSensorSwitch({guid='%s', RADER=%s,SONAR=%s,OECM=%s})" % (
            self.strGuid, radar, sonar, oecm)
        return self.mozi_server.send_and_recv(lua)

    def wcsf_contact_types_unit(self, holdTightFreeInherited):
        """
        功能：控制指定单元对所有目标类型的攻击状态。
        参数：holdTightFreeInherited {str: 'Hold'-禁止，'Tight'-限制，'Free'-自由，'Inherited'-按上级条令执行}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        lua = "Hs_WCSFAContactTypesSUnit('%s','%s','%s')" % (self.m_Side, self.strGuid, holdTightFreeInherited)
        return self.mozi_server.send_and_recv(lua)

    def allocate_all_weapons_to_target(self, targetGuid, weaponDbid):
        """
        功能：为手动交战分配同类型所有武器。
        参数：targetGuid {str: 目标guid}
            weaponDbid {int: 武器dbid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        lua = "Hs_ScenEdit_AllocateAllWeaponsToTarget('%s',{TargetGUID='%s'},%s)" % (
            self.strGuid, targetGuid, weaponDbid)
        return self.mozi_server.send_and_recv(lua)

    def remove_salvo_target(self, weaponSalvoGuid):
        """
        功能：取消手动交战时齐射攻击目标。# 接口当前不可用
        参数：WeaponSalvoGUID {str: 武器齐射 GUID}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        lua = "Hs_ScenEdit_RemoveWeapons_Target('%s','%s')" % (self.strGuid, weaponSalvoGuid)
        return self.mozi_server.send_and_recv(lua)

    def set_salvo_timeout(self, b_is_salvo_timeout='false'):
        """
        功能：设置超时自动取消齐射
        参数：b_is_salvo_timeout {str: 'true'-是 'false'-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：解洋
        单位：北京华戍防务技术有限公司
        时间：2020-3-11
        """
        lua = "Hs_ScenEdit_SetSalvoTimeout(%s) " % b_is_salvo_timeout
        return self.mozi_server.send_and_recv(lua)

    def allocate_salvo_to_target(self, target, weaponDBID):
        """
        功能：单元手动分配一次齐射攻击(打击情报目标), 或者纯方位攻击(打击一个位置)
        参数：target {str: 情报目标guid
                    or tuple: (lat, lon) 例：(40.90,30.0)}
            weaponDBID {int: 武器型号数据库id}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-3-11
        """
        if type(target) == str:
            table = "{TargetGUID ='" + target + "'}"
        elif type(target) == tuple:
            table = "{TargetLatitude =" + str(target[0]) + ", TargetLongitude = " + str(target[1]) + "}"
        else:
            raise Exception("target 参数错误")
        lua_script = "Hs_ScenEdit_AllocateSalvoToTarget('{}',{},{})".format(self.strGuid, table, str(weaponDBID))
        return self.mozi_server.send_and_recv(lua_script)

    def allocate_weapon_auto_targeted(self, target_guids, weapon_dbid, num):
        """
        功能：为自动交战进行弹目匹配。此时自动交战意义在于不用指定对多个目标的攻击顺序。
        参数：target_guids {list: 目标guid列表}
            weapon_dbid {int: 武器型号数据库id}
            num {int: 武器发射数量} 对单个目标的数量
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：2020-3-11
        """
        targets = None
        for target_guid in target_guids:
            if targets:
                targets += ",'%s'" % target_guid
            else:
                targets = "'%s'" % target_guid
        lua = "Hs_AllocateWeaponAutoTargeteds('%s',{%s},%s,%s)" % (self.strGuid, targets, weapon_dbid, num)
        return self.mozi_server.send_and_recv(lua)

    def auto_target(self, contacts_guid_list):
        """
        功能：让单元自动进行弹目匹配并攻击目标。
        参数：contacts {str list: 目标guid列表}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修订：aie, 张志高
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        targets = None
        for target_guid in contacts_guid_list:
            if targets:
                targets += ",'%s'" % target_guid
            else:
                targets = "'%s'" % target_guid
        cmd = "Hs_AutoTargeted('%s',{%s})" % (self.strGuid, targets)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def self_update(self, options):
        result = self.mozi_server.send_and_recv(" ReturnObj(scenEdit_UpdateUnit({}))".format(options))
        activeUnit = CActiveUnit(self.strGuid, self.mozi_server, self.situation)
        if result[:4] == "unit":
            # 处理接收的数据
            result_split = result[6:-1].replace('\'', '')
            result_join = ""
            result_join = result_join.join([one for one in result_split.split('\n')])
            lst = result_join.split(',')
            for keyValue in lst:
                keyValue_list = keyValue.split('=')
                if len(keyValue_list) == 2:
                    attr = keyValue_list[0].strip()
                    value = keyValue_list[1].strip()
                    if attr == "name":
                        activeUnit.name = value
                    elif attr == "side":
                        activeUnit.side = value
                    elif attr == "type":
                        activeUnit.type = value
                    elif attr == "subtype":
                        activeUnit.subtype = value
                    elif attr == "guid":
                        activeUnit.guid = value
                    elif attr == "proficiency":
                        activeUnit.proficiency = value
                    elif attr == "latitude":
                        activeUnit.latitude = float(value)
                    elif attr == "longitude":
                        activeUnit.longitude = float(value)
                    elif attr == "altitude":
                        activeUnit.altitude = float(value)
                    elif attr == "heading":
                        activeUnit.heading = float(value)
                    elif attr == "speed":
                        activeUnit.speed = float(value)
                    elif attr == "throttle":
                        activeUnit.throttle = value
                    elif attr == "autodetectable":
                        activeUnit.autodetectable = bool(value)
                    elif attr == "mounts":
                        activeUnit.mounts = int(value)
                    elif attr == "magazines":
                        activeUnit.magazines = int(value)
                    elif attr == "unitstate":
                        activeUnit.unitstate = value
                    elif attr == "fuelstate":
                        activeUnit.fuelstate = value
                    elif attr == "weaponstate":
                        activeUnit.weaponstate = value
            code = "200"
        else:
            code = "500"
        return code, activeUnit

    def update_way_point(self, way_point_index, lat, lon):
        """
        功能：更新单元航路点的具体信息,必须首先有一个航路点
        参数：way_point_index {index: 航路点序号，从0开始，0表示第1个}
            lat {float: 纬度}
            lon {float: 经度}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修订：张志高 2021-8-3
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        return self.mozi_server.send_and_recv('Hs_UpdateWayPoint("%s",%s,{latitude="%s",longitude="%s"})'
                                              % (self.strGuid, way_point_index, lat, lon))

    def set_way_point_sensor(self, wayPointIndex, sensor, sensorStatus):
        """
        功能：设置航路点传感器的开关状态
        参数：wayPointIndex:{int:航路点序号，从0开始}
            sensor:{str: 'CB_Sonar'-声呐，'CB_radar'-雷达，'CB_ECM'-干扰机}
            sensorStatus: {str: 'Unchecked'-未开机，'Checked'-开机，'Indeterminate'-未配置}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        lua_script = "Hs_UpdateWayPointSensorStatus('{}',{},'{}','{}')".format(self.strGuid, wayPointIndex, sensor,
                                                                               sensorStatus)
        return self.mozi_server.send_and_recv(lua_script)

    def set_desired_height(self, desired_height, moveto='true'):
        """
        功能：设置单元的期望高度
        限制：专项赛限制使用，禁止设置moveto='false'
        参数：desired_height {int or float, 期望高度值, 海拔高度：m}
            moveto {str, 'true'-是，瞬间到达该高度, 'false'-否，不瞬间到达该高度}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        if isinstance(desired_height, int) or isinstance(desired_height, float):
            lua_script = "ScenEdit_SetUnit({guid='" + str(self.strGuid) + "', Altitude=" + str(
                desired_height) + ", moveto='" + moveto + "'}) "
            return self.mozi_server.send_and_recv(lua_script)
        else:
            pass

    def unit_auto_detectable(self, isAutoDetectable):
        """
        功能： 单元自动探测到
        限制：专项赛禁用
        参数：isAutoDetectable:{str:'true'-自动探测到，'false'-不自动探测到}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        lua_script = "ScenEdit_SetUnit({guid='%s',autodetectable=%s})" % (self.strGuid, isAutoDetectable)
        return self.mozi_server.send_and_recv(lua_script)

    def set_fuel_qty(self, remainingFuel):
        """
        功能：设置单元燃油量
        限制：专项赛禁用
        类别：编辑所用函数
        参数：remainingFuel {float - 剩余燃油的公斤数}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        return self.mozi_server.send_and_recv("Hs_SetFuelQty('{}','{}')".format(self.strGuid, remainingFuel))

    def set_own_side(self, new_side):
        """
        功能：改变单元所属阵营
        限制：专项赛禁用
        参数：new_side {str: 新的方名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        side = self.situation.side_dic[self.m_Side]
        return self.mozi_server.send_and_recv(
            "ScenEdit_SetUnitSide({side='%s',name='%s',newside='%s'})" % (side.strName, self.strName, new_side))

    def set_loadout(self, loadout_id, time_to_ready_minutes, ignore_magazines, exclude_optional_weapons):
        """
        功能：设置挂载方案
        限制：专项赛禁用
        参数：loadout_id {str: 挂载方案ID, 0表示使用当前挂载方案}
            time_to_ready_minutes {int: 载荷准备时间（分钟）}
            ignore_magazines {str: 'true'-忽略弹药库，'false'-不忽略弹药库}
            exclude_optional_weapons {str: 'true'-不包含可选武器，'false'-包含可选武器}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv(
            "ScenEdit_SetLoadout ({UnitName='%s',LoadoutID='%s',TimeToReady_Minutes='%s',IgnoreMagazines=%s,"
            "ExcludeOptionalWeapons=%s})" % (
                self.strName, loadout_id, time_to_ready_minutes, ignore_magazines, exclude_optional_weapons))

    def reload_weapon(self, wpn_dbguid, number, fillout='false'):
        """
        功能：让指定单元重新装载武器
        限制：专项赛禁用
        参数：wpn_dbguid {int: 武器数据库guid}
            number {int: 要添加的数量}
            fillout {str: 'true'-装满，'false'-不装满}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv(
            "ScenEdit_AddReloadsToUnit({guid='%s', wpn_dbguid='%s', number=%s, fillout=%s})" % (
                self.strGuid, wpn_dbguid, number, fillout))

    def load_cargo(self, cargo_dbid):
        """
        功能：添加货物
        限制：专项赛禁用
        参数：cargo_dbid {int: 货物DBID}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv("Hs_AddCargoToUnit('{}',{})".format(self.strGuid, cargo_dbid))

    def remove_cargo(self, cargo_dbid):
        """
        功能：删除货物
        限制：专项赛禁用
        参数：cargo_dbid {int: 货物DBID}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv("Hs_RemoveCargoToUnit('{}',{})".format(self.strGuid, cargo_dbid))

    def set_magazine_weapon_current_load(self, wpnrec_guid, current_load):
        """
        功能：设置弹药库武器数量
        限制：专项赛禁用
        参数：wpnrec_guid {str: 武器记录guid}
            current_load {int: 当前武器装载数量}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv(
            "Hs_ScenEdit_SetMagazineWeaponCurrentLoad({guid='%s',WPNREC_GUID='%s',currentLoad=%s})" % (
                self.strGuid, wpnrec_guid, current_load))

    def remove_magazine(self, magazine_guid):
        """
        功能：删除弹药库
        限制：专项赛禁用
        参数：magazine_guid {str: 弹药库guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv(
            "Hs_ScenEdit_RemoveMagazine({guid='%s', magazine_guid='%s'})" % (self.strGuid, magazine_guid))

    def set_magazine_state(self, magazine_guid, state):
        """
        功能：设置弹药库状态
        限制：专项赛禁用
        参数：magazine_guid {str: 弹药库guid}
            state {str: '正常运转'，'轻度毁伤'，'中度毁伤'，'重度毁伤' or '摧毁'}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv(
            "Hs_ScenEdit_SetMagazineState({guid='%s', magazine_guid='%s',state='%s'})" % (
                self.strGuid, magazine_guid, state))

    def set_weapon_current_load(self, wpn_rec_guid, number):
        """
        功能：设置挂架武器数量
        限制：专项赛禁用
        参数：wpn_rec_guid {str: 武器guid}
            number {int: 数量}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/8/20
        """
        return self.mozi_server.send_and_recv(
            "Hs_ScenEdit_SetWeaponCurrentLoad({guid='%s',WPNREC_GUID='%s',CURRENTLOAD=%s})"
            % (self.strGuid, wpn_rec_guid, number))

    def add_to_host(self, base_guid):
        """
        功能：将单元部署进基地
        限制：专项赛禁用
        参数：base_guid {str: 基地的guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        return self.mozi_server.send_and_recv("ScenEdit_HostUnitToParent({{HostedUnitNameOrID='{}',"
                                              "SelectedHostNameOrID='{}'}})".format(self.strGuid, base_guid))

    def add_mount(self, mount_dbid, heading_code_dict):
        """
        功能：为单元添加武器挂架
        限制：专项赛禁用
        参数：mount_dbid {int: 挂架dbid}
            heading_code_dict {dict: key(str)'-枚举值，
                                        'PS1'-左弦尾1
                                        'PMA1'-左弦中后1
                                        'PMF1'-左弦中前1
                                        'PB1'-左弦首1
                                        'SS1'-右弦尾1
                                        'SMA1'-右弦中后1
                                        'SMF1'-右弦中前1
                                        'SB1'-右弦首1
                                        'PS2'-左弦尾2
                                        'PMA2'-左弦中后2
                                        'PMF2'-左弦中前2
                                        'PB2'-左弦首2
                                        'SS2'-右弦尾2
                                        'SMA2'-右弦中后2
                                        'SMF2'-右弦中前2
                                        'SB2'-右弦首2
                                        '360'-全覆盖
                                    value(str): 'true' or 'false'}
            example: {'PS1':'true', 'PB1':'true'}
            不设置时，默认为false
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修订：张志高2021-7-23
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        heading_code = ''
        for key, value in heading_code_dict.items():
            if heading_code:
                heading_code += f',{key}={value}'
            else:
                heading_code = f'{key}={value}'
        lua_script = f"Hs_ScenEdit_AddMount({{unitname='{self.strName}',mount_dbid={mount_dbid},{heading_code}}})"
        self.mozi_server.send_and_recv(lua_script)

    def remove_mount(self, mount_guid):
        """
        功能：删除单元中指定的武器挂架
        限制：专项赛禁用
        参数：mount_guid {str: 武器挂架的GUID}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修订：张志高 2021-7-23
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        return self.mozi_server.send_and_recv(
            "Hs_ScenEdit_RemoveMount({unitname='%s',mount_guid='%s'})" % (self.strName, mount_guid))

    def add_weapon(self, wpn_dbid, MOUNT_GUID):
        """
        功能：给单元挂架中添加武器
        限制：专项赛禁用
        参数：wpn_dbid {int: 武器DBID}
            MOUNT_GUID {str: 挂架guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修订：张志高 2021-7-23
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        return self.mozi_server.send_and_recv(
            "Hs_ScenEdit_AddWeapon({guid='%s',wpn_dbid=%s,MOUNT_GUID = '%s',IsTenThousand=true})" % (
                self.strGuid, wpn_dbid, MOUNT_GUID))

    def remove_weapon(self, wpn_rec_guid):
        """
        功能：通过武器属性删除单元的武器
        限制：专项赛禁用
        参数：wpn_rec_guid {str: 武器记录guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：2020-3-9
        """
        return self.mozi_server.send_and_recv(
            "Hs_ScenEdit_RemoveWeapon({unitname='%s', WPNREC_GUID='%s'})" % (self.strName, wpn_rec_guid))

    def set_unit_damage(self, overalldamage, comp_guid, level):
        """
        功能：设置单元总体毁伤和单元各组件的毁伤值
        限制：专项赛禁用
        函数类别：编辑函数
        参数：overalldamage:{float: 总体毁伤值%}
            comp_guid:{str: 组件guid}
            level: {int: 0-正常工作，1-轻度毁伤，2-中度毁伤,3-重度毁伤,4-被摧毁}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修订：张志高 2021-7-23
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        lua_script = f"HS_SetUnitDamage({{guid='{self.strGuid}',OVERALLDEMAGE={overalldamage}," \
                     f"components={{'{comp_guid}','{level}'}}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def set_magazine_weapon_number(self, mag_guid, wpn_db_guid, number):
        """
        功能：往单元的弹药库中添加指定数量的武器
        限制：专项赛禁用
        函数类别：编辑函数
        参数：mag_guid: {str: 弹药库guid}
            wpn_db_guid: {str: 武器数据库guid}
            number: {int: 武器数量}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：赵俊义
        修订：张志高 2021-8-4
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        return self.mozi_server.send_and_recv(
            "ScenEdit_AddWeaponToUnitMagazine({{guid='{}',mag_guid='{}',wpn_dbguid='{}',number={}}})".format(
                self.strGuid,
                mag_guid, wpn_db_guid,
                number))

    def set_proficiency(self, proficiency):
        """
        功能：设置单元训练水平
        限制：专项赛禁用
        参数：proficiency {str: Novice-新手，Cadet-初级，Regular-普通，Veteran-老手，Ace-顶级}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-9
        """
        side = self.situation.side_dic[self.m_Side]
        lua_script = f"ScenEdit_SetSideOptions({{side='{side.strName}', guid='{self.strGuid}', " \
                     f"proficiency='{proficiency}'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def rename(self, new_name):
        """
        功能：重命名
        参数：new_name {str: 活动单元新名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-10-22
        """
        return self.mozi_server.send_and_recv(
            "ScenEdit_SetUnit({guid='%s',Newname='%s'})" % (self.strGuid, new_name))

    def set_longitude_latitude(self, lon, lat):
        """
        功能：移动单元，设置单元的经纬度
        参数：lon {float: 单元经度}
            lat {float: 单元纬度}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-12-1
        """
        lua_script = f"ScenEdit_SetUnit({{side='{self.m_Side}', guid='{self.strGuid}', latitude='{lat}', " \
                     f"longitude='{lon}'}})"
        return self.mozi_server.send_and_recv(lua_script)


    def set_waypoint(self, longitude, latitude):
        """
        功能：设置单元下一个航路点
        参数：
            longitude {float - 经度}
            latitude {float - 纬度}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：3/28/22
        """
        lua_str = "ScenEdit_SetUnit({side= '%s', guid='%s', course={ { Description = ' ', TypeOf = " \
                  "'ManualPlottedCourseWaypoint', longitude = %s, latitude = %s } } })" % (
                      self.m_Side, self.strGuid, longitude, latitude)
        return self.mozi_server.send_and_recv(lua_str)
