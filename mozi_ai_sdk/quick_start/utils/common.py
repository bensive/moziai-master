# 时间 : 2021/09/15 17:27
# 作者 : 张志高
# 文件 : common
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import os
import psutil


def kill_proc_by_name(name):
    """
    功能：Windows环境按名称杀死进程
    参数：name {str, 杀死进程名称}
    返回：None
    作者：张志高
    单位：北京华戍防务技术有限公司
    时间：2021-9-28
    """
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == name:
            cmd = 'taskkill /F /IM MoziServer.exe'
            os.system(cmd)


def get_obj_by_name(obj_dict, name):
    """
    功能：从对象字典中获取特定名称的对象
    参数：obj_dict：{dict: key为对象guid, value为对象}
        name {str: 对象名称}
    返回：obj_dict中的对象
    作者：张志高
    单位：北京华戍防务技术有限公司
    时间：2021-9-18
    """
    obj_list = [j for i, j in obj_dict.items() if name == j.strName]
    if obj_list:
        return obj_list[0]
    return None


def get_obj_by_description(obj_dict, name):
    """
    功能：从对象字典中获取特定名称的对象
    参数：obj_dict：{dict: key为对象guid, value为对象}
        name {str: 对象名称}
    返回：obj_dict中的对象
    作者：张志高
    单位：北京华戍防务技术有限公司
    时间：2021-9-18
    """
    obj_list = [j for i, j in obj_dict.items() if name == j.strDescription]
    if obj_list:
        return obj_list[0]
    return None


def get_obj_by_name_in(obj_dict, name):
    """
    功能：从对象字典中获取特定名称的对象
    参数：obj_dict：{dict: key为对象guid, value为对象}
        name {str: 对象名称}
    返回：obj_dict中的对象
    作者：张志高
    单位：北京华戍防务技术有限公司
    时间：2021-9-18
    """
    obj_list = [j for i, j in obj_dict.items() if name in j.strName]
    if obj_list:
        return obj_list[0]
    return None


def get_obj_list_by_name(obj_dict, name):
    """
    功能：从对象字典中获取特定名称的对象
    参数：obj_dict：{dict: key为对象guid, value为对象}
        name {str: 对象名称}
    返回：obj_dict中的对象
    作者：张志高
    单位：北京华戍防务技术有限公司
    时间：2021-9-18
    """
    obj_list = [j for i, j in obj_dict.items() if name in j.strName]
    if obj_list:
        return obj_list
    return None


def print_obj(obj):
    """
    功能：将对象的所有属性名称和值打印出来
    参数：obj：{对象}
    返回：无
    作者：张志高
    单位：北京华戍防务技术有限公司
    时间：2021-9-26
    """
    for k, v in obj.__dict__.items():
        print(f"{k}\t{v}")
