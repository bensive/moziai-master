##########################################################################################################
# File name : magazine.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:aie
##########################################################################################################


class CResponse:
    """
    响应类
    """
    def __init__(self, ID):
        # 编号
        self.ID = ID    # changed by aie
        # 响应内容
        self.Response = ''
        # 类型
        self.Type = ''
        # 类名
        self.ClassName = ''

