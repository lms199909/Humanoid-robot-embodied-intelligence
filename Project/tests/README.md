# Project 测试

## 结构

```
tests/
├── unit/                     # 单元测试(无 ROS / 无 Isaac)
│   ├── test_types.py         # common.types
│   ├── test_skill_library.py # 技能库
│   ├── test_safety.py        # 安全监测
│   ├── test_llm_factory.py   # LLM 工厂
│   └── test_model_storage.py # 模型存储
│
├── integration/              # 模块间集成
│   ├── test_perception_pipeline.py
│   └── test_control_loop.py
│
├── sim_e2e/                  # 仿真端到端(需 Isaac Sim,默认 skip)
│   └── test_stair_env.py
│
├── safety/                   # 安全专项
│   └── test_estop.py
│
└── conftest.py               # pytest fixtures
```

## 运行

```bash
# 全部测试(默认会跳过 sim_e2e)
cd Project
pytest tests/

# 只跑单元
pytest tests/unit/

# 跑某个文件
pytest tests/unit/test_skill_library.py -v

# 包括 sim_e2e(需先装 Isaac Sim + Oli URDF)
pytest tests/sim_e2e/

# 跑安全专项
pytest tests/safety/ -v
```

## 当前覆盖

| 模块 | 覆盖 | 状态 |
|---|---|---|
| `common.types` | 100% 字段 | ✅ |
| `skill_library` | 8 个技能注册 + lookup | ✅ |
| `feedback` (L1-L5) | 阈值 + clamp 桩 | 🟡 stub |
| `llm_client` 工厂 | Remote/Local 分支 | ✅ |
| `model_storage` | Local backend + version | ✅ |
| `perception` 集成 | SceneGraphBuilder merge | 🟡 stub |
| `control` 集成 | 三层 tick | 🟡 stub |
| `stair_env` e2e | 需 Isaac Sim | ⏭️ skip |
| `estop` 响应时间 | 50ms 阈值 | ✅(stub) |

🟡 表示依赖尚未实装的 stub,跑通即转 ✅。
⏭️ 表示需要外部依赖(Isaac Sim / Oli URDF / 真机)。

## 写测试的约定

1. **单元测试不依赖 ROS 2 / Isaac Sim** — 用 mock / stub
2. **集成测试可依赖多个模块** — 但仍避开 ROS 2
3. **仿真 e2e 必须 skip if no Isaac** — 用 `@pytest.mark.skip(reason=...)`
4. **fixture 集中在 conftest.py**
5. **不要写长测试** — 一个测试只验一件事
