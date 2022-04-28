# -*- coding:utf-8 -*-
##########################################################################################################
# File name : contact.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################


class CContact:
    contact_type = {
        # 空中目标
        0: "Air",
        # 导弹
        1: "Missile",
        # 水面 / 地面
        2: "Surface",
        # 潜艇
        3: "Submarine",
        # 未确定的海军
        4: "UndeterminedNaval",
        # 瞄准点？？
        5: "Aimpoint",
        # 轨道目标
        6: "Orbital",
        # 固定设施
        7: "Facility_Fixed",
        # 移动设施
        8: "Facility_Mobile",
        # 鱼雷
        9: "Torpedo",
        # 水雷
        10: "Mine",
        # 爆炸
        11: "Explosion",
        # 不确定
        12: "Undetermined",
        # 空中诱饵
        13: "Decoy_Air",
        # 表面诱饵
        14: "Decoy_Surface",
        # 陆地诱饵
        15: "Decoy_Land",
        # 水下诱饵
        16: "Decoy_Sub",
        # 声纳浮标
        17: "Sonobuoy",
        # 军事设施
        18: "Installation",
        # 空军基地
        19: "AirBase",
        # 海军基地
        20: "NavalBase",
        # 移动集群
        21: "MobileGroup",
        # 激活点：瞄准点
        22: "ActivationPoint",
    }

    def __init__(self, strGuid, mozi_server, situation):
        # GUID
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 态势
        self.situation = situation
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
        # 实体类别
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
        # 是否在陆地上
        self.bIsOnLand = False
        # 可能匹配结果
        self.m_MatchingDBIDList = ""
        # 识别出的辐射平台
        self.strRadiantPoint = ""
        self.strIconType = ""
        self.strCommonIcon = ""
        # 目标类型
        self.m_ContactType = 0
        # 属方是否已知
        self.bSideIsKnown = False
        # 单元的识别状态
        # 0--未知
        # 1--已知空域（如空中、地面）
        # 2--已知类型（如飞机、导弹）
        # 3--已知级别
        # 4--确认对象
        self.m_IdentificationStatus = 0
        # 本身单元的GUID
        self.m_ActualUnit = ""
        # 探测到的推演方
        self.m_OriginalDetectorSide = ""
        # 其它推演方对本目标的立场姿态
        self.m_SidePostureStanceDictionary = ""
        # 速度是否已知
        self.bSpeedKnown = False
        # 朝向是否已知
        self.bHeadingKnown = False
        # 高度是否已知
        self.bAltitudeKnown = False
        # 电磁辐射Title
        self.strElectromagnetismEradiateTitle = ""
        # 电磁辐射集合
        self.strElectromagnetismEradiate = ""
        # 匹配结果标题
        self.strMatchingTitle = ""
        # 侦察记录
        self.m_DetectionRecord = ""
        # 不确定区域集合
        self.m_UncertaintyArea = ""
        # 目标持续时间
        self.strAge = ""
        # 取目标发射源容器中传感器的最大探测距离
        self.fMaxDetectRange = 0.0
        # 获取最大对海探测范围
        self.fMaxRange_DetectSurfaceAndFacility = 0.0
        # 获取最大对潜探测范围
        self.fMaxRange_DetectSubsurface = 0.0
        # 获取目标探测时间
        self.fTimeSinceDetection_Visual = 0.0
        # 获取瞄准目标的武器数量
        self.iWeaponsAimingAtMe = 0
        # 目标武器对空最大攻击距离
        self.fAirRangeMax = 0.0
        # 目标武器对海最大攻击距离
        self.fSurfaceRangeMax = 0.0
        # 目标武器对陆最大攻击距离
        self.fLandRangeMax = 0.0
        # 目标武器对潜最大攻击距离
        self.fSubsurfaceRangeMax = 0.0
        # 态势控制——目标电磁辐射显示信息
        self.strContactEmissions = ""
        self.m_OriginalDetectorSide = ''

    def get_type_description(self):
        """
        功能：获取探测目标的类型描述
        参数：无
        返回：str  以self.m_ContactType为key获取的self.contact_type中的值
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        return self.contact_type[self.m_ContactType]

    def get_contact_info(self):
        """
        功能：获取目标信息字典
        参数：无
        返回：dict
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        info_dict = {
            'type': self.get_type_description(),
            'typed': self.m_ContactType,
            'classificationlevel': self.m_IdentificationStatus,
            'name': self.strName,
            'guid': self.m_ActualUnit,
            'latitude': self.dLatitude,
            'longitude': self.dLongitude,
            'altitude': self.fCurrentAltitude_ASL,
            'heading': self.fCurrentHeading,
            'speed': self.fCurrentSpeed,
            'firingAt': [],
            'missile_defence': 0,
            'fromUnits': self.m_DetectionRecord,
            'fg': self.strGuid,
        }
        return info_dict

    def get_original_detector_side(self):
        """
        功能：获取探测到单元的方
        参数：无
        返回：推演方对象
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        return self.situation.side_dic[self.m_OriginalDetectorSide]

    def set_mark_contact(self, contact_type):
        """
        功能：标识目标立场
        参数：contact_type {str: 'F'-友方，'N'-中立，'U'-非友方，'H'-敌方}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        lua_script = "Hs_SetMarkContact('%s','%s','%s')" % (self.m_OriginalDetectorSide, self.strGuid, contact_type)
        self.mozi_server.send_and_recv(lua_script)

    def hs_contact_rename(self, new_name):
        """
        功能：重命名目标
        参数：new_name {str: 新的目标名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        lua_script = "Hs_ContactRename('%s','%s','%s')" % (self.m_OriginalDetectorSide, self.strGuid, new_name)
        self.mozi_server.send_and_recv(lua_script)

    def hs_contact_drop_target(self):
        """
        功能：放弃目标，不再将所选目标列为探测对象。
        参数：new_name {str: 新的目标名称}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        lua_script = "Hs_ContactDropTarget('%s','%s')" % (self.m_OriginalDetectorSide, self.strGuid)
        self.mozi_server.send_and_recv(lua_script)

    def get_actual_unit(self):
        """
        功能：获取目标真实单元
        限制：专项赛禁用
        参数：无
        返回：活动单元对象
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        return self.situation.get_obj_by_guid(self.m_ActualUnit)

    def get_original_target_side(self):
        """
        功能：获取目标单元所在方
        限制：专项赛禁用
        参数：无
        返回：推演方对象
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        return self.situation.side_dic[self.m_Side]
