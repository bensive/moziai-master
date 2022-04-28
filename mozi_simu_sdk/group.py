# -*- coding:utf-8 -*-
##########################################################################################################
# File name : group.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################

from .activeunit import CActiveUnit


class CGroup(CActiveUnit):
    """
    编组类
    """

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 悬停
        self.fHoverSpeed = 0.0
        # 低速
        self.fLowSpeed = 0.0
        # 巡航
        self.fCruiseSpeed = 0.0
        # 军力
        self.fMilitarySpeed = 0.0
        # 加速
        self.fAddForceSpeed = 0.0
        # 是否在作战中
        self.bIsOperating = False
        # 停靠的单元GUID集合
        self.m_DockedUnits = ''
        # 实体的停靠设施(部件)
        # 集合
        self.m_DockFacilitiesComponent = ''
        # 停靠的飞机的GUID集合
        self.m_DockAircrafts = ''
        # 实体的航空设施(部件)
        # 集合
        self.m_AirFacilitiesComponent = ''
        # 实体的通信设备及数据链（部件）
        self.m_CommDevices = ''
        # 单元搭载武器
        self.m_UnitWeapons = ''
        # 状态
        self.strActiveUnitStatus = ''
        # 训练水平
        self.m_ProficiencyLevel = ''
        # 是否是护卫角色
        self.bIsEscortRole = False
        # 当前油门
        self.m_CurrentThrottle = ''
        # 通讯设备是否断开
        self.bIsCommsOnLine = False
        # 是否视图隔离
        self.bIsIsolatedPOVObject = False
        # 是否地形跟随
        self.bTerrainFollowing = False
        # 是否是领队
        self.bIsRegroupNeeded = False
        # 是否保持阵位
        self.bHoldPosition = False
        # 是否可自动探测
        self.bAutoDetectable = False
        # 燃油百分比，作战单元燃油栏第一个进度条的值
        self.dFuelPercentage = False
        # 单元的通讯链集合
        self.m_CommLink = ''
        # 传感器GUID集合
        self.m_NoneMCMSensors = ''
        # 显示“干扰”或“被干扰”
        self.iDisturbState = 0
        # 单元所属多个任务数量
        self.iMultipleMissionCount = 0
        # 单元所属多个任务guid集合
        self.m_MultipleMissionGUIDs = ''
        # 弹药库GUID集合
        self.m_Magazines = ''
        # 编组类型
        self.m_GroupType = ''
        # 编组中心点
        self.m_GroupCenter = ''
        # 编组领队
        self.m_GroupLead = ''
        # 编组所有单元
        self.m_UnitsInGroup = ''
        # 航路点名称
        self.strWayPointName = ''
        # 航路点描述
        self.strWayPointDescription = ''
        # 航路点剩余航行距离
        self.WayPointDTG = ''
        # 航路点剩余航行时间
        self.WayPointTTG = ''
        # 航路点需要燃油数
        self.WayPointFuel = ''
        # 发送队形方案选择的索引
        self.iFormationSelectedIndex = ''
        # 发送队形方案详情
        self.m_FormationFormula = ''
        # 载机按钮的文本描述
        self.strDockAircraft = ''
        # 载艇按钮的文本描述
        self.strDockShip = ''

    def get_units(self):
        """
        功能：获取编组下单元
        参数：无
        返回：dict - 格式 {unit_guid1:unit_obj_1, unit_guid2:unit_obj_2, ...}
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        units_guid = self.m_UnitsInGroup.split('@')
        units_group = {}
        for guid in units_guid:
            units_group[guid] = self.situation.get_obj_by_guid(guid)
        return units_group

    def get_doctrine(self):
        """
        功能：获取条令
        参数：无
        返回：CDoctrine对象
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        if self.m_Doctrine in self.situation.doctrine_dic:
            doctrine = self.situation.doctrine_dic[self.m_Doctrine]
            doctrine.category = 'Group'  # 需求来源：20200331-2/2:Xy
            return doctrine
        return None

    def add_unit(self, unit_guid):
        """
        功能：编队添加一个单元
        参数：unit_guid {str: 单元guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        lua_script = "ScenEdit_SetUnit({group='%s',guid='%s'})" % (self.strGuid, unit_guid)
        return self.mozi_server.send_and_recv(lua_script)

    def remove_unit(self, unit_guid):
        """
        功能：将单元移除编组
        类别：推演所用函数
        参数：unit_guid {str: 单元guid}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        return self.mozi_server.send_and_recv("Hs_RemoveUnitFromGroup('{}')".format(unit_guid))

    def set_formation_group_lead(self, unit_name):
        """
        功能：设置编队领队
        类别：推演所用函数
        参数：unit_name {str: 所设领队的单元名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-17
        """
        lua_script = f"ScenEdit_SetFormation({{NAME='{unit_name}',SETTOGROUPLEAD='Yes'}})"
        return self.mozi_server.send_and_recv(lua_script)

    def set_formation_group_member(self, unit_name, area_type, bearing, distance):
        """
        功能：设置编队队形
        类别：推演所用函数
        参数：
            unit_name {str: 单元名称}
            area_type 与领队的空间相对关系的维持模式 {str: 'FIXED'-维持平动，'Rotating'-同步转动}
            bearing {int: 与领队的相对方位}
            distance {int: 与领队的距离} 单位海里
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-17
        """
        lua_script = f"ScenEdit_SetFormation({{NAME='{unit_name}', TYPE='{area_type}', BEARING={bearing}, " \
                     f"DISTANCE={distance}}})"
        return self.mozi_server.send_and_recv(lua_script)

    def set_unit_sprint_and_drift(self, unit, true_or_false):
        """
        功能：控制编队内非领队单元相对于编队是否进行高低速交替航行。
        类别：推演所用函数
        参数：
            unit {str: 单元guid}   设置单元名称不起作用
            true_or_false 是否交替航行的状态标识符 {str: 'true'-是，'false'-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：2020-8-17
        """
        return self.mozi_server.send_and_recv("Hs_SetUnitSprintAndDrift('{}',{})".format(unit, true_or_false))
