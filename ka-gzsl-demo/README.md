# KA-GZSL 原始视频论文展示系统

独立项目，全部新增源代码和说明位于 **WH/ka-gzsl-demo**，不修改 `pointerHu/KA-GZSL`。

**2026-09-18：已在 DESKTOP-VOA285C 的 WSL2 + RTX 3090 Ti 上完成真实含音轨视频的端到端推理。** 用户安装的 `HTSAT_BERT_zero_shot.pt` 已接入；本次没有继续下载 Google Drive 文件。当前展示使用已完整训练的 UCF 模型。

实际状态与证据：[验证报告](artifacts/VALIDATION.md) · [完整 JSON 记录集合](artifacts/raw_video_verification.json)。成功运行不代表已经复现论文准确率或完成置信度校准。

## 立即使用：VOA285C

双击 Windows 启动入口：

```text
D:\learning\work\WH\ka-gzsl-demo\start-demo.cmd
```

浏览器访问：

```text
http://127.0.0.1:8765
```

点击选择或拖入**含音轨**的视频，保留 `GZSL · 已见类 + 未见类`，点击“开始视频分类”。真实推理完成后显示类别、Top-5 相对置信分数、耗时和可下载 JSON。不要把“运行真实特征验证”按钮当成视频上传识别，它只测试已提取特征的分类器。

本机已经准备了一个浏览器可播放的真实测试示例：

```text
D:\learning\work\WH\ka-gzsl-demo\examples\mmaction2-test-av.mp4
```

本次该 MP4 的预测是 `ApplyEyeMakeup`，相对分数 **25.89%**，模型工作进程耗时 **7.22 秒**。对应原始 AVI 的相对分数为 **28.47%**；转码改变了输入，不要求两个文件的分数一致。来源和 SHA256 见验证记录，这不是新的准确率基准。

视频结果会把任务 ID 写入地址栏，刷新页面可恢复结果与中间帧。已完成原始 AVI 任务的本机地址：

```text
http://127.0.0.1:8765/?job=e7e30d80745046a49a4bc949d615e74f
```

历史任务清理后链接会失效。选择新视频时会清除旧预测，防止把上一段视频的结果误认为新视频结果。

## 输入视频如何进入论文模型

```text
原始视频
  ├─ 读取中间帧 → 冻结 CLIP ViT-B/32 → 512 维视觉特征
  └─ 提取音轨 → 32 kHz 单声道 → 居中截取/补齐至 10 秒
                              → 冻结 WavCaps HTSAT-BERT → 1024 维音频特征
       ↓
原 KA-GZSL 已训练网络 → 类别语义原型距离 → 已见类偏置 → 类别与相对分数
```

以固定版本代码为准：当前接口是 **512 维 CLIP 视觉 + 1024 维 WavCaps 音频**。旧 YAML 的 128/4096 字段不是当前实际特征接口，也不能任意换成另一个同名 CLAP。类别文本向量使用已导出的 1536 维 CLIP/WavCaps 语义原型。

完整 WavCaps checkpoint 已包含音频编码器和投影层，本项目严格加载这两部分；推理现有类别不需要再下载 BERT，也不需要先加载作者硬编码路径中的 HTSAT.ckpt。无音轨视频会明确报错，不使用随机特征或假音频补位。

默认保留原提取脚本的 `legacy` 行为。原脚本的 BGR/浮点转 PIL 处理存在值得注意的历史行为，不能偷偷修正后声称特征完全一致。详细分析见 [技术方案](docs/architecture.md)。原始视频与已有训练特征的配对数值一致性仍待验证。

## 候选类别和置信分数

当前 GZSL 候选为 **42 个已见类 + 6 个未见类，共 48 类**；ZSL 仅在 6 个未见类中选择。不是 UCF101 全部 101 类，更不是任意开放词汇。默认建议使用 GZSL 展示普通上传视频；ZSL 会主动排除所有已见类。

分数计算为 `softmax((-distance - seen_bias) / temperature)`。温度默认 1.0，显示为**未校准相对置信分数**，不等于准确率或真实正确概率。候选外事件也会被分到某个候选类；本系统没有开放世界拒识保证。不会为了使页面分数更好看而人为缩小温度。

`calibrate_temperature.py` 仅对独立标注校准数据拟合温度并写报告，不自动改线上配置；不得用训练或测试标签冒充独立校准集。

## 新电脑部署与依赖

网页使用独立 Python >=3.10 环境；模型使用独立 Python 3.8.20 环境，复用已验证的 PyTorch 1.7.1 依赖，不覆盖原训练环境。

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

没有旧环境的电脑，先按原项目建立可用训练环境，再导出展示包。本机 `.venv-model` 仍依赖共享的旧 PyTorch 包目录，不能删除该目录。实际配置在未提交的 `config.local.json`。

导出配对的训练模型、类别向量和验证集偏置：

```bash
.venv-model/bin/python scripts/export_bundle.py \
  --stage-a /path/to/full-run/stage-a \
  --stage-b /path/to/full-run/stage-b \
  --data-root /path/to/data/UCF
.venv-model/bin/python scripts/download_clip.py
.venv-model/bin/python scripts/download_clip.py --wavcaps-local /path/to/HTSAT_BERT_zero_shot.pt
```

只安装可信来源的本地权重；不允许浏览器上传 `.pt`。权重来源与安全边界见 [模型说明](assets/MODELS.md) 和 [安全说明](docs/security.md)。不自动下载 Google Drive 文件，不用其他 LAION-CLAP 权重替代。

启动 WSL 服务：

```bash
cd /home/admin/projects/WH/ka-gzsl-demo
bash scripts/serve.sh
```

只监听本机 `127.0.0.1:8765`，不是公网部署。默认最多 100 MB、120 秒，GPU 串行处理。公网部署还需要独立的鉴权、HTTPS、资源隔离及安全评估，不能简单开放当前端口。

## 复查与测试

```bash
.venv-web/bin/python -m pytest -q tests/test_web.py
.venv-model/bin/python scripts/verify_model.py
.venv-model/bin/python scripts/verify_media.py
.venv-model/bin/python scripts/verify_backbones.py
# 先启动服务，再从实际 HTTP 上传视频：
python3 scripts/verify_video_http.py runtime/public-samples/real-av-demo.mp4 \
  --description real_av_demo --output artifacts/my_video_verification.json
```

脚本 `prepare_public_sample.py --archive /path/to/archive.zip` 可从固定官方 MMAction2 归档提取并校验测试 AVI，再生成浏览器 MP4。归档地址为：

```text
https://codeload.github.com/open-mmlab/mmaction2/zip/a5a167dff2399e2d182a60332325f9c0d4663517
```

本次验证包含真实 AVI 的 GZSL/ZSL、真实转码 MP4、合成音视频流程、无音轨拒绝、JSON 下载一致性、分类器等价性和 Windows 页面截图检查。详细结果不以“代码看起来能运行”代替，见验证报告。

## 目录和上传范围

```text
static/                  页面、交互与历史结果恢复
webapp.py                FastAPI 上传、任务和结果 API
inference.py             独立模型进程
media.py                 视频/音轨预处理
model_adapter.py         原 KA-GZSL、CLIP、WavCaps 适配
scripts/                 环境、导出、样本、验证和校准脚本
tests/                   Web API 测试
docs/                    技术方案、安全与来源
artifacts/               真实验证报告及中间结果 JSON 集合
assets/                  本机模型、类别向量及来源清单
runtime/jobs/<uuid>/      本机输入、中间帧/音频/特征/分数、结果、日志
.vendor/                 固定上游源码副本，不改原仓库
```

**WH 是公开仓库。** 上传源代码、配置模板、脚本、说明、模型校验清单和完整验证记录集合；不把权重、语义 NPZ、虚拟环境、原视频/音频或私人上传内容发布到 Git 历史。所有任务中间文件留在本项目本机目录。默认 24 小时保留策略在服务启动或新建任务时清理，历史结果链接届时会失效。

原模型固定提交为 `085eae46195728fef3ad86b7a046528913f9bc39`。第三方论文、源代码与许可见 [来源说明](docs/sources.md)。展示工程不改变原论文模型贡献，也不把单个演示视频的预测写成论文性能结论。
