"""楼梯环境(15°/30°/45° 域随机化)。"""
from __future__ import annotations
from common.types import RobotState, JointCommand
from .base_env import BaseEnv


class StairEnv(BaseEnv):
    """楼梯攀爬训练任务(对应 G1 / M2)。"""

    def __init__(self, task_config: dict):
        super().__init__(task_config)
        # TODO: 用 Isaac Lab ManagerBasedEnv 或 MuJoCo MJX env 包装

    def reset(self) -> RobotState:
        # TODO: 随机化楼梯角度 / 踏面高度 / 摩擦
        raise NotImplementedError

    def step(self, action: JointCommand) -> tuple[RobotState, float, bool, dict]:
        # TODO
        raise NotImplementedError

    @property
    def observation_space(self):
        # TODO: 33 维本体 + 楼梯几何
        raise NotImplementedError

    @property
    def action_space(self):
        # TODO: 31 维关节位置 / 力矩
        raise NotImplementedError
