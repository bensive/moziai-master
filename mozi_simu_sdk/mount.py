# -*- coding:utf-8 -*-
##########################################################################################################
# File name : mount.py
# Create date : 2020-3-18
# Modified date : 2020-3-18
# Author : xy
# Describe : not set
# All rights reserved:北京华戍防务技术有限公司
# Email : yang_31296@163.com
##########################################################################################################


class CMount:
    """挂架"""

    def __init__(self, strGuid, mozi_server, situation):
        # GUID
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 态势
        self.situation = situation
        # 名称
        self.strName = ''
        # 所属单元GUID
        self.m_ParentPlatform = ''
        # 部件状态
        self.m_ComponentStatus = 0
        # 毁伤程度的轻,中,重
        self.m_DamageSeverity = 0
        # 挂载方位
        self.m_CoverageArc = ""
        # 挂载的武器开火状态
        self.strWeaponFireState = ""
        # 挂载的武器的数量
        self.strLoadWeaponCount = ""
        # 获取挂架下武器的最大载弹量和当前载弹量集合
        self.m_LoadRatio = ""
        # 传感器的guid
        self.m_Sensors = ""
        # 重新装载优先级选中的武器DBID集合
        self.m_ReloadPrioritySet = ""
        # 左弦尾1
        self.PS1 = False
        # 左弦中后1
        self.PMA1 = False
        # 左弦中前
        self.PMF1 = False
        # 左弦首1
        self.PB1 = False
        # 右弦尾1
        self.SS1 = False
        # 右弦中后1
        self.SMA1 = False
        # 右弦中前1
        self.SMF1 = False
        # 右弦首1-bow
        self.SB1 = False
        # 左弦尾2-stern
        self.PS2 = False
        # 左弦中后2
        self.PMA2 = False
        # 左弦中前2
        self.PMF2 = False
        # 左弦首2
        self.PB2 = False
        # 右弦尾2
        self.SS2 = False
        # 右弦中后2
        self.SMA2 = False
        # 右弦中前2
        self.SMF2 = False
        # 右弦首2
        self.SB2 = False
        # 是否查找挂实体
        self.select = False

