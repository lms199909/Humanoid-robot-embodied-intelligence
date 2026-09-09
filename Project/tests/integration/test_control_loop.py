"""控制回路集成测试(MPC + WBC + Servo 三层)。"""
from __future__ import annotations
import numpy as np
from common.types import Skill, RobotState, JointState, IMUState, JointCommand
from motion_control.skill_executor import SkillExecutor
from motion_control.control_node import ControlNode


def make_dummy_state() -> RobotState:
    return RobotState(
        joint=JointState(position=[0.0] * 31, velocity=[0.0] * 31, effort=[0.0] * 31),
        imu=IMUState(),
        base_pose=(0, 0, 1.0, 0, 0, 0, 1),
        timestamp_ns=0,
    )


def test_control_node_construction():
    """ControlNode 能构造(不实际跑 tick)。"""
    node = ControlNode(config={"urdf_path": "dummy.urdf"})
    assert node.mpc is not None
    assert node.wbc is not None
    assert node.feedback is not None
    assert node.executor is not None
    assert node.servo is None   # 默认未注入(sim 模式)


def test_skill_executor_idle_by_default():
    from motion_control.mpc import MPCPlanner
    mpc = MPCPlanner()
    ex = SkillExecutor(mpc=mpc)
    assert ex.is_running is False


def test_control_node_tick_2khz_without_servo_is_noop():
    """无 servo 注入时,2kHz tick 不应抛。"""
    node = ControlNode(config={})
    cmd = JointCommand(position=[0.0] * 31, velocity=[0.0] * 31, effort=[0.0] * 31)
    node.tick_2khz(cmd)   # 不应抛
