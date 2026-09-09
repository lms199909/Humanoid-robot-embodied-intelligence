"""奖励函数(Oli 专属,按动力学重调)。"""
from __future__ import annotations
from common.types import RobotState, JointCommand


class StairClimbReward:
    """楼梯攀爬奖励 = 前进速度 + 高度增益 - 能耗 - 跌倒惩罚。"""

    def __init__(self, weights: dict | None = None):
        self.w = weights or {"forward": 1.0, "height": 2.0, "energy": -0.01, "fall": -10.0}

    def __call__(self, state: RobotState, prev_state: RobotState, action: JointCommand) -> float:
        # TODO: r = w.forward * d_forward + w.height * d_height + w.energy * |action|^2
        raise NotImplementedError


class GraspReward:
    """抓取奖励 = 抓取成功 +1,脱落 -1,精准度 bonus。"""

    def __call__(self, state: RobotState, grasp_force: float) -> float:
        raise NotImplementedError


class TrackingReward:
    """轨迹跟踪奖励(供 WBC 训练用)。"""

    def __call__(self, state: RobotState, target: RobotState) -> float:
        # TODO: -||state - target||^2
        raise NotImplementedError
