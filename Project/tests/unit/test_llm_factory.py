"""task_planning.llm_client 工厂单元测试。"""
from __future__ import annotations
from task_planning.llm_client import (
    make_llm_client, make_vlm_client,
    RemoteLLMClient, LocalLLMClient,
    RemoteVLMClient, LocalVLMClient,
)


def test_make_remote_llm():
    cfg = {"llm": {"mode": "remote", "endpoint": "https://api.deepseek.com/v1",
                   "api_key": "sk-test", "model": "deepseek-chat"}}
    c = make_llm_client(cfg)
    assert isinstance(c, RemoteLLMClient)
    assert c.endpoint == "https://api.deepseek.com/v1"
    assert c.model == "deepseek-chat"


def test_make_local_llm():
    cfg = {"llm": {"mode": "local", "endpoint": "http://127.0.0.1:8000",
                   "model": "Qwen2.5-7B", "timeout_s": 5.0}}
    c = make_llm_client(cfg)
    assert isinstance(c, LocalLLMClient)
    assert c.timeout_s == 5.0
    assert c.api_key == "EMPTY"   # 本地默认无 key


def test_make_remote_vlm():
    cfg = {"vlm": {"mode": "remote", "endpoint": "https://api.openai.com/v1",
                   "api_key": "sk-test"}}
    c = make_vlm_client(cfg)
    assert isinstance(c, RemoteVLMClient)


def test_make_local_vlm():
    cfg = {"vlm": {"mode": "local"}}
    c = make_vlm_client(cfg)
    assert isinstance(c, LocalVLMClient)
    assert c.endpoint == "http://127.0.0.1:8001"   # 默认本地端点


def test_default_mode_is_remote():
    """未指定 mode 时默认 remote。"""
    c = make_llm_client({})
    assert isinstance(c, RemoteLLMClient)
