"""mujoco — MuJoCo / MJX 适配(**可选**,QUESTIONS B 决策)。

主仿真平台是 Isaac Sim + Isaac Lab(与 G1DWAQ_Lab-main 一致)。
MuJoCo 留作:
  - 快速 sanity check(无 Isaac 安装时)
  - 跨仿真器一致性验证(配合 Sim2SimValidator)
  - 老笔记本上跑小规模实验

默认不启用,需要时再实现。
"""
from .runner import MujocoRunner

__all__ = ["MujocoRunner"]
