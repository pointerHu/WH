# VOA285C 实际验证记录

日期：2026-09-18。设备：DESKTOP-VOA285C；WSL2 Ubuntu-22.04；RTX 3090 Ti。

**当前结论：网页、真实已提取特征的 KA-GZSL 分类、视频预处理和 CLIP 编码均已验证；原始视频完整双模态分类仍未验证，因为缺少匹配的 WavCaps 权重。**

## 已执行的验证

| 项目 | 实际结果 | 记录 |
|---|---|---|
| Web API 测试 | 8 passed，退出码0；两条测试依赖弃用提示 | `tests/test_web.py` |
| 原模型适配一致性 | 真实 UCF 特征；logit 最大绝对差0；错误音频维度被拒绝 | `model_verification.json` |
| HTTP→独立模型进程→JSON下载 | 成功，48个候选；本次模型工作耗时约1.98秒 | `http_verification.json`、`http_feature_result.json` |
| 视频/音轨预处理 | 合成测试视频中间帧320×240；音频[1,320000]；无音轨被拒绝 | `media_verification.json` |
| 官方 CLIP 权重 | 下载成功、官方SHA256匹配、GPU前向输出[1,512]、归一化范数1 | `media_verification.json` |
| Windows浏览器 | 127.0.0.1:8765可访问；Chrome无头截图已人工检查布局及缺件提示 | 截图保留本机 `runtime/page-preview.png` |
| Windows启动入口 | 已验证可识别已有服务，避免重复启动并打开页面 | `windows/start-demo.cmd` |
| 原始视频端到端分类 | **尚未完成** | 缺少 `HTSAT_BERT_zero_shot.pt` |

预处理测试使用合成色彩图和440Hz音调，只证明解码和形状正确，绝不作为真实动作识别准确率证据。

模型测试固定使用数据集第一条特征，没有挑选“看起来正确”的示例。本条参考类别是 ApplyEyeMakeup（ID 0），按原模型及验证偏置得到的第一预测为 ShavingBeard（ID 77），相对分数约22.90%。这条样本分类不正确；**测试通过指原模型与适配代码一致，不是预测正确，也不是论文指标重新得到证明。**

## 使用的模型

原 KA-GZSL 固定提交：`085eae46195728fef3ad86b7a046528913f9bc39`。

使用已有完整 UCF 训练记录：stage A训练20轮，配对stage B checkpoint为第12轮；已见类偏置从stage-A验证结果取得，值2.933333158493042。候选为42个已见类+6个未见类，合计48类；ZSL模式仅6个未见类。不是UCF101全部101类，也不是任意开放词汇。

模型源文件校验值前后相同：`1cfbbac918c583354646f24001710e886153d37c0ca2c5306fbf9fb09773df7b`。原KA-GZSL目录的git状态未新增本项目修改。展示工程只在WH目录新增内容。

## 文件位置

WSL项目：`/home/admin/projects/WH/ka-gzsl-demo`。

Windows快捷入口：`D:\learning\work\WH\ka-gzsl-demo\start-demo.cmd`。

页面：`http://127.0.0.1:8765`（只监听本机）。

本机模型、类别向量：`assets/ucf/`，模型包约46.95MiB。CLIP权重：`assets/backbones/ViT-B-32.pt`，约337.5MiB。

依赖分别安装到本项目的`.venv-web`和`.venv-model`。模型环境使用Python3.8.20，并只读复用之前已经验证的PyTorch1.7.1依赖目录；不能删除该旧依赖目录。PyPI直连不通时，本次用HTTPS清华镜像临时安装，没有修改全局pip源。网页实际依赖版本见 `web-requirements.lock.txt`。

## 尚缺的文件与下一项验证

本机未找到匹配的WavCaps `HTSAT_BERT_zero_shot.pt`。官方Google Drive模型目录的连接访问授权未通过，没有绕过授权获取文件。取得可信的同款文件后，放到：

```text
/home/admin/projects/WH/ka-gzsl-demo/assets/backbones/HTSAT_BERT_zero_shot.pt
```

刷新页面可重新检测文件；仍须执行真实含音轨视频的完整推理，并用“原始视频+已有特征”配对样本验证特征一致性。不能仅凭文件存在或维度相同就宣称匹配。

## 上传到WH与本机保留的范围

提交：全部新增应用源代码、界面、配置模板、启动/模型导出/下载/校准/验证脚本、说明、真实测试报告、依赖版本、模型与类别校验清单、非私密示例JSON结果。

本机保留、不提交公开Git历史：模型权重和语义NPZ、虚拟环境、上游源码快照、上传视频/音频、中间帧/特征、进程日志和浏览器临时资料。所有这些项目相关资产均有本项目内的存放位置、生成脚本或说明；并非声称已经把所有二进制资产上传到了GitHub。
