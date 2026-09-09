"""motion_control — 动作执行层(Readme §6-7)。

控制频率分级:
  技能调度 10Hz  →  mpc.py(MPC,100Hz)  →  wbc.py(WBC,1kHz)  →  low_level_servo(2kHz)

反馈闭环:feedback.py(失败检测 + 误差计算)
"""
from .mpc import MPCPlanner
from .wbc import WBCController
from .low_level_servo import LowLevelServo
from .skill_executor import SkillExecutor
from .feedback import FeedbackMonitor
from .control_node import ControlNode

__all__ = [
    "MPCPlanner", "WBCController", "LowLevelServo",
    "SkillExecutor", "FeedbackMonitor", "ControlNode",
]
