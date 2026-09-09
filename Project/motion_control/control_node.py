"""动作执行 ROS 2 节点入口。

订阅:/oli/planning/skill_seq + /oli/perception/robot_state
发布:/oli/control/trajectory + /oli/control/joint_cmd

频率:MPC 100Hz / WBC 1kHz / 伺服 2kHz
"""
from __future__ import annotations
# from rclpy.node import Node
from common.types import SkillSequence, RobotState, Trajectory, JointCommand
from .mpc import MPCPlanner
from .wbc import WBCController
from .low_level_servo import LowLevelServo
from .skill_executor import SkillExecutor
from .feedback import FeedbackMonitor


class ControlNode:
    """动作执行 ROS 2 节点(留 TODO 继承 rclpy.node.Node)。"""

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self.mpc = MPCPlanner(urdf_path=self.config.get("urdf_path"), config=self.config.get("mpc"))
        self.wbc = WBCController(urdf_path=self.config.get("urdf_path"), config=self.config.get("wbc"))
        self.feedback = FeedbackMonitor(config=self.config.get("safety"))
        self.executor = SkillExecutor(mpc=self.mpc, config=self.config.get("executor"))
        # self.servo: 在 sim/real 切换时由 deployment 注入 SDK client
        self.servo: LowLevelServo | None = None

    def on_skill_sequence(self, seq: SkillSequence) -> None:
        """收到新技能序列时启动执行。"""
        # TODO: for skill in seq.skills: self.executor.start(skill, state)
        pass

    def tick_100hz(self, state: RobotState) -> Trajectory:
        """MPC tick:每 10ms 调一次。"""
        # TODO: return self.executor.tick(state)
        raise NotImplementedError

    def tick_1khz(self, state: RobotState, traj: Trajectory) -> JointCommand:
        """WBC tick:每 1ms 调一次。"""
        # TODO:
        # cmd = self.wbc.control(traj, state)
        # if not self.feedback.check_joint_limits(cmd):
        #     cmd = self.feedback.clamp(cmd)
        # return cmd
        raise NotImplementedError

    def tick_2khz(self, cmd: JointCommand) -> None:
        """Servo tick:每 0.5ms 下发。"""
        if self.servo:
            self.servo.step(cmd)
