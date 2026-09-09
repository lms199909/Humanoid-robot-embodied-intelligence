"""6 轴 IMU 读取 + 滤波(自研 IMU,Readme §3.1)。"""
from __future__ import annotations
from common.types import IMUState


class IMUReader:
    """通过 Oli SDK 读 IMU(具体协议留 TODO)。"""

    def __init__(self, port: str = "", config: dict | None = None):
        self.port = port
        self.config = config or {}
        # TODO: 打开串口 / SDK 调用

    def read(self) -> IMUState:
        """读一帧 IMU 原始数据(已去零漂 / 已校准)。"""
        # TODO: 读 Oli SDK,做 ESKF/UKF 滤波后输出
        raise NotImplementedError

    def calibrate(self) -> None:
        """零位 / 偏差标定(机器人静止时调用)。"""
        # TODO: 采样 N 秒取平均
        pass
