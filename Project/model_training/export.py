"""导出 checkpoint → ONNX(给真机部署用,Readme §6 + QUESTIONS C2)。"""
from __future__ import annotations
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True, help="rsl_rl .pt checkpoint 路径")
    p.add_argument("--out", required=True, help="输出 ONNX 路径")
    p.add_argument("--opset", type=int, default=17)
    args = p.parse_args()

    # TODO:
    # 1. load .pt
    # 2. 提取 actor 网络(state_dict)
    # 3. torch.onnx.export(...)
    # 4. 用 onnxruntime 验证 forward 一次


if __name__ == "__main__":
    main()
