# LimX Oli 具身智能项目 — 代码大纲

> 依据:`Readme.md` 项目架构设计 + 借鉴 `G1DWAQ_Lab-main/` 的目录组织与接口设计思路
> 适用机器人:LimX Oli(31 DoF,逐际动力)
> 不重复造轮子:G1DWAQ_Lab-main 作为"参考实现"放在仓库里,新代码以"架构平移 + 接口重定义"为主,具体实现按 Oli 重写

---

## 1. 设计原则

| 原则 | 说明 |
|---|---|
| **架构借鉴,实现重写** | G1DWAQ_Lab-main 是宇树 G1/天工的训推代码,跟 Oli 硬件/SDK 不同,不能直接复制。具体逻辑(环境、任务、奖励)按 Oli 重新实现 |
| **算法库复用** | `rsl_rl` 是通用 RL 库,跟机器人无关,**直接复用**,不重写 |
| **4 层架构对齐 README** | 认知层 / 规划层 / 控制层 / 感知层 — 4 个目录分别对应 |
| **通信统一** | 机内 ROS 2、机外 WebSocket JSON;所有模块都跑同一个 ROS 2 graph,sim/real 同一份代码 |
| **仿真优先** | Isaac Sim 为主、MuJoCo 为辅;先 sim 跑通,再 sim2real |
| **安全前置** | 安全监测是横切关注点,每个执行类模块都嵌入安全 hook |

---

## 2. 顶层目录(在仓库根下新增)

```
Humanoid-robot-embodied-intelligence/
├── Readme.md                       # 现有:项目设计文档
├── docs/                           # 新增:架构/接口/里程碑文档
│   ├── PROJECT_OUTLINE.md          # 本文件
│   ├── interfaces.md               # 各模块接口定义(从 Readme 抽出来细化)
│   ├── milestones.md               # M0~M3 任务拆解
│   └── safety.md                   # L1~L5 安全等级细则
│
├── oli_hardware/                   # 硬件抽象层(从感知/控制中分离,跟具体硬件解耦)
│   ├── urdf/                       # Oli 官方 URDF + mesh
│   ├── sdk_python/                 # Oli SDK Python wrapper(逐际 SDK 适配层)
│   ├── ros2_nodes/                 # 关节驱动 / IMU 读取 / 力矩反馈节点
│   ├── limits/                     # 关节角度/速度/力矩限位 YAML
│   └── zero_calibration/           # 零位标定
│
├── perception/                     # 感知层(对应 Readme §3)
│   ├── rgbd_drivers/               # RealSense D435i 驱动 + 内外参
│   ├── imu_fusion/                 # IMU 滤波 + 姿态估计(ESKF/UKF)
│   ├── object_detection/           # YOLO / 6D 位姿估计
│   ├── scene_graph/                # 场景图构建
│   ├── multimodal_fusion/          # 视觉 + 力/触觉融合
│   └── ros2_msgs/                  # 自定义 msg:SceneGraph / ObjectList / RobotState
│
├── planning/                       # 规划与决策层(对应 Readme §4 §5)
│   ├── llm_client/                 # 云端 LLM/VLM REST/WebSocket 客户端
│   ├── task_decomposer/            # 任务分解器(LLM 驱动)
│   ├── skill_library/              # 技能库(SK_WALK/CLIMB/REACH/GRASP/...)
│   ├── skill_scheduler/            # 技能调度器(10Hz)
│   ├── replan/                     # 失败检测 + 重规划触发
│   └── ros2_msgs/                  # TaskGoal / SkillSequence
│
├── control/                        # 运动控制层(对应 Readme §6,机载 1kHz)
│   ├── mpc/                        # 模型预测控制(100Hz)
│   ├── wbc/                        # 全身控制(1kHz)
│   ├── low_level/                  # 关节伺服(2kHz)
│   ├── skill_executor/             # 把 skill 转成 motion primitive
│   ├── feedback/                   # 误差计算 + 失败分类(对应 Readme §7)
│   └── ros2_msgs/                  # Trajectory / JointCommand
│
├── safety/                         # 安全与降级(对应 Readme §10,横切)
│   ├── joint_limits.py             # L1 关节力矩限位
│   ├── stability_monitor.py        # L2 姿态稳定
│   ├── collision_check.py          # L3 碰撞检测
│   ├── emergency_stop.py           # L4 急停
│   ├── comm_timeout.py             # L5 通信超时
│   └── degrade/                    # 降级策略(LLM 不可用 → 预设技能模板 等)
│
├── simulation/                     # 仿真与 sim2real(对应 Readme §9)
│   ├── isaac_sim/
│   │   ├── scenes/                 # 楼梯(15/30/45°) / 工作台 USD
│   │   ├── tasks/                  # 任务 env(继承 IsaacLab)
│   │   └── ros2_bridge/            # ISAAC ↔ ROS 2 桥
│   ├── mujoco/
│   │   ├── scenes/                 # MJCF(快速 RL 训练)
│   │   └── tasks/                  # MJX env
│   ├── sim2sim/                    # Isaac → MuJoCo 一致性验证
│   └── domain_randomization/       # 域随机化参数
│
├── training/                       # 训练框架(借鉴 TienKung-Lab 的"env/算法"分离思想)
│   ├── envs/                       # 任务环境(包 isaaclab env + mujoco env)
│   ├── mdp/                        # 奖励 / 终止 / 重置 / 课程学习
│   ├── algorithms/                 # 调 rsl_rl(PPO/AMP/DWAQ)
│   ├── policies/                   # 训好的模型(ONNX 导出)
│   ├── scripts/
│   │   ├── train.py                # 入口
│   │   ├── play.py                 # 回放评估
│   │   ├── sim2sim.py              # 跨仿真器一致性
│   │   └── export_onnx.py          # 导出给真机
│   └── configs/                    # 超参 YAML
│
├── deployment/                     # 真机部署(借鉴 LeggedLabDeploy 的"config + deploy"模式)
│   ├── onnx_runner/                # ONNX 运行时(不动 rsl_rl,只调推理)
│   ├── ros2_nodes/
│   │   ├── state_publisher.py      # 把 Oli 状态发到 ROS 2
│   │   ├── cmd_subscriber.py       # 接收策略输出
│   │   └── safety_node.py          # 部署时的安全监测
│   ├── configs/                    # 部署参数(控制频率、限位、…)
│   └── common/                     # 遥控手柄 / 命令助手 / 坐标系辅助
│
├── communication/                  # 通信与中间件(对应 Readme §8)
│   ├── ros2_msgs/                  # 自定义 msg/srv 集中放
│   ├── websocket_bridge/           # ROS 2 ↔ WebSocket JSON(机载 ↔ 服务器)
│   └── external_api/               # LLM/VLM REST 客户端
│
├── utils/                          # 通用工具
│   ├── logging/
│   ├── config_loader/
│   ├── math/                       # 旋转 / 插值 / 滤波
│   └── viz/                        # RViz 插件 / PlotJuggler 配置
│
├── tests/
│   ├── unit/                       # 各模块单测
│   ├── integration/                # ROS 2 节点间
│   ├── sim_e2e/                    # 仿真端到端(M1/M2/M3 验收)
│   └── safety/                     # 急停 / 限位 / 通信超时
│
├── scripts/                        # 运维入口
│   ├── start_sim.sh
│   ├── start_robot.sh
│   └── deploy_to_oli.sh
│
├── G1DWAQ_Lab-main/                # 保留作为参考实现,不改
└── LimX Oli 折页.pdf
```

---

## 3. 与 G1DWAQ_Lab-main 的对应关系

| 新代码模块 | G1DWAQ_Lab-main 对应 | 借鉴方式 | 说明 |
|---|---|---|---|
| `training/envs/` | `TienKung-Lab/legged_lab/envs/` | **架构平移,实现重写** | env/任务基类注册方式、`g1_env.py` 的类结构可参考,但 Oli 关节/URDF 完全不同,得新写 |
| `training/mdp/` | `TienKung-Lab/legged_lab/mdp/` | **接口平移** | `events.py` / `rewards.py` / `curriculum.py` 的接口签名值得参考 |
| `training/algorithms/` | `TienKung-Lab/rsl_rl/` | **直接复用** | rsl_rl 是通用 RL 库,装为 pip 依赖即可,不改源码 |
| `training/scripts/` | `TienKung-Lab/scripts/` | **入口脚本参考** | `train.py` / `play.py` / `export_onnx.py` 的参数解析、模型加载流程可参考 |
| `simulation/isaac_sim/` | `TienKung-Lab/legged_lab/assets/` | **资产重写** | Oli URDF + 自建楼梯/工作台 USD,不直接用 G1/TienKung mesh |
| `deployment/onnx_runner/` | `LeggedLabDeploy/deploy.py` | **流程参考** | deploy 入口、`policy/g1/exported/policy.onnx` 的加载流程、`config_dwaq.py` 的 ROS 节点骨架 |
| `deployment/ros2_nodes/` | `LeggedLabDeploy/config.py` | **节点骨架参考** | config.py 是一个 ROS 节点 + 关节映射表,Oli 版本结构相同但关节名映射要重写 |
| `deployment/common/` | `LeggedLabDeploy/common/` | **少量复用** | `remote_controller.py`(手柄输入)、`command_helper.py` 是通用辅助,基本可平移 |
| `oli_hardware/sdk_python/` | `unitree_sdk2_python/` | **模式参考,具体重写** | SDK 包的目录结构(IDL 消息、core、rpc、example)可平移,但 Oli 是逐际 SDK,API 完全不同 |
| `perception/` | `TienKung-Lab/legged_lab/sensors/` | **接口参考** | `camera.py` / `tiled_camera.py` 的 sensor 抽象可参考,Oli 用 RealSense 不是 Isaac 内置 camera |
| `safety/` | (G1DWAQ_Lab-main 中没有) | **新增** | 整个安全层是 Oli 项目独有的,Readme 明确要求 L1~L5 |

**核心不抄的边界**:
- 任何 G1/TienKung/TienKung-Lite 的专属 URDF、mesh、关节映射 — 全部 Oli 重写
- 任何跟具体硬件绑定的 SDK API(宇树 DDS、宇树 RPC)— 用 Oli SDK 替换
- 训练超参、奖励权重 — 按 Oli 的动力学重新调

---

## 4. 里程碑与代码落地顺序(对齐 Readme §11)

| M | 周期 | 关键代码落地 |
|---|---|---|
| **M0 启动** | Week 1-2 | 仓库骨架(`docs/` + 空目录占位)、`oli_hardware/sdk_python` 适配层、URDF 导入验证、ROS 2 基础 topic 跑通 |
| **M1 仿真基础** | Week 3-4 | `simulation/isaac_sim/` 楼梯 + 工作台场景、`perception/` 视觉/IMU ROS 节点、`control/wbc` + `skill_library/SK_WALK/SK_STAND`、`tests/sim_e2e` 基础场景 |
| **M2 楼梯搬运** | Week 5-6 | `planning/task_decomposer`(LLM 路径) + `planning/skill_library/SK_CLIMB`、`training/` 跑通 PPO 训步态、`deployment/sim2sim` 一致性 |
| **M3 装配集成** | Week 7-8 | `skill_library/SK_REACH/SK_GRASP/SK_PLACE/SK_ASSEMBLE`、`safety/` 全套、`deployment/onnx_runner` 跑通真机联调(可选,如硬件到位)|

---

## 5. 待你确认的关键决策(影响大纲微调)

| # | 决策项 | 当前假设 |
|---|---|---|
| 1 | 训练代码要不要做? | **要做**(M2 需要 PPO 训步态) |
| 2 | LLM/VLM 客户端现在做还是 M3 再说? | M0 先做空接口,真接入放到 M2/M3 |
| 3 | ROS 2 版本? | 假设 **Humble**(Readme 没指定,Humble 是目前主流 LTS) |
| 4 | Isaac Sim 还是 Isaac Lab? | 假设 **Isaac Lab**(它是 Isaac Sim 内的 RL 框架,跟 rsl_rl 配合最好) |
| 5 | 仓库里 G1DWAQ_Lab-main/ 继续保留作参考,还是之后拆出去? | 假设 **保留**(短期翻阅参考价值大) |
| 6 | ONNX 推理用什么后端? | 假设 **onnxruntime**(跨平台,Mavis 实测最稳) |
| 7 | 关节限位等硬件参数从哪里来? | 等 Oli 官方 SDK 拿到后填进 `oli_hardware/limits/` |