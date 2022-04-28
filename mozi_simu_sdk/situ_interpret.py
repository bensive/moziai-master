# -*- coding:utf-8 -*-

from enum import Enum


class CCurrentScenarioDict:
    class Info(Enum):
        GUID = "string GUID"
        strTitle = "string 想定标题"
        strScenFileName = "string 想定文件名"
        strDescription = "string 描述"
        m_Time = "double 当前时间"
        bDaylightSavingTime = "bool 是否是夏令时"
        m_FirstTimeRunDateTime = "double 当前想定第一次启动的开始时间"
        strDaylightSavingTime_Start = "string 夏令时开始时间"
        strDaylightSavingTime_End = "string 夏令时结束时间"
        m_StartTime = "double 想定开始时间"
        m_Duration = "string 想定持续时间"
        sMeta_Complexity = "short 想定复杂度"
        sMeta_Difficulty = "short 想定困难度"
        strMeta_ScenSetting = "string 想定发生地"
        strDeclaredFeatures = "string  想定精细度枚举值"
        strCustomFileName = "string 想定名称"


class CDoctrineDict:
    class Info(Enum):
        strGuid = "string GUID"
        m_DoctrineOwner = "string 条令的拥有者"
        m_Nukes = "int 核武器使用规则 (枚举量)"
        m_WCS_Air = "int 对空目标武器控制规则 (枚举量)"
        m_WCS_Surface = "int 对海目标武器控制规则 (枚举量)"
        m_WCS_Submarine = "int 对潜目标武器控制规则 (枚举量)"
        m_WCS_Land = "int 对地目标武器控制规则 (枚举量)"
        m_IgnorePlottedCourseWhenAttacking = "int 进攻时是否忽略绘制航线规则 (枚举量)"
        m_BehaviorTowardsAmbigousTarget = "int 对不明目标的行为态度规则 (枚举量)"
        m_ShootTourists = "int 对临机目标进行射击规则 (枚举量)"
        m_IgnoreEMCONUnderAttack = "int 受攻击时是否考虑电磁管控规则 (枚举量)"
        m_UseTorpedoesKinematicRange = "int 鱼雷使用动力航程规则 (枚举量)"
        m_AutomaticEvasion = "int 是否自动规避目标规则 (枚举量)"
        m_UseRefuel = "int 是否可加油/补给规则 (枚举量)"
        m_RefuelSelection = "int 对所选单元加油/补给时加油机选择规则 (枚举量)"
        m_RefuelAllies = "int 与盟军单元加油/补给规则 (枚举量)"
        m_AirOpsTempo = "int 空战节奏规则 (枚举量)"
        m_QuickTurnAround = "int 快速出动规则 (枚举量)"
        m_BingoJoker = "int 预先规划终止任务返回基地油量阈值规则 (枚举量)"
        m_BingoJokerRTB = "int 编组成员达到预先规划油量状态时编组或成员返回基地规则 (枚举量)"
        m_WeaponState = "int 预先规划武器使用规则、武器状态与平台脱离战斗规则 (枚举量)"
        m_WeaponStateRTB = "int 编组成员达到预先规划武器状态时，编组或成员返回基地规则 (枚举量)"
        m_GunStrafeGroundTargets = "int 航炮是否对地面目标扫射规则 (枚举量)"
        m_JettisonOrdnance = "int 受到攻击时是否抛弃弹药规则 (枚举量)"
        m_SAM_ASUW = "int 以反舰模式使用舰空导弹规则 (枚举量)"
        m_MaintainStandoff = "int 与目标保持一定距离规则 (枚举量)"
        m_AvoidContact = "int 尽可能规避目标规则 (枚举量)"
        m_DiveWhenThreatsDetected = "int 探测到威胁目标后下潜规则 (枚举量)"
        m_RechargePercentagePatrol = "int 巡逻任务充电时电池剩余电量规则 (枚举量)"
        m_RechargePercentageAttack = "int 进攻战充电时电池剩余电量规则 (枚举量)"
        m_AIPUsage = "int AIP推进技术使用规则 (枚举量)"
        m_DippingSonar = "int 吊放声呐使用规则 (枚举量)"
        m_WithdrawDamageThreshold = "int 毁伤达到阈值时应撤退规则 (枚举量)"
        m_WithdrawFuelThreshold = "int 油量达到阈值时应撤退规则 (枚举量)"
        m_WithdrawAttackThreshold = "int 进攻战武器数量达到阈值应撤退规则 (枚举量)"
        m_WithdrawDefenceThreshold = "int 防御战武器数量达到阈值应撤退规则 (枚举量)"
        m_RedeployDamageThreshold = "int 毁伤达到阈值时应重新部署规则 (枚举量)"
        m_RedeployFuelThreshold = "int 油量达到阈值时应重新部署规则 (枚举量)"
        m_RedeployAttackDamageThreshold = "int 进攻战武器数量达到阈值时应重新部署规则 (枚举量)"
        m_RedeployDefenceDamageThreshold = "int 防御战武器数量达到阈值时应重新部署规则 (枚举量)"
        m_bEMCON_AccordingSuperior = "bool 电磁管控设置是否有值"
        m_EMCON_SettingsForRadar = "int 雷达管控规则设置模式 (枚举量)"
        m_EMCON_SettingsForSonar = "int 声呐管控规则设置模式 (枚举量)"
        m_EMCON_SettingsForOECM = "int 进攻型电子对抗措施（干扰机）管控规则设置模式(枚举量)"
        m_WRA_WeaponRule_WeaponDBID = "string 武器使用规则的武器DBID"
        m_WRA_WeaponRule = "string 武器使用规则"
        bchkUseNuclerWeapon = "bool 使用核武器是否允许用户编辑"
        bchkWeaponStateAir = "bool 武器控制状态对空是否允许用户编辑"
        bchkWeaponStateSea = "bool 武器控制状态对海是否允许用户编辑"
        bchkWeaponStateSeaLatent = "bool 武器控制状态对潜是否允许用户编辑"
        bchkWeaponStateland = "bool 武器控制状态对地是否允许用户编辑"
        bchkIgnoreRoutes = "bool 受到攻击时忽略计划航线是否允许用户编辑"
        bchkFuzzlocationOfTheReceIvingstation = "bool 接战模糊位置目标是否允许用户编辑"
        bchkImminentTarget = "bool 接战临机出现目标是否允许用户编辑"
        bchkIgnoreElectromagneticControl = "bool 受攻击时忽略电磁管控是否允许用户编辑"
        bchkTopedopower = "bool 鱼雷使用动力航程是否选中复选框"
        bchkAutoAcoid = "bool 自动规避是否允许用户编辑"
        bchkComeOn = "bool 加油/补给是否选中复选框"
        bchkSelectUnitComeOn = "bool 对所选单元进行加油/补给是否允许用户编辑"
        bchkAlliedUnitComeOn = "bool 对盟军单元进行加油/补给是否允许用户编辑"
        bchkAirOpsTempo_Player = "bool 空战节奏是否允许用户编辑"
        bchkQTA_Player = "bool 快速出动是否允许用户编辑"
        bchkBingoJoker_Player = "bool 燃油状态，预先规划是否允许用户编辑"
        bchkBingoJokerRTB_Player = "bool 燃油状态—返航是否允许用户编辑"
        bchkWeaponStateFirast = "bool 武器状态, 预先规划是否允许用户编辑"
        bchkWeaponStateReturn = "bool 武器状态-返航是否允许用户编辑"
        bchkAirToGroundUserEdit = "bool 空对地扫射(航炮)是否允许用户编辑"
        bchkAbandonedAmmunition = "bool 抛弃弹药是否允许用户编辑"
        bchkSAM_ASUW_Player = "bool 以反舰模式使用舰空导弹规则是否允许用户编辑"
        bchkKeepTargetDistance = "bool 与目标保持一定距离规则是否允许用户编辑"
        bchkToAvoidTheSearch = "bool 规避搜索规则是否允许用户编辑"
        bchkThreatWasDetectedAndDived = "bool 探测到威胁进行下潜规则是否允许用户编辑"
        bchkSetSail = "bool 电池充电 %, 出航/阵位是否允许用户编辑"
        bchkAttack = "bool 电池充电%, 进攻/防御是否允许用户编辑"
        bchkAPI = "bool 使用AIP推进技术是否允许用户编辑"
        bchkDippingSonar = "bool 吊放声纳是否允许用户编辑"

    m_Nukes = {
        0: "不授权，禁止使用",
        1: "授权，可以使用",
        2: "多样",
        3: "未配置"
        }

    m_WCS_Air = {
        0: "自由开火",
        1: "谨慎开火",
        2: "限制开火",
        3: "多样",
        4: "未配置"
        }
    m_WCS_Surface = {
        0: "自由开火",
        1: "谨慎开火",
        2: "限制开火",
        3: "多样",
        4: "未配置"
        }
    m_WCS_Submarine = {
        0: "自由开火",
        1: "谨慎开火",
        2: "限制开火",
        3: "多样",
        4: "未配置"
        }
    m_WCS_Land = {
        0: "自由开火",
        1: "谨慎开火",
        2: "限制开火",
        3: "多样",
        4: "未配置"
        }
    m_IgnorePlottedCourseWhenAttacking = {
        0: "不忽略",
        1: "忽略",
        2: "多样",
        3: "未配置"
        }
    m_BehaviorTowardsAmbigousTarget = {
        0: "忽略模糊性",
        1: "乐观决策",
        2: "悲观决策",
        3: "多样",
        4: "未配置"
        }
    m_ShootTourists = {
        0: "否,只与任务相关的目标进行交战",
        1: "是,可对临机目标进行射击",
        2: "多样",
        3: "未配置"
        }
    m_IgnoreEMCONUnderAttack = {
        0: "不忽略,考虑电磁管控",
        1: "忽略,不考虑电磁管控",
        2: "多样",
        3: "未配置"
        }
    m_UseTorpedoesKinematicRange = {
        0: "自动与手动发射都使用动力航程",
        1: "只有手动发射时使用动力航程",
        2: "使用实际航程",
        3: "多样",
        4: "未配置"
        }
    m_AutomaticEvasion = {
        0: "否",
        1: "是",
        2: "多样",
        3: "未配置"
        }
    m_UseRefuel = {
        0: "允许,不允许加油机对加油机加油",
        1: "不允许",
        2: "允许",
        3: "多样",
        4: "未配置"
        }
    m_RefuelSelection = {
        0: "选择最近的加油机",
        1: "选择位于我们和目标之间的加油机",
        2: "优先考虑位于我们和目标之间的加油机, 但不允许往回飞",
        3: "多样",
        4: "未配置"
        }
    m_RefuelAllies = {
        0: "补给",
        1: "只接收",
        2: "只传送",
        3: "不补给",
        4: "多样",
        5: "未配置"
        }
    m_AirOpsTempo = {
        0: "大批出动",
        1: "可持续性出动",
        2: "多样",
        3: "未配置"
        }
    m_QuickTurnAround = {
        0: "可以快速出动",
        1: "战斗机以及反潜战挂载武器可以快速出动",
        2: "不可以快速出动",
        3: "多样",
        4: "未配置"
        }
    m_BingoJoker = {
        0: "返航油量（计划预留燃油）: 足够回基地,包括降落耗油",
        1: "10%,比返航油量多10%的任务油量",
        2: "20%",
        3: "25%",
        4: "30%",
        5: "40%",
        6: "50%",
        7: "60%",
        8: "70%",
        9: "75%",
        10: "80%",
        11: "90%",
        12: "多样",
        14: "未配置"
        }
    m_BingoJokerRTB = {
        0: "不返回基地",
        1: "最后单元达到返回基地油量状态时,编组返回基地",
        2: "首个单元达到返回基地油量状态时,编组返回基地",
        3: "当单元达到返回基地油量状态时,脱离编组返回基地",
        4: "多样",
        5: "未配置"
        }
    m_WeaponState = {
        0: "使用挂载设置",
        2001: "任务武器已耗光,立即脱离战斗",
        2002: "任务武器已耗光.允许使用航炮对临机目标进行打击（推荐）",
        3001: "所有超视距与防区外打击武器已经耗光.立即脱离战斗",
        3002: "所有超视距与防区外打击武器已经耗光. 允许使用视距内或防区内打击武器对较易攻击的临机出现目标进行攻击. 不使用航炮",
        3003: "所有超视距与防区外打击武器已经耗光. 允许使用视距内、防区内打击武器或者航炮对较易攻击的临机出现目标进行攻击",
        5001: "使用超视距或防区外打击武器进行一次交战.立即脱离战斗",
        5002: "使用超视距或防区外打击武器进行一次交战. 允许使用视距内或防区内打击武器对较易攻击的临机出现目标进行攻击. 不使用航炮",
        5003: "使用超视距或防区外打击武器进行一次交战. 允许使用视距内、防区内打击武器或者航炮对较易攻击的临机出现目标进行攻击",
        5005: "同时使用超视距/视距内或防区外/防区内打击武器进行一次交战.不使用航炮",
        5006: "同时使用超视距/视距内或防区外/防区内打击武器进行一次交战. 允许使用航炮对较易攻击的临机出现目标进行攻击",
        5011: "使用视距内或防区内打击武器进行一次交战. 立即脱离战斗",
        5012: "使用视距内或防区内打击武器进行一次交战. 允许使用航炮与临机出现目标格斗",
        5021: "使用航炮进行一次交战",
        4001: "25%相关武器已经耗光. 立即脱离战斗",
        4002: "25%相关武器已经耗光. 允许与临机出现目标交战,包括航炮",
        4011: "50%相关武器已经耗光. 立即脱离战斗",
        4012: "50%相关武器已经耗光. 允许与临机出现目标交战,包括航炮",
        4021: "75%相关武器已经耗光. 立即脱离战斗",
        4022: "75%相关武器已经耗光. 允许与临机出现目标交战,包括航炮",
        1: "多样",
        2: "未配置"
        }
    m_WeaponStateRTB = {
        0: "否, 达到武器状态时编组均不返回基地",
        1: "是, 当编组最后一个单元达到武器状态时,编组返回基地",
        2: "是, 当编组第一个单元达到武器状态时,编组返回基地",
        3: "是, 编组成员达到武器状态时离开编队返回基地",
        4: "多样",
        5: "未配置"
        }
    m_GunStrafeGroundTargets = {
        0: "否",
        1: "是",
        2: "多样",
        3: "未配置"
        }
    m_JettisonOrdnance = {
        0: "不抛弃",
        1: "抛弃",
        2: "多样",
        3: "未配置"
        }
    m_SAM_ASUW = {
        0: "不能使用反舰模式",
        1: "可以使用反舰模式",
        2: "多样",
        3: "未配置"
        }
    m_MaintainStandoff = {
        0: "否",
        1: "是",
        2: "多样",
        3: "未配置"
        }
    m_AvoidContact = {
        0: "不规避",
        1: "除自防御外尽可能规避",
        2: "总是规避",
        3: "多样",
        4: "未配置"
        }
    m_DiveWhenThreatsDetected = {
        0: "当电子侦察措施探测和目标接近时下潜",
        1: "当潜艇的ESM探测到目标,并且目标的传感器有潜望镜 或者 潜艇深度小于5米并且目标的传感器有水面搜索能力时下潜",
        2: "当水面舰艇20海里内或飞机在30海里内时下潜",
        3: "不下潜",
        4: "多样",
        5: "未配置"
        }
    m_RechargePercentagePatrol = {
        0: "电池耗光电量",
        10: "电池10%电量",
        20: "电池20%电量",
        30: "电池30%电量",
        40: "电池40%电量",
        50: "电池50%电量",
        60: "电池60%电量",
        70: "电池70%电量",
        80: "电池80%电量",
        90: "电池90%电量",
        -100: "多样",
        -101: "未配"
        }
    m_RechargePercentageAttack = {
        0: "电池耗光电量",
        10: "电池10%电量",
        20: "电池20%电量",
        30: "电池30%电量",
        40: "电池40%电量",
        50: "电池50%电量",
        60: "电池60%电量",
        70: "电池70%电量",
        80: "电池80%电量",
        90: "电池90%电量",
        -100: "多样",
        -101: "未配"
        }
    m_AIPUsage = {
        0: "不使用",
        1: "只在进攻时",
        2: "总是",
        3: "多样",
        4: "未配置"
        }
    m_DippingSonar = {
        0: "盘旋于150英尺高时自动部署",
        1: "人工或任务部署",
        2: "多样",
        3: "未配置"
        }
    m_WithdrawDamageThreshold = {
        0: "忽略",
        1: "毁伤程度大于5%",
        2: "毁伤程度大于25%",
        3: "毁伤程度大于50%",
        4: "毁伤程度大于75%",
        5: "多样",
        6: "未配置"
        }
    m_WithdrawFuelThreshold = {
        0: "忽略,不考虑油量",
        1: "返航油量",
        2: "燃油少于25%",
        3: "燃油少于50%",
        4: "燃油少于75%",
        5: "燃油少于100%",
        6: "多样",
        7: "未配置"
        }
    m_WithdrawAttackThreshold = {
        0: "忽略,不考虑武器数量",
        1: "耗尽",
        2: "攻击武器至少处于25%",
        3: "攻击武器至少处于50%",
        4: "攻击武器至少处于75%",
        5: "攻击武器至少处于100%",
        6: "满载",
        7: "多样",
        8: "未配置"
        }
    m_WithdrawDefenceThreshold = {
        0: "忽略,不考虑武器数量",
        1: "耗尽",
        2: "攻击武器至少处于25%",
        3: "攻击武器至少处于50%",
        4: "攻击武器至少处于75%",
        5: "攻击武器至少处于100%",
        6: "满载",
        7: "多样",
        8: "未配置"
        }
    m_RedeployDamageThreshold = {
        0: "忽略",
        1: "毁伤程度大于5%",
        2: "毁伤程度大于25%",
        3: "毁伤程度大于50%",
        4: "毁伤程度大于75%",
        5: "多样",
        6: "未配"
        }
    m_RedeployFuelThreshold = {
        0: "忽略,不考虑油量",
        1: "返航油量",
        2: "燃油少于25%",
        3: "燃油少于50%",
        4: "燃油少于75%",
        5: "燃油少于100%",
        6: "多样",
        7: "未配置"
        }
    m_RedeployAttackDamageThreshold = {
        0: "忽略,不考虑武器数量",
        1: "耗尽",
        2: "攻击武器至少处于25%",
        3: "攻击武器至少处于50%",
        4: "攻击武器至少处于75%",
        5: "攻击武器至少处于100%",
        6: "满载",
        7: "多样",
        8: "未配置"
        }
    m_RedeployDefenceDamageThreshold = {
        0: "忽略,不考虑武器数量",
        1: "耗尽",
        2: "攻击武器至少处于25%",
        3: "攻击武器至少处于50%",
        4: "攻击武器至少处于75%",
        5: "攻击武器至少处于100%",
        6: "满载",
        7: "多样",
        8: "未配置"
        }
    m_EMCON_SettingsForRadar = {
        0: "静默",
        1: "激活",
        2: "多样",
        3: "未配置"
        }
    m_EMCON_SettingsForSonar = {
        0: "静默",
        1: "激活",
        2: "多样",
        3: "未配置"
        }
    m_EMCON_SettingsForOECM = {
        0: "静默",
        1: "激活",
        2: "多样",
        3: "未配置"
        }


class CWeatherDict:
    class Info(Enum):
        fSkyCloud = "float 天空云量"
        fRainFallRate = "float 降水量"
        dTemperature = "double 平均气温"
        iSeaState = "int 风力/海力"


class CSideDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        m_PosturesDictionary = "string 获取针对其它推演方的立场"
        fCamerAltitude = "float 中心点相机高度"
        fCenterLatitude = "float 地图中心点纬度"
        fCenterLongitude = "float 地图中心点经度"
        bAIOnly = "bool 推演方非人"
        bCATC = "bool "
        bCollectiveResponsibility = "bool 集体行为"
        iSideStopCount = "int 停止次数"
        iTotalScore = "int 总分"
        m_AwarenessLevel = "int 对敌方的认知级别 (枚举量)"
        m_ContactList = "string 接触的列表"
        m_Doctrine = "string 条令的GUID"
        m_Expenditures = "string 消耗"
        m_Losses = "string 损失"
        m_ProficiencyLevel = "int 熟练等级 (枚举量)"
        m_ScoringLogs = "string 得分记录"
        m_WarDamageOtherTotal = "string "
        strBriefing = "string 想定摘要"
        strCloseResult = "string "
        strFriendlyColorKey = "string 友方颜色"
        strHostileColoryKey = "string 敌方颜色"
        strNeutralColorKey = "string 中立方颜色"
        strSideColorKey = "string 本方颜色"
        strUnFriendlyColorKey = "string 不明方颜色"

    m_AwarenessLevel = {
        -1: "一无所知",
        0: "普通水平",
        1: "知其属方",
        2: "知其属方及单元",
        3: "无所不知无"
        }
    m_ProficiencyLevel = {
        0: "新手",
        1: "实习",
        2: "普通",
        3: "老手",
        4: "顶级"
        }


class CGroupDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        fAltitude_AGL = "float 地理高度"
        iAltitude_ASL = "int 一段时间后的海拔高度"
        m_Side = "string 所在推演方GUID"
        strUnitClass = "string 实体类别"
        dLatitude = "double 当前纬度"
        dLongitude = "double 当前经度"
        fCurrentHeading = "float 当前朝向"
        fCurrentSpeed = "float 当前速度"
        fCurrentAltitude_ASL = "float 当前海拔高度"
        fPitch = "float 倾斜角"
        fRoll = "float 翻转角"
        bIsOnLand = "bool 是否在陆地上"
        fDesiredAltitude = "float 期望高度"
        fDesiredSpeed = "float 期望速度"
        m_MaxThrottle = "int 最大油门 (枚举量)"
        fMaxSpeed = "float 最大速度"
        fMaxAltitude = "float 最大高度"
        fMinAltitude = "float 最小高度"
        fMinSpeed = "float 最小速度"
        fHoverSpeed = "float 悬停"
        fLowSpeed = "float 低速"
        fCruiseSpeed = "float 巡航"
        fMilitarySpeed = "float 军力"
        fAddForceSpeed = "float 加速"
        bIsOperating = "bool 是否在作战中"
        m_DockedUnits = "string 停靠的单元GUID集合"
        m_DockFacilitiesComponent = "string 实体的停靠设施(部件)集合"
        m_DockAircrafts = "string 停靠的飞机的GUID集合"
        m_AirFacilitiesComponent = "string 实体的航空设施(部件)集合 "
        m_CommDevices = "string 实体的通信设备及数据链（部件）"
        m_Engines = "string 实体的引擎（部件）"
        m_Sensors = "string 传感器GUID集合"
        m_Mounts = "string 挂架GUID集合"
        strDamageState = "string 毁伤状态"
        iFireIntensityLevel = "int 失火状态 (枚举量)"
        iFloodingIntensityLevel = "int 进水状态 (枚举量)"
        m_AssignedMission = "string 分配的任务GUID"
        strFuelState = "string 显示燃油信息"
        m_WayPoints = "string 路径点GUID集合"
        m_Doctrine = "string 条令的GUID"
        m_UnitWeapons = "string 系统右栏->对象信息->作战单元武器 内数据"
        strActiveUnitStatus = "string 状态"
        m_ProficiencyLevel = "int 训练水平 (枚举量)"
        bIsEscortRole = "bool 是否是护卫角色"
        m_CurrentThrottle = "int 当前油门 (枚举量)"
        bIsCommsOnLine = "bool 通讯设备是否断开"
        bIsIsolatedPOVObject = "bool 是否视图隔离"
        bTerrainFollowing = "bool 是否地形跟随"
        bIsRegroupNeeded = "bool 是否是领队"
        bHoldPosition = "bool 是否保持阵位"
        bAutoDetectable = "bool 是否可自动探测"
        dFuelPercentage = "double 燃油百分比，作战单元燃油栏第一个进度条的值"
        m_CommLink = "string 单元的通讯链集合"
        m_NoneMCMSensors = "string 传感器GUID集合"
        iDisturbState = "int 显示'干扰'或'被干扰'"
        iMultipleMissionCount = "int 单元所属多个任务数量"
        m_MultipleMissionGUIDs = "string 单元所属多个任务guid集合"
        m_Magazines = "string 弹药库GUID集合"
        m_GroupType = "int 编组类型 (枚举量)"
        m_GroupCenter = "string 编组中心点"
        m_GroupLead = "string 编组领队"
        m_UnitsInGroup = "string 编组所有单元"
        strWayPointName = "string 航路点名称"
        strWayPointDescription = "string 航路点描述"
        WayPointDTG = "string 航路点剩余航行距离"
        WayPointTTG = "string 航路点剩余航行时间"
        WayPointFuel = "string 航路点需要燃油数"
        iFormationSelectedIndex = "int 发送队形方案选择的索引"
        m_FormationFormula = "string 发送队形方案详情"
        strDockAircraft = "string 载机按钮的文本描述"
        strDockShip = "string 载艇按钮的文本描述"

    m_MaxThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    iFireIntensityLevel = {
        0: "无火",
        1: "小火",
        2: "中火",
        3: "猛火",
        4: "大火"
        }
    iFloodingIntensityLevel = {
        0: "未进水",
        1: "少量",
        2: "中等",
        3: "严重",
        4: "翻覆"
        }
    m_ProficiencyLevel = {
        0: "新手",
        1: "实习",
        2: "普通",
        3: "老手",
        4: "顶级"
        }
    m_CurrentThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    m_GroupType = {
        0: "飞机编组",
        1: "水面舰艇编组",
        2: "潜艇编组",
        3: "设施编组",
        4: "车辆编组",
        5: "空军基地",
        6: "海军基地海"
        }


class CSubmarineDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        fAltitude_AGL = "float 地理高度"
        iAltitude_ASL = "int 一段时间后的海拔高度"
        m_Side = "string 所在推演方GUID"
        strUnitClass = "string 实体类别"
        dLatitude = "double 当前纬度"
        dLongitude = "double 当前经度"
        fCurrentHeading = "float 当前朝向"
        fCurrentSpeed = "float 当前速度"
        fCurrentAltitude_ASL = "float 当前海拔高度"
        fPitch = "float 倾斜角"
        fRoll = "float 翻转角"
        fDesiredSpeed = "float 期望速度"
        bDesiredAltitudeOverride = "bool 手动覆盖高度"
        bDesiredSpeedOverride = "bool 手动覆盖速度"
        m_MaxThrottle = "int 最大油门 (枚举量)"
        iDBID = "int DBID"
        bIsOperating = "bool 是否在作战中"
        m_ParentGroup = "string 父级编组GUID"
        m_DockedUnits = "string 停靠的单元GUID集合"
        m_DockFacilitiesComponent = "string 实体的停靠设施(部件)集合"
        m_DockAircrafts = "string 停靠的飞机的GUID集合"
        m_AirFacilitiesComponent = "string 实体的航空设施(部件)集合 "
        m_CommDevices = "string 实体的通信设备及数据链（部件）"
        m_Engines = "string 实体的引擎（部件）"
        m_Sensors = "string 传感器GUID集合"
        m_Mounts = "string 挂架GUID集合"
        strDamageState = "string 毁伤状态"
        iFireIntensityLevel = "int 失火状态 (枚举量)"
        iFloodingIntensityLevel = "int 进水状态 (枚举量)"
        m_AssignedMission = "string 分配的任务GUID"
        fMaxSpeed = "float 最大速度"
        fMinSpeed = "float 最小速度"
        fCurrentAlt = "float 当前高度"
        fDesiredAlt = "float 期望高度"
        fMaxAltitude = "float 最大高度"
        fMinAltitude = "float 最小高度"
        m_WayPoints = "string 路径点GUID集合"
        bAutoDetectable = "bool 是否可自动探测"
        m_Cargo = "string 当前货物"
        dFuelPercentage = "double 燃油百分比"
        m_CommLink = "string 单元的通讯链集合"
        m_NoneMCMSensors = "string 传感器GUID集合"
        iDisturbState = "int 显示'干扰'或'被干扰' (枚举量)"
        iMultipleMissionCount = "int 单元所属多个任务数量"
        m_MultipleMissionGUIDs = "string 单元所属多个任务guid集合"
        m_Magazines = "string 弹药库GUID集合"
        m_Doctrine = "string 条令的GUID"
        m_UnitWeapons = "string 系统右栏->对象信息->作战单元武器 内数据"
        m_HostActiveUnit = "string 配属基地GUID"
        strActiveUnitStatus = "string 状态"
        m_ProficiencyLevel = "int 训练水平 (枚举量)"
        bIsEscortRole = "bool 是否是护卫角色"
        m_CurrentThrottle = "int 当前油门 (枚举量)"
        bIsCommsOnLine = "bool 通讯设备是否断开"
        bIsIsolatedPOVObject = "bool 是否视图隔离"
        bTerrainFollowing = "bool 是否地形跟随"
        bIsRegroupNeeded = "bool 是否是领队"
        bHoldPosition = "bool 是否保持阵位"
        bObeysEMCON = "bool 是否遵守电磁管控 "
        m_BearingType = "int 方位类型 (枚举量)"
        m_Bearing = "float 方位"
        m_Distance = "float 距离（转换为千米）"
        bSprintAndDrift = "bool 高低速交替航行"
        m_AITargets = "string AI对象的目标集合"
        strDockAircraft = "string 载机按钮的文本描述"
        strDockShip = "string 载艇按钮的文本描述"
        m_Category = "int 潜艇类别 (枚举量)"
        m_CIC = "string 指挥部"
        m_Rudder = "string 船舵"
        m_PressureHull = "string 船身"
        strFuelState = "string 显示燃油信息"
        dPercentageDiesel = "double 柴油剩余百分比"
        dPercentageBattery = "double 电池剩余百分比"
        m_Type = "int 潜艇类型 (枚举量)"
        strCavitation = "string 空泡"
        fHoverSpeed = "float 悬停"
        fLowSpeed = "float 低速"
        fCruiseSpeed = "float 巡航"
        fMilitarySpeed = "float 军力"
        fAddForceSpeed = "float 加速"
        iThermoclineUpDepth = "int 温跃层上"
        iThermoclineDownDepth = "int 温跃层下"
        strDamageInfo = "string 毁伤"
        strWeaponInfo = "string 武器"
        strMagazinesInfo = "string 弹药库"
        strFuelInfo = "string 燃料"
        strStatusInfo = "string 状态"
        strTimeToReadyInfo = "string 就绪时间"
        strWayPointName = "string 航路点名称"

    m_MaxThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    iFireIntensityLevel = {
        0: "无火",
        1: "小火",
        2: "中火",
        3: "猛火",
        4: "大火"
        }
    iFloodingIntensityLevel = {
        0: "未进水",
        1: "少量",
        2: "中等",
        3: "严重",
        4: "翻覆"
        }
    iDisturbState = {
        0: "显示干扰",
        1: "显示不干扰示"
        }
    m_ProficiencyLevel = {
        0: "新手",
        1: "实习",
        2: "普通",
        3: "老手",
        4: "顶级"
        }
    m_CurrentThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    m_BearingType = {
        0: "固定的,不随领队朝向变化而变化",
        1: "旋转的,随领队朝向改变旋转改"
        }
    m_Category = {
        1001: "其他",
        2001: "潜艇",
        2002: "生物",
        2003: "假目标"
        }
    m_Type = {
        1001: "其他",
        2001: "辅助/实验潜艇",
        2002: "辅助货运潜艇",
        2003: "攻击/舰队型潜艇",
        2004: "弹道导弹潜艇",
        2005: "弹道导弹核潜艇",
        2006: "导弹攻击型潜艇",
        2007: "核动力导弹攻击型潜艇",
        2008: "猎杀潜艇",
        2009: "小型潜水艇",
        2010: "核动力攻击型潜艇",
        2011: "运输型潜艇",
        2012: "雷达预警潜艇",
        2013: "核动力雷达预警潜艇",
        3001: "蛙人运送艇",
        4001: "远程遥控潜艇",
        4002: "无人潜航器",
        9001: "海洋生物",
        9002: "假目标"
        }


class CShipDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        fAltitude_AGL = "float 地理高度"
        iAltitude_ASL = "int 一段时间后的海拔高度"
        m_Side = "string 所在推演方GUID"
        strUnitClass = "string 实体类别"
        dLatitude = "double 当前纬度"
        dLongitude = "double 当前经度"
        fCurrentHeading = "float 当前朝向"
        fCurrentSpeed = "float 当前速度"
        fCurrentAltitude_ASL = "float 当前海拔高度"
        fPitch = "float 倾斜角"
        fRoll = "float 翻转角"
        fDesiredSpeed = "float 期望速度"
        bDesiredAltitudeOverride = "bool 手动覆盖高度"
        bDesiredSpeedOverride = "bool 手动覆盖速度"
        fMaxAltitude = "float 最大高度"
        fMinAltitude = "float 最小高度"
        iDBID = "int DBID"
        bIsOperating = "bool 是否在作战中"
        m_ParentGroup = "string 父级编组GUID"
        m_DockedUnits = "string 停靠的单元GUID集合"
        m_DockFacilitiesComponent = "string 实体的停靠设施(部件)集合"
        m_DockAircrafts = "string 停靠的飞机的GUID集合"
        m_AirFacilitiesComponent = "string 实体的航空设施(部件)集合 "
        m_CommDevices = "string 实体的通信设备及数据链（部件）"
        m_Engines = "string 实体的引擎（部件）"
        m_Sensors = "string 传感器GUID集合"
        m_Mounts = "string 挂架GUID集合"
        strDamageState = "string 毁伤状态"
        iFireIntensityLevel = "int 失火状态 (枚举量)"
        iFloodingIntensityLevel = "int 进水状态 (枚举量)"
        m_AssignedMission = "string 分配的任务GUID"
        fMaxSpeed = "float 最大速度"
        fMinSpeed = "float 最小速度"
        fCurrentAlt = "float 当前高度"
        fDesiredAlt = "float 期望高度"
        m_MaxThrottle = "int 最大油门 (枚举量)"
        m_WayPoints = "string 路径点GUID集合"
        m_Doctrine = "string 条令的GUID"
        m_UnitWeapons = "string 系统右栏->对象信息->作战单元武器 内数据"
        m_HostActiveUnit = "string 配属基地GUID"
        strActiveUnitStatus = "string 状态"
        m_ProficiencyLevel = "int 训练水平 (枚举量)"
        bIsEscortRole = "bool 是否是护卫角色"
        m_CurrentThrottle = "int 当前油门 (枚举量)"
        bIsCommsOnLine = "bool 通讯设备是否断开"
        bIsIsolatedPOVObject = "bool 是否视图隔离"
        bTerrainFollowing = "bool 是否地形跟随"
        bIsRegroupNeeded = "bool 是否是领队"
        bHoldPosition = "bool 是否保持阵位"
        bAutoDetectable = "bool 是否可自动探测"
        bObeysEMCON = "bool 是否遵守电磁管控 "
        m_Cargo = "string 当前货物"
        dFuelPercentage = "double 燃油百分比"
        m_AITargets = "string AI对象的目标集合"
        m_CommLink = "string 单元的通讯链集合"
        m_NoneMCMSensors = "string 传感器GUID集合"
        iDisturbState = "int 显示'干扰'或'被干扰' (枚举量)"
        iMultipleMissionCount = "int 单元所属多个任务数量"
        m_MultipleMissionGUIDs = "string 单元所属多个任务guid集合"
        m_Magazines = "string 弹药库GUID集合"
        strDockAircraft = "string 载机按钮的文本描述"
        strDockShip = "string 载艇按钮的文本描述"
        m_BearingType = "int 方位类型 (枚举量)"
        m_Bearing = "float 方位"
        m_Distance = "float 距离（转换为千米）"
        bSprintAndDrift = "bool 高低速交替航行"
        m_Category = "int 类别 (枚举量)"
        m_CommandPost = "string 指挥部"
        m_Rudder = "string 船舵"
        strFuelState = "string 显示燃油信息"
        m_Type = "int 船的子类型 (枚举量)"
        strCavitation = "string 空泡"
        fHoverSpeed = "float 悬停"
        fLowSpeed = "float 低速"
        fCruiseSpeed = "float 巡航"
        fMilitarySpeed = "float 军力"
        fAddForceSpeed = "float 加速"
        strDamageInfo = "string 毁伤"
        strWeaponInfo = "string 武器"
        strMagazinesInfo = "string 弹药库"
        strFuelInfo = "string 燃料"
        strStatusInfo = "string 状态"
        strTimeToReadyInfo = "string 就绪时间"
        strWayPointName = "string 航路点名称"
        m_CargoType = "int 货物类型 (枚举量)"
        bCanRefuelOrUNREP = "bool "
        strShowTankerHeader = "string 补给队列header"
        m_ShowTanker = "string 补给队列"

    iFireIntensityLevel = {
        0: "无火",
        1: "小火",
        2: "中火",
        3: "猛火",
        4: "大火"
        }
    iFloodingIntensityLevel = {
        0: "未进水",
        1: "少量",
        2: "中等",
        3: "严重",
        4: "翻覆"
        }
    m_MaxThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    m_ProficiencyLevel = {
        0: "新手",
        1: "实习",
        2: "普通",
        3: "老手",
        4: "顶级"
        }
    m_CurrentThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    iDisturbState = {
        0: "显示干扰",
        1: "显示不干扰示"
        }
    m_BearingType = {
        0: "固定的,不随领队朝向变化而变化",
        1: "旋转的,随领队朝向改变旋转改"
        }
    m_Category = {
        1001: "未知",
        2001: "航空母舰",
        2002: "水面战斗舰艇",
        2003: "两栖舰艇",
        2004: "辅助舰艇",
        2005: "商船",
        2006: "民用船",
        2007: "水面战斗舰艇（航空能力）",
        2008: "移动海上基地（航空能力）空"
        }
    m_Type = {
        1001: "其他",
        2001: "航空母舰",
        2002: "攻击型航空母舰",
        2003: "大型航空母舰",
        2004: "护航航空母舰",
        2005: "导弹直升机航母",
        2006: "直升机航母",
        2007: "轻型航空母舰",
        2008: "核动力航空母舰",
        2009: "水上飞机母舰",
        2010: "反潜航空母舰",
        3001: "战列舰",
        3002: "战列舰",
        3003: "指挥战列舰",
        3004: "导弹战列舰",
        3005: "直升机战列舰",
        3006: "核动力导弹战列巡洋舰",
        3007: "小型浅水重炮舰",
        3101: "巡洋舰",
        3102: "重型巡洋舰",
        3103: "重型导弹巡洋舰",
        3104: "大型巡洋舰",
        3105: "大型导弹巡洋舰",
        3106: "导弹巡洋舰",
        3107: "导弹直升机巡洋舰",
        3108: "核动力导弹巡洋舰",
        3109: "轻型巡洋舰",
        3110: "轻型防空巡洋舰",
        3111: "轻型指挥巡洋舰",
        3112: "轻型导弹巡洋舰",
        3113: "轻型直升机巡洋舰",
        3114: "侦查巡洋舰",
        3201: "驱逐舰",
        3202: "驱逐舰",
        3203: "导弹驱逐舰",
        3204: "直升机驱逐舰",
        3205: "反潜艇驱逐舰",
        3206: "雷达警戒驱逐舰",
        3207: "护航驱逐舰",
        3208: "导弹护航驱逐舰",
        3209: "雷达警戒护航驱逐舰",
        3210: "驱逐舰",
        3211: "导弹驱逐舰",
        3212: "布雷驱逐舰（改装自驱逐舰）",
        3301: "护卫舰",
        3302: "护卫舰",
        3303: "导弹护卫舰",
        3304: "轻型护卫舰",
        3305: "巡逻护卫舰",
        3306: "濒海战斗舰",
        3307: "海洋巡逻艇",
        3401: "巡逻艇",
        3402: "海岸巡逻艇",
        3403: "猎潜艇",
        3404: "猎潜护航艇",
        3405: "快速巡逻艇",
        3406: "快速导弹巡逻艇",
        3407: "巡逻舰",
        3408: "轻型护卫舰",
        3409: "导弹炮舰",
        3410: "水翼炮艇",
        3411: "导弹水翼船",
        3412: "水翼鱼雷快艇",
        3413: "巡逻鱼雷艇",
        3414: "小型鱼雷巡逻艇",
        3415: "鱼雷摩托艇",
        3416: "海岸警卫队高续航快艇",
        3417: "海岸警卫队中续航快艇",
        3418: "海岸警卫队巡逻船",
        3419: "海岸警卫队巡逻炮艇",
        3420: "海事海防船",
        4000: "指挥舰",
        4001: "两栖舰队旗舰",
        4002: "气垫登陆艇",
        4003: "两栖指挥舰",
        4004: "机械化登陆艇",
        4005: "人员登陆艇",
        4006: "坦克登陆艇",
        4007: "通用登陆艇",
        4008: "车辆及人员登陆艇",
        4009: "近岸火力支援船",
        4010: "通用两栖攻击舰",
        4011: "多用途两栖攻击舰",
        4012: "两栖货舰",
        4013: "两栖船坞运输舰",
        4014: "两栖攻击直升机航母",
        4015: "船坞登陆舰",
        4016: "未知！英国型号！",
        4017: "后勤登陆舰",
        4018: "中型登陆舰",
        4019: "中型火箭登陆舰",
        4020: "坦克登陆舰",
        4021: "通用登陆舰",
        4022: "车辆登陆舰",
        4023: "步兵登陆舰",
        4024: "半潜水快艇",
        4025: "气垫式人员登陆舰",
        4026: "远征快速运输舰",
        4027: "远征转运码头舰",
        4028: "远征移动基地舰",
        5001: "辅助船",
        5002: "驱逐舰供应舰",
        5003: "弹药船",
        5004: "冷藏储运船",
        5005: "军需品储运船",
        5006: "通用辅助船",
        5007: "重型破冰船",
        5008: "指挥舰",
        5009: "情报收集舰",
        5010: "通信中继船",
        5011: "海洋科学考察船",
        5012: "海洋监测船",
        5013: "雷达警戒（改装自货船）",
        5014: "测量船",
        5015: "技术考察船",
        5016: "医疗船",
        5017: "货船",
        5018: "武装货船",
        5019: "干货船",
        5020: "滚装船",
        5021: "通用存运船",
        5022: "舰队油船",
        5023: "快速战斗支援舰",
        5024: "小型油船",
        5025: "补给油船",
        5026: "运油船",
        5027: "攻击型人员运输舰",
        5028: "运兵船（高速）",
        5029: "修理船",
        5030: "潜艇供应舰",
        5031: "武装运兵船 (靶船)",
        5032: "辅助远洋拖船",
        5033: "救助拖船",
        5034: "水上飞机供应舰",
        5035: "训练舰",
        5036: "潜艇救援舰",
        5037: "人员运输舰",
        5038: "潜水支援船/深潜车",
        5039: "导弹射程测量船",
        5101: "MSC (军事海运司令部) 海洋监测船",
        5102: "MSC (军事海运司令部) 医疗船",
        5103: "MSC (军事海运司令部)货船",
        5104: "MSC (军事海运司令部) 干货船",
        5105: "MSC (军事海运司令部) 滚装船",
        5106: "MSC (军事海运司令部) 舰队油船",
        5107: "MSC (军事海运司令部) 运油船",
        5108: "MSC (军事海运司令部) 移动登陆平台",
        6001: "反水雷无人机",
        6002: "反水雷舰",
        6003: "反水雷支援舰",
        6004: "沿岸猎雷艇",
        6005: "布雷艇",
        6006: "沿海扫雷舰",
        6007: "钢壳舰队扫雷舰",
        6008: "近岸扫雷舰",
        6010: "远洋扫雷舰",
        6011: "扫雷舰支援舰",
        6012: "近岸猎雷舰",
        6013: "雷区养护舰",
        7001: "各类勤务船",
        9001: "民用船只",
        9002: "贸易船只",
        9003: "平底驳船/海上钻井平台",
        9004: "NGS (美国国家大地测量局) Buoy",
        9005: "底部固定阵列声纳",
        9006: "系泊声纳浮标",
        9007: "特殊（地面单位/卫星）",
        9011: "移动式近海基地"

        }
    m_CargoType = {
        0: "不可以编辑货物",
        1000: "人员",
        2000: "小型货物",
        3000: "中型货物",
        4000: "大型货物",
        5000: "超大型货物大"
        }


class CFacilityDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        fAltitude_AGL = "float 地理高度"
        iAltitude_ASL = "int 一段时间后的海拔高度"
        bDesiredAltitudeOverride = "bool 手动覆盖高度"
        bDesiredSpeedOverride = "bool 手动覆盖速度"
        m_Side = "string 所在推演方GUID"
        strUnitClass = "string 实体类别"
        dLatitude = "double 当前纬度"
        dLongitude = "double 当前经度"
        fCurrentHeading = "float 当前朝向"
        fCurrentSpeed = "float 当前速度"
        fCurrentAltitude_ASL = "float 当前海拔高度"
        fPitch = "float 倾斜角"
        fRoll = "float 翻转角"
        fDesiredSpeed = "float 期望速度"
        iDBID = "int 数据库ID"
        bIsOperating = "bool 是否在作战中"
        m_ParentGroup = "string 父级编组GUID"
        m_DockedUnits = "string 停靠的单元GUID集合"
        m_DockFacilitiesComponent = "string 实体的停靠设施(部件)集合"
        m_DockAircrafts = "string 停靠的飞机的GUID集合"
        m_AirFacilitiesComponent = "string 实体的航空设施(部件)集合 "
        m_CommDevices = "string 实体的通信设备及数据链（部件）"
        m_Engines = "string 实体的引擎（部件）"
        m_Sensors = "string 传感器GUID集合"
        m_Mounts = "string 挂架GUID集合"
        strDamageState = "string 毁伤状态"
        iFireIntensityLevel = "int 失火状态 (枚举量)"
        iFloodingIntensityLevel = "int 进水状态 (枚举量)"
        fMaxSpeed = "float 最大速度"
        fMinSpeed = "float 最小速度"
        fCurrentAlt = "float 当前高度"
        fDesiredAlt = "float 期望高度"
        fMaxAltitude = "float 最大高度"
        fMinAltitude = "float 最小高度"
        m_MaxThrottle = "int 最大油门 (枚举量)"
        m_WayPoints = "string 路径点GUID集合"
        m_Doctrine = "string 条令的GUID"
        m_AssignedMission = "string 分配的任务GUID"
        m_UnitWeapons = "string 系统右栏->对象信息->作战单元武器 内数据"
        m_HostActiveUnit = "string 配属基地GUID"
        strActiveUnitStatus = "string 状态"
        m_ProficiencyLevel = "int 训练水平 (枚举量)"
        bIsEscortRole = "bool 是否是护卫角色"
        m_CurrentThrottle = "int 当前油门 (枚举量)"
        bIsCommsOnLine = "bool 通讯设备是否断开"
        bIsIsolatedPOVObject = "bool 是否视图隔离"
        bTerrainFollowing = "bool 是否地形跟随"
        bIsRegroupNeeded = "bool 是否是领队"
        bHoldPosition = "bool 是否保持阵位"
        bAutoDetectable = "bool 是否可自动探测"
        m_BearingType = "int 方位类型 (枚举量)"
        m_Bearing = "float 方位"
        m_Distance = "float 距离（转换为千米）"
        bSprintAndDrift = "bool 高低速交替航行"
        m_Cargo = "string 当前货物"
        dFuelPercentage = "double 燃油百分比"
        m_AITargets = "string AI对象的目标集合"
        bDockingOpsHasPier = "bool 停靠参数是否包含码头"
        m_CommLink = "string 单元的通讯链集合"
        m_NoneMCMSensors = "string 传感器GUID集合"
        iDisturbState = "int 显示'干扰'或'被干扰' (枚举量)"
        iMultipleMissionCount = "int 单元所属多个任务数量"
        m_MultipleMissionGUIDs = "string 单元所属多个任务guid集合"
        m_Magazines = "string 弹药库GUID集合"
        strDockAircraft = "string 载机按钮的文本描述"
        strDockShip = "string 载艇按钮的文本描述"
        m_Category = "int 类别 (枚举量)"
        m_CommandPost = "string 战情中心"
        fHoverSpeed = "float 悬停"
        fLowSpeed = "float 低速"
        fCruiseSpeed = "float 巡航"
        fMilitarySpeed = "float 军力"
        fAddForceSpeed = "float 加速"

    iFireIntensityLevel = {
        0: "无火",
        1: "小火",
        2: "中火",
        3: "猛火",
        4: "大火"
        }
    iFloodingIntensityLevel = {
        0: "未进水",
        1: "少量",
        2: "中等",
        3: "严重",
        4: "翻覆"
        }
    m_MaxThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    m_ProficiencyLevel = {
        0: "新手",
        1: "实习",
        2: "普通",
        3: "老手",
        4: "顶级"
        }
    m_CurrentThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    iDisturbState = {
        0: "显示干扰",
        1: "显示不干扰示"
        }
    m_BearingType = {
        0: "固定的,不随领队朝向变化而变化",
        1: "旋转的,随领队朝向改变旋转改"
        }
    m_Category = {
        1001: "其他",
        2001: "跑道",
        2002: "滑行道",
        2003: "跑道入口",
        3001: " 建筑物（地表）",
        3002: "建筑物（混凝土）",
        3003: "建筑物（地堡）",
        3004: "建筑物（地下）",
        3005: "建筑结构（开放）",
        3006: "建筑结构（混凝土）",
        4001: "水下",
        5001: "移动车辆",
        5002: "移动人员",
        6001: "航空器系泊设备",
        9001: "空军基地"
        }


class CAircraftDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        fAltitude_AGL = "float 地理高度"
        iAltitude_ASL = "int 一段时间后的海拔高度"
        m_Side = "string 所在推演方GUID"
        strUnitClass = "string 实体类别"
        dLatitude = "double 当前纬度"
        dLongitude = "double 当前经度"
        fCurrentHeading = "float 当前朝向"
        fCurrentSpeed = "float 当前速度"
        fCurrentAltitude_ASL = "float 当前海拔高度"
        fPitch = "float 倾斜角"
        fRoll = "float 翻转角"
        fDesiredAltitude = "float 期望高度"
        fDesiredSpeed = "float 期望速度"
        m_MaxThrottle = "int 最大油门 (枚举量)"
        fMaxSpeed = "float 最大速度"
        fMinSpeed = "float 最小速度"
        fCurrentAlt = "float 当前高度"
        fDesiredAlt = "float 期望高度"
        bDesiredAltitudeOverride = "bool 手动覆盖高度"
        bDesiredSpeedOverride = "bool 手动覆盖速度"
        fMaxAltitude = "float 最大高度"
        fMinAltitude = "float 最小高度"
        iDBID = "int DBID"
        bIsOperating = "bool 是否在作战中"
        m_ParentGroup = "string 父级编组GUID"
        m_DockedUnits = "string 停靠的单元GUID集合"
        m_DockFacilitiesComponent = "string 实体的停靠设施(部件)集合"
        m_DockAircrafts = "string 停靠的飞机的GUID集合"
        m_AirFacilitiesComponent = "string 实体的航空设施(部件)集合 "
        m_CommDevices = "string 实体的通信设备及数据链（部件）"
        m_Engines = "string 实体的引擎（部件）"
        m_Sensors = "string 传感器GUID集合"
        m_Mounts = "string 挂架GUID集合"
        strDamageState = "string 毁伤状态"
        iFireIntensityLevel = "int 失火状态 (枚举量)"
        iFloodingIntensityLevel = "int 进水状态 (枚举量)"
        m_AssignedMission = "string 分配的任务GUID"
        m_Doctrine = "string 条令的GUID"
        m_UnitWeapons = "string 系统右栏->对象信息->作战单元武器 内数据"
        m_HostActiveUnit = "string 配属基地GUID"
        strActiveUnitStatus = "string 飞机状态"
        strFuelState = "string 显示燃油信息"
        m_WayPoints = "string 路径点GUID集合"
        m_ProficiencyLevel = "int 训练水平 (枚举量)"
        bIsEscortRole = "bool 是否是护卫角色"
        m_CurrentThrottle = "int 当前油门 (枚举量)"
        bIsCommsOnLine = "bool 通讯设备是否断开"
        bIsIsolatedPOVObject = "bool 是否视图隔离"
        bTerrainFollowing = "bool 是否地形跟随"
        bIsRegroupNeeded = "bool 是否是领队"
        bHoldPosition = "bool 是否保持阵位"
        bAutoDetectable = "bool 是否可自动探测"
        m_Cargo = "string 当前货物"
        dFuelPercentage = "double 燃油百分比"
        m_AITargets = "string AI对象的目标集合"
        m_CommLink = "string 单元的通讯链集合"
        m_NoneMCMSensors = "string 传感器GUID集合"
        iDisturbState = "int 显示'干扰'或'被干扰' (枚举量)"
        iMultipleMissionCount = "int 单元所属多个任务数量"
        m_MultipleMissionGUIDs = "string 单元所属多个任务guid集合"
        m_Magazines = "string 弹药库GUID集合"
        bObeysEMCON = "bool 是否遵守电磁管控 "
        m_BearingType = "int 方位类型 (枚举量)"
        m_Bearing = "float 方位"
        m_Distance = "float 距离（转换为千米）"
        bSprintAndDrift = "bool 高低速交替航行"
        strDockAircraft = "string 载机按钮的文本描述"
        m_Category = "int 类别 (枚举量)"
        m_Type = "int 类型 (枚举量)"
        m_CurrentHostUnit = "string 宿主单元对象"
        iLoadoutDBID = "int 挂载方案的DBID"
        m_LoadoutGuid = "string 挂载方案的GUID"
        strAirOpsConditionString = "int 当前行动状态 (枚举量)"
        strFinishPrepareTime = "float 完成准备时间"
        strQuickTurnAroundInfo = "string 快速出动信息"
        fHoverSpeed = "float 悬停"
        fLowSpeed = "float 低速"
        fCruiseSpeed = "float 巡航"
        fMilitarySpeed = "float 军力"
        fAddForceSpeed = "float 加速"
        m_MaintenanceLevel = "int 维护状态 (枚举量)"
        fFuelConsumptionCruise = "float 指定工作高度的燃料消耗速度"
        fAbnTime = "float 滞空时间"
        iFuelRecsMaxQuantity = "int 各种燃料的最大数量之和"
        iCurrentFuelQuantity = "int 当前油量"
        bQuickTurnaround_Enabled = "bool 是否快速出动"
        bIsAirRefuelingCapable = "bool 是否有空中加油能力"
        strShowTankerHeader = "string 加油队列header"
        m_ShowTanker = "string 加油队列明细"
        m_bProbeRefuelling = "bool 是否可受油探管加油"
        m_bBoomRefuelling = "bool 是否可输油管加油"
        strWayPointName = "string 航路点名称"
        strWayPointDescription = "string 航路点描述"
        WayPointDTG = "string 航路点剩余航行距离"
        WayPointTTG = "string 航路点剩余航行时间"
        WayPointFuel = "string 航路点需要燃油数"

    iFireIntensityLevel = {
        0: "无火",
        1: "小火",
        2: "中火",
        3: "猛火",
        4: "大火"
        }
    iFloodingIntensityLevel = {
        0: "未进水",
        1: "少量",
        2: "中等",
        3: "严重",
        4: "翻覆"
        }
    m_MaxThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    m_ProficiencyLevel = {
        0: "新手",
        1: "实习",
        2: "普通",
        3: "老手",
        4: "顶级"
        }
    m_CurrentThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    iDisturbState = {
        0: "显示干扰",
        1: "显示不干扰示"
        }
    m_BearingType = {
        0: "固定的,不随领队朝向变化而变化",
        1: "旋转的,随领队朝向改变旋转改"
        }
    m_Category = {
        1001: "未知",
        2001: "固定翼",
        2002: "固定翼舰载机",
        2003: "直升机",
        2004: "倾转旋翼机",
        2006: "飞艇",
        2007: "水上飞机",
        2008: "两栖飞机"
        }
    m_Type = {
        1001: "其他",
        2001: "战斗机",
        2002: "多用途飞机",
        2101: "反卫星飞机",
        2102: "空中激光平台",
        3001: "攻击机",
        3002: "野鼬鼠 （防空压制）",
        3101: "轰炸机",
        3401: "战场空中拦截（BAI/ CAS）",
        4001: "电子战飞机",
        4002: "预警机",
        4003: "指挥机 （ACP）",
        4101: "救援飞机",
        4201: "反水雷飞机",
        6001: "反潜作战飞机",
        6002: "海上巡逻机",
        7001: "前进观察员",
        7002: "区域监视",
        7003: "侦察机",
        7004: "电子情报收集飞机",
        7005: "信号情报收集飞机",
        7101: "运输机",
        7201: "货机",
        7301: "商业飞机",
        7302: "民用",
        7401: "通用直升机",
        7402: "海军通用直升机",
        8001: "空中加油机",
        8101: "教练机",
        8102: "牵引机",
        8103: "靶机",
        8201: "无人机",
        8202: "无人作战飞行器",
        8901: "飞艇",
        8902: "航空器",
        9001: "0x0400204A RID:'8266'",
        9002: "航天飞机",
        9003: "0x0400204C RID:'8268'",
        9004: "自杀式无人机"
        }
    strAirOpsConditionString = {
        0: "空中",
        1: "停泊",
        2: "正在滑行准备起飞",
        3: "正在滑行到停机位",
        4: "正在起飞过程中",
        5: "最终进场",
        6: "正在完成降落",
        7: "正在进行出动准备",
        8: "等待可用的滑行道/升降机",
        9: "等待跑道空闲",
        10: "处于降落队列中",
        11: "返回基地",
        12: "准备出动",
        13: "机动到加油阵位",
        14: "正在加油",
        15: "卸载燃油",
        16: "准备部署吊放式声纳:尚未到达部署点",
        17: "紧急着陆",
        18: "到飞行甲板",
        19: "正在执行超视距攻击任务",
        20: "超视距攻击往复运动？远距离攻击往复运动？",
        21: "近距空中格斗",
        22: "投送货物",
        23: "滑行至加油区",
        24: "滑行",
        25: "通过跑道滑行降落（用于演示功能）",
        26: "通过跑道滑行起飞（用于演示功能）"
        }
    m_MaintenanceLevel = {
        0: "武器状态未知,或不考虑连发机关枪",
        1: "武器状态已知,且考虑连发机关枪",
        2: "不可用",
        3: "备用挂载方案",
        4: "没有挂载方案"
        }


class CSatelliteDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        fAltitude_AGL = "float 地理高度"
        iAltitude_ASL = "int 一段时间后的海拔高度"
        m_Side = "string 所在推演方GUID"
        strUnitClass = "string 实体类别"
        dLatitude = "double 当前纬度"
        dLongitude = "double 当前经度"
        fCurrentHeading = "float 当前朝向"
        fCurrentSpeed = "float 当前速度"
        fCurrentAltitude_ASL = "float 当前海拔高度"
        fPitch = "float 倾斜角"
        fRoll = "float 翻转角"
        iDBID = "int 数据库ID"
        bIsOperating = "bool 是否在作战中"
        m_ParentGroup = "string 编组GUID"
        m_DockedUnits = "string 停靠的设施的ID(关系)"
        m_DockFacilitiesComponent = "string 实体的停靠设施(部件)"
        m_DockAircrafts = "string 停靠的飞机的ID(关系)"
        m_AirFacilitiesComponent = "string 实体的航空设施(部件)  "
        m_CommDevices = "string  实体的通信设备及数据链（部件）  "
        m_Engines = "string 实体的引擎（部件）"
        m_Sensors = "string 传感器GUID集合"
        m_Mounts = "string 挂架 GUID集合"
        strDamageState = "string 毁伤状态"
        iFireIntensityLevel = "int 失火 (枚举量)"
        iFloodingIntensityLevel = "int 进水 (枚举量)"
        m_AssignedMission = "string 分配的任务"
        fMinSpeed = "float 最小速度"
        fMaxSpeed = "float 最大速度"
        fCurrentAlt = "float 当前高度"
        fDesiredAlt = "float 期望高度"
        fMaxAltitude = "float 最大高度"
        fMinAltitude = "float 最小高度"
        m_MaxThrottle = "int 最大油门 (枚举量)"
        m_WayPoints = "string 路径点"
        m_Doctrine = "string 作战条令"
        m_UnitWeapons = "string 系统右栏->对象信息->作战单元武器 "
        m_HostActiveUnit = "string 配属基地"
        strActiveUnitStatus = "string 状态"
        m_ProficiencyLevel = "int 训练水平 (枚举量)"
        bIsEscortRole = "bool 是否是护卫角色"
        m_CurrentThrottle = "int 当前油门 (枚举量)"
        bIsCommsOnLine = "bool 通讯设备是否断开"
        bIsIsolatedPOVObject = "bool 是否视图隔离"
        bTerrainFollowing = "bool 是否地形跟随"
        bIsRegroupNeeded = "bool 是否是领队"
        bHoldPosition = "bool 是否保持阵位"
        bAutoDetectable = "bool 是否可自动探测"
        bObeysEMCON = "bool 是否遵守电磁管控"
        dFuelPercentage = "double 燃油百分比"
        m_AITargets = "string AI对象的目标集合"
        m_CommLink = "string 单元的通讯链集合"
        m_NoneMCMSensors = "string 传感器GUID集合"
        iDisturbState = "int 显示'干扰'或'被干扰' (枚举量)"
        iMultipleMissionCount = "int 单元所属多个任务数量"
        m_MultipleMissionGUIDs = "string 单元所属多个任务guid集合"
        m_Magazines = "string 弹药库GUID集合"
        m_SatelliteCategory = "int 卫星类型"
        m_TracksPoints = "string 卫星航迹线"

    iFireIntensityLevel = {
        0: "无火",
        1: "小火",
        2: "中火",
        3: "猛火",
        4: "大火"
        }
    iFloodingIntensityLevel = {
        0: "未进水",
        1: "少量",
        2: "中等",
        3: "严重",
        4: "翻覆"
        }
    m_MaxThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    m_ProficiencyLevel = {
        0: "新手",
        1: "实习",
        2: "普通",
        3: "老手",
        4: "顶级"
        }
    m_CurrentThrottle = {
        0: "完全停止",
        1: "原地徘徊",
        2: "巡航",
        3: "全速",
        4: "军用",
        5: "滑行"
        }
    iDisturbState = {
        0: "显示干扰",
        1: "显示不干扰示"
        }
    m_SatelliteCategory = {
        1001: "未知",
        2001: "地球同步卫星"
        }


class CSensorDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        iDBID = "int 数据库中的DBID"
        m_ParentPlatform = "string 所属单元GUID"
        m_ComponentStatus = "int 部件状态 (枚举量)"
        m_DamageSeverity = "int 毁伤程度的轻,中,重 (枚举量)"
        m_CoverageArc = "string 挂载方位"
        bActive = "bool 是否开机"
        strDescription = "string 传感器类型"
        strWorkStatus = "string 传感器工作状态"
        m_SensorType = "int 传感器类型 (枚举量)"
        m_SensorRole = "long 传感器角色"
        fMaxRange = "float 最大探测距离"
        fMinRange = "float 最小探测距离"
        i_TrackingTargetsWhenUsedAsDirector = "int 当传感器用作武器指示器时，正在跟踪照射的目标列表数量"
        m_TrackingTargetsWhenUsedAsDirector = "string 当传感器用作武器指示器时，正在跟踪照射的目标列表集合"
        m_SensorCapability = "string 传感器能力"

    m_ComponentStatus = {
        0: "正常工作",
        1: "受到毁伤",
        2: "已被摧毁"
        }

    m_DamageSeverity = {
        0: "轻",
        1: "中",
        2: "重"
        }

    m_SensorType = {
        1001: "未知",
        2001: "雷达",
        2002: "半主动",
        2003: "光学",
        2004: "红外",
        2005: "通过导弹跟踪",
        3001: "电子支援",
        3002: "电子干扰",
        3003: "GPS干扰",
        3004: "烟雾干扰",
        4001: "激光指示",
        4002: "激光光斑跟踪器",
        4003: "激光测距",
        5001: "船体被动声呐",
        5002: "船体主被动声呐",
        5003: "船体主动声呐",
        5011: "被动拖曳阵列",
        5012: "主被动拖曳阵列",
        5013: "主动拖曳阵列",
        5021: "可变深度被动声呐",
        5022: "可变深度主被动声呐",
        5023: "可变深度主动声呐",
        5031: "投吊式被动声呐",
        5032: "投吊式主被动声呐",
        5033: "投吊式主动声呐",
        5041: "海底固定被动声呐",
        5101: "磁异常",
        5901: "回声拦截(主动声呐告警)",
        6001: "水雷扫描，机械式铁索剪",
        6002: "T水雷扫描，磁场作用",
        6003: "水雷扫描，声场作用",
        6004: "水雷扫描，磁场 & 声场共同作用",
        6011: "水雷扫描，双船磁场作用",
        6021: "可对系泊雷进行切割",
        6022: "水雷中性化，爆破式水雷处理",
        6031: "水雷中性化，潜水员爆破炸药部署",
        9001: "传感器组"
        }


class CLoadoutDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        idbid = "int 数据库ID"
        strLoadWeaponCount = "string 挂载的武器的数量"
        m_LoadRatio = "string 挂载的数量和挂架载荷"
        m_AircraftGuid = "string 飞机的guid"
        bQuickTurnaround = "bool 是否支持快速出动"
        iMaxSorties = "int 最大飞行波次"
        m_CargoType = "int 货物类型 (枚举量)"

    m_CargoType = {
        0: "不可以编辑货物",
        1000: "人员",
        2000: "小型货物",
        3000: "中型货物",
        4000: "大型货物",
        5000: "超大型货物"
        }


class CMountDict:
    class Info(Enum):
        strName = "string 挂架名称"
        strGuid = "string 挂架GUID"
        iDBID = "int 数据库中的DBID"
        m_ParentPlatform = "string 父平台GUID"
        m_ComponentStatus = "int 部件状态 (枚举量)"
        m_DamageSeverity = "int 毁伤程度的轻,中,重 (枚举量)"
        m_CoverageArc = "string 挂载方位"
        strWeaponFireState = "string 挂载的武器开火状态"
        strLoadWeaponCount = "string 挂载的武器的数量"
        m_LoadRatio = "string 获取挂架下武器的最大载弹量和当前载弹量集合"
        m_Sensors = "string 传感器GUID集合"
        m_ReloadPrioritySet = "string 重新装载优先级选中的武器DBID集合"

    m_ComponentStatus = {
        0: "正常工作",
        1: "受到毁伤",
        2: "已被摧毁"
        }
    m_DamageSeverity = {
        0: "轻",
        1: "中",
        2: "重"
        }


class CMagazineDict:
    class Info(Enum):
        strName = "string 弹药库名称"
        strGuid = "string 弹药库GUID"
        Idbid = "int 数据库中的DBID"
        m_ParentPlatform = "string 父平台guid"
        m_ComponentStatus = "int 状态 (枚举量)"
        m_DamageSeverity = "int 毁伤程度的轻,中,重 (枚举量)"
        m_CoverageArc = "string 覆盖角度"
        m_LoadRatio = "string 挂架已挂载的数量和挂架载荷"

    m_ComponentStatus = {
        0: "正常工作",
        1: "受到毁伤",
        2: "已被摧毁"
        }
    m_DamageSeverity = {
        0: "轻",
        1: "中",
        2: "重"
        }


class CWeaponDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        fAltitude_AGL = "float 地理高度"
        iAltitude_ASL = "int 一段时间后的海拔高度"
        m_Side = "string 所在推演方GUID"
        strUnitClass = "string 实体类别"
        dLatitude = "double 当前纬度"
        dLongitude = "double 当前经度"
        fCurrentHeading = "float 当前朝向"
        fCurrentSpeed = "float 当前速度"
        fCurrentAltitude_ASL = "float 当前海拔高度"
        fPitch = "float 倾斜角"
        fRoll = "float 翻转角"
        iDBID = "int DBID"
        bIsOperating = "bool 是否在作战中"
        m_ParentGroup = "string 父级编组GUID"
        m_CommDevices = "string 实体的通信设备及数据链（部件）"
        m_Engines = "string 实体的引擎（部件）"
        m_strDataLinkParentGuid = "string 提供数据链的活动单元GUID"
        m_Sensors = "string 传感器GUID集合"
        m_Mounts = "string 挂架GUID集合"
        m_ParentMount = "string 父挂架的GUID"
        m_ParentMagazine = "string 父弹药库的GUID"
        strDamageState = "string 毁伤状态"
        iFireIntensityLevel = "int 失火状态 (枚举量)"
        iFloodingIntensityLevel = "int 进水状态 (枚举量)"
        m_AssignedMission = "string 分配的任务GUID"
        fMaxAltitude = "float 最大高度"
        fMinAltitude = "float 最小高度"
        m_MaxThrottle = "int 最大油门"
        m_Doctrine = "string 条令的GUID"
        m_HostActiveUnit = "string 配属基地GUID"
        bIsEscortRole = "bool 是否是护卫角色"
        m_CurrentThrottle = "int 当前油门"
        bIsCommsOnLine = "bool 通讯设备是否断开"
        bIsIsolatedPOVObject = "bool 是否视图隔离"
        bTerrainFollowing = "bool 是否地形跟随"
        bIsRegroupNeeded = "bool 是否是领队"
        bHoldPosition = "bool 是否保持阵位"
        m_PrimaryTargetGuid = "string 主要目标"
        m_WayPoints = "string 路径点"
        bAutoDetectable = "bool 是否可自动探测"
        dFuelPercentage = "double 燃油百分比"
        m_CommLink = "string 单元的通讯链集合"
        m_NoneMCMSensors = "string 传感器GUID集合"
        iDisturbState = "int 显示'干扰'或'被干扰' (枚举量)"
        iMultipleMissionCount = "int 单元所属多个任务数量"
        m_MultipleMissionGUIDs = "string 单元所属多个任务guid集合"
        fRangeASWMin = "float 反潜模式使用时最小作用距离"
        fRangeASWMax = "float 反潜模式使用时最大作用距离"
        fRangeLandMin = "float 最小射程"
        fRangeLandMax = "float 最大射程"
        fRangeASUWMin = "float 反舰模式使用时最小距离"
        fRangeASUWMax = "float 反舰模式使用时最大距离"
        fRangeAAWMin = "float 防空作战最小大作用距离"
        fRangeAAWMax = "float 防空作战最大作用距离"
        m_WeaponType = "int 武器类型 (枚举量)"
        m_WeaponTargetType = "string 打击的目标类型"
        m_SonobuoyDepthSetting = "int 声呐深度设置"
        bIsOfAirLaunchedGuidedWeapon = "bool 是否是空射制导武器"
        bSonobuoyActive = "bool 是否是主动声纳"
        m_FiringUnitGuid = "string 发射单元GUID"
        m_AITargets = "string 获取AI对象的目标集合"
        strSonobuoyRemainingTime = "string 如果是声纳浮标则发送它的剩余时间"

    iFireIntensityLevel = {
        0: "无火",
        1: "小火",
        2: "中火",
        3: "猛火",
        4: "大火"
        }
    iFloodingIntensityLevel = {
        0: "未进水",
        1: "少量",
        2: "中等",
        3: "严重",
        4: "翻覆"
        }
    iDisturbState = {
        0: "显示干扰",
        1: "显示不干扰示"
        }
    m_WeaponType = {
        1001: "未知",
        2001: "制导武器",
        2002: "火箭弹",
        2003: "炸弹",
        2004: "火炮",
        2005: "诱饵（一次性）",
        2006: "诱饵（拖曳型）",
        2007: "诱饵（移动车辆）",
        2008: "训练设备",
        2009: "集束炸弹",
        2010: "自杀式接触炸弹",
        2011: "接触炸弹（破坏）",
        2012: "制导炮弹",
        3001: "探测吊舱",
        3002: "副油箱",
        3003: "加油油箱",
        3004: "转场油箱",
        4001: "鱼雷",
        4002: "深弹",
        4003: "声呐浮标",
        4004: "沉底水雷",
        4005: "锚雷",
        4006: "浮雷",
        4007: "自航水雷",
        4008: "上浮雷",
        4009: "漂雷",
        4011: "教练雷",
        4101: "直升机拖曳装置",
        5001: "重入载具",
        6001: "激光",
        8001: "高超音速滑翔飞行器",
        9001: "货物",
        9002: "装甲部队",
        9003: "伞兵"
        }


class CUnguidedWeapon:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string Guid"
        fAltitude_AGL = "float 地理高度"
        iAltitude_ASL = "int 一段时间后的海拔高度"
        m_Side = "string 所属推演方Guid"
        strUnitClass = "string 单元类型"
        dLatitude = "double 纬度"
        dLongitude = "double 经度"
        fCurrentHeading = "float 当前朝向"
        fCurrentSpeed = "float 当前速度"
        fCurrentAltitude_ASL = "float 当前海拔高度"
        fPitch = "float 倾斜角"
        fRoll = "float 翻转角"
        bIsOnLand = "bool 是否在陆地上"
        iDBID = "int 数据库ID"
        m_LaunchPoint = "string 获取非自导武器发射点的经纬度"
        m_FiringParent = "string 发射单元ID"
        m_Target = "string 武器目标的GUID"


class CWeaponImpactDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        dLatitude = "double 爆炸经度"
        dLongitude = "double 爆炸纬度"
        iAltitude_ASL = "int 海拔高度"
        m_ImpactType = "int 碰撞类型 (枚举量)"

    m_ImpactType = {
        0: "空爆",
        1: "脉冲"
        }


class CSideWayDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string Guid"
        m_Side = "string 推演方的GUID"
        m_bShow = "bool 是否显示航线"
        m_eSideWayType = "int 航线类型 (枚举量)"
        m_WayPoints = "string 所有航路点的集合"

    m_eSideWayType = {
        0: "作战单元预设航线",
        1: "武器预设航行"
        }


class CWayPointDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        dLongitude = "double 经度"
        dLatitude = "double 纬度"
        fAltitude = "float 高度"
        m_ActiveUnit = "string 活动单元的GUID"
        m_WaypointType = "int 路径点类型 (枚举量)"
        m_ThrottlePreset = "int 枚举类-进气道压力 (枚举量)"
        m_AltitudePreset = "int 高空压力 (枚举量)"
        m_DepthPreset = "int 深潜压力 (枚举量)"
        bTerrainFollowing = "bool 是否采用地形跟随"
        fDesiredSpeed = "float 期望速度"
        fDesiredAltitude = "float 期望高度"
        m_Doctrine = "string 作战条令GUID"
        iThermoclineUpDepth = "int 温跃层上"
        iThermoclineDownDepth = "int 温跃层下"
        m_RadarState = "int 雷达状态 (枚举量)"
        m_SonarState = "int 声纳状态 (枚举量)"
        m_ECMState = "int 电磁干扰状态 (枚举量)"

    m_WaypointType = {
        0: "手动绘制的航路点",
        1: "巡逻点",
        2: "武器武器终点",
        3: "非惯性制导导航定位航路点",
        4: "寻路点：搜索到的、避开禁航区的路径点",
        5: "集结点",
        6: "转折点",
        7: "初始点",
        8: "分批",
        9: "编队",
        10: "目标",
        11: "降落集合编组点",
        12: "进入突击区",
        13: "退出突击区",
        14: "加油点",
        15: "起飞点",
        16: "编列",
        17: "武器发射",
        18: "降落",
        19: "武器分配目标",
        20: "航迹点",
        21: "GIS Road Finder",
        22: "预设航线"
        }
    m_ThrottlePreset = {
        0: "停车",
        1: "低速",
        2: "巡航",
        3: "全速",
        4: "最大",
        5: "无",
        6: "滑行"
        }
    m_AltitudePreset = {
        0: "无",
        1: "最小高度：0米",
        2: "1000英尺",
        3: "2000英尺",
        4: "12000英尺",
        5: "25000英尺",
        6: "36000英尺",
        7: "最大高度"
        }
    m_DepthPreset = {
        0: "无",
        1: "负20米",
        2: "负40米",
        3: "温跃层上方10米",
        4: "温跃层下方10米",
        5: "尽可能深",
        6: "0米"
        }
    m_RadarState = {
        0: "未开机",
        1: "开机",
        2: "不确定"
        }
    m_SonarState = {
        0: "未开机",
        1: "开机",
        2: "不确定"
        }
    m_ECMState = {
        0: "未开机",
        1: "开机",
        2: "不确定"
        }


class CContactDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string Guid"
        fAltitude_AGL = "float 地面高度"
        iAltitude_ASL = "int 海拔高度"
        m_Side = "string 目标真实单元所在方的GUID"
        strUnitClass = "string 实体类别"
        dLatitude = "double 当前纬度"
        dLongitude = "double 当前经度"
        fCurrentHeading = "float 当前朝向"
        fCurrentSpeed = "float 当前速度"
        fCurrentAltitude_ASL = "float 当前海拔高度"
        fPitch = "float 倾斜角"
        fRoll = "float 翻转角"
        bIsOnLand = "bool 是否在陆地上"
        m_ContactType = "int 目标类型 (枚举量)"
        bSideIsKnown = "bool 属方是否已知"
        m_IdentificationStatus = "int 目标的识别状态 (枚举量)"
        m_ActualUnit = "string 本身单元的GUID"
        m_OriginalDetectorSide = "string 探测到的推演方"
        m_SidePostureStanceDictionary = "string 其它推演方对本目标的立场姿态"
        bSpeedKnown = "bool 速度是否已知"
        bHeadingKnown = "bool 朝向是否已知"
        bAltitudeKnown = "bool 高度是否已知"
        strElectromagnetismEradiateTitle = "string 电磁辐射Title"
        strElectromagnetismEradiate = "string 电磁辐射集合"
        strMatchingTitle = "string 匹配结果标题"
        m_MatchingDBIDList = "string 可能匹配结果"
        strRadiantPoint = "string 识别出的辐射平台"
        m_DetectionRecord = "string 侦察记录"
        m_UncertaintyArea = "string 不确定区域集合"
        strAge = "string 目标持续时间"
        fMaxDetectRange = "float 目标发射源容器中传感器的最大探测距离"
        fMaxRange_DetectSurfaceAndFacility = "float 最大对海探测范围"
        fMaxRange_DetectSubsurface = "float 最大对潜探测范围"
        fTimeSinceDetection_Visual = "float 目标探测时间"
        iWeaponsAimingAtMe = "int 瞄准目标的武器数量"
        fAirRangeMax = "float 目标武器对空最大攻击距离"
        fSurfaceRangeMax = "float 目标武器对海最大攻击距离"
        fLandRangeMax = "float 目标武器对陆最大攻击距离"
        fSubsurfaceRangeMax = "float 目标武器对潜最大攻击距离"
        m_EmissionContainer = "string 目标发射源容器"
        strContactEmissions = "string 态势控制——目标电磁辐射显示信息"

    m_ContactType = {
        0: "空中目标",
        1: "导弹",
        2: "水面/地面",
        3: "潜艇",
        4: "未确定的海军",
        5: "瞄准点",
        6: "轨道目标",
        7: "固定设施",
        8: "移动设施",
        9: "鱼雷",
        10: "水雷",
        11: "爆炸",
        12: "不确定",
        13: "空中诱饵",
        14: "表面诱饵",
        15: "陆地诱饵",
        16: "水下诱饵",
        17: "声纳浮标",
        18: "军事设施",
        19: "空军基地",
        20: "海军基地",
        21: "移动集群",
        22: "激活点：瞄准点"
        }
    m_IdentificationStatus = {
        0: "未知",
        1: "已知空域（如空中、地面）",
        2: "已知类型（如飞机、导弹）",
        3: "已知级别",
        4: "确认对象"
        }


class CLoggedMessageDict:
    class Info(Enum):
        pass


class CSimEventDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 描述"
        bIsRepeatable = "bool 事件是否可重复"
        bIsActive = "bool 事件是否启动"
        bIsMessageShown = "bool 是否输出日志提示"
        sProbability = "short 发生事件概率值"
        m_Triggers = "string 触发器的GUID"
        m_Conditions = "string 条件的GUID"
        m_Actions = "string 动作的GUID"


class CTriggerUnitDetectedDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件触发器描述"
        m_EventTriggerType = "int 事件触发器类型"
        strTargetSide = "string 目标推演方GUID"
        m_TargetType = "int 目标类型 (枚举量)"
        iTargetSubType = "int 目标子类型 (枚举量)"
        iSpecificUnitClass = "int 目标等级"
        m_SpecificUnit = "string 特殊单元GUID"
        strDetectorSideID = "string 探测器推演方GUID"
        m_identificationStatus = "int 最小等级分类 (枚举量)"

    m_TargetType = {
        0: "未知",
        1: "飞机",
        2: "船只",
        3: "潜艇",
        4: "设施",
        5: "瞄准点",
        6: "武器"
        }
    m_identificationStatus = {
        0: "未知",
        1: "已知空域（如空中、地面）",
        2: "已知类型（如飞机、导弹）",
        3: "已知级别",
        4: "确认对象"
        }


class CTriggerUnitDamagedDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件触发器描述"
        m_EventTriggerType = "int 事件触发器类型 (枚举量)"
        strTargetSide = "string 目标推演方GUID"
        m_TargetType = "int 目标类型 (枚举量)"
        iTargetSubType = "int 目标子类型 (枚举量)"
        iSpecificUnitClass = "int 目标等级"
        m_SpecificUnit = "string 特殊单元GUID"
        iDamagePercent = "int 百分比阀值"

    m_EventTriggerType = {
        0: "单元被毁",
        1: "推演方得分 添加注释 董卓 2018年8月4日10:50:03",
        2: "时间",
        3: "单元受损",
        4: "单元在区域内",
        5: "单元进入区域",
        6: "随时时间",
        7: "单元被探测到",
        8: "想定已加载",
        9: "规则时间",
        10: "20171106 ZSP 1.13版本 Lua 2.0；想定结束",
        11: "20171106 ZSP 1.13版本 Lua 2.0 ",
        12: "飞机起飞",
        13: "飞机降落"
        }
    m_TargetType = {
        0: "未知",
        1: "飞机",
        2: "船只",
        3: "潜艇",
        4: "设施",
        5: "瞄准点",
        6: "武器",
        7: "卫星"
        }
    iTargetSubType = {
        1: {
            1001: "其他",
            2001: "战斗机",
            2002: "多用途飞机",
            2101: "反卫星飞机",
            2102: "空中激光平台",
            3001: "攻击机",
            3002: "野鼬鼠 （防空压制）",
            3101: "轰炸机",
            3401: "战场空中拦截（BAI/ CAS）",
            4001: "电子战飞机",
            4002: "预警机",
            4003: "指挥机 （ACP）",
            4101: "救援飞机",
            4201: "反水雷飞机",
            6001: "反潜作战飞机",
            6002: "海上巡逻机",
            7001: "前进观察员",
            7002: "区域监视",
            7003: "侦察机",
            7004: "电子情报收集飞机",
            7005: "信号情报收集飞机",
            7101: "运输机",
            7201: "货机",
            7301: "商业飞机",
            7302: "民用",
            7401: "通用直升机",
            7402: "海军通用直升机",
            8001: "空中加油机",
            8101: "教练机",
            8102: "牵引机",
            8103: "靶机",
            8201: "无人机",
            8202: "无人作战飞行器",
            8901: "飞艇",
            8902: "航空器",
            9001: "0x0400204A RID: 8266",
            9002: "航天飞机",
            9003: "0x0400204C RID: 8268",
            9004: "自杀式无人机"
            },
        2: {
            1001: "其他",
            2001: "航空母舰",
            2002: "攻击型航空母舰",
            2003: "大型航空母舰",
            2004: "护航航空母舰",
            2005: "导弹直升机航母",
            2006: "直升机航母",
            2007: "轻型航空母舰",
            2008: "核动力航空母舰",
            2009: "水上飞机母舰",
            2010: "反潜航空母舰",
            3001: "战列舰",
            3002: "战列舰",
            3003: "指挥战列舰",
            3004: "导弹战列舰",
            3005: "直升机战列舰",
            3006: "核动力导弹战列巡洋舰",
            3007: "小型浅水重炮舰",
            3101: "巡洋舰",
            3102: "重型巡洋舰",
            3103: "重型导弹巡洋舰",
            3104: "大型巡洋舰",
            3105: "大型导弹巡洋舰",
            3106: "导弹巡洋舰",
            3107: "导弹直升机巡洋舰",
            3108: "核动力导弹巡洋舰",
            3109: "轻型巡洋舰",
            3110: "轻型防空巡洋舰",
            3111: "轻型指挥巡洋舰",
            3112: "轻型导弹巡洋舰",
            3113: "轻型直升机巡洋舰",
            3114: "侦查巡洋舰",
            3201: "驱逐舰",
            3202: "驱逐舰",
            3203: "导弹驱逐舰",
            3204: "直升机驱逐舰",
            3205: "反潜艇驱逐舰",
            3206: "雷达警戒驱逐舰",
            3207: "护航驱逐舰",
            3208: "导弹护航驱逐舰",
            3209: "雷达警戒护航驱逐舰",
            3210: "驱逐舰",
            3211: "导弹驱逐舰",
            3212: "布雷驱逐舰（改装自驱逐舰）",
            3301: "护卫舰",
            3302: "护卫舰",
            3303: "导弹护卫舰",
            3304: "轻型护卫舰",
            3305: "巡逻护卫舰",
            3306: "濒海战斗舰",
            3307: "海洋巡逻艇",
            3401: "巡逻艇",
            3402: "海岸巡逻艇",
            3403: "猎潜艇",
            3404: "猎潜护航艇",
            3405: "快速巡逻艇",
            3406: "快速导弹巡逻艇",
            3407: "巡逻舰",
            3408: "轻型护卫舰",
            3409: "导弹炮舰",
            3410: "水翼炮艇",
            3411: "导弹水翼船",
            3412: "水翼鱼雷快艇",
            3413: "巡逻鱼雷艇",
            3414: "小型鱼雷巡逻艇",
            3415: "鱼雷摩托艇",
            3416: "海岸警卫队高续航快艇",
            3417: "海岸警卫队中续航快艇",
            3418: "海岸警卫队巡逻船",
            3419: "海岸警卫队巡逻炮艇",
            3420: "海事海防船",
            4000: "指挥舰",
            4001: "两栖舰队旗舰",
            4002: "气垫登陆艇",
            4003: "两栖指挥舰",
            4004: "机械化登陆艇",
            4005: "人员登陆艇",
            4006: "坦克登陆艇",
            4007: "通用登陆艇",
            4008: "车辆及人员登陆艇",
            4009: "近岸火力支援船",
            4010: "通用两栖攻击舰",
            4011: "多用途两栖攻击舰",
            4012: "两栖货舰",
            4013: "两栖船坞运输舰",
            4014: "两栖攻击直升机航母",
            4015: "船坞登陆舰",
            4016: "未知！英国型号！",
            4017: "后勤登陆舰",
            4018: "中型登陆舰",
            4019: "中型火箭登陆舰",
            4020: "坦克登陆舰",
            4021: "通用登陆舰",
            4022: "车辆登陆舰",
            4023: "步兵登陆舰",
            4024: "半潜水快艇",
            4025: "气垫式人员登陆舰",
            4026: "远征快速运输舰",
            4027: "远征转运码头舰",
            4028: "远征移动基地舰",
            5001: "辅助船",
            5002: "驱逐舰供应舰",
            5003: "弹药船",
            5004: "冷藏储运船",
            5005: "军需品储运船",
            5006: "通用辅助船",
            5007: "重型破冰船",
            5008: "指挥舰",
            5009: "情报收集舰",
            5010: "通信中继船",
            5011: "海洋科学考察船",
            5012: "海洋监测船",
            5013: "雷达警戒（改装自货船）",
            5014: "测量船",
            5015: "技术考察船",
            5016: "医疗船",
            5017: "货船",
            5018: "武装货船",
            5019: "干货船",
            5020: "滚装船",
            5021: "通用存运船",
            5022: "舰队油船",
            5023: "快速战斗支援舰",
            5024: "小型油船",
            5025: "补给油船",
            5026: "运油船",
            5027: "攻击型人员运输舰",
            5028: "运兵船（高速）",
            5029: "修理船",
            5030: "潜艇供应舰",
            5031: "武装运兵船 (靶船)",
            5032: "辅助远洋拖船",
            5033: "救助拖船",
            5034: "水上飞机供应舰",
            5035: "训练舰",
            5036: "潜艇救援舰",
            5037: "人员运输舰",
            5038: "潜水支援船/深潜车",
            5039: "导弹射程测量船",
            5101: "MSC (军事海运司令部) 海洋监测船",
            5102: "MSC (军事海运司令部) 医疗船",
            5103: "MSC (军事海运司令部)货船",
            5104: "MSC (军事海运司令部) 干货船",
            5105: "MSC (军事海运司令部) 滚装船",
            5106: "MSC (军事海运司令部) 舰队油船",
            5107: "MSC (军事海运司令部) 运油船",
            5108: "MSC (军事海运司令部) 移动登陆平台",
            6001: "反水雷无人机",
            6002: "反水雷舰",
            6003: "反水雷支援舰",
            6004: "沿岸猎雷艇",
            6005: "布雷艇",
            6006: "沿海扫雷舰",
            6007: "钢壳舰队扫雷舰",
            6008: "近岸扫雷舰",
            6010: "远洋扫雷舰",
            6011: "扫雷舰支援舰",
            6012: "近岸猎雷舰",
            6013: "雷区养护舰",
            7001: "各类勤务船",
            9001: "民用船只",
            9002: "贸易船只",
            9003: "平底驳船/海上钻井平台",
            9004: "NGS (美国国家大地测量局) Buoy",
            9005: "底部固定阵列声纳",
            9006: "系泊声纳浮标",
            9007: "特殊（地面单位/卫星）",
            9011: "移动式近海基地"
            },
        3: {
            1001: "其他",
            2001: "辅助/实验潜艇",
            2002: "辅助货运潜艇",
            2003: "攻击/舰队型潜艇",
            2004: "弹道导弹潜艇",
            2005: "弹道导弹核潜艇",
            2006: "导弹攻击型潜艇",
            2007: "核动力导弹攻击型潜艇",
            2008: "猎杀潜艇",
            2009: "小型潜水艇",
            2010: "核动力攻击型潜艇",
            2011: "运输型潜艇",
            2012: "雷达预警潜艇",
            2013: "核动力雷达预警潜艇",
            3001: "蛙人运送艇",
            4001: "远程遥控潜艇",
            4002: "无人潜航器",
            9001: "海洋生物",
            9002: "假目标"
            }
        }


class CTriggerUnitDestroyedDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件触发器描述"
        m_EventTriggerType = "int 事件触发器类型 (枚举量)"
        strTargetSide = "string 目标推演方GUID"
        m_TargetType = "int 目标类型 (枚举量)"
        iTargetSubType = "int 目标子类型 (枚举量)"
        iSpecificUnitClass = "int 目标等级"
        m_SpecificUnit = "string 特殊单元GUID"

    m_EventTriggerType = {
        0: "单元被毁",
        1: "推演方得分添加注释董卓2018年8月4日10:50:03",
        2: "时间",
        3: "单元受损",
        4: "单元在区域内",
        5: "单元进入区域",
        6: "随时时间",
        7: "单元被探测到",
        8: "想定已加载",
        9: "规则时间",
        10: "20171106ZSP1.13版本Lua2.0；想定结束",
        11: "20171106ZSP1.13版本Lua2.0",
        12: "飞机起飞",
        13: "飞机降落"
        }
    m_TargetType = {
        0: "未知",
        1: "飞机",
        2: "船只",
        3: "潜艇",
        4: "设施",
        5: "瞄准点",
        6: "武器",
        7: "卫星"
        }


class CTriggerPointsDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件触发器描述"
        m_EventTriggerType = "int 事件触发器类型 (枚举量)"
        m_strSideID = "string 推演方的GUID"
        m_reachDirection = "int 得分类型 (枚举量)"
        iPointValue = "int 得分"

    m_EventTriggerType = {
        0: "单元被毁",
        1: "推演方得分",
        2: "时间",
        3: "单元受损",
        4: "单元在区域内",
        5: "单元进入区域",
        6: "随时时间",
        7: "单元被探测到",
        8: "想定已加载",
        9: " 规则时间",
        10: "20171106 ZSP 1.13版本 Lua 2.0；想定结束",
        11: "20171106 ZSP 1.13版本 Lua 2.0 ",
        12: "飞机起飞",
        13: "飞机降落"
        }
    m_reachDirection = {
        0: "负",
        1: "平",
        2: "胜"
        }


class CTriggerTimeDict:
    class Info(Enum):
        strName = " string 名称 "
        strGuid = " string GUID "
        strDescription = " string 事件触发器描述 "
        m_EventTriggerType = "int 事件触发器类型  (枚举量)"
        strCurrentSetting = "string 当前时间 "
        m_Time = "uint 当前时间的时间戳"

    m_EventTriggerType = {
        0: "单元被毁",
        1: "推演方得分",
        2: "时间",
        3: "单元受损",
        4: "单元在区域内",
        5: "单元进入区域",
        6: "随时时间",
        7: "单元被探测到",
        8: "想定已加载",
        9: " 规则时间",
        10: "20171106 ZSP 1.13版本 Lua 2.0；想定结束",
        11: "20171106 ZSP 1.13版本 Lua 2.0 ",
        12: "飞机起飞",
        13: "飞机降落"
        }


class CTriggerRegularTimeDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件触发器描述"
        m_EventTriggerType = "int 事件触发器类型 (枚举量)"
        m_Interval = "int 触发器每几秒将会触发"

    m_EventTriggerType = {
        0: "单元被毁",
        1: "推演方得分",
        2: "时间",
        3: "单元受损",
        4: "单元在区域内",
        5: "单元进入区域",
        6: "随时时间",
        7: "单元被探测到",
        8: "想定已加载",
        9: " 规则时间",
        10: "20171106 ZSP 1.13版本 Lua 2.0；想定结束",
        11: "20171106 ZSP 1.13版本 Lua 2.0 ",
        12: "飞机起飞",
        13: "飞机降落"
        }


class CTriggerRandomTimeDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件触发器描述"
        m_EventTriggerType = "int 事件触发器类型 (枚举量)"
        strCurrentSetting = "string 当前设置最早最晚时间"
        m_EarliestTime = "uint 最早时间的时间戳"
        m_LatestTime = "uint 最晚时间的时间戳"

    m_EventTriggerType = {
        0: "单元被毁",
        1: "推演方得分",
        2: "时间",
        3: "单元受损",
        4: "单元在区域内",
        5: "单元进入区域",
        6: "随时时间",
        7: "单元被探测到",
        8: "想定已加载",
        9: " 规则时间",
        10: "20171106 ZSP 1.13版本 Lua 2.0；想定结束",
        11: "20171106 ZSP 1.13版本 Lua 2.0 ",
        12: "飞机起飞",
        13: "飞机降落"
        }


class CTriggerScenLoadedDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件触发器描述"
        m_EventTriggerType = "int 事件触发器类型 (枚举量)"

    m_EventTriggerType = {
        0: "单元被毁",
        1: "推演方得分",
        2: "时间",
        3: "单元受损",
        4: "单元在区域内",
        5: "单元进入区域",
        6: "随时时间",
        7: "单元被探测到",
        8: "想定已加载",
        9: " 规则时间",
        10: "20171106 ZSP 1.13版本 Lua 2.0；想定结束",
        11: "20171106 ZSP 1.13版本 Lua 2.0 ",
        12: "飞机起飞",
        13: "飞机降落"
        }


class CTriggerUnitRemainsInAreaDict:
    class Info(Enum):
        strName = " string 名称 "
        strGuid = " string GUID "
        strDescription = " string 事件触发器描述 "
        m_EventTriggerType = " int 事件触发器类型 (枚举量) "
        strTargetSide = " string 目标推演方GUID "
        m_TargetType = " int 目标类型 (枚举量)"
        iTargetSubType = " int 目标子类型 "
        iSpecificUnitClass = " int 目标等级"
        m_SpecificUnit = " string 特殊单元GUID "
        bModifier = " bool 反选 "
        m_ETOA = " uint 最早时间 "
        m_LTOA = " uint 最晚时间 "
        m_ReferencePoint = " string 区域 "

    m_EventTriggerType = {
        0: "单元被毁",
        1: "推演方得分",
        2: "时间",
        3: "单元受损",
        4: "单元在区域内",
        5: "单元进入区域",
        6: "随时时间",
        7: "单元被探测到",
        8: "想定已加载",
        9: " 规则时间",
        10: "20171106 ZSP 1.13版本 Lua 2.0；想定结束",
        11: "20171106 ZSP 1.13版本 Lua 2.0 ",
        12: "飞机起飞",
        13: "飞机降落"
        }
    m_TargetType = {
        0: "未知",
        1: "飞机",
        2: "船只",
        3: "潜艇",
        4: "设施",
        5: "瞄准点",
        6: "武器",
        7: "卫星"
        }


class CConditionScenHasStartedDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件条件描述"
        m_EventConditionType = "int 事件条件类型 (枚举量)"
        bModifier = "bool 反选"

    m_EventConditionType = {
        0: "推演方立场",
        1: "想定开始执行",
        2: "LUA脚本"
        }


class CConditionSidePostureDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件条件描述"
        m_EventConditionType = "int 事件条件类型 (枚举量)"
        bModifier = "bool 反选"
        strObserverSideID = "string 推演方GUID"
        strTargetSideID = "string 考虑推演方GUID"
        m_TargetPosture = "int 推演方关系"

    m_EventConditionType = {
        0: "推演方立场",
        1: "想定开始执行",
        2: "LUA脚本"
        }
    m_TargetPosture = {
        0: "中立",
        1: "友方",
        2: "不友好",
        3: "敌对",
        4: "未知"
        }


class CConditionLuaScriptDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件条件描述"
        m_EventConditionType = "int 事件条件类型 (枚举量)"
        strLuaScript = "string Lua脚本"

    m_EventConditionType = {
        0: "推演方立场",
        1: "想定开始执行",
        2: "LUA脚本"
        }


class CActionMessageDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件动作描述"
        m_EventActionType = "int 事件动作类型 (枚举量)"
        m_strSideID = "string 推演方GUID"
        strMessageText = "string 消息文本"

    m_EventActionType = {
        0: "得分",
        1: "想定结束",
        2: "进入某个区域",
        3: "接收消息",
        4: "改变任务状态",
        5: "LUA脚本"
        }


class CActionPointsDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件动作描述"
        m_EventActionType = "int 事件动作类型 (枚举量)"
        m_strSideID = "string 推演方GUID"
        iPointChange = "int 变化评分"

    m_EventActionType = {
        0: "得分",
        1: "想定结束",
        2: "进入某个区域",
        3: "接收消息",
        4: "改变任务状态",
        5: "LUA脚本"
        }


class CActionTeleportInAreaDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件动作描述"
        m_EventActionType = "int 事件动作类型 (枚举量)"
        strUnitIDs = "string 要瞬间移动的目标"
        m_ReferencePoint = "string 区域"

    m_EventActionType = {
        0: "得分",
        1: "想定结束",
        2: "进入某个区域",
        3: "接收消息",
        4: "改变任务状态",
        5: "LUA脚本"
        }


class CActionChangeMissionStatusDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件动作描述"
        m_EventActionType = "int 事件动作类型 (枚举量)"
        m_strSideID = "string 推演方GUID"
        strMissionID = "string 任务GUID"
        m_newmissionStatus = "int 是否启动"

    m_EventActionType = {
        0: "得分",
        1: "想定结束",
        2: "进入某个区域",
        3: "接收消息",
        4: "改变任务状态",
        5: "LUA脚本"
        }


class CActionEndScenarioDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件动作描述"
        m_EventActionType = "int 事件动作类型 (枚举量)"

    m_EventActionType = {
        0: "得分",
        1: "想定结束",
        2: "进入某个区域",
        3: "接收消息",
        4: "改变任务状态",
        5: "LUA脚本"
        }


class CActionLuaScriptDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        strDescription = "string 事件动作描述"
        m_EventActionType = "int 事件动作类型 (枚举量)"
        strLuaScript = "string Lua脚本"

    m_EventActionType = {
        0: "得分",
        1: "想定结束",
        2: "进入某个区域",
        3: "接收消息",
        4: "改变任务状态",
        5: "LUA脚本"
        }


class CPatrolMissionDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        m_Side = "string 方GUID"
        m_Category = "int 任务类别 (枚举量)"
        m_MissionClass = "int 任务类型 (枚举量)"
        m_StartTime = "uint 任务开始时间"
        m_EndTime = "uint 任务结束时间"
        m_MissionStatus = "int 任务状态"
        m_AssignedUnits = "string 已分配的单元"
        m_UnassignedUnits = "string 未分配的单元"
        m_PatrolType = "int 巡逻任务类型 (枚举量)"
        iMNOS = "int 巡逻-阵位上每类平台保持几个作战单元"
        bOTR = "bool 巡逻- 1/3规则"
        bIOPA = "bool 巡逻- 对巡逻区外的探测目标进行分析"
        bIWWR = "bool 巡逻- 对武器射程内的探测目标进行分析"
        bAEOIPA = "bool 巡逻-仅在巡逻/警戒区内打开电磁辐射"
        m_FlightSize = "int 飞机设置-编队规模："
        bUseRefuel = "bool 空中加油选项是否与上级保持一致"
        m_UseRefuel = "int 飞机设置-空中加油 (枚举量)"
        m_MinAircraftReq = "int 执行任务所需的最低飞机数"
        bUseFlightSizeHardLimit = "bool 飞机数低于编队规模要求,不能起飞……"
        m_GroupSize = "int 水面舰艇/潜艇设置-编队规模"
        m_strSideWayGUID = "string 单元航线"
        bUseGroupSizeHardLimit = "bool 水面舰艇/潜艇设置-水面舰艇/潜艇树低于编队规模要求,不能出击(根据基地编组)"
        m_PatrolAreaVertices = "string 编辑巡逻区-返回参考点的guid集合  "
        m_ProsecutionAreaVertices = "string 编辑警戒区-返回参考点的guid集合"
        m_TransitThrottle_Aircraft = "int 飞机航速与高度-出航油门 (枚举量)"
        m_StationThrottle_Aircraft = "int 飞机航速与高度-阵位油门 (枚举量)"
        m_AttackThrottle_Aircraft = "int 飞机航速与高度-攻击油门 (枚举量)"
        strTransitAltitude_Aircraft = "string 飞机航速与高度-出航高度"
        strStationAltitude_Aircraft = "string 飞机航速与高度-阵位高度"
        strAttackAltitude_Aircraft = "string 飞机航速与高度-攻击高度"
        strAttackDistance_Aircraft = "string 飞机航速与高度-攻击距离"
        m_TransitThrottle_Submarine = "int 潜艇航速与潜深-出航油门 (枚举量)"
        m_StationThrottle_Submarine = "int 潜艇航速与潜深-阵位油门 (枚举量)"
        m_AttackThrottle_Submarine = "int 潜艇航速与潜深-攻击油门 (枚举量)"
        strTransitDepth_Submarine = "string 潜艇航速与潜深-出航潜深"
        strStationDepth_Submarine = "string 潜艇航速与潜深-阵位潜深"
        strAttackDepth_Submarine = "string 潜艇航速与潜深-攻击潜深"
        strAttackDistance_Submarine = "string 潜艇航速与潜深-攻击距离"
        m_TransitThrottle_Ship = "int 水面舰艇航速-出航油门 (枚举量)"
        m_StationThrottle_Ship = "int 水面舰艇航速-阵位油门 (枚举量)"
        m_AttackThrottle_Ship = "int 水面舰艇航速-攻击油门 (枚举量)"
        m_Doctrine = "string 作战条令的GUID"
        strAttackDistance_Ship = "string 水面舰艇航速-攻击距离"
        fnudSonobuoysCoverMul = "float 声呐浮标覆盖半径倍数"
        m_cboSonobuoysType = "int 投放声呐浮标的类型参数 (枚举量)"
        iEmptySlots = "int 这个值是对ReadyAircraft类对象的成员list赋值的count"

    m_Category = {
        0: "任务",
        1: "任务包",
        2: "任务池"
        }
    m_MissionClass = {
        0: "未知",
        1: "打击/截击",
        2: "巡逻",
        3: "支援",
        4: "转场",
        5: "布雷",
        6: "扫雷",
        7: "护航",
        8: "投送选项"
        }
    m_PatrolType = {
        0: "反潜战",
        1: "反水面战（海上）",
        2: "空战",
        3: "反水面战（陆上）",
        4: "反水面战（混合）",
        5: "压制敌防空",
        6: "海上控制"
        }
    m_UseRefuel = {
        0: "允许,但不允许加油机对加油机加油",
        1: "不允许",
        2: "允许",
        3: "多样",
        4: "未配置"
        }
    m_TransitThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner:加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner:加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_AttackThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner:加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_TransitThrottle_Submarine = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner:加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Submarine = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner:加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_AttackThrottle_Submarine = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner:加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_TransitThrottle_Ship = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner:加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Ship = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner:加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_AttackThrottle_Ship = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner:加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_cboSonobuoysType = {
        0: "温跃层随机",
        1: "浅_温跃层之上",
        2: "深_温跃层之下"
        }


class CStrikeMissionDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        m_Side = "string 方GUID"
        m_Category = "int 任务类别 (枚举量)"
        m_MissionClass = "int 任务类型 (枚举量)"
        m_StartTime = "uint 任务开始时间"
        m_EndTime = "uint 任务结束时间"
        m_MissionStatus = "int 任务状态 (枚举量)"
        m_AssignedUnits = "string 已分配的单元"
        m_UnassignedUnits = "string 未分配的单元"
        m_StrikeType = "int 打击任务类型 (枚举量)"
        m_MinimumContactStanceToTrigger = "int 任务触发的探测目标类型 (枚举量)"
        m_FlightSize = "int 飞机设置-编队规模"
        m_Bingo = "int 飞机设置-燃油/弹药："
        m_MinAircraftReq_Strikers = "int 飞机设置-任务允许出动的最大飞行批次 "
        iMinResponseRadius = "int 飞机设置-最小打击半径(与目标距离)"
        iMaxResponseRadius = "int 飞机设置-最大打击半径(与目标距离)"
        m_RadarBehaviour = "int 飞机设置-雷达运用 (枚举量)"
        bUseRefuel = "bool 空中加油是否上级一致"
        m_UseRefuel = "int 飞机设置-空中加油 (枚举量)"
        bUseFlightSizeHardLimit = "bool 飞机设置-飞机数低于编组规模数要求不能起飞"
        bUseAutoPlanner = "bool 飞机设置-多扇面攻击(任务AI自动生成) 是否选中"
        bOneTimeOnly = "bool 飞机设置-仅限一次 是否选中"
        m_GroupSize = "int 水面舰艇/潜艇设置-编队规模，返回选中项的值   "
        bUseGroupSizeHardLimit = "bool 水面舰艇/潜艇设置-水面舰艇或潜艇数低于编队规模要求不能出击(根据基地进行编组)  是否选中 "
        bPrePlannedOnly = "bool 仅考虑计划目标(在目标) 是否选中"
        m_Doctrine = "string 作战条令的GUID"
        m_SpecificTargets = "string 水面舰艇/潜艇设置- 目标清单 返回清单的guid集合"
        m_strSideWayGUID = "string 单元航线GUID"
        m_strSideWeaponWayGUID = "string 武器航线"
        m_EscortFlightSize = "int 飞机设置-火力打击-编队规模"
        m_MinAircraftReqEscorts = "int 飞机设置-火力打击-任务执行所需的最低护航数"
        m_MaxAircraftToFlyEscort = "int 飞机设置-火力打击-飞机任务允许的最大护航数"
        iEscortResponseRadius = "int 飞机设置-火力打击-最大威胁响应半径"
        m_EscortFlightSizeNo = "int 飞机设置-非火力打击-飞机编队规模"
        m_MinAircraftReqEscortsNo = "int 飞机设置-非火力打击-执行任务所需的最低就绪护航数"
        m_MaxAircraftToFlyEscortNo = "int 飞机设置-非火力打击-飞行任务允许最大护航数"
        bUseFlightSizeHardLimitEscort = "bool 飞机设置-飞机数低于编组规模数要求不能起飞 (根据基地、类型或者挂载编组)"
        m_EscortGroupSize = "int 水面舰艇/潜艇设置 -编组规模"
        bUseGroupSizeHardLimitEscort = "bool 水面舰艇/潜艇设置-水面舰艇或潜艇数低于编队规模要求不能出击(根据基地进行编组)"
        m_Doctrine_Escorts = "string 护航的作战条令GUID"
        m_strContactWeaponWayGuid = "string 武器预设的打击航线"
        iEmptySlots = "int "

    m_Category = {
        0: " 任务",
        1: " 任务包",
        2: " 任务池"
        }
    m_MissionClass = {
        0: "未知",
        1: "打击/截击",
        2: "巡逻",
        3: "支援",
        4: "转场",
        5: "布雷",
        6: "扫雷",
        7: "护航",
        8: "投送选项"
        }
    m_MissionStatus = {
        0: "激活状态",
        1: "未激活",
        2: "已完成"
        }
    m_StrikeType = {
        0: "空中截击",
        1: "对陆打击",
        2: "对海打击",
        3: "对潜突击"
        }
    m_RadarBehaviour = {
        0: "整个飞行计划全部使用任务电磁管控",
        1: "从初始点到武器消耗光打开雷达：winchester",
        2: "从攻击进入点到武器消耗光打开雷达",
        3: "默认:缺省"
        }
    m_UseRefuel = {
        0: "允许,但不允许加油机对加油机加油",
        1: "不允许",
        2: "允许",
        3: "多样",
        4: "未配置"
        }


class CSupportMissionDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        m_Side = "string 方GUID"
        m_Category = "int 任务类别 (枚举量)"
        m_MissionClass = "int 任务类型 (枚举量)"
        m_StartTime = "uint 任务开始时间"
        m_EndTime = "uint 任务结束时间"
        m_MissionStatus = "int 任务状态 (枚举量)"
        m_AssignedUnits = "string 已分配的单元"
        m_UnassignedUnits = "string 未分配的单元"
        iMNOS = "int 支援-阵位上每类平台保持几个作战单元"
        bOTR = "bool 1/3规则"
        bOTO = "bool 仅一次"
        bAEOOS = "bool 仅在阵位上打开电磁辐射(需要主动EMCON)"
        iNLT = "int 导航类型 (枚举量)"
        m_FlightSize = "int 飞机设置-编队规模"
        bUseRefuel = "bool 空中加油是否上级一致"
        m_UseRefuel = "int 飞机设置-空中加油 (枚举量)"
        m_GroupSize = "int 水面舰艇/潜艇设置-编队规模"
        m_strSideWayGUID = "string 单元航线"
        bUseGroupSizeHardLimit = "bool 水面舰艇/潜艇数低于编队规模要求,不能出击(根据基地编组)"
        m_NavigationCourseReferencePoints = "string 编辑支援航线"
        m_TransitThrottle_Aircraft = "int 飞机航速与高度-出航油门 (枚举量)"
        m_StationThrottle_Aircraft = "int 飞机航速与高度-阵位油门 (枚举量)"
        strTransitAltitude_Aircraft = "string 飞机航速与高度-出航高度"
        strStationAltitude_Aircraft = "string 飞机航速与高度-阵位高度"
        m_TransitThrottle_Submarine = "int 潜艇航速与潜深-出航油门 (枚举量)"
        m_StationThrottle_Submarine = "int 潜艇航速与潜深-阵位油门 (枚举量)"
        strTransitDepth_Submarine = "string 潜艇航速与潜深-出航潜深"
        strStationDepth_Submarine = "string 潜艇航速与潜深-阵位潜深"
        m_TransitThrottle_Ship = "int 水面舰艇航速-出航油门 (枚举量)"
        m_StationThrottle_Ship = "int 水面舰艇航速-阵位油门 (枚举量)"
        m_Doctrine = "string 作战条令GUID"
        iEmptySlots = "int "

    m_Category = {
        0: " 任务",
        1: " 任务包",
        2: " 任务池"
        }
    m_MissionClass = {
        0: "未知",
        1: "打击/截击",
        2: "巡逻",
        3: "支援",
        4: "转场",
        5: "布雷",
        6: "扫雷",
        7: "护航",
        8: "投送选项"
        }
    m_MissionStatus = {
        0: "激活状态",
        1: "未激活",
        2: "已完成"
        }
    iNLT = {
        0: "连续循环",
        1: "一次循环"
        }
    m_UseRefuel = {
        0: "允许,但不允许加油机对加油机加油",
        1: "不允许",
        2: "允许",
        3: "多样",
        4: "未配置"
        }
    m_TransitThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度，悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行，返航",
        3: "最大战斗功率，油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门，油耗是巡航时的20倍；afterbuner，加力燃烧室，一般高性能战斗机配备；使用时机：空中格——或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度，悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行，返航",
        3: "最大战斗功率，油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门，油耗是巡航时的20倍；afterbuner，加力燃烧室，一般高性能战斗机配备；使用时机：空中格——或逃离目标区域",
        5: "滑行"
        }
    m_TransitThrottle_Submarine = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度，悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行，返航",
        3: "最大战斗功率，油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门，油耗是巡航时的20倍；afterbuner，加力燃烧室，一般高性能战斗机配备；使用时机：空中格——或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Submarine = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度，悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行，返航",
        3: "最大战斗功率，油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门，油耗是巡航时的20倍；afterbuner，加力燃烧室，一般高性能战斗机配备；使用时机：空中格——或逃离目标区域",
        5: "滑行"
        }
    m_TransitThrottle_Ship = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度，悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行，返航",
        3: "最大战斗功率，油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门，油耗是巡航时的20倍；afterbuner，加力燃烧室，一般高性能战斗机配备；使用时机：空中格——或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Ship = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度，悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行，返航",
        3: "最大战斗功率，油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门，油耗是巡航时的20倍；afterbuner，加力燃烧室，一般高性能战斗机配备；使用时机：空中格——或逃离目标区域",
        5: "滑行"
        }


class CCargoMissionDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        m_Side = "string 方GUID"
        m_Category = "int 任务类别 (枚举量)"
        m_MissionClass = "int 任务类型 (枚举量)"
        m_StartTime = "uint 任务开始时间"
        m_EndTime = "uint 任务结束时间"
        m_MissionStatus = "int 任务状态 (枚举量)"
        m_AssignedUnits = "string 已分配的单元"
        m_UnassignedUnits = "string 未分配的单元"
        m_Motherships = "string 母舰平台"
        m_MountsToUnload = "string 要卸载的货物"
        m_strSideWayGUID = "string 单元航线"
        m_TransitThrottle_Aircraft = "int 飞机出航油门 (枚举量)"
        m_StationThrottle_Aircraft = "int 飞机落区油门 (枚举量)"
        strTransitAltitude_Aircraft = "string 飞机出航高度"
        strStationAltitude_Aircraft = "string 飞机落区高度"
        m_TransitThrottle_Ship = "int 水面舰艇出航油门 (枚举量) "
        m_StationThrottle_Ship = "int 水面舰艇码头油门 (枚举量)"
        iEmptySlots = "int "
        m_listAreaPoints = "string 参考点集合"

    m_Category = {
        0: " 任务",
        1: " 任务包",
        2: " 任务池"
        }
    m_MissionClass = {
        0: "未知",
        1: "打击/截击",
        2: "巡逻",
        3: "支援",
        4: "转场",
        5: "布雷",
        6: "扫雷",
        7: "护航",
        8: "投送选项"
        }
    m_MissionStatus = {
        0: "激活状态",
        1: "未激活",
        2: "已完成"
        }
    m_TransitThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_TransitThrottle_Ship = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Ship = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }


class CFerryMissionDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        m_Side = "string 方GUID"
        m_Category = "int 任务类别 (枚举量)"
        m_MissionClass = "int 任务类型 (枚举量)"
        m_StartTime = "uint 任务开始时间"
        m_EndTime = "uint 任务结束时间"
        m_MissionStatus = "int 任务状态 (枚举量)"
        m_AssignedUnits = "string 已分配的单元"
        m_UnassignedUnits = "string 未分配的单元"
        m_FerryMissionBehavior = "int 转场规则 (枚举量)"
        m_FlightSize = "int 编队规模"
        bUseRefuel = "bool 空中加油是否上级一致"
        m_UseRefuel = "int 飞机设置-空中加油 (枚举量)"
        m_MinAircraftReqMining = "int 飞机设置最低飞机数"
        bUseGroupSizeHardLimit = "bool 飞机设置飞机数低于编队规模要求"
        m_TankerUsage = "int 空中加油设置加油机 (枚举量)"
        m_TankerMissionList = "string 空中加油设置列表"
        m_FerryThrottle_Aircraft = "int 飞机转场油门 (枚举量)"
        bFerryTerrainFollowing_Aircraft = "bool 转场地形跟随"
        strTransitAltitude_Aircraft = "string 飞机转场高度"
        iEmptySlots = "int "

    m_Category = {
        0: "任务",
        1: "任务包",
        2: "任务池"
        }
    m_MissionClass = {
        0: "未知",
        1: "打击/截击",
        2: "巡逻",
        3: "支援",
        4: "转场",
        5: "布雷",
        6: "扫雷",
        7: "护航",
        8: "投送选项"
        }
    m_MissionStatus = {
        0: "激活状态",
        1: "未激活",
        2: "已完成"
        }
    m_FerryMissionBehavior = {
        0: "单向",
        1: "循环",
        2: "随机"
        }
    m_UseRefuel = {
        0: "允许,但不允许加油机对加油机加油",
        1: "不允许",
        2: "允许",
        3: "多样",
        4: "未配置"
        }
    m_TankerUsage = {
        0: "自动使用",
        1: "任务中使用"
        }
    m_FerryThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }


class CMiningMissionDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        m_Side = "string 方GUID"
        m_Category = "int 任务类别 (枚举量)"
        m_MissionClass = "int 任务类型 (枚举量)"
        m_StartTime = "uint 任务开始时间"
        m_EndTime = "uint 任务结束时间"
        m_MissionStatus = "int 任务状态 (枚举量)"
        m_AssignedUnits = "string 已分配的单元"
        m_UnassignedUnits = "string 未分配的单元"
        Botr = "bool 1/3规则"
        m_AD = "string 天 时 分 秒"
        m_FlightSize = "int 编队规模"
        bUseRefuel = "bool 空中加油是否上级一致"
        m_UseRefuel = "int 飞机设置-空中加油 (枚举量)"
        m_MinAircraftReqMining = "int 最低飞机数"
        bUseGroupSizeHardLimit = "bool 飞机数低于编队规模要求"
        m_TankerUsage = "int 加油机 (枚举量)"
        m_TankerMissionList = "string 加油机任务列表"
        m_GroupSize = "int 编队规模"
        m_MiningAreaVertices = "string 布雷区域"
        m_TransitThrottle_Aircraft = "int 飞机出航油门 (枚举量)"
        m_StationThrottle_Aircraft = "int 飞机阵位油门 (枚举量)"
        strTransitAltitude_Aircraft = "string 飞机出航高度"
        strStationAltitude_Aircraft = "string 飞机阵位高度"
        m_TransitThrottle_Ship = "int 水面舰艇出航油门 (枚举量)"
        m_StationThrottle_Ship = "int 水面舰艇阵位油门 (枚举量)"
        m_TransitThrottle_Submarine = "int 潜艇出航油门 (枚举量)"
        m_StationThrottle_Submarine = "int 潜艇阵位油门 (枚举量)"
        strTransitDepth_Submarine = "string 潜艇出航潜深"
        strStationDepth_Submarine = "string 潜艇阵位潜深"
        iEmptySlots = "int "

    m_Category = {
        0: "任务",
        1: "任务包",
        2: "任务池"
        }
    m_MissionClass = {
        0: "未知",
        1: "打击/截击",
        2: "巡逻",
        3: "支援",
        4: "转场",
        5: "布雷",
        6: "扫雷",
        7: "护航",
        8: "投送选项"
        }
    m_MissionStatus = {
        0: "激活状态",
        1: "未激活",
        2: "已完成"
        }
    m_UseRefuel = {
        0: "允许,但不允许加油机对加油机加油",
        1: "不允许",
        2: "允许",
        3: "多样",
        4: "未配置"
        }
    m_TankerUsage = {
        0: "自动使用",
        1: "任务中使用"
        }
    m_TransitThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_TransitThrottle_Ship = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Ship = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_TransitThrottle_Submarine = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Submarine = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }


class CMineClearingMissionDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        m_Side = "string 方GUID"
        m_Category = "int 任务类别 (枚举量)"
        m_MissionClass = "int 任务类型 (枚举量)"
        m_StartTime = "uint 任务开始时间"
        m_EndTime = "uint 任务结束时间"
        m_MissionStatus = "int 任务状态 (枚举量)"
        m_AssignedUnits = "string 已分配的单元"
        m_UnassignedUnits = "string 未分配的单元"
        bOTR = "bool 1/3规则"
        m_FlightSize = "int 编队规模"
        bUseRefuel = "bool 空中加油是否上级一致"
        m_UseRefuel = "int 飞机设置-空中加油 (枚举量)"
        m_MinAircraftReqMining = "int 飞机设置最低飞机数"
        bUseGroupSizeHardLimit = "bool 飞机设置飞机数低于编队规模要求"
        m_TankerUsage = "int 空中加油设置加油机 (枚举量)"
        m_GroupSize = "int 编队规模"
        m_TankerMissionList = "string 空中加油设置列表"
        m_MineClearinAreaVertices = "string 区域"
        m_TransitThrottle_Aircraft = "int 飞机出航油门 (枚举量)"
        m_StationThrottle_Aircraft = "int 飞机阵位油门 (枚举量)"
        strTransitAltitude_Aircraft = "string 飞机出航高度"
        strStationAltitude_Aircraft = "string 飞机阵位高度"
        m_TransitThrottle_Ship = "int 水面舰艇出航油门 (枚举量)"
        m_StationThrottle_Ship = "int 水面舰艇阵位油门 (枚举量)"
        m_TransitThrottle_Submarine = "int 潜艇出航油门 (枚举量)"
        m_StationThrottle_Submarine = "int 潜艇阵位油门 (枚举量)"
        strTransitDepth_Submarine = "string 潜艇出航潜深"
        strStationDepth_Submarine = "string 潜艇阵位潜深"
        iEmptySlots = "int "

    m_Category = {
        0: "任务",
        1: "任务包",
        2: "任务池"
        }
    m_MissionClass = {
        0: "未知",
        1: "打击/截击",
        2: "巡逻",
        3: "支援",
        4: "转场",
        5: "布雷",
        6: "扫雷",
        7: "护航",
        8: "投送选项"
        }
    m_MissionStatus = {
        0: "激活状态",
        1: "未激活",
        2: "已完成"
        }
    m_UseRefuel = {
        0: "允许,但不允许加油机对加油机加油",
        1: "不允许",
        2: "允许",
        3: "多样",
        4: "未配置"
        }
    m_TankerUsage = {
        0: "自动使用",
        1: "任务中使用"
        }
    m_TransitThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Aircraft = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_TransitThrottle_Ship = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Ship = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_TransitThrottle_Submarine = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }
    m_StationThrottle_Submarine = {
        0: "完全停止",
        1: "原地徘徊（悬停）:直升机-自动尝试保持原位、朝向和高度,悬停飞机必须使用最大战斗功率",
        2: "巡航,功率大概为最大战斗功率的75-80%；使用时机：向目标区航行,返航",
        3: "最大战斗功率,油耗大约为巡航的2-3倍；使用时机：起飞和接近攻击目标时",
        4: "加力：不能长时间使用该油门,油耗是巡航时的20倍；afterbuner,加力燃烧室,一般高性能战斗机配备；使用时机：空中格斗,或逃离目标区域",
        5: "滑行"
        }


class CReferencePointDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        m_Side = "string 推演方GUID"
        dLongitude = "double 经度"
        dLatitude = "double 纬度"
        fAltitude = "float 高度"
        m_RelativeToUnit = "string 相对单元guid"
        fRelativeBearing = "float 相对方位角"
        fRelativeDistance = "float 相对距离"
        m_BearingType = "int 方向类型 (枚举量)"
        bIsLocked = "bool 是否锁定"

    m_BearingType = {
        0: "固定的，不随领队朝向变化而变化",
        1: "旋转的，随领队朝向改变旋转"
        }


class CNoNavZoneDict:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        m_Side = "string 所属推演方GUID"
        strDescription = "string 区域描述"
        m_AreaRefPointList = "string 区域的参考点集"
        m_AffectedUnitTypes = "string 单元类型集合"
        bIsActive = "bool 是否启用"
        bIsLocked = "bool 是否已锁"


class CExclusionZone:
    class Info(Enum):
        strName = "string 名称"
        strGuid = "string GUID"
        m_Side = "string 所属推演方GUID"
        strDescription = "string 区域描述"
        m_AreaRefPointList = "string 区域的参考点集"
        m_AffectedUnitTypes = "string 单元类型集合"
        bIsActive = "bool 是否启用"
        m_MarkViolatorAs = "int 推演方立场 (枚举量)"

    m_MarkViolatorAs = {
        0: "中立",
        1: "友方",
        2: "不友好",
        3: "敌对",
        4: "未知"
        }
