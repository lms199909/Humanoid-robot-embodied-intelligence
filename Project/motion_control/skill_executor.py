"""技能执行器:把 Skill 转成对 MPC 的连续调用 + 状态监测。"""
from __future__ import annotations
from common.types import Skill, RobotState, Trajectory
from .mpc import MPCPlanner


class SkillExecutor:
    """单 skill 的执行状态机:idle → running → success/failed。"""

    def __init__(self, mpc: MPCPlanner, config: dict | None = None):
        self.mpc = mpc
        self.config = config or {}
        self._state = "idle"
        self._current_skill: Skill | None = None

    def start(self, skill: Skill, state: RobotState) -> None:
        """启动一个 skill。"""
        # TODO: self._current_skill = skill
        # self.mpc.reset()
        # self._state = "running"
        pass

    def tick(self, state: RobotState) -> Trajectory:
        """单步:让 MPC 重新规划一次。"""
        # TODO: return self.mpc.plan(self._current_skill, state)
        raise NotImplementedError

    @property
    def is_running(self) -> bool:
        return self._state == "running"
