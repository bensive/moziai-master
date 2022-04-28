
# 时间 : 2021/09/29 11:52
# 作者 : 张志高
# 文件 : main_versus
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

from mozi_ai_sdk.feihai_red.env import etc
from mozi_ai_sdk.feihai_red.env.env import Environment
from mozi_ai_sdk.feihai_red.utils import actions
import argparse
import sys
import os
import traceback
import time

parser = argparse.ArgumentParser()
# parser.add_argument("--avail_ip_port", type=str, default='192.168.1.102:6060')
parser.add_argument("--avail_ip_port", type=str, default='127.0.0.1:6060')
# 比赛专用 Mozi Intelligent competition
parser.add_argument("--is_mic", type=bool, default=False)
parser.add_argument("--side_name", type=str, default='红方')
parser.add_argument("--agent_key_event_file", type=str, default=None)
parser.add_argument("--request_id", type=str, default='红方')


def main():

    args = parser.parse_args()
    if args.is_mic:     # 比赛专用 Mozi Intelligent competition
        print('专项赛模式')
        ip_port = args.avail_ip_port.split(":")
        ip = ip_port[0]
        port = ip_port[1]
        # 是否传入决策步长需讨论
        env = Environment(ip, port, duration_interval=etc.DURATION_INTERVAL, app_mode=3,
                          agent_key_event_file=args.agent_key_event_file, request_id=args.request_id)
    else:
        # 设置墨子安装目录下bin目录为MOZIPATH，程序会跟进路径自动启动墨子
        os.environ['MOZIPATH'] = etc.MOZI_PATH
        print('默认开发模式')
        env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME, etc.SIMULATE_COMPRESSION,
                          etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)

    # 启动墨子服务端
    # 通过gRPC连接墨子服务端，产生env.mozi_server对象
    # 设置推进模式 SYNCHRONOUS
    # 设置决策步长 DURATION_INTERVAL
    env.start()

    # 加载想定，产生env.scenario
    # 设置推进速度 SIMULATE_COMPRESSION
    # 初始化全局态势
    env.scenario = env.reset()

    side = env.scenario.get_side_by_name('红方')

    actions.set_side_doctrine(side)

    step_count = 0
    while not env.is_done():
        # 创建预警机支援任务
        actions.create_support_mission_1(side)
        actions.create_support_mission_2(side)
        # 创建空战飞机巡逻任务
        actions.create_patrol_mission(side)
        # 创建空战飞机打击任务
        actions.create_strike_mission(side)
        print(f"'推演步数：{step_count},本方得分：{side.iTotalScore}")
        step_count += 1
        print(time.time())
        env.step()


try:
    main()
except Exception as e:
    error_file = open(__file__.replace('main_versus.py', 'error.log'), 'w', encoding='utf-8')
    exc_type, exc_value, exc_obj = sys.exc_info()
    traceback.print_exc(file=error_file)
    sys.exit()
