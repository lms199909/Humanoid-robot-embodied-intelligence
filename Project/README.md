# Project 代码框架

> 项目代码主目录。对齐 `Readme.md` 设计,具体实现按模块分布。
> 本目录由骨架脚本生成,所有 `.py` 仅有接口签名 + `pass`/`TODO` 占位,**不可直接运行**。

## 1. 目录结构(7 大功能模块 + common + configs)

```
Project/
├── README.md                          # 本文件
├── QUESTIONS.md                       # 项目内问题清单(决策待你确认)
│
├── environment_perception/            # 环境感知(视觉/RGB-D/场景)
├── proprioception/                    # 本体感知(IMU/关节/力矩/状态估计)
├── task_planning/                     # 任务理解规划(LLM/任务分解/技能库)
├── motion_control/                    # 动作执行(MPC/WBC/伺服/反馈)
├── simulation/                        # 仿真调用(Isaac Sim + MuJoCo)
│   ├── isaac_sim/
│   └── mujoco/
├── model_storage/                     # 模型存储(注册表/版本/后端)
├── model_training/                    # 模型训练(env/算法/训练/导出)
│   ├── envs/
│   ├── algorithms/
│   └── configs/
│
├── common/                            # 通用基础(数据类型/配置/日志)
└── configs/                           # 全局配置
```

## 2. 每个模块的"角色"

| 模块 | 角色 | 频率 | ROS 2 入口 |
|---|---|---|---|
| `environment_perception` | 把 RGB-D → 场景图/物体位姿 | 30 Hz | `perception_node.py` |
| `proprioception` | IMU + 关节 → 全身状态(33 维) | 1 kHz | `proprioception_node.py` |
| `task_planning` | LLM → 任务分解 → 技能序列 | 1-10 Hz | `planning_node.py` |
| `motion_control` | 技能 → 轨迹 → 关节指令 | 100-1000 Hz | `control_node.py` |
| `simulation` | 统一 sim 接口,跟 real 共享 control/perception | — | — |
| `model_storage` | ONNX/TorchScript 模型注册与版本管理 | — | — |
| `model_training` | 训/评/导出(借鉴 TienKung-Lab 的 env/算法分离) | — | — |

## 3. 数据流

```
[Real/Sim 传感器] → environment_perception + proprioception
                  → common/types (SceneGraph, RobotState)
                  → task_planning (LLM 慢思考)
                  → motion_control (MPC/WBC 快系统)
                  → 关节指令
                  → 反馈 → proprioception (闭环)
```

## 4. 跟 Readme / G1DWAQ_Lab-main 的关系

- 跟 Readme 4 层架构一一对应:认知(task_planning)/规划+控制(motion_control)/执行(motion_control.low_level_servo)/感知(env+proprio)
- 跟 G1DWAQ_Lab-main 的对应详见 `docs/PROJECT_OUTLINE.md` §3
- `model_training/algorithms/` 调 `rsl_rl` 作为依赖,直接复用

## 5. 接下来要做的事

1. 看 `QUESTIONS.md` 把决策点过一遍,告诉我哪些调整
2. 按 M0 优先级落地 `proprioception` + `environment_perception`(机载先跑通)
3. 仿真场景先在 `simulation/isaac_sim/scene_loader.py` 留接口,M1 再填
