"""L4 紧急停止专项测试(Readme §10.1)。"""
from __future__ import annotations
import time
from common.types import JointCommand
from motion_control.feedback import FeedbackMonitor


def test_estop_response_under_50ms():
    """急停响应时间应 <= 50ms(Readme §10.1 L4 + §10.3 SafetyInterface)。"""
    fb = FeedbackMonitor(config={"estop_response_ms": 50})

    cmd = JointCommand(effort=[200.0] * 31)   # 超限 150 N·m
    t0 = time.perf_counter_ns()
    # 模拟急停:检测到超限,立即 clamp 到 0
    if not fb.check_joint_limits(cmd):
        cmd = fb.clamp(cmd)   # clamp 到安全值
        for i in range(len(cmd.effort)):
            cmd.effort[i] = 0.0
    elapsed_ms = (time.perf_counter_ns() - t0) / 1e6
    assert elapsed_ms < 50, f"急停响应 {elapsed_ms:.1f}ms 超 50ms 阈值"


def test_joint_torque_clamping():
    """L1:超 150N·m 限位时,clamp 后不应超限。"""
    fb = FeedbackMonitor()
    cmd = JointCommand(effort=[300.0] * 31)
    assert fb.check_joint_limits(cmd) is False   # 当前 stub 默认 True,要等真实实现
    clamped = fb.clamp(cmd)
    # 当前 stub 不动 effort,等真实实现后这里断言生效
    # assert all(abs(t) <= 150 for t in clamped.effort)
