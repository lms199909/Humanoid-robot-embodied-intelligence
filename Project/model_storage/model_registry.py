"""模型注册表:按"模型名 + 版本"管理所有 ONNX / TorchScript。"""
from __future__ import annotations
from pathlib import Path
from .storage_backend import StorageBackend


class ModelEntry:
    def __init__(self, name: str, version: str, path: Path, metadata: dict | None = None):
        self.name = name
        self.version = version
        self.path = path
        self.metadata = metadata or {}


class ModelRegistry:
    """模型名 → ModelEntry 映射 + 版本历史。"""

    def __init__(self, storage: StorageBackend, manifest_path: str = "models/registry.json"):
        self.storage = storage
        self.manifest_path = manifest_path
        self._entries: dict[str, list[ModelEntry]] = {}
        # TODO: 启动时加载 manifest

    def register(self, name: str, version: str, model_bytes: bytes, metadata: dict | None = None) -> ModelEntry:
        """上传新模型 + 写入 manifest。"""
        # TODO: path = self.storage.put(f"{name}/{version}/model.onnx", model_bytes)
        # self._entries.setdefault(name, []).append(ModelEntry(...))
        # self._save_manifest()
        raise NotImplementedError

    def get_path(self, name: str, version: str = "latest") -> Path:
        """获取模型路径(deployment 时调用)。"""
        # TODO: self._resolve_latest(name, version) → self.storage.get(...)
        raise NotImplementedError

    def list_versions(self, name: str) -> list[str]:
        return [e.version for e in self._entries.get(name, [])]
