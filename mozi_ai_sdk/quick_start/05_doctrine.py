# 时间 : 2021/09/26 16:41
# 作者 : 张志高
# 文件 : 06_doctrine
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment
from mozi_ai_sdk.quick_start.utils import common

"""
本案例目标：
1、掌握作战条令类的使用
2、不同维度设置条令：推演方条令、任务条令、编组条令、单元条令
3、掌握总体条令常用设置
4、掌握电磁管控设置
5、掌握武器使用规则设置
6、相应文件介绍
    doctrine.py CDoctrine
"""

os.environ['MOZIPATH'] = etc.MOZI_PATH
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME_DEMO_06,
                  etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)
env.start()
env.scenario = env.reset()

red_side = env.scenario.get_side_by_name('红方')

flag = False
while not env.is_done():
    if env.step_count == 0 and not flag:
        flag = True

        # 推演方条令
        side_doctrine = red_side.get_doctrine()

        # 任务条令
        mission = red_side.get_missions_by_name('巡逻任务')
        mission_doctrine = mission.get_doctrine()

        # 编组条令
        groups = red_side.get_groups()
        group = common.get_obj_by_name(groups, '飞行编队 4')
        group_doctrine = group.get_doctrine()

        # 单元条令
        aircrafts = red_side.get_aircrafts()
        aircraft = common.get_obj_by_name(aircrafts, '战斗机1')
        aircraft_doctrine = aircraft.get_doctrine()

        # 当前不支持航路点条令

        ####################################################################

        # 总体条令

        # 武器控制状态
        # 对海-自由开火
        side_doctrine.set_weapon_control_status_surface(0)
        # 对潜-谨慎开火
        side_doctrine.set_weapon_control_status_subsurface(1)
        # 对地-限制开火
        side_doctrine.set_weapon_control_status_land(2)
        # 对空-自由开火
        side_doctrine.set_weapon_control_status_air(0)

        # 进攻时忽略计划航线 - 对巡逻任务不起作用
        side_doctrine.ignore_plotted_course('yes')

        # 设置与模糊位置目标的交战状态 - 忽略模糊性
        side_doctrine.set_ambiguous_targets_engaging_status(0)

        # 决定与临机目标的交战状态 - 可与任何目标交战
        side_doctrine.set_opportunity_targets_engaging_status('true')

        # 设置受到攻击时是否忽略电磁管控 - 忽略
        side_doctrine.ignore_emcon_while_under_attack('true')

        # 决定是否自动规避 - 是
        side_doctrine.evade_automatically('true')

        # 是否运行加油补给
        side_doctrine.use_refuel_supply(2)
        # 设置加油补给的选择对象 - 选择最近的加油机
        side_doctrine.select_refuel_supply_object(0)
        # 设置是否给盟军单元加油补给 - 否
        side_doctrine.refuel_supply_allies(3)

        # 燃油状态-返航：编队中所有飞机均因达到单机油料状态要返航时，编队才返航
        side_doctrine.set_fuel_state_for_air_group('YesLastUnit')

        # 武器状态-返航：编队中所有飞机均因达到单机武器状态要返航时，编队才返航
        side_doctrine.set_weapon_state_for_air_group('YesLastUnit')

        # 反舰作战行动-设置是否与目标保持距离
        side_doctrine.maintain_standoff('true')

        ###########################################################

        # 电磁管控设置 - 设置电磁管控状态
        # 雷达打开
        side_doctrine.set_em_control_status('Radar', 'Active')
        # 声呐打开
        side_doctrine.set_em_control_status('Sonar', 'Active')
        # 干扰机打开
        side_doctrine.set_em_control_status('OECM', 'Active')

        ###########################################################

        # 武器：AIM-152B
        # 目标类型号：五代机
        # target_type：Lua使用手册，附录 WRA_WeaponTargetType
        # 齐射发射架数，设置为2时不起作用
        side_doctrine.set_weapon_release_authority(weapon_dbid='3152', target_type='2001', quantity_salvo=2,
                                                   shooter_salvo=4, firing_range=120, self_defense=11,
                                                   escort='')
        pass

    else:
        # 下一步，更新态势
        env.step()

