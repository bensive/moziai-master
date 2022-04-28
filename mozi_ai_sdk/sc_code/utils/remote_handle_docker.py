# 时间 : 2021/2/25 20:45 
# 作者 : Dixit
# 文件 : remote_handle_docker.py 
# 说明 : 
# 项目 : 墨子联合作战开发训练平台
# 版权 : 北京华戍防务技术有限公司


import docker
import socket
from contextlib import closing
import random
import sys
import time
from urllib.request import urlopen
import paramiko
from threading import Thread

# docker api
# https://zhuanlan.zhihu.com/p/66226815 通过Python连接Docker进行编程
MAX_DOCKER_RETRIES = 3


def remote_connect(hostname, password):
    client = paramiko.SSHClient()
    # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不在本地know_hosts文件中记录的主机将无法连接
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for i in range(MAX_DOCKER_RETRIES):
        try:
            client.connect(hostname=hostname, port=22, username='root', password=password)
            return client
        except Exception as e:
            i += 1
            print('paramiko第%s次连接，连接失败原因是%s' % (i, e))


def generate_remote_docker(hostname, docker_port, password, path):
    # 连接SSH服务端，以用户名和密码进行认证
    client = remote_connect(hostname, password)
    if not client:
        print('paramiko创建连接失败！！！')

    # 远程每次只创建一个墨子容器
    cmd = f'python {path}/remote_handle_docker.py --mode=\'create\' --sever_docker_ip={hostname}  --remote_docker_port={docker_port} --mono_num=1'
    for i in range(MAX_DOCKER_RETRIES):
        try:
            stdin, stdout, stderr = client.exec_command(cmd)
            stderr = stderr.read().decode('utf-8')
            stdout = stdout.read().decode('utf-8')
            if 'fail' in stdout:
                print('fail stdout: ', stdout)
                continue
            elif 'success' in stdout:
                print('success stdout: ', stdout)
                break
            else:
                raise NotImplementedError
            # stdout为正确输出，stderr为错误输出，同时是有1个变量有值

            # 打印执行结果
            if stderr:
                print("stderr: ", stderr)
        except Exception as e:
            print("exception: ", e)

    # 关闭SSHClient
    client.close()


def release_remote_docker(hostname, password, path, docker_ip_port):
    client = remote_connect(hostname, password)
    if not client:
        print('paramiko创建连接失败！！！')
    cmd = f'python {path}/remote_handle_docker.py --mode=\'release\' --sever_docker_ip_port={docker_ip_port} '
    for i in range(MAX_DOCKER_RETRIES):
        try:
            stdin, stdout, stderr = client.exec_command(cmd, timeout=60)
            stderr = stderr.read().decode('utf-8')
            stdout = stdout.read().decode('utf-8')
            if 'fail' in stdout:
                print('fail stdout: ', stdout)
                continue
            elif 'success' in stdout:
                print('success stdout: ', stdout)
                break
            else:
                raise NotImplementedError
            # stdout为正确输出，stderr为错误输出，同时是有1个变量有值

            # 打印执行结果
            if stderr:
                print("stderr: ", stderr)
        except Exception as e:
            print("exception: ", e)

    # 关闭SSHClient
    client.close()


def restart_remote_docker(hostname, password, path, docker_ip_port):
    client = remote_connect(hostname, password)
    if not client:
        print('paramiko创建连接失败！！！')
    # python remote_handle_docker.py --mode='restart' --sever_docker_ip_port='127.0.0.1:57463'
    cmd = f'python {path}/remote_handle_docker.py --mode=\'restart\' --sever_docker_ip_port={docker_ip_port} '
    for i in range(MAX_DOCKER_RETRIES):
        try:
            stdin, stdout, stderr = client.exec_command(cmd, timeout=60)
            stderr = stderr.read().decode('utf-8')
            stdout = stdout.read().decode('utf-8')
            if 'fail' in stdout:
                print('fail stdout: ', stdout)
                continue
            elif 'success' in stdout:
                print('success stdout: ', stdout)
                break
            else:
                raise NotImplementedError
            # stdout为正确输出，stderr为错误输出，同时是有1个变量有值

            # 打印执行结果
            if stderr:
                print("stderr: ", stderr)
        except Exception as e:
            print("exception: ", e)

    # 关闭SSHClient
    client.close()


def delete_remote_docker(hostname, path, password):
    client = remote_connect(hostname, password)
    if not client:
        print('paramiko创建连接失败！！！')
    # python remote_handle_docker.py --mode='delete' --sever_docker_ip='8.140.121.210'
    cmd = f'python {path}/remote_handle_docker.py --mode=\'delete\' --sever_docker_ip={hostname} '
    for i in range(MAX_DOCKER_RETRIES):
        try:
            stdin, stdout, stderr = client.exec_command(cmd, timeout=60)
            stderr = stderr.read().decode('utf-8')
            stdout = stdout.read().decode('utf-8')
            if 'fail' in stdout:
                print('fail stdout: ', stdout)
                continue
            elif 'success' in stdout:
                print('success stdout: ', stdout)
                break
            else:
                raise NotImplementedError
            # stdout为正确输出，stderr为错误输出，同时是有1个变量有值

            # 打印执行结果
            if stderr:
                print("stderr: ", stderr)
        except Exception as e:
            print("exception: ", e)

    # 关闭SSHClient
    client.close()


def generate_docker(sever_docker_dict, password=None, path=None, remote_docker_port=None):
    """

    Args:
        sever_docker_dict: {'8.140.121.210': 3, '123.57.137.210': 2}

    Returns:

    """
    sever_docker_info = []
    for ip, docker_num in sever_docker_dict.items():
        # client = docker.DockerClient(base_url=f'tcp://{ip}:2375')
        client = docker.from_env()
        if ip == '127.0.0.1' or ip == 'localhost' or ip == get_local_ip() or ip == get_public_ip():
            generate_local_docker(ip, client, docker_num, sever_docker_info, remote_docker_port)
        else:
            assert password is not None
            assert path is not None
            for _ in range(docker_num):
                docker_port = get_remote_free_port(ip)
                generate_remote_docker(ip, docker_port, password, path)
                docker_info = f'{ip}:{docker_port}'
                sever_docker_info.append(docker_info)

    return sever_docker_info


def generate_local_docker(ip, client, docker_num, sever_docker_info, remote_docker_port):
    for _ in range(docker_num):
        if remote_docker_port:
            assert docker_num == 1
            docker_port = remote_docker_port
        else:
            docker_port = get_local_free_port(ip)
        docker_info = _start_mozi_docker(ip, client, docker_port)

        sever_docker_info.append(docker_info)


def _start_mozi_docker(ip, client, docker_port):
    # noinspection PyBroadException
    try:
        for _ in range(MAX_DOCKER_RETRIES):
            for _ in range(MAX_DOCKER_RETRIES):
                container = client.containers.create('mozi_internet_v16',
                                                     command='/bin/bash',
                                                     name=f'mozi_{ip}_{docker_port}',
                                                     detach=True,
                                                     tty=True,
                                                     ports={'6060': docker_port},
                                                     user='root')
                container.start()
                out = container.exec_run(cmd='sh -c "service mysql start && echo success"',
                                         tty=True,
                                         user='root',
                                         detach=False)
                print(out.output)
                if 'started' in out.output.decode('utf-8'):
                    break
                print(f'mozi_{ip}_{docker_port} mysql fail to start!')
                container.stop()
                container.remove()
            print(f'mozi_{ip}_{docker_port} mysql was started success!')
            container.exec_run(cmd='sh -c "mono /home/LinuxServer/bin/LinuxServer.exe --AiPort 6060"',
                               tty=True,
                               user='root',
                               detach=True)
            out2 = container.exec_run(cmd='sh -c "pgrep mono"',
                                      tty=True,
                                      user='root',
                                      detach=False)
            if out2.output != b'':
                print(f'mozi_{ip}_{docker_port} mozi was started success!')
                break
            print(f'mozi_{ip}_{docker_port} mozi fail to start!')
            container.stop()
            container.remove()
        return f'{ip}:{docker_port}'
    except Exception:
        print('fail create mozi docker!')
        sys.exit(1)


def release_docker(docker_ip_port, password=None, path=None):
    docker_ip = docker_ip_port.split(":")[0]
    docker_port = docker_ip_port.split(":")[1]
    if docker_ip == '127.0.0.1' or docker_ip == 'localhost' or docker_ip == get_local_ip() or docker_ip == get_public_ip():
        # client = docker.DockerClient(base_url=f'tcp://{docker_ip}:2375')
        client = docker.from_env()
        # noinspection PyBroadException
        try:
            container = client.containers.get(f'mozi_{docker_ip}_{docker_port}')  #
            container.stop()
            container.remove()
            print(f'success release mozi_{docker_ip}_{docker_port}!')
        except Exception:
            print(f'fail get or stop or remove mozi_{docker_ip}_{docker_port} container!')
    else:
        assert password is not None
        assert path is not None
        release_remote_docker(docker_ip, password, path, docker_ip_port)


def restart_mozi_container(docker_ip_port, password=None, path=None):
    docker_ip = docker_ip_port.split(":")[0]
    if docker_ip == '127.0.0.1' or docker_ip == 'localhost' or docker_ip == get_local_ip() or docker_ip == get_public_ip():
        restart_local_docker(docker_ip_port)
    else:
        assert password is not None
        assert path is not None
        restart_remote_docker(docker_ip, password, path, docker_ip_port)


def restart_local_docker(docker_ip_port):
    docker_ip = docker_ip_port.split(":")[0]
    docker_port = docker_ip_port.split(":")[1]
    # client = docker.DockerClient(base_url=f'tcp://{docker_ip}:2375')
    client = docker.from_env()
    # noinspection PyBroadException
    try:
        container = client.containers.get(f'mozi_{docker_ip}_{docker_port}')
        container.stop()
        container.remove()
    except Exception:
        print(f'fail get or stop or remove mozi_{docker_ip}_{docker_port} container!')
        sys.exit(1)
    # noinspection PyBroadException
    try:
        for _ in range(MAX_DOCKER_RETRIES):
            for _ in range(MAX_DOCKER_RETRIES):
                container = client.containers.create('mozi_internet_v16',
                                                     command='/bin/bash',
                                                     name=f'mozi_{docker_ip}_{docker_port}',
                                                     detach=True,
                                                     tty=True,
                                                     ports={'6060': docker_port},
                                                     user='root')
                container.start()
                out = container.exec_run(cmd='sh -c "service mysql start && echo success"',
                                         tty=True,
                                         user='root',
                                         detach=False)
                print(out.output)
                if 'started' in out.output.decode('utf-8'):
                    break
                print(f'mozi_{docker_ip}_{docker_port} mysql fail to start!')
                container.stop()
                container.remove()
            print(f'mozi_{docker_ip}_{docker_port} mysql was started success!')
            container.exec_run(cmd='sh -c "mono /home/LinuxServer/bin/LinuxServer.exe --AiPort 6060"',
                               tty=True,
                               user='root',
                               detach=True)
            time.sleep(2)
            out2 = container.exec_run(cmd='sh -c "pgrep mono"',
                                      tty=True,
                                      user='root',
                                      detach=False)
            if out2.output != b'':
                print(f'mozi_{docker_ip}_{docker_port} mozi was started success!')
                break
            print(f'mozi_{docker_ip}_{docker_port} mozi fail to start!')
            container.stop()
            container.remove()
    except Exception:
        print('fail create mozi docker!')
        sys.exit(1)


def stop_docker(sever_docker_dict, password=None, path=None):
    '''

    Args:
        sever_docker_dict:
        key_word: 'mozi'

    Returns:

    '''
    ip_list = list(sever_docker_dict.keys())
    try:
        for ip in ip_list:
            if ip == '127.0.0.1' or ip == 'localhost' or ip == get_local_ip() or ip == get_public_ip():
                # client = docker.DockerClient(base_url=f'tcp://{ip}:2375')
                client = docker.from_env()
                container_list = client.containers.list(all=True)
                for doc in container_list:
                    if 'mozi' in doc.name:
                        container = client.containers.get(doc.name)
                        container.stop()
                        container.remove()
                        print('success remove container: ' + doc.name)
            else:
                assert password is not None
                assert path is not None
                delete_remote_docker(ip, path, password)
    except Exception as e:
        print('fail ', e)


def get_local_free_port(ip):
    """ Get free port"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def get_remote_free_port(remote_ip):
    ret = False
    while not ret:
        temp_port = random.randint(60000, 65535)
        ret = check_remote_port_is_free(remote_ip, temp_port)
    docker_port = temp_port
    return docker_port


def check_remote_port_is_free(remote_ip, port_=None):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.settimeout(1)
        # noinspection PyBroadException
        try:
            s.connect((remote_ip, port_))
            return False
        except Exception:
            return True


def get_public_ip():
    # noinspection PyBroadException
    try:
        public_ip = urlopen('http://ip.42.pl/raw').read()
        public_ip = public_ip.decode('ascii')
        return public_ip
    except Exception as e:
        print('获取本机IP失败！')


def get_local_ip():
    local_ip = socket.gethostbyname(socket.gethostname())
    return local_ip


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    # 'create': 创建docker；'delete'：删除某一服务器上所有docker；
    # 'restart': 重启docker；'release': 释放某一docker；
    parser.add_argument("--mode", type=str, default='delete')
    parser.add_argument("--sever_docker_ip", type=str, default='8.140.121.210')
    parser.add_argument("--remote_docker_port", type=str, default='')  # 代码自动检测
    parser.add_argument("--sever_docker_ip_port", type=str, default='8.140.121.210:12354')
    parser.add_argument("--mono_num", type=int, default=1)
    parser.add_argument("--path", type=str, default='/root')  # 后续统一放到RAY_HOME
    parser.add_argument("--password", type=str, default='123456')  # 后续换成密钥的方式

    # 本地创建容器 python remote_handle_docker.py --mode='create' --sever_docker_ip='127.0.0.1' --mono_num=1
    # 远程创建容器 python remote_handle_docker.py --mode='create' --sever_docker_ip='39.105.23.84' --mono_num=3 --path='/root' --password='123456'

    # 本地删除容器 python remote_handle_docker.py --mode='delete' --sever_docker_ip='127.0.0.1'
    # 远程删除容器 python remote_handle_docker.py --mode='delete' --sever_docker_ip='39.105.23.84'  --path='/root'  --password='123456'

    # 本地重启容器 python remote_handle_docker.py --mode='restart' --sever_docker_ip_port='127.0.0.1:12354'
    # 远程重启容器 python remote_handle_docker.py --mode='restart' --sever_docker_ip_port='39.105.23.84:64077' --path='/root'  --password='123456'

    # 本地释放容器 python remote_handle_docker.py --mode='release' --sever_docker_ip_port='127.0.0.1:12354'
    # 远程释放容器 python remote_handle_docker.py --mode='release' --sever_docker_ip_port='39.105.23.84:41314' --path='/root'  --password='123456'

    args = parser.parse_args()
    if args.mode == 'create':
        sever_docker_dict = {args.sever_docker_ip: args.mono_num, }  # {'8.140.121.210': 3, '123.57.137.210': 2}
        if args.remote_docker_port:
            sever_docker_info = generate_docker(sever_docker_dict, password=args.password, path=args.path,
                                                remote_docker_port=args.remote_docker_port)
        else:
            sever_docker_info = generate_docker(sever_docker_dict, password=args.password, path=args.path)
        print("sever_docker_info: ", sever_docker_info)
    elif args.mode == 'delete':
        sever_docker_dict = {args.sever_docker_ip: 0, }
        stop_docker(sever_docker_dict, password=args.password, path=args.path)
    elif args.mode == 'restart':
        restart_mozi_container(args.sever_docker_ip_port, password=args.password, path=args.path)
    elif args.mode == 'release':
        release_docker(args.sever_docker_ip_port, password=args.password, path=args.path)
    else:
        raise NotImplementedError
