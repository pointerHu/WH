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
