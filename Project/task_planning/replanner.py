"""重规划:失败检测 + 触发(Readme §5.1 重规划机制 + §7.2 失败分类)。

失败类型:
  F_STABILITY / F_GRASP / F_COLLISION / F_TRAJECTORY / F_TIMEOUT / F_PERCEPTION
"""
from __future__ import annotations
from common.types import SkillSequence, FailureType, RobotState
from .llm_client import LLMClient


class Replanner:
    """失败时调 LLM 重规划,LLM 不可用时降级。"""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def detect_failure(self, expected_state: dict, actual_state: dict) -> str:
        """失败检测 + 分类(Readme §7.3 `classify_failure`)。"""
        # TODO: 阈值规则 + 异常检测
        raise NotImplementedError

    def replan(
        self,
        failure: str,
        failed_skill_id: str,
        current_state: RobotState,
        scene: dict | None = None,
    ) -> SkillSequence:
        """触发重规划(Readme §5.3 `replan`)。"""
        # TODO:
        # try:
        #     return self.llm.replan(failure, current_state.__dict__)
        # except Timeout:
        #     return self._fallback_replan(failure, failed_skill_id)
        raise NotImplementedError

    def _fallback_replan(self, failure: str, failed_skill_id: str) -> SkillSequence:
        """LLM 不可用时的硬编码兜底(Readme §10.2)。"""
        # TODO: 比如 F_GRASP → 重试一次;F_STABILITY → SK_STAND
        raise NotImplementedError
