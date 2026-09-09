"""PPO 训练器(QUESTIONS C1:rsl_rl + 自实现 双接口,统一通过 BaseRLAlgorithm)。

调用方用工厂 `make_ppo_trainer(env, config, impl="rsl_rl" | "native")` 选择实现。
"""
from __future__ import annotations
from model_training.envs import BaseEnv
from .base import BaseRLAlgorithm


class PPOTrainer(BaseRLAlgorithm):
    """PPO 训练器:基类 wrapper,通过 `self._impl` 委托到具体实现。

    使用方式:
        trainer = PPOTrainer(env, config, impl="rsl_rl")  # 调 rsl_rl
        trainer = PPOTrainer(env, config, impl="native")   # 调自实现
        trainer.train()
    """

    def __init__(self, env: BaseEnv, config: dict, log_dir: str = "logs/", impl: str = "rsl_rl"):
        super().__init__(env, config, log_dir)
        self.impl_kind = impl
        if impl == "rsl_rl":
            from .ppo_rsl_rl import PPORslRlImpl
            self._impl = PPORslRlImpl(env, config, log_dir)
        elif impl == "native":
            from .ppo_native import PPONativeImpl
            self._impl = PPONativeImpl(env, config, log_dir)
        else:
            raise ValueError(f"unknown ppo impl: {impl!r}, expected 'rsl_rl' or 'native'")

    def train(self) -> None:
        self._impl.train()

    def save(self, path: str) -> None:
        self._impl.save(path)

    def load(self, path: str) -> None:
        self._impl.load(path)

    def export_onnx(self, out_path: str, opset: int = 17) -> None:
        self._impl.export_onnx(out_path, opset=opset)


def make_ppo_trainer(env: BaseEnv, config: dict, log_dir: str = "logs/", impl: str = "rsl_rl") -> PPOTrainer:
    """工厂:按 config["algorithm"]["impl"] 选 PPO 实现。"""
    impl = config.get("algorithm", {}).get("impl", impl)
    return PPOTrainer(env, config, log_dir=log_dir, impl=impl)
