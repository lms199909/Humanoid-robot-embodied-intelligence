"""MuJoCo 仿真 runner(可选备用,主用 Isaac Sim,QUESTIONS B)。"""
from __future__ import annotations
from common.types import RobotState, JointCommand
from ..sim_interface import SimInterface


class MujocoRunner(SimInterface):
    """MuJoCo / MJX 仿真器封装。"""

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        # TODO: 加载 MJCF / Oli MJCF
        # import mujoco
        # self._model = mujoco.MjModel.from_xml_path(self.config["mjcf_path"])
        # self._data = mujoco.MjData(self._model)

    def load_robot(self, urdf_path: str) -> None:
        # TODO: 把 URDF 转 MJCF(用 urdf2mjcf),再加载
        pass

    def load_scene(self, scene_config: str) -> None:
        # TODO
        pass

    def reset(self) -> RobotState:
        # TODO: mujoco.mj_resetData; mujoco.mj_forward
        raise NotImplementedError

    def step(self, cmd: JointCommand) -> RobotState:
        # TODO: self._data.ctrl[:] = cmd.effort; mujoco.mj_step
        raise NotImplementedError

    def get_ground_truth(self) -> dict:
        return {}
