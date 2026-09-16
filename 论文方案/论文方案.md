
```
```

# 融合 Semi-IIN、QA-TIGER 与 EZ-AVGZSL 的 Audio-Visual GZSL 方案

## 0. 上下文归档与文件索引

### 0.1 当前方案状态

本文件是当前已经确定采用并准备继续完善的论文方案，也是后续新对话、论文方法设计、公式修订、实验规划和论文写作的主要上下文文件。

- **资料目录绝对路径**：`/home/admin/claude-wokeplace/论文方案`
- **当前文件绝对路径**：`/home/admin/claude-wokeplace/论文方案/AVGZSL_SemiIIN_QATIGER_EZAVGZSL论文方案.md`
- **方案用途**：作为拟写 Audio-Visual Generalized Zero-Shot Learning 论文的确定版本，后续工作应在本方案的核心科学问题和三个创新点基础上继续深化。

后续新对话应优先读取本文件。除非明确提出重新设计研究方向，否则不再回退到旧方案，也不把三个核心挑战重新拆散。

### 0.2 使用到的论文及本地文件

以下四篇论文是本方案的直接理论和方法来源。表中的文件名与磁盘中的实际文件名完全一致。

| 论文角色             | 论文名称                                                                                                       | 本地文件名                                         | 相对路径                                                    | 绝对路径                                                                       | 本方案采用的内容                                                                                                                                                             |
| -------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AVGZSL 基线论文      | *Audio-Visual Generalized Zero-Shot Learning using Pre-Trained Large Multi-Modal Models*                     | `Audio-Visual_Generalized_Zero-Shot_Learning.md` | `论文方案/Audio-Visual_Generalized_Zero-Shot_Learning.md` | `/home/admin/claude-wokeplace/论文方案/Audio-Visual_Generalized_Zero-Shot_Learning.md` | AVGZSL 任务定义；CLIP 视觉特征、CLAP 音频特征；CLIP/CLAP 类别文本嵌入；音视频表示与类别语义对齐；VGGSound-GZSL、UCF-GZSL、ActivityNet-GZSL 实验设置                          |
| 模态交互来源论文     | *Semi-IIN: Semi-supervised Intra-inter modal Interaction Learning Network for Multimodal Sentiment Analysis* | `Semi-IIN论文完整.md`                            | `论文方案/Semi-IIN论文完整.md`                            | `/home/admin/claude-wokeplace/论文方案/Semi-IIN论文完整.md`                            | Intra-modal Masked Attention、Inter-modal Masked Attention，以及对模态内/模态间信息进行动态选择的 gate；本方案不把其情感分析任务和伪标签自训练作为当前主创新                 |
| 时序建模来源论文     | *Question-Aware Gaussian Experts for Audio-Visual Question Answering*                                        | `QA-TIGER_CVPR2025_完整论文.md`                  | `论文方案/QA-TIGER_CVPR2025_完整论文.md`                  | `/home/admin/claude-wokeplace/论文方案/QA-TIGER_CVPR2025_完整论文.md`                  | Question-aware early fusion 迁移为 class-semantic-aware early fusion；question-guided Gaussian experts 迁移为类别语义条件的音频/视觉多高斯时间专家；连续软时间定位与专家路由 |
| 语义原型优化来源论文 | *Audio-visual Generalized Zero-shot Learning the Easy Way*                                                   | `EZ-AVGZL论文实验前内容.md`                      | `论文方案/EZ-AVGZL论文实验前内容.md`                      | `/home/admin/claude-wokeplace/论文方案/EZ-AVGZL论文实验前内容.md`                      | Class embedding optimization；在增强类别可分性的同时保持原始语义结构；supervised audio-visual language contrastive alignment；非线性类别匹配思想                             |

说明：EZ-AVGZSL 论文在本地保存时的文件名为 `EZ-AVGZL论文实验前内容.md`，文件名中是 `AVGZL`，但本文叙述中的方法名称统一写为 `EZ-AVGZSL`。后续检索文件时必须使用磁盘上的实际文件名。

### 0.3 已生成的历史方案文件

下面两个文件记录了当前方案形成前的推导过程，可用于追溯设计依据，但不应替代本文件作为后续写作的主方案。

| 文件性质         | 本地文件名                             | 相对路径                                        | 绝对路径                                                           | 与当前方案的关系                                                                                                       |
| ---------------- | -------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| 第一阶段融合方案 | `AVGZSL_Semi-IIN融合方案.md`         | `论文方案/AVGZSL_Semi-IIN融合方案.md`         | `/home/admin/claude-wokeplace/论文方案/AVGZSL_Semi-IIN融合方案.md`         | 记录将 Semi-IIN 的 intra/inter masked attention 和 dynamic gate 迁移到 AVGZSL 的早期方案，是当前挑战3的来源            |
| 第二阶段扩展方案 | `AVGZSL_SemiIIN_QATIGER_扩展方案.md` | `论文方案/AVGZSL_SemiIIN_QATIGER_扩展方案.md` | `/home/admin/claude-wokeplace/论文方案/AVGZSL_SemiIIN_QATIGER_扩展方案.md` | 在第一阶段基础上引入 QA-TIGER 的语义感知早期融合和多高斯专家；当前方案将其中原挑战1和挑战2合并，并进一步引入 EZ-AVGZSL |

当前方案的演化关系为：

```text
AVGZSL baseline
    + Semi-IIN 的模态内/模态间分离交互与动态门控
    -> AVGZSL_Semi-IIN融合方案.md
    + QA-TIGER 的语义感知早期融合与多高斯时间专家
    -> AVGZSL_SemiIIN_QATIGER_扩展方案.md
    + EZ-AVGZSL 的判别性类别原型优化与监督式语义对齐
    -> AVGZSL_SemiIIN_QATIGER_EZAVGZSL论文方案.md（当前确定方案）
```

### 0.4 新对话的推荐读取顺序

为了在新的对话中快速恢复完整上下文，建议按以下顺序读取文件：

1. 先读取当前主方案：`论文方案/AVGZSL_SemiIIN_QATIGER_EZAVGZSL论文方案.md`。
2. 读取 AVGZSL 基线：`论文方案/Audio-Visual_Generalized_Zero-Shot_Learning.md`。
3. 读取三个创新来源：`论文方案/Semi-IIN论文完整.md`、`论文方案/QA-TIGER_CVPR2025_完整论文.md`、`论文方案/EZ-AVGZL论文实验前内容.md`。
4. 只有需要追溯方案演化或比较旧版本时，再读取两个历史方案文件。

### 0.5 新对话必须保留的研究约定

后续继续丰富论文时，应保留以下上下文和边界：

1. **任务不变**：研究任务是 Audio-Visual Generalized Zero-Shot Learning，训练阶段只使用 seen 类音视频样本，测试阶段同时识别 seen 和 unseen 类。
2. **最终方案不变**：当前采用 DiSAGE-IIG-AVGZSL，不再把旧方案作为并列候选。
3. **挑战结构不变**：三个核心挑战分别是语义引导时序证据发现、兼顾可分性与语义保持的类别原型学习、模态内/模态间分离交互与动态融合。
4. **未见类使用边界**：可以使用 seen/unseen 类别名称及文本语义，因为类别语义是零样本学习的已知侧信息；训练时不能使用 unseen 类音视频样本，避免破坏 inductive GZSL 设定。
5. **迁移而非照搬**：QA-TIGER 的 question feature 被替换为 class semantic prototype；Semi-IIN 的情感分析任务和半监督伪标签流程不是当前主方法；EZ-AVGZSL 的类别原型优化需要服务于本文的早期融合、高斯定位和最终分类，而不是作为孤立模块。
6. **后续重点**：继续完善时应优先统一符号、梳理模块数据流、确认损失函数之间的关系、设计可执行的消融实验，并逐步形成论文摘要、引言、相关工作和方法章节。

### 0.6 可直接用于新对话的接续说明

```text
请先读取“/home/admin/claude-wokeplace/论文方案/AVGZSL_SemiIIN_QATIGER_EZAVGZSL论文方案.md”，它是已经确定采用的论文方案。论文来源和历史方案的文件索引记录在该文件第0节，所有材料均位于“/home/admin/claude-wokeplace/论文方案”目录。后续工作不重新拆分三个核心挑战，并严格保持 inductive AVGZSL 中不使用 unseen 类音视频训练样本的设定。在继续写作前，可按第0.4节的顺序读取相关论文文件。
```

## 1. 文档目标与修订背景

本文件在同一目录下的 `AVGZSL_SemiIIN_QATIGER_扩展方案.md` 基础上继续扩展，进一步引入 `EZ-AVGZL论文实验前内容.md` 中关于类别嵌入优化与监督式文本-音视频对齐的思想，形成一个更适合作为论文初稿创新方案的版本。完整文件路径和上下文恢复说明见第0节。

本次修订的重点是：

1. 原方案中的“类别语义早期参与特征学习”和“多高斯专家时间建模”不再拆成两个独立挑战，而是合并为一个更自然的科学问题：如何利用类别语义引导音视频时序证据发现。
2. 新增一个来自 EZ-AVGZSL 的核心问题：类别文本嵌入虽然具有语义关系，但并不一定具有足够的分类可分性，因此需要学习判别性更强、同时保留语义结构的类别原型。
3. 保留 Semi-IIN-like 序列版方案中的模态内交互、模态间交互和动态门控思想，用于解决音频与视觉弱相关、噪声干扰和模态偏置问题。

涉及材料包括：

- `Audio-Visual_Generalized_Zero-Shot_Learning.md`：提供 AVGZSL 任务基线、CLIP/CLAP 特征和类别语义对齐框架。
- `Semi-IIN论文完整.md`：提供 intra-modal / inter-modal masked attention 与动态 gate 思想。
- `QA-TIGER_CVPR2025_完整论文.md`：提供 question-aware early fusion 与 temporal Gaussian experts 的连续时间建模思想。
- `EZ-AVGZL论文实验前内容.md`：提供 class embedding optimization 与 supervised audio-visual language alignment 思想。
- `AVGZSL_Semi-IIN融合方案.md`：记录将 Semi-IIN 思想迁移到 AVGZSL 的第一阶段方案。
- `AVGZSL_SemiIIN_QATIGER_扩展方案.md`：已有的语义感知高斯专家 Intra-Inter 门控 AVGZSL 方案。

新版方案可命名为：

```text
DiSAGE-IIG-AVGZSL
```

即：

```text
Discriminative Semantic-Aware Gaussian Expert Intra-Inter Gated Audio-Visual Generalized Zero-Shot Learning
```

中文可称为：

```text
判别语义增强的高斯专家 Intra-Inter 门控音视频广义零样本学习
```

其中：

- **Discriminative** 来自 EZ-AVGZSL，强调类别语义原型的可分性优化。
- **Semantic-Aware Gaussian Expert** 来自 QA-TIGER 的问题引导融合与多高斯时间专家，迁移为类别语义引导的时序证据发现。
- **Intra-Inter Gated** 来自 Semi-IIN-like 方案，强调模态内信息和模态间信息的分离建模与动态融合。

## 2. 新方案的核心科学问题

本文拟解决的核心科学问题可以概括为：

> 在音频-视觉广义零样本学习中，如何将类别文本语义从被动的最终分类原型，提升为同时具备判别性、时序引导性和模态融合调控能力的语义条件信号，从而在没有未见类训练样本的情况下，学习对 seen/unseen 类均有效的音视频语义对齐表示？

这个科学问题包含三个层次：

1. 类别语义如何引导模型在长时序音视频中找到真正与类别相关的证据。
2. 类别语义原型如何在保持语义关系的同时具备更强的类别可分性。
3. 音频与视觉如何在存在弱相关、噪声和模态偏置时进行可靠融合。

因此，新论文的创新点不再是简单地“融合三篇论文”，而是围绕 AVGZSL 中的语义迁移、时序定位和跨模态融合三个关键瓶颈构建统一框架。

## 3. 三篇论文思想的可迁移关系

| 来源论文/方案 | 原始思想                                   | 迁移到本文中的形式                             | 解决的问题                             |
| ------------- | ------------------------------------------ | ---------------------------------------------- | -------------------------------------- |
| QA-TIGER      | question-aware early fusion                | class-semantic-aware early fusion              | 类别语义提前参与音视频序列编码         |
| QA-TIGER      | temporal Gaussian experts                  | semantic-conditioned Gaussian temporal experts | 连续定位类别相关视觉帧和音频片段       |
| EZ-AVGZSL     | class embedding optimization               | discriminative semantic prototype optimization | 提高类别原型可分性，同时保留语义结构   |
| EZ-AVGZSL     | supervised audio-visual language alignment | supervised semantic-AV contrastive alignment   | 用简洁对比目标对齐音视频表示与类别语义 |
| Semi-IIN-like | intra/inter masked attention               | intra/inter audio-visual sequence interaction  | 分离模态内稳定线索和跨模态互补线索     |
| Semi-IIN-like | dynamic gate                               | semantic-aware intra/inter dynamic gate        | 根据样本和类别自适应融合不同信息源     |

## 4. 拟写论文的核心挑战、原因与解决方法

### 挑战1：如何利用类别语义引导音视频时序证据发现，而不是先全局编码再最终匹配？

**原因：**
音频-视觉广义零样本学习依赖类别语义将已见类知识迁移到未见类。现有方法通常先把视频编码为一个类别无关的全局音视频表示，再与类别文本嵌入计算相似度。这种“先编码、后匹配”的范式存在明显不足。首先，类别标签通常只是简短短语，例如 `playing piano`、`basketball dunk`、`wood thrush calling`，难以充分表达动作过程、声音属性、场景上下文和主体对象等细粒度语义。其次，长视频中并非所有帧和音频片段都与类别相关，关键动作或关键声音往往只出现在局部时间段。如果类别语义只在最终分类阶段使用，模型在编码阶段就缺少明确的语义查询信号，容易把背景、静音、噪声和无关动作混入最终表示。对于未见类而言，模型没有该类训练样本，更需要依靠类别语义主动定位可能相关的时序证据。

**方法：**
本文将 QA-TIGER 的 question-aware early fusion 和 Gaussian temporal experts 迁移到 AVGZSL 中，提出类别语义引导的时序证据发现模块。具体来说，先将类别名称扩展为更丰富的语义描述，包括动作描述、声音属性、典型场景、主体对象和易混类别差异等信息，构建类别语义原型；然后将类别语义原型提前注入视觉帧序列和音频片段序列，使模型在编码阶段就能形成 class-conditioned audio-visual features。在此基础上，引入多高斯专家时间建模，由类别语义动态生成多个连续 soft temporal masks，对视觉和音频分别进行类别相关片段定位。相比均匀池化，该方法能够减少冗余片段干扰；相比 Top-K 离散选择，高斯权重能够保留连续动作和持续声音的时间结构；相比单一 attention pooling，多专家结构能够覆盖多段关键证据，并允许音频和视觉关注不同时间区域。

### 挑战2：如何提升类别语义原型的分类可分性，同时保留 seen/unseen 类之间的语义关系？

**原因：**
AVGZSL 的最终分类依赖类别文本嵌入作为语义原型。CLIP、CLAP 或大型语言模型生成的文本嵌入通常具有较好的语义关系，例如 `playing guitar` 与 `playing violin` 在语义空间中应当比 `playing guitar` 与 `dog barking` 更接近。然而，这类预训练文本嵌入并不是专门为当前 AVGZSL 分类任务优化的，可能存在类别间距离过近、未见类边界模糊、相似动作或相似声音类别难以区分等问题。如果只追求类别间最大分离，又可能破坏原本有价值的语义结构，使模型失去从已见类迁移到未见类的基础。因此，本文需要解决的不是“是否使用类别语义”，而是如何学习既有判别性、又保持语义拓扑关系的类别原型。

**方法：**
本文引入 EZ-AVGZSL 的 class embedding optimization 思想，在原始类别语义原型的基础上学习一组优化后的判别性语义原型。优化目标同时包含两部分：一方面，通过类别分离损失扩大不同类别原型之间的距离，提高分类边界清晰度；另一方面，通过语义保持约束维持原始文本嵌入中的相对语义关系，避免把语义相近类和语义无关类强行拉成同等距离。优化后的类别原型不仅用于最终分类对齐，也作为前述 semantic-aware early fusion 和 Gaussian temporal experts 的语义查询信号。这样，类别语义不只是更丰富，而且更适合驱动时序定位、跨模态融合和 zero-shot 分类。

### 挑战3：如何分离模态内线索和模态间互补信息，并通过动态融合抑制模态干扰？

**原因：**
真实视频中的音频和视觉并不总是强相关。视觉中可能存在背景、遮挡、非关键动作或无关主体；音频中也可能包含背景音乐、环境噪声、静音片段或与画面弱相关的声音。不同类别对模态的依赖程度也不同：有些类别主要依赖视觉动作，有些类别主要依赖声音事件，还有一些类别需要音视频共同验证。若直接拼接音频和视觉特征，模型容易把无关信息一起融合，造成模态干扰；若固定依赖某一模态，又容易在 seen 类上形成模态偏置，降低对 unseen 类的泛化能力。

**方法：**
本文保留 Semi-IIN-like 序列版方案中的 intra/inter 分离思想，设计模态内和模态间双分支交互模块。Intra-modal Masked Attention 只允许同一模态内部 token 进行注意力交互，用于建模视觉帧内部的动作变化和音频片段内部的声音演化，保留相对纯净的模态特定线索；Inter-modal Masked Attention 主要允许音频 token 与视觉 token 之间交互，用于捕捉声音事件和视觉动作之间的互补关系。随后，结合语义高斯专家得到的关键片段表征，构建动态门控机制，根据当前样本和候选类别自适应调节模态内信息、模态间信息和高斯时序证据的融合比例。当音频与视觉互补性强时，模型增强跨模态交互；当某一模态存在噪声或弱相关时，模型更多依赖模态内稳定线索和高斯定位后的可靠片段。

## 6. 总体框架

给定一个视频样本，本文框架包含六个阶段：

1. **音视频序列特征提取**：使用 CLIP 提取视觉帧序列特征，使用 CLAP 提取音频片段序列特征。
2. **多粒度类别语义构建**：由类别名称、动作描述、声音属性、场景上下文和易混类别差异构建原始类别语义原型。
3. **判别性类别原型优化**：借鉴 EZ-AVGZSL，在保持语义结构的同时增强类别原型可分性。
4. **语义感知早期融合与高斯时间定位**：借鉴 QA-TIGER，将类别语义作为查询信号注入音视频序列，并通过多高斯专家定位类别相关片段。
5. **模态内/模态间分离交互**：借鉴 Semi-IIN-like 方案，分别建模模态内部时序关系和跨模态互补关系。
6. **动态融合与语义对齐分类**：通过门控机制融合多类信息，并用监督式文本-音视频对比目标完成 seen/unseen 共享语义空间对齐。
