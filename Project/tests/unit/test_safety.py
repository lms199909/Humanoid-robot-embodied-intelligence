"""motion_control.feedback 安全监测单元测试。"""
from __future__ import annotations
import pytest
from common.types import JointCommand
from motion_control.feedback import FeedbackMonitor


def test_feedback_default_all_checks_pass():
    fb = FeedbackMonitor()
    cmd = JointCommand(
        position=[0.0] * 31,
        velocity=[0.0] * 31,
        effort=[10.0] * 31,        # 远低于 150 N·m 限位
    )
    assert fb.check_joint_limits(cmd) is True
    assert fb.check_stability(None) is True
    assert fb.check_collision(None) is True


def test_feedback_disabled_levels():
    fb = FeedbackMonitor(config={"enabled_levels": ["L1"]})
    # L1 启用,其他禁用
    assert "L1" in fb._enabled_levels
    assert "L4" not in fb._enabled_levels
