```

```

# 融合 Semi-IIN、QA-TIGER 与 EZ-AVGZSL 的 Audio-Visual GZSL 新扩展方案

## 0. 上下文归档与文件索引

### 0.1 当前方案状态

本文件是当前已经确定采用并准备继续完善的论文方案，也是后续新对话、论文方法设计、公式修订、实验规划和论文写作的主要上下文文件。

- **当前方案名称**：DiSAGE-IIG-AVGZSL
- **当前方案文件**：`AVGZSL_SemiIIN_QATIGER_EZAVGZSL_新扩展方案.md`
- **资料目录绝对路径**：`C:\codex-workplace\论文方案`
- **当前文件绝对路径**：`C:\codex-workplace\论文方案\AVGZSL_SemiIIN_QATIGER_EZAVGZSL_新扩展方案.md`
- **相对于工作区的路径**：`论文方案/AVGZSL_SemiIIN_QATIGER_EZAVGZSL_新扩展方案.md`
- **方案用途**：作为拟写 Audio-Visual Generalized Zero-Shot Learning 论文的确定版本，后续工作应在本方案的核心科学问题和三个创新点基础上继续深化。

后续新对话应优先读取本文件。除非明确提出重新设计研究方向，否则不再回退到旧方案，也不把三个核心挑战重新拆散。

### 0.2 使用到的论文及本地文件

以下四篇论文是本方案的直接理论和方法来源。表中的文件名与磁盘中的实际文件名完全一致。

| 论文角色             | 论文名称                                                                                                       | 本地文件名                                         | 相对路径                                                    | 绝对路径                                                                       | 本方案采用的内容                                                                                                                                                             |
| -------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AVGZSL 基线论文      | *Audio-Visual Generalized Zero-Shot Learning using Pre-Trained Large Multi-Modal Models*                     | `Audio-Visual_Generalized_Zero-Shot_Learning.md` | `论文方案/Audio-Visual_Generalized_Zero-Shot_Learning.md` | `C:\codex-workplace\论文方案\Audio-Visual_Generalized_Zero-Shot_Learning.md` | AVGZSL 任务定义；CLIP 视觉特征、CLAP 音频特征；CLIP/CLAP 类别文本嵌入；音视频表示与类别语义对齐；VGGSound-GZSL、UCF-GZSL、ActivityNet-GZSL 实验设置                          |
| 模态交互来源论文     | *Semi-IIN: Semi-supervised Intra-inter modal Interaction Learning Network for Multimodal Sentiment Analysis* | `Semi-IIN论文完整.md`                            | `论文方案/Semi-IIN论文完整.md`                            | `C:\codex-workplace\论文方案\Semi-IIN论文完整.md`                            | Intra-modal Masked Attention、Inter-modal Masked Attention，以及对模态内/模态间信息进行动态选择的 gate；本方案不把其情感分析任务和伪标签自训练作为当前主创新                 |
| 时序建模来源论文     | *Question-Aware Gaussian Experts for Audio-Visual Question Answering*                                        | `QA-TIGER_CVPR2025_完整论文.md`                  | `论文方案/QA-TIGER_CVPR2025_完整论文.md`                  | `C:\codex-workplace\论文方案\QA-TIGER_CVPR2025_完整论文.md`                  | Question-aware early fusion 迁移为 class-semantic-aware early fusion；question-guided Gaussian experts 迁移为类别语义条件的音频/视觉多高斯时间专家；连续软时间定位与专家路由 |
| 语义原型优化来源论文 | *Audio-visual Generalized Zero-shot Learning the Easy Way*                                                   | `EZ-AVGZL论文实验前内容.md`                      | `论文方案/EZ-AVGZL论文实验前内容.md`                      | `C:\codex-workplace\论文方案\EZ-AVGZL论文实验前内容.md`                      | Class embedding optimization；在增强类别可分性的同时保持原始语义结构；supervised audio-visual language contrastive alignment；非线性类别匹配思想                             |

说明：EZ-AVGZSL 论文在本地保存时的文件名为 `EZ-AVGZL论文实验前内容.md`，文件名中是 `AVGZL`，但本文叙述中的方法名称统一写为 `EZ-AVGZSL`。后续检索文件时必须使用磁盘上的实际文件名。

### 0.3 已生成的历史方案文件

下面两个文件记录了当前方案形成前的推导过程，可用于追溯设计依据，但不应替代本文件作为后续写作的主方案。

| 文件性质         | 本地文件名                             | 相对路径                                        | 绝对路径                                                           | 与当前方案的关系                                                                                                       |
| ---------------- | -------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| 第一阶段融合方案 | `AVGZSL_Semi-IIN融合方案.md`         | `论文方案/AVGZSL_Semi-IIN融合方案.md`         | `C:\codex-workplace\论文方案\AVGZSL_Semi-IIN融合方案.md`         | 记录将 Semi-IIN 的 intra/inter masked attention 和 dynamic gate 迁移到 AVGZSL 的早期方案，是当前挑战3的来源            |
| 第二阶段扩展方案 | `AVGZSL_SemiIIN_QATIGER_扩展方案.md` | `论文方案/AVGZSL_SemiIIN_QATIGER_扩展方案.md` | `C:\codex-workplace\论文方案\AVGZSL_SemiIIN_QATIGER_扩展方案.md` | 在第一阶段基础上引入 QA-TIGER 的语义感知早期融合和多高斯专家；当前方案将其中原挑战1和挑战2合并，并进一步引入 EZ-AVGZSL |

当前方案的演化关系为：

```text
AVGZSL baseline
    + Semi-IIN 的模态内/模态间分离交互与动态门控
    -> AVGZSL_Semi-IIN融合方案.md
    + QA-TIGER 的语义感知早期融合与多高斯时间专家
    -> AVGZSL_SemiIIN_QATIGER_扩展方案.md
    + EZ-AVGZSL 的判别性类别原型优化与监督式语义对齐
    -> AVGZSL_SemiIIN_QATIGER_EZAVGZSL_新扩展方案.md（当前确定方案）
```

### 0.4 新对话的推荐读取顺序

为了在新的对话中快速恢复完整上下文，建议按以下顺序读取文件：

1. 先读取当前主方案：`论文方案/AVGZSL_SemiIIN_QATIGER_EZAVGZSL_新扩展方案.md`。
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
请先读取“C:\codex-workplace\论文方案\AVGZSL_SemiIIN_QATIGER_EZAVGZSL_新扩展方案.md”，它是已经确定采用的论文方案。论文来源和历史方案的文件索引记录在该文件第0节，所有材料均位于“C:\codex-workplace\论文方案”目录。后续工作请以 DiSAGE-IIG-AVGZSL 为唯一主方案，不重新拆分三个核心挑战，并严格保持 inductive AVGZSL 中不使用 unseen 类音视频训练样本的设定。在继续写作前，可按第0.4节的顺序读取相关论文文件。
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

## 5. 给导师审核的简洁版挑战表述

### 挑战1：类别语义没有有效引导时序证据发现

音视频类别通常只在视频的部分时间段中表现明显，而现有方法常把类别文本只作为最后分类时的匹配原型，导致模型在特征提取阶段缺少语义引导。本文拟将类别语义提前注入音视频序列编码，并使用多高斯专家连续定位与候选类别相关的视觉帧和音频片段，从而减少无关时序信息对未见类识别的干扰。

### 挑战2：类别文本原型语义相关但分类可分性不足

预训练文本嵌入能够表达类别之间的语义关系，但并不一定适合直接作为 AVGZSL 的分类原型，尤其容易混淆相似动作或相似声音类别。本文拟借鉴 EZ-AVGZSL，优化一组判别性类别语义原型，在扩大类别间距离的同时保留原始语义关系，使其更适合作为未见类迁移和音视频对齐的桥梁。

### 挑战3：音频与视觉弱相关时，简单融合容易产生模态干扰

真实视频中音频和视觉可能不同步或语义不一致，直接拼接容易引入噪声并形成固定模态偏置。本文拟分离建模模态内线索和模态间互补信息，再通过动态门控根据样本和类别自适应融合，从而提高音视频表示的鲁棒性和泛化能力。

## 6. 总体框架

给定一个视频样本，本文框架包含六个阶段：

1. **音视频序列特征提取**：使用 CLIP 提取视觉帧序列特征，使用 CLAP 提取音频片段序列特征。
2. **多粒度类别语义构建**：由类别名称、动作描述、声音属性、场景上下文和易混类别差异构建原始类别语义原型。
3. **判别性类别原型优化**：借鉴 EZ-AVGZSL，在保持语义结构的同时增强类别原型可分性。
4. **语义感知早期融合与高斯时间定位**：借鉴 QA-TIGER，将类别语义作为查询信号注入音视频序列，并通过多高斯专家定位类别相关片段。
5. **模态内/模态间分离交互**：借鉴 Semi-IIN-like 方案，分别建模模态内部时序关系和跨模态互补关系。
6. **动态融合与语义对齐分类**：通过门控机制融合多类信息，并用监督式文本-音视频对比目标完成 seen/unseen 共享语义空间对齐。

## 7. 方法

### 7.1 问题定义

在音频-视觉广义零样本学习（Audio-Visual Generalized Zero-Shot Learning, AVGZSL）任务中，类别被划分为已见类别集合 $\mathcal{Y}^{s}$ 和未见类别集合 $\mathcal{Y}^{u}$，且二者互不相交：

$$
\mathcal{Y}
=
\mathcal{Y}^{s}\cup\mathcal{Y}^{u},
\qquad
\mathcal{Y}^{s}\cap\mathcal{Y}^{u}
=
\varnothing .
\tag{1}
$$

模型只能利用已见类别的音视频样本进行训练。训练集表示为

$$
\mathcal{D}^{s}
=
\left\{
\left(X_i^{v},X_i^{a},y_i\right)
\right\}_{i=1}^{N},
\qquad
y_i\in\mathcal{Y}^{s},
\tag{2}
$$

其中，$X_i^{v}$ 和 $X_i^{a}$ 分别表示第 $i$ 个样本的视觉序列与音频序列，$y_i$ 为其类别标签。与普通零样本学习不同，广义零样本学习的测试样本同时来自已见类别和未见类别。因此，模型不仅需要将在已见类别上学习到的视听知识迁移到未见类别，还必须保留对已见类别的识别能力。测试阶段的预测目标为

$$
\hat y_i
=
\arg\max_{c\in\mathcal{Y}^{s}\cup\mathcal{Y}^{u}}
s_{i,c},
\tag{3}
$$

其中，$s_{i,c}$ 表示第 $i$ 个音视频样本与候选类别 $c$ 的匹配分数。训练期间不存在任何未见类别的音频或视觉样本，但所有类别的名称及类别级文本描述均可使用，这些语义信息构成知识从已见类别迁移到未见类别的桥梁。

### 7.2 总体结构

现有基于预训练大多模态模型的 AVGZSL 方法通常先将音频和视觉编码为类别无关的全局表示，再在分类阶段与类别文本嵌入进行匹配。该范式有效利用了 CLIP 和 CLAP 的跨模态知识，但仍存在三个相互关联的问题。首先，简短类别名称及其预训练嵌入并非专门针对当前类别集合优化，语义相近类别可能缺少清晰的分类间隔。其次，动作或声音事件往往只出现在视频的局部时间段，如果类别语义仅参与最终匹配，背景帧、静音片段和无关事件可能已经被聚合到全局表示中。最后，真实视频中的音频与视觉并不总是同步或语义一致，直接融合容易使一个模态中的噪声干扰另一个模态。

针对上述问题，本文在 *Audio-Visual Generalized Zero-Shot Learning using Pre-Trained Large Multi-Modal Models* 的预训练特征与共享语义空间框架上，提出一个类别语义驱动的音视频学习方法。该方法的核心思想是将类别语义从最终分类时的被动匹配原型，转化为贯穿时序证据发现、模态关系建模和最终预测的主动条件信号。

整体框架由三个相互衔接的模块组成。首先，判别性多粒度类别语义模块利用类别名称、动作过程、声音属性和场景信息建立类别语义，并在保持类别关系的同时扩大易混类别之间的间隔，使模型明确“需要寻找什么”。随后，语义条件多高斯时序证据发现模块将优化后的类别语义分别注入视觉和音频序列，通过多个连续高斯窗口定位与候选类别相关的时间区域，回答“相关证据出现在哪里”。最后，模态内–模态间解耦交互模块在筛选后的时序证据上分别学习单模态稳定模式和跨模态互补关系，并根据候选类别动态判断“当前预测应当依赖哪类证据”。融合表示最终被映射到类别语义空间，在全部已见类别和未见类别上完成统一预测。

这三个模块并不是彼此独立的功能堆叠。判别性语义原型为时间定位提供可靠查询；时间定位为模态交互过滤无关片段；模态关系分解和动态融合则将筛选后的证据组织成适合语义对齐的音视频表示。由此形成“类别语义—时间证据—模态关系—语义预测”的完整计算链路。

### 7.3 预训练音视频表示与多粒度类别语义

#### 7.3.1 音视频序列表示

为了保留动作和声音事件的时间变化，将每个视频划分为 $T$ 个不重叠且时间对齐的片段，每个时间位置包含对应的视觉内容和音频内容。本文沿用基础 AVGZSL 工作使用预训练大多模态模型提取特征的思想，分别采用冻结的 CLIP 图像编码器和 CLAP 音频编码器处理两种模态：

$$
f_{i,t}^{v}
=
E_{\mathrm{CLIP}}^{\mathrm{img}}
\left(x_{i,t}^{v}\right),
\qquad
f_{i,t}^{a}
=
E_{\mathrm{CLAP}}^{\mathrm{aud}}
\left(x_{i,t}^{a}\right),
\qquad
t=1,\ldots,T.
\tag{4}
$$

其中，$f_{i,t}^{v}\in\mathbb{R}^{d_v}$ 和 $f_{i,t}^{a}\in\mathbb{R}^{d_a}$ 分别表示第 $t$ 个片段的视觉特征和音频特征。由于两个编码器的输出维度不同，使用独立的投影网络将其映射到统一的 $d$ 维空间，并加入模态类型嵌入和位置编码：

$$
v_{i,t}
=
P_vf_{i,t}^{v}
+e_v+p_t,
\qquad
a_{i,t}
=
P_af_{i,t}^{a}
+e_a+p_t.
\tag{5}
$$

由此得到视觉序列 $V_i=[v_{i,1},\ldots,v_{i,T}]\in\mathbb{R}^{T\times d}$ 和音频序列 $A_i=[a_{i,1},\ldots,a_{i,T}]\in\mathbb{R}^{T\times d}$。与直接提取单个全局特征相比，序列表示能够保留动作开始、持续和结束以及声音强度变化等时间信息，为后续局部证据发现提供基础。

#### 7.3.2 多粒度类别语义

类别名称通常只能提供概括性的语义。例如，“playing basketball”和“slam dunk”具有相似的语言含义，但后者包含更具体的起跳和扣篮过程；一些视觉相似的事件也需要根据声音特征加以区分。仅使用类别名称难以告诉模型应该在音视频中寻找哪些具体证据。

为此，本文为每个类别 $c$ 构建多粒度描述集合：

$$
\mathcal{P}_c
=
\left\{
p_c^{\mathrm{name}},
p_c^{\mathrm{act}},
p_c^{\mathrm{sound}},
p_c^{\mathrm{scene}},
p_c^{\mathrm{object}},
p_c^{\mathrm{diff}}
\right\}.
\tag{6}
$$

其中，各描述分别对应类别名称、动作过程、声音属性、典型场景、关键主体或物体，以及与易混类别之间的差异。所有类别均采用相同的固定提示模板生成和整理描述，避免为未见类别引入额外的样本级信息。

考虑到 CLIP 文本编码器更关注视觉相关语义，而 CLAP 文本编码器更关注声音相关语义，分别对每条描述进行编码，并将两种文本表示融合为统一的描述级语义：

$$
q_{c,k}
=
\operatorname{Norm}
\left(
W_t
[
E_{\mathrm{CLIP}}^{\mathrm{txt}}(p_{c,k});
E_{\mathrm{CLAP}}^{\mathrm{txt}}(p_{c,k})
]
+b_t
\right).
\tag{7}
$$

将同一类别的全部描述保留为语义 token 集合

$$
Q_c
=
[q_{c,1};\ldots;q_{c,K_p}]
\in
\mathbb{R}^{K_p\times d},
\tag{8}
$$

其中，$K_p$ 为描述数量。进一步对描述级语义进行聚合，得到类别级初始原型：

$$
t_c
=
\operatorname{Norm}
\left(
\frac{1}{K_p}
\sum_{k=1}^{K_p}
q_{c,k}
\right).
\tag{9}
$$

这里保留两层语义表示：$Q_c$ 描述动作、声音和场景等局部属性，供后续时序片段选择不同的语义线索；$t_c$ 表示类别的整体含义，用于构建全局类别空间。多粒度语义解决了类别名称表达过于粗糙的问题，但这些预训练语义仍然未必具有适合当前分类任务的类别间隔，因此下一步需要进一步优化其判别结构。

### 7.4 判别性类别语义原型学习

预训练文本嵌入能够使语义相关的类别在表示空间中保持接近，这种结构是零样本知识迁移的重要基础。然而，语义相关并不等同于适合分类。例如，“playing guitar”和“playing violin”理应具有较高的语义相似度，但如果二者原型过于接近，它们会产生相似的时间查询和分类边界，从而增加混淆风险。

受 EZ-AVGZSL 类别嵌入优化思想启发，本文在初始语义 $t_c$ 的基础上学习兼具类别可分性和语义保持能力的判别性原型。令可优化向量 $u_c$ 由 $t_c$ 初始化，并进行单位化：

$$
u_c\leftarrow t_c,
\qquad
w_c
=
\frac{u_c}{\lVert u_c\rVert_2},
\qquad
c\in\mathcal{Y}^{s}\cup\mathcal{Y}^{u}.
\tag{10}
$$

为了提高最容易混淆类别之间的可分性，类别分离损失关注每个类别的最近邻：

$$
\mathcal{L}_{\mathrm{sep}}
=
\frac{1}{|\mathcal{Y}|}
\sum_{c\in\mathcal{Y}}
\left[
m_{\mathrm{sep}}
-
\min_{j\neq c}
\lVert w_c-w_j\rVert_2
\right]_{+}.
\tag{11}
$$

仅扩大类别距离会破坏原始文本空间中的语义关系，使模型失去从已见类别迁移到未见类别的依据。令 $d_{c,i}^{t}=\lVert t_c-t_i\rVert_2$ 和 $d_{c,i}^{w}=\lVert w_c-w_i\rVert_2$，若类别 $c$ 在初始空间中更接近类别 $i$ 而不是类别 $j$，优化后的空间也应保持相同顺序。因此，语义结构保持损失定义为

$$
\mathcal{L}_{\mathrm{sem}}
=
\frac{1}{|\mathcal{R}|}
\sum_{(c,i,j)\in\mathcal{R}}
\left[
m_{\mathrm{sem}}
+d_{c,i}^{w}
-d_{c,j}^{w}
\right]_{+},
\qquad
\mathcal{R}
=
\left\{
(c,i,j)\mid d_{c,i}^{t}<d_{c,j}^{t}
\right\}.
\tag{12}
$$

综合类别分离和语义结构保持，原型优化目标为

$$
\mathcal{L}_{\mathrm{proto}}
=
\lambda_{\mathrm{sep}}\mathcal{L}_{\mathrm{sep}}
+
\lambda_{\mathrm{sem}}\mathcal{L}_{\mathrm{sem}}.
\tag{13}
$$

该阶段只利用全部类别的文本描述进行优化，不使用任何未见类别的音频或视觉样本。优化完成后得到 $w_c^{\ast}$，并在音视频主网络训练期间保持固定。为了同时利用类别级判别方向和描述级细粒度属性，构建后续模块使用的类别语义库：

$$
B_c
=
[
P_sw_c^{\ast};
P_dq_{c,1};
\ldots;
P_dq_{c,K_p}
]
\in
\mathbb{R}^{(K_p+1)\times d}.
\tag{14}
$$

其中，$w_c^{\ast}$ 表示模型需要寻找的整体类别概念，$Q_c$ 则进一步说明该概念可能以何种动作、声音和场景形式出现。判别性语义库使模型明确了“需要寻找什么”，但尚未指出相关事件位于音视频序列的哪个位置，因此需要进一步进行类别条件的时间证据发现。

### 7.5 语义引导的多高斯时序证据发现

动作或声音事件通常只出现在视频的局部时间段。例如，一个较长视频中可能只有少数片段包含完整动作，其余部分是准备动作、背景或无关内容。如果先对所有片段进行全局池化，再与类别原型匹配，局部判别证据容易被大量无关信息稀释。

受 QA-TIGER 问题感知时序建模思想启发，本文将候选类别语义视为模型需要从音视频中回答的语义查询。与直接进行音视频交叉融合不同，本阶段先使用同一类别语义分别调制视觉和音频序列，在保留两种模态自身信息的同时确定各自与候选类别的相关性。真正的跨模态交互留到后续 Inter 分支中完成，从而避免模态内信息在进入 Intra 分支前被提前混合。

#### 7.5.1 类别语义早期注入

对于候选类别 $c$，首先通过自注意力建模每个模态内部的时间上下文，再使用类别语义库 $B_c$ 重新评估各时间位置：

$$
X_{i,c}^{v}
=
\operatorname{LN}
\left(
V_i
+\operatorname{SA}(V_i)
+\operatorname{CA}(V_i,B_c,B_c)
\right),
\tag{15}
$$

$$
X_{i,c}^{a}
=
\operatorname{LN}
\left(
A_i
+\operatorname{SA}(A_i)
+\operatorname{CA}(A_i,B_c,B_c)
\right).
\tag{16}
$$

其中，$\operatorname{SA}$ 和 $\operatorname{CA}$ 分别表示多头自注意力和多头交叉注意力。由于 $B_c$ 同时包含全局判别原型和多粒度属性 token，不同视觉帧或音频片段可以关注不同的类别信息。经过该过程后，同一个样本面对不同候选类别会得到不同的视觉和音频序列表示，但两种模态尚未相互混合，从而保留后续模态内外关系分解所需的清晰输入。

#### 7.5.2 多高斯时间专家

语义注入能够判断各片段与候选类别的相关性，但动作和声音通常具有连续的时间结构。关键证据可能持续一段时间，也可能分布在动作开始、主体交互和动作结束等多个阶段。单一时间窗口难以覆盖这种复杂过程，而离散选择又容易破坏事件的连续性。

为此，本文分别为视觉和音频生成多个语义条件高斯专家。首先，使用判别性类别原型从各模态序列中聚合类别相关上下文：

$$
h_{i,r}^{c}
=
\operatorname{CA}
\left(
P_qw_c^{\ast},
X_{i,c}^{r},
X_{i,c}^{r}
\right),
\qquad
r\in\{v,a\}.
\tag{17}
$$

对于第 $e$ 个高斯专家，以均匀分布在时间轴上的位置 $b_e=(e-\tfrac{1}{2})/E$ 为初始中心，并由类别上下文预测中心偏移和宽度：

$$
\mu_{i,r,e}^{c}
=
b_e
+\Delta_e
\tanh
\left(
\phi_{\mu}^{r,e}
[h_{i,r}^{c};w_c^{\ast}]
\right),
\tag{18}
$$

$$
\sigma_{i,r,e}^{c}
=
\sigma_{\min}
+
(\sigma_{\max}-\sigma_{\min})
\operatorname{sigmoid}
\left(
\phi_{\sigma}^{r,e}
[h_{i,r}^{c};w_c^{\ast}]
\right).
\tag{19}
$$

均匀初始中心使不同专家从不同时间区域开始搜索，语义条件偏移则使其逐渐移动到对当前类别更有判别力的位置。令归一化时间坐标为 $\tau_t=(t-\tfrac{1}{2})/T$，第 $e$ 个专家的连续时间权重为

$$
\alpha_{i,r,e}^{c}(t)
=
\frac{
\exp
\left[
-\frac{
(\tau_t-\mu_{i,r,e}^{c})^2
}{
2(\sigma_{i,r,e}^{c})^2
}
\right]
}{
\sum_{t'=1}^{T}
\exp
\left[
-\frac{
(\tau_{t'}-\mu_{i,r,e}^{c})^2
}{
2(\sigma_{i,r,e}^{c})^2
}
\right]
}.
\tag{20}
$$

不同样本所需要的专家并不相同，因此使用 router 根据当前模态上下文和候选类别预测专家权重：

$$
r_{i,r}^{c}
=
\operatorname{Softmax}
\left(
W_r^{r}
[h_{i,r}^{c};w_c^{\ast}]
\right)
\in\mathbb{R}^{E}.
\tag{21}
$$

多个专家共同形成候选类别在该模态上的整体时间相关性：

$$
\omega_{i,r}^{c}(t)
=
\sum_{e=1}^{E}
r_{i,r,e}^{c}
\alpha_{i,r,e}^{c}(t).
\tag{22}
$$

利用该时间分布，一方面增强类别相关的时序 token，另一方面保留直接的局部证据摘要：

$$
\widehat X_{i,c}^{r}(t)
=
\left[
1+\kappa T\omega_{i,r}^{c}(t)
\right]
X_{i,c}^{r}(t),
\tag{23}
$$

$$
z_{i,r}^{G,c}
=
\sum_{t=1}^{T}
\omega_{i,r}^{c}(t)
X_{i,c}^{r}(t).
\tag{24}
$$

多高斯专家能够覆盖同一事件的多个连续阶段，视觉和音频分别预测时间分布，也避免强制两种模态在完全相同的时刻提供证据。经过该模块后，$\widehat X_{i,c}^{v}$ 和 $\widehat X_{i,c}^{a}$ 保留完整的时间结构，但类别相关片段被优先增强；$z_{i,v}^{G,c}$ 和 $z_{i,a}^{G,c}$ 则保存未经深层交互改写的局部证据。时间定位解决了“证据在哪里”的问题，但被筛选出的音频与视觉证据并不总是可靠对应，因此还需要判断这些证据应当通过单模态模式还是跨模态关系进行解释。

### 7.6 模态内–模态间解耦交互与自适应融合

时间定位能够减少背景和无关片段的干扰，却不能保证音频与视觉始终具有一致语义。对于主要依赖动作外观的类别，过强的跨模态融合可能引入背景声音；对于声音特征明显的类别，视觉遮挡也可能削弱联合表示。基于 Semi-IIN 的模态内外分离思想，本文在高斯增强后的时序证据上建立两个并行分支：Intra 分支学习各模态内部的稳定模式，Inter 分支学习音频与视觉之间的互补关系。

#### 7.6.1 Intra-Inter Masked Attention

为了避免音频和视觉通过共享聚合 token 在 Intra 分支中间接交换信息，Intra 分支分别设置音频聚合 token $z_{\mathrm{cls}}^{a}$ 和视觉聚合 token $z_{\mathrm{cls}}^{v}$；Inter 分支则使用一个联合聚合 token $z_{\mathrm{cls}}^{av}$。两个分支的输入分别为

$$
Z_{i,c}^{I,0}
=
[
z_{\mathrm{cls}}^{a};
\widehat X_{i,c}^{a};
z_{\mathrm{cls}}^{v};
\widehat X_{i,c}^{v}
],
\qquad
Z_{i,c}^{X,0}
=
[
z_{\mathrm{cls}}^{av};
\widehat X_{i,c}^{a};
\widehat X_{i,c}^{v}
].
\tag{25}
$$

在 Intra 分支中，将音频聚合 token 与音频序列视为一个组，将视觉聚合 token 与视觉序列视为另一个组。注意力只在同一组内部开放：

$$
M_I(p,q)
=
\begin{cases}
0, & g(p)=g(q),\\
-\infty, & g(p)\neq g(q),
\end{cases}
\tag{26}
$$

其中，$g(\cdot)\in\{a,v\}$ 表示 token 所属的模态组。该块对角结构确保音频和视觉在 Intra 分支中不会直接或间接交换信息。

在 Inter 分支中，普通音频 token 只与视觉 token 交互，普通视觉 token 只与音频 token 交互，联合聚合 token 可以访问全部序列：

$$
M_X(p,q)
=
\begin{cases}
0, & p=0\ \text{或}\ q=0,\\
0, & \operatorname{mod}(p)\neq\operatorname{mod}(q),\\
-\infty, & \text{其他情况}.
\end{cases}
\tag{27}
$$

对于分支 $b\in\{I,X\}$，第 $l$ 层带掩码的注意力更新过程为

$$
\widetilde Z_b^{l}
=
Z_b^{l-1}
+
\operatorname{Softmax}
\left(
\frac{Q_bK_b^{\top}}{\sqrt{d_k}}
+M_b
\right)V_b,
\tag{28}
$$

$$
Z_b^{l}
=
\widetilde Z_b^{l}
+
\operatorname{FFN}_b
\left(
\operatorname{LN}(\widetilde Z_b^{l})
\right),
\qquad
l=1,\ldots,L.
\tag{29}
$$

经过 $L$ 层交互后，Intra 分支分别读取音频和视觉聚合 token，再将二者融合为模态内表示；Inter 分支读取联合聚合 token：

$$
z_{i,c}^{I}
=
P_I
[
Z_I^{L}[0];
Z_I^{L}[T+1]
],
\qquad
z_{i,c}^{X}
=
P_XZ_X^{L}[0].
\tag{30}
$$

其中，$z_{i,c}^{I}$ 保留声音事件自身的变化和视觉动作自身的演化，$z_{i,c}^{X}$ 则描述声音与画面之间的相互验证和互补关系。

#### 7.6.2 语义感知动态融合

Intra 和 Inter 分支经过深层注意力后能够形成较强的关系表示，但局部且短暂的高斯时间证据可能在多层交互过程中被稀释。因此，本文保留一条直接高斯证据分支，将视觉和音频的局部摘要融合为

$$
z_{i,c}^{G}
=
P_G
[
z_{i,v}^{G,c};
z_{i,a}^{G,c};
z_{i,v}^{G,c}\odot z_{i,a}^{G,c};
|z_{i,v}^{G,c}-z_{i,a}^{G,c}|
].
\tag{31}
$$

三类表示分别回答不同问题：$z_{i,c}^{I}$ 描述每个模态自身提供了什么稳定线索，$z_{i,c}^{X}$ 描述音频和视觉之间是否形成互补证据，$z_{i,c}^{G}$ 则保留被时间专家直接定位的局部响应。由于不同样本和类别对三类信息的依赖不同，使用候选类别语义共同预测门控权重：

$$
[
\gamma_{i,c}^{I},
\gamma_{i,c}^{X},
\gamma_{i,c}^{G}
]
=
\operatorname{Softmax}
\left(
G_{\gamma}
[
z_{i,c}^{I};
z_{i,c}^{X};
z_{i,c}^{G};
w_c^{\ast}
]
\right).
\tag{32}
$$

最终类别条件音视频表示为

$$
z_{i,c}
=
\gamma_{i,c}^{I}z_{i,c}^{I}
+
\gamma_{i,c}^{X}z_{i,c}^{X}
+
\gamma_{i,c}^{G}z_{i,c}^{G}.
\tag{33}
$$

当音频和视觉具有可靠对应关系时，模型可以提高 Inter 分支的权重；当跨模态关系较弱时，模型能够更多依赖 Intra 分支或高斯分支。至此，模型已经完成从类别语义到局部证据，再到模态关系和最终融合的完整编码过程。下一步需要将该类别条件音视频表示映射回统一语义空间，以实现对未见类别的知识迁移。

### 7.7 音视频—语言对齐与模型优化

本文沿用预训练大多模态 AVGZSL 的共享嵌入空间思想，将类别条件音视频表示和判别性类别原型分别投影为

$$
\theta_{i,c}^{o}
=
\operatorname{Norm}
(W_oz_{i,c}),
\qquad
\theta_c^{w}
=
\operatorname{Norm}
(W_ww_c^{\ast}).
\tag{34}
$$

其中，$\theta_{i,c}^{o}$ 表示样本 $i$ 在候选类别 $c$ 引导下形成的音视频表示，$\theta_c^{w}$ 表示对应的类别语义锚点。二者的匹配分数定义为

$$
s_{i,c}
=
\frac{
(\theta_{i,c}^{o})^{\top}\theta_c^{w}
}{
\tau
},
\tag{35}
$$

其中，$\tau$ 为温度系数。训练阶段对每个已见类别 $c\in\mathcal{Y}^{s}$ 计算类别条件分数，并使用监督式音视频—语言对齐目标：

$$
\mathcal{L}_{\mathrm{AVLA}}
=
-\frac{1}{N}
\sum_{i=1}^{N}
\log
\frac{
\exp(s_{i,y_i})
}{
\sum_{c\in\mathcal{Y}^{s}}
\exp(s_{i,c})
}.
\tag{36}
$$

该损失使音视频表示接近真实类别语义，并远离其他已见类别原型。为了延续基础 AVGZSL 框架中的显式语义约束，进一步加入回归损失：

$$
\mathcal{L}_{\mathrm{reg}}
=
\frac{1}{N}
\sum_{i=1}^{N}
\left\|
\theta_{i,y_i}^{o}
-
\theta_{y_i}^{w}
\right\|_2^2.
\tag{37}
$$

同时，使用音视频解码器 $D_o$ 和文本解码器 $D_w$ 重构优化前的初始类别语义，减少共同空间映射过程中的语义信息损失：

$$
\mathcal{L}_{\mathrm{rec}}
=
\frac{1}{N}
\sum_{i=1}^{N}
\left(
\left\|
D_o(\theta_{i,y_i}^{o})-t_{y_i}
\right\|_2^2
+
\left\|
D_w(\theta_{y_i}^{w})-t_{y_i}
\right\|_2^2
\right).
\tag{38}
$$

为使多个高斯专家覆盖不同时间区域，加入中心分散约束：

$$
\mathcal{L}_{\mathrm{div}}
=
\frac{1}{N}
\sum_{i=1}^{N}
\sum_{r\in\{v,a\}}
\sum_{e<e'}
\exp
\left(
-\frac{
|\mu_{i,r,e}^{y_i}-\mu_{i,r,e'}^{y_i}|
}{\eta}
\right).
\tag{39}
$$

主网络的训练目标为

$$
\mathcal{L}_{\mathrm{main}}
=
\mathcal{L}_{\mathrm{AVLA}}
+
\lambda_{\mathrm{reg}}\mathcal{L}_{\mathrm{reg}}
+
\lambda_{\mathrm{rec}}\mathcal{L}_{\mathrm{rec}}
+
\lambda_{\mathrm{div}}\mathcal{L}_{\mathrm{div}}.
\tag{40}
$$

整体训练分为两个阶段。第一阶段仅利用全部已见类别和未见类别的文本描述优化 $\mathcal{L}_{\mathrm{proto}}$，获得稳定的判别性原型 $w_c^{\ast}$。第二阶段固定这些类别原型，仅使用已见类别音视频样本优化 $\mathcal{L}_{\mathrm{main}}$。这种训练方式使未见类别只通过类别级语义参与知识空间构建，不会接触任何未见类别音视频数据，符合 AVGZSL 的标准设置。

### 7.8 广义零样本推理

测试阶段，对每个候选类别 $c\in\mathcal{Y}^{s}\cup\mathcal{Y}^{u}$ 依次使用其判别性语义原型引导音视频编码，并根据式（35）计算统一匹配分数。由于广义零样本模型容易偏向训练期间出现过的类别，采用 calibrated stacking 对已见类别分数进行校准：

$$
s_{i,c}^{\mathrm{cal}}
=
s_{i,c}
-
\delta\,
\mathbb{I}
[c\in\mathcal{Y}^{s}],
\tag{41}
$$

最终预测为

$$
\hat y_i
=
\arg\max_{c\in\mathcal{Y}^{s}\cup\mathcal{Y}^{u}}
s_{i,c}^{\mathrm{cal}}.
\tag{42}
$$

其中，$\delta$ 通过独立验证集确定。至此，类别语义在整个方法中承担了统一角色：它首先建立具有判别性的类别空间，随后引导模型定位相关时间证据、调节模态关系，并最终作为已见类别和未见类别共享的分类锚点完成预测。

## 8. EZ-AVGZSL 创新点融入后的合理性

原 `AVGZSL_SemiIIN_QATIGER_扩展方案.md` 已经解决了两个问题：类别语义如何提前引导音视频序列，以及如何通过高斯专家定位类别相关片段。但该方案默认类别语义原型本身是可靠的，没有进一步处理类别文本嵌入的分类可分性问题。

EZ-AVGZSL 的关键价值恰好补上这一点：

1. **类别语义更适合作为查询信号**：如果类别原型之间距离过近，那么 semantic-aware fusion 和 Gaussian experts 可能对相似类别产生相似的时间关注模式。判别性原型优化可以让不同类别查询更清晰。
2. **类别语义更适合作为分类原型**：AVGZSL 最终仍需要在 seen/unseen 类之间进行匹配。优化后的原型能缓解未见类边界模糊问题。
3. **语义结构仍然可迁移**：通过 ranking-based semantic preservation，模型不会单纯把所有类别均匀推开，而是保留原始语言空间中的相对语义关系，这对于未见类迁移至关重要。
4. **训练目标更简洁**：监督式文本-音视频对比学习可以作为主对齐目标，减少对复杂重构模块的依赖，也更容易和本文的 class-conditioned 表示结合。

因此，EZ-AVGZSL 不应被理解为额外堆叠的模块，而应作为整套方案的语义基础层：先让类别原型变得更判别，再用它引导时序定位、模态交互和最终分类。

## 9. 预期论文贡献写法

### 中文贡献表述

1. 本文提出一种判别语义增强的音视频广义零样本学习框架，将类别文本语义从最终分类原型扩展为贯穿特征编码、时序定位和跨模态融合的语义条件信号。
2. 本文设计类别语义引导的多高斯专家时序证据发现模块，将 QA-TIGER 中的问题引导时间建模迁移为类别语义引导时间建模，实现对关键视觉帧和音频片段的连续软定位。
3. 本文引入判别性类别语义原型优化，在扩大类别间可分性的同时保持原始语言空间中的语义关系，从而增强 seen/unseen 类之间的知识迁移能力。
4. 本文结合模态内/模态间 masked attention 与动态门控机制，自适应融合模态内部稳定线索、跨模态互补信息和高斯时序证据，缓解音视频弱相关带来的模态干扰。

### 英文贡献表述

1. We propose a discriminative semantic-aware audio-visual GZSL framework that upgrades class semantics from passive classification prototypes to active conditional signals for feature encoding, temporal grounding, and cross-modal fusion.
2. We introduce semantic-conditioned Gaussian temporal experts to softly localize class-relevant visual frames and audio segments, adapting question-guided temporal reasoning to generalized zero-shot audio-visual recognition.
3. We incorporate discriminative class prototype optimization to improve class separability while preserving the semantic topology of language embeddings, thereby strengthening seen-to-unseen knowledge transfer.
4. We combine intra-/inter-modal masked attention with dynamic gating to adaptively balance modality-specific cues, cross-modal complementary information, and Gaussian-grounded temporal evidence.

## 10. 实验与消融设计

### 10.1 主实验

建议在以下 AVGZSL 数据集上进行实验：

- VGGSound-GZSL
- UCF-GZSL
- ActivityNet-GZSL

评价指标包括：

- Seen accuracy
- Unseen accuracy
- Harmonic Mean

核心对比方法包括：

- 原 AVGZSL baseline
- EZ-AVGZSL
- Semi-IIN-like 序列版 AVGZSL
- `AVGZSL_SemiIIN_QATIGER_扩展方案.md` 中的 SAGE-IIG-AVGZSL
- 本文 DiSAGE-IIG-AVGZSL

### 10.2 消融实验

建议至少包含以下消融：

1. 去掉判别性类别原型优化，直接使用原始 CLIP/CLAP 文本原型。
2. 只使用 $\mathcal{L}_{sep}$，不使用语义保持约束。
3. 只使用语义保持约束，不使用类别分离约束。
4. 使用 proximity semantic preservation 与 ranking semantic preservation 的对比。
5. 去掉 semantic-aware early fusion，只在最终分类阶段使用类别语义。
6. 去掉 Gaussian experts，改为 average pooling。
7. 单 Gaussian expert 与多 Gaussian experts 对比。
8. 共享音频/视觉 Gaussian experts 与模态独立 Gaussian experts 对比。
9. 去掉 Intra-modal Masked Attention。
10. 去掉 Inter-modal Masked Attention。
11. 去掉 dynamic gate，改为固定权重融合。
12. 余弦相似度与 non-linear cross-attention similarity 对比。

### 10.3 可视化分析

建议展示：

1. 类别原型优化前后的 t-SNE/UMAP 分布，证明类别间可分性提升。
2. 类别原型优化前后的 nearest neighbor 关系，证明语义结构没有被严重破坏。
3. 不同候选类别下的 Gaussian temporal masks，证明模型能根据类别语义关注不同时间片段。
4. 音频和视觉 Gaussian masks 的差异，证明模态独立时间定位的必要性。
5. Dynamic gate value distribution，证明模型会根据类别和样本动态调整模态内/模态间信息权重。

## 11. 风险与实现建议

### 11.1 主要风险

1. **类别原型优化可能过度分离**：如果 $\alpha$ 过大，类别语义关系可能被破坏，影响未见类迁移。需要通过 nearest neighbor 分析和 unseen accuracy 共同验证。
2. **class-conditioned encoding 计算量较高**：每个候选类别都参与语义融合和高斯定位，推理复杂度较高。可以使用 Top-M reranking 降低成本。
3. **LLM 生成描述质量不稳定**：类别描述应采用固定模板和人工检查，避免引入与类别无关或过度具体的信息。
4. **高斯专家可能塌缩**：多个专家可能关注相同时间段，需要使用中心分散正则或专家 dropout。

### 11.2 推荐实现顺序

第一阶段：复现或构建原 AVGZSL baseline，保证 CLIP/CLAP 特征和类别文本原型对齐流程可用。
第二阶段：加入 EZ-AVGZSL 风格的类别原型优化，只验证 $\mathcal{L}_{proto}+\mathcal{L}_{AVLC}$ 是否提升 seen/unseen harmonic mean。
第三阶段：加入 semantic-aware early fusion 和 Gaussian temporal experts，验证时序证据发现模块的收益。
第四阶段：加入 Intra/Inter Masked Attention 和 dynamic gate，验证模态干扰抑制能力。
第五阶段：进行完整消融、可视化和复杂度分析。

### 11.3 最小可行版本

如果希望先快速验证论文创新是否有效，可以从最小版本开始：

```text
CLIP/CLAP sequence features
+ discriminative class prototype optimization
+ semantic-conditioned Gaussian pooling
+ supervised AV-language contrastive loss
```

该版本先不加入复杂的 Intra/Inter 多层 Transformer，只验证两个关键点：

1. 判别性类别原型是否优于原始类别文本嵌入。
2. 语义高斯时间池化是否优于全局平均池化。

若最小版本有效，再逐步加入 Intra/Inter Masked Attention 和 dynamic gate。

## 12. 最终结论

新版 DiSAGE-IIG-AVGZSL 的核心逻辑是：先通过 EZ-AVGZSL 风格的类别原型优化，让类别语义具备更强判别性；再借鉴 QA-TIGER，将判别性类别语义作为查询信号，提前引导音视频序列编码并通过多高斯专家定位类别相关时间片段；最后结合 Semi-IIN-like 的模态内/模态间分离交互和动态门控机制，抑制弱相关音视频带来的模态干扰。

因此，该方案相比原 `AVGZSL_SemiIIN_QATIGER_扩展方案.md` 的主要增强在于：

- 不再只假设类别语义原型天然可靠，而是显式学习更具分类可分性的类别原型。
- 将“语义早期融合”和“高斯时间定位”合并为一个更完整的语义引导时序证据发现问题。
- 形成从类别语义优化、时序证据定位、模态关系建模到最终语义对齐的完整 AVGZSL 论文框架。

## 13. 方法章节重写提示词（记录）

### 13.1 使用说明

下面的提示词用于让 AI 以 `SCER-AVGZSL_方法章节重写版.md` 为内容底稿，以 `理论部分参考.md` 为首要的阐述与语言风格模板，重新撰写论文“方法”章节。目标不是改变已经确定的 SCER-AVGZSL 技术路线，而是在保证公式、符号和 AVGZSL 任务边界正确的前提下，使章节组织、模块引入、公式讲解、段落衔接和中文行文方式与理论参考文档高度接近。使用时可直接复制下面的完整提示词；若 AI 能访问本地文件，应先完整读取所列材料，再开始写作。

### 13.2 可直接使用的完整提示词

```text
你现在是一名长期从事多模态学习、音视频理解和广义零样本学习研究的中文论文作者。请以 `SCER-AVGZSL_方法章节重写版.md` 为待改写的内容底稿，以 `理论部分参考.md` 为最高优先级的写作风格与方法阐述模板，重新撰写完整的中文“方法”章节。必须保留 SCER-AVGZSL 已经确定的科学问题、模块功能、数据流和数学机制，但要显著改变当前偏技术规范式的表达，使方法的章节组织、模块引出、过程叙述、公式前后解释和段落节奏与 `理论部分参考.md` 非常接近。

一、写作前必须完整读取的材料

请按以下顺序完整读取，不要只读取摘要、标题或检索片段：

1. 当前需要改写的 SCER-AVGZSL 方法底稿：
   \\wsl.localhost\Ubuntu-22.04\home\admin\claude-wokeplace\SCER-AVGZSL_方法章节重写版.md
2. 必须重点模仿的方法阐述与语言风格模板：
   C:\codex-workplace\论文方案\理论部分参考.md
3. 当前主方案及研究边界：
   C:\codex-workplace\论文方案\AVGZSL_SemiIIN_QATIGER_EZAVGZSL_新扩展方案.md
4. AVGZSL 任务与基础特征框架：
   C:\codex-workplace\论文方案\Audio-Visual_Generalized_Zero-Shot_Learning.md
5. 类别原型优化与音视频—语言监督对齐的数学依据：
   C:\codex-workplace\论文方案\EZ-AVGZL论文实验前内容.md
6. 语义早期注入与连续高斯时序建模的数学依据：
   C:\codex-workplace\论文方案\QA-TIGER_CVPR2025_完整论文.md
7. 模态内/模态间掩码交互与动态门控的数学依据：
   C:\codex-workplace\论文方案\Semi-IIN论文完整.md

材料的使用优先级必须明确：`SCER-AVGZSL_方法章节重写版.md` 决定本文具体写什么，三篇方法来源论文和 AVGZSL 基线负责校验数学机制，`理论部分参考.md` 决定这些内容应当如何组织、阐述和表达。若语言模仿与数学正确性发生冲突，必须先保证数学和任务设定正确，再用理论参考文档的叙述方式重新表达。不要在最终回答中展示阅读笔记、来源对照表或思维过程。

二、必须保持的研究任务与方法主线

1. 研究任务始终是 Audio-Visual Generalized Zero-Shot Learning（AVGZSL）。训练阶段只能使用已见类别的音视频样本，测试类别来自已见类别与未见类别的并集。
2. 可以使用全部已见/未见类别的类别名称和类别级文本语义，因为它们属于零样本学习允许的侧信息；严禁以任何形式使用未见类别的音频、视频、样本标签、伪标签或样本统计量参与训练。
3. 整体科学主线必须保持为：先建立兼具判别性与语义拓扑保持能力的类别语义空间；再以类别语义为条件，从音频和视觉序列中发现连续且类别相关的局部时序证据；随后分解并建模模态特定关系与跨模态互补关系，根据样本—类别条件自适应融合；最后在统一语义空间中完成训练与 seen/unseen 联合预测。
4. 三个核心模块必须构成明确的因果链，而不是并列堆叠：前一模块的输出必须成为后一模块的必要输入。语义原型负责提供可靠条件查询；时序模块负责过滤和增强类别相关片段；关系建模与融合模块负责组织被筛选的证据；对齐目标负责把最终表示约束回 seen/unseen 共享的类别语义空间。
5. `SCER-AVGZSL_方法章节重写版.md` 是本次改写的直接内容底稿，其中已经形成的公式、模块和数据流应当保留并核验，而不是重新设计另一套方法。若底稿与原文机制、张量维度、AVGZSL 设定或前后数据流冲突，应以“任务边界正确、整体逻辑自洽、原始机制有据可依”为优先级进行修正，并在正文中给出自足的解释。

三、方法正文中禁止出现来源性表述

1. 方法正文不得出现 Semi-IIN、QA-TIGER、EZ-AVGZSL（或 EZ-AVGZL）这三个论文/方法名称，也不得出现其作者、论文标题或“来自某论文”等表述。
2. 不得使用“借鉴……”“受……启发”“沿用……方法”“迁移自……”“类似于……”等相关工作式措辞。三篇论文只在后续“相关工作”章节中讨论；本次方法章节必须把技术写成本文统一框架中的自然组成部分。
3. 不要逐句翻译或大段复述原文。必须理解原始机制和公式后，用本文任务、符号体系和数据流重新组织学术表述，避免形成拼贴感。
4. 可以正常写出 CLIP、CLAP、Transformer、cross-attention、Gaussian distribution 等必要的基础技术名称；必要时也可以为这些通用组件预留规范引用位置，但不要在方法正文中提到上述三篇直接参考论文。

四、方法名称与模块名称

1. 沿用当前底稿已经确定的整体方法名 SCER-AVGZSL，以及三个核心模块名称：类别语义结构校准（CSSC）、类别条件连续时序证据路由（CTER）和可靠性感知交互分解与证据融合（RIDE）。本次任务的重点是重写方法阐述与语言风格，不再重新生成另一套名称。
2. 名称首次进入正文时，按照 `理论部分参考.md` 的写法，在提出模块的完整句子中给出“中文名称（缩写，英文全称）”，随后统一使用中文名称或缩写。例如采用“本文提出类别语义结构校准（CSSC，Class Semantic Structure Calibration）……”的自然句式，而不是先给出独立命名表。
3. 最终方法正文前不得保留“新命名方案表”或“关键设计说明”。其中有价值的功能说明和设计取舍必须自然融入“整体结构”和相应模块段落，不得以表格、清单或方法外说明代替论文叙述。

五、原文描述与数学公式的使用原则

“参考原文”是指保持关键机制的数学内核和成立条件，而不是原封不动复制任务特定符号。请逐项完成以下核验和任务化改写：

1. 类别语义空间部分：以原文中的最近邻类别分离、语义邻域/相对排序保持以及二者的联合优化为数学依据。明确初始文本原型、可学习原型、归一化方式、距离度量、margin 或权衡系数以及优化范围。若采用 ranking-based semantic preservation，必须保证三元组排序方向、符号和 hinge 形式在数学上正确；不要把原文损失随意改成另一种形式而不解释设计含义。
2. 时序证据部分：以原文中的条件语义早期注入、多高斯中心与尺度参数生成、专家路由和加权时序聚合为依据，把 question 条件严格改写为 class-semantic 条件。明确样本索引、候选类别索引、模态索引、时间索引和专家索引，并写清 Gaussian 权重在时间维上的归一化方式。
3. 必须解决“早期跨模态融合”与“后续模态关系分解”之间可能产生的逻辑冲突。若早期阶段已经让音频和视觉完全交叉混合，后续再声称获得纯粹的模态内分支会缺乏依据。请结合当前统一框架选择一致的计算路径：早期阶段重点执行类别语义对各模态的条件化，跨模态关系主要留给后续关系模块；若确实保留早期音视频交叉注意力，则必须精确说明它不会破坏后续分解的原因和信息边界。
4. 模态关系部分：以原文中的两类 attention mask、masked self-attention 更新和动态 gate 为数学依据，重新建立适合“两种模态 + 类别条件时序序列”的掩码矩阵。必须明确聚合 token 是否可跨组访问，避免通过共享 token 造成未声明的间接信息泄漏。写清每个分支输出的语义角色和张量维度。
5. 动态融合部分：门控公式必须与实际分支数量一致。若融合模态特定分支、跨模态分支和直接时序证据分支三个表示，可使用归一化的三路权重；若只融合两个表示，则使用严格对应的二路门控。不要同时使用二路 sigmoid 解释和三路 softmax 公式，却不说明两者差异。
6. 音视频—语言对齐部分：以监督式对比对齐的原始目标为依据，并根据本文是“按全部已见类别计算候选分数”还是“按 batch 构造负类”选择唯一一致的分母定义。不要把 batch-level contrastive loss 与 class-level cross-entropy 混写。若保留回归、重构或高斯多样性正则，必须逐一说明其不可替代作用，并确保总损失中的每一项都在前文定义和实际训练阶段被使用。
7. 不要杜撰原文没有、当前科学问题也不需要的复杂结构。任何必要的新公式都应来自本文统一数据流中的真实运算，并明确说明它相对原始机制为何需要进行 AVGZSL 任务化调整。
8. 所有公式从头连续编号。每个符号必须在首次出现时定义；同一符号全文只能表示一个概念。给出关键张量的维度或所属空间，明确 Softmax 的归一化轴、Norm 的含义、拼接与逐元素运算符、可学习参数以及冻结参数。

六、以理论部分参考为基准的阐述与语言风格（最高优先级）

1. 必须把 `理论部分参考.md` 作为中文行文模板，而不仅是一般性参考。最终正文应在段落组织、句式推进、公式引入和模块衔接上呈现明显相似的写法，同时使用 SCER-AVGZSL 自身的技术内容和符号，不能复制参考文档中的 KAS、AVCE、AKG 等不同方法内容。
2. 方法章节直接从“3 方法”开始，随后依次展开“问题定义”“整体结构”、各核心模块、联合嵌入与损失函数、训练和推理。不要在方法正文之前输出命名表、关键设计说明、来源对照表或 ASCII 数据流图。
3. “问题定义”应先用连续自然段说明零样本学习与广义零样本学习的区别、已见类与未见类的训练/测试关系及知识迁移难点，再给出集合、数据和预测目标。不要一开始连续堆砌多个集合公式；每个公式后用“其中，……”解释变量。
4. “整体结构”应尽量贴近参考文档的两层阐述方式：第一段先指出传统方法或现有范式的具体局限，再说明本文框架由哪些模块组成，并使用“首先、其次、随后、最后”交代处理顺序；第二段从输入视频开始，按实际数据流完整叙述各阶段如何衔接。若已有框架图，可采用“如图 X 所示”的图文衔接方式；若没有确定图号，不得虚构图号。
5. 每个核心模块的首段都采用“问题或局限—本文提出的模块—模块作用”的组织方式。优先使用“为了解决……问题，本文提出/设计……”“具体来说……”等与参考文档相近的学术句式。必要时可使用与 AVGZSL 类别相关的具体例子帮助说明问题，但不得引入未经材料支持的新设定。
6. 模块内部按真实计算顺序展开，使用“首先”“随后”“接着”“最后”等连接词组织步骤。每一步先用一至两句说明操作目的和输入，再以“定义如下”“可表示为”“其计算过程为”等句式引出公式；公式之后立即使用“其中，……”集中定义符号、维度和运算，并补充该结果在本模块中的作用。
7. 不要连续展示多组公式而缺少解释。参考文档中的基本节奏应被保留为“阐述目的 → 给出公式 → 解释符号 → 说明作用 → 进入下一步”。当两个公式属于视觉和音频的严格对称计算时可以并列给出，但随后必须统一解释二者的对应关系。
8. 采用“本文/我们”作为主要叙述主体，多使用“本文提出”“我们构建”“我们采用”“我们利用”“我们将……输入……”等主动表达。减少当前底稿中偏规范文档式的“必须”“严格”“合法”“唯一输入”“信息泄漏”“不可替代”等措辞；只有在说明 AVGZSL 数据边界或关键数学约束时才保留必要的严格限定。
9. 相邻模块之间应通过上一模块的输出自然过渡到下一模块需要解决的问题。例如，在类别语义校准结束时说明所得原型如何指导时序证据发现；在时序路由结束时说明筛选后的视听证据为何仍需进行模态关系建模；在证据融合结束时说明联合表示为何需要投影到共享语义空间。过渡应写成论文正文，而不是“模块 A 是模块 B 的必要输入”式说明。
10. “损失函数”部分采用参考文档的分项叙述方式。每个损失先用加粗小标题和一段话说明优化目的，再给出公式和“其中”解释，最后汇总整体目标。两阶段训练协议在损失函数之后用连续段落说明，不要写成操作手册或检查清单。
11. 章节标题和小标题以简洁中文为主，避免不必要的中英双标题。模块英文全称和缩写只在首次提出时出现。段落长度、信息密度和句子节奏应接近参考文档：以完整解释性段落为主，不把正文切成大量细碎条目，也不使用过度压缩、类似审计报告的表达。
12. “风格非常接近”不等于复制原句，也不等于继承参考文档中的错别字、重复表述、占位符、未定义符号或不严谨公式。必须保留其“先提出问题、再提出模块、随后逐步公式化、最后解释作用”的叙述范式，同时修正语言和数学错误，使成稿达到正式论文标准。

七、必须明确交代的技术细节

1. 给出 seen/unseen 类别集合、训练集和测试目标，明确 inductive AVGZSL 数据边界。
2. 说明视频如何划分为时间片段、视觉和音频特征如何由冻结的预训练编码器获得，以及二者如何映射到共享维度。
3. 说明类别名称或类别级描述如何形成初始语义表示，以及类别级全局原型与属性级语义 token 是否同时保留、分别用于何处。
4. 说明类别原型优化是独立的第一阶段还是与主网络联合训练，并明确优化后原型在主网络阶段是否固定。训练阶段之间不得出现含糊或自相矛盾的参数更新关系。
5. 说明候选类别条件编码在训练和推理时如何计算：训练时参与分数归一化的类别范围是什么，推理时如何覆盖 seen/unseen 全部候选类别；如计算复杂度较高，可在方法末尾客观说明复杂度或可实施的推理策略，但不要擅自改变主算法。
6. 说明音频和视觉的高斯时间分布是否独立预测、多个专家如何避免完全塌缩到同一位置，以及路由权重如何作用于各专家。
7. 说明两类关系分支的 attention 可见性边界、聚合 token 的读取方式、动态权重的条件变量和最终融合表示。
8. 给出完整训练目标、两阶段训练流程和 generalized zero-shot 推理公式。若采用 calibrated stacking，说明校准项只在推理时作用于已见类别分数，且校准系数由不泄漏测试信息的验证协议确定。

八、输出要求

只输出重写后的完整中文“方法”章节，不要输出命名方案表、关键设计说明、提纲、写作建议、来源对照表、风格分析、原文引用说明或尚未填充的占位符。正文必须能够独立阅读，包含连贯段落、完整 LaTeX 公式和连续公式编号。除 CLIP、CLAP、Transformer、Gaussian distribution 等必要的通用技术名称外，全文不得出现三篇直接参考论文的方法名。

九、输出前自检

在提交正文前自行逐项核查，但不要把核查过程输出：

1. 是否只输出方法正文，并删除了命名表、关键设计说明和 ASCII 数据流图。
2. 方法的段落结构、模块引入句式、步骤连接词、公式前后解释和损失分项写法是否与 `理论部分参考.md` 明显接近。
3. 是否保持 SCER-AVGZSL、CSSC、CTER 和 RIDE 的名称、功能及前后数据流，没有擅自重构另一套方法。
4. 每个模块是否按照“具体问题—提出模块—逐步计算—公式解释—作用与过渡”的顺序展开，而不是写成技术规范或设计检查报告。
5. 三篇来源论文名称及“借鉴/受启发/迁移自”等措辞是否已从方法正文中完全删除。
6. 每个公式是否有原始机制依据或明确的任务化必要性，是否不存在符号方向错误、维度错误、归一化轴不明或公式与文字矛盾。
7. 原型优化、主网络训练和推理三个阶段的可用数据、候选类别范围和参数更新关系是否清楚，并严格满足不使用未见类音视频训练数据的 AVGZSL 设定。
8. 是否保留参考文档的叙述风格但修正了其中的错别字、重复表述、占位符和不严谨符号，没有机械复制原句。

如果原始论文公式、当前方案与 SCER 底稿之间存在实质冲突，应在写作前自行完成统一处理，并把处理结果自然写入相应模块，不得在最终正文前额外输出“关键设计说明”。
```
