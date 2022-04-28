# 时间 : 2021/09/29 11:52
# 作者 : 张志高
# 文件 : main_versus
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import os
from mozi_ai_sdk.practical_operation_bt.env import etc
from mozi_ai_sdk.practical_operation_bt.env.env import Environment
from mozi_ai_sdk.practical_operation_bt.utils.bt_agent import CAgent

# 设置墨子安装目录下bin目录为MOZIPATH，程序会跟进路径自动启动墨子
os.environ['MOZIPATH'] = etc.MOZI_PATH

# 创建环境类对象
env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME,
                  etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)

# 启动墨子服务端
# 通过gRPC连接墨子服务端，产生env.mozi_server对象
# 设置推进模式 SYNCHRONOUS
# 设置决策步长 DURATION_INTERVAL
env.start()

for i in range(10):
    etc.flag_1 = False
    etc.flag_2 = False
    etc.flag_3 = False
    # 加载想定，产生env.scenario
    # 设置推进速度 SIMULATE_COMPRESSION
    # 初始化全局态势
    env.scenario = env.reset()

    side_name = '蓝方'
    side = env.scenario.get_side_by_name(side_name)

    # 实例化智能体
    agent = CAgent()
    # 初始化行为树
    agent.init_bt(env, side_name, 0, '')

    etc.SCENARIO_START_TIME = int(env.scenario.m_Time)

    step_count = 0
    while not env.is_done():

        # 更新动作
        agent.update_bt(side_name, env.scenario)
        step_count += 1
        env.step()
    print(f"第{i+1}局，推演步数：{step_count},本方得分：{side.iTotalScore}")
