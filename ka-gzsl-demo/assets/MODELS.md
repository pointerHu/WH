# 模型与资产清单

| 文件 | 角色 | 获取方式 |
|---|---|---|
| `ucf/model.pt` | 完整训练 stage-B 的 KA-GZSL 权重，不含优化器 | `scripts/export_bundle.py` 从本机复现记录导出 |
| `ucf/class_bank.npz` | 与 checkpoint 配对的类别语义向量、ID、seen mask | 同一导出脚本；不是重新生成不匹配文本向量 |
| `ucf/example_features.npz` | 第一条真实 UCF 测试特征，用于分类接口验证 | 同一导出脚本，不用于概率校准 |
| `ucf/manifest.json` | 版本、参数、类别表、验证偏置、SHA256 | 同一导出脚本 |
| `backbones/ViT-B-32.pt` | 官方 CLIP ViT-B/32 | `scripts/download_clip.py`，官方校验值验证 |
| `backbones/HTSAT_BERT_zero_shot.pt` | 匹配原特征的 WavCaps ASE 音频分支权重 | 官方项目模型目录，须具备访问权限并核对版本 |

WavCaps 官方来源：
https://github.com/XinhaoMei/WavCaps/tree/master/retrieval

官方 README 指向的模型目录：
https://drive.google.com/drive/folders/1pFr8IRY3E1FAtc2zjYmeuSVY3M5a-Kdj

若下载目录需要授权，必须先取得授权/由用户提供正确文件。不要换成网络上名称类似但未经验证的权重；同样维度的 LAION-CLAP 也不能直接替代此编码器。完成安装后还需用原始视频和已提取特征的配对数据验证数值一致性。

大体积模型、语义向量和用户中间文件默认不加入公开 Git 历史。发布于 `artifacts/export_manifest.json` 的校验清单用于确认本机导出包，不是伪造可用下载链接。
