"""本体感知 ROS 2 节点入口。

订阅:imu / joint_states / ft_sensor
发布:RobotState(1 kHz,Readme §3.3)
"""
from __future__ import annotations
# from rclpy.node import Node
from common.types import RobotState
from .imu_reader import IMUReader
from .joint_state import JointStateReader
from .state_estimator import StateEstimator


class ProprioceptionNode:
    """本体感知 ROS 2 节点(留 TODO 继承 rclpy.node.Node)。"""

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self.imu = IMUReader(config=self.config.get("imu"))
        self.joints = JointStateReader(config=self.config.get("joints"))
        self.estimator = StateEstimator(
            urdf_path=self.config.get("urdf_path", ""),
            config=self.config.get("estimator"),
        )
        # TODO: super().__init__("proprioception_node")
        # TODO: 1kHz 定时器 + 发布 RobotState

    def step(self) -> RobotState:
        """单步:读 IMU+关节 → 融合 → 输出 RobotState。"""
        # TODO:
        # imu = self.imu.read()
        # joint = self.joints.read()
        # return self.estimator.estimate(imu, joint)
        raise NotImplementedError
