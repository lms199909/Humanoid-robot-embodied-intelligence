"""训练入口脚本。

用法示例(M2 楼梯训练):
    python -m model_training.train --task stair --algo ppo --max_iter 1000

参考:TienKung-Lab/scripts/train.py
"""
from __future__ import annotations
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True, choices=["stair", "industrial"])
    p.add_argument("--algo", default="ppo", choices=["ppo", "dwaq"])
    p.add_argument("--max_iter", type=int, default=1000)
    p.add_argument("--config", default="model_training/configs/stair_ppo.yaml")
    p.add_argument("--out_dir", default="models/")
    args = p.parse_args()

    # TODO:
    # 1. 加载 config
    # 2. 构造 env(StairEnv / IndustrialEnv)
    # 3. 构造 trainer(PPOTrainer / DWAQTrainer)
    # 4. trainer.train(max_iterations=args.max_iter)
    # 5. export 到 models/


if __name__ == "__main__":
    main()
