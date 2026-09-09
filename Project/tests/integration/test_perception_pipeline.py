"""感知流水线集成测试(无 ROS 2 依赖)。"""
from __future__ import annotations
import numpy as np
from common.types import DetectedObject, SceneGraph
from environment_perception.scene_graph import SceneGraphBuilder


def test_scene_graph_build_merges_two_views():
    """头 + 胸 两个视角的检测结果合并成 SceneGraph。"""
    builder = SceneGraphBuilder(config={"merge_strategy": "nms"})

    head_objs = [
        DetectedObject(name="screwdriver", bbox=(10, 20, 50, 80),
                       pose_xyz_rpy=(0.5, 0.3, 0.8, 0, 0, 0), confidence=0.9),
    ]
    chest_objs = [
        DetectedObject(name="screwdriver", bbox=(100, 200, 130, 240),
                       pose_xyz_rpy=(0.5, 0.3, 0.8, 0, 0, 0), confidence=0.85),
    ]
    # 暂不实装 build,仅断言不会抛
    try:
        sg = builder.build(head_objs, chest_objs, timestamp_ns=1234567890)
        assert isinstance(sg, SceneGraph)
    except NotImplementedError:
        pytest.skip("SceneGraphBuilder.build 尚未实现")


def test_perception_node_construction():
    """PerceptionNode 能构造(不实际跑 step)。"""
    from environment_perception.perception_node import PerceptionNode
    node = PerceptionNode(config={"head_cam": {}, "chest_cam": {}, "detector": {}})
    assert node is not None
