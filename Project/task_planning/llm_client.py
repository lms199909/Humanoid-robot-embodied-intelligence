"""云端 LLM / VLM 客户端(对齐 Readme §8.4 + QUESTIONS D1)。

按 D1 决策:同时保留两种调用方式,通过统一抽象 + 工厂方法注入:
  - RemoteLLMClient:HTTP REST 调云端(OpenAI/DeepSeek/自建 API)
  - LocalLLMClient:本地推理(vLLM / TGI / llama.cpp,OpenAI-compatible 协议)

机内 → 服务器的 WebSocket 桥放在 `communication/websocket_bridge/`(后续 M2 落)。
这里只关心 LLM 协议层。
"""
from __future__ import annotations
import time
from abc import ABC, abstractmethod
from typing import Any


# ============================================================
# LLM 抽象基类
# ============================================================

class BaseLLMClient(ABC):
    """LLM 客户端统一接口(Remote / Local 共用)。"""

    def __init__(self, timeout_s: float = 2.0, **kwargs):
        self.timeout_s = timeout_s

    @abstractmethod
    def understand_instruction(self, text: str) -> dict:
        """自然语言 -> TaskGoal dict。"""
        ...

    @abstractmethod
    def decompose(self, goal: dict, scene: dict) -> list[dict]:
        """任务分解 -> SkillSequence(原始 dict 列表,调用方负责包装 Skill)。"""
        ...

    @abstractmethod
    def replan(self, failure: str, state: dict) -> list[dict]:
        """重规划(失败后调用)。"""
        ...

    def close(self) -> None:
        """释放连接(R1:子类按需覆盖)。"""
        pass


# ============================================================
# Remote 实现:HTTP REST 调云端
# ============================================================

class RemoteLLMClient(BaseLLMClient):
    """云端 LLM 客户端(POST/JSON,2s 超时)。

    适配 OpenAI-compatible 协议(/v1/chat/completions),覆盖:
      - OpenAI / Anthropic(走代理)/ DeepSeek / 智谱 / 自建 OpenAI-compatible API
    """

    def __init__(
        self,
        endpoint: str = "",
        api_key: str = "",
        model: str = "gpt-4o-mini",
        timeout_s: float = 2.0,
        max_retries: int = 1,
    ):
        super().__init__(timeout_s=timeout_s)
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries
        # TODO: 用 httpx.AsyncClient(避免阻塞机载控制回路)

    def understand_instruction(self, text: str) -> dict:
        # TODO:
        # payload = {"model": self.model, "messages": [
        #     {"role": "system", "content": "<理解指令的 system prompt>"},
        #     {"role": "user", "content": text},
        # ], "response_format": {"type": "json_object"}}
        # resp = httpx.post(f"{self.endpoint}/v1/chat/completions",
        #                   json=payload,
        #                   headers={"Authorization": f"Bearer {self.api_key}"},
        #                   timeout=self.timeout_s)
        # return json.loads(resp.json()["choices"][0]["message"]["content"])
        raise NotImplementedError

    def decompose(self, goal: dict, scene: dict) -> list[dict]:
        # TODO: 同上,prompt 换成"任务分解 + 输出 JSON 技能序列"
        raise NotImplementedError

    def replan(self, failure: str, state: dict) -> list[dict]:
        # TODO: 同上,prompt 换成"重规划"
        raise NotImplementedError


# ============================================================
# Local 实现:本地推理(走 OpenAI-compatible 协议)
# ============================================================

class LocalLLMClient(BaseLLMClient):
    """本地 LLM 客户端。

    假设本地推理服务走 OpenAI-compatible HTTP(覆盖 vLLM / TGI / llama.cpp server 等)。
    本机地址默认 127.0.0.1:8000。
    """

    def __init__(
        self,
        endpoint: str = "http://127.0.0.1:8000",
        model: str = "local-model",
        api_key: str = "EMPTY",   # 本地服务通常不校验
        timeout_s: float = 5.0,   # 本地推理比云端慢,超时放宽
    ):
        super().__init__(timeout_s=timeout_s)
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.api_key = api_key
        # TODO: httpx.Client 预热连接池

    def understand_instruction(self, text: str) -> dict:
        # TODO: 同 RemoteLLMClient,只是 endpoint 是本地服务
        raise NotImplementedError

    def decompose(self, goal: dict, scene: dict) -> list[dict]:
        # TODO
        raise NotImplementedError

    def replan(self, failure: str, state: dict) -> list[dict]:
        # TODO
        raise NotImplementedError


# ============================================================
# VLM 抽象 + 双实现(对齐 D3:VLM 单独接口)
# ============================================================

class BaseVLMClient(ABC):
    """VLM 客户端统一接口。"""

    def __init__(self, timeout_s: float = 2.0, **kwargs):
        self.timeout_s = timeout_s

    @abstractmethod
    def understand_scene(self, image_bytes: bytes, prompt: str = "") -> dict:
        """图像 -> 场景图 dict。"""
        ...

    def close(self) -> None:
        pass


class RemoteVLMClient(BaseVLMClient):
    """云端 VLM(走 OpenAI-compatible vision 接口,或专用 VLM API)。"""

    def __init__(self, endpoint: str = "", api_key: str = "", model: str = "gpt-4o", timeout_s: float = 2.0):
        super().__init__(timeout_s=timeout_s)
        self.endpoint = endpoint
        self.api_key = api_key
        self.model = model
        # TODO: 图片转 base64 + multipart

    def understand_scene(self, image_bytes: bytes, prompt: str = "") -> dict:
        # TODO
        raise NotImplementedError


class LocalVLMClient(BaseVLMClient):
    """本地 VLM(LLaVA / InternVL 等 OpenAI-compatible 部署)。"""

    def __init__(self, endpoint: str = "http://127.0.0.1:8001", model: str = "llava", timeout_s: float = 5.0):
        super().__init__(timeout_s=timeout_s)
        self.endpoint = endpoint
        self.model = model
        # TODO
        pass

    def understand_scene(self, image_bytes: bytes, prompt: str = "") -> dict:
        # TODO
        raise NotImplementedError


# ============================================================
# 工厂:按 config 选 Remote / Local
# ============================================================

def make_llm_client(config: dict) -> BaseLLMClient:
    """按 config["llm"] 自动选 Remote / Local 实现。

    config 示例:
      {"llm": {"mode": "remote", "endpoint": "https://api.deepseek.com/v1",
               "api_key": "sk-...", "model": "deepseek-chat", "timeout_s": 2.0}}
      {"llm": {"mode": "local", "endpoint": "http://127.0.0.1:8000",
               "model": "Qwen2.5-7B-Instruct", "timeout_s": 5.0}}
    """
    cfg = config.get("llm", {})
    mode = cfg.get("mode", "remote")
    if mode == "local":
        return LocalLLMClient(
            endpoint=cfg.get("endpoint", "http://127.0.0.1:8000"),
            model=cfg.get("model", "local-model"),
            api_key=cfg.get("api_key", "EMPTY"),
            timeout_s=cfg.get("timeout_s", 5.0),
        )
    return RemoteLLMClient(
        endpoint=cfg.get("endpoint", ""),
        api_key=cfg.get("api_key", ""),
        model=cfg.get("model", "gpt-4o-mini"),
        timeout_s=cfg.get("timeout_s", 2.0),
    )


def make_vlm_client(config: dict) -> BaseVLMClient:
    """VLM 工厂(同上,独立 endpoint)。"""
    cfg = config.get("vlm", {})
    mode = cfg.get("mode", "remote")
    if mode == "local":
        return LocalVLMClient(
            endpoint=cfg.get("endpoint", "http://127.0.0.1:8001"),
            model=cfg.get("model", "llava"),
            timeout_s=cfg.get("timeout_s", 5.0),
        )
    return RemoteVLMClient(
        endpoint=cfg.get("endpoint", ""),
        api_key=cfg.get("api_key", ""),
        model=cfg.get("model", "gpt-4o"),
        timeout_s=cfg.get("timeout_s", 2.0),
    )
