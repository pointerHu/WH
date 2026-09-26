# 第三阶段：作者信息、参考文献与引用核验

核验日期：2026-09-23；设备：DESKTOP-VOA285C。项目：`C:\Users\admin\Documents\GitHub\WH\论文方案\SGTG_InformationFusion`。

本阶段仅更新本地项目；未暂存、提交或推送 GitHub。作者迁移授权不等同于全体作者已确认本篇稿件的署名与身份。

## 1. 本地交付

| 文件 | 内容 |
| --- | --- |
| source/frontmatter.tex | 已按实际旧稿重新核验的 CAS 作者区；摘要和关键词未改 |
| source/references.bib | 32 条结构化条目，不再以 note 保存整段参考文献 |
| citation_map.csv | 69 个引用目标出现记录，另加 1 个 AVFS 缺引文标记记录；UTF-8 BOM |
| source/build/main.pdf | 本地实际编译的当前 15 页论文 |
| audit/stage3/ | 原始来源缓存、字段决策、映射核验、构建日志、哈希及截图 |
| author_reference_review.md | 本报告，包括作者确认项与文献待处理项 |

## 2. 作者信息：来自旧稿，而非新稿适用性已获确认

实际来源：`../KA_GZSL_TMM/KA-GZSL_TMM.tex` 作者区与 thanks，带原行号摘录保存在 `audit/stage3/old-author-source.txt`。同时读取了旧工程 `sec/references.bib`；未找到旧 bbl，不假定它存在。

| 顺序 | 姓名 | 单位 | 邮箱 | ORCID | 明确存在的身份 |
| --- | --- | --- | --- | --- | --- |
| 1 | Hu Wang | 1 | gs.wanghu24@gzu.edu.cn | 0009-0008-1596-5311 | 无额外标记 |
| 2 | Jing Yang | 1+2 | jyang23@gzu.edu.cn | 0000-0003-1915-9487 | 通讯作者；Member, IEEE |
| 3 | Xiaoli Ruan | 1 | xlruan@gzu.edu.cn | 0000-0002-7623-3308 | 无额外标记 |
| 4 | Yuling Chen | 1 | ylchen3@gzu.edu.cn | 0000-0002-8674-8356 | 无额外标记 |
| 5 | Xinru Yi | 3 | cme.xryi23@gzu.edu.cn | 0009-0007-4224-4774 | 无额外标记 |
| 6 | Chengjiang Li | 4 | cjli3@gzu.edu.cn | 0000-0002-1864-2023 | 无额外标记 |
| 7 | Minyi Guo | 1+2 | myguo@gzu.edu.cn | 0000-0003-0034-2302 | Fellow, IEEE |

单位 1：State Key Laboratory of Public Big Data, Guizhou University, Guiyang 550025, China。
单位 2：Department of Computer Science and Engineering, Shanghai Jiao Tong University, Shanghai 200240, China。
单位 3：School of Mechanical Engineering, Guizhou University, Guiyang, Guizhou 550025, China。
单位 4：School of Management, Guizhou University, Guiyang 550025, China。

新 Word 的标题、摘要、关键词之后直接进入 Introduction，没有独立论文作者区。因此没有发现可逐人列出的新旧作者信息冲突；这不等于新稿作者已确认。

### 作者脚注分类与投稿前确认

| 标识 | 源码事实 | 当前草稿与待确认事项 |
| --- | --- | --- |
| AUTHOR-APPLICABILITY | 7 位作者及单位、邮箱、ORCID 均实际存在于旧稿 | 名单、顺序、作者-单位关系原样迁移；请全体作者确认适用于本篇 SGTG |
| CORRESPONDING | 旧稿只明确标记 Jing Yang 为通讯作者 | CAS cormark/cortext 已迁移；新稿通讯身份尚未单独确认 |
| SHARED-AUTHORSHIP | 旧作者区未明确共同一作或共同通讯 | 未增加任何共同身份标记；投稿前分别确认是否适用，不能从作者次序或星号推断 |
| IEEE-IDENTITY | Jing Yang: Member, IEEE；Minyi Guo: Fellow, IEEE | 用 CAS fnmark/fntext 迁移信息，而非 IEEEmembership 命令；属于来源记录，不是本次外部身份更新认证 |
| FUNDING/DECLARATIONS | 原 thanks 混有资助与基金编号 | 单位/通讯信息已分离；资助、基金编号、贡献分工、致谢和论文专属声明均未复制 |

作者区没有新增地址或邮编，没有删改姓名。新增的脚注 1、2 是 IEEE 身份说明，不表示共同一作。

## 3. 全部引用及身份映射

实际扫描 Word 全正文、表格单元格、图表注、页眉页脚以及存在的其他故事部件：发现 67 个引用组，对应 69 个文献目标出现记录、32 篇不同文献。正文 49 组、表格 18 组；本稿图注/表注/页眉页脚未发现额外引用，也无实际附录或叙述脚注需要补入。

CSV 每行包括原标识、Word 部件/body 或单元格位置、所在章节、原上下文、文献题名/作者/年份/DOI、BibTeX key、旧库 key 和路径、条目来源、证据 URL、访问日期、匹配状态、目标 tex 行号及编译后的新编号。

33 个有引用的来源单元已逐单元比较 Word 指向的身份序列与 TeX key 序列，身份错配 0。没有将单纯编译成功当作身份匹配成功。旧库有 20 个同一工作候选，其余 12 条按新稿及原始发布来源建立；其中 UCF101 和 Adam 保留新稿指定载体，不沿用旧 arXiv 条目类型。

原稿 body 117 的 [3]–[5] 转为同一条 cite 中的 3 个语义 key，完整覆盖原引用范围；不再用两个端点号码拼接。正文其他措辞、数学、实验数字、图像和表格源码未改。

已停用 reference_order.tex 的强制 nocite 顺序。所有 32 条均实际被引用，文后没有仅靠 nocite 搬入的条目。编号由 BibTeX 根据正文实际出现顺序生成。

| Word 原号 | 当前号 | key | 旧库候选 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | 1 | `parida2020cjme` | 3 | identity_verified |
| 2 | 2 | `mazumder2021avgzslnet` | 4 | identity_verified |
| 3 | 3 | `mercea2022avca` | 1 | identity_verified |
| 4 | 4 | `kurzendorfer2024clipclap` | 2 | identity_verified |
| 5 | 5 | `mercea2022tcaf` | 5 | identity_verified |
| 6 | 6 | `chen2023kda` | 9 | identity_verified |
| 7 | 7 | `mo2024easy` | 12 | identity_verified_year_convention_pending |
| 8 | 8 | `tsai2019mult` | 无准确对应 | identity_verified |
| 9 | 9 | `nagrani2021bottlenecks` | 无准确对应 | identity_verified |
| 10 | 10 | `lin2025semiinn` | 无准确对应 | identity_verified |
| 11 | 11 | `ma2026famav` | 无准确对应 | identity_verified |
| 12 | 12 | `li2023pstp` | 无准确对应 | identity_verified |
| 13 | 13 | `li2024tspm` | 无准确对应 | identity_verified |
| 14 | 14 | `xiao2024trust` | 无准确对应 | identity_verified |
| 15 | 15 | `kim2025qatiger` | 无准确对应 | identity_verified |
| 16 | 16 | `chao2016gzsl` | 无准确对应 | identity_verified |
| 17 | 17 | `chen2020vggsound` | 34 | identity_verified |
| 18 | 18 | `soomro2012ucf101` | 35 | identity_verified |
| 19 | 19 | `heilbron2015activitynet` | 36 | identity_verified |
| 20 | 20 | `kingma2015adam` | 37 | identity_verified_pagination_unverified |
| 21 | 21 | `frome2013devise` | 38 | identity_verified |
| 22 | 22 | `akata2016ale` | 39 | identity_verified |
| 23 | 23 | `akata2015sje` | 40 | identity_verified |
| 24 | 24 | `xu2020apn` | 无准确对应 | identity_verified |
| 25 | 25 | `xian2019fvaegan` | 42 | identity_verified |
| 26 | 26 | `hong2023hyperbolic` | 7 | identity_verified |
| 27 | 32 | `maaten2008tsne` | 无准确对应 | identity_verified |
| 28 | 27 | `li2024stft` | 43 | identity_verified |
| 29 | 28 | `yang2025mstr` | 14 | identity_verified |
| 30 | 29 | `li2025mdst` | 44 | identity_verified |
| 31 | 30 | `yang2026sacma` | 45 | identity_verified |
| 32 | 31 | `ma2026sgpan` | 无准确对应 | identity_verified |

## 4. 已处理的文献差异与仍需确认的项目

旧库同题或同主题不等于同一版本：APN 采用新稿 NeurIPS 2020 的 Zero-Shot 论文，不采用旧 key41 的 IJCV 2022 Any-Shot 扩展；t-SNE 采用 van der Maaten/Hinton 2008，不采用旧 key46 的 2019 理论论文。KDA 保留 2023 原始年份及 2024-04-24 v2 备注；Adam 保留 ICLR 2015；UCF101 保留技术报告身份。

CJME、AVGZSLNet、AVCA、f-VAEGAN-D2、Hyperbolic 等条目在 CVF 与 IEEE DOI 元数据中存在不同页码序列。本阶段使用与 Word 相符的 CVF 官方页码，另存两套值和取舍理由，不将差异当成另一篇文献。AVGZSLNet 的 Singh/Parida 姓名边界按 CVF 修正；ActivityNet 第一作者 Caba Heilbron、SJE 的 Honglak Lee 也单独核对。

为避免重复显示同一个标识，25 个与 DOI 完全等价的 doi.org URL 从排版字段去重，DOI 本身保留。预印本版本链接、无 DOI 文献的原始页面链接保留。VGGSound 大写形式按 Word 保留。所有字段变化均在 reference-decisions.json 中记录。

| 标识 | 原稿位置 | 尚未解决的内容 | 目前处理 |
| --- | --- | --- | --- |
| REF-AVFS-01 | Table 2 的 AVFS 行 | 无引文编号，32 条列表也没有对应条目 | 保留方法名及数据；CSV 单独标记。旧 key6 只作为候选，未擅自加第 33 篇 |
| YEAR-CONVENTION-07 | Word [7]，当前 [7] | Springer 首次在线为 2024，Cite-as 年为 2025 | 暂保留 Word/旧库/Crossref 的 2024；投稿前确认年份口径 |
| BIB-PAGES-ADAM | Word [20]，当前 [20] | 未取得 ICLR 2015 可核验的会议页码 | pages 留空，保留 1 个 BibTeX 提示；不以 arXiv PDF 页数编造会议页码 |

来源限制说明：DeViSE 页码 2121–2129 来自 Word 与旧库一致记录，官方 NeurIPS BibTeX 导出为空；本阶段没有将其宣称为独立外部页码确证。这不构成引用身份错配。

上述“身份已核验”“元数据仍有口径/字段限制”“编译是否解析”是不同检查，不互相替代。引用对象核对中未发现错配；编译未解析引文 0；另有 1 个没有引用标识的 AVFS 待作者补充，以及 2 项元数据保留问题。

## 5. 引用样式与期刊要求状态

继续使用 CAS-DC + natbib[numbers] + 本项目的 elsarticle-num.bst + BibTeX，不采用 IEEEtran.bst，不混入 biblatex/Biber。文后编号是 BibTeX 的结果，CSV 中的新编号从 aux 读取，不手工固定旧编号。

2026-09-23 再次访问 Information Fusion 官方 Guide for Authors 仍返回 HTTP 403，未取得正文；不能声称本刊专属引用规则已核验。当前数字样式是已实际测试的兼容方案，投稿前仍须核对本刊要求。官方通用说明也要求查询具体期刊 Guide。来源：https://www.sciencedirect.com/journal/information-fusion/publish/guide-for-authors ；https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions 。

Springer 年份证据：https://link.springer.com/chapter/10.1007/978-3-031-73209-6_22 。其他逐条出版商/DOI/官方论文集/原始预印本证据与访问日期已附于 CSV 和 audit/stage3/evidence-index.json。失败请求同样保留，不冒充已访问成功。

## 6. 实际本地编译和当前警告

正文引擎：`C:\Users\admin\texlive\2026\bin\windows\xelatex.exe`；构建程序为同目录 latexmk，实际显式使用 -xelatex，并实际运行 BibTeX。
工作目录：`C:\Users\admin\Documents\GitHub\WH\论文方案\SGTG_InformationFusion\source`。
最新构建：2026-09-23T13:46:47.923099+08:00 至 2026-09-23T13:47:01.065248+08:00；退出码 0。
控制台日志：`C:\Users\admin\Documents\GitHub\WH\论文方案\SGTG_InformationFusion\audit\stage3\build-20260923-134647\console.log`。
引擎日志首行：`This is XeTeX, Version 3.141592653-2.6-0.999998 (TeX Live 2026) (preloaded format=xelatex 2026.8.6)  23 SEP 2026 13:46`。

| 项目 | 实际数量 |
| --- | --- |
| 缺字 | 0 |
| 未解析引文 | 0 |
| 未解析交叉引用 | 0 |
| BibTeX empty year | 0 |
| BibTeX 提示（Adam empty pages） | 1 |
| 标题区 overfull | 1 |
| underfull 盒子 | 61 |
| CAS empty anchor | 5 |

剩余 BibTeX 提示是 Adam 会议页码未取得，不是引用 key 缺失；不通过假填页码或把它改成另一版本来消除提示。版面/锚点提示属于 CAS 排版问题，不宣称零警告或最终投稿版。

实际渲染保存了 15 页；重点检查作者页、页码范围引用位置、Table 2 新引文号和文后列表。记录见 audit/stage3/visual-review.md。

## 7. 内容边界、来源保护和本地收尾

本阶段只改动 source 下的 frontmatter.tex、main.tex、references.bib、reference_order.tex 和 04-experiments.tex 中的一处引用范围命令。除这些允许变化外，其他 66 个既有 source 文件哈希不变；摘要、关键词、作者顺序/单位/邮箱/ORCID 保持一致。全部公式、表格数值和三张原图未改；73 个章节/公式/图表标签编号仍与原稿对应。

46 个原始材料文件哈希全部不变。Git HEAD 为 `10ef224b043957319d772a1de9ecd3406366e259`，分支 main；暂存区为空、已跟踪文件没有差异，仅本项目新增。没有提交、推送或更改远程。

PDF SHA-256：`733b5132462e3ef6f6897c99eaf885532aea7cf5f00e791e542020c0020d78bb`。

复编译用 scripts/build_stage3.py；随后可运行 stage3_citations.py 和 stage3_verify.py 更新映射与复核。一次性生成脚本保留审计作用，存在完成记录时拒绝覆盖；人工核对后的 reference-decisions.json 和 source 文件代表当前版本。


## 8. 旧作者简介的附加核对

补查旧稿第 619–665 行的全部 7 段 IEEEbiography，原文、姓名与行号已保存到 audit/stage3/author-biographies.json。学历、职称、历史访问、ACM 身份及编辑任职等另作来源记录，未把旧简介全部当作现任身份塞入 CAS 前置信息。

新稿是否使用这些附加身份、旧作者区双单位的适用性，以及简介中重复/不同的学位经历表述，均另列作者确认项；具体见 audit/stage3/author-biography-review.md。没有据此改动旧稿或判断本人真实现状。

## 第九阶段更新（2026-09-25）：where、公式(5)/(27)、AVFS

AVFS缺引文已按用户明确授权解决：旧工程key6 -> zheng2023avfs；在4.1.4和表2出现，当前[26]。33条文献、71次引用目标、身份错配0。此前章节的缺引文标记仅作为历史记录。
