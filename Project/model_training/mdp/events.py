"""域随机化(Readme §9.2)。"""
from __future__ import annotations
import numpy as np


class DomainRandomization:
    """训练时每 episode 随机化物理参数,提高 sim2real 鲁棒性。"""

    def __init__(self, ranges: dict | None = None):
        # 默认范围,Oli 专属可调
        self.ranges = ranges or {
            "mass": (0.8, 1.2),          # 质量 ±20%
            "friction": (0.5, 1.5),      # 摩擦系数
            "motor_strength": (0.9, 1.1),
            "imu_noise_std": 0.01,
            "vision_noise_std": 0.005,
        }

    def sample(self) -> dict:
        """每 episode 采样一次。"""
        return {k: np.random.uniform(*v) for k, v in self.ranges.items() if isinstance(v, tuple)}
