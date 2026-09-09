"""训练环境基类(对标 legged_lab.envs.base_env,Readme §11 训练任务)。"""
from __future__ import annotations
from common.types import RobotState, JointCommand
from abc import ABC, abstractmethod


class BaseEnv(ABC):
    """所有训练任务的基类(供 rsl_rl 的 OnPolicyRunner 调用)。"""

    def __init__(self, task_config: dict):
        self.cfg = task_config

    @abstractmethod
    def reset(self) -> RobotState:
        """重置 + 域随机化(Readme §9.2 域随机化)。"""
        ...

    @abstractmethod
    def step(self, action: JointCommand) -> tuple[RobotState, float, bool, dict]:
        """单步:返回 (obs, reward, done, info)。"""
        ...

    @property
    @abstractmethod
    def observation_space(self): ...

    @property
    @abstractmethod
    def action_space(self): ...
