"""DWAQ 训练器(QUESTIONS C5:留接口)。

DWAQ = Discriminator-Weighted Actor-Q,AMP-style 风格 + latent code。
参考:`TienKung-Lab/rsl_rl/algorithms/dwaq_ppo.py` + `TienKung-Lab/docs/DWAQ_LATENT_CODE.md`。

实现策略:优先调 rsl_rl 的 DWAQ 实现(如果有),否则自实现。
"""
from __future__ import annotations
from model_training.envs import BaseEnv
from .base import BaseRLAlgorithm


class DWAQTrainer(BaseRLAlgorithm):
    """DWAQ 训练器:AMP 风格判别器 + PPO。"""

    def __init__(self, env: BaseEnv, config: dict, log_dir: str = "logs/", impl: str = "rsl_rl"):
        super().__init__(env, config, log_dir)
        self.impl_kind = impl
        self._impl = None
        # TODO:
        # if impl == "rsl_rl":
        #     from rsl_rl.algorithms import DWAQPPO
        #     self._impl = DWAQPPO(...)
        # elif impl == "native":
        #     from .dwaq_native import DWAQNativeImpl
        #     self._impl = DWAQNativeImpl(env, config, log_dir)
        raise NotImplementedError("DWAQ 接口已留,具体实现等 TienKung-Lab 适配时填")

    def train(self) -> None:
        raise NotImplementedError

    def save(self, path: str) -> None:
        raise NotImplementedError

    def load(self, path: str) -> None:
        raise NotImplementedError

    def export_onnx(self, out_path: str, opset: int = 17) -> None:
        raise NotImplementedError
