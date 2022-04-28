# 时间 : 2021/09/15 17:27
# 作者 : 张志高
# 文件 : common
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司

import os
import psutil


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


def get_group(side, unit_name_list):
    """
    功能：根据单元名称返回单元所在编组的对象
    参数：side：推演方对象
        unit_name_list：str 单元名称列表
    返回：None或编组对象
    作者：张志高
    单位：北京华戍防务技术有限公司
    时间：2021-10-3
    """
    groups = side.get_groups()
    for k, v in groups.items():
        group_units = v.get_units()
        for item in unit_name_list:
            if get_obj_by_name(group_units, item):
                return v
    return None


def get_lead(side, group):
    """
    功能：获取编组的领队单元对象
    参数：side：推演方对象
        group：编组对象
    返回：None或编组的领队单元对象
    作者：张志高
    单位：北京华戍防务技术有限公司
    时间：2021-10-3
    """
    lead = side.get_unit_by_guid(group.m_GroupLead)
    return lead
