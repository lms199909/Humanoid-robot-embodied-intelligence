"""task_planning.skill_library 单元测试。"""
from __future__ import annotations
import pytest
from task_planning.skill_library import SkillLibrary, SkillSpec


def test_skill_library_has_all_skills():
    lib = SkillLibrary()
    expected = {"SK_WALK", "SK_CLIMB", "SK_REACH", "SK_GRASP",
                "SK_PLACE", "SK_ASSEMBLE", "SK_STAND", "SK_TURN"}
    assert set(lib.list_ids()) == expected


def test_skill_get_returns_spec():
    lib = SkillLibrary()
    spec = lib.get("SK_CLIMB")
    assert isinstance(spec, SkillSpec)
    assert spec.requires_ee is False
    assert "left_leg" in spec.required_dofs


def test_skill_get_ee_required():
    lib = SkillLibrary()
    assert lib.get("SK_GRASP").requires_ee is True
    assert lib.get("SK_ASSEMBLE").requires_ee is True
    assert lib.get("SK_WALK").requires_ee is False


def test_skill_unknown_raises():
    lib = SkillLibrary()
    with pytest.raises(KeyError):
        lib.get("SK_NOT_EXIST")


def test_check_feasibility_default_true():
    lib = SkillLibrary()
    from task_planning.skill_library import Skill
    assert lib.check_feasibility(Skill(id="SK_WALK"), robot_state=None) is True
