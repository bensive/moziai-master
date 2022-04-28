#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : main_versus.py
# Create date : 2019-10-20 19:37
# Modified date : 2020-04-29 21:55
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

# 系统或第三方包
import os
import datetime
import numpy as np
import argparse

# 墨子Utils
from mozi_utils.pyfile import read_start_epoch
from mozi_utils.pyfile import read_start_step
from mozi_utils.pyfile import write_start_step_file
from mozi_utils.pyfile import write_start_epoch_file

# 墨子AI SDK
from mozi_ai_sdk.uav_anti_tank.env.env import EnvUavAntiTank as Environment
from mozi_ai_sdk.uav_anti_tank.env import etc
from mozi_ai_sdk.uav_anti_tank.utils.agent import AgentUavAntiTank

#  设置墨子安装目录下bin目录为MOZIPATH，程序会自动启动墨子
os.environ['MOZIPATH'] = 'D:\\202102-mozi\\Mozi\\MoziServer\\bin'
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
                          etc.SYNCHRONOUS, etc.SIMULATE_COMPRESSION, etc.SCENARIO_NAME,
                          platform_mode=args.platform_mode)
    env.start(env.server_ip, env.aiPort)
    # 开始的轮数
    epoch_file_path = "%s/epoch.txt" % etc.OUTPUT_PATH
    start_epoch = read_start_epoch(epoch_file_path)  # 目前已经训练的轮数
    # 开始步数
    step_file_path = "%s/step.txt" % etc.OUTPUT_PATH
    cur_step = read_start_step(step_file_path)
    print("start step: %s" % cur_step)
    # 创建智能体对象
    agent = AgentUavAntiTank(env, start_epoch)

    # 启动训练
    try:
        for _ep in range(start_epoch, etc.MAX_EPISODES):
            print(" ")
            print("%s：第%s轮训练开始======================================" % (datetime.datetime.now(), _ep))

            # 重置智能体、环境、训练器
            state_now, reward_now = env.reset()
            env.step_count = 0
            agent.reset()

            # 智能体作决策，产生动作，动作影响环境，智能体根据动作的效果进行训练优化
            for step in range(etc.MAX_STEPS):
                # 智能体根据当前的状态及回报值，进行决策，生成下一步的动作
                action_new = agent.make_decision(np.float32(state_now), reward_now)

                # 环境执行动作，生成下一步的状态及回报值
                state_new, reward_new = env.execute_action(action_new)

                # 根据推演结果，训练一次智能体
                agent.train(np.float32(state_now), action_new, reward_new, np.float32(state_new), cur_step)
                cur_step += 1
                write_start_step_file(step_file_path, str(cur_step))
                # 更新状态、回报值
                state_now = state_new
                reward_now = reward_new

                # 打印提示
                print("%s：轮数:%s 决策步数:%s  Reward:%.2f" % (datetime.datetime.now(), _ep, step, reward_now))

                # 检查是否结束本轮推演
                if env.check_done():
                    break
                # 如果显示此图，代码会卡住
                if cur_step % 100 == 0:
                    # show_pic()
                    pass
            write_start_epoch_file(epoch_file_path, str(_ep))

    except KeyboardInterrupt:
        pass


main()
