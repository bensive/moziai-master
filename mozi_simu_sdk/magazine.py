# -*- coding:utf-8 -*-
##########################################################################################################
# File name : magazine.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################


class CMagazine:
    """弹药库"""

    def __init__(self, strGuid, mozi_server, situation):
        # GUID
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 态势
        self.situation = situation
        # 弹药库名称
        self.strName = ''
        # 父平台guid
        self.m_ParentPlatform = ''
        # 状态
        self.m_ComponentStatus = 0
        # 毁伤程度的轻,中,重
        self.m_DamageSeverity = 0
        # 覆盖角度
        self.m_CoverageArc = ""
        # 挂架已挂载的数量和挂架载荷
        self.m_LoadRatio = ""
        self.select = False  # 选择是否查找所属单元

    def set_magazine_state(self, state):
        """
        功能：设置弹药库状态
        限制：专项赛禁用
        参数：state {str: '正常运转'，'轻度毁伤'，'中度毁伤'，'重度毁伤' 或 '摧毁'}
        返回：'lua执行成功'或'脚本执行出错'
        作者：-
        修订：张志高 2021-8-26
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        return self.mozi_server.send_and_recv(
          "Hs_ScenEdit_SetMagazineState({guid='%s', magazine_guid='%s',state='%s'})" % (self.m_ParentPlatform,
                                                                                        self.strGuid, state))

    def remove_weapon(self, weapon_guid):
        """
        功能：删除单元中指定弹药库下的指定武器
        限制：专项赛禁用
        参数：weapon_guid {str: 武器guid}  可通过m_LoadRatio
        返回：'lua执行成功'或'脚本执行出错'
        作者：-
        修订：张志高 2021-8-26
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        return self.mozi_server.send_and_recv(
            "Hs_ScenEdit_RemoveMagazineWeapon({GUID='%s',WPNREC_GUID='%s'})" % (self.m_ParentPlatform, weapon_guid))

