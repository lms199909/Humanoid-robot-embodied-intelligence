"""algorithms — RL 算法库(QUESTIONS C1:同时支持 rsl_rl 和自实现)。

支持的算法:
  - PPO:rsl_rl 实现 + 自实现 PyTorch 实现
  - DWAQ:rsl_rl 实现(留接口,等适配)
  - AMP / SAC / TD3 等:留扩展位

调用方式:
  from model_training.algorithms import make_ppo_trainer
  trainer = make_ppo_trainer(env, config, impl="rsl_rl")
"""
from .base import BaseRLAlgorithm
from .ppo import PPOTrainer, make_ppo_trainer
from .dwaq import DWAQTrainer

__all__ = [
    "BaseRLAlgorithm",
    "PPOTrainer", "make_ppo_trainer",
    "DWAQTrainer",
]
