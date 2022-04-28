# -*- coding:utf-8 -*-
##########################################################################################################
# File name :trigger.py
# Create date : 2020-4-11
# Modified date : 2020-4-11
# Author : aie
# Describe : triggers' father-class
# Unit : bjhs
##########################################################################################################


class CTrigger:
    """
    事件触发器
    """

    def __init__(self, strGuid, mozi_server, situation):
        # GUID
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 态势
        self.situation = situation