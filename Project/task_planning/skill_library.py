"""技能库(Readme §5.2):8 个基元技能。

SK_WALK / SK_CLIMB / SK_REACH / SK_GRASP / SK_PLACE / SK_ASSEMBLE / SK_STAND / SK_TURN
每个技能描述它的:
  - 入参(目标位姿 / 物体 / 力)
  - 出参(成功 / 失败 + 错误码)
  - 依赖(需要哪些关节 / 末端执行器)
  - 触发条件(需要什么前置状态)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from common.types import Skill


@dataclass
class SkillSpec:
    id: str
    name: str
    description: str
    required_dofs: list[str] = field(default_factory=list)
    requires_ee: bool = False   # 末端执行器
    timeout_s: float = 30.0


class SkillLibrary:
    """技能注册表。每个 SkillSpec 提供一个 callable 实现(后续可独立 .py 文件)。"""

    SKILLS: dict[str, SkillSpec] = {
        "SK_WALK": SkillSpec(
            id="SK_WALK", name="平地行走",
            description="双足行走,速度<=5km/h",
            required_dofs=["left_leg", "right_leg"],
        ),
        "SK_CLIMB": SkillSpec(
            id="SK_CLIMB", name="斜梯攀爬",
            description="斜坡/阶梯攀爬",
            required_dofs=["left_leg", "right_leg", "left_arm", "right_arm", "waist"],
        ),
        "SK_REACH": SkillSpec(
            id="SK_REACH", name="手臂伸展",
            description="末端到达目标位置",
            required_dofs=["left_arm", "right_arm", "waist"],
        ),
        "SK_GRASP": SkillSpec(
            id="SK_GRASP", name="抓取",
            description="夹爪闭合抓取物体",
            required_dofs=["left_arm", "right_arm"],
            requires_ee=True,
        ),
        "SK_PLACE": SkillSpec(
            id="SK_PLACE", name="放置",
            description="将物体放置到目标位置",
            required_dofs=["left_arm", "right_arm"],
            requires_ee=True,
        ),
        "SK_ASSEMBLE": SkillSpec(
            id="SK_ASSEMBLE", name="装配",
            description="精准插入/旋拧操作",
            required_dofs=["left_arm", "right_arm", "waist"],
            requires_ee=True,
        ),
        "SK_STAND": SkillSpec(
            id="SK_STAND", name="站立平衡",
            description="静态站立保持",
            required_dofs=["left_leg", "right_leg", "waist"],
        ),
        "SK_TURN": SkillSpec(
            id="SK_TURN", name="转向",
            description="原地转向",
            required_dofs=["left_leg", "right_leg", "waist"],
        ),
    }

    def get(self, skill_id: str) -> SkillSpec:
        if skill_id not in self.SKILLS:
            raise KeyError(f"unknown skill: {skill_id}")
        return self.SKILLS[skill_id]

    def list_ids(self) -> list[str]:
        return list(self.SKILLS.keys())

    def check_feasibility(self, skill: Skill, robot_state) -> bool:
        """检查机器人状态是否能执行该 skill(关节健康 / 末端在线等)。"""
        # TODO: 跟 StateEstimator 输出比对
        return True
