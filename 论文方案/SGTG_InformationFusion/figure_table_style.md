# 第四阶段：图片与实验表格样式说明

核验日期：2026-09-23；实际设备：DESKTOP-VOA285C，Windows，UTC+08:00。
项目：`C:\Users\admin\Documents\GitHub\WH\论文方案\SGTG_InformationFusion`。

本阶段在既有 CAS-DC 双栏工程内精排 3 幅图和全部 9 张表；没有重新写作、改数值、改数学含义或执行 Git 写操作。当前稿件仍由 `source/main.tex` 构建。

## 1. 来源与边界

正文、表格、图注的主来源是本地 `SGTG_English_Translation.docx`。旧 `KA_GZSL_TMM/KA-GZSL_TMM.tex` 仅提供视觉规则参考，旧稿数字、方法年份标注、排名结论和文献编号没有覆盖新稿。

原始 Word、两张指定 PDF、原模板和旧工程仍只读。新增样式集中在 `source/sgtg-floats.sty`，原 `cas-dc.cls`、`cas-common.sty` 未改。

## 2. 原图实际检查与安全显示

已打开并渲染查看 Introduction.pdf、SGTG.pdf，均为 1 页；MediaBox 均为 `[0, 0, 841.92, 595.32]` bp。逐项查看了编码器名称、图例、箭头、Gaussian Generator/Router、掩码矩阵、子图 (a)/(b)/(c) 与图像内容边缘。

原图自带非零 CropBox：Introduction 为 `[48.006894,104.721005,816.867001,550.310998]`；SGTG 为 `[16.502401,16.203306,824.368001,539.749012]`。不能把按完整画布测得的裁边再次相对于这些 CropBox 应用。

当前 `includegraphics` 显式指定 `pagebox=mediabox`，仅对显示范围 trim/clip。裁边顺序为左、下、右、上；单位 bp。两张项目内 PDF 与指定原文件逐字节相同。

| 图 | 显示裁边 | 宽度与比例 | 当前位置 |
| --- | --- | --- | --- |
| Fig. 1 / Introduction.pdf | `43bp 99bp 20bp 29bp` | textwidth，保持长宽比、跨双栏 | 第 3 页；首个解释引用在第 2 页 Introduction |
| Fig. 2 / SGTG.pdf | `12bp 11bp 13bp 51bp` | textwidth，保持长宽比、跨双栏 | 第 5 页；结构说明与引用在第 4 页 3.2 |
| Fig. 3 / tsne-word.png | 不裁切、不重采样 | 0.97 textwidth，保持长宽比、跨双栏 | 第 13 页，与 4.4 节起始同页，在 Conclusion/References 前 |

两张 PDF 的裁边在可见内容外保留约 6 bp 安全余量；图中文字、子图标记、图例和箭头没有被裁掉。预览 PNG 只用于审计，不进入论文图片引用；没有将 PDF 栅格化替换、重画或改变颜色。

图注保持 Word 原文，12 个图注/表题均经去格式回译核验。沿用语义 label/ref，每幅图只引用一次。第三图仍为 Word 内原始 1141×835 PNG，不以旧稿 tsne.png 替换；按当前约 168.6 mm 宽显示，有效采样约 172 ppi，这只是实际尺寸记录，不等于已核验期刊分辨率阈值。

引言图的源码锚点移至解释性段落 body[5] 后；第三图锚点提前到 Table 9 之后，以便跨栏浮动体落在 4.4 节附近。所有正文段落的词语与顺序不变。在 Conclusion 前设置 FloatBarrier，避免实验图进入参考文献；没有在每个章节强制清空浮动体造成空白半页。

## 3. 旧表格样式提取及未完成的旧 PDF 对照

已重新读取旧主稿的主对比表、组件消融表和其他代表表源码。排除注释表后识别到 4 个活动表格环境。对 WH 仓库中本工程之外的 13 个 PDF 逐一检查页数和首屏文本，并检查现有材料 ZIP 目录，仍未发现旧主稿成稿 PDF。旧 `figure/KA-GZSL.pdf` 是单页架构图，不是论文 PDF。

因此：旧稿 PDF 视觉对照未完成，不能把本阶段新生成 PDF 或模板示例称为旧稿 PDF；以下旧样式结论仅据实际源码。记录见 `audit/stage4/old-pdf-search.json`。

| 样式项 | 旧源码所见 | 本次 CAS 处理 |
| --- | --- | --- |
| 表头 | 数据集组头，下面 S/U/HM/ZSL；multirow/multicolumn | 保留新稿实际 13 列内容，添加兼容 CAS 的分组短横线与组间留白 |
| 线条 | 顶/底 2 pt，中线 1 pt | 使用较轻的 0.8/0.4/0.3 pt 顶底/中线/组头线，不照搬粗重参数 |
| 列间距/行距 | 代表表未设置局部 tabcolsep/arraystretch；以额外空列分组 | 当前 tabcolsep=2.6 pt，arraystretch=1.18；不用额外数据列，组间增加 0.65 em 留白 |
| 数字字体及对齐 | 普通 c 列，字号继承旧正文；没有原生小数点对齐 | 保留 CAS 表格字体体系，small（9 pt），新增不改变数值的 tablenum 小数点对齐 |
| 最佳/次佳 | 旧主表明确说明粗体/下划线 | 不迁入此排名规则；新 Word 无该定义，仅保留原稿已有逐格强调 |
| 本方法行 | 浅灰底及局部粗体/下划线 | 不复制旧灰底和排名；原稿整行粗体保留，可用中线隔开末行 |
| 方法出处 | 部分带 scriptsize 会议/年份标签 | 不补入新稿没有的会议名或年份；仅保留已有方法名和正确 cite key |
| 表注及显著性 | 所读代表表没有独立显著性星号/均值标准差说明 | 不创造表注、显著性符号或统计量；新稿已有百分号与数学标识完整保留 |

## 4. 当前表格技术规则

9 张表均为原生 `tabular*`，Table 1 是 10 列划分表，Tables 2–9 均保留三数据集 × 四指标。表题与图题由 CAS 自身命令处理，不引入 IEEE 类、caption 风格覆盖或极端负间距。

方法名列采用约 0.25 textwidth 的可换行列；划分表首列约 0.27 textwidth。未缩短方法名、未强制整表 resizebox/scalebox、未删列或删行。当前最后一表的完整 “Visual + auditory descriptions” 已可完整显示，不再在词中强制断开。

小数单元格使用 `SGTGnum`，内部为 `tablenum`，设置 `round-mode=none`、`round-pad=false`、`group-digits=none`、`table-format=2.2`，格式位只预留对齐空白，不补写零。原稿的 576 个小数均为两位小数；另有 32 个整数，保持原样。

## 5. 全覆盖数字保真核验

`table_audit.csv` 为 UTF-8 BOM、全部字段加引号的 CSV，共 814 条单元格数据记录；不是只抽查或比较行列数。字段包括 original_table、row、physical_column、grid_column、original_value、typeset_value、verification_status、emphasis、pdf_numeric_check 及 TeX 位置。

核验链：直接读当前 Word 的 9 张表与合并属性 → 对照此前迁移台账和本阶段前 TeX → 去除新加的纯对齐包装 → 比较每格内容/强调 → 从实际 PDF 独立提取 51 个数字数据行，与 Word 的 608 个数字单元格逐项比较原始字串。未按浮点近似或四舍五入判等。

| 表号 | 物理行 | 物理格 | 当前页 |
| --- | ---: | ---: | ---: |
| 1 | 6 | 54 | 9 |
| 2 | 22 | 277 | 10 |
| 3 | 6 | 69 | 11 |
| 4 | 6 | 69 | 11 |
| 5 | 7 | 82 | 12 |
| 6 | 6 | 69 | 12 |
| 7 | 6 | 69 | 12 |
| 8 | 5 | 56 | 12 |
| 9 | 6 | 69 | 13 |

814/814 单元格内容和原有强调核验通过；608/608 数字在最终 PDF 中按原字串核验通过。方法/数据行的关联、合并单元格、空格占位单元格和 16 个表内数学对象均保留。原稿未出现均值±标准差、置信区间、显著性标记或缺失值占位，本阶段没有添加这些内容。

CSV 中 typeset_value 使用第三阶段生成的当前文献号；normalized_original_numbering 将文献号还原为 Word 号进行身份核验。少数方法名的引用数字变化是第三阶段已确认的自动编号，不是实验数值变化，标记为 PASS_AUTO_CITATION_RENUMBERED。

CSV 文件本身保留例如 10.30、24.50 的字面值。用 Excel/WPS 查看时，应把原始值、排版后值等列按“文本”导入，避免查看软件自动隐藏尾零；这不改变 CSV 或 PDF 的真实内容。

## 6. 本地构建、视觉检查与复核入口

实际工具为 VOA 的 `C:\Users\admin\texlive\2026\bin\windows\latexmk.exe`，显式使用 `-g -xelatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error -outdir=build -auxdir=build main.tex`。工作目录为 source。没有切换引擎、设备、安装软件或更改全局配置。

最新构建：2026-09-23 15:08:18–15:08:33（UTC+08:00），退出码 0；日志明确为 XeTeX/format=xelatex 和 BibTeX。实际 PDF 为 15 页，1,730,559 字节。完整日志快照见 `audit/stage4/build-20260923-150818/`。

最终 15 页全部有视觉核验覆盖；最后一次只调整第三图锚点后，第 1–12 页与已查看版本逐像素相同，第 13–15 页重新打开检查。最终渲染在 `audit/stage4/renders-final2/`。图中文字/图例/子图标记未裁切，表头和数据无重叠或越界，第三图不再漂入参考文献。

第一轮曾因未显式区分原图 CropBox 与 MediaBox 出现显示裁剪问题，已在视觉检查中拒收并修复；失败试排只保留在 audit 的历史目录，不是交付 PDF。最终统一使用 pagebox=mediabox，原 PDF 从未修改。

本次图表未引入未定义引用、缺字或表格溢出警告；仍保留既有标题区 1 个 overfull、5 个 empty-anchor、61 个 underfull，以及 Adam 的 1 条 empty pages 文献提示。不得把这些记录说成已消除，也不把本阶段作为期刊最终合规认证。

复编译：`python -X utf8 scripts/build_stage4.py`；全表复核：`python -X utf8 scripts/stage4_audit.py`。VS Code 仍使用原有项目级 latexmk (xelatex) recipe。维护时编辑 source 中对应图表文件；stage4_style.py 只是首次样式变更的历史审计脚本，有重复运行保护，不应覆盖后续人工调整。

核心证据：`audit/stage4/verification.json`、`table-cells.json`、`pdf-numeric-rows.json`、`caption-checks.json`、`positions.json`、`visual-regression.json` 和 `visual-review.md`。剩余确认项集中在 `figure_table_remaining.md`。

本阶段只保存本地。Git 分支、历史和远程不变，不执行 git add/commit/push，也不进行正式投稿。
