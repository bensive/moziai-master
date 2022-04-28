
from mozi_ai_sdk.test.utils.test_framework import TestFramework


class TestDoctrine(TestFramework):
    """测试条令"""

    def test_get_doctrine_owner(self):
        """获取条令所有者"""
        a = self.doctrine.get_doctrine_owner()
        self.assertEqual(a, self.doctrine_owner)

    def test_use_nuclear_weapons(self):
        """战略武器运用-设置授权使用核武器"""
        # 设置授权-使用核武器
        self.doctrine.use_nuclear_weapons('yes')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_Nukes)
        self.doctrine.use_nuclear_weapons('no')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_Nukes)

    def test_set_weapon_control_status(self):
        """交战规则-设置武器控制状态"""
        # 设置对潜自由开火
        self.doctrine.set_weapon_control_status('weapon_control_status_subsurface', 0)
        # 设置对海谨慎开火
        self.doctrine.set_weapon_control_status('weapon_control_status_surface', 1)
        # 设置对地限制开火
        self.doctrine.set_weapon_control_status('weapon_control_status_land', 2)
        # 设置对空限制开火
        self.doctrine.set_weapon_control_status('weapon_control_status_air', 2)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WCS_Submarine)
        self.assertEqual(1, self.doctrine.m_WCS_Surface)
        self.assertEqual(2, self.doctrine.m_WCS_Land)
        self.assertEqual(2, self.doctrine.m_WCS_Air)

    def test_set_weapon_control_status_subsurface(self):
        """交战规则-设置武器控制状态-对潜"""
        # 自由开火
        self.doctrine.set_weapon_control_status_subsurface(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WCS_Submarine)
        # 谨慎开火
        self.doctrine.set_weapon_control_status_subsurface(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WCS_Submarine)
        # 限制开火
        self.doctrine.set_weapon_control_status_subsurface(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WCS_Submarine)

    def test_set_weapon_control_status_surface(self):
        """交战规则-设置武器控制状态-对海"""
        # 自由开火
        self.doctrine.set_weapon_control_status_surface(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WCS_Surface)
        # 谨慎开火
        self.doctrine.set_weapon_control_status_surface(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WCS_Surface)
        # 限制开火
        self.doctrine.set_weapon_control_status_surface(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WCS_Surface)

    def test_set_weapon_control_status_land(self):
        """交战规则-设置武器控制状态-对地"""
        # 自由开火
        self.doctrine.set_weapon_control_status_land(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WCS_Land)
        # 谨慎开火
        self.doctrine.set_weapon_control_status_land(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WCS_Land)
        # 限制开火
        self.doctrine.set_weapon_control_status_land(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WCS_Land)

    def test_set_weapon_control_status_air(self):
        """交战规则-设置武器控制状态-对空"""
        # 自由开火
        self.doctrine.set_weapon_control_status_air(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WCS_Air)
        # 谨慎开火
        self.doctrine.set_weapon_control_status_air(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WCS_Air)
        # 限制开火
        self.doctrine.set_weapon_control_status_air(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WCS_Air)

    def test_ignore_plotted_course(self):
        """交战规则-设置进攻时忽略计划航线"""
        # 进攻时忽略计划航线-是
        self.doctrine.ignore_plotted_course('yes')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_IgnorePlottedCourseWhenAttacking)
        # 进攻时忽略计划航线-否
        self.doctrine.ignore_plotted_course('no')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_IgnorePlottedCourseWhenAttacking)

    def test_set_ambiguous_targets_engaging_status(self):
        """交战规则-设置与模糊位置目标的交战状态"""
        # 忽略模糊性
        self.doctrine.set_ambiguous_targets_engaging_status(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_BehaviorTowardsAmbigousTarget)
        # 乐观决策
        self.doctrine.set_ambiguous_targets_engaging_status(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_BehaviorTowardsAmbigousTarget)
        # 悲观决策
        self.doctrine.set_ambiguous_targets_engaging_status(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_BehaviorTowardsAmbigousTarget)

        # 忽略模糊性
        self.doctrine.set_ambiguous_targets_engaging_status('Ignore')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_BehaviorTowardsAmbigousTarget)
        # 乐观决策
        self.doctrine.set_ambiguous_targets_engaging_status('Optimistic')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_BehaviorTowardsAmbigousTarget)
        # 悲观决策
        self.doctrine.set_ambiguous_targets_engaging_status('Pessimistic')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_BehaviorTowardsAmbigousTarget)

    def test_set_opportunity_targets_engaging_status(self):
        """交战规则-设置与临机目标的交战状态"""
        # 可与任何目标交战
        self.doctrine.set_opportunity_targets_engaging_status('true')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_ShootTourists)
        # 只与任务相关目标交战
        self.doctrine.set_opportunity_targets_engaging_status('false')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_ShootTourists)

    def test_ignore_emcon_while_under_attack(self):
        """电磁管控-设置受到攻击时是否忽略电磁管控"""
        # 不忽略
        self.doctrine.ignore_emcon_while_under_attack('false')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_IgnoreEMCONUnderAttack)
        # 忽略
        self.doctrine.ignore_emcon_while_under_attack('true')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_IgnoreEMCONUnderAttack)

    def test_use_kinematic_range_for_torpedoes(self):
        """杂项-设置决定如何使用鱼雷的动力航程"""
        # 仅手动开火下使用
        self.doctrine.use_kinematic_range_for_torpedoes(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_UseTorpedoesKinematicRange)
        # 手动自动开火下都使用
        self.doctrine.use_kinematic_range_for_torpedoes(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_UseTorpedoesKinematicRange)
        # 实际航程
        self.doctrine.use_kinematic_range_for_torpedoes(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_UseTorpedoesKinematicRange)

        # TODO 字符串不起作用，暂时注释掉
        # 仅手动开火下使用
        # self.doctrine.use_kinematic_range_for_torpedoes('AutomaticAndManualFire')
        # self.env.step()
        # self.assertEqual(0, self.doctrine.m_UseTorpedoesKinematicRange)
        # # 手动自动开火下都使用
        # self.doctrine.use_kinematic_range_for_torpedoes('ManualFireOnly')
        # self.env.step()
        # self.assertEqual(1, self.doctrine.m_UseTorpedoesKinematicRange)
        # # 实际航程
        # self.doctrine.use_kinematic_range_for_torpedoes('No')
        # self.env.step()
        # self.assertEqual(2, self.doctrine.m_UseTorpedoesKinematicRange)

    def test_evade_automatically(self):
        """杂项-设置是否自动规避"""
        # 否
        self.doctrine.evade_automatically('false')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_AutomaticEvasion)
        # 是
        self.doctrine.evade_automatically('true')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_AutomaticEvasion)

    def test_use_refuel_supply(self):
        """杂项-设置是否允许加油补给"""
        # 允许
        self.doctrine.use_refuel_supply(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_UseRefuel)
        # 允许但禁止加油机相互加油
        self.doctrine.use_refuel_supply(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_UseRefuel)
        # 不允许
        self.doctrine.use_refuel_supply(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_UseRefuel)

    def test_select_refuel_supply_object(self):
        """杂项-设置加油补给的选择对象"""
        # 优先选择敌我之间的加油机并禁止回飞
        self.doctrine.select_refuel_supply_object(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_RefuelSelection)
        # 选择最近的加油机
        self.doctrine.select_refuel_supply_object(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RefuelSelection)
        # 选择敌我之间的加油机
        self.doctrine.select_refuel_supply_object(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_RefuelSelection)

    def test_refuel_supply_allies(self):
        """杂项-设置是否给盟军单元加油补给"""
        # 否
        self.doctrine.refuel_supply_allies(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_RefuelAllies)
        # 是
        self.doctrine.refuel_supply_allies(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RefuelAllies)
        # 是且仅接受
        self.doctrine.refuel_supply_allies(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_RefuelAllies)
        # 是且仅供给
        self.doctrine.refuel_supply_allies(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_RefuelAllies)

    def test_set_air_operations_tempo(self):
        """空中作战行动-设置空战节奏"""
        # 快速出动 (高强度出动) 大批出动
        self.doctrine.set_air_operations_tempo(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_AirOpsTempo)
        # 一般强度出动
        self.doctrine.set_air_operations_tempo(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_AirOpsTempo)

        # 快速出动 (高强度出动) 大批出动
        self.doctrine.set_air_operations_tempo('Surge')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_AirOpsTempo)
        # 一般强度出动
        self.doctrine.set_air_operations_tempo('Sustained')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_AirOpsTempo)

    def test_quick_turnaround_for_aircraft(self):
        """空中作战行动-设置是否快速出动飞机"""
        # 否
        self.doctrine.quick_turnaround_for_aircraft(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_QuickTurnAround)
        # 是
        self.doctrine.quick_turnaround_for_aircraft(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_QuickTurnAround)
        # 战斗机与反潜机快速出动(战斗机与反潜战挂载)
        self.doctrine.quick_turnaround_for_aircraft(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_QuickTurnAround)

        # 否
        self.doctrine.quick_turnaround_for_aircraft('No')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_QuickTurnAround)
        # 是
        self.doctrine.quick_turnaround_for_aircraft('Yes')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_QuickTurnAround)
        # 战斗机与反潜机快速出动(战斗机与反潜战挂载)
        self.doctrine.quick_turnaround_for_aircraft('Yes_FighterAndASWLoadoutOnly')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_QuickTurnAround)

    def test_set_fuel_state_for_aircraft(self):
        """空中作战行动-设置单架飞机返航的油料状态"""
        # 剩下计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_BingoJoker)
        # 剩下1.1倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_BingoJoker)
        # 剩下1.2倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_BingoJoker)
        # 剩下1.25倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_BingoJoker)
        # 剩下1.3倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(4)
        self.env.step()
        self.assertEqual(4, self.doctrine.m_BingoJoker)
        # 剩下1.4倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(5)
        self.env.step()
        self.assertEqual(5, self.doctrine.m_BingoJoker)
        # 剩下1.5倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(6)
        self.env.step()
        self.assertEqual(6, self.doctrine.m_BingoJoker)
        # 剩下1.6倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(7)
        self.env.step()
        self.assertEqual(7, self.doctrine.m_BingoJoker)
        # 剩下1.7倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(8)
        self.env.step()
        self.assertEqual(8, self.doctrine.m_BingoJoker)
        # 剩下1.75倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(9)
        self.env.step()
        self.assertEqual(9, self.doctrine.m_BingoJoker)
        # 剩下1.8倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(10)
        self.env.step()
        self.assertEqual(10, self.doctrine.m_BingoJoker)
        # 剩下1.9倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft(11)
        self.env.step()
        self.assertEqual(11, self.doctrine.m_BingoJoker)

        # 剩下计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Bingo')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_BingoJoker)
        # 剩下1.1倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker10Percent')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_BingoJoker)
        # 剩下1.2倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker20Percent')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_BingoJoker)
        # 剩下1.25倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker25Percent')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_BingoJoker)
        # 剩下1.3倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker30Percent')
        self.env.step()
        self.assertEqual(4, self.doctrine.m_BingoJoker)
        # 剩下1.4倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker40Percent')
        self.env.step()
        self.assertEqual(5, self.doctrine.m_BingoJoker)
        # 剩下1.5倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker50Percent')
        self.env.step()
        self.assertEqual(6, self.doctrine.m_BingoJoker)
        # 剩下1.6倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker60Percent')
        self.env.step()
        self.assertEqual(7, self.doctrine.m_BingoJoker)
        # 剩下1.7倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker70Percent')
        self.env.step()
        self.assertEqual(8, self.doctrine.m_BingoJoker)
        # 剩下1.75倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker75Percent')
        self.env.step()
        self.assertEqual(9, self.doctrine.m_BingoJoker)
        # 剩下1.8倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker80Percent')
        self.env.step()
        self.assertEqual(10, self.doctrine.m_BingoJoker)
        # 剩下1.9倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker90Percent')
        self.env.step()
        self.assertEqual(11, self.doctrine.m_BingoJoker)

    def test_set_fuel_state_for_air_group(self):
        """空中作战行动-设置飞行编队返航的油料状态"""
        # 无约束，编队不返航
        self.doctrine.set_fuel_state_for_air_group(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_BingoJokerRTB)
        # 编队中所有飞机均因达到单机油料状态要返航时，编队才返航
        self.doctrine.set_fuel_state_for_air_group(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_BingoJokerRTB)
        # 编队中任意一架飞机达到单机油料状态要返航时，编队就返航
        self.doctrine.set_fuel_state_for_air_group(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_BingoJokerRTB)
        # 编队中任意一架飞机达到单机油料状态要返航时，其可离队返航
        self.doctrine.set_fuel_state_for_air_group(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_BingoJokerRTB)

        # 无约束，编队不返航
        self.doctrine.set_fuel_state_for_air_group('No')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_BingoJokerRTB)
        # 编队中所有飞机均因达到单机油料状态要返航时，编队才返航
        self.doctrine.set_fuel_state_for_air_group('YesLastUnit')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_BingoJokerRTB)
        # 编队中任意一架飞机达到单机油料状态要返航时，编队就返航
        self.doctrine.set_fuel_state_for_air_group('YesFirstUnit')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_BingoJokerRTB)
        # 编队中任意一架飞机达到单机油料状态要返航时，其可离队返航
        self.doctrine.set_fuel_state_for_air_group('YesLeaveGroup')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_BingoJokerRTB)

    def test_set_weapon_state_for_aircraft(self):
        """空中作战行动-设置单架飞机的武器状态"""
        # '0'-使用挂载设置
        self.doctrine.set_weapon_state_for_aircraft(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WeaponState)
        # '2001' - 任务武器已耗光，立即脱离战斗,
        self.doctrine.set_weapon_state_for_aircraft(2001)
        self.env.step()
        self.assertEqual(2001, self.doctrine.m_WeaponState)
        # '2002' - 任务武器已耗光.允许使用航炮对临机目标进行打击（推荐）,
        self.doctrine.set_weapon_state_for_aircraft(2002)
        self.env.step()
        self.assertEqual(2002, self.doctrine.m_WeaponState)
        # '3001' - 所有超视距与防区外打击武器已经耗光.立即脱离战斗,
        self.doctrine.set_weapon_state_for_aircraft(3001)
        self.env.step()
        self.assertEqual(3001, self.doctrine.m_WeaponState)
        # '3002' - 所有超视距与防区外打击武器已经耗光.允许使用视距内或防区内打击武器对较易攻击的临机出现目标进行攻击.不使用航炮,
        self.doctrine.set_weapon_state_for_aircraft(3002)
        self.env.step()
        self.assertEqual(3002, self.doctrine.m_WeaponState)
        # '3003' - 所有超视距与防区外打击武器已经耗光.允许使用视距内、防区内打击武器或者航炮对较易攻击的临机出现目标进行攻击,
        self.doctrine.set_weapon_state_for_aircraft(3003)
        self.env.step()
        self.assertEqual(3003, self.doctrine.m_WeaponState)
        # '5001' - 使用超视距或防区外打击武器进行一次交战.立即脱离战斗,
        self.doctrine.set_weapon_state_for_aircraft(5001)
        self.env.step()
        self.assertEqual(5001, self.doctrine.m_WeaponState)
        # '5002' - 使用超视距或防区外打击武器进行一次交战.允许使用视距内或防区内打击武器对较易攻击的临机出现目标进行攻击.不使用航炮,
        self.doctrine.set_weapon_state_for_aircraft(5002)
        self.env.step()
        self.assertEqual(5002, self.doctrine.m_WeaponState)
        # '5003' - 使用超视距或防区外打击武器进行一次交战.允许使用视距内、防区内打击武器或者航炮对较易攻击的临机出现目标进行攻击,
        self.doctrine.set_weapon_state_for_aircraft(5003)
        self.env.step()
        self.assertEqual(5003, self.doctrine.m_WeaponState)
        # '5005' - 同时使用超视距 / 视距内或防区外 / 防区内打击武器进行一次交战.不使用航炮,
        self.doctrine.set_weapon_state_for_aircraft(5005)
        self.env.step()
        self.assertEqual(5005, self.doctrine.m_WeaponState)
        # '5006' - 同时使用超视距 / 视距内或防区外 / 防区内打击武器进行一次交战.允许使用航炮对较易攻击的临机出现目标进行攻击,
        self.doctrine.set_weapon_state_for_aircraft(5006)
        self.env.step()
        self.assertEqual(5006, self.doctrine.m_WeaponState)
        # '5011' - 使用视距内或防区内打击武器进行一次交战.立即脱离战斗,
        self.doctrine.set_weapon_state_for_aircraft(5011)
        self.env.step()
        self.assertEqual(5011, self.doctrine.m_WeaponState)
        # '5012' - 使用视距内或防区内打击武器进行一次交战.允许使用航炮与临机出现目标格斗,
        self.doctrine.set_weapon_state_for_aircraft(5012)
        self.env.step()
        self.assertEqual(5012, self.doctrine.m_WeaponState)
        # '5021' - 使用航炮进行一次交战:
        self.doctrine.set_weapon_state_for_aircraft(5021)
        self.env.step()
        self.assertEqual(5021, self.doctrine.m_WeaponState)
        # '4001' - 25 % 相关武器已经耗光.立即脱离战斗,
        self.doctrine.set_weapon_state_for_aircraft(4001)
        self.env.step()
        self.assertEqual(4001, self.doctrine.m_WeaponState)
        # '4002' - 25 % 相关武器已经耗光.允许与临机出现目标交战，包括航炮,
        self.doctrine.set_weapon_state_for_aircraft(4002)
        self.env.step()
        self.assertEqual(4002, self.doctrine.m_WeaponState)
        # '4011' - 50 % 相关武器已经耗光.立即脱离战斗
        self.doctrine.set_weapon_state_for_aircraft(4011)
        self.env.step()
        self.assertEqual(4011, self.doctrine.m_WeaponState)
        # '4012' - 50 % 相关武器已经耗光.允许与临机出现目标交战，包括航炮
        self.doctrine.set_weapon_state_for_aircraft(4012)
        self.env.step()
        self.assertEqual(4012, self.doctrine.m_WeaponState)
        # '4021' - 75 % 相关武器已经耗光.立即脱离战斗
        self.doctrine.set_weapon_state_for_aircraft(4021)
        self.env.step()
        self.assertEqual(4021, self.doctrine.m_WeaponState)
        # '4022' - 75 % 相关武器已经耗光.允许与临机出现目标交战，包括航炮: 4022
        self.doctrine.set_weapon_state_for_aircraft(4022)
        self.env.step()
        self.assertEqual(4022, self.doctrine.m_WeaponState)

    def test_set_weapon_state_for_air_group(self):
        """空中作战行动-设置飞行编队的武器状态"""
        # 无约束，编队不返航
        self.doctrine.set_weapon_state_for_air_group(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WeaponStateRTB)
        # 编队中所有飞机均因达到单机武器状态要返航时，编队才返航
        self.doctrine.set_weapon_state_for_air_group(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WeaponStateRTB)
        # 编队中任意一架飞机达到单机武器状态要返航时，编队就返航
        self.doctrine.set_weapon_state_for_air_group(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WeaponStateRTB)
        # 编队中任意一架飞机达到单机武器状态要返航时，其可离队返航
        self.doctrine.set_weapon_state_for_air_group(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_WeaponStateRTB)

        # 无约束，编队不返航
        self.doctrine.set_weapon_state_for_air_group('No')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WeaponStateRTB)
        # 编队中所有飞机均因达到单机武器状态要返航时，编队才返航
        self.doctrine.set_weapon_state_for_air_group('YesLastUnit')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WeaponStateRTB)
        # 编队中任意一架飞机达到单机武器状态要返航时，编队就返航
        self.doctrine.set_weapon_state_for_air_group('YesFirstUnit')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WeaponStateRTB)
        # 编队中任意一架飞机达到单机武器状态要返航时，其可离队返航
        self.doctrine.set_weapon_state_for_air_group('YesLeaveGroup')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_WeaponStateRTB)

    def test_gun_strafe_for_aircraft(self):
        """空中作战行动-设置是否用航炮扫射"""
        # 是
        self.doctrine.gun_strafe_for_aircraft(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_GunStrafeGroundTargets)
        # 否
        self.doctrine.gun_strafe_for_aircraft(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_GunStrafeGroundTargets)

        # 是
        self.doctrine.gun_strafe_for_aircraft('Yes')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_GunStrafeGroundTargets)
        # 否
        self.doctrine.gun_strafe_for_aircraft('No')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_GunStrafeGroundTargets)

    def test_jettison_ordnance_for_aircraft(self):
        """空中作战行动-设置是否抛弃弹药"""
        # 是 （受到攻击时抛弃弹药）
        self.doctrine.jettison_ordnance_for_aircraft(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_JettisonOrdnance)
        # 否
        self.doctrine.jettison_ordnance_for_aircraft(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_JettisonOrdnance)

        # 是 （受到攻击时抛弃弹药）
        self.doctrine.jettison_ordnance_for_aircraft('Yes')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_JettisonOrdnance)
        # 否
        self.doctrine.jettison_ordnance_for_aircraft('No')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_JettisonOrdnance)

    def test_use_sams_to_anti_surface(self):
        """反舰作战行动-设置是否以反舰模式使用舰空导弹"""
        # 是
        self.doctrine.use_sams_to_anti_surface('true')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_SAM_ASUW)
        # 否
        self.doctrine.use_sams_to_anti_surface('false')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_SAM_ASUW)

    def test_maintain_standoff(self):
        """反舰作战行动-设置是否与目标保持距离"""
        # 否
        self.doctrine.maintain_standoff('false')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_MaintainStandoff)
        # 是
        self.doctrine.maintain_standoff('true')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_MaintainStandoff)

    def test_avoid_being_searched_for_submarine(self):
        """反潜作战行动-设置潜艇是否规避搜索"""
        # 否
        self.doctrine.avoid_being_searched_for_submarine(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_AvoidContact)
        # 除非自卫均是（是，除非自防御）
        self.doctrine.avoid_being_searched_for_submarine(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_AvoidContact)
        # 总是
        self.doctrine.avoid_being_searched_for_submarine(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_AvoidContact)

        # 否
        self.doctrine.avoid_being_searched_for_submarine('No')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_AvoidContact)
        # 除非自卫均是（是，除非自防御）
        self.doctrine.avoid_being_searched_for_submarine('Yes_ExceptSelfDefence')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_AvoidContact)
        # 总是
        self.doctrine.avoid_being_searched_for_submarine('Yes_Always')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_AvoidContact)

    def test_dive_on_threat(self):
        """反潜作战行动-设置潜艇探测到威胁时是否下潜"""
        # 在敌潜望镜或对面搜索雷达侦察时下潜
        self.doctrine.dive_on_threat(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_DiveWhenThreatsDetected)
        # 在敌电子侦察措施侦察或目标接近时下潜
        self.doctrine.dive_on_threat(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_DiveWhenThreatsDetected)
        # 在20海里内有敌舰或30海里内有敌机时下潜
        self.doctrine.dive_on_threat(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_DiveWhenThreatsDetected)
        # 否
        self.doctrine.dive_on_threat(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_DiveWhenThreatsDetected)

        # 在敌潜望镜或对面搜索雷达侦察时下潜
        self.doctrine.dive_on_threat('Yes')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_DiveWhenThreatsDetected)
        # 在敌电子侦察措施侦察或目标接近时下潜
        self.doctrine.dive_on_threat('Yes_ESM_Only')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_DiveWhenThreatsDetected)
        # 在20海里内有敌舰或30海里内有敌机时下潜
        self.doctrine.dive_on_threat('Yes_Ships20nm_Aircraft30nm')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_DiveWhenThreatsDetected)
        # 否
        self.doctrine.dive_on_threat('No')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_DiveWhenThreatsDetected)

    def test_set_recharging_condition_on_patrol(self):
        """反潜作战行动-设置潜艇出航或阵位再充电条件"""
        # 电量用完再充
        self.doctrine.set_recharging_condition_on_patrol(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下10%时再充
        self.doctrine.set_recharging_condition_on_patrol(10)
        self.env.step()
        self.assertEqual(10, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下20%时再充
        self.doctrine.set_recharging_condition_on_patrol(20)
        self.env.step()
        self.assertEqual(20, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下30%时再充
        self.doctrine.set_recharging_condition_on_patrol(30)
        self.env.step()
        self.assertEqual(30, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下40%时再充
        self.doctrine.set_recharging_condition_on_patrol(40)
        self.env.step()
        self.assertEqual(40, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下50%时再充
        self.doctrine.set_recharging_condition_on_patrol(50)
        self.env.step()
        self.assertEqual(50, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下60%时再充
        self.doctrine.set_recharging_condition_on_patrol(60)
        self.env.step()
        self.assertEqual(60, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下70%时再充
        self.doctrine.set_recharging_condition_on_patrol(70)
        self.env.step()
        self.assertEqual(70, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下80%时再充
        self.doctrine.set_recharging_condition_on_patrol(80)
        self.env.step()
        self.assertEqual(80, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下90%时再充
        self.doctrine.set_recharging_condition_on_patrol(90)
        self.env.step()
        self.assertEqual(90, self.doctrine.m_RechargePercentagePatrol)

        # 电量用完再充
        self.doctrine.set_recharging_condition_on_patrol('Recharge_Empty')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下10%时再充
        self.doctrine.set_recharging_condition_on_patrol('Recharge_10_Percent')
        self.env.step()
        self.assertEqual(10, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下20%时再充
        self.doctrine.set_recharging_condition_on_patrol('Recharge_20_Percent')
        self.env.step()
        self.assertEqual(20, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下30%时再充
        self.doctrine.set_recharging_condition_on_patrol('Recharge_30_Percent')
        self.env.step()
        self.assertEqual(30, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下40%时再充
        self.doctrine.set_recharging_condition_on_patrol('Recharge_40_Percent')
        self.env.step()
        self.assertEqual(40, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下50%时再充
        self.doctrine.set_recharging_condition_on_patrol('Recharge_50_Percent')
        self.env.step()
        self.assertEqual(50, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下60%时再充
        self.doctrine.set_recharging_condition_on_patrol('Recharge_60_Percent')
        self.env.step()
        self.assertEqual(60, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下70%时再充
        self.doctrine.set_recharging_condition_on_patrol('Recharge_70_Percent')
        self.env.step()
        self.assertEqual(70, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下80%时再充
        self.doctrine.set_recharging_condition_on_patrol('Recharge_80_Percent')
        self.env.step()
        self.assertEqual(80, self.doctrine.m_RechargePercentagePatrol)
        # 电量剩下90%时再充
        self.doctrine.set_recharging_condition_on_patrol('Recharge_90_Percent')
        self.env.step()
        self.assertEqual(90, self.doctrine.m_RechargePercentagePatrol)

    def test_set_recharging_condition_on_attack(self):
        """反潜作战行动-设置潜艇进攻或防御再充电条件"""
        # 电量用完再充
        self.doctrine.set_recharging_condition_on_attack(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下10%时再充
        self.doctrine.set_recharging_condition_on_attack(10)
        self.env.step()
        self.assertEqual(10, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下20%时再充
        self.doctrine.set_recharging_condition_on_attack(20)
        self.env.step()
        self.assertEqual(20, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下30%时再充
        self.doctrine.set_recharging_condition_on_attack(30)
        self.env.step()
        self.assertEqual(30, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下40%时再充
        self.doctrine.set_recharging_condition_on_attack(40)
        self.env.step()
        self.assertEqual(40, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下50%时再充
        self.doctrine.set_recharging_condition_on_attack(50)
        self.env.step()
        self.assertEqual(50, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下60%时再充
        self.doctrine.set_recharging_condition_on_attack(60)
        self.env.step()
        self.assertEqual(60, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下70%时再充
        self.doctrine.set_recharging_condition_on_attack(70)
        self.env.step()
        self.assertEqual(70, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下80%时再充
        self.doctrine.set_recharging_condition_on_attack(80)
        self.env.step()
        self.assertEqual(80, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下90%时再充
        self.doctrine.set_recharging_condition_on_attack(90)
        self.env.step()
        self.assertEqual(90, self.doctrine.m_RechargePercentageAttack)

        # 电量用完再充
        self.doctrine.set_recharging_condition_on_attack('Recharge_Empty')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下10%时再充
        self.doctrine.set_recharging_condition_on_attack('Recharge_10_Percent')
        self.env.step()
        self.assertEqual(10, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下20%时再充
        self.doctrine.set_recharging_condition_on_attack('Recharge_20_Percent')
        self.env.step()
        self.assertEqual(20, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下30%时再充
        self.doctrine.set_recharging_condition_on_attack('Recharge_30_Percent')
        self.env.step()
        self.assertEqual(30, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下40%时再充
        self.doctrine.set_recharging_condition_on_attack('Recharge_40_Percent')
        self.env.step()
        self.assertEqual(40, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下50%时再充
        self.doctrine.set_recharging_condition_on_attack('Recharge_50_Percent')
        self.env.step()
        self.assertEqual(50, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下60%时再充
        self.doctrine.set_recharging_condition_on_attack('Recharge_60_Percent')
        self.env.step()
        self.assertEqual(60, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下70%时再充
        self.doctrine.set_recharging_condition_on_attack('Recharge_70_Percent')
        self.env.step()
        self.assertEqual(70, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下80%时再充
        self.doctrine.set_recharging_condition_on_attack('Recharge_80_Percent')
        self.env.step()
        self.assertEqual(80, self.doctrine.m_RechargePercentageAttack)
        # 电量剩下90%时再充
        self.doctrine.set_recharging_condition_on_attack('Recharge_90_Percent')
        self.env.step()
        self.assertEqual(90, self.doctrine.m_RechargePercentageAttack)

    def test_use_aip(self):
        """反潜作战行动-设置潜艇是否使用“不依赖空气推进”系统"""
        # 否
        self.doctrine.use_aip(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_AIPUsage)
        # 在进攻或防御时使用
        self.doctrine.use_aip(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_AIPUsage)
        # 总是
        self.doctrine.use_aip(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_AIPUsage)

        # 否
        self.doctrine.use_aip('No')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_AIPUsage)
        # 在进攻或防御时使用
        self.doctrine.use_aip('Yes_AttackOnly')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_AIPUsage)
        # 总是
        self.doctrine.use_aip('Yes_Always')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_AIPUsage)

    def test_use_dipping_sonar(self):
        """反潜作战行动-设置是否使用吊放声呐"""
        # 只能人工使用或者分配到任务
        self.doctrine.use_dipping_sonar(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_DippingSonar)
        # 自动到150英尺悬停并使用
        self.doctrine.use_dipping_sonar(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_DippingSonar)

        # 只能人工使用或者分配到任务
        self.doctrine.use_dipping_sonar('ManualAndMissionOnly')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_DippingSonar)
        # 自动到150英尺悬停并使用
        self.doctrine.use_dipping_sonar('Automatically_HoverAnd150ft')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_DippingSonar)

    def test_set_em_control_status(self):
        """电磁管控设置-设置电磁管控状态"""
        # 雷达打开
        self.doctrine.set_em_control_status('Radar', 'Active')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_EMCON_SettingsForRadar)
        # 雷达静默
        self.doctrine.set_em_control_status('Radar', 'Passive')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_EMCON_SettingsForRadar)
        # 声呐打开
        self.doctrine.set_em_control_status('Sonar', 'Active')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_EMCON_SettingsForSonar)
        # 声呐静默
        self.doctrine.set_em_control_status('Sonar', 'Passive')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_EMCON_SettingsForSonar)
        # 干扰机打开
        self.doctrine.set_em_control_status('OECM', 'Active')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_EMCON_SettingsForOECM)
        # 干扰机静默
        self.doctrine.set_em_control_status('OECM', 'Passive')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_EMCON_SettingsForOECM)

    def test_set_weapon_release_authority(self):
        """武器使用规则"""
        # 设置条令的武器使用规则
        # weapon_dbid: {str: 武器的数据库ID}
        # target_type: {str: 目标类型号}
        # quantity_salvo: {str: 'n' - 齐射武器数, 'inherit' - 继承设置, 'max' - 全量齐射, 'none' - 禁用}
        # shooter_salvo: {str: 'n' - 齐射发射架数，'inherit' - 继承设置, 'max' - 全量齐射}
        # firing_range: {str: 'n' - 自动开火距离，'inherit' - 继承设置, 'none' - 禁用自动开火}
        # self_defense: {str: 'n' - 自动防御距离, 'inherit' - 继承设置, 'max' - 最大射程射击, 'none' - 禁用自卫}
        # escort: {str: 'true' - 护航任务, 'false' - 非护航任务}

        # 武器：AIM-120D型先进中程空空导弹 P3I.4
        # 目标类型号：五代机
        self.doctrine.set_weapon_release_authority(weapon_dbid='15', target_type='2001', quantity_salvo=1,
                                                   shooter_salvo=1, firing_range='max', self_defense='max',
                                                   escort='')
        self.env.step()
        self.doctrine.set_weapon_release_authority(weapon_dbid='15', target_type='2001',
                                                   quantity_salvo='none', shooter_salvo=1,
                                                   firing_range='none', self_defense='none', escort='')
        self.env.step()
        self.doctrine.set_weapon_release_authority(weapon_dbid='15', target_type='2001',
                                                   quantity_salvo='max', shooter_salvo='max',
                                                   firing_range='max', self_defense='max', escort='')
        self.env.step()
        print(self.doctrine.m_WRA_WeaponRule)
        self.doctrine.set_weapon_release_authority(weapon_dbid='15', target_type='2001',
                                                   quantity_salvo='inherit', shooter_salvo='inherit',
                                                   firing_range='inherit', self_defense='inherit', escort='')
        self.env.step()
        self.doctrine.set_weapon_release_authority(weapon_dbid='15', target_type='2001',
                                                   quantity_salvo=3, shooter_salvo=4,
                                                   firing_range=5, self_defense=5, escort='')
        self.env.step()
        self.assertTrue(False)

    def test_withdraw_on_damage(self):
        """撤退与部署-设置导致撤退的毁伤程度"""
        # 忽略毁伤不撤退
        self.doctrine.withdraw_on_damage(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WithdrawDamageThreshold)
        # 毁伤大于5%撤退
        self.doctrine.withdraw_on_damage(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WithdrawDamageThreshold)
        # 毁伤大于25%撤退
        self.doctrine.withdraw_on_damage(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WithdrawDamageThreshold)
        # 毁伤大于50%撤退
        self.doctrine.withdraw_on_damage(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_WithdrawDamageThreshold)
        # 毁伤大于75%撤退
        self.doctrine.withdraw_on_damage(4)
        self.env.step()
        self.assertEqual(4, self.doctrine.m_WithdrawDamageThreshold)

        # 忽略毁伤不撤退
        self.doctrine.withdraw_on_damage('Ignore')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WithdrawDamageThreshold)
        # 毁伤大于5%撤退
        self.doctrine.withdraw_on_damage('Percent5')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WithdrawDamageThreshold)
        # 毁伤大于25%撤退
        self.doctrine.withdraw_on_damage('Percent25')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WithdrawDamageThreshold)
        # 毁伤大于50%撤退
        self.doctrine.withdraw_on_damage('Percent50')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_WithdrawDamageThreshold)
        # 毁伤大于75%撤退
        self.doctrine.withdraw_on_damage('Percent75')
        self.env.step()
        self.assertEqual(4, self.doctrine.m_WithdrawDamageThreshold)

    def test_withdraw_on_fuel(self):
        """撤退与部署-设置导致撤退的油量多少"""
        # 忽略油量不撤退
        self.doctrine.withdraw_on_fuel(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WithdrawFuelThreshold)
        # 少于计划储备油量时撤退
        self.doctrine.withdraw_on_fuel(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WithdrawFuelThreshold)
        # 少于25%时撤退
        self.doctrine.withdraw_on_fuel(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WithdrawFuelThreshold)
        # 少于50%时撤退
        self.doctrine.withdraw_on_fuel(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_WithdrawFuelThreshold)
        # 少于75%时即撤退
        self.doctrine.withdraw_on_fuel(4)
        self.env.step()
        self.assertEqual(4, self.doctrine.m_WithdrawFuelThreshold)

        # 忽略油量不撤退
        self.doctrine.withdraw_on_fuel('Ignore')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WithdrawFuelThreshold)
        # 少于计划储备油量时撤退
        self.doctrine.withdraw_on_fuel('Bingo')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WithdrawFuelThreshold)
        # 少于25%时撤退
        self.doctrine.withdraw_on_fuel('Percent25')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WithdrawFuelThreshold)
        # 少于50%时撤退
        self.doctrine.withdraw_on_fuel('Percent50')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_WithdrawFuelThreshold)
        # 少于75%时即撤退
        self.doctrine.withdraw_on_fuel('Percent75')
        self.env.step()
        self.assertEqual(4, self.doctrine.m_WithdrawFuelThreshold)

    def test_withdraw_on_attack_weapon(self):
        """撤退与部署-设置导致撤退的主攻武器量"""
        # 忽略武器量不撤退
        self.doctrine.withdraw_on_attack_weapon(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WithdrawAttackThreshold)
        # 打光才撤
        self.doctrine.withdraw_on_attack_weapon(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WithdrawAttackThreshold)
        # 主攻武器量消耗到25%时撤退
        self.doctrine.withdraw_on_attack_weapon(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WithdrawAttackThreshold)
        # 主攻武器量消耗到50%时撤退
        self.doctrine.withdraw_on_attack_weapon(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_WithdrawAttackThreshold)
        # 主攻武器量消耗到75%时撤退
        self.doctrine.withdraw_on_attack_weapon(4)
        self.env.step()
        self.assertEqual(4, self.doctrine.m_WithdrawAttackThreshold)

        # 忽略武器量不撤退
        self.doctrine.withdraw_on_attack_weapon('Ignore')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WithdrawAttackThreshold)
        # 打光才撤
        self.doctrine.withdraw_on_attack_weapon('Exhausted')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WithdrawAttackThreshold)
        # 主攻武器量消耗到25%时撤退
        self.doctrine.withdraw_on_attack_weapon('Percent25')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WithdrawAttackThreshold)
        # 主攻武器量消耗到50%时撤退
        self.doctrine.withdraw_on_attack_weapon('Percent50')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_WithdrawAttackThreshold)
        # 主攻武器量消耗到75%时撤退
        self.doctrine.withdraw_on_attack_weapon('Percent75')
        self.env.step()
        self.assertEqual(4, self.doctrine.m_WithdrawAttackThreshold)

    def test_withdraw_on_defence_weapon(self):
        """撤退与部署-设置导致撤退的主防武器量"""
        # 忽略武器量不撤退
        self.doctrine.withdraw_on_defence_weapon(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WithdrawDefenceThreshold)
        # 打光才撤
        self.doctrine.withdraw_on_defence_weapon(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WithdrawDefenceThreshold)
        # 主防武器量消耗到25%时撤退
        self.doctrine.withdraw_on_defence_weapon(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WithdrawDefenceThreshold)
        # 主防武器量消耗到50%时撤退
        self.doctrine.withdraw_on_defence_weapon(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_WithdrawDefenceThreshold)
        # 主防武器量消耗到75%时撤退
        self.doctrine.withdraw_on_defence_weapon(4)
        self.env.step()
        self.assertEqual(4, self.doctrine.m_WithdrawDefenceThreshold)

        # 忽略武器量不撤退
        self.doctrine.withdraw_on_defence_weapon('Ignore')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_WithdrawDefenceThreshold)
        # 打光才撤
        self.doctrine.withdraw_on_defence_weapon('Exhausted')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_WithdrawDefenceThreshold)
        # 主防武器量消耗到25%时撤退
        self.doctrine.withdraw_on_defence_weapon('Percent25')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_WithdrawDefenceThreshold)
        # 主防武器量消耗到50%时撤退
        self.doctrine.withdraw_on_defence_weapon('Percent50')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_WithdrawDefenceThreshold)
        # 主防武器量消耗到75%时撤退
        self.doctrine.withdraw_on_defence_weapon('Percent75')
        self.env.step()
        self.assertEqual(4, self.doctrine.m_WithdrawDefenceThreshold)

    def test_redeploy_on_damage(self):
        """撤退与部署-设置导致重新部署的毁伤程度"""
        # 忽略毁伤不撤退
        self.doctrine.redeploy_on_damage(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RedeployDamageThreshold)
        # 毁伤大于5%撤退
        self.doctrine.redeploy_on_damage(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_RedeployDamageThreshold)
        # 毁伤大于25%撤退
        self.doctrine.redeploy_on_damage(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_RedeployDamageThreshold)
        # 毁伤大于50%撤退
        self.doctrine.redeploy_on_damage(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_RedeployDamageThreshold)
        # 毁伤大于75%撤退
        self.doctrine.redeploy_on_damage(4)
        self.env.step()
        self.assertEqual(4, self.doctrine.m_RedeployDamageThreshold)

        # 忽略毁伤不撤退
        self.doctrine.redeploy_on_damage('Ignore')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RedeployDamageThreshold)
        # 毁伤大于5%撤退
        self.doctrine.redeploy_on_damage('Percent5')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_RedeployDamageThreshold)
        # 毁伤大于25%撤退
        self.doctrine.redeploy_on_damage('Percent25')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_RedeployDamageThreshold)
        # 毁伤大于50%撤退
        self.doctrine.redeploy_on_damage('Percent50')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_RedeployDamageThreshold)
        # 毁伤大于75%撤退
        self.doctrine.redeploy_on_damage('Percent75')
        self.env.step()
        self.assertEqual(4, self.doctrine.m_RedeployDamageThreshold)

    def test_redeploy_on_fuel(self):
        """撤退与部署-设置导致重新部署的油量多少"""
        # 忽略油量不撤退
        self.doctrine.redeploy_on_fuel(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RedeployFuelThreshold)
        # 少于计划储备油量时撤退
        self.doctrine.redeploy_on_fuel(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_RedeployFuelThreshold)
        # 少于25%时撤退
        self.doctrine.redeploy_on_fuel(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_RedeployFuelThreshold)
        # 少于50%时撤退
        self.doctrine.redeploy_on_fuel(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_RedeployFuelThreshold)
        # 少于75%时即撤退
        self.doctrine.redeploy_on_fuel(4)
        self.env.step()
        self.assertEqual(4, self.doctrine.m_RedeployFuelThreshold)

        # 忽略油量不撤退
        self.doctrine.redeploy_on_fuel('Ignore')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RedeployFuelThreshold)
        # 少于计划储备油量时撤退
        self.doctrine.redeploy_on_fuel('Bingo')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_RedeployFuelThreshold)
        # 少于25%时撤退
        self.doctrine.redeploy_on_fuel('Percent25')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_RedeployFuelThreshold)
        # 少于50%时撤退
        self.doctrine.redeploy_on_fuel('Percent50')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_RedeployFuelThreshold)
        # 少于75%时即撤退
        self.doctrine.redeploy_on_fuel('Percent75')
        self.env.step()
        self.assertEqual(4, self.doctrine.m_RedeployFuelThreshold)

    def test_redeploy_on_attack_weapon(self):
        """撤退与部署-设置导致重新部署的主攻武器量"""
        # 忽略武器量不重新部署
        self.doctrine.redeploy_on_attack_weapon(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RedeployAttackDamageThreshold)
        # 打光才重新部署
        self.doctrine.redeploy_on_attack_weapon(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_RedeployAttackDamageThreshold)
        # 主攻武器量消耗到25%时重新部署
        self.doctrine.redeploy_on_attack_weapon(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_RedeployAttackDamageThreshold)
        # 主攻武器量消耗到50%时重新部署
        self.doctrine.redeploy_on_attack_weapon(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_RedeployAttackDamageThreshold)
        # 主攻武器量消耗到75%时重新部署
        self.doctrine.redeploy_on_attack_weapon(4)
        self.env.step()
        self.assertEqual(4, self.doctrine.m_RedeployAttackDamageThreshold)

        # 忽略武器量不重新部署
        self.doctrine.redeploy_on_attack_weapon('Ignore')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RedeployAttackDamageThreshold)
        # 打光才重新部署
        self.doctrine.redeploy_on_attack_weapon('Exhausted')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_RedeployAttackDamageThreshold)
        # 主攻武器量消耗到25%时重新部署
        self.doctrine.redeploy_on_attack_weapon('Percent25')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_RedeployAttackDamageThreshold)
        # 主攻武器量消耗到50%时重新部署
        self.doctrine.redeploy_on_attack_weapon('Percent50')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_RedeployAttackDamageThreshold)
        # 主攻武器量消耗到75%时重新部署
        self.doctrine.redeploy_on_attack_weapon('Percent75')
        self.env.step()
        self.assertEqual(4, self.doctrine.m_RedeployAttackDamageThreshold)

    def test_redeploy_on_defence_weapon(self):
        """撤退与部署-设置导致重新部署的主防武器量"""
        # 忽略武器量不重新部署
        self.doctrine.redeploy_on_defence_weapon(0)
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RedeployDefenceDamageThreshold)
        # 打光才重新部署
        self.doctrine.redeploy_on_defence_weapon(1)
        self.env.step()
        self.assertEqual(1, self.doctrine.m_RedeployDefenceDamageThreshold)
        # 主防武器量消耗到25%时重新部署
        self.doctrine.redeploy_on_defence_weapon(2)
        self.env.step()
        self.assertEqual(2, self.doctrine.m_RedeployDefenceDamageThreshold)
        # 主防武器量消耗到50%时重新部署
        self.doctrine.redeploy_on_defence_weapon(3)
        self.env.step()
        self.assertEqual(3, self.doctrine.m_RedeployDefenceDamageThreshold)
        # 主防武器量消耗到75%时重新部署
        self.doctrine.redeploy_on_defence_weapon(4)
        self.env.step()
        self.assertEqual(4, self.doctrine.m_RedeployDefenceDamageThreshold)

        # 忽略武器量不重新部署
        self.doctrine.redeploy_on_defence_weapon('Ignore')
        self.env.step()
        self.assertEqual(0, self.doctrine.m_RedeployDefenceDamageThreshold)
        # 打光才重新部署
        self.doctrine.redeploy_on_defence_weapon('Exhausted')
        self.env.step()
        self.assertEqual(1, self.doctrine.m_RedeployDefenceDamageThreshold)
        # 主防武器量消耗到25%时重新部署
        self.doctrine.redeploy_on_defence_weapon('Percent25')
        self.env.step()
        self.assertEqual(2, self.doctrine.m_RedeployDefenceDamageThreshold)
        # 主防武器量消耗到50%时重新部署
        self.doctrine.redeploy_on_defence_weapon('Percent50')
        self.env.step()
        self.assertEqual(3, self.doctrine.m_RedeployDefenceDamageThreshold)
        # 主防武器量消耗到75%时重新部署
        self.doctrine.redeploy_on_defence_weapon('Percent75')
        self.env.step()
        self.assertEqual(4, self.doctrine.m_RedeployDefenceDamageThreshold)

    def test_reset(self):
        """重置作战条令"""

        if self.doctrine_owner != self.red_side:
            # 设置授权-使用核武器
            self.doctrine.use_nuclear_weapons('yes')
            self.env.step()
            self.assertEqual(1, self.doctrine.m_Nukes)
            # 重置本级条令（与上级保持一致）
            # 总体条令
            self.doctrine.reset(level='Left', aspect='Ensemble', escort_status='false')
            self.env.step()
            # 文档中没有-1相关的描述
            self.assertEqual(-1, self.doctrine.m_Nukes)

            # 雷达打开
            self.doctrine.set_em_control_status('Radar', 'Active')
            self.env.step()
            self.assertEqual(1, self.doctrine.m_EMCON_SettingsForRadar)
            # 电磁管控条令
            self.doctrine.reset(level='Left', aspect='EMCON', escort_status='false')
            self.env.step()
            self.assertEqual(0, self.doctrine.m_EMCON_SettingsForRadar)

            self.doctrine.set_weapon_release_authority(weapon_dbid='51', target_type='2001', quantity_salvo=1,
                                                       shooter_salvo=1, firing_range='max', self_defense='max',
                                                       escort='')
            self.env.step()
            # 武器使用规则
            self.doctrine.reset(level='Left', aspect='Weapon', escort_status='false')

        # 重置关联单元的作战条令（对单元不起作用）
        # 总体条令
        self.doctrine.reset(level='Middle', aspect='Ensemble', escort_status='false')
        # 电磁管控条令
        self.doctrine.reset(level='Middle', aspect='EMCON', escort_status='false')
        # 武器使用规则
        self.doctrine.reset(level='Middle', aspect='Weapon', escort_status='false')

        # 重置关联任务的作战条令（对单元不起作用）
        # 总体条令
        self.doctrine.reset(level='Right', aspect='Ensemble', escort_status='false')
        # 电磁管控条令
        self.doctrine.reset(level='Right', aspect='EMCON', escort_status='false')
        # 武器使用规则
        self.doctrine.reset(level='Right', aspect='Weapon', escort_status='false')

    def test_set_emcon_according_to_superiors(self):
        """设置单元电磁管控与上级一致"""
        # 本接口只适用于单元
        if self.doctrine_owner != self.aircraft:
            return

        # 设置单元电磁管控与上级一致
        self.doctrine.set_emcon_according_to_superiors('yes')
        self.env.step()
        self.assertEqual(True, self.doctrine.m_bEMCON_AccordingSuperior)

        # 设置单元电磁管控与上级不一致
        self.doctrine.set_emcon_according_to_superiors('no')
        self.env.step()
        self.assertEqual(False, self.doctrine.m_bEMCON_AccordingSuperior)

    def test_unit_obeys_emcon(self):
        """设置单元是否遵循电磁管控"""
        # 如果条令拥有者不是单元，结束
        if self.doctrine_owner != self.ship:
            return

        # 设置单元遵循电磁管控
        self.doctrine.unit_obeys_emcon('true')
        self.env.step()
        self.assertEqual(True, self.aircraft.bObeysEMCON)

        # 设置单元不遵循电磁管控
        self.doctrine.unit_obeys_emcon('false')
        self.env.step()
        self.assertEqual(False, self.aircraft.bObeysEMCON)
        self.env.step()

    # def test_param(self):
    #     d = self.doctrine
    #     dic = d.__dict__
    #     self.env.step()


if __name__ == '__main__':
    TestDoctrine.main()
