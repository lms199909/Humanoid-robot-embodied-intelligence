"""Isaac Sim 场景加载器(楼梯 15/30/45° + 工作台)。"""
from __future__ import annotations


class IsaacSceneLoader:
    """负责把 Oli + 楼梯/工作台 USD 加载到 Isaac Sim,生成 ground truth 场景图。"""

    def __init__(self, sim_app, config: dict | None = None):
        self.sim_app = sim_app       # SimulationApp 实例
        self.config = config or {}

    def load_stair_scene(self, angle_deg: float = 30.0) -> None:
        """加载楼梯场景。"""
        # TODO: 用 IsaacLab 的 StairsCfg + 域随机化
        raise NotImplementedError

    def load_industrial_scene(self) -> None:
        """加载工业工作台(搬运 / 装配)。"""
        # TODO
        raise NotImplementedError
