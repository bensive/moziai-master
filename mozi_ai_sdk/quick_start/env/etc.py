# 时间 : 2021/09/14 14:10
# 作者 : 张志高
# 文件 : etc
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

# 墨子服务端所在机器的IP, 默认127.0.0.1
SERVER_IP = "127.0.0.1"
# 墨子服务端与智能体客户端通信的端口，默认6060
SERVER_PORT = "6060"
# 平台:windows或linux
PLATFORM = 'windows'
# 想定名称
# windows环境使用.scen文件，使用文件全名带后缀，如：active_unit_test.scen
# linux环境使用.xml文件，使用文件名不带后缀，且文件名不能出现中文，如：active_unit_test
SCENARIO_NAME = "active_unit_test.scen"
SCENARIO_NAME_DEMO_01 = "demo01.scen"
SCENARIO_NAME_DEMO_02 = "demo02.scen"
SCENARIO_NAME_DEMO_03 = "demo03.scen"
SCENARIO_NAME_DEMO_04 = "demo04.scen"
SCENARIO_NAME_DEMO_05 = "demo05.scen"
SCENARIO_NAME_DEMO_06 = "demo06.scen"
SCENARIO_NAME_DEMO_07 = "demo07.scen"
# 推演档位
# 与推演控制中的推进速度对应
# 0-1倍速，1-2倍速，2-5倍速，3-15倍速，
# 4-30倍速，5-60倍速，6-300倍速，7-900倍速，8-1800倍速
SIMULATE_COMPRESSION = 3
# 决策步长，单位秒
# 环境类里有个step()方法，DURATION_INTERVAL是执行这个方法之后，向前推进的想定时间。
# 执行这个step()方法后，会有一个态势更新的动作，我们可以根据更新的态势做决策，所有叫决策步长。
# 设置的值应大于等于推演档位倍速的值，否则会影响推进速度
DURATION_INTERVAL = 10
# 推进模式: True为同步模式，False为异步模式
# 是否等待智能体客户端决策完成
# 同步模式：调用step方法后，推进暂停，直到智能体客户端调用下一个step才向下推进
# 异步模式：当前版本不支持
SYNCHRONOUS = True
# APP_MODE:
# 1 -- 本地windows模式
# 2 -- linux模式
# 3 -- 比赛模式
# 三种模式在创建env对象时有所区别
# app_mode=1或2
# env = Environment(etc.SERVER_IP, etc.SERVER_PORT, etc.PLATFORM, etc.SCENARIO_NAME_DEMO_01,
#                   etc.SIMULATE_COMPRESSION, etc.DURATION_INTERVAL, etc.SYNCHRONOUS, etc.APP_MODE)
# app_mode=3
# env = Environment(ip, port, duration_interval=etc.DURATION_INTERVAL, app_mode=3,
#                   agent_key_event_file=args.agent_key_event_file)
APP_MODE = 1
# Windows下墨子安装目录下bin目录
MOZI_PATH = 'D:/202102-mozi/Mozi/MoziServer/bin'


