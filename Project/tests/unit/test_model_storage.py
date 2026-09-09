"""model_storage 单元测试。"""
from __future__ import annotations
from model_storage.storage_backend import LocalStorageBackend
from model_storage.version_manager import VersionManager, VersionMetadata


def test_local_storage_put_get(tmp_models_dir):
    be = LocalStorageBackend(root=str(tmp_models_dir))
    p = be.put("ppo/v0.1.0/model.onnx", b"fake-onnx-bytes")
    assert p.exists()
    assert be.get("ppo/v0.1.0/model.onnx") == b"fake-onnx-bytes"
    assert be.exists("ppo/v0.1.0/model.onnx")


def test_local_storage_nested_keys(tmp_models_dir):
    be = LocalStorageBackend(root=str(tmp_models_dir))
    be.put("a/b/c/file.bin", b"x")
    assert be.exists("a/b/c/file.bin")


def test_version_metadata_now_isoformat():
    md = VersionMetadata.now()
    # ISO 8601 格式以 Z 结尾
    assert md.endswith("Z")
    assert "T" in md


def test_version_manager_init():
    vm = VersionManager(initial="0.0.0")
    md = vm.stamp()
    assert md.semver == "0.0.0"
