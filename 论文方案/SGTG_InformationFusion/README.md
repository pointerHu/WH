# SGTG Information Fusion LaTeX 排版项目

**排版稿，存在待作者确认项；不是可直接投稿终稿。**

正文、公式及实验数据来自 SGTG_English_Translation.docx；作者信息按指定旧稿迁移。使用所提供 CAS-DC 双栏模板，原 CAS 版权及许可保留。没有正式投稿。

## 交付入口

| 文件或目录 | 用途 |
| --- | --- |
| `source/main.tex` | 可维护工程主入口 |
| `SGTG_InformationFusion.pdf` | 本次正式交付的本地 XeLaTeX 编译 PDF |
| `submission_flat/` | 独立编译通过的扁平化源文件，仅本地保留 |
| `SGTG_InformationFusion_submission.zip` | 从实际扁平化目录生成的源包，仅本地保留 |
| `QA_REPORT.md`、`TODO.md` | 实际核验与投稿前确认事项 |
| `inventory.md`、`content_map.md` | 历史来源清单、内容映射及最终阶段补充 |
| `citation_map.csv`、`table_audit.csv` | 逐处引文与全部表格逐格核验 |
| `audit/stage5/` | 原始日志、独立构建、逐页预览、来源哈希；本地审计证据 |

## 在 VOA 构建

在 VS Code 打开本项目文件夹，而不是仅打开上级 WH 仓库；再打开 `source/main.tex`。项目 `.vscode/settings.json` 选择原有 `latexmk (xelatex)` recipe，避免默认第一项的 pdfLaTeX。用户级设置和全局 PATH 未修改。

本地终端在项目根目录运行：

```powershell
python -X utf8 scripts/build_project.py --out build-review --full
```

脚本显式调用 VOA 的 `C:\Users\admin\texlive\2026\bin\windows\latexmk.exe -xelatex`，自动运行 BibTeX 与必要重编译。不会删除目录或安装/升级 TeX。`--out` 是 source 内的直接子目录；全新核验请选择尚不存在的目录名。实际交付构建目录是 `source/build-final-20260923-r4/`，控制台与编译参数保存在其中。

源文件编译需要现有 TeX Live 2026 的 XeLaTeX、latexmk、BibTeX、STIX、natbib、siunitx、placeins 等；项目内已带 CAS 类、样式、图片和文献库。不依赖项目外 Word、旧 TMM 工程或旧模板目录。Python 构建入口仅用标准库；扁平化脚本的验证还使用 VOA 已有 pypdf。

## 重新生成扁平化投稿包

首次从 Git 检出时不会包含 submission_flat 和 ZIP。在完成上述 build-review 构建后运行：

```powershell
python -X utf8 scripts/prepare_submission.py --source-build build-review
```

生成器会检查重名、展平相对路径、在独立输出目录运行同一 XeLaTeX/BibTeX 链，核对页文字和 bbl，再生成 ZIP。若同名生成目录或 ZIP 已存在，会停止，避免覆盖；需先检查并归档这些本项目生成物，再重新生成。不对源稿或其他目录执行清理。

扁平目录主文件仍为 `main.tex`，文献文件为 `main.bbl`。为了保留原 CAS 文件并满足扁平依赖，生成的类/宏包分别命名为 `cas-dc-flat.cls`、`cas-common-flat.sty`，只调整内部文件名和图片路径，许可头保持。其余文稿内容不变。投稿包不含原始 Word、旧论文、临时日志、Git 目录或未确认声明草稿。

## 维护与核验

正文在 sections，32 个编号公式在 equations，9 张可编辑表在 tables，3 幅真实图在 figures。保留 DOCX body 与 CELL 来源注释。修改内容后必须重新编译并更新映射、数值及引用核验，不能只替换 PDF。

`source/main.bbl` 是与最终文献库一致的可复现依赖，纳入本地 Git 提交。只忽略构建目录，不无差别忽略 bbl 或 PDF。最终 PDF 与两幅 PDF 插图均保留。

本次未推送至公开远程：新稿公开授权尚未给出。当前本地提交详情和远程核验记录保存在 `git_sync_status.json`（本地文件，不作为投稿材料）。具体待确认项见 TODO.md。

标题页已采用 CAS 常规前置信息布局，页脚使用“Manuscript prepared for Information Fusion”，不宣称已经投稿。既有模板警告、密集图例清晰度及未确认内容均在 QA_REPORT.md 中如实记录。

## 当前更新：2026-09-24 投稿附件与声明

用户已确定使用当前CAS-DC模板。本轮新增 `source/sections/06-declarations.tex`，包含用户提供的五人CRediT、授权复用的旧稿资助，以及给定利益冲突声明。七人作者区、原正文、摘要和全部实验数字不变。数据共享与AI声明暂缓。

五份独立Word附件位于 `submission_materials/`，详见该目录README。Cover Letter为七问草稿，前六问完成，第七问需要前序发表/关联稿件及作者批准事实；CRediT文件标为PARTIAL，因为Xinru Yi和Minyi Guo角色尚未提供。不能将这两个文件视为无待确认项的正式附件。

本轮实际构建目录为 `source/build-stage6-20260924/`；根目录PDF与源码ZIP已更新，15页，包含72个扁平化源文件。旧交付物保留于 `audit/stage6/before/`。本轮核验以 `audit/stage6/verification.json` 和 `QA_REPORT.md` 第9节为准；前文r4构建路径是历史记录。

日常仍使用 `scripts/build_project.py --out <source内的输出目录名> --full`，明确调用本地XeLaTeX和BibTeX。下次重新生成源包前，应先检查归档同名生成物；源码ZIP只包含排版工程，独立投稿Word文件需另行管理。封面信草稿和数据/AI待办没有混入源码ZIP。

本轮没有新增Git提交或推送，新的文件变更仅在本地，不能认为已包含在此前提交中。独立利益冲突Word文件按用户原文准备，尚未操作官方Declarations tool或投稿系统。


## 第七阶段更新（2026-09-25）

Funding标题按要求改为Acknowledgement；资助正文及编号不变。表2–表9按各数据集的每个指标列最高值加粗，96列核验通过，20个数值格调整字重；不再整行强调本方法。表2的19个基线添加实际引用版本的期刊/会议/平台及年份。

全部814个物理格的内容核对通过；608个渲染数字原字串不变，576个指标字重逐项从PDF字体资源核验。原正文、作者、公式、图注、实验数值和文献库未改。当前主PDF仍15页；主工程与扁平目录均已在VOA XeLaTeX+BibTeX独立构建通过，ZIP已更新。详见STAGE7_CHANGELOG.md和audit/stage7/。

当前构建目录source/build-stage7-20260925。此次只保存本地，不提交或推送；数据和AI范围仍暂缓。


## 第八阶段更新：表后Note与图3（2026-09-25）

删除8条表后Note及对应宏，保持全部数值、最高值粗体和方法出处。4.4第二段已转为图3图注，正文删除重复段落，保留的第一段增加自动图3引用。图3改用用户提供的tsne.pdf矢量原文件，项目副本与原文件逐字节一致；原PNG仅留审计备份，不再打入源包。

当前PDF仍15页，图3在第13页；source/build-stage8-20260925和独立扁平目录均由VOA的XeLaTeX+BibTeX成功编译。814格、608个PDF数字、576个指标字重核验通过，原74个正文/列表内容单元为73个正文加1个移至图注；未改实验数据。详情见STAGE8_CHANGELOG.md及audit/stage8/。

## 第九阶段更新（2026-09-25）：where、公式(5)/(27)、AVFS

最新主构建：source/build-stage9-final-20260925/。交付入口不变，参考文献现33篇，AVFS [26]已补入。修改范围与证据见STAGE9_CHANGELOG.md及audit/stage9/；独立Word材料保持原状。

## 第十阶段当前排版（2026-09-25）

当前主PDF为16页，最终构建目录source/build-stage10-r4。source/sgtg-page-layout.sty使用原CAS表题和图注函数，在sections/04-experiments.tex以SGTGPageTop组织页顶分组。表格自身仍位于tables/并保持可编辑；附加依赖balance已经存在于VOA TeX Live中，无须新安装或全局配置。后续增删正文或表格后，应重新检查这些分页分组，不仅替换PDF。当前图3在第14页，表2在第10页。


## 2026-09-25 第十一阶段：文字连续排版

已去除第8页起的人为分页和逐页短栏平衡。表1至表9仍位于第9至13页页顶，分组不变；图3仍位于第14页。文字连续接排，最终15页。第1–7页内容和版式保持，仅页脚总页数自动更新。正文、公式、图表、声明与文献没有改写。第8–15页实际查看，主工程与扁平稿15页渲染逐像素一致。详细说明见 STAGE11_CHANGELOG.md 和 audit/stage11/；构建日志 source/build-stage11-r1/console.log。

页顶图表计划集中在 source/page-top-plan.tex；正文不再调用 SGTGPageTop 或 balance。后续正文长度变化时仍需重新核验图文页序，不要恢复按段落强制分页。


2026-09-25：当前封面信为submission_materials/SGTG_Cover_Letter.docx和SGTG_Cover_Letter.md；完整七问，无前序发表已由作者确认。旧DRAFT保留为历史来源。本次未改变论文或源包。
