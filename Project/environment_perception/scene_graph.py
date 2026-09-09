"""场景图构建:把检测结果聚合成 SceneGraph(供 task_planning 消费)。"""
from __future__ import annotations
from common.types import DetectedObject, SceneGraph


class SceneGraphBuilder:
    """聚合多相机 / 多检测器结果,做时间对齐、去重、坐标统一。"""

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        # TODO: 相机外参(头/胸 → world)

    def build(
        self,
        head_objects: list[DetectedObject],
        chest_objects: list[DetectedObject] | None = None,
        timestamp_ns: int = 0,
    ) -> SceneGraph:
        """合并多视角检测结果 → SceneGraph。"""
        # TODO:
        # 1. 把 chest_objects 通过外参转到 world 坐标
        # 2. 跟 head_objects 做 NMS/去重
        # 3. 区分 objects / obstacles
        raise NotImplementedError
