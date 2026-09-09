"""OLI DWAQ task configuration."""

from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass
from isaaclab.envs.mdp import events as isaaclab_events

import legged_lab.mdp as mdp
from legged_lab.assets.HU_D04_description.oli import (
    OLI_31DOF_CFG,
    OLI_ANKLE_ROLL_TO_SOLE_Z,
    OLI_BASE_BODY,
    OLI_FEET_BODY_NAMES,
    OLI_UPPER_BODY,
    OLI_WAIST_JOINTS,
)
from legged_lab.envs.g1.g1_dwaq_config import G1DwaqAgentCfg, G1DwaqEnvCfg, G1DwaqRewardCfg
from legged_lab.terrains import ROUGH_TERRAINS_CFG


@configclass
class OliDwaqRewardCfg(G1DwaqRewardCfg):
    undesired_contacts = RewTerm(
        func=mdp.undesired_contacts,
        weight=-1.0,
        params={
            "sensor_cfg": SceneEntityCfg("contact_sensor", body_names="(?!.*ankle.*|.*contact_foot.*).*"),
            "threshold": 1.0,
        },
    )
    body_orientation_l2 = RewTerm(
        func=mdp.body_orientation_l2,
        params={"asset_cfg": SceneEntityCfg("robot", body_names=OLI_BASE_BODY)},
        weight=-2.0,
    )
    upper_body_orientation_l2 = RewTerm(
        func=mdp.body_orientation_l2,
        params={"asset_cfg": SceneEntityCfg("robot", body_names=OLI_UPPER_BODY)},
        weight=-0.5,
    )
    waist_deviation = RewTerm(
        func=mdp.joint_deviation_l1_always,
        weight=-0.2,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=OLI_WAIST_JOINTS)},
    )
    joint_deviation_arms = RewTerm(
        func=mdp.joint_deviation_l1_always,
        weight=-0.2,
        params={
            "asset_cfg": SceneEntityCfg(
                "robot",
                joint_names=[
                    ".*_shoulder_roll.*",
                    ".*_shoulder_yaw.*",
                    ".*_shoulder_pitch.*",
                    ".*_elbow.*",
                    ".*_wrist.*",
                    "head_.*",
                ],
            )
        },
    )
    feet_swing_height = RewTerm(
        func=mdp.feet_swing_height,
        weight=-0.2,
        params={
            "sensor_cfg": SceneEntityCfg("contact_sensor", body_names=".*ankle_roll.*"),
            "asset_cfg": SceneEntityCfg("robot", body_names=".*ankle_roll.*"),
            "target_height": 0.08 + OLI_ANKLE_ROLL_TO_SOLE_Z,
        },
    )


@configclass
class OliDwaqEnvCfg(G1DwaqEnvCfg):
    reward = OliDwaqRewardCfg()

    def __post_init__(self):
        super().__post_init__()

        self.scene.height_scanner.prim_body_name = OLI_BASE_BODY
        self.scene.robot = OLI_31DOF_CFG
        self.scene.terrain_type = "generator"
        self.scene.terrain_generator = ROUGH_TERRAINS_CFG

        self.robot.terminate_contacts_body_names = [OLI_BASE_BODY]
        self.robot.feet_body_names = OLI_FEET_BODY_NAMES
        self.domain_rand.events.add_base_mass.params["asset_cfg"].body_names = [OLI_BASE_BODY]

        self.scene.height_scanner.enable_height_scan = True
        self.scene.height_scanner.critic_only = True

        self.scene.privileged_info.enable_feet_info = True
        self.scene.privileged_info.enable_feet_contact_force = True
        self.scene.privileged_info.enable_root_height = True

        self.robot.dwaq_obs_history_length = 5
        self.robot.actor_obs_history_length = 1
        self.robot.critic_obs_history_length = 1

        self.robot.gait_phase.enable = True
        self.robot.gait_phase.period = 0.8
        self.robot.gait_phase.offset = 0.5

        self.domain_rand.events.randomize_actuator_gains = EventTerm(
            func=isaaclab_events.randomize_actuator_gains,
            mode="startup",
            params={
                "asset_cfg": SceneEntityCfg("robot", joint_names=".*"),
                "stiffness_distribution_params": (0.8, 1.2),
                "damping_distribution_params": (0.8, 1.2),
                "operation": "scale",
                "distribution": "uniform",
            },
        )


@configclass
class OliDwaqAgentCfg(G1DwaqAgentCfg):
    experiment_name: str = "oli_dwaq"
    wandb_project: str = "oli_dwaq"

    def __post_init__(self):
        super().__post_init__()
        self.run_name = "oli_dwaq"
