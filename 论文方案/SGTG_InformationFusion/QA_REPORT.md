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
