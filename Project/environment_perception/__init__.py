"""environment_perception — 环境感知层(Readme §3)。

负责把 RGB-D 图像转成场景图(物体列表 + 位姿 + 语义标签)。
频率:30 Hz。

对应 Readme 接口:`PerceptionInterface`(§3.3)
对应 G1DWAQ_Lab-main:`TienKung-Lab/legged_lab/sensors/`(接口参考)
"""
from .rgbd_camera import RGBDCamera
from .object_detector import ObjectDetector
from .scene_graph import SceneGraphBuilder
from .perception_node import PerceptionNode

__all__ = ["RGBDCamera", "ObjectDetector", "SceneGraphBuilder", "PerceptionNode"]
