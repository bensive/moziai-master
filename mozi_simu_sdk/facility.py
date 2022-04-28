# -*- coding:utf-8 -*-
##########################################################################################################
# File name : facility.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################

from mozi_simu_sdk.activeunit import CActiveUnit


class CFacility(CActiveUnit):
    """地面设施"""

    def __init__(self, strGuid, mozi_server, situation):
        super().__init__(strGuid, mozi_server, situation)
        # 方位类型
        self.m_BearingType = 0
        # 方位
        self.m_Bearing = 0.0
        # 距离（千米）
        self.m_Distance = 0.0
        # 是否高速交替航行
        self.bSprintAndDrift = False
        # 载机按钮的文本描述
        self.strDockAircraft = ""
        # 类别
        self.m_Category = 0
        # 悬停
        self.fHoverSpeed = 0.0
        # 低速
        self.fLowSpeed = 0.0
        # 巡航
        self.fCruiseSpeed = 0.0
        # 军力
        self.fMilitarySpeed = 0.0
        # 载艇按钮的文本描述
        self.strDockShip = ""
        self.m_CommandPost = ""
        # 加油队列明细
        self.m_ShowTanker = ""
        self.ClassName = 'CFacility'

    def get_summary_info(self):
        """
        获取精简信息, 提炼信息进行决策
        :return: dict
        """
        info_dict = {
            "guid": self.strGuid,
            "DBID": self.iDBID,
            "subtype": str(self.m_Category),
            "facilityTypeID": "",
            "name": self.strName,
            "side": self.m_Side,
            "proficiency": self.m_ProficiencyLevel,
            "latitude": self.dLatitude,
            "longitude": self.dLongitude,
            "altitude": self.fAltitude_AGL,
            "altitude_asl": self.iAltitude_ASL,
            "course": self.get_way_points_info(),
            "heading": self.fCurrentHeading,
            "speed": self.fCurrentSpeed,
            "throttle": self.m_CurrentThrottle,
            "autodetectable": self.bAutoDetectable,
            "unitstate": self.strActiveUnitStatus,
            "fuelstate": "",
            "weaponstate": -1,
            "mounts": self.get_mounts(),
            "type": "Facility",
            "fuel": 0,
            "damage": self.strDamageState,
            "sensors": self.get_sensor(),
            "weaponsValid": self.get_weapon_infos()
        }
        return info_dict

