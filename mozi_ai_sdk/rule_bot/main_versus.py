import os
import sys
import argparse
from mozi_ai_sdk.rule_bot.env.env import Environment
from mozi_ai_sdk.rule_bot.utils import agent
from mozi_simu_sdk.mssnpatrol import CPatrolMission
from mozi_ai_sdk.rule_bot.env import etc
from mozi_simu_sdk.mssnstrike import CStrikeMission


parser = argparse.ArgumentParser()
parser.add_argument("--avail_ip_port", type=str, default='127.0.0.1:6060')
parser.add_argument("--platform_mode", type=str, default='eval')
parser.add_argument("--side_name", type=str, default='红方')
parser.add_argument("--agent_key_event_file", type=str, default=None)

#  设置墨子安装目录下bin目录为MOZIPATH，程序会自动启动墨子
os.environ['MOZIPATH'] = 'D:\\mozi_server_个人版\\Mozi\\MoziServer\\bin'
print(os.environ['MOZIPATH'])
air_name = '歼-16 #1'


# run函数
def run(env, side_name=None):
    if not side_name:
        side_name = '红方'
    # 启动墨子服务器，连接墨子服务器，获取初始态势数据
    env.start()
    # 加载想定，初始化推演方
    env.reset()
    # 获取更新态势
    scenario = env.step()

    # 获取推演方，获取本方的所有数据
    red_side = scenario.get_side_by_name(side_name)
    print('进入推演方%s' % side_name)
    # 获得敌方的所有数据
    contacts_dic = red_side.contacts

    """
    推演方条令/任务条令/单元条令
    """
    # 推演方条令
    doctrine1 = red_side.get_doctrine()
    agent.edit_side_doctrine(doctrine1)

    # 任务条令
    patrol_mission = red_side.get_missions_by_name('歼-16单机')
    doctrine2 = patrol_mission.get_doctrine()
    agent.edit_mission_doctrine(doctrine2)

    # 单元条令，先获取飞机
    airs = red_side.aircrafts
    air1 = [air for air in airs.values() if air.strName == '歼-16 #1'][0]
    # 单机出动
    air1.ops_single_out()
    air1.abort_launch()
    air1.set_loadout(2995, 2, 'true', 'false')
    # 雷达开关机
    air2 = [air for air in airs.values() if air.strName == 'tt'][0]
    doctrine2 = air2.get_doctrine()
    doctrine2.set_emcon_according_to_superiors('no')
    air2.set_radar_shutdown('false')
    air2.set_radar_shutdown('true')
    air2.set_oecm_shutdown('false')
    air2.set_oecm_shutdown('true')
    air2.set_sonar_shutdown('false')
    air2.set_sonar_shutdown('true')
    env.step()

    air2.set_desired_speed(555.6)
    air2.set_desired_height(5000, 'true')
    course_list = ([20.8257931015082, 111.386009080737], [20.7724645817724, 113.276545596993])
    air2.plot_course(course_list)
    env.step()
    air2.return_to_base()
    air3 = [air for air in airs.values() if air.strName == 'ss'][0]
    doctrine3 = air2.get_doctrine()
    # doctrine3.set_emcon_according_to_superiors('no')
    air3.set_sonar_shutdown('false')
    air3.set_sonar_shutdown('true')
    doctrine3.set_emcon_according_to_superiors('no')
    air3.set_sonar_shutdown('false')
    air3.set_sonar_shutdown('true')

    air3.drop_active_sonobuoy('deep')
    air3.drop_passive_sonobuoy('deep')
    env.step()

    air2.set_throttle(3)
    agent.edit_side_doctrine(doctrine2)

    airs_air = [j for i, j in airs.items() if j.strName == 'tt']
    air = airs_air[0]
    doctrine_air = air.get_doctrine()
    doctrine_air.unit_obeys_emcon('false')
    # air.set_radar_shutdown('true')
    doctrine_air.set_em_control_status('Radar','Passive')
    doctrine_air.set_em_control_status('Sonar','Active')
    doctrine_air.set_em_control_status('OECM','Active')

    air.plot_course([(20, 110.3), (25.1, 139.0)])
    air.set_throttle('4')
    air.set_throttle(3)
    air.set_desired_speed(1200)
    air.set_desired_height(5000, 'True')
    air.delete_coursed_point(0)
    air.unit_obeys_emcon('true')
    air.set_radar_shutdown('false')
    air.set_throttle('4')


    """
    创建任务：巡逻任务，打击任务，并对任务进行设置
    """
    # 巡逻任务添加参考点 
    patrol_area, cordon_area = agent.add_rp(red_side)
    # 创建巡逻任务
    red_side.add_mission_patrol('巡逻任务', 0, patrol_area)  # args:patrol_type
    patrol_mission = CPatrolMission('巡逻任务', scenario.mozi_server, scenario.situation)
    patrol_mission.strName = '巡逻任务'
    # 对创建的任务进行设置
    agent.edit_mission(patrol_mission, cordon_area)

    # 创建打击任务
    red_side.add_mission_strike('strike1', 2)  # args: strike_type
    strkmssn_1 = CStrikeMission('T+1_mode', scenario.mozi_server, scenario.situation)
    strkmssn_1.strName = 'strike1'

    targets = [item for item in contacts_dic.values() if 'CVN' in item.strName]
    if targets:
        target = targets[0]
        strkmssn_1.assign_unit_as_target(target)
    strkmssn_1.assign_units({air.strGuid: air})
    strkmssn_1.add_plan_way_to_mission(0, '预设航线1')

    while True:
        scenario.mozi_server.run_grpc_simulate()
        scenario = env.step()
        agent.update(scenario)
        time = scenario.m_Duration.split('@')
        duration = int(time[0]) * 86400 + int(time[1]) * 3600 + int(time[2]) * 60
        if scenario.m_StartTime + duration <= scenario.m_Time:
            print('推演已结束！')
            sys.exit(0)
        else:
            pass


def main():

    args = parser.parse_args()
    if args.platform_mode == 'versus':
        print('比赛模式')
        ip_port = args.avail_ip_port.split(":")
        ip = ip_port[0]
        port = ip_port[1]
        # 决策步长需讨论
        env = Environment(ip, port, duration_interval=etc.DURATION_INTERVAL, app_mode=2,
                          agent_key_event_file=args.agent_key_event_file, platform_mode=args.platform_mode)
        run(env, args.side_name)
    else:
        print('开发模式')
        env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME, etc.SIMULATE_COMPRESSION,
                          etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.app_mode)

        run(env)


main()

if __name__ == '__main__':
    main()
