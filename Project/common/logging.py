"""统一日志(结构化 JSON 输出,后续可加 trace_id / skill_id 等字段)。"""
from __future__ import annotations
import logging
import sys


def setup_logger(name: str = "oli", level: str = "INFO") -> logging.Logger:
    log = logging.getLogger(name)
    if not log.handlers:
        h = logging.StreamHandler(sys.stdout)
        # TODO: 替换为 JSON formatter
        h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s | %(message)s"))
        log.addHandler(h)
    log.setLevel(getattr(logging, level.upper(), logging.INFO))
    return log
