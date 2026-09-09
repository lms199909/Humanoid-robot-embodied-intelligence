"""Project 测试套件。

结构:
  tests/
  ├── unit/                    单元测试(各模块独立)
  ├── integration/             集成测试(模块间)
  ├── sim_e2e/                 仿真端到端(对应 M1/M2/M3 验收)
  └── safety/                  安全急停 / 限位 / 通信超时

约定:
  - pytest 框架(G 默认)
  - 单元测试不依赖 ROS 2 / Isaac Sim
  - 集成测试用 mock 或最小 stub
  - 仿真端到端需要 Isaac Sim 安装
"""
