"""common.types 的单元测试。"""
from __future__ import annotations
from common.types import JointState, RobotState, TaskGoal, Skill, SkillSequence, FailureType


def test_joint_state_default_construction():
    js = JointState()
    assert js.name == []
    assert js.position == []
    assert js.timestamp_ns == 0


def test_robot_state_nested():
    rs = RobotState()
    assert rs.joint is None
    assert rs.base_pose == (0, 0, 0, 0, 0, 0, 1)


def test_skill_sequence_construction():
    seq = SkillSequence(skills=[Skill(id="SK_WALK"), Skill(id="SK_GRASP")])
    assert len(seq.skills) == 2
    assert seq.skills[0].id == "SK_WALK"


def test_failure_type_constants():
    # 字符串值,便于 ROS 2 / JSON 序列化
    assert FailureType.F_STABILITY == "F_STABILITY"
    assert FailureType.F_GRASP == "F_GRASP"


def test_task_goal_to_dict():
    g = TaskGoal(type="assembly", target="螺丝", location="工作台")
    d = g.__dict__
    assert d["type"] == "assembly"
    assert d["target"] == "螺丝"
