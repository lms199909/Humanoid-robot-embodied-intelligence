"""版本管理:语义版本 + 训练元数据(指标 / 数据集 / commit SHA)。"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class VersionMetadata:
    semver: str = "0.0.1"             # e.g. 0.1.0
    trained_at: str = ""              # ISO-8601
    train_dataset: str = ""           # 数据集 hash / 路径
    metrics: dict = field(default_factory=dict)   # {"success_rate": 0.82, "ep_len": 480}
    git_commit: str = ""              # 训练时仓库 commit
    notes: str = ""

    @staticmethod
    def now() -> str:
        return datetime.utcnow().isoformat() + "Z"


class VersionManager:
    """每个训练 run 自动 bump 版本号 + 写 metadata。"""

    def __init__(self, initial: str = "0.0.0"):
        self._current = initial

    def next(self) -> str:
        """下一个版本号(简单 semver patch bump)。"""
        # TODO: 解析 → +1 patch
        # 真正发版用 full semver
        raise NotImplementedError

    def stamp(self) -> VersionMetadata:
        """生成当前版本的元数据快照。"""
        return VersionMetadata(semver=self._current, trained_at=VersionMetadata.now())
