# SGTG → Information Fusion：第一阶段盘点与排版方案

核验日期：2026-09-23（VOA 本地时区 UTC+08:00）。设备：DESKTOP-VOA285C。

项目唯一工作目录：`C:\Users\admin\Documents\GitHub\WH\论文方案\SGTG_InformationFusion`。

阶段边界：本阶段只完成实际连接、材料/内容/环境盘点、模板兼容性测试和方案。未开始全文 LaTeX 转换，未生成新论文成稿 PDF，未打包投稿源文件，未暂存、提交或推送 Git；模板测试 PDF 不是论文交付物。

初次检查时目标目录不存在，随后在指定“论文方案”目录内新建本项目。后续阶段继续使用本目录。原始 Word、两张 PDF、模板目录及旧工程均按只读来源处理；仅在本项目中保存审计文件和测试副本。

## 1. 材料清单与来源优先级

| 材料 | 实际位置 | 检查结果 / 用途 |
| --- | --- | --- |
| 新论文 Word | `C:\Users\admin\Documents\GitHub\WH\论文方案\SGTG_English_Translation.docx` | 可读；1,460,054 字节；正文、公式含义、实验设置与数字的唯一主来源 |
| 引言图 | `C:\Users\admin\Documents\GitHub\WH\论文方案\Introduction.pdf` | 可读；690,580 字节；1 页、未加密；已提取文字并渲染检查内容 |
| 架构图 | `C:\Users\admin\Documents\GitHub\WH\论文方案\SGTG.pdf` | 可读；682,308 字节；1 页、未加密；已提取文字并渲染检查内容 |
| CAS 模板 | `C:\Users\admin\Documents\GitHub\WH\论文方案\els-cas-templates` | 实际为目录；README、示例、类、宏包、文献样式及说明文件均已检查 |
| 旧工程 | `C:\Users\admin\Documents\GitHub\WH\论文方案\KA_GZSL_TMM` | 主文、独立补充材料、文献库、图文件均已定位；只复用作者信息、匹配文献和表格表现形式 |
| 同名顶层旧 tex | `C:\Users\admin\Documents\GitHub\WH\论文方案\KA-GZSL_TMM.tex` | 与旧工程内主 tex 字节完全相同；依赖路径应以旧工程内主文件为准 |

两张指定 PDF 的 MediaBox 均为 `[0, 0, 841.92, 595.32]` pt。不能因文件同名而改用旧工程 `figure/Introduction.pdf` 或 `figure/KA-GZSL.pdf`。

46 个主来源文件的绝对路径、大小、修改时间及 SHA-256 已保存到 `audit/source-manifest.json`。其中 Word SHA-256 为 `3d15426075f1a5b31e8628ee0fa4ee4c0be124dc4ad107607a7cf11b11e2d4bf`。

## 2. Word 内容结构与对象盘点

检查方法：直接读取 DOCX ZIP 内所有相关 OOXML 部件及关系，统计嵌套表格段落、原生公式、绘图、文本框、OLE/嵌入对象、脚注/尾注、页眉页脚和修订；不是仅用普通段落接口提取正文。

题目：**SGTG: Semantic-Guided Gaussian Temporal Grounding for Audio-Visual Generalized Zero-Shot Learning**。原 Word 在 Grounding 与 for 之间是显式换行；普通文字拼接所得 Groundingfor 不是原稿拼写错误，迁移时应保留合理空白。

| 对象 | 实测数量与说明 |
| --- | --- |
| 顶层内容 | 205 个 body 元素：195 个直接段落、9 张表和 1 个节属性元素 |
| 全部段落 | document.xml 共 1,009 个段落（含单元格），其中 981 个含文字；页眉、页脚另各 1 段 |
| 正文结构 | 5 个一级正文章节，另有 References；摘要约 272 个空白分词，3 个关键词（不是期刊官方字数核验） |
| 数学对象 | 244 个原生 `m:oMath`；其中 32 个带编号独立公式、196 个其他段落内数学对象、16 个表格内数学对象 |
| 公式段容器 | `m:oMathPara` 为 0，但独立公式 (1)–(32) 实际存在，不能据此漏掉公式 |
| 表格 | 9 张、70 个物理行、814 个物理单元格；已保留合并属性和逐格文本 |
| 图片 | 3 个 drawing、3 个嵌入 PNG；均已解析关系并原字节提取到审计目录 |
| 其他对象 | 未发现文本框、VML/pict、OLE 对象、嵌入文件、altChunk、脚注/尾注引用、批注部件或修订插入/删除 |
| 文献 | References 中 32 条，编号 [1]–[32]；引文为静态文字，主文未发现 `w:instrText` 引文字段 |

完整层级、表格、图片关联、样式及 ZIP 部件在 `audit/word-structure.json`；原始 document.xml 在 `audit/source-document.xml`。线性文本仅作查找，不代替 OMML 的上下标、分式、矩阵及符号含义。本阶段没有宣称完成 Word 全文逐页视觉核对。

### 2.1 章节清单

- **1 Introduction**。
- **2 Related Work**：2.1 Audio-Visual Generalized Zero-Shot Learning；2.2 Audio-Visual Cross-Modal Interaction and Fusion；2.3 Temporal Modeling and Grounding。
- **3 Method**：3.1 Problem Definition；3.2 Overall Architecture；3.3 Discriminative Semantic Prototype Optimization；3.4 Class-Conditioned Gaussian Temporal Aggregation；3.5 Decoupled Modality Interaction and Gated Fusion；3.6 Joint Embedding, Training, and Inference。
- **4 Experiments**：4.1 Experimental Setup（4.1.1 Datasets、4.1.2 Implementation Details、4.1.3 Evaluation Metrics、4.1.4 Baselines）；4.2 Quantitative Results；4.3 Ablation Studies；4.4 t-SNE Visualization。
- **4.3 的七项消融**：4.3.1 Effect of Core Components；4.3.2 Temporal Aggregation Strategies；4.3.3 Number of Gaussian Experts in CGTA；4.3.4 Optimization Objectives in DSPO；4.3.5 Interaction Branches and Gating in DMIF；4.3.6 Text Encoders；4.3.7 Fine-Grained Descriptions。
- **5 Conclusion**；随后为 **References**。

未发现独立的作者区、资助、致谢、作者贡献或利益冲突章节；不能据旧稿自动填写这些新稿声明。

### 2.2 公式清单

编号连续为 (1)–(32)，未发现编号断档。对应关系：

| 公式编号 | 内容 / 后续排版核验重点 |
| --- | --- |
| (1)–(3) | 视觉/听觉描述编码、拼接与归一化初始类别嵌入 |
| (4)–(6) | 最近邻分离损失、三重关系的间隔排序损失、单位球约束下联合优化；不得简化求和范围 |
| (7)–(12) | 冻结特征编码、投影与位置编码、注意力、两路类别条件化序列 |
| (13)–(18) | 类别查询、高斯参数、中心和宽度、高斯权重与时间归一化、自适应专家路由 |
| (19)–(21) | 增强序列、直接时序证据及两模态直接证据融合 |
| (22)–(26) | 特殊 token 输入、模态内/间掩码分段定义、带掩码注意力和残差层更新 |
| (27)–(28) | 三路门控权重及加权融合，必须保留第三路证据项 |
| (29)–(32) | 语义投影、带温度的余弦得分、训练对齐损失、seen 类校准推理 |

`audit/math-inventory.json` 保存全部 244 个对象的原始 OMML、body 索引与局部索引。后续以此逐项对照 LaTeX，尤其核验范数、转置、上下标、负无穷掩码及长分式。

### 2.3 表格清单

| 编号 | 原表内容 | 物理行数 / 最大单元格列数 |
| --- | --- | --- |
| Table 1 | Class splits of the three benchmark datasets | 6 / 10 |
| Table 2 | Performance comparison on the three benchmark datasets (%) | 22 / 13 |
| Table 3 | Ablation results for the core components (%) | 6 / 13 |
| Table 4 | Comparison of temporal aggregation strategies (%) | 6 / 13 |
| Table 5 | Effect of the number of Gaussian experts E in CGTA (%) | 7 / 13 |
| Table 6 | Class embedding optimization objectives in DSPO (%) | 6 / 13 |
| Table 7 | Interaction branches and gating in DMIF (%) | 6 / 13 |
| Table 8 | Text encoders (%) | 5 / 13 |
| Table 9 | Fine-grained description strategies (%) | 6 / 13 |

Table 2 包括 19 个对比方法和 SGTG。Tables 2–9 必须完整保留三组数据集及各组 S、U、HM、ZSL 四列；不能为了缩表删除指标或数据集。Table 1 的合并表头及整数划分单独处理。

逐格原文字串、数字 token 和合并属性保存在 `audit/table-cell-ledger.json`，共 814 格。禁止重算、预测或修订实验数值，也不读取实验结果.xlsx 替代本次指定 Word。显示精度以 Word 为准，不擅自把某个指标的最优/次优状态沿用旧论文。

新稿 SGTG 主结果基准（按 S/U/HM/ZSL）：VGGSound 为 35.08/16.87/22.78/17.65；UCF 为 85.49/46.97/60.63/50.38；ActivityNet 为 47.28/23.61/31.49/23.96。这里只建立迁移对照，不对结果作修改。

### 2.4 图片清单与实际内容检查

| 图 | Word 内来源 | 后续实际使用来源 |
| --- | --- | --- |
| Fig. 1 | body 12，rId11，image1.png，2100×1265 | 指定根目录 Introduction.pdf 原文件副本；内容已确认为三类 AVGZSL 框架比较 |
| Fig. 2 | body 29，rId12，image2.png，2100×1351 | 指定根目录 SGTG.pdf 原文件副本；内容已确认为 CLIP/CLAP、高斯专家和模态交互架构 |
| Fig. 3 | body 166，rId13，image3.png，1141×835 | 从新稿 DOCX 按原字节提取；三数据集×三种特征的 t-SNE 图；不能换成旧稿 tsne.png |

Fig. 3 已原字节保存为 `audit/visuals/image3.png`，SHA-256 为 `312cb01a1272752311eb7920359e8567cbea7b8683ed5f06d0f2bc40eccdaa9d`。两张指定 PDF 的渲染预览及三张 Word 原图均位于 `audit/visuals/`；预览不是替代投稿图片。

**待作者确认的图文一致性：** 指定 SGTG.pdf 中能明确看到两路输出及 λ1、λ2，未显式画出正文 (20)–(21)、(27)–(28) 和图注所述的直接证据第三分支 / λ3。这可能是示意简化，也可能是版本差异；目前不判定数学错误，不改图、不删正文第三路。最终严格使用指定图前应确认。

Fig. 3 的原始像素为 1141×835。后续需按实际排版宽度检查清晰度；尚未核验期刊分辨率阈值，不把它武断判为不合格。若需要更清晰版本，应由作者提供同一结果的原始高分辨率/矢量图，不重画、不替换实验内容。

## 3. 旧 KA_GZSL_TMM 工程识别

真正主文件：`C:\Users\admin\Documents\GitHub\WH\论文方案\KA_GZSL_TMM\KA-GZSL_TMM.tex`（63,198 字节），含 documentclass、begin/end document、完整正文、作者区和 `bibliography{sec/references}`。

独立补充材料：同目录 `KA-GZSL_TMM_Supp.tex`（15,048 字节），不是主文输入文件。文献库：同目录 `sec\references.bib`（40,051 字节），共 49 个条目。

主文明确使用 `IEEEtran` 文档类和 `IEEEtran` 文献样式；工程内没有自带 IEEEtran.cls/bst。已通过 kpsewhich 找到发行版中的 `c:/Users/admin/texlive/2026/texmf-dist/tex/latex/ieeetran/IEEEtran.cls` 和 `c:/Users/admin/texlive/2026/texmf-dist/bibtex/bst/ieeetran/IEEEtran.bst`。这些仅说明旧工程依赖，不用于新稿。

在旧工程及 WH 仓库相关文件搜索中未找到对应的已编译主文 PDF 或 `.bbl`。`KA_GZSL_TMM\figure\KA-GZSL.pdf` 是模型插图，不能冒认为论文 PDF。故旧稿的作者/文献/表格按 tex、bib 核验，旧整篇 PDF 视觉对照尚不可做；这不阻止先按源码设计排版。

### 3.1 作者区（按旧主 tex，保持顺序）

| 顺序 | 作者 | ORCID | 单位代码 / 邮箱 |
| --- | --- | --- | --- |
| 1 | Hu Wang | 0009-0008-1596-5311 | A；gs.wanghu24@gzu.edu.cn |
| 2 | Jing Yang，通讯作者 | 0000-0003-1915-9487 | A+B；jyang23@gzu.edu.cn |
| 3 | Xiaoli Ruan | 0000-0002-7623-3308 | A；xlruan@gzu.edu.cn |
| 4 | Yuling Chen | 0000-0002-8674-8356 | A；ylchen3@gzu.edu.cn |
| 5 | Xinru Yi | 0009-0007-4224-4774 | C；cme.xryi23@gzu.edu.cn |
| 6 | Chengjiang Li | 0000-0002-1864-2023 | D；cjli3@gzu.edu.cn |
| 7 | Minyi Guo | 0000-0003-0034-2302 | A+B；myguo@gzu.edu.cn |

A：State Key Laboratory of Public Big Data, Guizhou University, Guiyang 550025, China。
B：Department of Computer Science and Engineering, Shanghai Jiao Tong University, Shanghai 200240, China。
C：School of Mechanical Engineering, Guizhou University, Guiyang, Guizhou 550025, China。
D：School of Management, Guizhou University, Guiyang 550025, China。

按要求将上述作者信息映射到 CAS 的 author / affiliation / cormark / ead 结构；不增加、删除或调序作者，不复制 IEEE 页眉和会员头衔排版。单位及邮箱按旧文件记录，未作外部真实性更新。旧 thanks 中的资助项目不迁移，新稿资助、致谢、贡献与利益冲突须另行确认。

### 3.2 表格表现形式

旧主文有 5 个表格环境；已读取代表性的全方法比较表和核心组件消融表。其特点是 booktabs 三线表、multirow/multicolumn 数据集组头、S/U/HM/ZSL 分组、最优加粗、次优下划线、自身方法行浅灰强调；数值列主要为 c 列，并非现成的小数点对齐方案。

拟仅借鉴组头、留白与数值强调。新稿采用 CAS 版心，必要时用 dcolumn 或已安装 siunitx 实现小数点对齐；保留原数字字面值。不要照抄旧表的排名、年份标注、行底色、IEEE 双栏尺寸或旧数据，也不默认用缩放把全部表缩到难读。

### 3.3 参考文献候选匹配与禁止替换项

已逐项比较新稿 32 条文献和旧库 49 条文献，候选映射见 `audit/reference-mapping.json`。找到 20 个同一工作候选，其中包含版本/载体差异；另 11 条旧库无同一文献，1 条 APN 有不同扩展版本但不能直接复用。

候选“新编号→旧key”：1→3，2→4，3→1，4→2，5→5，6→9，7→12，17→34，18→35，19→36，20→37，21→38，22→39，23→40，25→42，26→7，28→43，29→14，30→44，31→45。此映射不是已完成的最终 bib。

| 项目 | 发现与处理边界 |
| --- | --- |
| 新 [18] UCF101 | 新稿技术报告、旧库 arXiv：同一工作但载体不同；保留新稿身份，不机械覆盖 |
| 新 [20] Adam | 新稿 ICLR 2015，旧库 arXiv 2014；年份及载体不能照抄 |
| 新 [24] APN | 新稿 NeurIPS 2020 的 zero-shot 论文；旧 key41 是 IJCV 2022 Any-Shot 扩展版，不能当成同一条直接替换 |
| 新 [27] t-SNE | 新稿 van der Maaten / Hinton 2008；旧 key46 是 Linderman / Steinerberger 2019，不对应 |
| 新 [6] KDA | arXiv 标识一致，但新稿注明 v2 2024，应保留该版本信息 |
| Table 2 的 AVFS | 新稿该行没有引用编号，32 条文献中也未列该 AVFS 工作；旧 key6 有候选，不擅自添加新引用，待作者确认 |

后续只建立新稿实际引用对应的条目；未匹配项按新稿记录建立并核验，不把旧 49 条全部导入。不得用旧引用编号替换新编号而不核对其文献身份。本阶段未联网改写任何参考文献元数据。

## 4. 本地模板检查与版式方案

模板 README 为 Version 2.4；cas-sc.cls / cas-dc.cls 的实际 RCS 标记为 2.4、2024/05/04。已检查 README、manifest、两个 template 和 sample、cas-common.sty、cas-model2-names.bst，以及 doc/elsdoc-cas.tex / PDF 等说明。

本包包含单栏 cas-sc、双栏 cas-dc、cas-common.sty、cas-model2-names.bst、示例 cas-refs.bib、figs 和 thumbnails。文档目录另有 pdfwidgets.sty、rvdtx.sty、glyphtounicode.tex；它们用于文档，不应无差别作为论文依赖。

### 4.1 起点选择

**暂选 `els-cas-templates\cas-sc-template.tex` 作为下一阶段主稿起点，使用 cas-sc 单栏。** 原因是新稿有长分式、分段掩码公式、13 列比较/消融表及多作者信息；单栏有利于审阅和内容逐项比对。这是工程选择，不是声称 Information Fusion 初投稿必须单栏或双栏。cas-dc 保留为可选版式，等待期刊要求核验或作者明确选择后再定。

拟保留 CAS 默认版心与数学字体，按实际作者区高度决定是否启用 longmktitle；review / 匿名参数须依据核验后的期刊流程，不凭已发表文章外观推断。新稿不继承 IEEEtran、IEEEkeywords、IEEEPARstart、fancyhdr 的 TMM 页眉或 cite 宏包。

类文件使用 article 作为基础，并载入 amsmath、graphicx、hyperref、booktabs、multirow、dcolumn、expl3 等；字体部分有 T1 / STIX 及可用性分支。当前发行版未找到 charis.sty，但模板已走可用分支成功编译，不需安装字体包或改引擎。

### 4.2 文献工具与样式注意事项

提供的 template 默认写有 `natbib[authoryear,longnamesfirst]`，同时给出 numbers 的注释选项；实际论文引文样式不能仅按模板默认或示例外观确定。cas-model2-names.bst 含排序操作，仅改 natbib 的 numbers 选项不等于按首次引用顺序排列表目。

拟采用 **XeLaTeX + BibTeX**，不是 Biber，也不省略文献步骤。匹配新稿静态数字引用的方式及最终 bst，待 Information Fusion 官方引用格式核验后确定。发行版已安装 Elsevier 的 elsarticle-num.bst；本地模板注释提到的 model1-num-names.bst 未找到。不得改用 IEEEtran.bst 冒充 Elsevier 样式，也不在本阶段擅自改写/下载替代样式。

### 4.3 已实际执行的兼容性测试

所有测试文件是本项目 `audit/template-smoke/` 内的模板副本；原模板未修改。使用原有 Windows XeLaTeX 工具链，在含中文路径的指定项目内分别编译 cas-sc-sample.tex 与 cas-dc-sample.tex。

| 项目 | CAS-SC | CAS-DC |
| --- | --- | --- |
| latexmk 最终退出码 | 0 | 0 |
| 实际引擎 | XeTeX / format=xelatex，TeX Live 2026 | 同左 |
| 本地生成 PDF | 7 页，767,339 字节 | 6 页，765,249 字节 |
| 文献处理 | BibTeX 0.99e；生成 bbl，3 条示例 bibitem | 同左 |
| 最终未解析引用/文献警告 | 未发现 | 未发现 |

两份 PDF 的第 3 页已渲染检查，版面分别为单栏和双栏。日志仍有模板示例作者脚注/书签的 hyperref 警告及 overfull/underfull boxes；这些不是零警告的正式稿，后续应在真实前置信息和正文中单独消除/审查。兼容性通过不代表新论文排版通过。

首次测试的 PowerShell `ErrorActionPreference=Stop` 把 native stderr 的首次缺 bbl 提示报告为错误；随后调整本次进程的错误处理并复核成功，没有更换 TeX 引擎、修改原 cls 或升级发行版。证据见 `audit/smoke-result.json`、`audit/smoke-verification.json`、smoke 控制台日志及测试 build 下的 log/blg/bbl/PDF。

## 5. VOA 本地 VS Code / XeLaTeX 配置摘要

| 项目 | 实际检查结果 |
| --- | --- |
| XeLaTeX | `C:\Users\admin\texlive\2026\bin\windows\xelatex.exe`；XeTeX 3.141592653-2.6-0.999998 |
| latexmk | 同一 bin 目录 `latexmk.exe`；4.88，2026-03-09 |
| BibTeX / Biber | 同一 bin 目录 `bibtex.exe` 0.99e / `biber.exe` 2.21；本方案用 BibTeX |
| VS Code | `C:\Users\admin\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd` |
| LaTeX 扩展 | `james-yu.latex-workshop@10.19.0`，已通过扩展目录与 Code CLI 双重确认 |
| 用户配置 | `C:\Users\admin\AppData\Roaming\Code\User\settings.json` 无 LaTeX 覆盖；keybindings 中存在 latex-workshop.build |
| 工作区 / 项目配置 | 检查仓库、论文方案、旧工程及新项目的 .vscode/settings.json 和仓库内 *.code-workspace，未发现现成 LaTeX 覆盖；历史 workspaceStorage 存有 WH 的本地 folder 记录 |
| 活动窗口 | 检查时未得到正在运行的 VS Code 主进程；因此本阶段通过本地终端调用同一安装工具链，不宣称点击了 VS Code 构建按钮 |
| 默认 recipe | 扩展默认为 first，第一项 latexmk 带 `-pdf`；不能把默认构建当作 XeLaTeX |
| 可复用 XeLaTeX recipe | `latexmk (xelatex)` → tool `xelatexmk`，命令为 latexmk，明确带 `-xelatex` |
| 默认输出 | outDir=`%DIR%`，auxDir=`%OUTDIR%`；测试显式设置 build 作为输出/辅助目录 |
| 环境变量 / rc | 未发现 TEXINPUTS、BIBINPUTS、BSTINPUTS、LATEXMKRC 等相关环境覆盖；home、仓库、论文方案、旧工程、新项目未发现 latexmkrc/.latexmkrc |

工具的实际解析已由 Get-Command 和版本输出确认。依赖位置详见 `audit/tex-dependencies.json`。没有改全局 PATH、用户 settings.json、系统字体或 TeX 安装，也没有使用 WSL、Docker、Overleaf、LuaLaTeX 或 pdfLaTeX 作为正文引擎。

下一阶段建议仅在本项目添加 `.vscode/settings.json`：将 `latex-workshop.latex.recipe.default` 设为已存在的 `latexmk (xelatex)`，将 outDir 设为 `%DIR%/build`，auxDir 跟随 OUTDIR。当前未创建此配置，也没有改变默认用户设置。

已测试的命令形态如下（工作目录必须是本项目中的模板测试目录；正式稿开始后才换成正式主 tex）：

```powershell
& 'C:\Users\admin\texlive\2026\bin\windows\latexmk.exe' -xelatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error -outdir=build -auxdir=build cas-sc-sample.tex
```

实际 latexmk 运行链包括 xelatex、BibTeX、必要的 xelatex 重跑和 xdvipdfmx。`xelatex -no-pdf` 生成 XDV 后由 xdvipdfmx 输出 PDF 是此 XeLaTeX recipe 的正常链路，不是切换成另一正文引擎。

## 6. Git 根目录、同步目标、权限与现有改动

| 检查项 | 实际结果 |
| --- | --- |
| Git 可执行文件 | `D:\Program Files\Git\cmd\git.exe` |
| 真正 Git 根目录 | `C:/Users/admin/Documents/GitHub/WH` |
| 当前分支 / 上游 | main / origin/main |
| 现有 origin（fetch 与 push） | `https://github.com/pointerHu/WH.git` |
| 目标仓库 | GitHub API 确认 pointerHu/WH，仓库 ID 1372969840，默认分支 main |
| 开始时工作区与暂存区 | 均干净，没有发现与本任务无关的待提交改动 |
| 初始本地 HEAD 与 origin/main | 均为 `10ef224b043957319d772a1de9ecd3406366e259` |
| GitHub 实时分支检查 | GitHub 连接器读取 branches/main，返回同一 SHA；没有通过 git fetch 更改本地引用 |
| 仓库可见性 | **PUBLIC**，由 GitHub 连接器及 VOA 的 gh repo view 双重确认 |
| 连接器 / gh 权限 | GitHub 连接器有 push/admin 权限；VOA gh api user 返回 pointerHu，repo view 返回 ADMIN |
| Git 凭据助手 | manager；只读取助手名称，没有导出或记录凭据 |
| Git 原生网络测试 | `git ls-remote --exit-code origin refs/heads/main` 失败，提示 `Recv failure: Connection was reset`；此为连接错误，不据此断言令牌错误 |
| 写权限实测 | 未尝试 commit、push 或 push --dry-run；gh/API 读取成功不等于原生 Git 推送已经验证 |

**公开风险阻塞：** 用户授权“最终阶段同步项目”不等同于已明确授权公开未发表论文。鉴于目标仓库为 PUBLIC，本次及后续未取得明确公开授权前均不得推送本项目；保留本地成果，不擅自改仓库可见性、不新建私有替代仓库。

本阶段没有 git init、remote 修改、分支切换、git add、commit、push、reset、clean、合并或清理操作。原有分支和历史不变。即使最终阶段授权公开，也必须先确认原生 Git 网络/认证恢复，并重新检查工作区，仅按本项目的明确路径暂存；不能使用 git add . / git add -A 收入其他改动。

## 7. Information Fusion 官方要求核验

访问日期统一为 **2026-09-23（UTC+08:00）**。本节严格区分“期刊要求”“出版商通用说明”“工程建议”和“未核验”。

- J1：`https://www.sciencedirect.com/journal/information-fusion/publish/guide-for-authors`；直接访问及复查均返回 HTTP 403，未取得正文。
- J2：`https://www.elsevier.com/journals/information-fusion/1566-2535/guide-for-authors`；官方旧入口也返回 HTTP 403，未取得正文。
- E1：`https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions`；可访问，已读取官方通用 LaTeX 说明，相关小节为 The Elsevier article class、Elsevier reference styles、Submitting your manuscript、Can I use subfolders in my TeX submission files?。
- T1：本地 `els-cas-templates\README`、`cas-sc.cls`、`cas-dc.cls` 及 `doc\elsdoc-cas.tex`；用于说明本地模板能力，不作为 Information Fusion 专属投稿规则。

### 7.1 已核验的通用要求 / 可选能力

| 性质 | 已核验事项 | 来源 / 适用边界 |
| --- | --- | --- |
| 必须，条件适用 | EM 处理 LaTeX 源文件时应放同一目录层级，不保留子目录 | E1 的 subfolders FAQ；最终投稿包拟另建扁平化副本，不要求开发工程扁平化 |
| 必须，条件适用 | 被要求提交源文件且允许 PDF 时，应附本地编译 PDF 及完整源文件归档；不要误归为补充材料 | E1 的 Submitting your manuscript；具体提交界面仍待期刊核验 |
| 必须继续核验 | 特定期刊参考文献样式须查该刊 Guide for Authors | E1 的 Elsevier reference styles；不能以 CAS 默认代替 |
| 可选模板能力 | Elsevier 提供单栏及双栏 CAS 类/模板 | E1 + T1；不能推出本期刊强制双栏 |
| 工程建议，非期刊规定 | 当前先用 cas-sc，保留完整审计、可编辑表格和原始公式对照 | 本项目方案，不伪装成官方推荐 |

### 7.2 尚未核验，不能判为必须/建议/可选

| Information Fusion 专属事项 | 本次状态与处理 |
| --- | --- |
| 初投稿单双栏、字体/行距、页数或字数限制 | 未取得 J1/J2 正文；不声称必须 cas-dc，也不擅自删减篇幅 |
| 摘要字数上限与关键词数量 | 未核验；摘要约 272 词仅为本地盘点，不据未核实的上限压缩 |
| Highlights 是否必需、条数和字符限制 | 未核验；本阶段不生成、扩写或冒充已满足 |
| Graphical abstract 是否可选/必需及尺寸 | 未核验；不能因模板示例含该页而当作必交项 |
| 匿名方式、单独 title page、通讯作者格式 | 未核验；保留已识别作者信息，最终版按明确规则处理 |
| 引用是否数字制、排序规则与参考文献格式 | 未核验；最终 natbib 选项和 bst 尚未锁定 |
| 图像格式、分辨率及尺寸阈值 | 未核验；保持指定 PDF 及 Word 第三图原文件，不人为补像素或重画 |
| 数据/代码可用性、CRediT、利益冲突、资助、致谢、AI 使用声明 | 期刊专属要求未核验，且内容必须由作者确认；不复制旧稿声明 |
| 初次提交文件种类、系统字段、源包细节 | 未核验本刊；只记录已核验的 E1 通用源文件指引 |

结论：**官方 Guide for Authors 本次未完成内容核验**。已完成的是实际访问尝试、失败记录及出版商通用说明核验；不得将本项目标为“已满足 Information Fusion 全部投稿要求”。下一阶段需取得可访问的官方页面或作者提供的该页/PDF，不能拿其他期刊规则代替。

## 8. 阻塞项与作者待确认事项

| 级别 / 影响 | 事项 | 当前处置 |
| --- | --- | --- |
| 阻塞未来公开推送 | pointerHu/WH 为 PUBLIC，尚未明确获准公开未发表稿件 | 仅本地保留；待明确公开授权；不自行变更 remote 或仓库可见性 |
| 阻塞当前原生 Git 网络验证 | ls-remote 连接被重置，尚未证明实际 push 通道可用 | 不修改全局代理/PATH/凭据；最终阶段经授权后重新只读检查 |
| 阻塞“期刊规则全部合规”的确认 | 官方 Guide 403，专属格式规则无法核验 | 保留待核验列表；需要可读官方材料；不以记忆或别刊规则替代 |
| 图文版本待确认 | SGTG.pdf 的两路图示与正文三路融合描述未完全显式对应 | 保留指定原图与全部正文；请确认示意简化是否有意，或提供正式替换版本 |
| 引文身份待确认 | APN、Adam、UCF101 的版本/载体，以及 AVFS 缺引用 | 不增引文、不更换所引论文；按 reference-mapping.json 逐项确认 |
| 声明内容待确认 | 新稿资助、致谢、CRediT、利益冲突、数据/代码可用性及适用 AI 声明 | 不复制旧稿或编造“无利益冲突”等陈述 |
| 质量增强，非自动阻塞迁移 | 第三图较低像素；旧主文 PDF/bbl 未找到 | 第三图先保留 Word 原字节；更高清同结果图、旧编译 PDF 可由作者提供 |

本地 XeLaTeX 和 CAS 编译依赖不存在阻止开始排版的致命问题；下一阶段可在作者指令下进行本地保真迁移，但涉及上述内容取舍、正式合规与公开同步的关口不能自行越过。

## 9. 下一阶段实施方案（尚未执行）

1. 继续本项目；建立 main.tex、sections、tables、figures、references.bib、项目级 VS Code 配置和 build 输出，不另建工作区。保留 CAS 所需本地类和样式副本及许可说明。
2. 逐块迁移 Word：章节、段落、强调和数据集 cls 斜体上标；使用原始 OMML 逐式转换，保持 32 个公式编号及 244 个数学对象的含义。凡有不可无损转换的对象，登记并人工核验，不平铺成普通文字或截图代替可编辑公式。
3. 9 张表全部做可编辑 LaTeX 表；与 814 格原文台账核验方法名、行列、合并头、数值、符号和脚注。数字与结论不修订，最优/次优格式也须按新稿核验。
4. 使用指定 Introduction.pdf、SGTG.pdf 的副本，以及从 Word 提取的第三图；保留原图哈希。仅在项目副本中处理排版尺寸与经视觉核对的空白裁切，不剪去内容或重画。
5. 按既定 7 作者顺序映射 CAS 前置信息；只生成新稿对应的文献库。把文字中的图表/公式/文献引用转换为可追踪 label/ref/cite，并保留旧编号→新 key 的核验映射。
6. 在 VOA 本地运行明确的 latexmk -xelatex + BibTeX 链，逐页检查 PDF、日志、未定义引用/文献、浮动体溢出、字体缺字、书签及图片清晰度。单独出具内容核验与版式核验，不把返回码 0 等同于成稿通过。
7. 最终交付时另建投稿源包副本：按已核验 EM 通用说明展平所需文件名/路径，在该副本上再次本地 XeLaTeX 编译，输出完整工程、成稿 PDF、源文件 ZIP 与核验报告。不包含凭据、TeX 安装、无关旧稿、临时审计图片或样例论文。
8. 只有最终完成核验且公开风险得到明确授权后，重新检查 Git 状态、网络和权限，仅提交本项目许可的交付文件并正常推送现有 origin/main。推送成功与本地提交分别验证；失败则如实报告，不强推、不自动处理歧义冲突。

## 10. 本阶段已保存文件与收尾核验

| 文件 / 目录（相对本项目） | 实际作用 |
| --- | --- |
| inventory.md | 本报告，供后续阶段沿用 |
| stage-state.json | 阶段标识、项目路径、未转换/未推送/待公开授权状态 |
| audit/source-manifest.json | 46 个主来源文件的完整路径和初始 SHA-256 |
| audit/source-integrity-final.json | 再次计算来源哈希，46/46 均与初始一致 |
| audit/word-structure.json、source-document.xml | Word 全结构索引和原始 OOXML |
| audit/math-inventory.json | 全部 244 个数学对象的 OMML 与位置 |
| audit/table-cell-ledger.json | 9 张表、814 个物理格的原始文本与合并属性 |
| audit/reference-mapping.json | 新稿 32 条与旧库 49 条的候选匹配、冲突及缺失 |
| audit/pdf-metadata.json、visuals/ | PDF 属性、指定两图渲染预览、3 张 Word 原图、模板检查页 |
| audit/environment-check.json、tex-dependencies.json | 本地工具版本、扩展 recipe 与依赖路径 |
| audit/template-smoke/、smoke-result.json、smoke-verification.json | 模板副本、实际 XeLaTeX/BibTeX 测试产物与日志核验 |
| audit/git-check-final.json | 分支、HEAD、远程/API、公开属性、认证和最终工作区状态 |

收尾检查：46 个纳入清单的原始文件全部哈希不变；Git HEAD 仍为 `10ef224b043957319d772a1de9ecd3406366e259`，当前 main，上游 origin/main。暂存区为空，已跟踪文件差异为空；工作区仅新增未跟踪的 `论文方案/SGTG_InformationFusion/`。

本报告及审计文件仅保存在本地项目。本阶段到此结束，等待下一阶段指令；没有启动无人值守后台排版、自动推送或正式期刊投稿。

## 后续阶段索引（2026-09-23 第二阶段）

第二阶段已完成全文迁移及 VOA 本地 XeLaTeX 初编译。用户在第二阶段明确指定 CAS-DC 双栏，当前主稿采用 cas-dc，不再采用本报告第 4.1 节的历史暂选 cas-sc。

当前主文件为 source/main.tex，实际 PDF 为 source/build/main.pdf（15 页）。最新内容映射、数量核验、未完成元数据与日志问题见 content_map.md；阶段状态见 stage-state.json。阶段一原始状态另保存在 audit/stage2/stage1-state-before-stage2.json。

本索引不改动本报告的历史检查结论。第二阶段仍仅保存本地，没有 Git 暂存、提交或推送。

第二阶段续执行补记：本次再次核验并强制 XeLaTeX/BibTeX 构建成功，当前 PDF 仍为 15 页。原 Word 的运行页眉和 PAGE 自动页码域已明确映射到 CAS；这更正了之前辅助内容记录不充分之处，不改变学术正文。最新结果、日志和全部待处理事项见 content_map.md 第 12 节及 audit/stage2/recheck-latest.json。仍未暂存、提交或推送 Git。

## 第三阶段索引（2026-09-23）

作者区、32 条结构化参考文献与逐处引用映射已在原项目更新；当前主文件仍为 source/main.tex，CAS-DC，VOA 本地 XeLaTeX + BibTeX 实际编译成功，15 页。最新文件为 citation_map.csv、author_reference_review.md、audit/stage3/ 和 stage-state.json。

原稿 67 个引用组、69 个文献目标出现记录已核对身份；BibTeX 自动编号，无强制 nocite 顺序。未解析引文 0，另有 AVFS 缺引文、Easy Way 年份口径和 Adam 页码问题记录。全部 7 段旧作者简介也已提取留档，不当作现任身份自动加入前置信息。作者适用性和共同署名身份需单独确认。

官方 Guide 本次仍为 403；不宣称期刊专属样式已经全部核验。46 个原始材料哈希不变；本阶段没有 Git 暂存、提交或推送。历史阶段二的 note-only 文献库描述不再代表当前状态。

## 后续阶段索引：第四阶段图表精排（2026-09-23）

继续同一项目，CAS-DC双栏及VOA本地XeLaTeX/BibTeX。当前图表样式、剩余问题和全格核对分别见figure_table_style.md、figure_table_remaining.md、table_audit.csv；实际构建及审计位于audit/stage4/。

3幅图、9张表、814物理格和608个PDF数字字串全部核验，12个图注/表题保持原稿。当前PDF15页，最新构建15:08:18–15:08:33，退出码0。两张原PDF只作显示裁边，第三图保持Word原字节。

旧主稿成稿PDF本阶段仍未找到，未声称完成旧PDF视觉比较；原稿有10个非列最大值的粗体数字，保留原强调而非重新排序。本索引不改写历史盘点结果，本阶段仍未暂存、提交或推送Git。

## 最终阶段索引（2026-09-23）

最终命名PDF和投稿ZIP已在本项目根生成；source与submission_flat分别在全新输出目录使用VOA的XeLaTeX+BibTeX完整构建，均15页。最终输出为source/build-final-20260923-r4，扁平构建为audit/stage5/flat-build-20260923-160245；15对页面渲染像素一致。
最终QA_REPORT.md、TODO.md、submission_materials_check.md记录实际核验与剩余确认项。原始清单46文件哈希不变。此为排版稿并非可直接投稿终稿，作者与声明仍需确认；公开仓库推送待明确公开授权。本地commit及远程核验状态独立记录在git_sync_status.json。
