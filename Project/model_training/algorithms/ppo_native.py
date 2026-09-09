"""PPO 实现 #2:自实现(纯 PyTorch,作为兜底 / 学习用)。

不依赖 rsl_rl,便于:
  - 教学/演示算法
  - rsl_rl 装不上时的兜底
  - 深度定制(比如加课程学习 / 特殊奖励)

参考:
  - CleanRL 的 PPO 单文件实现(https://github.com/vwxyzjn/cleanrl)
  - spinningup 的 PPO
"""
from __future__ import annotations
import torch
import torch.nn as nn
from torch.distributions import Normal
from model_training.envs import BaseEnv
from .base import BaseRLAlgorithm


class ActorCritic(nn.Module):
    """自实现 Actor-Critic 网络。"""

    def __init__(self, obs_dim: int, act_dim: int, hidden: tuple = (256, 256, 128)):
        super().__init__()
        # TODO: 用 obs_dim / act_dim 构造 actor / critic
        # actor: MLP -> mean + log_std
        # critic: MLP -> value
        self.actor = nn.Sequential(
            nn.Linear(obs_dim, hidden[0]), nn.ELU(),
            nn.Linear(hidden[0], hidden[1]), nn.ELU(),
            nn.Linear(hidden[1], hidden[2]), nn.ELU(),
        )
        self.actor_mean = nn.Linear(hidden[2], act_dim)
        self.actor_log_std = nn.Parameter(torch.zeros(act_dim))
        self.critic = nn.Sequential(
            nn.Linear(obs_dim, hidden[0]), nn.ELU(),
            nn.Linear(hidden[0], hidden[1]), nn.ELU(),
            nn.Linear(hidden[1], hidden[2]), nn.ELU(),
            nn.Linear(hidden[2], 1),
        )

    def forward(self, obs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        h = self.actor(obs)
        mean = self.actor_mean(h)
        std = self.actor_log_std.exp().expand_as(mean)
        value = self.critic(obs).squeeze(-1)
        return mean, std, value

    def act(self, obs: torch.Tensor, deterministic: bool = False) -> tuple[torch.Tensor, torch.Tensor]:
        mean, std, value = self.forward(obs)
        if deterministic:
            return mean, value
        dist = Normal(mean, std)
        a = dist.sample()
        return a, value


class PPONativeImpl(BaseRLAlgorithm):
    """自实现 PPO 训练器。"""

    def __init__(self, env: BaseEnv, config: dict, log_dir: str = "logs/"):
        super().__init__(env, config, log_dir)
        self.device = torch.device(config.get("device", "cuda:0"))
        # TODO: 用 env.observation_space / action_space 推断 obs_dim / act_dim
        self.obs_dim = 33   # TODO: 替换
        self.act_dim = 31   # TODO: 替换
        self.ac = ActorCritic(self.obs_dim, self.act_dim).to(self.device)
        self.opt = torch.optim.Adam(self.ac.parameters(), lr=config.get("lr", 3e-4))
        # PPO 关键超参
        self.clip_eps = config.get("clip_eps", 0.2)
        self.gamma = config.get("gamma", 0.99)
        self.lam = config.get("lam", 0.95)
        self.entropy_coef = config.get("entropy_coef", 0.005)
        self.update_epochs = config.get("update_epochs", 4)
        self.minibatch_size = config.get("minibatch_size", 256)

    def train(self) -> None:
        # TODO: 实现 PPO 训练循环
        # 1. rollout N 步(收集 obs/action/logp/rew/done)
        # 2. compute GAE advantages
        # 3. update_epochs 次 minibatch SGD,clip objective
        # 4. tensorboard log
        raise NotImplementedError

    def save(self, path: str) -> None:
        torch.save({"ac": self.ac.state_dict()}, path)

    def load(self, path: str) -> None:
        ckpt = torch.load(path, map_location=self.device)
        self.ac.load_state_dict(ckpt["ac"])

    def export_onnx(self, out_path: str, opset: int = 17) -> None:
        """自实现 PPO 导出 actor 到 ONNX。"""
        # TODO:
        # self.ac.eval()
        # dummy = torch.zeros(1, self.obs_dim, device=self.device)
        # torch.onnx.export(self.ac.actor, dummy, out_path, opset=opset, ...)
        raise NotImplementedError
