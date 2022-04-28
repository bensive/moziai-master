#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : main_uav_anti_tank.py
# Create date : 2019-10-20 19:37
# Modified date : 2020-04-29 21:53
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################
import os
import argparse
from mozi_ai_sdk.heli_anti_sub.env.env import Env as Environment
from mozi_ai_sdk.heli_anti_sub.env import etc
from mozi_ai_sdk.heli_anti_sub.utils.agent import Agent
from mozi_utils.pyfile import read_start_epoch
from mozi_utils.pyfile import write_start_epoch_file

#  设置墨子安装目录下bin目录为MOZIPATH，程序会自动启动墨子
os.environ['MOZIPATH'] = 'D:\\mozi_server_个人版\\Mozi\\MoziServer\\bin'
parser = argparse.ArgumentParser()
parser.add_argument('--avail_ip_port', type=str, default='127.0.0.1:6060')
parser.add_argument('--platform_mode', type=str, default='development')
parser.add_argument('--side_name', type=str, default='红方')
parser.add_argument('--agent_key_event_file', type=str, default=None)


def main():
    """主函数，用于构建训练环境及智能体，并进行训练"""
    args = parser.parse_args()
    if args.platform_mode == 'versus':
        print('比赛模式')
        ip_port = args.avail_ip_port.split(':')
        ip = ip_port[0]
        port = ip_port[1]
        env = Environment(ip, port, duration_interval=etc.DURATION_INTERVAL, app_mode=2,
                          agent_key_event_file=args.agent_key_event_file, platform_mode=args.platform_mode)

    else:
        print('开发模式')
        env = Environment(etc.SERVER_IP, etc.SERVER_PORT, None, etc.DURATION_INTERVAL, etc.app_mode,
                          etc.SYNCHRONOUS, etc.SIMULATE_COMPRESSION, etc.SCENARIO_NAME, platform_mode=args.platform_mode)
    env.start(env.server_ip, env.aiPort)
    env.step_count = 0
    epoch_file_path = "%s/epoch.txt" % etc.OUTPUT_PATH
    start_epoch = read_start_epoch(epoch_file_path)
    # 创建智能体对象
    agent = Agent(env)

    try:
        for _ep in range(start_epoch, etc.MAX_EPISODES):
            # 设置智能体
            agent.setup(env.state_space, env.action_space)
            # 重置环境，初始化态势， 获取单步数据
            timesteps = env.reset()
            env.step_count = 0
            # 重置智能体
            agent.reset()
            for step in range(etc.MAX_STEPS):
                # 运行一步
                timesteps = agent.step(timesteps[0])  # env.step()
                print(" ")
                print("轮数:%s 决策步数:%s" % (_ep, step))
                print("reward:%.2f" % (timesteps[1]))
                if timesteps[2]:
                    break
            write_start_epoch_file(epoch_file_path, str(_ep))

    except KeyboardInterrupt:
        pass


main()
