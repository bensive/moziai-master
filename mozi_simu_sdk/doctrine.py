# -*- coding:utf-8 -*-
##########################################################################################################
# File name : doctrine.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
#########################################################################################################


class CDoctrine:
    """
    条令类
    """

    def __init__(self, strGuid, mozi_server, situation):
        # GUID
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 态势
        self.situation = situation
        # 条令属主类型
        self.category = None
        self.mozi_server = mozi_server
        # 条令的拥有者GUID（具体作用对象）
        self.m_DoctrineOwner = ""
        # 核武器使用规则
        self.m_Nukes = 0
        # 对空目标武器控制规则
        self.m_WCS_Air = 0
        # 对海目标武器控制规则
        self.m_WCS_Surface = 0
        # 对潜目标武器控制规则
        self.m_WCS_Submarine = 0
        # 对地目标武器控制规则
        self.m_WCS_Land = 0
        # 进攻时是否忽略绘制航线规则
        self.m_IgnorePlottedCourseWhenAttacking = 0
        # 对不明目标的行为态度规则
        self.m_BehaviorTowardsAmbigousTarget = 0
        # 对临机目标进行射击规则
        self.m_ShootTourists = 0
        # 受攻击时是否考虑电磁管控规则
        self.m_IgnoreEMCONUnderAttack = 0
        # 鱼雷使用动力航程规则
        self.m_UseTorpedoesKinematicRange = 0
        # 是否自动规避目标规则
        self.m_AutomaticEvasion = 0
        # 是否可加油/补给规则
        self.m_UseRefuel = 0
        # 对所选单元加油/补给时加油机选择规则
        self.m_RefuelSelection = 0
        # 与盟军单元加油/补给规则
        self.m_RefuelAllies = 0
        # 空战节奏规则
        self.m_AirOpsTempo = 0
        # 快速出动规则
        self.m_QuickTurnAround = 0
        # 预先规划终止任务返回基地油量阈值规则
        self.m_BingoJoker = 0
        # 编组成员达到预先规划油量状态时编组或成员返回基地规则
        self.m_BingoJokerRTB = 0
        # 预先规划武器使用规则、武器状态与平台脱离战斗规则
        self.m_WeaponState = 0
        # 编组成员达到预先规划武器状态时，编组或成员返回基地规则
        self.m_WeaponStateRTB = 0
        # 航炮是否对地面目标扫射规则
        self.m_GunStrafeGroundTargets = 0
        # 受到攻击时是否抛弃弹药规则
        self.m_JettisonOrdnance = 0
        # 以反舰模式使用舰空导弹规则
        self.m_SAM_ASUW = 0
        # 与目标保持一定距离规则
        self.m_MaintainStandoff = 0
        # 尽可能规避目标规则
        self.m_AvoidContact = 0
        # 探测到威胁目标后下潜规则
        self.m_DiveWhenThreatsDetected = 0
        # 巡逻任务充电时电池剩余电量规则
        self.m_RechargePercentagePatrol = 0
        # 进攻战充电时电池剩余电量规则
        self.m_RechargePercentageAttack = 0
        # AIP推进技术使用规则
        self.m_AIPUsage = 0
        # 吊放声呐使用规则
        self.m_DippingSonar = 0
        # 毁伤达到阈值时应撤退规则
        self.m_WithdrawDamageThreshold = 0
        # 油量达到阈值时应撤退规则
        self.m_WithdrawFuelThreshold = 0
        # 进攻战武器数量达到阈值应撤退规则
        self.m_WithdrawAttackThreshold = 0
        # 防御战武器数量达到阈值应撤退规则
        self.m_WithdrawDefenceThreshold = 0
        # 毁伤达到阈值时应重新部署规则
        self.m_RedeployDamageThreshold = 0
        # 油量达到阈值时应重新部署规则
        self.m_RedeployFuelThreshold = 0
        # 进攻战武器数量达到阈值时应重新部署规则
        self.m_RedeployAttackDamageThreshold = 0
        # 防御战武器数量达到阈值时应重新部署规则
        self.m_RedeployDefenceDamageThreshold = 0
        # 电磁管控设置是否有值
        self.m_bEMCON_AccordingSuperior = False
        # 雷达管控规则设置模式
        self.m_EMCON_SettingsForRadar = 0
        # 声呐管控规则设置模式
        self.m_EMCON_SettingsForSonar = 0
        # 进攻型电子对抗措施（干扰机）管控规则设置模式
        self.m_EMCON_SettingsForOECM = 0
        # 武器使用规则的武器DBID
        self.m_WRA_WeaponRule_WeaponDBID = ""
        # 武器使用规则
        self.m_WRA_WeaponRule = ""
        # 使用核武器是否允许用户编辑
        self.bchkUseNuclerWeapon = False
        # 武器控制状态对空是否允许用户编辑
        self.bchkWeaponStateAir = False
        # 武器控制状态对海是否允许用户编辑
        self.bchkWeaponStateSea = False
        # 武器控制状态对潜是否允许用户编辑
        self.bchkWeaponStateSeaLatent = False
        # 武器控制状态对地是否允许用户编辑
        self.bchkWeaponStateland = False
        # 受到攻击时忽略计划航线是否允许用户编辑
        self.bchkIgnoreRoutes = False
        # 接战模糊位置目标是否允许用户编辑
        self.bchkFuzzlocationOfTheReceIvingstation = False
        # 接战临机出现目标是否允许用户编辑
        self.bchkImminentTarget = False
        # 受攻击时忽略电磁管控是否允许用户编辑
        self.bchkIgnoreElectromagneticControl = False
        # 鱼雷使用动力航程是否允许用户编辑
        self.bchkTopedopower = False
        # 自动规避是否允许用户编辑
        self.bchkAutoAcoid = False
        # 加油/补给是否允许用户编辑
        self.bchkComeOn = False
        # 对所选单元进行加油/补给是否允许用户编辑
        self.bchkSelectUnitComeOn = False
        # 对盟军单元进行加油/补给是否允许用户编辑
        self.bchkAlliedUnitComeOn = False
        # 空战节奏是否允许用户编辑
        self.bchkAirOpsTempo_Player = False
        # 快速出动是否允许用户编辑
        self.bchkQTA_Player = False
        # 燃油状态，预先规划是否允许用户编辑
        self.bchkBingoJoker_Player = False
        # 燃油状态—返航是否允许用户编辑
        self.bchkBingoJokerRTB_Player = False
        # 武器状态, 预先规划是否允许用户编辑
        self.bchkWeaponStateFirast = False
        # 武器状态-返航是否允许用户编辑
        self.bchkWeaponStateReturn = False
        # 空对地扫射(航炮)是否允许用户编辑
        self.bchkAirToGroundUserEdit = False
        # 抛弃弹药是否允许用户编辑
        self.bchkAbandonedAmmunition = False
        # 以反舰模式使用舰空导弹规则是否允许用户编辑
        self.bchkSAM_ASUW_Player = False
        # 与目标保持一定距离规则是否允许用户编辑
        self.bchkKeepTargetDistance = False
        # 规避搜索规则是否允许用户编辑
        self.bchkToAvoidTheSearch = False
        # 探测到威胁进行下潜规则是否允许用户编辑
        self.bchkThreatWasDetectedAndDived = False
        # 电池充电 %, 出航/阵位是否允许用户编辑
        self.bchkSetSail = False
        # 电池充电%, 进攻/防御是否允许用户编辑
        self.bchkAttack = False
        # 使用AIP推进技术是否允许用户编辑
        self.bchkAPI = False
        # 吊放声纳是否允许用户编辑
        self.bchkDippingSonar = False

    def get_doctrine_owner(self):
        """
        功能：获取条令所有者
        参数：无
        返回：条令所有者
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        return self.situation.get_obj_by_guid(self.m_DoctrineOwner)

    @staticmethod
    def _classify_owner(owner_class_name):
        """
        功能：对条令所属对象进行分类
        参数：owner_class_name：{str:所属对象的类名}
        返回：'Side','Mission'或'Others'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        kinds = {
            'CSide': 'Side',
            'CPatrolMission': 'Mission',
            'CStrikeMission': 'Mission',
            'CSupportMission': 'Mission',
            'CCargoMission': 'Mission',
            'CFerryMission': 'Mission',
            'CMiningMission': 'Mission',
            'CMineClearingMission': 'Mission',
            'CGroup': 'Group'
        }
        if owner_class_name not in kinds:
            return 'Others'
        return kinds[owner_class_name]

    def use_nuclear_weapons(self, nuclear_status):
        """
        功能：决定是否使用核武器。
        参数：nuclear_status:{str:'yes'-使用，'no'-不使用}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {use_nuclear_weapons ='%s'})" % (
                owner.strGuid, nuclear_status)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {use_nuclear_weapons ='%s'})" % (
                owner.m_Side, owner.strGuid, nuclear_status)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {use_nuclear_weapons ='%s'})" % (
                owner.strGuid, nuclear_status)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_weapon_control_status(self, domain, fire_status):
        """
        功能：设置武器控制状态
        参数：domain:{str: 'weapon_control_status_subsurface'-对潜,
                          'weapon_control_status_surface'-对面,
                          'weapon_control_status_land'-对陆,
                          'weapon_control_status_air'-对空}
            fire_status:{str: '0'-自由开火,'1'-谨慎开火,'2'-限制开火}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/24/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {%s ='%s'})" % (
                owner.strGuid, domain, fire_status)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {%s ='%s'})" % (
                owner.m_Side, owner.strGuid, domain, fire_status)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {%s ='%s'})" % (
                owner.strGuid, domain, fire_status)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_weapon_control_status_subsurface(self, fire_status):
        """
        功能：设置对潜武器控制状态
        参数：fire_status:{str: '0'-自由开火,'1'-谨慎开火,'2'-限制开火}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/2/20, 4/24/20
        """
        return self.set_weapon_control_status('weapon_control_status_subsurface', fire_status)

    def set_weapon_control_status_surface(self, fire_status):
        """
        功能：设置对海武器控制状态
        参数：fire_status:{str: '0'-自由开火,'1'-谨慎开火,'2'-限制开火}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20, 4/24/20
        """
        return self.set_weapon_control_status('weapon_control_status_surface', fire_status)

    def set_weapon_control_status_land(self, fire_status):
        """
        功能：设置对地武器控制状态
        参数：fire_status:{str: '0'-自由开火,'1'-谨慎开火,'2'-限制开火}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        return self.set_weapon_control_status('weapon_control_status_land', fire_status)

    def set_weapon_control_status_air(self, fire_status):
        """
        功能：设置对空武器控制状态
        参数：fire_status:{str: '0'-自由开火,'1'-谨慎开火,'2'-限制开火}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/2/20, 4/24/20
        """
        return self.set_weapon_control_status('weapon_control_status_air', fire_status)

    def ignore_plotted_course(self, decision):
        """
        功能：决定是否忽略计划航线。
        参数：decision:{str:'yes'-忽略，'no'-不忽略}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {ignore_plotted_course ='%s'})" % (owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {ignore_plotted_course ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {ignore_plotted_course ='%s'})" % (owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_ambiguous_targets_engaging_status(self, ambiguous_targets_engaging_status):
        """
        功能：决定与模糊位置目标的交战状态。
        参数：ambiguous_targets_engaging_status:{str:'Ignore'('0')-忽略模糊性, 'Optimistic'('1')-乐观决策, 'Pessimistic'('2')-悲观决策}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {engaging_ambiguous_targets ='%s'})" % (
                owner.strGuid, ambiguous_targets_engaging_status)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {engaging_ambiguous_targets ='%s'})" % (
                owner.m_Side, owner.strGuid, ambiguous_targets_engaging_status)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {engaging_ambiguous_targets ='%s'})" % (
                owner.strGuid, ambiguous_targets_engaging_status)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_opportunity_targets_engaging_status(self, opportunity_targets_engaging_status):
        """
        功能：决定与临机目标的交战状态。
        参数：opportunity_targets_engaging_status:{str:'true'-可与任何目标交战, 'false'-只与任务相关目标交战}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {engage_opportunity_targets =%s})" % (
                owner.strGuid, opportunity_targets_engaging_status)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {engage_opportunity_targets =%s})" % (
                owner.m_Side, owner.strGuid, opportunity_targets_engaging_status)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {engage_opportunity_targets =%s})" % (
                owner.strGuid, opportunity_targets_engaging_status)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def ignore_emcon_while_under_attack(self, decision):
        """
        功能：决定受到攻击时是否忽略电磁管控。
        参数：decision: {str: 'true'-忽略，'false'-不忽略}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {ignore_emcon_while_under_attack =%s})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {ignore_emcon_while_under_attack =%s})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {ignore_emcon_while_under_attack =%s})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def use_kinematic_range_for_torpedoes(self, decision):
        """
        功能：决定如何使用鱼雷的动力航程。
        参数：decision: {str(或int): 'AutomaticAndManualFire'(0)-手动自动开火下都使用, 'ManualFireOnly'(1)仅手动开火下使用, 'No'(2)-不用}
        已知问题: decision使用字符串设置出错
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {kinematic_range_for_torpedoes ='%s'})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {kinematic_range_for_torpedoes ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {kinematic_range_for_torpedoes ='%s'})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def evade_automatically(self, decision):
        """
        功能：决定是否自动规避。
        参数：decision: {str: 'true'-是, 'false'-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {automatic_evasion =%s})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {automatic_evasion =%s})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {automatic_evasion =%s})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def use_refuel_supply(self, decision):
        """
        功能：决定是否允许加油补给。
        参数：decision: {str: '0'-允许但禁止加油机相互加油，'1'-不允许，'2'-允许}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {use_refuel_unrep ='%s'})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {use_refuel_unrep ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {use_refuel_unrep ='%s'})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def select_refuel_supply_object(self, decision):
        """
        功能：决定加油补给的选择对象。
        参数：decision: {str: '0'-选择最近的加油机, '1'-选择敌我之间的加油机, '2'-优先选择敌我之间的加油机并禁止回飞}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {refuel_unrep_selection ='%s'})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {refuel_unrep_selection ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {refuel_unrep_selection ='%s'})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def refuel_supply_allies(self, decision):
        """
        功能：决定是否给盟军单元加油补给。
        参数：decision: {str: '0'-是, '1'-是且仅接受，'2'-是且仅供给，'3'-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {refuel_unrep_allied ='%s'})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {refuel_unrep_allied ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {refuel_unrep_allied ='%s'})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_air_operations_tempo(self, tempo):
        """
        功能：设置空战节奏。
        参数：tempo: {str: 'Surge'('0')-快速出动,'Sustained'('1')-一般强度出动}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {air_operations_tempo ='%s'})" % (
                owner.strGuid, tempo)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {air_operations_tempo ='%s'})" % (
                owner.m_Side, owner.strGuid, tempo)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {air_operations_tempo ='%s'})" % (
                owner.strGuid, tempo)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def quick_turnaround_for_aircraft(self, decision):
        """
        功能：决定是否快速出动飞机。
        参数：decision: {str: 'Yes'('0')-是, 'Yes_FighterAndASWLoadoutOnly'('1')-战斗机与反潜机快速出动，'No'('2')-否}
        已知问题：设置为FightersAndASW时脚本执行出错
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {quick_turnaround_for_aircraft ='%s'})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {quick_turnaround_for_aircraft ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {quick_turnaround_for_aircraft ='%s'})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_fuel_state_for_aircraft(self, fuel_state):
        """
        功能：设置单架飞机返航的油料状态。
        参数：fuel_state: {str: 'Bingo'('0')-剩下计划储备油量时即终止任务返航,
                               'Joker10Percent'('1')-剩下1.1倍计划储备油量时即终止任务返航,
                               'Joker20Percent'('2')-剩下1.2倍计划储备油量时即终止任务返航,
                               'Joker25Percent'('3')-剩下1.25倍计划储备油量时即终止任务返航,
                               'Joker30Percent'('4')-剩下1.3倍计划储备油量时即终止任务返航,
                               'Joker40Percent'('5')-剩下1.4倍计划储备油量时即终止任务返航,
                               'Joker50Percent'('6')-剩下1.5倍计划储备油量时即终止任务返航,
                               'Joker60Percent'('7')-剩下1.6倍计划储备油量时即终止任务返航,
                               'Joker70Percent'('8')-剩下1.7倍计划储备油量时即终止任务返航,
                               'Joker75Percent'('9')-剩下1.75倍计划储备油量时即终止任务返航,
                               'Joker80Percent'('10')-剩下1.8倍计划储备油量时即终止任务返航,
                               'Joker90Percent'('11')-剩下1.9倍计划储备油量时即终止任务返航 }
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {fuel_state_planned ='%s'})" % (
                owner.strGuid, fuel_state)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {fuel_state_planned ='%s'})" % (
                owner.m_Side, owner.strGuid, fuel_state)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {fuel_state_planned ='%s'})" % (
                owner.strGuid, fuel_state)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_fuel_state_for_air_group(self, fuel_state):
        """
        功能：设置飞行编队返航的油料状态。
        参数：fuel_state: {str: 'No'('0')-无约束，编队不返航,
                           'YesLastUnit'('1')-编队中所有飞机均因达到单机油料状态要返航时，编队才返航,
                           'YesFirstUnit'('2')-编队中任意一架飞机达到单机油料状态要返航时，编队就返航,
                           'YesLeaveGroup'('3')-编队中任意一架飞机达到单机油料状态要返航时，其可离队返航}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {fuel_state_rtb ='%s'})" % (
                owner.strGuid, fuel_state)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {fuel_state_rtb ='%s'})" % (
                owner.m_Side, owner.strGuid, fuel_state)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {fuel_state_rtb ='%s'})" % (
                owner.strGuid, fuel_state)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_weapon_state_for_aircraft(self, weapon_state):
        """
        功能：设置单架飞机的武器状态。
        参数：weapon_state: {str: '0'-使用挂载设置,
                            '2001'-任务武器已耗光，立即脱离战斗,
                            '2002'-任务武器已耗光.允许使用航炮对临机目标进行打击（推荐）,
                            '3001'-所有超视距与防区外打击武器已经耗光.立即脱离战斗,
                            '3002'-所有超视距与防区外打击武器已经耗光. 允许使用视距内或防区内打击武器对较易攻击的临机出现目标进行攻击. 不使用航炮,
                            '3003'-所有超视距与防区外打击武器已经耗光. 允许使用视距内、防区内打击武器或者航炮对较易攻击的临机出现目标进行攻击,
                            '5001'-使用超视距或防区外打击武器进行一次交战.立即脱离战斗,
                            '5002'-使用超视距或防区外打击武器进行一次交战. 允许使用视距内或防区内打击武器对较易攻击的临机出现目标进行攻击. 不使用航炮,
                            '5003'-使用超视距或防区外打击武器进行一次交战. 允许使用视距内、防区内打击武器或者航炮对较易攻击的临机出现目标进行攻击,
                            '5005'-同时使用超视距/视距内或防区外/防区内打击武器进行一次交战.不使用航炮,
                            '5006'-同时使用超视距/视距内或防区外/防区内打击武器进行一次交战. 允许使用航炮对较易攻击的临机出现目标进行攻击,
                            '5011'-使用视距内或防区内打击武器进行一次交战. 立即脱离战斗,
                            '5012'-使用视距内或防区内打击武器进行一次交战. 允许使用航炮与临机出现目标格斗,
                            '5021'-使用航炮进行一次交战:
                            '4001'-25%相关武器已经耗光. 立即脱离战斗,
                            '4002'-25%相关武器已经耗光. 允许与临机出现目标交战，包括航炮,
                            '4011'-50%相关武器已经耗光. 立即脱离战斗
                            '4012'-50%相关武器已经耗光. 允许与临机出现目标交战，包括航炮
                            '4021'-75%相关武器已经耗光. 立即脱离战斗
                            '4022'-75%相关武器已经耗光. 允许与临机出现目标交战，包括航炮:4022}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {weapon_state_planned ='%s'})" % (
                owner.strGuid, weapon_state)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {weapon_state_planned ='%s'})" % (
                owner.m_Side, owner.strGuid, weapon_state)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {weapon_state_planned ='%s'})" % (
                owner.strGuid, weapon_state)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_weapon_state_for_air_group(self, weapon_state):
        """
        功能：设置飞行编队的武器状态。
        参数：weapon_state: {str: 'No'('0')-无约束，编队不返航,
                           'YesLastUnit'('1')-编队中所有飞机均因达到单机武器状态要返航时，编队才返航,
                           'YesFirstUnit'('2')-编队中任意一架飞机达到单机武器状态要返航时，编队就返航,
                           'YesLeaveGroup'('3')-编队中任意一架飞机达到单机武器状态要返航时，其可离队返航}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {weapon_state_rtb ='%s'})" % (
                owner.strGuid, weapon_state)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {weapon_state_rtb ='%s'})" % (
                owner.m_Side, owner.strGuid, weapon_state)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {weapon_state_rtb ='%s'})" % (
                owner.strGuid, weapon_state)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def gun_strafe_for_aircraft(self, decision):
        """
        功能：决定是否用航炮扫射
        参数：decision: {str: 'No'('0'):否， 'Yes'('1'):是}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {gun_strafing ='%s'})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {gun_strafing ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {gun_strafing ='%s'})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def jettison_ordnance_for_aircraft(self, decision):
        """
        功能：决定是否抛弃弹药。
        参数：decision: {str: 'No'('0')-否, 'Yes'('1')-是}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {jettison_ordnance ='%s'})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {jettison_ordnance ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {jettison_ordnance ='%s'})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def use_sams_to_anti_surface(self, decision):
        """
        功能：决定是否以反舰模式使用舰空导弹。
        参数：decision: {str: 'true'-是，'false'-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {use_sams_in_anti_surface_mode =%s})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {use_sams_in_anti_surface_mode =%s})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {use_sams_in_anti_surface_mode =%s})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def maintain_standoff(self, decision):
        """
        功能：决定是否与目标保持距离。
        参数：decision: {str: 'true'-是, 'false'-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {maintain_standoff =%s})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {maintain_standoff =%s})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {maintain_standoff =%s})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def avoid_being_searched_for_submarine(self, decision):
        """
        功能：决定是否规避搜索。
        参数：decision: {str: 'No'('0')-否, 'Yes_ExceptSelfDefence'('1')除非自卫均是,'Yes_Always'('2')-总是}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {avoid_contact ='%s'})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {avoid_contact ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {avoid_contact ='%s'})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def dive_on_threat(self, decision):
        """
        功能：决定探测到威胁时是否下潜。
        参数：decision: {str: 'Yes'('0')-在敌潜望镜或对面搜索雷达侦察时下潜,
                             'Yes_ESM_Only'('1')-在敌电子侦察措施侦察或目标接近时下潜,
                             'Yes_Ships20nm_Aircraft30nm'('2')-在20海里内有敌舰或30海里内有敌机时下潜,
                             'No'('3')-否}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {dive_on_threat ='%s'})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {dive_on_threat ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {dive_on_threat ='%s'})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_recharging_condition_on_patrol(self, recharging_condition):
        """
        功能：设置出航或阵位再充电条件。
        参数：recharging_condition: {string: 'Recharge_Empty'('0')-电量用完再充,
                                            'Recharge_10_Percent'('10')-电量剩下10%时再充,
                                            'Recharge_20_Percent'('20')-电量剩下20%时再充,
                                            'Recharge_30_Percent'('30')-电量剩下30%时再充,
                                            'Recharge_40_Percent'('40')-电量剩下40%时再充,
                                            'Recharge_50_Percent'('50')-电量剩下50%时再充,
                                            'Recharge_60_Percent'('60')-电量剩下60%时再充,
                                            'Recharge_70_Percent'('70')-电量剩下70%时再充,
                                            'Recharge_80_Percent'('80')-电量剩下80%时再充,
                                            'Recharge_90_Percent'('90')-电量剩下90%时再充}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {recharge_on_patrol ='%s'})" % (
                owner.strGuid, recharging_condition)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {recharge_on_patrol ='%s'})" % (
                owner.m_Side, owner.strGuid, recharging_condition)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {recharge_on_patrol ='%s'})" % (
                owner.strGuid, recharging_condition)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_recharging_condition_on_attack(self, recharging_condition):
        """
        功能：设置进攻或防御再充电条件。
        参数：recharging_condition: {string: 'Recharge_Empty'('0')-电量用完再充,
                                            'Recharge_10_Percent'('10')-电量剩下10%时再充,
                                            'Recharge_20_Percent'('20')-电量剩下20%时再充,
                                            'Recharge_30_Percent'('30')-电量剩下30%时再充,
                                            'Recharge_40_Percent'('40')-电量剩下40%时再充,
                                            'Recharge_50_Percent'('50')-电量剩下50%时再充,
                                            'Recharge_60_Percent'('60')-电量剩下60%时再充,
                                            'Recharge_70_Percent'('70')-电量剩下70%时再充,
                                            'Recharge_80_Percent'('80')-电量剩下80%时再充,
                                            'Recharge_90_Percent'('90')-电量剩下90%时再充}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {recharge_on_attack ='%s'})" % (
                owner.strGuid, recharging_condition)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {recharge_on_attack ='%s'})" % (
                owner.m_Side, owner.strGuid, recharging_condition)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {recharge_on_attack ='%s'})" % (
                owner.strGuid, recharging_condition)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def use_aip(self, decision):
        """
        功能：决定是否使用“不依赖空气推进”系统。
        参数：decision: {str: 'No'('0')-否, 'Yes_AttackOnly'('1')-在进攻或防御时使用, 'Yes_Always'('2')-总是}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {use_aip ='%s'})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {use_aip ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {use_aip ='%s'})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def use_dipping_sonar(self, decision):
        """
        功能：决定是否使用吊放声呐。
        参数：decision: {str: 'Automatically_HoverAnd150ft'('0')-自动到150英尺悬停并使用,
                             'ManualAndMissionOnly'('1')-只能人工使用或者分配到任务}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/3/20
        张志高修改于2021-7-26，修正错误的Lua
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {dipping_sonar ='%s'})" % (
                owner.strGuid, decision)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {dipping_sonar ='%s'})" % (
                owner.m_Side, owner.strGuid, decision)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {dipping_sonar ='%s'})" % (
                owner.strGuid, decision)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_em_control_status(self, em_item, status):
        """
        功能：设置电磁管控状态
        参数：em_item: {str: 'Radar'-雷达, 'Sonar'-声呐, 'OECM'-光电对抗}
             status: {str: 'Passive'-仅有被动设备工作, 'Active'-另有主动设备工作
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetEMCON('Side','%s','%s=%s')" % (
                owner.strGuid, em_item, status)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetEMCON('Mission','%s','%s=%s')" % (
                owner.strGuid, em_item, status)
        elif owner_type == 'Group':
            cmd = "ScenEdit_SetEMCON('Group','%s','%s=%s')" % (
                owner.strGuid, em_item, status)
        else:
            cmd = "ScenEdit_SetEMCON('Unit','%s','%s=%s')" % (
                owner.strGuid, em_item, status)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_weapon_release_authority(self, weapon_dbid, target_type, quantity_salvo=2, shooter_salvo=1,
                                     firing_range='none', self_defense='max', escort=''):
        """
        功能：设置条令的武器使用规则
        参数：weapon_dbid: {str: 武器的数据库ID}
             target_type: {str: 目标类型号,具体映射关系参照args.py中的WRA_WeaponTargetType}
             quantity_salvo: {str or int: 'n'-齐射武器数, 'inherit'-继承设置, 'max'-全量齐射, 'none'-禁用}
             shooter_salvo: {str or int: 'n'-齐射发射架数，'inherit'-继承设置, 'max'-全量齐射}
             firing_range: {str or float: 'n'-自动开火距离(单位海里)，'inherit'-继承设置, 'max'-最大射程射击，'none'-禁用自动开火}
             self_defense: {str or float: 'n'-自动防御距离（单位海里）, 'inherit'-继承设置, 'max'-最大射程射击, 'none'-禁用自卫}
             escort: {str: 'true'-护航任务, 'false'-非护航任务}
             注：其中n为数字，如果n不与列表中的项匹配，取最近的值。
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        修改：张志高 2021-8-18
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "Hs_SetDoctrineWRA({side='%s', WEAPON_ID='%s' , target_type='%s', escort='%s'},{qty_salvo='%s'," \
                  "shooter_salvo='%s',firing_range='%s',self_defence='%s'})" % (
                      owner.strGuid, weapon_dbid, target_type, escort, quantity_salvo, shooter_salvo, firing_range,
                      self_defense)
        elif owner_type == 'Mission':
            cmd = "Hs_SetDoctrineWRA({side='%s', mission='%s', WEAPON_ID='%s' , target_type='%s', escort='%s'}," \
                  "{qty_salvo='%s'," \
                  "shooter_salvo='%s',firing_range='%s',self_defence='%s'})" % (
                      owner.m_Side, owner.strGuid, weapon_dbid, target_type, escort, quantity_salvo, shooter_salvo,
                      firing_range, self_defense)
        else:
            cmd = "Hs_SetDoctrineWRA({guid ='%s', WEAPON_ID='%s', target_type='%s', escort='%s'},{qty_salvo='%s'," \
                  "shooter_salvo='%s',firing_range='%s',self_defence='%s'})" % (
                      owner.strGuid, weapon_dbid, target_type, escort, quantity_salvo, shooter_salvo, firing_range,
                      self_defense)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def withdraw_on_damage(self, damage_degree):
        """
        功能：决定导致撤退的毁伤程度。
        参数：damage_degree: {str: 'Ignore'('0')-忽略毁伤不撤退,
                                  'Percent5'('1')-毁伤大于5%撤退,
                                  'Percent25'('2')-毁伤大于25%撤退,
                                  'Percent50'('3')-毁伤大于50%撤退,
                                  'Percent75'('4')-毁伤大于75%撤退}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/4/20 悼念全国新冠疫情遇难同胞，默哀~~~
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {withdraw_on_damage ='%s'})" % (
                owner.strGuid, damage_degree)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {withdraw_on_damage ='%s'})" % (
                owner.m_Side, owner.strGuid, damage_degree)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {withdraw_on_damage ='%s'})" % (
                owner.strGuid, damage_degree)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def withdraw_on_fuel(self, fuel_quantity):
        """
        功能：决定导致撤退的油量多少。
        参数：fuel_quantity: {str: 'Ignore'('0')-忽略油量不撤退,
                                  'Bingo'('1')-少于计划储备油量时撤退,
                                  'Percent25'('2')-少于25%时撤退,
                                  'Percent50'('3')-少于50%时撤退,
                                  'Percent75'('4')-少于75%时即撤退}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/4/20  悼念全国新冠疫情遇难同胞，默哀~~~
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {withdraw_on_fuel ='%s'})" % (
                owner.strGuid, fuel_quantity)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {withdraw_on_fuel ='%s'})" % (
                owner.m_Side, owner.strGuid, fuel_quantity)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {withdraw_on_fuel ='%s'})" % (
                owner.strGuid, fuel_quantity)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def withdraw_on_attack_weapon(self, weapon_quantity):
        """
        功能：决定导致撤退的主攻武器量。
        参数：weapon_quantity: {str: 'Ignore'('0')-忽略武器量不撤退,
                                    'Exhausted'('1')-打光才撤,
                                    'Percent25'('2')-主攻武器量消耗到25%时撤退,
                                    'Percent50'('3')-主攻武器量消耗到50%时撤退,
                                    'Percent75'('4')-主攻武器量消耗到75%时撤退}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/4/20 悼念全国新冠疫情遇难同胞，默哀~~~
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {withdraw_on_attack ='%s'})" % (
                owner.strGuid, weapon_quantity)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {withdraw_on_attack ='%s'})" % (
                owner.m_Side, owner.strGuid, weapon_quantity)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {withdraw_on_attack ='%s'})" % (
                owner.strGuid, weapon_quantity)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def withdraw_on_defence_weapon(self, weapon_quantity):
        """
        功能：决定导致撤退的主防武器量。
        参数：weapon_quantity: {str: 'Ignore'('0')-忽略武器量不撤退,
                                    'Exhausted'('1')-打光才撤,
                                    'Percent25'('2')-主防武器量消耗到25%时撤退,
                                    'Percent50'('3')-主防武器量消耗到50%时撤退,
                                    'Percent75'('4')-主防武器量消耗到75%时撤退}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/4/20 悼念全国新冠疫情遇难同胞，默哀~~~
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {withdraw_on_defence ='%s'})" % (
                owner.strGuid, weapon_quantity)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {withdraw_on_defence ='%s'})" % (
                owner.m_Side, owner.strGuid, weapon_quantity)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {withdraw_on_defence ='%s'})" % (
                owner.strGuid, weapon_quantity)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def redeploy_on_damage(self, damage_degree):
        """
        功能：决定导致重新部署的毁伤程度。
        参数：damage_degree: {str: 'Ignore'('0')-忽略毁伤重新部署,
                                  'Percent5'('1')-毁伤小于5%重新部署,
                                  'Percent25'('2')-毁伤小于25%重新部署,
                                  'Percent50'('3')-毁伤小于50%重新部署,
                                  'Percent75'('4')-毁伤小于75%重新部署}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/4/20 悼念全国新冠疫情遇难同胞，默哀~~~
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {deploy_on_damage ='%s'})" % (
                owner.strGuid, damage_degree)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {deploy_on_damage ='%s'})" % (
                owner.m_Side, owner.strGuid, damage_degree)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {deploy_on_damage ='%s'})" % (
                owner.strGuid, damage_degree)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def redeploy_on_fuel(self, fuel_quantity):
        """
        功能：决定导致重新部署的油量多少。
        参数：fuel_quantity: {str: 'Ignore'('0')-忽略油量重新部署,
                                  'Bingo'('1')-至少为计划储备油量时重新部署,
                                  'Percent25'('2')-至少为25%时重新部署,
                                  'Percent50'('3')-至少为50%时重新部署,
                                  'Percent75'('4')-至少为75%时即重新部署,
                                  'Percent100'('5')-必须满油才能重新部署}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/4/20  悼念全国新冠疫情遇难同胞，默哀~~~
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {deploy_on_fuel ='%s'})" % (
                owner.strGuid, fuel_quantity)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {deploy_on_fuel ='%s'})" % (
                owner.m_Side, owner.strGuid, fuel_quantity)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {deploy_on_fuel ='%s'})" % (
                owner.strGuid, fuel_quantity)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def redeploy_on_attack_weapon(self, weapon_quantity):
        """
        功能：决定导致重新部署的主攻武器量。
        参数：weapon_quantity: {str: 'Ignore'('0')-忽略武器量重新部署,
                                    'Exhausted'('1')-耗光也要重新部署,
                                    'Percent25'('2')-主攻武器量处于25%时重新部署,
                                    'Percent50'('3')-主攻武器量处于50%时重新部署,
                                    'Percent75'('4')-主攻武器量处于75%时重新部署,
                                    'Percent100'('5')--主攻武器满载才能重新部署,
                                    'LoadFullWeapons'('6')-所有武器挂满才能重新部署}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/4/20 悼念全国新冠疫情遇难同胞，默哀~~~
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {deploy_on_attack ='%s'})" % (
                owner.strGuid, weapon_quantity)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {deploy_on_attack ='%s'})" % (
                owner.m_Side, owner.strGuid, weapon_quantity)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {deploy_on_attack ='%s'})" % (
                owner.strGuid, weapon_quantity)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def redeploy_on_defence_weapon(self, weapon_quantity):
        """
        功能：决定导致重新部署的主防武器量。
        参数：weapon_quantity: {str: 'Ignore'('0')-忽略武器量重新部署,
                                    'Exhausted'('1')-耗光也要重新部署,
                                    'Percent25'('2')-主防武器量处于25%时重新部署,
                                    'Percent50'('3')-主防武器量处于50%时重新部署,
                                    'Percent75'('4')-主防武器量处于75%时重新部署,
                                    'Percent100'('5')--主防武器满载才能重新部署,
                                    'LoadFullWeapons'('6')-所有武器挂满才能重新部署}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/4/20 悼念全国新冠疫情遇难同胞，默哀~~~
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side':
            cmd = "ScenEdit_SetDoctrine({side ='%s' }, {deploy_on_defence ='%s'})" % (
                owner.strGuid, weapon_quantity)
        elif owner_type == 'Mission':
            cmd = "ScenEdit_SetDoctrine({side ='%s', mission = '%s'}, {deploy_on_defence ='%s'})" % (
                owner.m_Side, owner.strGuid, weapon_quantity)
        else:
            cmd = "ScenEdit_SetDoctrine({guid ='%s' }, {deploy_on_defence ='%s'})" % (
                owner.strGuid, weapon_quantity)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def reset(self, level, aspect, escort_status='false'):
        """
        功能：重置作战条令
        参数：level: {str: 'Left'-重置本级作战条令,'Middle'-重置关联单元的作战条令,'Right'-重置关联任务的作战条令}
             aspect: {str: 'Ensemble'-总体条令，'EMCON'-电磁管控条令，'Weapon'-武器使用规则}
             escort_status: {str: 'true'-针对护航任务，'false'-非护航任务}
        返回：'lua执行成功' 或
             '脚本执行出错' 或
             '错：推演方没有上级，无法继承条令设置。' 或
             '错：编队之下没有受其影响的任务，无法向其传递条令。' 或
             '错：单元之下没有受其影响的任务或单元，无法向下传递条令。'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type == 'Side' and level == 'Left':
            return "错：推演方没有上级，无法继承条令设置。"
        if owner_type == 'Group' and level == 'Right':
            return "错：编队之下没有受其影响的任务，无法向其传递条令。"
        if owner_type == 'Others' and level != 'Left':
            return "错：单元之下没有受其影响的任务或单元，无法向下传递条令。"
        cmd = "Hs_ResetDoctrine('%s', '%s', '%s', %s)" % (owner.strGuid, level, aspect, escort_status)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def set_emcon_according_to_superiors(self, em_status, escort_status='false'):
        """
        功能：设置单元电磁管控与上级一致.
        参数：em_status: {str: 'yes'-与上级一致，'no'-与上级不一致}
             escort_status: {str: 'true'-为护航电磁管控， 'false'-非护航电磁管控}
        返回：'lua执行成功' 或 '脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/7/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type in ['Side', 'Mission', 'Group']:
            return None
        else:
            cmd = "Hs_SetInLineWithSuperiors('%s','%s',%s)" % (owner.strGuid, em_status, escort_status)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)

    def unit_obeys_emcon(self, is_obey):
        """
        函数功能：设置单元是否遵循电磁管控
        函数类型：推演函数
        :param is_obey: {str: 'true'-遵循电磁管控， 'false'-不遵循电磁管控}
        :return: None, 'lua执行成功' 或 '脚本执行出错'
        修订：aie
        时间：4/8/20
        """
        owner = self.get_doctrine_owner()
        owner_type = self._classify_owner(owner.ClassName)
        if owner_type in ['Side', 'Mission', 'Group']:
            return None
        else:
            cmd = "Hs_UnitObeysEMCON('{}', {})".format(owner.strGuid, is_obey)
        self.mozi_server.throw_into_pool(cmd)
        return self.mozi_server.send_and_recv(cmd)
