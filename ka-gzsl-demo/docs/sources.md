# 固定源码、论文与官方文档

检索/核对日期：2026-09-18。以下均为技术来源，不意味着取得了所有模型文件。

1. KA-GZSL 用户仓库，固定 commit：
   https://github.com/pointerHu/KA-GZSL/tree/085eae46195728fef3ad86b7a046528913f9bc39
2. 实际 UCF 特征提取脚本（包括原脚本的预处理及本机绝对路径问题）：
   https://github.com/pointerHu/KA-GZSL/blob/085eae46195728fef3ad86b7a046528913f9bc39/clip_feature_extraction/get_clip_features_ucf.py
3. CLIP 官方代码，固定 commit：
   https://github.com/openai/CLIP/tree/d05afc436d78f1c48dc0dbf8e5980a9d471f35f6
4. WavCaps 官方代码及模型说明：
   https://github.com/XinhaoMei/WavCaps
   https://github.com/XinhaoMei/WavCaps/tree/master/retrieval
5. AVCA 官方代码，用于澄清命名/数据划分来源：
   https://github.com/ExplainableML/AVCA-GZSL
6. ClipClap-GZSL 官方代码：
   https://github.com/dkurzend/ClipClap-GZSL
7. FastAPI 文件上传文档：
   https://fastapi.tiangolo.com/tutorial/request-files/
8. Guo et al., On Calibration of Modern Neural Networks, ICML 2017：
   https://proceedings.mlr.press/v70/guo17a.html

## 许可

原 KA-GZSL/CLIP 源码各自保留上游许可。WavCaps 官方 README 对数据集说明学术用途限制，并说明其模型依据英国非商业研究数据版权豁免创建；外部公开或商业使用前需自行核对适用许可。本项目不重新许可这些第三方模型，不将它们当作自己训练的编码器。
