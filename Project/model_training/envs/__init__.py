"""envs — 训练任务环境。

每个任务一个 .py:继承自 base_env.BaseEnv(对 Isaac Lab / MuJoCo 都做适配)。
"""
from .base_env import BaseEnv
from .stair_env import StairEnv       # 楼梯
from .industrial_env import IndustrialEnv   # 工业装配

__all__ = ["BaseEnv", "StairEnv", "IndustrialEnv"]
