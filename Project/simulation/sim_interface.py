"""仿真统一接口(Readme §9.4 SimulationInterface)。

Sim 和 Real 共用 motion_control / perception 代码 → 通过同一接口替换传感器源。
"""
from __future__ import annotations
from common.types import RobotState, JointCommand, SceneGraph
from abc import ABC, abstractmethod


class SimInterface(ABC):
    """仿真器统一抽象。Real 模式下用空实现或 Oli SDK 替代。"""

    @abstractmethod
    def load_robot(self, urdf_path: str) -> None: ...

    @abstractmethod
    def load_scene(self, scene_config: str) -> None: ...

    @abstractmethod
    def reset(self) -> RobotState:
        """重置到初始位姿,返回初始状态。"""
        ...

    @abstractmethod
    def step(self, cmd: JointCommand) -> RobotState:
        """单步仿真,返回新状态。"""
        ...

    @abstractmethod
    def get_ground_truth(self) -> dict:
        """获取 ground truth(用于验证 / 评估,Readme §9.4)。"""
        ...

    def get_scene_graph(self) -> SceneGraph:
        """获取仿真器"看到"的场景(给 perception 模块,用于 sim2real 验证)。"""
        # TODO: 用仿真器内置 sensor API
        raise NotImplementedError
