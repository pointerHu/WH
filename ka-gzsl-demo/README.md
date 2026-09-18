# KA-GZSL 原始视频论文展示系统

独立于 `pointerHu/KA-GZSL` 的新项目。所有新增源代码、部署脚本和说明均位于 **WH/ka-gzsl-demo**。本项目不修改原论文仓库。

## 目标与边界

浏览器选择/拖入含音轨的视频 → 中间帧与音轨预处理 → 冻结 CLIP ViT-B/32 与 WavCaps HTSAT-BERT → 原 KA-GZSL 已训练模型 → 类别语义原型距离匹配 → 预测类别、Top-5 相对置信分数及可下载 JSON。

**重要：代码完整不等于端到端已经验证。** 验证状态以 `artifacts/VALIDATION.md` 和实际测试报告为准。缺少编码器权重时，页面明确禁用视频分类，不会用随机特征、零音频、其他 CLAP 模型或假概率冒充结果。真实特征验证按钮只验证 KA-GZSL 分类部分。

当前优先接入已完成完整训练的 **UCF 模型**。不会将 ActivityNet/VGGSound 的短程测试权重当成完整训练模型。

## 为什么要加前端编码器

你提到的“AVCV”可能指 AVCA，但本次以实际代码为依据：所固定 KA-GZSL 版本的提取脚本使用 **CLIP 512 维视觉特征 + WavCaps 1024 维音频特征**，不是直接把视频送进 KA-GZSL，也不是随意找一个音频网络即可替换。旧配置中的 128/4096 维字段不能用来推断当前模型的实际输入接口。详见 [技术方案](docs/architecture.md)。

## 页面功能

- 选择/拖入视频、浏览器本地预览、GZSL / ZSL 候选集切换。
- 后端实际阶段进度、类别、Top-5、剩余候选概率总和、耗时与模型校验值。
- 明确区分“原始视频推理”和“已有特征验证”，错误及缺件状态不伪造输出。
- 任务隔离、上传体积/时长限制、串行 GPU 推理、本机访问限制、短期中间文件留存。

## 在 VOA285C 上打开

服务在 WSL Ubuntu-22.04 中运行。浏览器访问：

```text
http://127.0.0.1:8765
```

在 WSL 中启动：

```bash
cd /home/admin/projects/WH/ka-gzsl-demo
bash scripts/serve.sh
```

Windows 启动脚本及本机实际路径见 `windows/` 和 `artifacts/VALIDATION.md`。

## 新环境部署

网页使用独立 Python >=3.10 环境。模型兼容层使用独立 Python 3.8.20 环境，复用已验证的 PyTorch 1.7.1 依赖；不修改旧训练环境。

```bash
python3 scripts/bootstrap_local.py \
  --source-repo /absolute/path/to/KA-GZSL-repro \
  --python38 /absolute/path/to/python38/bin/python \
  --legacy-site-packages /absolute/path/to/clipclap/lib/python3.8/site-packages \
  --ffmpeg-bin /absolute/path/to/clipclap/bin
.venv-web/bin/python -m pip install -r requirements-web.txt
.venv-model/bin/python -m pip install -r requirements-model-extra.txt
.venv-model/bin/python -m pip install --no-deps \
  https://codeload.github.com/openai/CLIP/zip/d05afc436d78f1c48dc0dbf8e5980a9d471f35f6
```

没有旧训练环境的电脑，应先按原代码完成训练环境和模型复现，再导出展示包。此项目不是把旧依赖强行升级到新 PyTorch 的实现。

### 导出已训练模型、类别向量与验证集偏置

```bash
.venv-model/bin/python scripts/export_bundle.py \
  --stage-a /path/to/full-run/stage-a \
  --stage-b /path/to/full-run/stage-b \
  --data-root /path/to/data/UCF
```

脚本依据 stage-A 最佳模型的 epoch 选择配对 stage-B checkpoint，只从 `Validation betas` 读取偏置，**不使用测试标签调参**。示例固定选择测试特征的第一条，只用于功能检查，不用于概率校准。

### 编码器权重

```bash
.venv-model/bin/python scripts/download_clip.py
# 已取得可信的同款 WavCaps 权重后，可安装到项目内：
.venv-model/bin/python scripts/download_clip.py --wavcaps-local /path/to/HTSAT_BERT_zero_shot.pt
```

CLIP 下载自官方源码内的地址并验证官方 SHA256。WavCaps 必须使用与训练特征匹配的权重，官方来源见 [模型清单](assets/MODELS.md)。该脚本不会绕过下载站点授权，不会自动选择其他 LAION-CLAP。

### 测试与启动

```bash
.venv-web/bin/python -m pytest -q tests/test_web.py
.venv-model/bin/python scripts/verify_model.py
bash scripts/serve.sh
```

## 相对置信分数并非准确率

当前使用 `softmax((-distance - seen_bias) / temperature)`。默认 `temperature=1.0`，显示为**未校准相对置信分数**。候选类别变化会改变这些数值，候选外的视频也可能被高分归到某个候选类。不能据此宣称开放世界识别能力。

`calibrate_temperature.py` 只在用户提供的独立标注校准数据上拟合温度并写出报告，不自动改动线上配置。最终模型与输入域仍需独立验证。详见 [概率与评估说明](docs/architecture.md)。

## 中间文件与上传范围

每次运行在本项目 `runtime/jobs/<uuid>/` 保存 `request.json`、`metadata.json`、中间帧、10 秒音频数组、`features.npz`、`scores.npz`、`result.json` 和工作日志。没有原始视频的特征验证任务不会生成视频帧。

**WH 是公开仓库。** 提交源代码、配置模板、脚本、去标识化实验清单、验证报告和非私密示例结果；不自动发布用户上传的视频/音频，不把虚拟环境、原始数据集和大体积模型权重塞入 Git 历史。模型和类别向量保留在本机 `assets/ucf/`，并提供导出脚本与 SHA256 清单。测试报告会列出已上传和本机保留的范围。

## 目录

```text
static/                  展示页面，无外部 CDN 依赖
webapp.py                FastAPI 上传、任务与结果 API
inference.py             独立 Python 模型进程
media.py                 视频与音轨预处理
model_adapter.py         原 KA-GZSL / CLIP / WavCaps 适配
scripts/                 环境、模型导出、下载、测试与校准脚本
tests/                   Web API 安全/错误处理测试
docs/                    方案、可信度与部署边界
assets/                  模型来源清单；大模型与语义向量留在本机
artifacts/               可公开的真实验证报告、参数和结果
runtime/                 本机任务及中间文件，不提交
.vendor/                 固定上游源码快照，不修改原仓库
```

## 引用与第三方说明

原模型代码：`pointerHu/KA-GZSL`，固定提交 `085eae46195728fef3ad86b7a046528913f9bc39`。CLIP 与 WavCaps 原项目、论文和第三方许可见 [来源说明](docs/sources.md)。新增展示代码不改变原论文的模型贡献，也不将网页工程实现当作新的实验结果。
