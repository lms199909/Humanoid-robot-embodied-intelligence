"""RL 算法抽象基类(对齐 QUESTIONS C1)。

所有具体算法(PPO / DWAQ / AMP / SAC / 自实现 PPO)都实现这套接口。
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from model_training.envs import BaseEnv


class BaseRLAlgorithm(ABC):
    """RL 训练器统一抽象。

    config 必含字段:
      - num_learning_iterations: 训练总迭代数
      - save_every: checkpoint 保存间隔
    """

    def __init__(self, env: BaseEnv, config: dict, log_dir: str = "logs/"):
        self.env = env
        self.config = config
        self.log_dir = log_dir

    @abstractmethod
    def train(self) -> None:
        """主训练循环。"""
        ...

    @abstractmethod
    def save(self, path: str) -> None:
        """保存 checkpoint。"""
        ...

    @abstractmethod
    def load(self, path: str) -> None:
        """从 checkpoint 恢复(继续训练 / 评估)。"""
        ...

    @abstractmethod
    def export_onnx(self, out_path: str, opset: int = 17) -> None:
        """导出策略到 ONNX(给真机部署)。"""
        ...

    def close(self) -> None:
        """释放资源(env / 写日志 / 关闭 tensorboard)。"""
        pass
