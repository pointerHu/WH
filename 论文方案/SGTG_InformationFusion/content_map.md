# SGTG → Information Fusion：第二阶段内容迁移对应表

> 当前作者与文献状态已更新至第三阶段；请同时阅读本文件第 13 节、author_reference_review.md 和 citation_map.csv。前面的阶段二文献状态与旧编号表保留为历史记录。

日期：2026-09-23（VOA 本地 UTC+08:00）。设备：DESKTOP-VOA285C。

唯一项目目录：`C:\Users\admin\Documents\GitHub\WH\论文方案\SGTG_InformationFusion`。

本阶段状态：完整 LaTeX 初稿已建立，并在 VOA 本地实际编译出 15 页 PDF。尚非最终精排稿或期刊合规认证；没有进行 Git 暂存、提交、推送，也没有正式投稿。

本次用户明确指定双栏，因此主稿采用本地 cas-dc-template.tex 的 CAS-DC 结构，取代 inventory.md 第 4.1 节的阶段一“暂选 cas-sc”方案。inventory.md 保留为历史盘点；本文件记录本阶段的实际执行结果。

## 1. 本地交付与工程组织

| 内容 | 本项目内的实际路径 |
| --- | --- |
| 主文件 | `source/main.tex` |
| 作者、标题、完整摘要与关键词 | `source/frontmatter.tex` |
| 五个正文文件 | `source/sections/01-introduction.tex` 至 `05-conclusion.tex` |
| 32 个原生编号公式 | `source/equations/eq-01-*.tex` 至 `eq-32-*.tex` |
| 9 张可编辑表格 | `source/tables/table-01-*.tex` 至 `table-09-*.tex` |
| 三张真实图片与图环境 | `source/figures/` |
| 新稿 32 条原文文献 | `source/references.bib`；顺序在 `source/reference_order.tex` |
| 实际编译的当前 PDF | `source/build/main.pdf`（15 页，1,723,520 字节） |
| XeLaTeX / BibTeX 原始日志 | `source/build/main.log`、`main.blg`、`main.bbl`、`main.aux` |
| 构建控制台日志及参数 | `audit/stage2/recheck-20260923-123348/build-console.log`、`build-latest.json` |
| 本地复编译入口 | `scripts/build_local.py` |
| VS Code 项目设置 | `.vscode/settings.json` |
| 来源、逐段/逐格、公式、编号核验 | `audit/stage2/` |

所有正文 input、图像、文献均以 source 为基准使用相对路径；实际构建工作目录就是 source。依据 main.fls，除已安装的 TeX 发行版外，不依赖本项目之外的输入文件，更不依赖旧 KA_GZSL_TMM 工程。

CAS 类、宏包、文献样式的原版权与许可头保持不变。source/license/ 保存原 README、manifest、原 cas-dc-template.tex 及 PROVENANCE.md。没有引入 IEEEtran、IEEEkeywords 或 TMM 导言区。

## 2. 数量、顺序与内容保真核验

| 检查对象 | 原稿 → 本工程的实际核验 |
| --- | --- |
| body 元素 | 205 → 205 个来源对象均分类映射；含 195 个直接段落、9 张表及节属性 |
| 全部文档段落 | 1,009（含单元格）；均在 word-paragraph-ledger.json 中保留来源 XML |
| 正文/列表 | 70 个正文段落 + 4 个贡献列表项；74/74 回译去格式后的文字与 Word 一致，且源码中存在对应完整片段 |
| 标题、摘要、关键词 | 3/3 核验通过；摘要未缩写，3 个关键词未增删 |
| 编号标题 | 29/29 核验通过；含 5 个一级正文章节及各级子标题；References 单独生成 |
| 数学对象 | 244/244 转为原生 LaTeX，每项仅使用一次，出现顺序与 Word 一致；无未知 OMML 元素 |
| 独立编号公式 | 32/32；aux 中实际编号为 (1)–(32)，语义 label 对应正确 |
| 公式文字叶节点 | 1,619 个 m:t 叶节点均由结构解析器消费；源 OMML 和转换结果完整留档 |
| 表格 | 9/9；70 个物理行、814 个物理单元格；814/814 逐格去格式文字与数字 token 核验通过 |
| 图与图注 | 3/3 图片；图注、表题共 12/12 文字核验通过 |
| 参考文献 | 32/32 原文保留；32/32 文字核验及原编号→BibTeX key→实际引文编号核验通过 |
| 其他 Word 内容 | 未发现自动列表编号、文本框、超链接、脚注/尾注、OLE、引文字段、修订或附录/声明章节；另有一条运行页眉及一个 PAGE 页码域，已映射到 CAS shorttitle 和自动页码（见第 12 节） |
| 来源保护 | 初始清单中的 46 个原始文件全部 SHA-256 不变；三张图及模板副本的字节核验通过 |

回译核验只规范化空白并还原 LaTeX 转义、字体命令、数学对象和交叉引用；不删除或替换学术词语、数字、标点。核验没有重新计算实验结果，也没有将旧稿数字复制到新稿。

Word 中仅用于排版的 9 个空段、节属性及图片占位段不作为可见空白逐段复制；图片占位段已映射为真实 figure，内容未遗漏。贡献列表原本是静态 (1)–(4)，现用 enumerate 生成同样编号。

核验范围：32 个独立公式已结合结构与当前 PDF 检查上下标、分式、求和范围、范数、转置、帽/波浪/横线重音、集合及两类掩码；全部 244 项都有原始 OMML 位置和转换台账。此项是排版保真核验，不是对原稿理论正确性的重新论证。

## 3. 原稿章节与 TeX 文件对应

表中 body 索引为原 document.xml 的零基索引；行号为本阶段当前文件的一基行号。每个正文块也有 `% DOCX body[n]` 注释，后续编辑导致行号变化时仍可用此注释定位。

| 原稿标题 | body | TeX 文件与行 | 实际标签 |
| --- | --- | --- | --- |
| 1 Introduction | 3 | `source/sections/01-introduction.tex:4` | `sec:introduction` |
| 2 Related Work | 14 | `source/sections/02-related-work.tex:4` | `sec:related-work` |
| 2.1 Audio-Visual Generalized Zero-Shot Learning | 15 | `source/sections/02-related-work.tex:7` | `sec:audio-visual-generalized-zero-shot-learning` |
| 2.2 Audio-Visual Cross-Modal Interaction and Fusion | 18 | `source/sections/02-related-work.tex:16` | `sec:audio-visual-cross-modal-interaction-and-fusion` |
| 2.3 Temporal Modeling and Grounding | 21 | `source/sections/02-related-work.tex:25` | `sec:temporal-modeling-and-grounding` |
| 3 Method | 24 | `source/sections/03-method.tex:4` | `sec:method` |
| 3.1 Problem Definition | 25 | `source/sections/03-method.tex:7` | `sec:problem-definition` |
| 3.2 Overall Architecture | 27 | `source/sections/03-method.tex:13` | `sec:overall-architecture` |
| 3.3 Discriminative Semantic Prototype Optimization | 31 | `source/sections/03-method.tex:22` | `sec:discriminative-semantic-prototype-optimization` |
| 3.4 Class-Conditioned Gaussian Temporal Aggregation | 46 | `source/sections/03-method.tex:67` | `sec:class-conditioned-gaussian-temporal-aggregation` |
| 3.5 Decoupled Modality Interaction and Gated Fusion | 77 | `source/sections/03-method.tex:160` | `sec:decoupled-modality-interaction-and-gated-fusion` |
| 3.6 Joint Embedding, Training, and Inference | 93 | `source/sections/03-method.tex:208` | `sec:joint-embedding-training-and-inference` |
| 4 Experiments | 106 | `source/sections/04-experiments.tex:4` | `sec:experiments` |
| 4.1 Experimental Setup | 107 | `source/sections/04-experiments.tex:7` | `sec:experimental-setup` |
| 4.1.1 Datasets | 108 | `source/sections/04-experiments.tex:10` | `sec:datasets` |
| 4.1.2 Implementation Details | 115 | `source/sections/04-experiments.tex:25` | `sec:implementation-details` |
| 4.1.3 Evaluation Metrics | 118 | `source/sections/04-experiments.tex:34` | `sec:evaluation-metrics` |
| 4.1.4 Baselines | 120 | `source/sections/04-experiments.tex:40` | `sec:baselines` |
| 4.2 Quantitative Results | 122 | `source/sections/04-experiments.tex:46` | `sec:quantitative-results` |
| 4.3 Ablation Studies | 127 | `source/sections/04-experiments.tex:55` | `sec:ablation-studies` |
| 4.3.1 Effect of Core Components | 128 | `source/sections/04-experiments.tex:58` | `sec:effect-of-core-components` |
| 4.3.2 Temporal Aggregation Strategies | 133 | `source/sections/04-experiments.tex:67` | `sec:temporal-aggregation-strategies` |
| 4.3.3 Number of Gaussian Experts in CGTA | 138 | `source/sections/04-experiments.tex:76` | `sec:number-of-gaussian-experts-in-cgta` |
| 4.3.4 Optimization Objectives in DSPO | 143 | `source/sections/04-experiments.tex:85` | `sec:optimization-objectives-in-dspo` |
| 4.3.5 Interaction Branches and Gating in DMIF | 148 | `source/sections/04-experiments.tex:94` | `sec:interaction-branches-and-gating-in-dmif` |
| 4.3.6 Text Encoders | 153 | `source/sections/04-experiments.tex:103` | `sec:text-encoders` |
| 4.3.7 Fine-Grained Descriptions | 158 | `source/sections/04-experiments.tex:112` | `sec:fine-grained-descriptions` |
| 4.4 t-SNE Visualization | 164 | `source/sections/04-experiments.tex:124` | `sec:t-sne-visualization` |
| 5 Conclusion | 169 | `source/sections/05-conclusion.tex:4` | `sec:conclusion` |

标题和摘要取自 body 0–2；References 标题取自 body 171，32 条原文依次为 body 172–203。作者区不是 Word 原有内容：依照此前明确授权，从旧主稿识别并映射 7 位作者、顺序、单位、邮箱、ORCID 和 Jing Yang 的通讯作者标记。未迁移旧稿资助、致谢、贡献、利益冲突或作者简介。

## 4. 公式编号、位置及正文引用

行内与表内公式仍在所属段落或单元格内；全 244 项详见 audit/stage2/math-conversion.json，其中每个 M 编号包含原始 OMML、body 索引、局部数学索引和原生 LaTeX。以下为 32 个独立公式的位置。

| 原编号 | body | TeX 文件 | label | 当前 PDF 页 |
| --- | --- | --- | --- | --- |
| (1) | 34 | `source/equations/eq-01-visual-description-encoding.tex` | `eq:visual-description-encoding` | 4 |
| (2) | 35 | `source/equations/eq-02-audio-description-encoding.tex` | `eq:audio-description-encoding` | 4 |
| (3) | 37 | `source/equations/eq-03-initial-class-embedding.tex` | `eq:initial-class-embedding` | 5 |
| (4) | 40 | `source/equations/eq-04-separation-loss.tex` | `eq:separation-loss` | 5 |
| (5) | 42 | `source/equations/eq-05-ranking-loss.tex` | `eq:ranking-loss` | 5 |
| (6) | 44 | `source/equations/eq-06-prototype-objective.tex` | `eq:prototype-objective` | 6 |
| (7) | 49 | `source/equations/eq-07-visual-feature.tex` | `eq:visual-feature` | 6 |
| (8) | 50 | `source/equations/eq-08-audio-feature.tex` | `eq:audio-feature` | 6 |
| (9) | 52 | `source/equations/eq-09-feature-projection.tex` | `eq:feature-projection` | 6 |
| (10) | 54 | `source/equations/eq-10-attention.tex` | `eq:attention` | 6 |
| (11) | 57 | `source/equations/eq-11-conditioned-visual.tex` | `eq:conditioned-visual` | 6 |
| (12) | 58 | `source/equations/eq-12-conditioned-audio.tex` | `eq:conditioned-audio` | 6 |
| (13) | 61 | `source/equations/eq-13-class-queries.tex` | `eq:class-queries` | 6 |
| (14) | 63 | `source/equations/eq-14-gaussian-parameters.tex` | `eq:gaussian-parameters` | 7 |
| (15) | 64 | `source/equations/eq-15-gaussian-centers-widths.tex` | `eq:gaussian-centers-widths` | 7 |
| (16) | 66 | `source/equations/eq-16-gaussian-mask.tex` | `eq:gaussian-mask` | 7 |
| (17) | 67 | `source/equations/eq-17-normalized-mask.tex` | `eq:normalized-mask` | 7 |
| (18) | 69 | `source/equations/eq-18-expert-routing.tex` | `eq:expert-routing` | 7 |
| (19) | 71 | `source/equations/eq-19-enhanced-sequence.tex` | `eq:enhanced-sequence` | 7 |
| (20) | 73 | `source/equations/eq-20-direct-evidence.tex` | `eq:direct-evidence` | 7 |
| (21) | 75 | `source/equations/eq-21-direct-av-evidence.tex` | `eq:direct-av-evidence` | 7 |
| (22) | 80 | `source/equations/eq-22-branch-input.tex` | `eq:branch-input` | 7 |
| (23) | 82 | `source/equations/eq-23-intra-mask.tex` | `eq:intra-mask` | 7 |
| (24) | 83 | `source/equations/eq-24-inter-mask.tex` | `eq:inter-mask` | 8 |
| (25) | 85 | `source/equations/eq-25-masked-attention.tex` | `eq:masked-attention` | 8 |
| (26) | 87 | `source/equations/eq-26-branch-updates.tex` | `eq:branch-updates` | 8 |
| (27) | 90 | `source/equations/eq-27-three-way-gate.tex` | `eq:three-way-gate` | 8 |
| (28) | 91 | `source/equations/eq-28-gated-fusion.tex` | `eq:gated-fusion` | 8 |
| (29) | 95 | `source/equations/eq-29-semantic-projection.tex` | `eq:semantic-projection` | 8 |
| (30) | 97 | `source/equations/eq-30-similarity.tex` | `eq:similarity` | 8 |
| (31) | 101 | `source/equations/eq-31-alignment-loss.tex` | `eq:alignment-loss` | 8 |
| (32) | 104 | `source/equations/eq-32-calibrated-inference.tex` | `eq:calibrated-inference` | 8 |

所有独立公式使用 equation 的自动编号，没有用截图代替，也没有通过手写 tag 固定编号。正文中的公式、图表、章节引用转为 eqref/ref；文献用 cite，所有对应对象实际解析成功。详见 cross-reference-map.json、numbering-checks.json。

公式 (24) 的长掩码条件和 (27) 的嵌套门控表达式为适应双栏增加了分行与对齐；原有项、条件、次序及括号分组均保留。未引入新的中间变量、删项、改求和范围或改变矩阵维度。OMML 中默认的帽重音按帽处理，未误换为波浪；范数与拼接双竖线仍分别保留。

## 5. 图、表及原始数字映射

| 图号 | 原稿图片/图注 body | 实际文件与图环境 | 当前 PDF 页 |
| --- | --- | --- | --- |
| Fig. 1 | 12/13 | `source/figures/Introduction.pdf`；`figure-01-comparison.tex` | 3 |
| Fig. 2 | 29/30 | `source/figures/SGTG.pdf`；`figure-02-architecture.tex` | 5 |
| Fig. 3 | 166/167 | `source/figures/tsne-word.png`；`figure-03-tsne.tex` | 14 |

Fig. 1 和 Fig. 2 只各插入一次指定根目录 Introduction.pdf 和 SGTG.pdf 的原字节副本，未同时插入 DOCX 对应 PNG。Fig. 3 使用新 Word 的 image3.png 原字节，改保存名为 tsne-word.png；未使用旧稿的 tsne.png。三图未重画、未裁切、未上采样，原始字节及哈希见 asset-integrity.json。

| 表号 | 原表 body / 表题 body | 物理行 / 单元格 | TeX 文件 | 当前 PDF 页 |
| --- | --- | --- | --- | --- |
| Table 1 | 112/111 | 6 / 54 | `source/tables/table-01-class-splits.tex` | 9 |
| Table 2 | 124/123 | 22 / 277 | `source/tables/table-02-main-results.tex` | 10 |
| Table 3 | 130/129 | 6 / 69 | `source/tables/table-03-core-components.tex` | 11 |
| Table 4 | 135/134 | 6 / 69 | `source/tables/table-04-temporal-strategies.tex` | 11 |
| Table 5 | 140/139 | 7 / 82 | `source/tables/table-05-expert-count.tex` | 12 |
| Table 6 | 145/144 | 6 / 69 | `source/tables/table-06-prototype-objectives.tex` | 12 |
| Table 7 | 150/149 | 6 / 69 | `source/tables/table-07-interaction-gating.tex` | 12 |
| Table 8 | 155/154 | 5 / 56 | `source/tables/table-08-text-encoders.tex` | 12 |
| Table 9 | 161/160 | 6 / 69 | `source/tables/table-09-descriptions.tex` | 13 |

Table 1 的 10 列网格、纵向合并和分组表头完整保留；Tables 2–9 均保留三数据集 × S/U/HM/ZSL 四指标及全部原始行。每个物理单元格都有 `% CELL TxxRxxCxx` 标识。每格的原始字符串、数字 token、合并属性、LaTeX 和核验结果分别保存于 table-cell-migration.json 与 table-roundtrip.json。

本阶段仅做可读的 CAS 跨双栏三线表，保留 Word 已有加粗/斜体/上标；没有重新判定最优和次优，没有依据旧表或 Excel 替换数据。小数位（例如 10.30、24.50）和原始表示保留。更细的数值对齐、列距和浮动体位置属于后续精排。

逻辑插入点与 Word 顺序一致。CAS 浮动体会在后页顶部/底部显示，当前 t-SNE 图浮至第 14 页并位于参考文献版面上方；它在源码中仍位于 4.4 节，未改变文章内容次序。浮动体与相应叙述更紧密的版面安排尚待下一阶段。

## 6. 参考文献：已迁移内容与未完成元数据分开记录

本稿的 32 条真实参考文献已全部迁移，原作者文字、题名、年份、会议/期刊、页码、DOI 及版本备注均按 Word 保留。当前采用 natbib 数字引文 + 已安装 Elsevier elsarticle-num.bst + BibTeX。该数字样式是本阶段的工程选择，不是对尚未核验的期刊专属规则作结论。

为避免把旧稿同编号条目、不同版本或不相干文献混入，本阶段 references.bib 每条使用独立语义 key，并把完整原文保存在 note 字段。reference_order.tex 仅列原稿已有 32 个 key，保持原 [1]–[32] 序号，不额外搬入旧稿 49 条文献。

**可检索标记：BIB-META。** 这表示文献文本已经真实迁移，但 author/title/year 等结构化字段与版本核验未完成；不是虚构文献或未解决引文占位符。当前 main.blg 的 32 条 empty year 警告是 year 字段未单列，年份仍在 note 原文及 PDF 中真实显示。正文没有问号引文，也没有未解析 BibTeX key。不要把这些元数据警告描述为已消除。

旧库候选关系继承 audit/reference-mapping.json，以下给出新稿编号与本工程 key，供下一阶段定点核验。候选只表示身份匹配线索，不代表允许以旧版本覆盖新稿。

| 新稿编号 | 本工程 key | 旧库候选 / 未完成事项 |
| --- | --- | --- |
| [1] | `parida2020cjme` | 旧 key 3 为同一工作候选；本次仍保留新稿原文 |
| [2] | `mazumder2021avgzslnet` | 旧 key 4 为同一工作候选；本次仍保留新稿原文 |
| [3] | `mercea2022avca` | 旧 key 1 为同一工作候选；本次仍保留新稿原文 |
| [4] | `kurzendorfer2024clipclap` | 旧 key 2 为同一工作候选；本次仍保留新稿原文 |
| [5] | `mercea2022tcaf` | 旧 key 5 为同一工作候选；本次仍保留新稿原文 |
| [6] | `chen2023kda` | 旧 key 9；新稿 v2/2024 备注已保留，不能静默省略 |
| [7] | `mo2024easy` | 旧 key 12 为同一工作候选；本次仍保留新稿原文 |
| [8] | `tsai2019mult` | 旧库未匹配；已保留 Word 实际条目，结构化字段待核验 |
| [9] | `nagrani2021bottlenecks` | 旧库未匹配；已保留 Word 实际条目，结构化字段待核验 |
| [10] | `lin2025semiinn` | 旧库未匹配；已保留 Word 实际条目，结构化字段待核验 |
| [11] | `ma2026famav` | 旧库未匹配；已保留 Word 实际条目，结构化字段待核验 |
| [12] | `li2023pstp` | 旧库未匹配；已保留 Word 实际条目，结构化字段待核验 |
| [13] | `li2024tspm` | 旧库未匹配；已保留 Word 实际条目，结构化字段待核验 |
| [14] | `xiao2024trust` | 旧库未匹配；已保留 Word 实际条目，结构化字段待核验 |
| [15] | `kim2025qatiger` | 旧库未匹配；已保留 Word 实际条目，结构化字段待核验 |
| [16] | `chao2016gzsl` | 旧库未匹配；已保留 Word 实际条目，结构化字段待核验 |
| [17] | `chen2020vggsound` | 旧 key 34 为同一工作候选；本次仍保留新稿原文 |
| [18] | `soomro2012ucf101` | 旧 key 35；新技术报告与旧 arXiv 载体不同 |
| [19] | `heilbron2015activitynet` | 旧 key 36 为同一工作候选；本次仍保留新稿原文 |
| [20] | `kingma2015adam` | 旧 key 37；新 ICLR 2015 与旧 arXiv 2014 不同 |
| [21] | `frome2013devise` | 旧 key 38 为同一工作候选；本次仍保留新稿原文 |
| [22] | `akata2016ale` | 旧 key 39 为同一工作候选；本次仍保留新稿原文 |
| [23] | `akata2015sje` | 旧 key 40 为同一工作候选；本次仍保留新稿原文 |
| [24] | `xu2020apn` | 旧 key 41 为 IJCV 2022 扩展版，不替换新 NeurIPS 2020 条目 |
| [25] | `xian2019fvaegan` | 旧 key 42 为同一工作候选；本次仍保留新稿原文 |
| [26] | `hong2023hyperbolic` | 旧 key 7 为同一工作候选；本次仍保留新稿原文 |
| [27] | `maaten2008tsne` | 旧 key 46 为 2019 理论文献，不替换新 2008 原始 t-SNE 文献 |
| [28] | `li2024stft` | 旧 key 43 为同一工作候选；本次仍保留新稿原文 |
| [29] | `yang2025mstr` | 旧 key 14 为同一工作候选；本次仍保留新稿原文 |
| [30] | `li2025mdst` | 旧 key 44 为同一工作候选；本次仍保留新稿原文 |
| [31] | `yang2026sacma` | 旧 key 45 为同一工作候选；本次仍保留新稿原文 |
| [32] | `ma2026sgpan` | 旧库未匹配；已保留 Word 实际条目，结构化字段待核验 |

## 7. 原稿待确认事项与未成功迁移内容

**本阶段未发现未成功迁移的正文、公式、表格、图片或文献条目；未使用无法解析的公式截图/占位文本。** 仍需作者确认或后续处理的事项如下，均与内容遗漏区分。

| 标识 | 来源位置 | 问题 / 当前处理 |
| --- | --- | --- |
| FIG-TEXT-01 | SGTG.pdf；正文 (20)–(21)、(27)–(28)；body 30 图注 | 指定图显式画出两路 λ1/λ2，文字包含第三路直接证据/λ3。保留指定图与全部三路公式、图注；不自行判断或重画 |
| REF-AVFS-01 | Table 2 的 AVFS 行 | 原稿该行没有引用编号；不补上旧 key 6，不增加第 33 条文献 |
| TEXT-COUNT-01 | body 121，4.1.4 Baselines | 原文称 14 种 audio-visual GZSL 方法，但随后名称列举有 13 项，表中另有 AVFS。仅记录疑似列举不全，原句原样保留 |
| BIB-META | references.bib / 上节映射 | 32 条已迁移但未拆分结构化字段；版本冲突与未匹配项保留，需后续核验 |
| FIG-QUALITY-03 | Word Fig. 3，1141×835 PNG | 已保留同一结果原图，未重画或伪造高清版；最终排版尺寸与清晰度待精排 |
| DECLARATIONS | 原稿未有相关独立章节 | 不编写“无利益冲突”等声明，不复制旧稿资助、致谢或 CRediT |
| JOURNAL-GUIDE | inventory.md 阶段一访问记录 | 专属 Guide for Authors 未核验；本阶段不宣称满足全部投稿要求、不删摘要、不额外写 Highlights |

除上述已记录的原稿问题与文献元数据外，没有为了消除编译错误而删除内容、公式、引文、表格行或指标。

## 8. 本地编译、修复与当前日志

实际使用 VOA Windows TeX Live 2026 中的 XeLaTeX：

`C:\Users\admin\texlive\2026\bin\windows\xelatex.exe`

构建工作目录：`C:\Users\admin\Documents\GitHub\WH\论文方案\SGTG_InformationFusion\source`。

实际构建参数：`latexmk.exe -g -xelatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error -outdir=build -auxdir=build main.tex`。

最后一次成功构建：2026-09-23 12:33:48–12:33:53（UTC+08:00），退出码 0。main.log 明确记录 XeTeX / format=xelatex；main.blg 明确记录 BibTeX 0.99e、elsarticle-num.bst 和 references.bib。XDV 后经 xdvipdfmx 生成 PDF 是此 XeLaTeX 链的正常组成，不是改用其他正文引擎。

| 问题类别 | 实际处理或状态 |
| --- | --- |
| 模板兼容 | CAS 2.4 longmktitle 使用旧 expl3 名称 vbox_unpack_clear:N，本地 2026 内核未定义；在新 cas-xetex-compat.sty 中添加仅在缺失时生效的别名，指向本地已存在的 vbox_unpack_drop:N。原 CAS 文件完全未改 |
| 文字字体 | CAS 的 T1 文本字体对 Unicode 引号、撇号、破折号产生缺字；改为相同字符的原生 TeX 命令，未替换文本含义或字体安装 |
| 双栏公式排版 | (24)、(27) 增加原生多行对齐；未缩为图片、删项或改写公式 |
| 环境依赖 | 无阻止构建的缺失依赖；未安装、升级 TeX 或字体，没有改全局 PATH/用户 VS Code 设置 |
| 本阶段文献问题 | 32 个 year 字段未结构化警告；全部真实文献和引文均已显示，后续继续处理 |
| 当前未解析引用/缺字 | main.log 中未定义引用/引文 0，缺字 0 |
| 当前版式警告 | 1 个标题区 overfull hbox（123.62721pt）、3 个 hyperref empty-anchor 警告、61 个 underfull 盒子提示；未伪称零警告 |

标题区 overfull 提示与原模板示例同类；实际第一页已视觉检查，未见可见文字越界或裁切，但仍保留为后续模板/版式核验项。正文公式与表格的 overfull 提示已消除。15 页均已渲染并逐页检查图、表、公式、段落与参考文献的存在性、重叠/裁切及可读性；当前预览在 audit/stage2/recheck-20260923-123348/renders/。本阶段不把退出码 0 等同于最终排版验收。

## 9. 纯格式转换及超出转换范围的变化记录

| 变化 | 性质与边界 |
| --- | --- |
| 标题 Word 换行改空白，Abstract/Keywords 显示标签交给 CAS | 格式转换；完整标题、摘要、关键词文字保留 |
| 标题/公式/图表手写号转自动编号及 label/ref/eqref/cite | 格式与维护性转换；实际编号映射核验通过 |
| 原生 OMML 转数学环境，包括线性分式改可编辑分式 | 数学排版转换；原始对象保存，可逐项追溯 |
| 双栏长公式 (24)、(27) 分行；段落 emergency stretch 增加 | 格式修复；不改词语和数学项 |
| 字符转义及 T1 字体兼容命令 | 相同可见字符的表示转换；未删除引号/破折号 |
| 表格转 tabular*/multirow/multicolumn；图转 figure* | 可编辑格式转换；原图字节、逐格数字和内容保留 |
| 新增项目兼容 shim 和 VS Code recipe 选择 | 仅项目级工程配置，不改原模板或全局环境 |
| 7 作者、单位、邮箱、ORCID、通讯作者 | 经前阶段明确授权，按旧稿作者区补入 CAS；是 Word 之外的来源，已单独标明，不增删作者 |
| 参考文献临时放在 note 字段 | 保真保存真实原文而非最终规范元数据；BIB-META 明确标记，不冒充已核验 |

没有学术改写、润色、扩写、缩减分析、重算数字、改方法定义或改结论。具体兼容/格式修改记录及修改前文件在 format-changes.json、before-layout/，原文和生成初始稿的审计台账同时保留。

## 10. 维护方式与审计入口

今后维护以 source 内的实际 TeX 为准，编辑对应 sections/equations/tables/figures 文件即可。每个块/单元格的来源标记保持不变便于复核。scripts/stage2_migrate.py 与 stage2_content.py 保存首次转换逻辑，仅用于审计；为防覆盖当前人工核对后的稿件，生成器在检测到既有 main.tex 时拒绝直接再次运行。它们不是日常复编译入口。

日常复编译运行 scripts/build_local.py，或在 VS Code 打开本项目并选择已有 latexmk (xelatex) recipe。项目级设置明确指定该 recipe，避免扩展默认第一项使用 -pdf。未修改用户级配置。当前源文件无需 Pandoc、旧 Word 或旧 TMM 工程才能编译。

核心核验文件：verification-summary.json、prose-roundtrip.json、table-roundtrip.json、front-caption-heading-checks.json、numbering-checks.json、body-map.json、math-conversion.json、reference-ledger.json、input-dependencies.json、source-integrity-final.json。它们均位于 audit/stage2/。

## 11. Git 与收尾状态

只读检查：真实根目录 C:/Users/admin/Documents/GitHub/WH，当前 main，上游 origin/main；HEAD 保持 10ef224b043957319d772a1de9ecd3406366e259。暂存区为空，已跟踪文件差异为空，仅本项目为未跟踪新增目录。详见 audit/stage2/git-final.json。

本阶段没有 git add、commit、push、fetch、remote 变更、分支切换、reset、clean 或合并操作。此前确认远程为 PUBLIC 的公开风险仍保留，本阶段也未请求或执行任何公开上传。

完整初稿、PDF、日志、content_map 和核验资料均保存在 VOA 本项目。源包归档、正式投稿格式精排、文献元数据整理和最终 Git 同步不在本阶段执行。

## 12. 本次续执行复核与页眉/页码补齐

2026-09-23 再次连接 VOA 后发现本项目已经包含完整第二阶段源码和初编译产物。因此沿用本工程，不重新运行生成器，不覆盖已核对的正文。当前实际结果以本节及 audit/stage2/recheck-latest.json 为准；较早的 verification-summary.json 等保留为历史记录。

本次直接重新读取当前 Word OOXML、源码、表格和公式台账，以 scripts/recheck_stage2.py 独立复核，并使用同一 VOA 工具链加 -g 强制构建，而不是仅接受“目标已是最新”的缓存结果。-g 只要求重编译，不清理源文件。

复核结果：3,343 项检查通过，0 项失败。覆盖 46 个原文件哈希、205 个来源块、244 个原始数学对象、74 个正文/列表片段、814 个表格单元格及数字串、32 个编号公式、3 张图片、32 条文献、73 个标签和全部引文编号；实际输入没有项目外的旧稿或 Word 依赖。

### 12.1 辅助内容映射更正：HEADER-PAGE-01

| 原 Word 位置 | 原内容 | 本项目映射 |
| --- | --- | --- |
| word/header1.xml | SGTG \| Audio-Visual Generalized Zero-Shot Learning | source/frontmatter.tex 的 shorttitle，竖线用 textbar 等值转义；页眉位置服从 CAS |
| word/footer1.xml | PAGE 自动页码域 | CAS 自动页码；不复制 Word 的旧页码值 |

前次正文盘点没有完整说明此运行页眉和简单页码域。本次已补齐：只将原 shorttitle 的缩写 SGTG 改为 Word 的完整页眉文字，没有修改标题、摘要、正文、公式、表格数字、图注或文献。修改前 frontmatter 和来源映射保存在 audit/stage2/recheck-20260923-123204/。首次复核发现该 PAGE 域时的失败记录保留；完成明确映射后重新复核全部通过。

### 12.2 当前构建及页面检查

最新本地构建于 2026-09-23 12:33:48–12:33:53 完成，退出码 0，明确运行 XeLaTeX、BibTeX 和必要重编译。当前 PDF 为 15 页，1,723,520 字节，SHA-256 为 912ebdb1a1abba4a07d91a49c0eef25d6aa440099a897e89233cffb63840b7d3。

最新控制台和原始日志快照位于 audit/stage2/recheck-20260923-123348/：build-console.log、main.log、main.blg、main.bbl、main.aux；逐页视觉记录为 visual-review.md，当前 15 页预览在 renders/。本次已逐页检查当前 PDF，未见缺页、正文/图表公式裁切或相互覆盖。表格列距、长标题留白、个别公式编号另起行、t-SNE 浮至参考文献区域和尾页双栏平衡保留给下一阶段精排。

当前仍有 1 个 overfull、3 个 empty-anchor、61 个 underfull 和 32 个 BIB-META 对应的 empty-year 警告；缺字和未定义引用均为 0。文献原文已完整迁移，但结构化字段与版本核验未完成，不能据此宣称参考文献已最终规范化。

本次仍未执行任何 Git 暂存、提交或推送；原稿保护、作者确认事项及正式期刊要求待核验的边界不变。

## 13. 第三阶段更新：作者与参考文献（2026-09-23）

本节覆盖上文第二阶段的作者/文献临时状态；章节、图表、公式的来源映射仍有效。完整新报告：author_reference_review.md；逐处引用表：citation_map.csv。

本阶段重新读取旧 KA_GZSL_TMM 作者源码，核验 7 位作者顺序、单位对应、邮箱、ORCID 与 Jing Yang 通讯标记；以 CAS 作者脚注迁移原文明确的 Member/Fellow 身份。没有复制基金、致谢或论文专属声明。新 Word 无独立作者区，未发现可列出的新旧署名冲突，但新稿适用性、共同一作/共同通讯仍须作者确认。

32 条文献已由 note 整段保存改为结构化 BibTeX 字段。原稿 67 个引用组（69 个文献目标出现记录）均已映射到具体身份和 key；有引用的 33 个来源单元身份核对无错配。CSV 另列 1 个没有引用标识的 AVFS 问题，不新增未经确认的第 33 篇。

main.tex 已停用 reference_order.tex；后者仅保留退役说明。编号由 BibTeX 依据实际引用顺序生成：原 [27] 为当前 [32]，原 [28]–[32] 分别为当前 [27]–[31]，其余对应不变。不是把旧库同编号条目搬入新稿。

04-experiments.tex 只将 body 117 的两个引用端点写法改为三个原文献 key 的单次 cite，覆盖原 [3]–[5] 全部文献；可逆替换后恢复原文件哈希（保留 Windows CRLF）。其他正文措辞、公式、表格和原图未改。全部 46 个原始材料、其余 66 个既有 source 文件哈希不变；73 个章节/公式/图表标签编号核验通过。

仍有 YEAR-CONVENTION-07（2024/2025 口径）、BIB-PAGES-ADAM（未取得会议页码）及 REF-AVFS-01（缺引文）记录。DeViSE 页码按 Word/旧库一致值保留，官方导出未提供独立页码确证；没有编造字段。CVF/IEEE 的页码差异、姓名边界修复、DOI resolver URL 去重和所有来源均在 audit/stage3/reference-decisions.json。

最新成功构建：2026-09-23 13:46:47–13:47:01（UTC+08:00），VOA 本地 XeLaTeX + BibTeX，退出码 0，15 页。日志位于 audit/stage3/build-20260923-134647/。当前缺字、未解析引文、未解析交叉引用、empty year 均为 0；保留 1 个 Adam empty pages、1 个标题区 overfull、5 个 empty-anchor、61 个 underfull 提示。

本阶段没有提交或推送 GitHub。当前 stage-state.json、README.md 与 author_reference_review.md 为最新阶段入口。第二阶段的临时文献说明、旧 PDF 哈希和旧日志是历史记录，不应当作当前状态。

## 第四阶段更新：图表精排（2026-09-23，当前版本）

当前仍为 source/main.tex，CAS-DC 双栏；图表样式统一在 source/sgtg-floats.sty。完整说明见 figure_table_style.md，待确认项见 figure_table_remaining.md。

9 张表全部保留为原生 tabular*，使用分组表头和不改变精度的小数点对齐。table_audit.csv 对当前 Word 的 814 个物理格逐格核验；实际 PDF 的 51 个数字数据行、608 个数字字串全部一致。保留 16 个表内原生数学对象及原有逐格强调，不新增排名标记。

两张 PDF 保持原字节，显式采用 pagebox=mediabox 后仅裁显示空白；图1裁边43/99/20/29 bp，图2裁边12/11/13/51 bp，顺序左/下/右/上。原Word第三图保持1141×835 PNG，不重画、不裁切或上采样。

仅调整图1锚点至body[5]之后、图3锚点至Table9之后，保证跨栏浮动体靠近相关说明；其余正文顺序、措辞、实验数值和32个独立公式不变。图注/表题12项核对一致，第三阶段32个文献编号保持不变。

当前图页码：Fig.1第3页、Fig.2第5页、Fig.3第13页。表页码：Table1第9页，Table2第10页，Tables3–4第11页，Tables5–8第12页，Table9第13页。图3与4.4节起始同页，不再位于参考文献区域。

上一阶段的固定TeX行号属于历史定位；经过样式调整可能变化。当前按稳定的DOCX body/CELL标识定位，table_audit.csv记录当前目标文件与原稿行列；当前自动标签页码在audit/stage4/positions.json。

最新PDF为15页，1,730,559字节，SHA-256为67aa621e0613b10730608a82894aa8f826e326e50a5ce899a34a5954603f5a07。2026-09-23 15:08:18–15:08:33在VOA运行XeLaTeX+BibTeX，退出码0；日志见audit/stage4/build-20260923-150818/。

最终15页有视觉检查覆盖；原始46个来源文件哈希不变。当前仍有既有标题/锚点/underfull及Adam页码提示；新稿粗体含义不明确的10格均保留。旧稿成稿PDF未找到，旧表样式仅据已实际读取源码，不声称完成旧PDF对照。

本阶段未执行Git暂存、提交或推送。当前阶段状态以stage-state.json与audit/stage4/verification.json为准。

## 最终阶段补充（2026-09-23，r4交付）

本节覆盖此前章节中的“当前编译”路径与页码，但不删除历史迁移记录。最终主入口source/main.tex，命名PDF为项目根SGTG_InformationFusion.pdf（15页），实际来源source/build-final-20260923-r4/main.pdf。扁平源目录submission_flat独立XeLaTeX/BibTeX构建通过，逐页文字、bbl及15页渲染像素与主工程一致。

最终没有改变各节正文分文件或公式/表格语义标签；74段落/列表单位、29标题、244数学对象、32独立式、814表格物理格、608渲染数字、12图注表题和32文献均重新核对通过。67组引文的69个目标身份无错配；AVFS缺引文与2项元数据限制仍明确保留。

最终图页码：Fig.1第2页，Fig.2第5页，Fig.3第13页。表页码：Table1第9页；Table2/3第10页；Table4/5第11页；Table6/7/8第12页；Table9第13页。caption文字、图像字节、表格数字与强调未改变。

纯排版变更：取消不必要的longmktitle，使引言接在首页摘要后；用项目局部包将误导的模板submitted页脚改为prepared；参考文献按完整段落分页；拒收balance试排的输出例程副作用，最终不使用balance。原CAS文件、数学含义和科学措辞未改。

未使用的演示template.tex、reference_order.tex和cas-model2-names.bst移入本地audit/stage5/archived-unused；保留版权和许可，不混入最终稿或投稿包。详细日志、视觉与全文核验见QA_REPORT.md；待确认事项见TODO.md。GitHub公开上传因缺少明确公开授权而暂停，实际本地提交状态见git_sync_status.json。
