"""task_planning — 任务理解与规划(Readme §4-5)。

负责:
- LLM/VLM 云端 + 本地双接口(questions D1)
- 任务分解(LLM 慢系统)
- 技能库(SK_WALK / CLIMB / REACH / GRASP / ...)
- 重规划(失败检测 + 触发)

频率:1-10 Hz(慢系统)
"""
from .llm_client import (
    BaseLLMClient, BaseVLMClient,
    RemoteLLMClient, RemoteVLMClient,
    LocalLLMClient, LocalVLMClient,
    make_llm_client, make_vlm_client,
)
from .task_decomposer import TaskDecomposer
from .skill_library import SkillLibrary
from .replanner import Replanner
from .planning_node import PlanningNode

__all__ = [
    "BaseLLMClient", "BaseVLMClient",
    "RemoteLLMClient", "RemoteVLMClient",
    "LocalLLMClient", "LocalVLMClient",
    "make_llm_client", "make_vlm_client",
    "TaskDecomposer", "SkillLibrary", "Replanner",
    "PlanningNode",
]
