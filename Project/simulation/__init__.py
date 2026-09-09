"""simulation — 仿真调用(Readme §9,QUESTIONS B:对齐 G1DWAQ_Lab-main 用 Isaac Sim)。

主用:Isaac Sim + Isaac Lab(高保真物理 + 视觉,与 G1DWAQ_Lab-main 一致)
备用:MuJoCo / MJX(可选,目前仅在 Oli URDF 还没准备好 / 需要快速 sanity 时用)

通过统一 SimInterface 抽象,让 motion_control / perception 跑同一份代码。
"""
from .sim_interface import SimInterface
from .isaac_sim.scene_loader import IsaacSceneLoader
from .isaac_sim.bridge import IsaacBridge
from .mujoco.runner import MujocoRunner      # 可选
from .sim2sim import Sim2SimValidator

__all__ = [
    "SimInterface",
    "IsaacSceneLoader", "IsaacBridge",
    "MujocoRunner",         # 可选备用
    "Sim2SimValidator",
]
