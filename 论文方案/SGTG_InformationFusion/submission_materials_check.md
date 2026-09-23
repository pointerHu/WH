# 投稿材料要求核验

访问日期：2026-09-23。状态：期刊专属要求仍未全部核验，不能称为可直接投稿终稿。

## 官方来源与适用边界

J1：https://www.sciencedirect.com/journal/information-fusion/publish/guide-for-authors 。本阶段两次直接读取返回403 Forbidden，未取得作者指南正文。
E1：https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions 。已成功读取官方通用LaTeX说明。

| 性质 | 已核验或未核验内容 | 本地处置 |
| --- | --- | --- |
| 出版商通用要求，EM条件适用 | E1 subfolders FAQ要求图、表、样式及文献文件均同层 | submission_flat已实际展平，独立构建通过，ZIP无子目录 |
| 出版商通用要求，源文件提交条件适用 | E1要求本地编译PDF及完整源文件归档，并说明文件类型 | 保存最终PDF、完整源包；没有进入投稿系统操作 |
| 必须继续核验 | E1明确具体期刊参考文献要求看该刊Guide | 当前保留已验证的CAS+natbib+Elsevier数字样式，不冒充期刊格式认证 |
| 期刊专属未核验 | 摘要上限、关键词数、Highlights是否必需及限制 | 原文不删减；Highlights仅提供作者候选，不混入正式源包 |
| 期刊专属未核验 | 图像阈值、Graphical Abstract、匿名要求、作者信息文件 | 不将Introduction图自动作为GA，不伪造匿名或尺寸合规 |
| 必须作者提供内容 | 资助、利益冲突、CRediT、开放性、伦理及适用AI声明 | 不复制旧论文声明，不编造“无利益冲突”等内容 |

## 本地附加材料

author_review_candidates/Highlights_candidate.md：从论文原有贡献/实验结论提炼的四条候选，逐条标明来源；待作者确认。此文件不属于稿件正文，未加入submission_flat、ZIP或Git候选清单。
没有生成未经确认的声明，没有把引言图改名为Graphical Abstract，没有登录投稿平台、确认声明或正式投稿。

投稿ZIP是已独立编译核验的排版源包，不代表上表所有内容确认项已经解决。正式提交前应由作者取得可读的Information Fusion官方作者指南并核对当前投稿页面要求。
