"""终止条件。"""
from __future__ import annotations
from common.types import RobotState


class FallTermination:
    """摔倒 = base 高度 < 阈值 或 倾角 > 60°。"""

    def __init__(self, min_height: float = 0.3, max_tilt_deg: float = 60.0):
        self.min_height = min_height
        self.max_tilt_deg = max_tilt_deg

    def __call__(self, state: RobotState) -> bool:
        # TODO
        return False


class CollisionTermination:
    """碰撞 = 力矩突变 + 外部接触力超阈值。"""

    def __call__(self, state: RobotState) -> bool:
        return False


class TimeoutTermination:
    """单 episode 超时。"""

    def __init__(self, max_steps: int = 1000):
        self.max_steps = max_steps

    def __call__(self, step_count: int) -> bool:
        return step_count >= self.max_steps
