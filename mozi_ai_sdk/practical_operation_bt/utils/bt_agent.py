# 时间 : 2021/10/08 9:28
# 作者 : 张志高
# 文件 : bt_agent
# 项目 : 墨子联合作战智能体研发平台
# 版权 : 北京华戍防务技术有限公司


from mozi_ai_sdk.practical_operation_bt.utils.bt_leaf_node import *
from mozi_ai_sdk.btmodel.bt.bt_nodes import BT


class CAgent:
    def __init__(self):
        self.bt = None

    def init_bt(self, env, side_name, lenAI, options):
        side = env.scenario.get_side_by_name(side_name)
        sideGuid = side.strGuid
        shortSideKey = "a" + str(lenAI + 1)
        attributes = options

        # 行为树的节点
        root_sequence = BT()

        # 设置推演方条令节点
        leaf_set_side_doctrine = BT()

        control_mission_selector = BT()

        # 伴随干扰节点
        control_ecm_sequence = BT()
        leaf_create_support_mission = BT()
        leaf_create_patrol_mission = BT()
        leaf_ecm = BT()

        # 对海打击节点
        control_sea_strike_sequence = BT()
        leaf_update_support_mission = BT()
        leaf_create_strike_mission_1 = BT()
        leaf_create_strike_mission_2 = BT()

        # 连接节点形成树
        root_sequence.add_child(leaf_set_side_doctrine)
        root_sequence.add_child(control_mission_selector)

        control_mission_selector.add_child(control_ecm_sequence)
        control_mission_selector.add_child(control_sea_strike_sequence)

        control_ecm_sequence.add_child(leaf_create_support_mission)
        control_ecm_sequence.add_child(leaf_create_patrol_mission)
        control_ecm_sequence.add_child(leaf_ecm)

        control_sea_strike_sequence.add_child(leaf_update_support_mission)
        control_sea_strike_sequence.add_child(leaf_create_strike_mission_1)
        control_sea_strike_sequence.add_child(leaf_create_strike_mission_2)

        # 每个节点执行的动作
        # 根节点
        root_sequence.set_action(root_sequence.sequence, sideGuid, shortSideKey, attributes)

        # 二级节点
        leaf_set_side_doctrine.set_action(set_side_doctrine, sideGuid, shortSideKey, attributes)
        control_mission_selector.set_action(control_mission_selector.select, sideGuid, shortSideKey, attributes)

        # 三级节点
        control_ecm_sequence.set_action(control_ecm_sequence.sequence, sideGuid, shortSideKey, attributes)
        control_sea_strike_sequence.set_action(control_sea_strike_sequence.sequence, sideGuid, shortSideKey, attributes)

        # 四级节点
        leaf_create_support_mission.set_action(create_support_mission, sideGuid, shortSideKey, attributes)
        leaf_create_patrol_mission.set_action(create_patrol_mission, sideGuid, shortSideKey, attributes)
        leaf_ecm.set_action(ecm, sideGuid, shortSideKey, attributes)

        leaf_update_support_mission.set_action(update_support_mission, sideGuid, shortSideKey, attributes)
        leaf_create_strike_mission_1.set_action(create_strike_mission_1, sideGuid, shortSideKey, attributes)
        leaf_create_strike_mission_2.set_action(create_strike_mission_2, sideGuid, shortSideKey, attributes)

        # 定义根节点
        self.bt = root_sequence

    # 更新行为树
    def update_bt(self, side_name, scenario):
        return self.bt.run(side_name, scenario)
