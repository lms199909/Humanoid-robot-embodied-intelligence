"""模型预测控制(Readme §6.1 规划层,100Hz)。

输入:Skill + RobotState
输出:Trajectory(horizon ~ 1s,dt 10ms)
"""
from __future__ import annotations
from common.types import Skill, RobotState, Trajectory


class MPCPlanner:
    """MPC 规划器抽象(具体 solver:casadi / acados / 自实现 QP)。"""

    def __init__(self, urdf_path: str = "", config: dict | None = None):
        self.urdf_path = urdf_path
        self.config = config or {}
        # TODO: 加载 Oli 动力学模型(SRB / 简化单刚体)+ 摆动腿动力学

    def plan(self, skill: Skill, state: RobotState, horizon_s: float = 1.0, dt_s: float = 0.01) -> Trajectory:
        """MPC 滚动规划。

        TODO:
          1. 把 skill 转成 cost / target(比如 SK_WALK → 跟踪目标速度,SK_CLIMB → 跟踪上楼梯轨迹)
          2. 求解 QP,得未来 N 步状态
          3. 包装成 Trajectory 返回
        """
        raise NotImplementedError

    def reset(self) -> None:
        # TODO: 切 skill 时清零 warm-start
        pass
