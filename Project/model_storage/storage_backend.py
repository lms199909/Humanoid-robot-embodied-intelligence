"""存储后端抽象 + 本地 / S3 实现。"""
from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path


class StorageBackend(ABC):
    @abstractmethod
    def put(self, key: str, data: bytes) -> Path: ...

    @abstractmethod
    def get(self, key: str) -> bytes: ...

    @abstractmethod
    def exists(self, key: str) -> bool: ...


class LocalStorageBackend(StorageBackend):
    """本地文件系统后端(默认,Readme QUESTIONS C3)。"""

    def __init__(self, root: str = "models/"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, key: str, data: bytes) -> Path:
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def get(self, key: str) -> bytes:
        return (self.root / key).read_bytes()

    def exists(self, key: str) -> bool:
        return (self.root / key).exists()


class S3StorageBackend(StorageBackend):
    """S3 / MinIO 后端(留 TODO,生产环境用)。"""

    def __init__(self, bucket: str = "", endpoint: str = "", access_key: str = "", secret_key: str = ""):
        # TODO: 初始化 boto3 client
        self.bucket = bucket

    def put(self, key: str, data: bytes) -> Path:
        # TODO
        raise NotImplementedError

    def get(self, key: str) -> bytes:
        raise NotImplementedError

    def exists(self, key: str) -> bool:
        raise NotImplementedError
