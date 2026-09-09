"""全身控制 WBC(Readme §6.1 控制层,1kHz)。

把 Trajectory + 当前 RobotState → JointCommand。
通常用任务空间控制(operational space) + 零空间优化。
"""
from __future__ import annotations
from common.types import Trajectory, RobotState, JointCommand


class WBCController:
    """WBC 抽象(具体:pinocchio + 二次规划 / 逆动力学)。"""

    def __init__(self, urdf_path: str = "", config: dict | None = None):
        self.urdf_path = urdf_path
        self.config = config or {}
        # TODO: 加载 URDF + 任务链定义

    def control(self, traj: Trajectory, state: RobotState) -> JointCommand:
        """1kHz 控制循环:计算每关节位置 + kp/kd。"""
        # TODO: 任务空间加速度 → 关节力矩(逆动力学)→ 阻抗控制输出
        raise NotImplementedError
