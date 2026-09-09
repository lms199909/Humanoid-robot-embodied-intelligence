"""统一配置加载(支持 YAML / 环境变量覆盖)。

TODO: 等 PyYAML 依赖确认后实现加载逻辑。
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any


def load_config(name: str = "default") -> dict:
    """从 `configs/<name>.yaml` 加载配置。

    找不到时返回空 dict(便于按模块读 sub-config 时容错)。
    """
    path = Path(__file__).parent.parent / "configs" / f"{name}.yaml"
    if not path.exists():
        return {}
    # TODO: 实际用 PyYAML 加载
    return {}


def env_override(cfg: dict, prefix: str = "OLI_") -> dict:
    """用环境变量覆盖配置(支持嵌套 key:OLI_LLM__ENDPOINT 覆盖 cfg[llm][endpoint])。

    TODO: 实现嵌套 key 解析(`__` 当层级分隔符)。
    """
    return cfg
