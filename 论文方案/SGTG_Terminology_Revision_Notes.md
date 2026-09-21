# SGTG 英文稿专业术语修订说明

修订日期：2026-09-21  
目标文件：`论文方案/SGTG_English_Translation.docx`  
依据版本：`pointerHu/WH`，提交 `da53a2e296d8c669fa3b05ae4a9ebb642cc1a99b`。

用户所写的 `GTG_English_Translation.docx` 在该目录中不存在；本次修改的是此前生成并上传的 `SGTG_English_Translation.docx`。本次工作是术语溯源与表述修订，不是对方法、实验结果或参考文献元数据的重新验证。

## 一、按“本地文件名”实际读取的四篇材料

文件定位依据为 `论文方案.md` 第 0.2 节“使用到的论文及本地文件”。以下文件均位于当前说明所在的 `论文方案/` 目录。

| 编号 | 原论文与本地文件 | 本次使用的章节 | 在英文稿中的引文编号 |
|---|---|---|---|
| R1 | *Audio-Visual Generalized Zero-Shot Learning using Pre-Trained Large Multi-Modal Models*；`Audio-Visual_Generalized_Zero-Shot_Learning.md` | 第 2 节 Zero-Shot Learning；第 3 节 Model architecture；第 4.1 节 Evaluation metrics、Feature extraction、Implementation details | [4] |
| R2 | *Semi-IIN: Semi-supervised Intra-inter modal Interaction Learning Network for Multimodal Sentiment Analysis*；`Semi-IIN论文完整.md` | 第 3.2 节 Feature fusion；第 3.3 节 Gate mechanism | [10] |
| R3 | *Question-Aware Gaussian Experts for Audio-Visual Question Answering*；`QA-TIGER_CVPR2025_完整论文.md` | 第 2.2 节 Temporal Grounding；第 3.1 节 Input Representation；第 3.2 节 Question-Aware Fusion；第 3.3 节 Temporal Integration of Gaussian Experts | [15] |
| R4 | *Audio-visual Generalized Zero-shot Learning the Easy Way*；`EZ-AVGZL论文实验前内容.md` | 第 3.2 节 Class Embedding Optimization；第 3.3 节 Supervised Audio-Visual Language Alignment | [7] |

R4 本地材料只包含实验章节之前的内容。本次仅据其方法部分校对术语，未将未包含的实验内容当作依据。方案索引的说明文字建议写作 `EZ-AVGZSL`，但实际论文自称 `EZ-AVGZL`；英文稿保留原论文的 `EZ-AVGZL`，不按照索引中的改写重命名该方法。

## 二、主要术语与出处

“原文术语”表示四篇材料中有直接对应的英语表达；“本文适配/定义”表示保留原文术语的概念基础，但根据当前稿件的输入、公式或分支定义进行明确限定，不声称原论文已经提出本文模块。

| 原稿中的表述或问题 | 修订后的表达 | 依据与范围 |
|---|---|---|
| `class-text embeddings`、`class-label embeddings`、`dual text embeddings` | `class label embeddings`、`two class label embeddings` | R1 第 3 节原文术语；用于 CLIP/CLAP 文本编码器的类别嵌入。 |
| 泛指的 `class prototypes`、`semantic prototypes`、`prototypes` | `class embeddings`；摘要首次说明 `class embeddings (class prototypes)` | R4 第 3.2 节原文术语；建立与稿件原型概念的对应，未改变原型的构造、归一化或固定方式。DSPO 专有名称及原图标签不改。 |
| `class separation`、`prototype separability` | `class separability` | R4 第 3.2 节 Class Separability。t-SNE 的几何描述仍用 `inter-class separation`，不机械替换。 |
| `semantic topology preservation`、`semantic structure preservation` 等混用 | `semantic preservation`；具体解释使用 `semantic relationships`、`semantic structure` | R4 第 3.2 节原文术语，避免将保留距离相对排序过度表述为一般拓扑不变量保持。 |
| `ranking-based semantic-preservation loss`、`ranking-preservation loss` | `margin ranking loss for semantic preservation`、`margin ranking loss` | R4 第 3.2 节原文术语；原稿的损失符号和式 (5) 不变。 |
| `ranking margin` | `margin coefficient` | R4 第 3.2 节原文术语；原稿使用的符号和数值不变。 |
| 含混的 `semantic alignment loss`、`supervised contrastive alignment objective` | `Supervised audio-visual language alignment`；`a supervised text-audio-visual contrastive loss inspired by [7]` | R4 第 3.3 节及摘要；用 `inspired by` 明确本文并非逐式照搬原论文损失。 |
| `compatibility score` | `similarity score`；式 (30) 的计算说明为 `temperature-scaled cosine similarity` | `similarity` 来自 R4 第 3.3 节；后者由当前稿件式 (30) 和单位范数类别嵌入直接解释，不冒充 R4 的具体打分器。 |
| `projection head`、笼统的 shared space 表述 | `projection network`、`joint embedding space` | R1 第 3 节原文术语；不改投影结构或维度。 |
| 未明确命名的模态内/模态间 masked attention | `Intra-modal Masked Attention (IntraMA)`；`Inter-modal Masked Attention (InterMA)` | R2 第 3.2 节原文机制名；相关工作首次给出全称，DMIF 方法段说明其来源。 |
| DMIF 中 `cross-modal representation` 与 `inter-modal representation` 混用 | DMIF 两支统一为 `intra-modal representation`、`inter-modal representation` | 对齐 R2 的 intra/inter 区分；一般性 `cross-modal attention` 不被整体替换。 |
| `learnable aggregation token`、`masked-attention layers` | `learnable special token for feature aggregation`、`masked attention units` | R2 第 3.2–3.3 节；保留本文每支一个特殊 token 的实现，不加入 R2 的两个 token。 |
| `Semantic-conditioned sequence encoding` | `Class-semantic-aware early fusion` | 本文适配：R3 第 3.2 节是 `Question-Aware Fusion`，方案第 0.2 节明确将其迁移为类别语义感知早期融合。不是 R3 原有模块的同名复制。 |
| `Temporal aggregation with multiple Gaussian experts` | `Temporal integration of Gaussian experts` | R3 第 3.3 节原文标题；CGTA 的作者自定义名称及缩写保留。 |
| `Gaussian temporal distributions`、含混的中心锚定措辞 | `Gaussian distributions`；`predicted offsets from initial centers` | R3 第 3.3 节 Gaussian Generation；对应原稿现有中心偏移公式，不修改公式。 |
| 对高斯专家框架、摘要和路由的零散称呼 | `Mixture of Experts (MoE)`、`soft masks`、`aggregated representations`、`router`、`routing values (expert weights)` | R3 第 3.3 节原文术语；保留本文 Softmax 对所有专家赋权的方式，不称为离散专家选择。 |
| `attribute-level semantic tokens` | `description embeddings`；`one encoded description per row` | 本文适配/定义：R1 使用 class attributes/descriptions 与 text embeddings；结合稿件式 (1)–(2) 的行粒度说明。它不是 R3 的 `word-level question features`，也不宣称 `description embeddings` 是四篇论文中的专有模块名称。 |
| `class-name templates` | `class name prompts` | R1 第 4.1 节使用 text prompts / text prompt ensembles；当前稿件未明确的集成实现不额外添加。 |
| `mean accuracy` 与 HM 的表述不够精确 | `mean class accuracy`；`harmonic mean (HM)` | R1 第 4.1 节 Evaluation metrics；明确 seen/unseen 分别按类平均，常规 ZSL 的候选集与测试样本仅限未见类。 |
| 结尾的 `open-category recognition` | `audio-visual generalized zero-shot recognition` | 对齐 R1/R4 的任务范围，不将预先给定未见类别语义的 GZSL 混同于没有候选类别边界的开放集识别。 |

此外，正文的 `pretrained` 统一为 `pre-trained`；参考文献条目保持原状。

## 三、明确保留的本文设计边界

1. **作者自定义名称不伪装成来源术语。** 保留 SGTG、Discriminative Semantic Prototype Optimization (DSPO)、Class-Conditioned Gaussian Temporal Aggregation (CGTA)、Decoupled Modality Interaction and Gated Fusion (DMIF)。正文分别解释其与 class embedding optimization、Gaussian experts、IntraMA/InterMA 的关系，而不是把整个模块改成参考方法名。
2. **问题条件不等于类别条件。** QA-TIGER 的 query 来自问题；本文来自类别描述与优化后的类别嵌入。正文明确这是适配，并未移入原论文的问答任务、词级 token、patch-level 分支或全部跨注意力步骤。
3. **动态门控不意味着结构相同。** Semi-IIN 使用两个特殊 token 和 sigmoid 门控；本文保持每支一个特殊 token、三路 sample- and class-conditioned Softmax 门控，直接时序证据仍是本文定义的旁路。没有引入 Semi-IIN 的半监督伪标签自训练。
4. **同类损失名称不意味着同一公式。** EZ-AVGZL 的对比损失使用当前 batch 的类别嵌入；本文式 (31) 仍对全部已见类别归一化。EZ-AVGZL 的非线性相似度模块也不被强行复制到本文式 (30)。
5. **表征粒度依据当前公式。** 当前描述矩阵每行对应一条描述，因此不以 QA-TIGER 的 word-level terminology 替代 description-level 表征。直接时序证据的文字被解释为不经过后续 masked attention 分支，而非凭空增加新运算。
6. **不修订实验论断。** 文献中的特征配置、数值与本文实验表存在的差异不在本次术语任务中擅自消除；本次不意味着已经复现实验或验证性能结论。

## 四、文件与排版校验

- 修改正文 56 个段落，并修订相应表格标签；共修改 87 个 Word 文本节点。该计数不是“87 处科学错误”。
- 保留全部 32 个编号公式；244 个 Office Math 对象与修订前逐对象一致。
- 9 张表的数值逐项保持一致，3 幅嵌入图未改动。
- 32 条参考文献条目不改动；仅在正文相应位置补明已有引文 [7]、[10]、[15] 的方法来源。
- 文档包共 22 个部件，只有 `word/document.xml` 的普通文本节点发生改变；其余 21 个部件字节一致。原有段落、文字格式、公式、绘图及节属性保持不变。
- 完成 18 页渲染检查，未发现文字、表格或公式被裁切。三个数据集名称中的斜体上标 `cls` 保留。
- 中文论文、四篇参考材料、`论文方案.md` 与 `manuscript_translation_assets.zip` 不修改。

## 五、溯源校验值

以下为本次使用的 Git blob SHA（不是论文 DOI）：

```text
论文方案.md
80a5a4f03b7a4e0aa8372a7aca00290ffe5d6012

Audio-Visual_Generalized_Zero-Shot_Learning.md
0c93d936084085ad0e28fb24300fd33cb829bc44

Semi-IIN论文完整.md
1884802ef618685edc1f8a0cf8f9f7d0c671935a

QA-TIGER_CVPR2025_完整论文.md
d34c39df2523ae0d502aea2649a0cc4c0788568f

EZ-AVGZL论文实验前内容.md
353adfdfbd783bec4babdadadeb882041788a8dd

修订前 SGTG_English_Translation.docx
e5eff9e7f2d68e8e5dc5dcde5d837ea461bc297f
```

修订后的 `word/document.xml` SHA-256：

```text
eafd1d37e316ee47a0084f4264578d73a823e6eb1ea517dd877a72d94afcacdd
```
