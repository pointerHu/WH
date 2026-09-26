# SGTG 投稿材料 — 更新至2026-09-25

本轮按用户要求保留当前 CAS-DC 模板，生成独立 Word 材料，并在论文文末加入已授权的 CRediT、Funding 和利益冲突文字。数据共享和 AI 使用范围暂缓，不添加相关声明。

## 文件

| 文件 | 当前用途与状态 |
| --- | --- |
| SGTG_Highlights.docx | 4 条英文 Highlights；78、71、76、75 个字符，包含空格与标点 |
| SGTG_Cover_Letter.docx | 当前封面信：参考两份模板重写；完整七问；已确认无前序发表；三页渲染核验通过 |
| SGTG_Cover_Letter.md | 与当前Word封面信一致的可编辑文字版 |
| SGTG_Cover_Letter_Seven_Questions_DRAFT.docx | 历史草稿保留，不再作为当前封面信 |
| SGTG_CRediT_Statement_PARTIAL.docx | 原样列出本轮提供的五位作者贡献；Xinru Yi、Minyi Guo 尚缺贡献，不删除其署名 |
| SGTG_Funding_Statement.docx | 按本轮授权，从旧稿实际提取六项资助、七个编号；未编造资助方作用 |
| SGTG_Declaration_of_Competing_Interest.docx | 与用户提供的英文声明逐字一致；这是本地准备文件，不是已操作官方 Declarations tool 的证明 |
| SGTG_Highlights.md | 便于编辑的 Highlights 文本 |
| SGTG_Cover_Letter_Seven_Questions_DRAFT.md | 本次重写所用历史来源；当前内容见SGTG_Cover_Letter.md |

## 需要补充的作者事实

CRediT 仍缺 Xinru Yi、Minyi Guo 两位作者的贡献。用户已明确确认本研究不存在前序发表，新封面信第七问已据此定稿。当前在投情况和全部作者是否批准投稿仍需作者自行确认，未将其与“无前序发表”混为一谈，也未自动写入封面信。资助方在研究设计、执行、写作和投稿中的具体作用未给出，不自动补写“无参与”。

## 论文与源包

新增内容位于 source/sections/06-declarations.tex，在结论之后、参考文献之前。旧正文、摘要、公式、表格、图注、图片、作者名单和 references.bib 均不改变。当前稿仍为15页；主工程和扁平目录均用 VOA 本地 XeLaTeX + BibTeX 编译通过。主 PDF 和投稿源码 ZIP 已重新生成；Word 材料作为独立附件准备，尤其 DRAFT/PARTIAL 文件没有混入源码 ZIP。

所有五份 DOCX 在 VOA 实际生成；下载副本与 VOA 文件 SHA-256 一致，DOCX 的六页已渲染并查看。论文仅在 VOA 本地编译，新增声明与文末版式已查看。详细核验在 audit/stage6/；原始材料未修改。本轮没有 Git 暂存、提交、推送或正式投稿。

2026-09-25：当前使用SGTG_Cover_Letter.docx和同名md。两份模板及旧草稿原文件未修改；新文件没有DRAFT、确认占位符或模板原刊名。见audit/stage12/verification.json。
