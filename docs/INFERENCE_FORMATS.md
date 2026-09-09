# 模型推理格式详解(C2 决策参考资料)

> 决策位置:`Project/QUESTIONS.md` C2
> 当前默认:ONNX + onnxruntime
> 本文档帮你理解每个选项,再下决定

---

## 1. 什么是"推理格式"

训练时(用 PyTorch / rsl_rl / 自实现 PPO)模型是 **PyTorch `.pt` 权重 + Python 类结构**。
部署时(机载 1kHz 控制回路)我们要把训练好的模型放到真机或仿真器里跑 forward 推理。
**推理格式** 就是把 PyTorch 模型"序列化 + 固化为可移植产物"的方式。

部署时关心这些:
- **跨平台**:能不能在 RK3588(ARM)/ x86 PC / Jetson 上跑?
- **后端依赖**:需不需要装 PyTorch / CUDA?越小越好(机载 32GB RAM 紧张)
- **性能**:推理延迟多少毫秒?支不支持 fp16 / int8 量化?
- **回退路径**:训练版本升级了,老模型还能不能加载?
- **可调试性**:能不能用 Python 跟真机一起跑 sanity check?

---

## 2. 主流格式对比

| 格式 | 体积 | 后端依赖 | 跨平台 | 性能 | 调试 | 适合场景 |
|---|---|---|---|---|---|---|
| **PyTorch `.pt`** | 大(含图) | 整个 PyTorch + Python | ❌ 仅 Python | 中 | ✅ 强 | 训练 / 仿真回放 |
| **TorchScript `.pt`** | 中 | libtorch(C++/Python) | ✅ 强 | 中 | 中 | C++ 部署、PyTorch 生态内 |
| **ONNX** | 小 | onnxruntime 6 MB 左右,或专用 runtime | ✅ **强** | 高(可走 TensorRT/OpenVINO) | 中 | **跨平台部署首选** |
| **TensorRT** | 极小 | 仅 NVIDIA GPU + TensorRT | ❌ NVIDIA 专属 | **最高**(fp16/int8) | 弱 | 边缘 GPU(Jetson)|
| **OpenVINO** | 小 | Intel OpenVINO | ❌ Intel/部分 ARM | 高(int8) | 中 | Intel CPU/边缘 |
| **CoreML** | 小 | Apple CoreML | ❌ Apple 专属 | 高 | 弱 | 仅 macOS/iOS |

---

## 3. 推荐组合(分层)

| 部署目标 | 推荐格式 | 推理后端 | 备注 |
|---|---|---|---|
| **机载 RK3588**(Readme §2.2 感知芯片) | **ONNX** | onnxruntime CPU EP | 跨平台,无 CUDA 依赖 |
| **训练回放 / 仿真 sanity** | PyTorch `.pt` | PyTorch | 留 `.pt` 便于训练↔部署 diff |
| **未来若上 Jetson Orin 边缘 GPU** | ONNX → TensorRT | TensorRT | 性能翻 3-5x,但需 NVIDIA |

**为什么不直接上 TensorRT**:
- Oli 的运控芯片是 RK3588(ARM SoC,**没有 NVIDIA GPU**)
- TensorRT 必须 NVIDIA GPU,装了也跑不了
- ONNX 是中性选择,以后上 Jetson 再一键转 TensorRT

**为什么不用 TorchScript**:
- TorchScript 在 PyTorch 2.x 后维护力度下降,新算子支持慢
- 跟 onnxruntime 比,生态稍弱(onnxruntime 跨厂商支持更广)
- 但**如果**机载控制代码是 C++,TorchScript(libtorch)是个备选

**为什么不用 PyTorch `.pt` 直跑**:
- PyTorch 推理包太大(~500MB+),机载 32GB 感知芯片紧张
- 启动慢,延迟不稳定
- 依赖 Python 解释器,机载 C++ 控制代码不方便调

---

## 4. ONNX 生态圈(选定后要装什么)

```
训练(Python/PyTorch)                    部署(机载/任意平台)
        │                                       │
   torch.onnx.export()                  ┌──────┴──────┐
        │                               │             │
      .onnx                       onnxruntime    TensorRT(可选)
        │                          (CPU/GPU)       (NVIDIA)
        │                               │
        └──── 同一份 .onnx ─────────────┘
```

关键依赖:
- 训练端:`torch`(已有)+ `onnx`(导出)+ 可选 `onnxsim`(图优化)
- 部署端:`onnxruntime`(CPU EP 约 6 MB,GPU EP 约 200 MB)
- 可选:`onnx2torch`(反向:把 ONNX 转回 PyTorch 做 debug)

---

## 5. 实施流程(我们 Project 里要做什么)

1. **训练**:`Project/model_training/train.py` 训出 PyTorch checkpoint
2. **导出**:`Project/model_training/export.py` 用 `torch.onnx.export` 转 ONNX
   - opset 17(支持大部分 PyTorch 2.x 算子)
   - 输入 shape 写死(例如 obs=33 维)
   - 验证:`onnxruntime` 加载 + 跟 PyTorch 输出对比差异 < 1e-5
3. **存储**:`Project/model_storage/model_registry.py` 把 .onnx 入库,manifest 记录 input/output shape
4. **部署**:`Project/deployment/onnx_runner/`(待 M3 落地)用 `onnxruntime.InferenceSession` 加载

---

## 6. 你需要拍板的

| 决策 | 当前默认 | 备选 | 影响 |
|---|---|---|---|
| **主格式** | ONNX | TorchScript / PyTorch .pt 直跑 | 跨平台 + 小体积 |
| **后端** | onnxruntime(CPU EP) | TensorRT(需 NVIDIA) | 机载 RK3588 没 GPU,只能 CPU |
| **量化** | 暂不(fp32) | 训完做 PTQ → int8 | 性能换精度,M3 视情上 |
| **训练侧副产物** | 同时存 .pt(留底) | 只存 .onnx | 多 ~几十 MB,便于回放 debug |

**建议**:先按当前默认走(ONNX + onnxruntime CPU),等 M3 真机联调时如果延迟不够再讨论量化 / 换后端。

---

## 7. 常见坑

1. **动态 shape**:ONNX 默认要固定输入 shape,变长输入要显式声明 `dynamic_axes`
2. **算子不支持**:某些 PyTorch 算子(尤其 attention/flash)ONNX 不支持,导出时要替换
3. **fp16/int8 精度损失**:量化后 reward 网络可能掉 0.1-1% 精度,要验证
4. **ONNX 校验**:导出后必须 `onnxruntime` 跑一次,跟 PyTorch 输出 diff,否则容易 silent 错

---

## 8. 相关项目(参考 G1DWAQ_Lab-main)

`LeggedLabDeploy/policy/g1/exported/policy.onnx` 已经是 ONNX 格式 + `policy.pt` 双留底,跟我们计划一致。
`TienKung-Lab/legged_lab/scripts/export_dwaq_policy.py` 有完整的 .pt → .onnx 导出脚本(我们的 `export.py` 借鉴这个)。
