
# 时间 : 2021/09/24 11:17
# 作者 : 张志高
# 文件 : demo01_situation
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

"""
本案例目标：
1、了解态势类 situation.py CSituation
    获取全局态势 env.reset
    获取更新态势 env.step
    存储态势信息：env.scenario
2、掌握态势的层级结构
3、掌握态势对象的获取及使用方法（属性及方法）
4、了解对象属性枚举值的查询方法
    1）situ_interpret.py - CDoctrineDict
    2）接口文档
"""

import os
from mozi_ai_sdk.quick_start.env import etc
from mozi_ai_sdk.quick_start.env.env import Environment
from mozi_ai_sdk.quick_start.utils import common

os.environ['MOZIPATH'] = etc.MOZI_PATH
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME,
                  etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)
env.start()
# 获取全局态势
env.scenario = env.reset()
red_side = env.scenario.get_side_by_name('红方')
blue_side = env.scenario.get_side_by_name('蓝方')

flag = False
while not env.is_done():
    if env.step_count == 0 and not flag:
        flag = True

        # 想定对象属性
        # debug模式查看
        # 对枚举类型的属性，不同值得含义可在situ_interpret.py中或接口文档查看
        # 想定对象方法
        # 想定对象方法可在scenario.py中或接口文档查看

        # 天气对象
        # 对应想定编辑-气象环境部分
        # 通过获取的对象可以查看当前想定设置的平均气温、降水量、天空云量、风力/海况
        # 也可以通过想定类中的set_weather方法设置气象环境
        weather = env.scenario.get_weather()
        common.print_obj(weather)

        # 响应类对象字典
        # 墨子启动时的响应信息
        # 通过遍历所有响应对象，可以判断推演是否结束（env.is_done方法）
        responses = env.scenario.get_responses()

        # 事件类对象字典
        # 仅提供属性和少量方法（获取本事件的触发器、条件、动作）
        # 事件编辑的相关操作都在env.scenario中
        events = env.scenario.get_events()

        # 武器冲击类对象 暂不可用
        weapon_impacts = env.scenario.get_weapon_impacts()

        # 推演方类对象字典
        sides = env.scenario.get_sides()

        # 一般获取方式如下
        # 通常智能体客户端仅扮演一方，只允许获取和操作其中一个推演方对象
        red_side = env.scenario.get_side_by_name('红方')
        print('#########################################')
        common.print_obj(red_side)

        ##########################################################
        # 推演方

        # 推演方条令对象
        # 对应条令规划-推演方条令
        # 通过该对象可以获取对应的推演方条令的设置（对象属性）
        # 通过该对象可以设置对应的推演方条令（对象方法）
        side_doctrine = red_side.get_doctrine()
        print('#########################################')
        common.print_obj(side_doctrine)

        # 活动单元对象字典-获取单元对象后，可以通过该对象操控对应的单元
        # 所有单元对象继承CActiveUnit类，CActiveUnit类中有较为通用的对象属性和方法
        # 区别于其他子类的方法和属性，在各个子类中
        # 添加单元操作，在推演方对象中（比赛禁用）
        # 详细的内容04_active_unit中介绍
        groups = red_side.get_groups()          # 编组
        print('#########################################')
        group = common.get_obj_by_name(groups, '飞行编队 37')
        common.print_obj(group)

        ships = red_side.get_ships()            # 水面舰艇
        print('#########################################')
        unit = common.get_obj_by_name(ships, '舰船-纯方位发射')
        common.print_obj(unit)

        facilities = red_side.get_facilities()  # 地面兵力设施
        print('#########################################')
        unit = common.get_obj_by_name(facilities, '机场1')
        common.print_obj(unit)

        submarines = red_side.get_submarines()  # 潜艇
        print('#########################################')
        unit = common.get_obj_by_name(submarines, '潜艇1')
        common.print_obj(unit)

        aircrafts = red_side.get_aircrafts()    # 飞机
        print('#########################################')
        unit = common.get_obj_by_name(aircrafts, '反潜机1')
        common.print_obj(unit)

        weapons = red_side.get_weapons()        # 武器
        print('#########################################')
        unit = common.get_obj_by_name_in(weapons, '轻型鱼雷')
        common.print_obj(unit)

        unguided_weapons = red_side.get_unguided_weapons()  # 非制导武器，暂不可用
        # 也可以直接通过guid直接获取单元对象
        # guid可在服务端获取：选中单元-右键-想定编辑-拷贝单元ID到剪切板
        aircraft_1 = red_side.get_unit_by_guid('e85dc457-c49f-4ccd-84ee-36ec967fb0d4')

        # 探测目标对象字典-本方获取到的其他方单元信息
        # 对象方法可以在contact.py中查看
        contacts = red_side.get_contacts()
        # guid可在服务端获取：选中单元-右键-拷贝单元ID到剪切板
        contact = red_side.get_contact_by_guid('801ea534-a57c-4d3b-ba5d-0f77e909506c')
        # 从推演方用名称确认目标
        identified_targets_by_name = red_side.get_identified_targets_by_name('苏-34 型“鸭嘴兽”攻击机')

        print('#########################################')
        common.print_obj(contact)

        # 航线对象字典
        # 对应的文件和类：sideway.py CSideWay 只有属性
        # 创建和设置航线的方法均在推演方对象中
        side_ways = red_side.get_sideways()
        print('#########################################')
        unit = common.get_obj_by_name_in(side_ways, '航线1')
        common.print_obj(unit)

        # 任务对象字典
        # 获取任务后，可以获取任务属性或对任务进行设置
        # 创建任务的方法在推演方对象中
        # 任务相关的操作会在另一个案例中介绍
        patrol_missions = red_side.get_patrol_missions()    # 巡逻任务
        print('#########################################')
        unit = common.get_obj_by_name_in(patrol_missions, '空中巡逻')
        common.print_obj(unit)

        strike_missions = red_side.get_strike_missions()    # 打击任务
        print('#########################################')
        unit = common.get_obj_by_name_in(strike_missions, '空中打击')
        common.print_obj(unit)

        support_missions = red_side.get_support_missions()  # 支援任务
        print('#########################################')
        unit = common.get_obj_by_name_in(support_missions, '加油任务')
        common.print_obj(unit)

        cargo_missions = red_side.get_cargo_missions()      # 投送任务
        print('#########################################')
        unit = common.get_obj_by_name_in(cargo_missions, '投送')
        common.print_obj(unit)

        ferry_missions = red_side.get_ferry_missions()      # 转场任务
        print('#########################################')
        unit = common.get_obj_by_name_in(ferry_missions, '转场')
        common.print_obj(unit)

        mining_missions = red_side.get_mining_missions()                # 布雷任务 暂不可用
        mine_clearing_missions = red_side.get_mine_clearing_missions()  # 扫雷任务 暂不可用
        mission_1 = red_side.get_missions_by_name('空中打击')

        # 参考点
        # 添加和设置参考点的方法在推演方对象中
        reference_points = red_side.get_reference_points()
        rp_16 = red_side.get_reference_point_by_name('RP-16')
        print('#########################################')
        unit = common.get_obj_by_name_in(reference_points, 'RP-16')
        common.print_obj(unit)

        # 对象只有属性，添加和设置区域的方法在推演方类中
        # 禁航区
        no_nav_zones = red_side.get_no_nav_zones()
        print('#########################################')
        unit = common.get_obj_by_description(no_nav_zones, '禁航区1')
        common.print_obj(unit)

        # 封锁区
        exclusion_zones = red_side.get_exclusion_zones()
        print('#########################################')
        unit = common.get_obj_by_description(exclusion_zones, '封锁区')
        common.print_obj(unit)

        ##########################################################

        # 活动单元

        # 获取本方地空导弹中队对象
        facilities = red_side.get_facilities()
        ground_to_air_missile_squadron = common.get_obj_by_name(facilities, '地空导弹中队')

        # 单元条令对象
        unit_doctrine = ground_to_air_missile_squadron.get_doctrine()
        # 单元挂架对象字典 mount.py
        mounts = ground_to_air_missile_squadron.get_mounts()
        print('#########################################')
        unit = common.get_obj_by_name_in(mounts, 'M901式爱国者导弹')
        common.print_obj(unit)

        # 单元武器库对象字典 magazine.py
        magazines = ground_to_air_missile_squadron.get_magazines()
        print('#########################################')
        unit = common.get_obj_by_name_in(magazines, '“毒刺”肩射地空导弹')
        common.print_obj(unit)
        # 单元传感器对象字典 sensor.py
        sensors = ground_to_air_missile_squadron.get_sensor()
        print('#########################################')
        unit = common.get_obj_by_name_in(sensors, 'AN/MPQ-53型相控阵雷达')
        common.print_obj(unit)

        blue_aircrafts = blue_side.get_aircrafts()
        blue_aircraft = common.get_obj_by_name(blue_aircrafts, '敌机1')
        # 单元挂载方案对象 loadout.py
        loadout = blue_aircraft.get_loadout()
        print('#########################################')
        common.print_obj(loadout)
    else:
        # 下一步，更新态势
        env.step()
