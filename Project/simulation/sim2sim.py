"""Sim2Sim 验证:在 Isaac 和 MuJoCo 间跑同一段策略,验证一致性(Readme §9.3)。"""
from __future__ import annotations


class Sim2SimValidator:
    """对比 Isaac vs MuJoCo 在相同 SkillSequence 下的状态轨迹。"""

    def __init__(self, isaac_runner, mujoco_runner):
        self.isaac = isaac_runner
        self.mujoco = mujoco_runner

    def run(self, skill_seq) -> dict:
        """跑同一条技能序列,返回两个 sim 的状态差。"""
        # TODO:
        # i_state = self.isaac.reset()
        # m_state = self.mujoco.reset()
        # diff_log = []
        # for skill in skill_seq.skills:
        #     while not done:
        #         i_state = self.isaac.step(cmd)
        #         m_state = self.mujoco.step(cmd)
        #         diff_log.append(compute_diff(i_state, m_state))
        # return {"max_diff": max(d), "trajectory": diff_log}
        raise NotImplementedError
