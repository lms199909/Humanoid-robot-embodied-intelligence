"""RGB-D 相机驱动 + 标定(RealSense D435i,Readme §3.1)。

负责:
- 打开 / 关闭相机
- 同步取 RGB + Depth
- 内参 / 外参加载(标定 YAML)
- 帧时间戳对齐
"""
from __future__ import annotations
import numpy as np


class RGBDCamera:
    """RealSense D435i 抽象(Oli 头部 + 胸部各 1 台)。"""

    def __init__(self, serial: str = "", config: dict | None = None):
        self.serial = serial
        self.config = config or {}
        self._pipeline = None  # TODO: pyrealsense2 pipeline
        self._intrinsics = None  # TODO: 内参

    def open(self) -> None:
        """启动相机 pipeline,读取内参。"""
        # TODO: 用 pyrealsense2 启动
        # config = rs.config()
        # config.enable_device(self.serial)
        # config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        # self._pipeline.start(config)
        pass

    def read(self) -> tuple[np.ndarray, np.ndarray, int]:
        """同步读取一帧 RGB + Depth。

        Returns:
            rgb: HxWx3 uint8
            depth: HxW uint16(单位 mm)
            timestamp_ns
        """
        # TODO: frames = self._pipeline.wait_for_frames()
        raise NotImplementedError

    def close(self) -> None:
        # TODO: self._pipeline.stop()
        pass

    @property
    def intrinsics(self):
        # TODO: return self._intrinsics
        raise NotImplementedError
