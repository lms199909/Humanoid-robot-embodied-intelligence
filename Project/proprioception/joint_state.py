"""31 维关节状态读取(编码器 + 力矩)。"""
from __future__ import annotations
from common.types import JointState


class JointStateReader:
    """通过 Oli SDK 读所有主动关节的位置 / 速度 / 力矩。"""

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        # TODO: 打开 Oli 关节驱动(SDK)

    def read(self) -> JointState:
        """读一帧 31 维关节状态。"""
        # TODO: SDK 调用 / 解析
        raise NotImplementedError

    def send_command(self, cmd) -> None:
        """下发关节指令(测试 / 标定用,生产由 motion_control 负责)。"""
        # TODO
        raise NotImplementedError
