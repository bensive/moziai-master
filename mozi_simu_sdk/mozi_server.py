# -*- coding:utf-8 -*-
# coding=utf-8
import time
import datetime
import grpc
import psutil
import os
from queue import Queue

from mozi_simu_sdk.scenario import CScenario
from mozi_simu_sdk.comm import GRPCServerBase_pb2
from mozi_simu_sdk.comm import GRPCServerBase_pb2_grpc

q = Queue()


class MoziServer:
    """
    仿真服务类，墨子仿真服务器类
    """

    def __init__(self, server_ip, server_port, platform=None, scenario_name=None, compression=None, synchronous=True,
                 request_id=None, agent_key_event_file=None):
        # 服务器IP
        self.server_ip = server_ip
        # 服务器端口
        self.server_port = server_port
        # 平台： windows 或 linux
        self.platform = platform
        # 想定名称
        # windows上使用想定文件全称且带后缀，如 菲海战事-双方均无任务.scen
        # linux上使用使用想定文件名，不带后缀，且文件名要求不包含中文， 如 phisea-nomssn
        self.scenario_name = scenario_name
        # 推演档位 0-1倍速，1-2倍速，2-5倍速，3-15倍速，4-30倍速，5-60倍速，6-300倍速，7-900倍速，8-1800倍速
        self.compression = compression
        # 推进模式  True 同步 ,False 异步
        self.synchronous = synchronous
        # 平台模式
        # versus 比赛模式：手工或第三方程序启动墨子并加载想定
        # development 开发模式：智能体启动墨子并加载想定
        # train  训练模式：手工或第三方程序启动墨子，智能体加载想定
        # eval   对战模式：手工或第三方程序启动墨子，智能体加载想定
        self.request_id = request_id

        # grpc客户端
        self.grpc_client = None
        self.is_connected = None  # = self.connect_grpc_server() # 这应该时初始化GRPC客户端

        # 命令池
        self.exect_flag = True
        self.command_pool = []
        self.command_num = 0

        # 用于比赛，智能体关键事件文件绝对路径，用于判定智能体是否正常运行
        self.agent_key_event_file = agent_key_event_file
        self.step_count = 0

        # 启动墨子仿真服务器
        self.start_mozi_server()

    def start_mozi_server(self):
        """
        功能：启动墨子仿真服务端
        参数：无
        返回：无
        作者：许怀阳
        单位：北京华戍防务技术有限公司
        时间：2020.05.04
        """
        if self.platform == 'windows':
            # 判断墨子是否已经启动
            is_mozi_server_started = False
            for i in psutil.process_iter():
                if i.name() == 'MoziServer.exe':
                    str_tmp = str(i.name()) + "-" + str(i.pid) + "-" + str(i.status())
                    print("墨子已启动")
                    is_mozi_server_started = True
                    break

            # 启动墨子
            if not is_mozi_server_started:
                mozi_path = os.environ['MOZIPATH']
                mozi_server_exe_file = mozi_path + '\\' + 'MoziServer.exe'
                os.popen(mozi_server_exe_file)
                print("%s：墨子推演方服务端已启动" % (datetime.datetime.now()))

            # 启动墨子后，稍微等一会，让它初始化一下
            time.sleep(10)
        else:
            pass

        # 初始化GRPC客户端??????
        self.connect_grpc_server()

        # 测试墨子服务端是否启动成功，如果没有启动成功，则等待
        is_connected = False
        connect_cout = 0  # 连接次数
        while not is_connected:
            is_connected = self.is_server_connected()
            self.is_connected = is_connected
            connect_cout = connect_cout + 1
            if connect_cout > 60:
                break
            print("%s：还没连接上墨子推演服务器,再等1秒" % (datetime.datetime.now()))
            time.sleep(1)

        if is_connected:
            if self.agent_key_event_file:
                self.write_key_event_string_to_file('成功连接墨子推演服务器！')
            print("%s：成功连接墨子推演服务器！" % (datetime.datetime.now()))
        else:
            print("%s：连接墨子推演服务器失败（60秒）！" % (datetime.datetime.now()))

    def is_server_connected(self):
        """
        功能：判断是否已经连接上墨子服务器。使用笨办法，如果发送数据时发生异常，则认为墨子服务器未启动。
        参数：无
        返回：True - 已连接， False - 未连接
        作者：许怀阳
        单位：北京华戍防务技术有限公司
        时间：2020.5.5 22：10
        """
        try:
            self.send_and_recv("test")
        except Exception:
            return False
        return True

    def connect_grpc_server(self):
        """
        功能：连接墨子服务器
        参数：无
        返回：True - 连接成功， False - 连接失败
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        conn = grpc.insecure_channel(self.server_ip + ':' + str(self.server_port))
        self.grpc_client = GRPCServerBase_pb2_grpc.gRPCStub(channel=conn)
        if 'gRPCStub object' in self.grpc_client.__str__():
            return True
        else:
            return False

    def load_scenario(self):
        """
        功能：加载想定
        限制：专项赛选手code不得直接调用
        参数：无
        返回：想定类对象 或 None
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        scenario_file = self.scenario_name
        ret = None
        if self.platform == "windows":
            ret = self.load_scenario_in_windows(scenario_file, "false")
        # else:
        #     ret = self.load_scenario_in_linux(scenario_file, "false")
        elif self.platform == "linux":
            ret = self.load_scenario_in_linux(scenario_file, "false")
        else:
            pass

        if ret == "数据错误":
            print("%s：发送想定加载LUA指令给服务器，服务器返回异常！" % (datetime.datetime.now()))

        load_success = False
        for i in range(60):
            value = self.is_scenario_loaded()
            if str(value) == "'Yes'":
                print("%s：想定加载成功！" % (datetime.datetime.now()))
                load_success = True
                break
            print("%s：想定还没有加载完毕，再等一秒！可能原因，1）时间太短；2）服务端没有想定%s！" % (datetime.datetime.now(), self.scenario_name))
            time.sleep(1)

        # 如果想定加载失败
        if not load_success:
            print("%s：超过50秒，想定没有加载成功。可能是服务端没有想定:%s！" % (datetime.datetime.now(), scenario_file))
            return None

        scenario = CScenario(self)
        return scenario

    def load_scenario_in_windows(self, scen_path, is_deduce):
        """
        功能：Windows上加载想定
        限制：专项赛禁用
        参数：scen_path {str: 想定文件的相对路径（仅支持.scen文件）}
            is_deduce 模式 {str: "false"想定编辑模式 "true"想定推演模式}
        返回：lua返回结果信息 或 数据错误
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        return self.send_and_recv("Hs_ScenEdit_LoadScenario('{}', {})".format(scen_path, is_deduce))

    def load_scenario_in_linux(self, path, model):
        """
        功能：linux上加载想定
        限制：专项赛禁用
        参数：path {str: 想定文件的相对路径（仅支持XML文件）}
            model 模式 {str:  "Edit"-想定编辑模式 "Play"-想定推演模式}
        返回：lua返回结果信息 或 数据错误
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        return self.send_and_recv("Hs_PythonLoadScenario('{}', '{}')".format(path, model))

    def send_and_recv(self, cmd):
        """
        功能：gRPC发送和接收服务端消息方法
        参数：cmd：{str，lua命令}
        返回：lua返回结果信息 或 数据错误
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        if self.exect_flag:
            # print(cmd)
            # by dixit: GRPC中加入timeout参数，设置30秒超时。
            if self.request_id:
                response = self.grpc_client.GrpcConnect(
                    GRPCServerBase_pb2.GrpcRequest(name=cmd, requestID=self.request_id), timeout=30)
            else:
                response = self.grpc_client.GrpcConnect(GRPCServerBase_pb2.GrpcRequest(name=cmd), timeout=30)
            length = response.length
            if len(response.message) == length:
                # print(response.message)
                return response.message
            else:
                return "数据错误"
        else:
            self.command_num += 1
            self.throw_into_pool(cmd)

    def stream_send_and_recv(self):
        """
        功能：流式gRPC发送和接收服务端初始态势和更新态势的方法
        param：cmd ？？？
        时间：2021-09-15
        姓名：赵俊义
        """
        global q
        if self.exect_flag:
            response = self.grpc_client.GrpcConnectStream(
                GRPCServerBase_pb2.GrpcRequest(name='', requestID=self.request_id))  # name='' 参数可以没有
            blank_info_count = 0
            for item in response:
                info = item.message
                # 返回的数据是'' 或者' ',不加入数据
                if len(info) > 1:
                    blank_info_count = 0
                    q.put(info)
                else:
                    blank_info_count += 1
                    print(f'接收到空的态势信息，连续累计接收空数据次数为{blank_info_count}')
                    q.put("Blank info from MZ")

    def throw_into_pool(self, cmd):
        """
        功能：将命令投入命令池。
        参数：cmd：{类型：str，内容：lua命令}
        返回：无
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        self.command_pool.append(cmd)

    def transmit_pool(self):
        """
        功能：将命令池倾泄到墨子服务端
        参数：无
        返回：'lua执行成功'或'脚本执行出错'
        作者：aie
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        joiner = '\r\n'
        cmds = joiner.join(self.command_pool)
        return self.send_and_recv(cmds)

    def is_scenario_loaded(self):
        """
        功能：获取想定是否加载
        参数：无
        返回："'Yes'" 或 "'No'"
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        return self.send_and_recv("print(Hs_GetScenarioIsLoad())")

    def creat_new_scenario(self):
        """
        功能：新建想定
        限制：专项赛禁用
        参数：无
        返回：lua执行成功/lua执行失败
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：4/2/20
        """
        return self.send_and_recv("Hs_ScenEdit_CreateNewScenario()")

    def set_simulate_compression(self, n_compression=4):
        """
        功能：设置想定推演倍速
        限制：专项赛禁用
        参数：n_compression 推演时间步长档位 {int: 0：1 秒，1：2 秒，2：5 秒，3：15 秒，4：30 秒，
                                5：1 分钟，6：5 分钟，7：15 分钟，8：30 分钟}
        返回：lua执行成功/lua执行失败
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/9/20
        """
        lua_str = "ReturnObj(Hs_SetSimCompression(%d))" % n_compression
        ret = self.send_and_recv(lua_str)
        return ret

    def increase_simulate_compression(self):
        """
        功能：推演时间步长提高 1 个档位
        限制：专项赛禁用
        参数：无
        返回：lua执行成功/lua执行失败
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-11
        """
        return self.send_and_recv("Hs_SimIncreaseCompression()")

    def decrease_simulate_compression(self):
        """
        功能：将推演时间步长降低 1 个档位
        限制：专项赛禁用
        参数：无
        返回：lua执行成功/lua执行失败
        作者：赵俊义
        单位：北京华戍防务技术有限公司
        时间：2020-3-11
        """
        return self.send_and_recv("Hs_SimDecreaseCompression()")

    def set_simulate_mode(self, b_mode):
        """
        功能：设置想定推演模式
        限制：专项赛禁用
        参数：b_mode {bool: True-非脉冲式推进（尽快），False-脉冲式推进（一般）}
        返回：lua执行成功/lua执行失败
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/9/20
        """
        lua_str = "Hs_SetSimMode(%s)" % str(b_mode).lower()
        return self.send_and_recv(lua_str)

    def set_run_mode(self, synchronous):
        """
        功能：设置python端与墨子服务端的交互模式，智能体决策想定是否暂停
        限制：专项赛禁用
        参数：synchronous 智能体决策想定是否暂停 {bool: True 同步模式-是, False 异步模式-否}
        返回：lua执行成功/lua执行失败
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/9/20
        """
        if synchronous:
            return self.send_and_recv("SETRUNMODE(FALSE)")
        else:
            return self.send_and_recv("SETRUNMODE(TRUE)")

    def set_decision_step_length(self, step_interval):
        """
        功能：设置决策间隔
        参数：step_interval {int: 决策间隔，单位秒}
        返回：lua执行成功/lua执行失败
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/9/20
        """
        self.send_and_recv("Hs_OneTimeStop('Stop', %d)" % step_interval)

    def suspend_simulate(self):
        """
        功能：设置环境暂停
        限制：专项赛禁用
        参数：无
        返回：lua执行成功/lua执行失败
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/9/20
        """
        lua_str = "Hs_SimStop()"
        self.send_and_recv(lua_str)

    def run_simulate(self):
        """
        功能：开始推演
        参数：无
        返回：lua执行成功/lua执行失败
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/9/20
        """
        lua_str = "ReturnObj(Hs_SimRun(true))"
        return self.send_and_recv(lua_str)

    def run_grpc_simulate(self):
        """
        功能：开始推演
        参数：无
        返回：lua执行成功/lua执行失败
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/9/20
        """
        if self.agent_key_event_file:
            self.step_count += 1
            if self.step_count % 2 == 0:
                self.write_key_event_string_to_file(f"当前是第{self.step_count}步")
        lua_str = "ReturnObj(Hs_GRPCSimRun())"
        return self.send_and_recv(lua_str)

    def init_situation(self, scenario, app_mode):
        """
        功能：初始化态势
        参数：scenario {想定类对象}
            app_mode {int: 1--local windows 本地windows模式
                            2--linux mode    linux模式
                            3--evaluate mode 比赛模式}
        返回：lua执行成功/lua执行失败
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/9/20
        """
        b_init_success = scenario.situation.init_situation(self, scenario, app_mode)
        return b_init_success

    def update_situation(self, scenario, app_mode):
        """
        功能：更新态势
        参数：scenario {想定类对象}
        返回：lua执行成功/lua执行失败
        作者：-
        单位：北京华戍防务技术有限公司
        时间：4/9/20
        """
        return scenario.situation.update_situation(self, scenario, app_mode)

    def emulate_no_console(self):
        """
        作者：解洋
        日期：2020-3-12
        函数功能：模拟无平台推演
        函数类型：编辑函数
        :return:
        """
        return self.send_and_recv("Tool_EmulateNoConsole()")

    def run_script(self, script):
        """
        作者：解洋
        限制：专项赛禁用
        日期：2020-3-11
        函数功能：运行服务端 Lua 文件夹下的 Lua 文件（*.lua）。
        函数类型：推演函数
        :param script:字符串。服务端 Lua 文件夹下包括 Lua 文件名在内的相对路径
        :return:
        """
        return self.send_and_recv("ScenEdit_RunScript('{}')".format(script))

    def set_key_value(self, key, value):
        """
        功能：在系统中有一预设的“键-值”表，本函数向“键-值”表添加一条记录。
        参数：key {str: 键的内容}
            value {str: 值的内容}
        返回：lua执行成功/lua执行失败
        作者：解洋
        单位：北京华戍防务技术有限公司
        时间：2020-3-11
        """
        return self.send_and_recv("ScenEdit_SetKeyValue('{}','{}')".format(key, value))

    def get_value_by_key(self, key):
        """
        功能：在系统中有一预设的“键-值”表，本函数根据“键”的内容从“键-值”表中获取对应的“值”
        参数：key {str: 键的内容}
        返回：“值”的内容
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-8-26
        """
        return self.send_and_recv("ReturnObj(ScenEdit_GetKeyValue('{}'))".format(key))

    def write_key_event_string_to_file(self, key_event_str):
        """
        功能：将字符串写入文件，用于比赛智能体测试，用于检测智能体状态
        参数：key_event_str {str: 智能体关键事件内容}
        返回：无
        作者：张志高
        单位：北京华戍防务技术有限公司
        时间：2021-9-3
        """
        if not self.agent_key_event_file:
            return
        if key_event_str == '成功连接墨子推演服务器！':
            # 将原有文本删除，重新写入
            fh = open(self.agent_key_event_file, 'w', encoding='utf-8')
        else:
            # 原文基础上继续写入
            fh = open(self.agent_key_event_file, 'a', encoding='utf-8')
        fh.write(key_event_str + '\n')
        fh.close()
