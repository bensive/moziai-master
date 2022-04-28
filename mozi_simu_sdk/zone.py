
# -*- coding: utf-8 -*-
#####################################
# File name " : zone.py
# Create date : 2020-4-26
# Modified date :
# Author : aie
# Describe : not set
# Email :


class CZone:
    """
    封锁区
    """
    def __init__(self, strGuid, mozi_server, situation):
        # guid
        self.strGuid = strGuid
        # 仿真服务类MoziServer实例
        self.mozi_server = mozi_server
        # 态势
        self.situation = situation
