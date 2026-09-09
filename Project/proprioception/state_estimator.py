"""全身状态估计:IMU + 关节 → 33 维状态向量(Readme §3.2)。"""
from __future__ import annotations
from common.types import IMUState, JointState, RobotState


class StateEstimator:
    """融合 IMU(高频姿态) + 关节编码器(运动学) → RobotState。

    典型实现:
        - 基础位置:关节正运动学(base 在世界系下的位姿)
        - 基础姿态:IMU 主导(关节受形变影响)
        - 基础速度:关节微分 + IMU 积分
    """

    def __init__(self, urdf_path: str = "", config: dict | None = None):
        self.urdf_path = urdf_path
        self.config = config or {}
        # TODO: 加载 URDF(用 pinocchio / yourdfpy),建运动学模型

    def estimate(
        self,
        imu: IMUState,
        joint: JointState,
        timestamp_ns: int = 0,
    ) -> RobotState:
        """单次状态估计。"""
        # TODO: forward_kinematics + IMU 融合
        raise NotImplementedError

    def reset(self) -> None:
        """重置估计器状态(切换 skill / 摔倒恢复时)。"""
        # TODO: 清零积分器
        pass
