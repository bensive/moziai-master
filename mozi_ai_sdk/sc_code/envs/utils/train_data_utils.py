# 时间 : 2021/6/28 14:51 
# 作者 : Dixit
# 文件 : train_data_utils.py 
# 说明 : 
# 项目 : ncc_code
# 版权 : 北京华戍防务技术有限公司

import logging
from typing import List, Dict

from ray.rllib.env.multi_agent_env import ENV_STATE
from ray.rllib.policy.sample_batch import SampleBatch
from ray.rllib.utils.framework import try_import_tf, try_import_torch
from ray.rllib.utils.typing import TensorType


_, tf, _ = try_import_tf()
torch, _ = try_import_torch()


logger = logging.getLogger(__name__)


class AgentCollector:

    def __init__(self):
        self.buffers: Dict[str, List] = {}
        self.count = 0

    def add_init_obs(self, state: TensorType, t: int, ret: bool, init_obs: TensorType) -> None:

        if SampleBatch.OBS not in self.buffers:
            self._build_buffers(
                single_row={
                    SampleBatch.OBS: init_obs,
                    ENV_STATE: state,
                    "t": t,
                    "ret": ret
                })
        self.buffers[SampleBatch.OBS].append(init_obs)
        self.buffers[ENV_STATE].append(state)
        self.buffers["t"].append(t)
        self.buffers["ret"].append(ret)

    def add_values(self, values: Dict[str, TensorType]) -> \
            None:

        for k, v in values.items():
            if k not in self.buffers:
                self._build_buffers(single_row=values)
            self.buffers[k].append(v)
        self.count += 1

    def _build_buffers(self, single_row: Dict[str, TensorType]) -> None:

        for col, data in single_row.items():
            if col in self.buffers:
                continue
            self.buffers[col] = []