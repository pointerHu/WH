# SGTG Information Fusion 最终阶段核验报告

日期：2026-09-23，VOA本地时区UTC+08:00。实际设备：DESKTOP-VOA285C。
结论：**排版稿，存在待确认项；不是可直接投稿终稿。** 独立构建、内容核对和逐页视觉核验已执行；公开推送因未获得论文公开授权而暂停。实际本地提交状态另存git_sync_status.json。

## 1. 交付范围与入口

唯一项目：`C:\Users\admin\Documents\GitHub\WH\论文方案\SGTG_InformationFusion`。

| 交付 | 项目内实际位置 |
| --- | --- |
| 可维护源码 | source/main.tex，及sections/equations/tables/figures分文件 |
| 最终命名PDF | SGTG_InformationFusion.pdf，15页，1,730,805字节 |
| 投稿源目录 | submission_flat/，71个同层文件 |
| 源文件ZIP | SGTG_InformationFusion_submission.zip，1,607,698字节 |
| 内容/引文/表格映射 | content_map.md、citation_map.csv、table_audit.csv |
| 投稿前确认 | TODO.md、author_reference_review.md、figure_table_remaining.md |
| 官方要求核验 | submission_materials_check.md |
| 本次原始证据 | audit/stage5/，只在本地保留 |

最终PDF SHA-256：`aa2fad9f7410d9b4d83de4e8a0939363de98857507ca1befc57a8fd9ec68c8ae`。
投稿ZIP SHA-256：`4e649ea10da0ac03d605dbdc512e7b6e2e1c86d4e6fcfdf25645e73a928166cb`。

## 2. 两次独立完整构建

正文引擎为 `C:\Users\admin\texlive\2026\bin\windows\xelatex.exe`，版本 `XeTeX 3.141592653-2.6-0.999998 (TeX Live 2026)`。文献工具为BibTeX 0.99e，不是Biber。LaTeX Workshop使用既有latexmk (xelatex) recipe；没有修改用户级设置、全局PATH或TeX发行版。

主工程在全新 `source/build-final-20260923-r4/` 输出目录构建，没有复用此前aux/bbl；执行时间16:02:25–16:02:45，退出码0。独立扁平工程执行时间16:02:45–16:03:04，退出码0，初始辅助文件为空；不是只复制旧PDF冒充独立编译。

主工程真实命令（工作目录source）：
```text
C:\Users\admin\texlive\2026\bin\windows\latexmk.exe -g -xelatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error -outdir=build-final-20260923-r4 -auxdir=build-final-20260923-r4 main.tex
```
扁平工程真实命令（工作目录submission_flat）：
```text
C:\Users\admin\texlive\2026\bin\windows\latexmk.exe -g -xelatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error -outdir=../audit/stage5/flat-build-20260923-160245 -auxdir=../audit/stage5/flat-build-20260923-160245 main.tex
```
日志：`source/build-final-20260923-r4/console.log`、`main.log`、`main.blg`、`build-record.json`；以及 `audit/stage5/flat-build-20260923-160245/`。两份main.log均明确记载XeTeX及format=xelatex，blg记载BibTeX和elsarticle-num.bst。

## 3. 编译、依赖、警告与源包核验

| 项目 | 最终结果 |
| --- | --- |
| 缺失文件/未定义命令/字体缺字 | 未检出 |
| 重复label/未定义交叉引用/未解析文献key | 0 |
| 表格、正文公式的水平越界 | 未检出；存在原模板标题盒子提示，见下文 |
| 标题区Overfull hbox | 1条，123.62721pt；首屏实际未见可见文字裁切，保留提示 |
| Overfull vbox | 0；balance试排引发的问题已拒收，最终不使用balance |
| hyperref空锚点 | 5条，作者脚注相关，未屏蔽 |
| Underfull盒子 | 60条；段落松排提示，不等于内容缺失 |
| BibTeX提示 | 1条：Adam的empty pages；未编造页码消除提示 |
| 字体 | pdffonts列出的26项均嵌入；未向工程复制系统字体文件 |
| 隐含输入依赖 | 两套fls核验均无项目外论文、旧工程或隐藏用户文件；TeX发行版依赖除外 |

两套PDF均15页，逐页提取文字完全一致；bbl逐字节一致；另行渲染的15对页面逐像素一致。两PDF文件哈希可因生成时间/元数据不同而不同，不以文件哈希代替页面一致性检查。
扁平目录不依赖source/，重名检查通过。必要CAS类和宏包的扁平化副本改名为cas-dc-flat.cls/cas-common-flat.sty，只修改依赖名称与路径并保留许可。main.bbl与主文件名一致。ZIP CRC检查及每项解压字节对照通过，71个文件均同层；不含Word、旧TMM论文、Git目录、日志或未经确认的声明候选。

## 4. 内容一致性终审

直接读取当前Word OOXML，而非只比较字数；按body位置、段落标记、数学结构、物理格和文献身份核对当前源码。详细证据为audit/stage5下的content-final.json、prose-final.json、table-check/和citation-check/。

| 内容 | 实际核对 |
| --- | --- |
| 正文与贡献列表 | 74/74单位去除纯排版后文字一致；保留段落逻辑和顺序 |
| 编号标题 | 29/29对应原稿，5个主章节及各级标题完整 |
| 数学对象 | 244个OMML结构与源对象对应；32个独立公式文件与已核对阶段逐字节相同，未截图替代 |
| 图注/表题 | 12/12原稿文字一致 |
| 全部实验表格 | 9表、70物理行、814/814物理格的内容与强调核对通过 |
| 最终PDF数字 | 608/608原始数字字串精确一致，含576小数和32整数；不按浮点近似判等 |
| 图片 | 3图均存在；两PDF副本与原文件哈希一致，第三图与Word嵌入PNG相同 |
| 引用 | 67组、69目标出现、32篇文献；33个引用来源单元的身份序列与key一致，错配0 |
| 作者 | 7位姓名、顺序、单位映射、邮箱及ORCID与指定旧稿来源对应；仍需确认适用于新稿 |
| 页眉/页脚与其他对象 | Word运行页眉与PAGE域已映射；原稿无附录、叙述脚注或论文声明章节，不是发现后删除 |
| 原始材料 | 清单46个原始文件SHA-256均未改变 |

本阶段没有润色正文、删减分析、修改公式含义或重算实验结果。引用编号沿用第三阶段的实际BibTeX次序，所有32条均实际被引用，没有nocite强行列出。引用身份通过不等于缺失的AVFS引文已经补齐，也不等于所有元数据争议已消除。

当前活跃稿件源码和PDF中未检出TODO、TBD、??、演示作者、假DOI或占位图。原模板的示例tex、过期reference_order和未使用bst移入本地audit/archived-unused，不打包、不提交；原模板目录从未改动。原CAS程序内部保留的未调用演示/开发分支不是论文正文，未为清除搜索字串而破坏供应方源码。

## 5. 全部15页视觉核验

最终命名PDF对应r4，已在VOA渲染并实际逐页打开1–15页。逐页记录在audit/stage5/visual-review.md；最终预览在renders-final-source，扁平预览在renders-final-flat。
标题/作者/摘要/关键词完整；采用CAS常规标题布局，使引言从第1页开始而非保留大块标题页空白。图1第2页、图2第5页、图3第13页；跨栏图保持比例且有效内容未裁切。9张表的所有列、完整方法名和原精度可见。长公式均原生可编辑，个别编号另行显示但无重叠。文献DOI/URL保留，条目不跨栏截断。
没有发现正文、图表越界裁切、图像拉伸、正文页底孤立标题或页脚覆盖。第13页实验尾部与第15页末尾存在留白，属于浮动体边界和自然尾页，非缺失段落；末页未强制等栏，是可选优化。图2的密集标注和图3的原始像素质量仍应由作者按出版要求确认，不能因完成视觉检查便宣称无限制清晰。

## 6. 投稿要求与保留问题

Information Fusion官方作者指南本阶段访问仍为403；仅核验了Elsevier官方通用LaTeX源包指引。因此本包遵守同层源文件原则，但不声称期刊全部附加要求已满足。来源及访问日期见submission_materials_check.md。四条Highlights候选单独保存于author_review_candidates/，待作者确认，不进入源包或Git候选范围。

投稿前必须处理/确认：作者适用性及共同身份、图2与正文第三分支对应、AVFS缺引文、新论文专属声明；另保留Easy Way年份、Adam页码、DeViSE页码来源限制、10个原有非最大粗体值、Baselines列举数量及原图清晰度。没有用删除标记、伪造声明或改数据把这些问题假装解决。

页脚改为“Manuscript prepared for Information Fusion”，不宣称已提交。没有正式投稿、没有登录投稿平台或确认任何声明。原来的长标题模式改为CAS常规模式、参考文献按完整段落分页、元数据/页脚说明更正均为排版层改变；科学正文、数据、图注和公式未改。

## 7. 本地版本控制与公开推送限制

本次确认的真实仓库根为C:/Users/admin/Documents/GitHub/WH，当前main，上游origin/main，远程为pointerHu/WH。GitHub连接器确认仓库PUBLIC且有push权限；但尚无公开这篇未发表论文的明确授权，因此禁止本次push，不能把本地提交称为GitHub同步。

仅按本项目明确文件清单准备本地提交，不使用git add .或git add -A；提交前复核暂存区、文件类型、敏感内容和大小。实际清单和扫描结果保存在audit/stage5/git-preflight.json。实际本地commit SHA、提交后状态和远程分支检查写入git_sync_status.json；该状态记录仅本地保留，避免报告与commit SHA自引用。

默认纳入：最终源码、图片、BibTeX、source/main.bbl、必要模板及项目设置、最终命名PDF、README/QA/TODO及映射报告、两个可复现构建脚本。默认仅本地保留：audit证据与日志、所有构建输出、重复submission_flat、可再生成的ZIP、未经确认候选、历史一次性生成/验证脚本、缓存及阶段状态。只修改本项目.gitignore，不改变仓库根忽略规则。

本报告不宣称推送成功。公开授权是实际阻塞；取得授权后仍需重新核验远程是否分歧和原生Git网络，不得强推或自动合并语义冲突。

提交前实际检查补充：明确候选87个文件，最大文件为最终PDF（1,730,805字节），未发现需单独大文件处理的文件。候选文本按私钥、GitHub令牌、API密钥及敏感赋值模式扫描无命中；这是范围内扫描结果，不是对所有可能机密的绝对保证。Git hooks目录无活动脚本，暂存区和已跟踪差异均为空；所有候选均位于本项目。最终PDF、两幅PDF插图和source/main.bbl没有被忽略，五类本地生成物的忽略规则已实际测试。
Git差异空白检查另有329处空白提示：321处行尾空白、5处缩进空格/制表符、3处文件末尾空行，主要位于未改动的CAS/BST供应方源码及既有公式行；无合并冲突标记。未批量重写供应方文件或改变公式以清理这些非编译错误，详情保存在audit/stage5/staged-whitespace-check.txt。

## 8. 本次续执行的独立冷构建与交付复核（2026-09-23 18:05–18:06）

连接时发现上述完整交付及本地排版提交已经存在，因此沿用已确认工程，不重复迁移正文或覆盖已核验的源包。随后实际执行了两次额外冷构建：将当前可维护源码复制到全新 source-clean，将实际交付 ZIP 逐项解出到全新 flat-clean；这两个核验副本均不带任何既有 bbl/aux，输出目录初始为空。原工程、交付 ZIP 和保留的 main.bbl 未清理或修改。

新的核验根目录：`audit/stage5/recheck-20260923-180544/`。两个工作目录分别为其中的 `source-clean/` 和 `flat-clean/`；每套控制台、XeLaTeX、BibTeX 日志分别在自身 `build/console.log`、`build/main.log`、`build/main.blg`。命令均为：

```text
C:\Users\admin\texlive\2026\bin\windows\latexmk.exe -g -xelatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error -outdir=build -auxdir=build main.tex
```

源码副本构建时间18:05:44–18:06:04，投稿ZIP副本构建时间18:06:09–18:06:29，均为VOA本地UTC+08:00，退出码均0，均实际运行XeTeX/format=xelatex及BibTeX。两套fls均未发现各自核验目录和现有TeX发行版以外的输入依赖。26项字体记录均嵌入；没有打包字体安装文件。

两次新生成PDF与根目录现有交付PDF均为15页，逐页文字一致，15对三方渲染图逐像素一致。新生成bbl与source/main.bbl及submission_flat/main.bbl逐字节一致。因此保留原交付PDF与ZIP字节，不为生成时间差异改写二进制交付物。ZIP的71个同层文件CRC和逐项内容检查通过。

本次重新对当前Word执行：74个正文/列表单位、29个标题、244个原始OMML对象、32个独立公式、814个物理表格格、608个最终PDF数字、12个图注表题，以及67组/69次引用目标核验。引用身份错配和未解析key均为0。重新生成的citation_map.csv/table_audit.csv记录与现有交付记录完全一致；46个原始文件哈希仍不变。

本次已实际打开最新 renders-delivered 下的全部15页，并保存逐页记录visual-review.md。未发现正文/图表重叠、有效内容裁切、图片拉伸、假DOI或演示作者。图2密集标注、图3原像素限制及第13/15页尾部自然留白仍如第5节说明。已有1条标题盒子、5条空锚点、60条underfull及Adam的1条缺页码提示保留，没有批量屏蔽。

Information Fusion官方Guide再次访问仍返回403，搜索未补足其正文，未采用其他期刊或第三方模板说明替代。本次读取的Elsevier官方LaTeX通用说明仍要求EM源文件同层，并要求按具体期刊Guide确定参考文献样式；投稿材料检查的未核验状态不变。

本次Git只读复核确认main/origin/main和pointerHu/WH不变，仓库仍为PUBLIC，远程仍停在本地排版提交的父提交。公开这篇未发表论文尚未明确获准，推送继续暂停。已存在的排版提交保留，本次仅将实际新增核验记录作项目限定的本地提交；最新SHA与提交后状态记录于本地git_sync_status.json，不自引用写进本报告。

## 9. 2026-09-24：投稿附件和已授权声明更新

用户明确确定使用当前 CAS-DC 模板，不再在本任务中切换。新增 source/sections/06-declarations.tex，在结论之后、参考文献之前写入用户提供的五人 CRediT、授权复用的旧稿资助，以及逐字一致的利益冲突声明。旧稿资助仅提取资助句，规范换行/逗号后的空格；未复制通讯脚注或单位。六项资助共七个编号原样保留，资助方作用未编造。

作者区仍为七人且字节未改：Xinru Yi、Minyi Guo 贡献未提供，独立 CRediT 文件明确标为 PARTIAL。Cover Letter 按七问结构撰写，前六问据现稿方法、实验和已核验文献完成；第七问涉及前序发表、关联旧稿、在投与作者批准情况，保留明确确认段，不虚构事实。五篇比较参考文献均核对现有 BibTeX 身份和 DOI。数据共享与 AI 使用范围按指令暂缓，没有新增相关声明；摘要没有压缩。

独立 Word 文件实际生成在 submission_materials/，下载副本与 VOA 版本 SHA-256 相同。Highlights 共四条，含空格与标点字符数78/71/76/75。Cover Letter 两页，其余四个DOCX各一页；六页均渲染并实际查看，未见裁切、重叠或缺字。DOCX渲染检查只用于附件质量；论文没有在其他设备编译。

主工程在 source/build-stage6-20260924/ 使用现有 latexmk -g -xelatex + BibTeX 完整构建，09:28:13–09:28:35（VOA UTC+08:00），退出码0。扁平目录独立构建09:34:45–09:35:08，退出码0，日志在 audit/stage6/flat-build-20260924-093445/。日志明确为 XeTeX 3.141592653-2.6-0.999998 (TeX Live 2026)，文献工具BibTeX。两套逐页文字和bbl一致，扁平目录72个文件，ZIP逐项字节及CRC校验通过。

根目录 SGTG_InformationFusion.pdf 与新构建一致：15页、1,732,693字节，SHA-256 b9daf632e4aabfc3910ac45404c000c4b308fa38a219e34549589b759cd5a167。根目录ZIP已同步本轮源码，不含独立Word附件或未完成的封面信。此前PDF、ZIP和扁平目录保存在audit/stage6/before，没有清理原材料。

本轮重新对照当前Word核验74个正文/列表单位、29个编号标题、244个OMML对象、32个独立公式、814个表格物理格、608个PDF数字、12个图注/表题，以及67组/69次引文目标；全部通过。作者区、原科学正文、表格、图片、公式、摘要及references.bib字节不变。原始46个材料哈希全部不变。

本轮论文视觉检查范围为新增声明与文末重排的第13–15页，均已打开查看；第1–12页没有声称在本轮逐页重新查看。论文全部15页预览已生成于audit/stage6/page-*.png。当前零缺字、零未定义引文/交叉引用；仍有1个标题区overfull、5个empty-anchor、64个underfull提示及Adam的1条empty-pages提示，没有批量屏蔽。

本轮只更新本地文件，Git HEAD未改变，没有暂存、commit或push，也没有进入投稿或Declarations系统。新增源文件及附件尚未纳入此前本地提交。完整核验结果见audit/stage6/verification.json；本轮剩余确认事项以更新后的TODO.md和submission_materials/README.md为准。


## 第七阶段更新（2026-09-25）

Funding标题按要求改为Acknowledgement；资助正文及编号不变。表2–表9按各数据集的每个指标列最高值加粗，96列核验通过，20个数值格调整字重；不再整行强调本方法。表2的19个基线添加实际引用版本的期刊/会议/平台及年份。

全部814个物理格的内容核对通过；608个渲染数字原字串不变，576个指标字重逐项从PDF字体资源核验。原正文、作者、公式、图注、实验数值和文献库未改。当前主PDF仍15页；主工程与扁平目录均已在VOA XeLaTeX+BibTeX独立构建通过，ZIP已更新。详见STAGE7_CHANGELOG.md和audit/stage7/。

当前构建目录source/build-stage7-20260925。此次只保存本地，不提交或推送；数据和AI范围仍暂缓。

### 第七阶段独立复查补充（2026-09-25）

另在全新 source/build-stage7-review-20260925 输出目录实际执行 latexmk -g -xelatex 与 BibTeX，09:09:40–09:09:57（VOA UTC+08:00）完成，退出码0。没有使用旧辅助文件代替正文与文献构建。

独立脚本 audit/stage7/verify_tables.py 直接读取当前Word，核验814个物理单元格的原始内容、608个PDF数字字符串及576个指标数字的实际PDF字体粗细。96列最高值标记全部正确；20格粗体状态有授权变化，数字和显示精度无变化。表1及表头未改变，表2的19项出处标签与原实验内容分开记录，原图注和表题12项均保留。

复查编译PDF、当前命名交付PDF、独立扁平工程PDF三方逐页文本一致；15页逐像素比较全部通过，bbl一致，ZIP的72个同层文件与submission_flat逐项一致。复查PDF文件哈希因构建时间不同可以不同，不将哈希差异误作正文差异；交付PDF仍对应本阶段09:05构建记录。

本轮实际打开并查看第9–15页，包括全部9张表和Acknowledgement，未见新增裁切或重叠。证据：audit/stage7/verification-current.json、pdf-fonts-current.json、delivery-comparison.json、renders-review/。新增table_ranking_audit.csv保存全部576个指标值的最大值和粗体对应关系。原始46个材料文件哈希不变。此次复查未执行Git写操作。


## 第八阶段更新：表后Note与图3（2026-09-25）

删除8条表后Note及对应宏，保持全部数值、最高值粗体和方法出处。4.4第二段已转为图3图注，正文删除重复段落，保留的第一段增加自动图3引用。图3改用用户提供的tsne.pdf矢量原文件，项目副本与原文件逐字节一致；原PNG仅留审计备份，不再打入源包。

当前PDF仍15页，图3在第13页；source/build-stage8-20260925和独立扁平目录均由VOA的XeLaTeX+BibTeX成功编译。814格、608个PDF数字、576个指标字重核验通过，原74个正文/列表内容单元为73个正文加1个移至图注；未改实验数据。详情见STAGE8_CHANGELOG.md及audit/stage8/。

## 第九阶段更新（2026-09-25）：where、公式(5)/(27)、AVFS

已统一24处公式后where说明（小写、无首行缩进、无额外段落空行），另规范2处行内Here；仅公式(5)/(27)局部9pt，数学token核验一致。公式(5)紧凑排版，公式(27)三行改两行。AVFS按用户授权复用旧key 6，新增zheng2023avfs，在表2和4.1.4均为自动引用[26]，原文献自动顺延，共33篇。原32条元数据不变。

当前15页、3图、9表。814格、608个PDF数字与576个指标字重均核验通过，96列最高值不变，Note保持删除；图3矢量PDF及新图注保持。本轮原始46文件和tsne.pdf未改，正文除已记录where及AVFS补引外不改写。

主工程source/build-stage9-final-20260925与submission_flat实际XeLaTeX/BibTeX构建均退出0；最终PDF、源码ZIP和main.bbl已同步。实际查看第4–15页，独立源包同范围逐像素一致。缺字、未解析引文及重复label为0，既有1个标题overfull、5个空锚点、60个underfull及1个Adam页码提示保留。日志、逐项数学及引用核验在audit/stage9/。未提交或推送Git，未处理数据共享/AI范围，未改独立Word附件。

## 第十阶段更新：关键词、公式5与实验页布局（2026-09-25）

关键词为四项，Video首字母大写，末项无句点。公式5由前置距离/符号定义加一个单行主式构成，保留原有有序三元组域、范数、符号函数、margin和max(0,·)，恢复正常公式字号。120组含相等距离的等价回归全部通过。其余31个编号公式、33条文献、24处顶格where及实验数据不变。

实际页序：9页表1；10页仅表2；11页表3/4/5；12页表6/7；13页表8/9，全部位于页顶并在下方接原有正文。14页矢量图3下接结论和CRediT，不再产生只含图3的页面。实验正文采用平衡双栏，页脚保持固定位置。全文16页；所有16页已打开检查。页8的章节边界和尾页保留正常留白，没有通过增写正文、全局缩字、删行删图来填满页面。

主构建source/build-stage10-r4和新扁平目录都以VOA原有latexmk -xelatex + BibTeX执行成功；退出码均为0。73文件源包通过完整性检查，两套PDF逐页文字及16页渲染像素一致。全部814表格格、608数字、576指标字重通过；每列最高值规则、表2出处和已删除Note不变。46份原始材料哈希以及外部tsne.pdf不变。日志仍保留1个既有标题overfull、5个empty-anchor、60个underfull和1条Adam页码提示；没有新增overfull vbox或缺字/未解析引文。详见audit/stage10/verification.json与STAGE10_CHANGELOG.md。


## 2026-09-25 第十一阶段：文字连续排版

已去除第8页起的人为分页和逐页短栏平衡。表1至表9仍位于第9至13页页顶，分组不变；图3仍位于第14页。文字连续接排，最终15页。第1–7页内容和版式保持，仅页脚总页数自动更新。正文、公式、图表、声明与文献没有改写。第8–15页实际查看，主工程与扁平稿15页渲染逐像素一致。详细说明见 STAGE11_CHANGELOG.md 和 audit/stage11/；构建日志 source/build-stage11-r1/console.log。


## 2026-09-25 阶段12：Cover Letter重写

实际读取两份本地模板和原七问Markdown，并核对当前稿件。新信采用模板1的A4纸张、页边距和Calibri 10.5 pt文字，沿用日期—编辑称呼—正文—落款格式；内容按模板2的研究介绍、Key Contributions和期刊契合结构改写为SGTG，保留全部七问及五篇关键参考文献。用户已确认不存在前序发表，第七问不再含占位符。新信无其他期刊名或KA-GZSL专属机制。

新DOCX在VOA实际生成；同SHA-256副本通过ChatGPT工作环境的render_docx.py渲染为3页，三页均已打开检查，无截断/重叠/缺字。VOA Word COM预览尝试未返回结果后已终止，不据此声称已完成VOA Word预览。样式参考模板重新构建，未保留模板作者等隐藏元数据。论文源码、PDF、投稿ZIP以及两份原模板和旧草稿均未修改；无Git暂存、提交或推送。
