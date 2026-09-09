"""任务分解器:把 TaskGoal + SceneGraph → SkillSequence。

通常由 LLM 慢系统驱动,失败时降级到本地预设模板(Readme §10.2 降级策略)。
"""
from __future__ import annotations
from common.types import TaskGoal, SceneGraph, SkillSequence
from .llm_client import LLMClient


class TaskDecomposer:
    """调用 LLM 做任务分解;LLM 失败时降级到本地模板。"""

    def __init__(self, llm: LLMClient, fallback_template: dict | None = None):
        self.llm = llm
        self.fallback_template = fallback_template or self._default_template()

    def decompose(self, goal: TaskGoal, scene: SceneGraph) -> SkillSequence:
        """任务分解主入口。"""
        # TODO:
        # try:
        #     raw = self.llm.decompose(goal.__dict__, scene.__dict__)
        #     return self._parse_skill_sequence(raw)
        # except (Timeout, LLMError):
        #     return self._fallback(goal, scene)
        raise NotImplementedError

    def _fallback(self, goal: TaskGoal, scene: SceneGraph) -> SkillSequence:
        """降级:用预设模板(Readme §10.2)。"""
        # TODO: 按 goal.type 选模板
        raise NotImplementedError

    @staticmethod
    def _default_template() -> dict:
        # TODO: 几个常见任务的预设模板(assembly / transport / climb)
        return {}
