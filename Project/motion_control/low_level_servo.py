"""底层关节伺服(Readme §6.1 执行层,2kHz)。

把 JointCommand(关节空间指令)转发到 Oli 关节驱动,做底层限位 + 安全 hook。
"""
from __future__ import annotations
from common.types import JointCommand
from .feedback import FeedbackMonitor


class LowLevelServo:
    """关节底层伺服(发命令到 Oli SDK,带 L1 关节力矩限位 + L3 碰撞检测)。"""

    def __init__(self, sdk_client, config: dict | None = None):
        self.sdk = sdk_client                # Oli SDK
        self.config = config or {}
        self.feedback = FeedbackMonitor(config=self.config.get("safety"))
        # TODO: 初始化 Oli 关节驱动(2kHz 实时线程)

    def step(self, cmd: JointCommand) -> None:
        """单步:做安全检查后下发到 Oli 关节。"""
        # TODO:
        # 1. self.feedback.check_joint_limits(cmd)  # L1
        # 2. if not ok: cmd = self.feedback.clamp(cmd)
        # 3. self.sdk.send_joint_cmd(cmd)
        pass

    def emergency_stop(self) -> None:
        """L4 紧急停止(50ms 内响应,Readme §10.1)。"""
        # TODO: sdk.estop()
        pass
