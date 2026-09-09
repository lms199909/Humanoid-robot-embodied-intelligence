"""mdp — 奖励 / 终止 / 重置 / 课程学习。

借鉴 legged_lab.mdp 接口(对 Oli 重新调权重)。
"""
from .rewards import (
    StairClimbReward,
    GraspReward,
    TrackingReward,
)
from .terminations import (
    FallTermination,
    CollisionTermination,
    TimeoutTermination,
)
from .events import DomainRandomization

__all__ = [
    "StairClimbReward", "GraspReward", "TrackingReward",
    "FallTermination", "CollisionTermination", "TimeoutTermination",
    "DomainRandomization",
]
