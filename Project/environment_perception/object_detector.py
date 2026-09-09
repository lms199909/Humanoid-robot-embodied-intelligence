"""目标检测 + 6D 位姿估计(物体识别 / 抓取定位)。"""
from __future__ import annotations
import numpy as np
from common.types import DetectedObject


class ObjectDetector:
    """通用检测器抽象(后续可换 YOLO / DINO / FoundationPose 等)。"""

    def __init__(self, model_path: str = "", config: dict | None = None):
        self.model_path = model_path
        self.config = config or {}
        # TODO: 加载 ONNX / TorchScript 模型(onnxruntime 或 torch)

    def detect(self, rgb: np.ndarray, depth: np.ndarray | None = None) -> list[DetectedObject]:
        """从 RGB(+可选 Depth)输出物体列表。

        Returns:
            list[DetectedObject]:含 bbox、6D 位姿、置信度。
        """
        # TODO: 推理
        raise NotImplementedError

    @staticmethod
    def from_model_storage(storage, name: str, version: str) -> "ObjectDetector":
        """从 model_storage 加载(对齐 model_storage.ModelRegistry 接口)。"""
        # TODO: path = storage.get_path(name, version)
        raise NotImplementedError
