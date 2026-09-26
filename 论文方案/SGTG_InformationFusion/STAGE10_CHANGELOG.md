# 第十阶段：关键词、公式5简写与图文混排

日期：2026-09-25。沿用 CAS-DC 和 VOA 本地 XeLaTeX + BibTeX；未提交或推送 Git。

## 已修改

- Keywords 改为 Zero-shot learning；Audio-visual learning；Video classification；Gaussian temporal aggregation。没有末尾句点。
- 公式5之前的正文定义初始距离 d_ci^(0)、优化距离 d_ci，以及 eta_cij = sign(d_ci^(0) - d_cj^(0))；T 为所有类别两两不同的有序三元组。
- 公式5保留一个编号，用 sum_(c,i,j in T) max{0, Delta - eta_cij(d_ci-d_cj)} 表示原损失，恢复正常公式字号并排成一行。
- 式6–32编号不变，其他31个编号公式文件不变；24处where顶格说明不变。
- 用项目内 sgtg-page-layout.sty 组织页顶表格区域，调用原CAS的表题/图注函数。table源文件仍为可编辑的独立TeX，未改类文件。
- 使用现有 balance 宏包平衡这些页面正文双栏；局部修正其与CAS页脚高度及字形深度的兼容。无全局缩字、无负间距或警告屏蔽。

## 最终页序

| 页码 | 页顶内容 | 下方内容 |
| --- | --- | --- |
| 9 | 表1 | 实验设置 |
| 10 | 仅表2 | 主对比结果及核心组件消融分析 |
| 11 | 表3、4、5 | 时序聚合与专家数量分析 |
| 12 | 表6、7 | 原型目标与交互门控分析 |
| 13 | 表8、9 | 文本编码器、细粒度描述及4.4正文 |
| 14 | 图3及其原有完整图注 | 结论和CRediT |

全文由15页调整为16页，没有删减实验分析或改变表内数值。

## 核验与交付

最终源构建：source/build-stage10-r4；退出码0。投稿扁平目录另行冷构建通过，源码ZIP同步重新生成。全16页实际渲染检查。814个单元格、608个PDF数值、576个指标字重以及96个列最高值核验通过；表后Note保持为0。33条文献与原编号不变，AVFS仍为[26]。公式5由符号代入证明等价，并通过120组包含距离相等情形的随机数值回归检查；不是重新计算实验结果。
46个原始材料文件与外部tsne.pdf未修改。主稿PDF：SGTG_InformationFusion.pdf；源包：SGTG_InformationFusion_submission.zip；证据：audit/stage10/。所有未处理的作者声明事项保持原状态。
