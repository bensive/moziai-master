
# 时间 : 2021/08/31 10:17
# 作者 : 张志高
# 文件 : base_env
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司
import threading

from mozi_simu_sdk.mozi_server import MoziServer
import time


class BaseEnvironment:
    """
    基础环境类
    """

    def __init__(self, ip, port, platform=None, scenario_name=None, simulate_compression=3, duration_interval=None,
                 synchronous=True, app_mode=None, agent_key_event_file=None, request_id=None):
        # 墨子服务端IP
        self.server_ip = ip
        # 墨子服务端端口
        self.aiPort = port
        # 平台： windows 或 linux
        self.platform = platform
        # 想定名称
        # windows上使用想定文件全称且带后缀，如 菲海战事-双方均无任务.scen
        # linux上使用使用想定文件名，不带后缀，且文件名要求不包含中文， 如 phisea-nomssn
        self.scenario_name = scenario_name
        # app_mode:
        # 1--local windows 本地windows模式
        # 2--linux mode    linux模式
        # 3--evaluate mode 比赛模式
        self.app_mode = app_mode
        # 推演档位 0-1倍速，1-2倍速，2-5倍速，3-15倍速，4-30倍速，5-60倍速，6-300倍速，7-900倍速，8-1800倍速
        self.simulate_compression = simulate_compression
        # 决策步长，单位秒
        self.duration_interval = duration_interval
        # 推进模式  True 同步 ,False 异步
        self.synchronous = synchronous

        # 用于比赛，智能体关键事件文件绝对路径，用于判定智能体是否正常运行
        self.agent_key_event_file = agent_key_event_file
        # 对战模式 versus: 比赛模式, development：开发模式, train：训练模式, eval：对战模式
        self.request_id = request_id
        # 决策
        self.step_count = 0
        self.mozi_server = None
        self.scenario = None
        self.situation = None

    def step(self):
        """
        步长
        主要用途：单步决策的方法,根据环境态势数据改变战场环境
        """
        if self.step_count == 0:
            self.mozi_server.run_simulate()
            # zjy
            if self.app_mode == 3:
                task = threading.Thread(target=self.mozi_server.stream_send_and_recv, args=())
                task.setDaemon(True)  # 必须在start之前设置
                task.start()
        else:
            # if self.app_mode != 3:
            self.mozi_server.run_grpc_simulate()

        self.step_count += 1
        self.situation = self.mozi_server.update_situation(self.scenario, self.app_mode)
        for k, side in self.scenario.get_sides().items():
            side.static_update()
        return self.scenario

    def reset(self):
        """
        重置函数
        主要用途：加载想定，
        """
        self.step_count = 0
        self.create_scenario()
        self.mozi_server.set_simulate_compression(self.simulate_compression)
        self.mozi_server.init_situation(self.scenario, self.app_mode)
        for k, side in self.scenario.get_sides().items():
            side.static_construct()
        return self.scenario

    def create_scenario(self):
        """
        建立一个想定对象
        """
        self.scenario = self.mozi_server.load_scenario()

    def connect_mozi_server(self, ip=None, port=None):
        """
        功能：连接墨子服务器
        参数：
        返回：
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/28/20
        """
        if ip is None and port is None:
            self.mozi_server = MoziServer(self.server_ip, self.aiPort, self.platform, self.scenario_name,
                                          self.simulate_compression, self.synchronous, self.request_id,
                                          self.agent_key_event_file)
        elif ip is not None and port is not None:
            self.mozi_server = MoziServer(ip, str(port), self.platform, self.scenario_name,
                                          self.simulate_compression, self.synchronous, self.request_id,
                                          self.agent_key_event_file)
        time.sleep(4.0)

    def start(self, ip=None, port=None):
        """
        开始函数
        主要用途：
            1.连接服务器端
            2.设置运行模式
            3.设置步长参数
        """
        if ip is None and port is None:
            self.connect_mozi_server()
        elif ip is not None and port is not None:
            self.connect_mozi_server(ip, port)
        else:
            raise ValueError('请正确配置墨子IP与端口！！！')

        self.mozi_server.set_run_mode(self.synchronous)
        self.mozi_server.set_decision_step_length(self.duration_interval)

    def is_done(self):
        """
        判定推演是否结束
        """
        response_dic = self.scenario.get_responses()
        for _, v in response_dic.items():
            if v.Type == 'EndOfDeduction':
                print('打印出标记：EndOfDeduction')
                if self.agent_key_event_file:
                    self.mozi_server.write_key_event_string_to_file('推演结束！')
                return True
        return False
