"""环境感知 ROS 2 节点入口。

订阅:head_rgbd / chest_rgbd
发布:SceneGraph / ObjectList(Readme §3.3 规定的 `published` dict)

频率:30 Hz
"""
from __future__ import annotations
# from rclpy.node import Node
from .rgbd_camera import RGBDCamera
from .object_detector import ObjectDetector
from .scene_graph import SceneGraphBuilder


class PerceptionNode:
    """环境感知 ROS 2 节点(具体继承 rclpy.node.Node 留 TODO)。"""

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self.head_cam = RGBDCamera(config=self.config.get("head_cam"))
        self.chest_cam = RGBDCamera(config=self.config.get("chest_cam"))
        self.detector = ObjectDetector(
            model_path=self.config.get("detector", {}).get("model_path", "")
        )
        self.graph_builder = SceneGraphBuilder(config=self.config.get("scene_graph"))
        # TODO: super().__init__("perception_node")
        # TODO: 建订阅 / 发布 / 定时器(30Hz)

    def step(self) -> None:
        """单步:取帧 → 检测 → 构图 → 发布。"""
        # TODO:
        # rgb, depth, ts = self.head_cam.read()
        # objects = self.detector.detect(rgb, depth)
        # sg = self.graph_builder.build(objects, timestamp_ns=ts)
        # self.scene_pub.publish(sg)
        pass

    def destroy(self) -> None:
        self.head_cam.close()
        self.chest_cam.close()
