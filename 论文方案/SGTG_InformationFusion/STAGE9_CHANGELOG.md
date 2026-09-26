# 第九阶段：where 接排、长公式紧凑化、AVFS 引文

日期：2026-09-25。项目保持 CAS-DC；论文只在 VOA 本地 XeLaTeX + BibTeX 编译。

## 已修改

1. 24处公式后的符号/运算说明统一为小写 where，使用 noindent/unskip 顶格接排，去除公式与说明间的额外段落空行；另外2处行内 Here 说明改为连贯的 where 从句。PDF行首where的横坐标落在两栏左边界。
2. 公式(5)、(27)局部使用9pt，不改变全文字号。公式(5)将求和限制改为正常脚本大小，缩小过大的定界符和行距，保留完整三行表达；公式(27)由三行压为两行。只调整排版，逐项数学token核对一致，条件、下标、范数、拼接、系数及运算次序未变。
3. 从KA_GZSL_TMM/sec/references.bib的key 6提取AVFS，新增zheng2023avfs，保留作者、完整题名、IJCNN 2023、1–8页及DOI 10.1109/IJCNN54540.2023.10191705；只规范页码连接符并去除重复DOI URL等无用字段。
4. 表2 AVFS行及4.1.4 Baselines均补入同一引用，当前自动编号[26]。正文方法列表补上AVFS后与所称14种AVGZSL方法一致。其余文献按BibTeX自动重编号，不改变引用对象。

## 核验

当前15页、3图、9表、33篇参考文献。原有32条BibTeX的元数据完全保留。69个当前引文组包含71次目标出现，新增2次AVFS引用，未解析引文及身份错配0。
814个物理表格格逐格核对，608个实际PDF数字字串不变；576个指标字体字重与96列最高值规则一致。所有表后Note保持删除，图3仍使用用户提供的原始矢量PDF，图注及4.4迁移结果不变。
46个原始材料文件及额外tsne.pdf哈希不变。正文除本轮where连接、排版与明确授权的AVFS补引外不改写；资助、CRediT、利益冲突、数据共享及AI暂缓安排不变。

## 文件与记录

主文件source/main.tex；交付SGTG_InformationFusion.pdf；submission_flat和SGTG_InformationFusion_submission.zip同步重建并独立编译。
当前主构建source/build-stage9-final-20260925/；扁平构建见audit/stage9/flat-build.json。
详细证据：audit/stage9/verification.json、equation-token-checks.json、where-pdf-positions.json、citation-verification.json、visual-review.md及before备份。
已刷新citation_map.csv、table_audit.csv和table2_venue_year.csv。旧稿缺AVFS的历史记录保留，但当前问题已解决。
本轮已实际查看修改涉及的最终PDF第4–15页，公式(5)在第5页、公式(27)在第8页，未见新增公式越界或文字重叠。既有标题overfull、空锚点、段落underfull及Adam页码提示未屏蔽，详见QA。
本轮不提交或推送Git，不操作投稿系统。
