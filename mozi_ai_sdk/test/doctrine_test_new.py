
from mozi_ai_sdk.test.utils.test_framework import TestFramework


class TestDoctrine(TestFramework):
    """测试条令"""

    def test_doctrine(self):
        """
        条令快速测试
        :return:
        """
        """获取条令所有者"""
        a = self.doctrine.get_doctrine_owner()
        self.assertEqual(a, self.doctrine_owner)

        # 设置授权-使用核武器
        self.doctrine.use_nuclear_weapons('yes')

        # 设置对潜自由开火
        self.doctrine.set_weapon_control_status('weapon_control_status_subsurface', 0)
        # 设置对海自由开火
        self.doctrine.set_weapon_control_status('weapon_control_status_surface', 0)
        # 设置对地自由开火
        self.doctrine.set_weapon_control_status('weapon_control_status_land', 0)
        # 设置对空自由开火
        self.doctrine.set_weapon_control_status('weapon_control_status_air', 0)
        # 进攻时忽略计划航线-是
        self.doctrine.ignore_plotted_course('yes')
        # 接战模糊位置目标-忽略模糊性
        self.doctrine.set_ambiguous_targets_engaging_status(0)
        # 接战临机出现目标-可与任何目标交战
        self.doctrine.set_opportunity_targets_engaging_status('true')
        # 受到攻击时是否忽略电磁管控-不忽略
        self.doctrine.ignore_emcon_while_under_attack('false')
        # 使用鱼雷的动力航程 -仅手动开火下使用
        self.doctrine.use_kinematic_range_for_torpedoes(0)
        # 自动规避-否
        self.doctrine.evade_automatically('false')
        # 加油/补给-不允许
        self.doctrine.use_refuel_supply(1)
        # 设置加油补给的选择对象-优先选择敌我之间的加油机并禁止回飞
        self.doctrine.select_refuel_supply_object(2)
        # 设置是否给盟军单元加油补给-否
        self.doctrine.refuel_supply_allies(3)
        # 设置空战节奏-一般强度出动
        self.doctrine.set_air_operations_tempo(1)
        # 快速出动-否
        self.doctrine.quick_turnaround_for_aircraft(2)
        # 燃油预先规划-剩下1.25倍计划储备油量时即终止任务返航
        self.doctrine.set_fuel_state_for_aircraft('Joker25Percent')
        # 燃油状态-返航，离开编队返航
        self.doctrine.set_fuel_state_for_air_group('YesLeaveGroup')
        # 武器状态，预先规划-'2001' - 任务武器已耗光，立即脱离战斗,
        self.doctrine.set_weapon_state_for_aircraft(2001)
        # 武器状态-返航：编队中任意一架飞机达到单机武器状态要返航时，其可离队返航
        self.doctrine.set_weapon_state_for_air_group('YesLeaveGroup')
        # 设置是否用航炮扫射-是
        self.doctrine.gun_strafe_for_aircraft('Yes')
        # 抛弃弹药 - 是 （受到攻击时抛弃弹药）
        self.doctrine.jettison_ordnance_for_aircraft('Yes')
        # 反舰作战行动-设置是否以反舰模式使用舰空导弹-是
        self.doctrine.use_sams_to_anti_surface('true')
        # 设置是否与目标保持距离-否
        self.doctrine.maintain_standoff('false')
        # 规避搜索-总是
        self.doctrine.avoid_being_searched_for_submarine('Yes_Always')
        # 探测到威胁是否下潜-否
        self.doctrine.dive_on_threat('No')
        # 出航阵位充电电池剩余电量-电量剩下30%时再充
        self.doctrine.set_recharging_condition_on_patrol('Recharge_30_Percent')
        # 进攻防御充电电池剩余电量-电量剩下40%时再充
        self.doctrine.set_recharging_condition_on_attack('Recharge_40_Percent')
        # 使用AIP推进技术-否
        self.doctrine.use_aip('No')
        # 吊放声呐-只能人工使用或者分配到任务
        self.doctrine.use_dipping_sonar('ManualAndMissionOnly')

        # 雷达打开
        self.doctrine.set_em_control_status('Radar', 'Active')
        # 声呐打开
        self.doctrine.set_em_control_status('Sonar', 'Active')
        # 干扰机打开
        self.doctrine.set_em_control_status('OECM', 'Active')

        # 武器：RIM-162A 海麻雀舰空导弹
        # 目标类型号：五代机
        self.doctrine.set_weapon_release_authority(weapon_dbid='15', target_type='2001', quantity_salvo=1,
                                                   shooter_salvo=1, firing_range='max', self_defense='max',
                                                   escort='')

        # 撤退与部署-毁伤大于5%撤退
        self.doctrine.withdraw_on_damage('Percent5')
        # 燃油少于25%时撤退
        self.doctrine.withdraw_on_fuel('Percent25')
        # 主要攻击武器至少处于-打光才撤
        self.doctrine.withdraw_on_attack_weapon('Exhausted')
        # 主防武器量消耗到25%时撤退
        self.doctrine.withdraw_on_defence_weapon('Percent25')

        self.env.step()
        pass


if __name__ == '__main__':
    TestDoctrine.main()
