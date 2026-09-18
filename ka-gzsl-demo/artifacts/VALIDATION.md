# VOA285C 实际验证记录

更新：2026-09-18 23:12（UTC+08:00）。设备：DESKTOP-VOA285C；WSL2 Ubuntu-22.04；RTX 3090 Ti。

**当前结论：已使用用户安装的 HTSAT_BERT_zero_shot.pt，完成原始含音轨视频 → CLIP/WavCaps → KA-GZSL → 类别和相对置信分数的完整推理。不是只用已有特征或模拟预测。** 本次没有下载 Google Drive 文件。

完整机器记录在 [raw_video_verification.json](raw_video_verification.json)。其中 `reports` 按原文件名无损汇集本次编码器、HTTP、样本来源和分类器验证记录；单项 JSON 同时保留在本机 `artifacts/`。旧的“尚缺权重”状态可在 Git 历史中查看。

## 实际执行结果

| 项目 | 结果 | 说明 |
|---|---|---|
| 编码器加载与 GPU 前向 | 通过 | WavCaps 音频分支严格加载权重，输出 [1,1024]；CLIP 输出 [1,512]；输出有限且归一化 |
| 合成音视频 HTTP 完整流程 | 通过 | 仅检查技术流程，绝不计为准确率 |
| 真实 AVI，GZSL | 通过 | ApplyEyeMakeup，28.4743%；48 个候选；模型工作进程 7.53 秒，HTTP 总耗时 8.55 秒 |
| 同一 AVI，ZSL | 通过 | 仅 6 个未见类参与，返回 ShavingBeard，27.3694%；这证明候选过滤生效，不是该视频识别正确 |
| 浏览器兼容 MP4，GZSL | 通过 | ApplyEyeMakeup，25.8872%；模型工作进程 7.22 秒，HTTP 总耗时 8.05 秒 |
| 无音轨视频 | 按预期拒绝 | 明确提示双模态模型需要音轨，不填充假的音频特征 |
| 原分类器适配回归 | 通过 | 真实已提取特征；logit 最大绝对差 0；错误音频维度被拒绝 |
| Web API 回归 | 8 passed | 退出码 0；2 条测试依赖弃用提示 |
| Windows Chrome 页面检查 | 通过 | 就绪页及真实任务结果页已截图检查；历史结果显示 ApplyEyeMakeup / 28.47% |

HTTP 测试向实际服务上传真实视频字节，核对任务完成、特征维度、Top-5、分数总和、JSON 下载一致性及预览帧返回。没有声称完成了浏览器文件选择器的自动化测试。

## 样本与结果解释

真实测试视频来自 OpenMMLab MMAction2 官方仓库的 `tests/data/test.avi`，固定提交 `a5a167dff2399e2d182a60332325f9c0d4663517`。样本来源、SHA256、转码方法均在汇总 JSON 的 `public_sample_provenance.json` 中记录。官方 `demo/demo.mp4` 不含音轨，没有给它补假音频来冒充双模态测试。

浏览器示例是上述 AVI 转码成 H.264/AAC 的 MP4。转码会改变像素、音频和部分容器信息，因此两个文件的分数不同；不得将它们当成逐字节相同输入。这些样本用于功能验证，不是新的论文测试集实验。

候选范围为已完成训练的 UCF 模型所对应的 **42 个已见类 + 6 个未见类**。不是 UCF101 全部 101 类，也不是任意开放词汇。ApplyEyeMakeup 属于已见类，切换到 ZSL 后被排除，因而该模式下不能期待返回它。

## 模型与特征保持情况

原 KA-GZSL 固定提交：`085eae46195728fef3ad86b7a046528913f9bc39`。使用先前完整 UCF 训练导出的配对 stage-B 第 12 轮模型；不使用其他数据集的短程权重。

模型源文件校验值保持不变：`1cfbbac918c583354646f24001710e886153d37c0ca2c5306fbf9fb09773df7b`。

用户安装的 WavCaps 文件共 1,698,673,868 字节，本机计算 SHA256 为 `e2ab66db3af1aedea4100e294bbceeadf3df519f9bea8ae3121d5828a87f0a1b`。这是本机文件的追踪校验值，不是声称已取得官方发布者的签名或官方校验清单。

从完整 WavCaps checkpoint 中严格加载音频编码器和投影层，类别文本向量使用已导出的语义原型，因此本次不需要额外下载 BERT 或先加载 HTSAT.ckpt。模型实现和损失没有修改，新增页面和脚本只位于 WH。

默认保留原提取脚本的 `legacy` 预处理，包括其中的 BGR/浮点 ToPILImage 行为，没有擅自切换到修正版 RGB。**目前仍未取得“原始视频 + 对应训练特征”的配对一致性验证；结构匹配和一次成功分类不能替代这项检查。**

## 分数与科学边界

显示分数为 `softmax((-distance - seen_bias) / temperature)`，温度 1.0；已见类偏置 2.933333158493042 来自 stage-A 验证记录，而非测试标签调参。分数未经过独立数据概率校准，不等于准确率或正确概率；也没有开放集合拒识保证。

`model_verification.json` 的 `raw_video_end_to_end_verified=false` 仅说明该单项分类器测试不覆盖原始视频。当前整体结论以汇总 JSON 顶层的 `raw_video_end_to_end_verified=true` 及真实视频 HTTP 记录为准。

## 本机入口与中间文件

- 页面：`http://127.0.0.1:8765`。
- Windows 启动：`D:\learning\work\WH\ka-gzsl-demo\start-demo.cmd`。
- 可选择的真实 MP4 示例：`D:\learning\work\WH\ka-gzsl-demo\examples\mmaction2-test-av.mp4`。
- WSL 项目：`/home/admin/projects/WH/ka-gzsl-demo`。
- 原 AVI 的已完成任务：`runtime/jobs/e7e30d80745046a49a4bc949d615e74f/`。
- 视频结果页支持 `?job=<任务ID>`；刷新后可恢复真实结果及中间帧。选择新视频会清除旧预测，避免误配。

任务目录保存输入视频、音轨、32 kHz/10 秒波形、中间帧、features.npz、scores.npz、result.json 和日志。默认 24 小时保留策略在服务启动或创建新任务时执行清理；历史任务过期后链接会失效，已提交的验证报告不会受影响。

## GitHub 与本机保存范围

WH 中提交全部展示源代码、前端更新、配置模板、准备/验证/校准脚本、说明和完整 JSON 验证记录集合。模型权重、语义 NPZ、虚拟环境、第三方源快照、原视频/音频和截图留在本项目的本机目录，不发布到公开 Git 历史。JSON 中保留生成方式和校验信息，不把“留在本机”说成“已上传 GitHub”。
