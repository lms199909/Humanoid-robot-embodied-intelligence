# Project 问题清单(决策记录)

> 本文件记录已确定的决策 + 仍待确认项。
> 每条决策的当前位置都标了 ✅ 已定 / 🟡 部分定 / ⏳ 待定。

---

## A. 语言/版本(影响所有 .py imports)

| # | 问题 | 决策 | 状态 |
|---|---|---|---|
| A1 | 主语言 | **Python 3.10+** | ✅ 已定(2026-09-09) |
| A2 | ROS 2 版本 | **Humble**(LTS) | ✅ |
| A3 | ROS 2 Python 客户端 | **rclpy** | ✅ |
| A4 | 数值库 | **numpy + torch** | ✅ |

> "A 类问题暂时先如此设定,如果后续项目进程中有调整随时沟通"

## B. 仿真平台(影响 simulation/ 全部)

| # | 问题 | 决策 | 状态 |
|---|---|---|---|
| B1 | 首选仿真 | **Isaac Sim + Isaac Lab**(与 G1DWAQ_Lab-main 一致) | ✅ |
| B2 | 物理引擎 | PhysX(Isaac) | ✅ |
| B3 | 训练用 sim | Isaac Lab(主);MuJoCo 留为可选备用 | ✅ |
| B4 | 验证用 sim | Isaac Sim(高保真) | ✅ |

> "B 问题仿真平台采用跟 G1DWAQ_Lab-main 中的仿真平台及相关配置保持一致"
> 详细:C2 推理格式说明 / 仿真目录 `simulation/isaac_sim/` 是主路径,`simulation/mujoco/` 留作可选。

## C. 模型/训练(影响 model_*)

| # | 问题 | 决策 | 状态 |
|---|---|---|---|
| C1 | RL 库 | **同时保留 rsl_rl + 自实现 PPO 接口** | ✅ |
| C2 | 推理格式 | **ONNX + onnxruntime** | ✅ |
| C3 | 模型存储后端 | 本地文件系统(`models/`) | ✅ 默认 |
| C4 | 模型版本管理 | 文件名 + JSON manifest | ✅ 默认 |
| C5 | 其他 RL 算法 | 暂留接口(AMP/SAC/TD3 等可扩展) | ✅ |

> C2 详细对比见 `docs/INFERENCE_FORMATS.md`(5.5 KB,8 节)。
> C1 实现: `model_training/algorithms/` 下 `PPOTrainer` 通过 `impl="rsl_rl" | "native"` 切换。

## D. LLM 接入(影响 task_planning/llm_client.py)

| # | 问题 | 决策 | 状态 |
|---|---|---|---|
| D1 | LLM 调用方式 | **同时保留云端(remote) + 本地(local)双接口** | ✅ |
| D2 | 端点来源 | 未知,先预留接口(configs 中可配置) | ✅ |
| D3 | VLM 是否走同一接口 | **否,单独接口**(独立 endpoint) | ✅ |
| D4 | 超时/重试 | 2s 超时,失败降级到预设技能模板 | ✅ 默认 |

> D1 实现:`BaseLLMClient` 抽象 + `RemoteLLMClient`(HTTP REST,OpenAI-compatible)
> + `LocalLLMClient`(本地推理,vLLM/TGI/llama.cpp server OpenAI-compatible 协议)
> 工厂:`make_llm_client(config)` 按 `config["llm"]["mode"]` 选实现。

## E. 通信(影响 configs/ros2_topics.yaml)

| # | 问题 | 决策 | 状态 |
|---|---|---|---|
| E1 | 机内通信 | ROS 2 Humble + DDS | ✅ 默认 |
| E2 | 机外(LLM)通信 | WebSocket JSON | ✅ 默认 |
| E3 | QoS 默认 | Sensor: BEST_EFFORT, Control: RELIABLE | ✅ 默认 |

> "E 所有问题暂时先采用默认,后续有问题再调整"

## F. 安全(影响 motion_control 内部 hook)

| # | 问题 | 决策 | 状态 |
|---|---|---|---|
| F1 | 安全等级 | L1~L5 全部纳入 | ✅ 默认 |
| F2 | 急停响应时间 | ≤ 50ms | ✅ 默认 |
| F3 | 降级策略 | LLM 不可用 → 预设技能模板 | ✅ 默认 |

## G. 命名/代码风格

| # | 问题 | 决策 | 状态 |
|---|---|---|---|
| G1 | joint 命名 | 沿用 Oli URDF 的 joint 名(待 URDF 导入后确定) | ⏳ 等 Oli URDF |
| G2 | 配置文件格式 | YAML | ✅ 默认 |
| G3 | 日志 | stdlib `logging` + JSON formatter | ✅ 默认 |
| G4 | 测试框架 | **pytest** | ✅ 默认 |

## H. 优先级/范围

| # | 问题 | 决策 | 状态 |
|---|---|---|---|
| H1 | 训练代码范围 | 包含训 PPO 步态(M2) | ✅ 默认 |
| H2 | 仿真范围 | Isaac Sim 为主(与 G1 一致);MuJoCo 留可选 | ✅ |
| H3 | 真机部署 | M3 末做(取决于硬件到位) | ✅ 默认 |
| H4 | 时间盒 | 2 个月,4 milestone(Readme §11) | ✅ 默认 |

## I. 测试(新增,你刚说的)

| # | 问题 | 决策 | 状态 |
|---|---|---|---|
| I1 | 测试目录 | **`Project/tests/`**(已建) | ✅ |
| I2 | 框架 | pytest | ✅ |
| I3 | 覆盖 | unit + integration + sim_e2e + safety 四类 | ✅ |

> `Project/tests/` 下已建 8 个测试文件,覆盖 common.types / skill_library / feedback / llm 工厂 / model_storage / 集成 / 仿真 e2e / 急停。
> 跑法:见 `Project/tests/README.md`。

---

## 仍待确认 ⏳

1. **G1 joint 命名** — 等 Oli 官方 URDF 拿到后填进 `oli_hardware/urdf/`
2. **D2 端点来源** — 等你确定 LLM 走云端哪家 / 本地哪个模型后填 `configs/default.yaml`
3. **C1/C2 落地优先级** — rsl_rl 优先上,自实现 PPO 等 M2 训不稳时再补;ONNX 推理等真机联调时再压测

---

**怎么用这个清单**:
- 每条决策的当前位置标了状态(✅ / 🟡 / ⏳)
- 详细说明对应 `docs/INFERENCE_FORMATS.md`(C2)
- 改任何一条告诉我即可,我会同步更新代码 + 配置
