"""楼梯环境端到端(M2 验收用)。

需要 Isaac Sim/Isaac Lab 装好;否则 skip。
"""
from __future__ import annotations
import pytest


@pytest.mark.skip(reason="需 Isaac Sim 安装,等 Oli URDF 导入后启用")
def test_stair_env_reset_step():
    from model_training.envs import StairEnv
    env = StairEnv(task_config={"angle_deg": 30.0})
    state = env.reset()
    assert state is not None
    from common.types import JointCommand
    cmd = JointCommand(position=[0.0] * 31, velocity=[0.0] * 31, effort=[0.0] * 31)
    state, reward, done, info = env.step(cmd)
    assert isinstance(reward, float)
    assert isinstance(done, bool)


@pytest.mark.skip(reason="同上")
def test_stair_env_domain_randomization():
    from model_training.envs import StairEnv
    from model_training.mdp.events import DomainRandomization
    dr = DomainRandomization()
    sample = dr.sample()
    assert "mass" in sample
    assert 0.8 <= sample["mass"] <= 1.2
