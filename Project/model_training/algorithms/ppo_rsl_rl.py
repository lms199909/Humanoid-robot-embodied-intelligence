"""PPO 实现 #1:基于 rsl_rl(pip 装,直接复用)。"""
from __future__ import annotations
from model_training.envs import BaseEnv
from .base import BaseRLAlgorithm


class PPORslRlImpl(BaseRLAlgorithm):
    """rsl_rl OnPolicyRunner 包装,实现 PPO。"""

    def __init__(self, env: BaseEnv, config: dict, log_dir: str = "logs/"):
        super().__init__(env, config, log_dir)
        self._runner = None
        # TODO:
        # from rsl_rl.runners import OnPolicyRunner
        # self._runner = OnPolicyRunner(env, config, log_dir=log_dir)
        # 关键 config 项:
        #   algorithm: {class_name: PPO, learning_rate, num_steps_per_env, ...}
        #   policy: {class_name: ActorCritic, init_noise_std, actor_hidden_dims, ...}

    def train(self) -> None:
        # TODO: self._runner.learn(num_learning_iterations=self.config["max_iterations"])
        raise NotImplementedError

    def save(self, path: str) -> None:
        # TODO: self._runner.save(path)
        pass

    def load(self, path: str) -> None:
        # TODO: self._runner.load(path)
        pass

    def export_onnx(self, out_path: str, opset: int = 17) -> None:
        """从 rsl_rl checkpoint 导出 actor 网络到 ONNX。"""
        # TODO:
        # 1. 加载 checkpoint(.pt)
        # 2. 提取 actor 模型 state_dict
        # 3. 构造 dummy obs(33 维)
        # 4. torch.onnx.export(actor, dummy, out_path, opset=opset,
        #                       input_names=["obs"], output_names=["action"],
        #                       dynamic_axes={"obs": {0: "batch"}, "action": {0: "batch"}})
        # 5. onnxruntime 验证一次
        raise NotImplementedError
