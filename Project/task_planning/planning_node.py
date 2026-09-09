"""任务规划 ROS 2 节点入口。

订阅:/oli/llm/understand(Text) / SceneGraph
发布:/oli/planning/skill_seq(SkillSequence)

频率:1-10 Hz(慢系统)
"""
from __future__ import annotations
# from rclpy.node import Node
from common.types import SceneGraph
from .llm_client import LLMClient, VLMClient
from .task_decomposer import TaskDecomposer
from .skill_library import SkillLibrary
from .replanner import Replanner


class PlanningNode:
    """任务规划 ROS 2 节点(留 TODO 继承 rclpy.node.Node)。"""

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self.llm = LLMClient(
            endpoint=self.config.get("llm", {}).get("endpoint", ""),
            api_key=self.config.get("llm", {}).get("api_key", ""),
        )
        self.vlm = VLMClient(endpoint=self.config.get("vlm", {}).get("endpoint", ""))
        self.skills = SkillLibrary()
        self.decomposer = TaskDecomposer(llm=self.llm)
        self.replanner = Replanner(llm=self.llm)
        # TODO: super().__init__("planning_node")
        # TODO: Service(/oli/llm/understand) + Subscriber(SceneGraph) + Publisher(SkillSequence)

    def on_instruction(self, text: str, scene: SceneGraph) -> None:
        """收到自然语言指令时触发:理解 → 分解 → 发布技能序列。"""
        # TODO:
        # goal_dict = self.llm.understand_instruction(text)
        # skill_seq = self.decomposer.decompose(goal, scene)
        # self.skill_pub.publish(skill_seq)
        pass

    def on_failure(self, failure: str, current_state) -> None:
        """收到失败反馈时触发重规划。"""
        # TODO: skill_seq = self.replanner.replan(failure, ...)
        pass
