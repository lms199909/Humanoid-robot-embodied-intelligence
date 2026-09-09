"""pytest 共用 fixtures / 配置。"""
from __future__ import annotations
import pytest
import sys
from pathlib import Path

# 把 Project/ 根加入 sys.path,便于 `from common.types import ...` 这种绝对导入
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def default_config() -> dict:
    """加载 Project/configs/default.yaml。"""
    import yaml
    cfg_path = PROJECT_ROOT / "configs" / "default.yaml"
    return yaml.safe_load(cfg_path.read_text(encoding="utf-8"))


@pytest.fixture
def tmp_models_dir(tmp_path) -> Path:
    """model_storage 测试用临时目录。"""
    d = tmp_path / "models"
    d.mkdir()
    return d


@pytest.fixture
def mock_robot_state():
    """构造一个简单的 RobotState,供测试用。"""
    from common.types import JointState, IMUState, RobotState
    return RobotState(
        joint=JointState(
            name=[f"j{i}" for i in range(31)],
            position=[0.0] * 31,
            velocity=[0.0] * 31,
            effort=[0.0] * 31,
            timestamp_ns=0,
        ),
        imu=IMUState(),
        base_pose=(0, 0, 1.0, 0, 0, 0, 1),
        timestamp_ns=0,
    )
