# 第八阶段：删除表后 Note，修正图3图注与图像来源

2026-09-25，VOA，CAS-DC；本次只更新本地项目。

## 实际修改

1. 删除表2–9后的8条Note，以及生成这些文字的SGTGrankNote宏。表1原本没有Note。没有把这些说明移入表题或正文。
2. 将4.4节第二段（原Word body[168]）移入图3 caption，替换原有图注，删除正文中重复的第二段。仅移除开头“Fig. 3 presents the”的自指引导语，由自动图号承接；其余内容不改写。4.4节保留第一段，并在第一句补上自动Fig.3引用。
3. 使用用户提供的论文方案/tsne.pdf，复制为source/figures/tsne.pdf并相对路径引用，跨栏宽度0.97 textwidth，保持长宽比。原tsne.pdf不修改。
4. 旧tsne-word.png归档于audit/stage8，同时留有完整修改前备份，不再进入当前源码包。

## 图像检查

新PDF为1页，909.36×666 bp，74,171字节。页面含矢量绘图和可提取文字，未检测到栅格图片对象；三种字体均嵌入。不是将旧PNG装入PDF。
原图与项目副本SHA-256一致：a8f5d4f0bc6bc4e4e11a497f4d9f025517b499c862bc4c7dc5afac9439c18360。

## 内容核验

9张表共814格逐格内容与上一版一致；最终PDF的608个数字逐字符串一致，576个指标字重与96列最高值规则一致，19个方法出处不变。
原74个正文/列表内容单元中，73个留在正文、1个移为图注；29个编号标题、244个数学对象和32个独立公式保留。其余11个图注/表题不变。
32条文献及67组/69次引用对象不变，未解析引文和交叉引用为0；所有46个既有原始文件及本次新增的tsne.pdf均未修改。

## 构建与交付

source/build-stage8-20260925/为本次全新输出目录，日志确认XeLaTeX、BibTeX，退出码0。submission_flat独立构建通过，PDF为15页，图3在第13页。项目根SGTG_InformationFusion.pdf和SGTG_InformationFusion_submission.zip已更新。
实际打开查看新图及稿件第9–15页，检查全部表格、4.4节、图3新图注及文末重排。源码及PDF不再含表后Note；未出现新的图文裁切或重叠。保留现有1条标题盒子、5条空锚点、59条underfull及Adam缺页码提示。
详情：audit/stage8/changes.json、verification.json、content-final.json、citation-check/、tsne-inspection.json及visual-review.md。本轮未执行Git暂存、提交或推送。
