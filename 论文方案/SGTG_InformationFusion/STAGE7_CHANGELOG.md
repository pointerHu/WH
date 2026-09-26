# 第七阶段：Acknowledgement、逐列最高值和方法出处

日期：2026-09-25。工程继续使用用户确认的 CAS-DC 和 VOA 本地 XeLaTeX + BibTeX。

## 本轮修改

1. source/sections/06-declarations.tex 中的 Funding 标题改为 Acknowledgement；基金正文、编号、CRediT和利益冲突文字不变。
2. 表2–表9按每张表、每个数据集、每个S/U/HM/ZSL列的最大值加粗，并列最高全部加粗；不跨数据集比较，不把表5的专家数量E列当作评价指标。
3. 去除数据行方法名称的统一粗体；保留表头强调、数学向量原有字形。当前有些配置恰好12个指标全部最高，仍会出现12个数值都加粗，这是计算结果，不是方法行优待。
4. 表2除SGTG外的19个方法添加期刊、会议或预印本平台及年份；保持Method表头的正确拼写。出处标签参考KA旧稿的视觉样式，但按实际引用版本核对。
5. 每张结果表下增加明确表注说明列最大值加粗；保留原Word表题。表2第一列扩大到0.30 textwidth，局部tabcolsep为1.8pt，数值字号仍9pt，没有整表缩放。

## 出处与年份处理

完整19行对应表见 table2_venue_year.csv。ALE为TPAMI'16，SJE为CVPR'15，APN为NeurIPS'20，ClipClap-GZSL为CVPRW'24，SACMA按本稿正式卷期为Inf. Fusion'26；未照抄旧表中不同版本或有误的标签。
KDA保留arXiv'23，v2修订于2024年的说明仍保留在文献库；不编造其期刊。EZ-AVGZL标记ECCV'24是会议年份，不改文献库已有年份待确认记录。
AVFS的IJCNN'23依据旧工程明确的方法行与key 6及出版商记录；本轮未擅自增加Word原来缺少的引文标识，REF-AVFS-01仍保留。新稿文献库仍为32条。

## 完整核验

9张表814个物理单元格均核对；608个最终PDF数字字符串完全不变，其中576个指标数值按PDF字体资源逐项核验粗体。96个指标列最高值全部正确，目前无并列最高值；20个数值单元格的加粗状态相对上轮改变。
原正文、摘要、作者区、32个独立公式、3幅原图和references.bib没有修改；12个图注/表题原文保持。46个原始材料文件哈希不变。
主工程构建09:05:55–09:06:12（VOA UTC+08:00），退出码0；独立扁平构建也为0，逐页文本和bbl一致。最新PDF15页，SHA-256：ea9341ac18862e8a9158c5e752128e015d492a195555edffe0865c8fcb258678。

## 交付与边界

当前论文：SGTG_InformationFusion.pdf。当前源包：SGTG_InformationFusion_submission.zip；扁平目录submission_flat已同步重建。前一版源包和目录仅归档到audit/stage7/before，不删除。
详细证据：audit/stage7/verification.json、pdf-rendered-fonts.json、table-cells.json、venue-decisions.json、visual-review.md及各构建日志。table_audit.csv已区分原始值保留与本轮获授权的强调、出处格式变化；citation_map.csv已刷新目标行号。
本轮实际查看最终PDF第10–15页；所有修改表格及Acknowledgement可读，无重叠或截断。保留1个既有标题overfull、5个空锚点、64个underfull和1个Adam页码提示，没有批量屏蔽。
独立材料SGTG_Funding_Statement.docx已存在用户后续编辑（标题为Acknowledgment，正文起始为was supported）；为避免以旧下载副本回滚用户修改，本轮没有覆盖该Word文件。Funding改名要求已在论文、PDF与LaTeX源包中落实。
数据共享及AI使用范围继续按指令暂缓。两位作者的CRediT、Cover Letter第七问、图2三路对应等原有待确认项不属于此次修改，不自动补造。
本轮未执行Git暂存、提交或推送。既有未提交改动保持；公开论文授权尚未获得，不公开上传。
