"""Isaac ↔ ROS 2 桥(让 ROS 节点在 Isaac 仿真里跑同一份代码)。"""
from __future__ import annotations


class IsaacBridge:
    """封装 Isaac ROS Bridge(由 NVIDIA 提供)或自实现 sensor/topic 同步。"""

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        # TODO: 启动 isaac_ros_bridge 节点

    def publish_camera(self, name: str, rgb, depth) -> None:
        """把 Isaac 的相机图像发布到 ROS 2 topic。"""
        # TODO
        pass

    def publish_joint_states(self, joint_state) -> None:
        """把 Isaac 的关节状态发到 /oli/sensors/joint_states。"""
        # TODO
        pass
