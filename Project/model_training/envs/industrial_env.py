"""工业装配环境(搬运 / 装配)。"""
from __future__ import annotations
from common.types import RobotState, JointCommand
from .base_env import BaseEnv


class IndustrialEnv(BaseEnv):
    """工业装配训练任务(对应 G2 / M3)。"""

    def __init__(self, task_config: dict):
        super().__init__(task_config)
        # TODO: 工作台 + 待装配物体

    def reset(self) -> RobotState:
        # TODO: 随机化物体位置 / 工作台高度
        raise NotImplementedError

    def step(self, action: JointCommand) -> tuple[RobotState, float, bool, dict]:
        # TODO
        raise NotImplementedError

    @property
    def observation_space(self):
        # TODO: 本体 + 物体位姿 + 工作台
        raise NotImplementedError

    @property
    def action_space(self):
        # TODO
        raise NotImplementedError
