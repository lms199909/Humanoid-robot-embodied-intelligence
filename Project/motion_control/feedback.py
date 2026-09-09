"""执行反馈 / 安全监测(Readme §7 + §10,横切关注点)。

L1 关节力矩限位
L2 姿态稳定监测
L3 碰撞检测
L4 紧急停止
L5 通信超时
"""
from __future__ import annotations
from common.types import JointCommand, RobotState, FailureType


class FeedbackMonitor:
    """安全监测器:每个控制周期做检查,触发时降级 / 急停。"""

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self._enabled_levels = self.config.get("enabled_levels", ["L1", "L2", "L3", "L4", "L5"])
        # TODO: 加载各等级阈值(YAML)

    def check_joint_limits(self, cmd: JointCommand) -> bool:
        """L1:关节力矩限位。"""
        # TODO: torque_max = config["limits"]["max_torque_nm"]
        # return all(abs(t) <= torque_max for t in cmd.effort)
        return True

    def check_stability(self, state: RobotState) -> bool:
        """L2:姿态稳定(roll/pitch 角度 / 角速度阈值)。"""
        # TODO
        return True

    def check_collision(self, state: RobotState) -> bool:
        """L3:碰撞检测(关节力矩突变 / 外力估计)。"""
        # TODO
        return True

    def check_comm_timeout(self, last_msg_ts: int, now_ts: int) -> bool:
        """L5:通信超时(>3s 视为降级)。"""
        # TODO
        return True

    def clamp(self, cmd: JointCommand) -> JointCommand:
        """把超限指令钳到安全范围。"""
        # TODO: 复制 cmd,把超限 effort 钳到 ±max_torque_nm
        return cmd

    def classify_failure(self, expected, actual) -> str:
        """失败分类(Readme §7.2)。"""
        # TODO: 用阈值规则 + 异常检测做分类
        return FailureType.F_TIMEOUT
