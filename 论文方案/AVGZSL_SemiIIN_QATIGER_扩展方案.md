# 融合 Semi-IIN-like 序列建模与 QA-TIGER 高斯专家的 Audio-Visual GZSL 扩展方案

## 1. 文档目标

本文件在已有 `Semi-IIN-like 序列版方案` 的基础上，进一步引入 `QA-TIGER_CVPR2025_完整论文.md` 中可迁移的创新点，形成一个更完整、更有创新性的 audio-visual generalized zero-shot learning 方案。

涉及材料：

- `Audio-Visual_Generalized_Zero-Shot_Learning.md`：作为 baseline，核心是 CLIP/CLAP 特征与类别文本语义对齐。
- `Semi-IIN论文完整.md`：提供 intra-modal / inter-modal masked attention 与动态 gate 思想。
- `QA-TIGER_CVPR2025_完整论文.md`：提供 question-aware early fusion 与 temporal Gaussian experts 的连续时间建模思想。
- `AVGZSL_Semi-IIN融合方案.md`：已有 Semi-IIN-like Sequential AVGZSL 方案。

本文提出的新方案可以命名为：

```text
SAGE-IIG-AVGZSL
```

即：

```text
Semantic-Aware Gaussian Expert Intra-Inter Gated Audio-Visual GZSL
```

中文可称为：

```text
语义感知高斯专家增强的 Intra-Inter 门控音视频广义零样本学习
```

## 2. 为什么 QA-TIGER 可以迁移到 AVGZSL

QA-TIGER 原任务是 audio-visual question answering，其核心输入包含视频、音频和自然语言问题。AVGZSL 没有“问题”，但有一个天然的语义条件：类别文本嵌入。

因此可以建立如下对应关系：

| QA-TIGER | AVGZSL 迁移形式 |
| --- | --- |
| question feature | class semantic prototype |
| question-aware fusion | class/semantic-aware fusion |
| question-relevant frames | class-relevant frames |
| Gaussian temporal experts | semantic-conditioned temporal Gaussian experts |
| answer prediction | class semantic nearest-neighbor classification |

迁移的关键不是照搬 QA head，而是把 QA-TIGER 的“问题引导时间定位”改造成“类别语义引导时间定位”。这与 GZSL 是一致的，因为 unseen 类虽然没有训练样本，但仍然有文本类别嵌入，可作为语义查询使用。

## 3. 拟写论文的核心挑战、原因与解决方法

### 挑战1：如何让类别语义主动参与音视频特征学习，而不是只作为最终分类原型？

**原因：**  
音频-视觉广义零样本学习依赖类别语义作为已见类到未见类的知识迁移桥梁。但现有方法通常把文本类别嵌入只作为最终匹配的类别原型：模型先将视频编码成一个类别无关的全局音视频表示，再与类别文本嵌入计算相似度。这种“先编码、后匹配”的范式存在两个问题。第一，类别标签往往只是简短短语，例如 `playing piano`、`basketball dunk`、`wood thrush calling`，无法充分表达视觉动作、声音属性、场景上下文和主体对象等细粒度语义。第二，类别语义没有参与音频片段和视觉帧的早期特征提取，导致模型无法在编码过程中主动寻找“与当前候选类别相关”的时序证据。对于未见类而言，模型没有训练样本，如果语义原型贫乏且只在最后阶段使用，就很难建立稳定的跨类别迁移桥梁。

**方法：**  
本文提出语义感知早期融合机制。首先，将类别语义从单一类别名称扩展为多粒度语义原型：围绕每个类别构建动作描述、声音属性、典型场景、主体对象、上下文关系和易混类别差异等多种文本描述，并可借助大型语言模型生成更丰富的视听语义说明；随后分别通过 CLIP/CLAP 文本编码器提取视觉相关语义和音频相关语义，形成统一类别语义原型 $s^c$。其次，将 $s^c$ 从最终分类阶段前移到音视频序列编码阶段，通过 cross-attention 显式注入视觉帧序列和音频片段序列，生成类别条件的视觉表示 $V_{i,c}^{q}$ 和音频表示 $A_{i,c}^{q}$。这样，同一视频面对不同候选类别时会产生不同的 class-conditioned audio-visual representation。该设计使类别语义从静态分类锚点转变为主动查询信号，既增强未见类语义表征，也保证 seen/unseen 类共享同一套语义引导机制，符合 GZSL 的零样本迁移要求。

### 挑战2：如何在长时序音视频中定位类别相关关键片段，同时避免离散选择破坏时间连续性？

**原因：**  
音频-视觉类别往往只在视频局部时间段中显著出现。视觉上，关键动作、主体物体或场景线索可能只出现在少数帧；音频上，类别相关声音也可能被背景音乐、环境噪声或静音片段稀释。使用中间帧、均匀采样或全局平均池化，会把大量无关片段混入类别表示。离散 Top-K 选择虽然能筛选部分关键帧，但会把时间建模变成硬选择过程，容易破坏连续动作和持续声音事件的时间结构，也可能忽略多个非连续但同样重要的片段。对于 GZSL 中的未见类，模型无法从训练样本中学习该类的时间分布，因此更需要由类别语义驱动的软时间定位机制。

**方法：**  
本文设计语义条件多高斯专家时间建模模块。给定类别语义原型 $s^c$，模型分别为视觉和音频生成多组 Gaussian temporal experts，每个高斯专家在时间轴上形成一个连续 soft mask，用于表示一个可能与当前类别相关的时间区域。多个专家共同覆盖连续或非连续的关键片段，并通过 router 根据类别语义和音视频上下文动态分配专家权重。与 uniform sampling 相比，该机制能突出类别相关时间段；与 Top-K 离散选择相比，高斯权重保留了时间连续性；与单一 attention pooling 相比，多专家结构可以表达复杂的多峰时间分布。同时，视觉和音频分别拥有独立的高斯专家，不强制二者关注同一时间位置，从而适应声音主导、视觉主导或音视频共同决定的不同类别。高斯权重还可作为可解释证据，用于展示模型为某一候选类别关注了哪些视觉帧和音频片段。

### 挑战3：如何分离模态内线索和跨模态互补信息，并动态融合以抑制模态干扰？

**原因：**  
真实视频中的音频和视觉并不总是同步或语义一致。视觉中出现的动作可能没有对应声音，音频中出现的背景音乐也可能与画面主体无关；某些类别主要依赖视觉动作，某些类别主要依赖声音事件，还有一些类别需要音视频共同验证。若直接拼接音频和视觉特征，模型容易把无关模态信息混入类别表示，产生模态干扰。更严重的是，在 GZSL 中模型只从已见类学习融合方式，可能形成固定模态偏置，例如在训练类中过度依赖视觉或音频，从而损害未见类泛化。因此，新模型不仅要建模跨模态互补信息，还要保留模态内部较纯净的动作或声音线索，并能根据类别和样本动态决定融合比例。

**方法：**  
本文引入分离式 intra/inter 交互与动态门控融合。具体来说，Intra-modal Masked Attention 只允许同一模态内部 token 交互，用于建模视觉帧内部的动作变化和音频片段内部的声音变化，保留模态特定信息；Inter-modal Masked Attention 则主要允许音频和视觉 token 之间交互，用于捕获跨模态一致性、互补性和互证关系。随后，结合语义高斯专家定位到的关键片段，构建 Gaussian-enhanced dynamic gate，在样本级和类别级动态融合 $z_{intra}^{c}$、$z_{inter}^{c}$ 和 $z_g^c$。当音视频互补性强时，模型提高跨模态交互权重；当某一模态存在噪声或与类别弱相关时，模型更多依赖模态内线索或高斯定位后的可靠片段。训练上，仍保持以 CLIP/CLAP 类别语义原型为中心的 $L_{ce}+L_{reg}+L_{rec}$ 对齐目标，使增强后的融合表示始终回到共享语义空间。验证上，可通过去除 IntraMA、InterMA、gate 和 Gaussian guidance 的消融实验，以及 gate value distribution 可视化，证明模型确实学会了自适应模态选择，而不是简单依赖更多参数。

### 导师审核简版

下面是对上述三个挑战的更概括表述，可用于和导师讨论论文选题与创新点。

#### 挑战1：类别语义信息不足，难以支撑未见类识别

**原因：**  
音频-视觉广义零样本学习需要依靠类别文本信息把已见类知识迁移到未见类。但很多类别名称本身较短，例如“弹钢琴”“打篮球”“鸟叫”等，包含的语义信息有限，难以充分描述该类别对应的动作、声音、场景和上下文。因此，仅依赖类别名称生成文本嵌入，可能导致未见类语义表征不够丰富，影响模型对未见类的识别能力。

**方法：**  
我们计划构建更丰富的类别语义描述，并让类别语义更早参与音频和视觉特征学习。具体来说，不仅使用类别名称，还引入动作描述、声音特征、典型场景等文本信息，形成更完整的类别语义表示；同时，将这些语义信息提前注入音视频序列编码过程，使模型在提取视觉帧和音频片段特征时就能关注与目标类别相关的内容，而不是只在最后分类时才使用文本信息。

#### 挑战2：视频中关键音视频片段不明显，容易被冗余信息淹没

**原因：**  
一个视频中并不是所有帧和音频片段都与类别相关。关键动作可能只出现在少数帧中，关键声音也可能只在某些时间段出现。若直接使用均匀采样、平均池化或简单拼接，模型容易受到大量无关片段干扰。特别是在未见类识别中，模型没有该类别的训练样本，更难判断哪些时间片段真正重要。

**方法：**  
我们计划引入多高斯专家时间建模机制，让模型根据类别语义自动关注视频中可能相关的时间区域。相比只选择几个离散关键帧，高斯建模是一种连续的软选择方式，能够更自然地覆盖连续动作或持续声音。同时，多个高斯专家可以关注不同时间段，从而适应一个类别在视频中多次出现或音频、视觉线索分布不一致的情况。

#### 挑战3：音频和视觉可能不一致，简单融合容易产生模态干扰

**原因：**  
真实视频中的音频和视觉并不总是强相关。例如，画面中有人做动作，但背景音乐与动作无关；或者声音很明显，但画面中主体不清晰。简单地将音频和视觉特征拼接在一起，可能会把无关信息也融合进去，导致模型受到噪声模态干扰。此外，不同类别对音频和视觉的依赖程度不同，如果使用固定融合方式，容易造成模态偏置。

**方法：**  
我们计划将模态内信息和模态间信息分开建模，再通过动态门控进行融合。模态内建模用于保留视觉自身的动作线索和音频自身的声音线索，模态间建模用于捕捉音频与视觉之间真正有用的互补关系。最后，模型根据当前样本和类别语义自适应决定更依赖哪一部分信息，从而减少无关模态干扰，提高对未见类的泛化能力。

## 4. 可融入的 QA-TIGER 创新点

### 4.1 语义感知早期融合

QA-TIGER 指出，很多 AVQA 方法只在最终推理阶段使用问题信息，导致中间音视频特征没有被问题显式调制。迁移到 AVGZSL 后，对应的问题是：原 AVGZSL 虽然最终对齐类别文本嵌入，但音视频序列编码阶段并没有被类别语义显式引导。

因此可以引入 semantic-aware early fusion：

- 用类别语义原型作为 query/context。
- 在音视频序列建模早期就注入类别语义。
- 让视觉帧和音频片段更关注与当前候选类别相关的时间片段。

### 4.2 多高斯专家时间建模

多高斯专家时间建模可以理解为一种“语义引导的软时间定位机制”。它的目标不是简单平均所有帧，也不是粗暴地选出几个 Top-K 关键帧，而是让模型根据当前类别语义，在整段音视频序列中连续地分配注意力权重，从而找到最可能与该类别相关的时间区域。

具体来说，一个 Gaussian expert 可以看作时间轴上的一个“软窗口”。它由两个核心参数决定：

- **中心位置**：表示该专家主要关注视频中的哪个时间段。
- **宽度/方差**：表示该专家关注的是一个很窄的瞬间，还是一段较长的连续区域。

例如，对于一段 10 秒视频，如果某个高斯专家的中心落在第 4 秒附近，宽度较小，那么它会主要关注第 4 秒附近的视觉帧或音频片段；如果宽度较大，它会覆盖第 3 到第 6 秒之间的一段连续动作或声音。

之所以使用“多个”高斯专家，是因为一个类别相关证据不一定只出现在一个时间点。一个动作可能持续一段时间，也可能在视频中多次出现；音频和视觉线索也可能分布在不同时间段。因此，多个高斯专家可以分别关注不同时间区域，形成更灵活的时间建模能力。

在本文方案中，高斯专家不是固定的，而是由类别语义动态生成或动态调节。也就是说，对于不同候选类别，模型会产生不同的时间关注模式：

- 对于声音主导类别，如 `bird calling`，音频高斯专家可能更集中于鸟叫声出现的片段。
- 对于视觉主导类别，如 `basketball dunk`，视觉高斯专家可能更关注起跳、扣篮等关键动作帧。
- 对于音视频共同决定的类别，如 `playing violin`，音频专家可能关注弦乐声片段，视觉专家可能关注持琴和拉弓动作。

其基本流程可以概括为：

1. 输入视觉帧序列和音频片段序列。
2. 使用类别语义原型作为引导信号。
3. 根据类别语义分别生成视觉和音频的多个高斯时间窗口。
4. 每个高斯专家在时间轴上形成一组连续权重。
5. 用这些权重对视觉帧和音频片段进行加权聚合。
6. 通过专家路由权重决定不同高斯专家的重要性。
7. 得到类别相关的视觉时序表示和音频时序表示。

相比常见采样方式，该机制有以下优势：

- uniform sampling 可能漏掉类别相关关键帧。
- Top-K 离散选择会破坏时间连续性。
- Gaussian soft masks 是连续的软选择，可以保留动作和声音的时间结构。
- 多个 Gaussian experts 可以同时覆盖多个关键时间区域。
- audio 和 visual 可以分别建模，不要求二者在同一时间点出现最强证据。
- 高斯权重可以可视化，便于解释模型为什么关注某些帧或某些音频片段。

因此，多高斯专家时间建模的核心作用是：让类别语义主动告诉模型“应该在什么时间段寻找证据”，从而减少无关帧和无关声音对未见类识别的干扰。

### 4.3 模态独立的时间聚焦

QA-TIGER 分别为 audio 和 visual 生成高斯时间权重，而不是强制二者完全同步。迁移到 AVGZSL 后也很合理：

- 有些类别主要由声音决定，例如 bird calling、playing violin、engine running。
- 有些类别主要由视觉决定，例如 basketball dunk、climbing、diving。
- 有些类别需要音视频共同判断。

因此应设计 modality-specific Gaussian experts：

```text
visual Gaussian experts: G_v
audio Gaussian experts: G_a
```

再结合 Semi-IIN-like 的 intra/inter gate 进行最终融合。

## 5. 总体方案概览

新方案由四个核心模块组成：

1. **Sequence Feature Extraction**：使用 CLIP 提取视觉帧序列，使用 CLAP 提取音频片段序列。
2. **Semantic-Aware Early Fusion**：参考 QA-TIGER，将类别语义原型提前注入音视频序列。
3. **Semantic Gaussian Expert Temporal Grounding**：参考 QA-TIGER，用类别语义条件生成多高斯专家，进行连续时间聚焦。
4. **Intra-Inter Masked Attention with Dynamic Gate**：参考 Semi-IIN，分离模态内和模态间交互，再动态融合。

与已有 Semi-IIN-like Sequential AVGZSL 相比，本方案新增了两个更强创新点：

- 类别语义不仅用于最终对齐，也用于早期音视频编码。
- 模型不只是用 masked attention 处理序列，而是显式学习类别相关的连续时间定位。

## 6. 方法公式

### 5.1 GZSL 设置

类别集合被划分为 seen 类和 unseen 类：

$$
\mathcal{Y}=\mathcal{Y}^{s}\cup \mathcal{Y}^{u}, \quad
\mathcal{Y}^{s}\cap \mathcal{Y}^{u}=\emptyset .
\tag{1}
$$

训练集为：

$$
\mathcal{D}^{s}=\{(X_i^v,X_i^a,y_i)\}_{i=1}^{N}, \quad y_i\in \mathcal{Y}^{s}.
\tag{2}
$$

其中 $X_i^v$ 是视觉帧序列，$X_i^a$ 是音频片段序列。测试阶段需要在 $\mathcal{Y}^{s}\cup\mathcal{Y}^{u}$ 中分类。

### 5.2 音视频序列特征提取

对视频采样 $T_v$ 个视觉帧，并用 CLIP image encoder 提取帧级特征：

$$
v_i^t=E_{CLIP}^{img}(x_{i,t}^{v})\in \mathbb{R}^{d_v}, \quad t=1,\ldots,T_v .
\tag{3}
$$

得到视觉序列：

$$
V_i=[v_i^1,\ldots,v_i^{T_v}]\in \mathbb{R}^{T_v\times d_v}.
\tag{4}
$$

将音频切分为 $T_a$ 个片段，并用 CLAP audio encoder 提取片段级特征：

$$
a_i^t=E_{CLAP}^{aud}(x_{i,t}^{a})\in \mathbb{R}^{d_a}, \quad t=1,\ldots,T_a .
\tag{5}
$$

得到音频序列：

$$
A_i=[a_i^1,\ldots,a_i^{T_a}]\in \mathbb{R}^{T_a\times d_a}.
\tag{6}
$$

为了统一维度，将两种模态映射到共同维度 $d_h$：

$$
\hat{v}_i^t=f_v(v_i^t)\in \mathbb{R}^{d_h}, \quad
\hat{a}_i^t=f_a(a_i^t)\in \mathbb{R}^{d_h}.
\tag{7}
$$

加入模态类型嵌入和位置编码：

$$
\bar{v}_i^t=\hat{v}_i^t+e_v+p_v^t,
\tag{8}
$$

$$
\bar{a}_i^t=\hat{a}_i^t+e_a+p_a^t.
\tag{9}
$$

### 5.3 类别语义原型构造

对于任意类别 $c$，使用 CLIP 和 CLAP 文本编码器提取类别文本嵌入：

$$
w_v^c=E_{CLIP}^{txt}(prompt(c))\in \mathbb{R}^{d_v},
\tag{10}
$$

$$
w_a^c=E_{CLAP}^{txt}(prompt(c))\in \mathbb{R}^{d_a}.
\tag{11}
$$

参考 AVGZSL，将两种文本嵌入融合为统一语义原型：

$$
s^c=W_{enc}([w_v^c;w_a^c])\in \mathbb{R}^{d_h}.
\tag{12}
$$

再投影到最终类别语义空间：

$$
\theta_w^c=W_{proj}(s^c)\in \mathbb{R}^{d_{out}}.
\tag{13}
$$

这里 $s^c$ 既用于语义感知音视频编码，也用于最终 zero-shot 对齐。因为 unseen 类同样可以通过类别名称生成 $s^c$，所以该设计不会破坏 GZSL 设定。

### 5.4 Semantic-Aware Early Fusion

QA-TIGER 使用 question-aware fusion 将问题信息提前注入视觉和音频特征。本方案将 question feature 替换为 class semantic prototype $s^c$。

给定候选类别 $c$，首先对视觉和音频序列做模态内 self-attention：

$$
V_i^{sa}=SA(\bar{V}_i,\bar{V}_i,\bar{V}_i),
\tag{14}
$$

$$
A_i^{sa}=SA(\bar{A}_i,\bar{A}_i,\bar{A}_i).
\tag{15}
$$

然后进行跨模态交互与类别语义注入：

$$
V_{i,c}^{q}
=
\bar{V}_i
SA(\bar{V}_i,\bar{V}_i,\bar{V}_i)
CA(\bar{V}_i,\bar{A}_i,\bar{A}_i)
CA(\bar{V}_i,S^c,S^c),
\tag{16}
$$

$$
A_{i,c}^{q}
=
\bar{A}_i
SA(\bar{A}_i,\bar{A}_i,\bar{A}_i)
CA(\bar{A}_i,\bar{V}_i,\bar{V}_i)
CA(\bar{A}_i,S^c,S^c).
\tag{17}
$$

其中：

- $\bar{V}_i=[\bar{v}_i^1,\ldots,\bar{v}_i^{T_v}]$。
- $\bar{A}_i=[\bar{a}_i^1,\ldots,\bar{a}_i^{T_a}]$。
- $S^c$ 可以是单个类别语义 token $s^c$，也可以是由 prompt tokens 得到的类别语义 token 序列。
- $CA(Q,K,V)$ 表示 cross-attention。

式 (16)(17) 对应 QA-TIGER 中的 question-aware fusion，但将 question-aware 改造为 semantic-aware。它使每个类别语义都能提前调制音视频序列，而不是只在最后一步做距离匹配。

### 5.5 Semantic Gaussian Expert Temporal Grounding

QA-TIGER 的核心创新之一是用多个 Gaussian experts 对时间轴进行连续建模。本方案将其改造成类别语义条件的时间定位模块。

首先用类别语义原型 $s^c$ 聚合当前类别相关的视觉和音频上下文：

$$
u_{v}^{c}=CA(s^c,V_{i,c}^{q},V_{i,c}^{q})\in \mathbb{R}^{d_h},
\tag{18}
$$

$$
u_{a}^{c}=CA(s^c,A_{i,c}^{q},A_{i,c}^{q})\in \mathbb{R}^{d_h}.
\tag{19}
$$

然后分别为视觉和音频生成 $E$ 个 Gaussian experts。第 $e$ 个视觉专家的中心和方差为：

$$
\mu_{v,e}^{c},\sigma_{v,e}^{c}
=
\phi_v^{e}(u_v^c),
\tag{20}
$$

音频专家为：

$$
\mu_{a,e}^{c},\sigma_{a,e}^{c}
=
\phi_a^{e}(u_a^c).
\tag{21}
$$

为了减少专家冗余，可参考 QA-TIGER 的中心分散思想，将中心写为初始均匀中心加预测偏移：

$$
\mu_{m,e}^{c}
=
\frac{e-0.5}{E}+\Delta\mu_{m,e}^{c},
\quad m\in\{v,a\}.
\tag{22}
$$

其中 $\Delta\mu_{m,e}^{c}$ 由线性层预测，并可通过 sigmoid 或 clipping 限制在合法时间范围内。

对于归一化时间位置 $\tau_t\in[0,1]$，第 $e$ 个专家的高斯权重为：

$$
g_{m,e}^{c}(t)
=
\exp
\left(
-\frac{(\tau_t-\mu_{m,e}^{c})^2}{2(\sigma_{m,e}^{c})^2}
\right),
\quad m\in\{v,a\}.
\tag{23}
$$

归一化后得到 soft temporal mask：

$$
\alpha_{m,e}^{c}(t)
=
\frac{g_{m,e}^{c}(t)}
{\sum_{t'}g_{m,e}^{c}(t')}.
\tag{24}
$$

同时，用 router 预测每个专家的重要性：

$$
r_v^c=Softmax(u_v^c W_v^r)\in \mathbb{R}^{E},
\tag{25}
$$

$$
r_a^c=Softmax(u_a^c W_a^r)\in \mathbb{R}^{E}.
\tag{26}
$$

每个专家对时间序列进行加权池化：

$$
z_{v,e}^{c}
=
\sum_{t=1}^{T_v}\alpha_{v,e}^{c}(t) V_{i,c}^{q,t},
\tag{27}
$$

$$
z_{a,e}^{c}
=
\sum_{t=1}^{T_a}\alpha_{a,e}^{c}(t) A_{i,c}^{q,t}.
\tag{28}
$$

最后用 router 权重融合专家输出：

$$
z_{v}^{c}
=
\sum_{e=1}^{E}r_{v,e}^{c} z_{v,e}^{c},
\tag{29}
$$

$$
z_{a}^{c}
=
\sum_{e=1}^{E}r_{a,e}^{c} z_{a,e}^{c}.
\tag{30}
$$

这一模块的作用是：对于每一个候选类别，模型可以软选择与该类别最相关的视觉帧和音频片段。例如对于 `playing violin`，音频 Gaussian 可能聚焦在明显弦乐声片段，视觉 Gaussian 可能聚焦在乐器或演奏动作出现的帧。

### 5.6 Intra-Inter Masked Attention

经过语义感知高斯专家后，得到类别条件下的音频表示 $z_a^c$ 和视觉表示 $z_v^c$。为了保留 Semi-IIN-like 序列方案的 intra/inter 分离思想，可以在高斯聚焦前或聚焦后使用 masked attention。

更推荐的实现是：先在完整序列上做 IntraMA/InterMA，再用 Gaussian experts 聚合。这能保留时间结构。

构造序列：

$$
Z_{i,c}^{0}=[z_{cls}; A_{i,c}^{q}; V_{i,c}^{q}]\in \mathbb{R}^{T\times d_h},
\tag{31}
$$

其中 $T=1+T_a+T_v$。

定义模态索引 $m(r)$：

$$
m(r)=
\begin{cases}
cls, & r=0,\\
a, & 1\le r\le T_a,\\
v, & T_a<r<T.
\end{cases}
\tag{32}
$$

IntraMASK 为：

$$
M_{intra}(r,s)=
\begin{cases}
0, & r=0 \text{ or } s=0,\\
0, & m(r)=m(s),\\
-\infty, & m(r)\ne m(s),\ r\ne0,\ s\ne0.
\end{cases}
\tag{33}
$$

InterMASK 为：

$$
M_{inter}(r,s)=
\begin{cases}
0, & r=0 \text{ or } s=0,\\
0, & m(r)\ne m(s),\ r\ne0,\ s\ne0,\\
-\infty, & m(r)=m(s),\ r\ne0,\ s\ne0.
\end{cases}
\tag{34}
$$

Masked attention 统一写为：

$$
MA(X,M)=Softmax\left(\frac{QK^T}{\sqrt{d_k}}+M\right)V,
\tag{35}
$$

其中：

$$
Q=XW_Q,\quad K=XW_K,\quad V=XW_V.
\tag{36}
$$

第 $l$ 层 IntraMAU：

$$
\tilde{Z}_{intra}^{l}
=MA(LN(Z_{intra}^{l-1}),M_{intra})+LN(Z_{intra}^{l-1}),
\tag{37}
$$

$$
Z_{intra}^{l}
=FFN(LN(\tilde{Z}_{intra}^{l}))+LN(\tilde{Z}_{intra}^{l}).
\tag{38}
$$

第 $l$ 层 InterMAU：

$$
\tilde{Z}_{inter}^{l}
=MA(LN(Z_{inter}^{l-1}),M_{inter})+LN(Z_{inter}^{l-1}),
\tag{39}
$$

$$
Z_{inter}^{l}
=FFN(LN(\tilde{Z}_{inter}^{l}))+LN(\tilde{Z}_{inter}^{l}).
\tag{40}
$$

得到两个分支的类别条件序列表征：

$$
z_{intra}^{c}=Z_{intra}^{L}[0],
\tag{41}
$$

$$
z_{inter}^{c}=Z_{inter}^{L}[0].
\tag{42}
$$

### 5.7 Gaussian-Enhanced Intra-Inter Gate

现在有两类信息：

- $z_{intra}^{c}$：类别条件下的模态内时序线索。
- $z_{inter}^{c}$：类别条件下的跨模态互补线索。
- $z_v^c,z_a^c$：类别条件高斯专家得到的关键视觉/音频时间片段表征。

为了将 QA-TIGER 的时间聚焦与 Semi-IIN 的动态 gate 统一起来，先构造高斯增强特征：

$$
z_{g}^{c}=F_g([z_v^c;z_a^c;z_v^c\odot z_a^c;|z_v^c-z_a^c|]).
\tag{43}
$$

然后计算动态门控：

$$
g_i^c=\sigma(z_{intra}^{c}W_1+z_{inter}^{c}W_2+z_g^cW_3+b_g).
\tag{44}
$$

融合得到类别条件音视频表示：

$$
z_i^c
=
g_i^c\odot z_{inter}^{c}
+
(1-g_i^c)\odot z_{intra}^{c}
+
F_r(z_g^c).
\tag{45}
$$

最后投影到 AVGZSL 输出空间：

$$
\theta_{o_i}^{c}=O_{proj}(z_i^c)\in \mathbb{R}^{d_{out}}.
\tag{46}
$$

注意这里 $\theta_{o_i}^{c}$ 是 class-conditioned audio-visual representation，即同一个视频在不同候选类别语义引导下会产生不同的音视频表征。这是本方案区别于原 AVGZSL 的关键创新。

如果担心计算量过大，可以使用轻量版本：训练时只对 ground-truth 类和若干 hard negative 类计算 $\theta_{o_i}^{c}$；推理时先用 AVGZSL baseline 选出 Top-M 候选类别，再对 Top-M 进行 semantic-aware Gaussian reranking。

## 7. 分类与训练目标

### 6.1 类别匹配分数

对于样本 $i$ 和候选类别 $c$，定义匹配分数：

$$
s(i,c)=
\frac{
(\theta_{o_i}^{c})^T\theta_w^c
}{
\|\theta_{o_i}^{c}\|_2\|\theta_w^c\|_2
}.
\tag{47}
$$

训练时只在 seen 类上计算 softmax：

$$
p(y=c|X_i^v,X_i^a)
=
\frac{\exp(s(i,c)/\tau)}
{\sum_{j\in\mathcal{Y}^{s}}\exp(s(i,j)/\tau)}.
\tag{48}
$$

分类损失：

$$
L_{ce}
=
-\frac{1}{N}\sum_{i=1}^{N}
\log p(y=y_i|X_i^v,X_i^a).
\tag{49}
$$

### 6.2 语义回归损失

继承 AVGZSL 的语义对齐思想，对 ground-truth 类别进行回归约束：

$$
L_{reg}
=
\frac{1}{N}\sum_{i=1}^{N}
\left\|\theta_{o_i}^{y_i}-\theta_w^{y_i}\right\|_2^2.
\tag{50}
$$

### 6.3 语义重构损失

令 $D_o$ 和 $D_w$ 为解码器：

$$
\rho_{o_i}=D_o(\theta_{o_i}^{y_i}), \quad
\rho_{w_i}=D_w(\theta_w^{y_i}).
\tag{51}
$$

重构损失：

$$
L_{rec}
=
\frac{1}{N}\sum_{i=1}^{N}
\left\|\rho_{o_i}-s^{y_i}\right\|_2^2
+
\frac{1}{N}\sum_{i=1}^{N}
\left\|\rho_{w_i}-s^{y_i}\right\|_2^2.
\tag{52}
$$

### 6.4 高斯专家多样性正则

为了避免多个 Gaussian experts 学到同一时间区域，可加入中心分散正则：

$$
L_{div}
=
\sum_{m\in\{v,a\}}
\sum_{e\ne e'}
\exp
\left(
-\frac{|\mu_{m,e}-\mu_{m,e'}|}{\eta}
\right).
\tag{53}
$$

该项鼓励不同专家关注不同时间片段。第一版实验中可以先不加入，或只作为 ablation。

### 6.5 总损失

最终损失为：

$$
L
=
L_{ce}
\lambda_{reg}L_{reg}
\lambda_{rec}L_{rec}
\lambda_{div}L_{div}.
\tag{54}
$$

为了与 AVGZSL 公平比较，初始设置建议：

$$
\lambda_{reg}=1,\quad \lambda_{rec}=1,\quad \lambda_{div}=0.01.
\tag{55}
$$

如果不使用 $L_{div}$，则退化为 AVGZSL 原始复合损失加新的结构模块。

## 8. 推理策略

### 7.1 全类别推理

对所有 seen 和 unseen 类计算分数：

$$
\hat{y}_i
=
\arg\max_{c\in\mathcal{Y}^{s}\cup\mathcal{Y}^{u}}s(i,c).
\tag{56}
$$

如果存在 seen 类偏置，沿用 AVGZSL calibrated stacking：

$$
s'(i,c)=
\begin{cases}
s(i,c)-\gamma, & c\in\mathcal{Y}^{s},\\
s(i,c), & c\in\mathcal{Y}^{u}.
\end{cases}
\tag{57}
$$

最终预测：

$$
\hat{y}_i
=
\arg\max_{c\in\mathcal{Y}^{s}\cup\mathcal{Y}^{u}}s'(i,c).
\tag{58}
$$

### 7.2 Top-M Reranking 推理

由于 class-conditioned encoding 对每个类别都要计算语义感知特征，复杂度可能较高。可采用两阶段推理：

1. 使用原 AVGZSL 或不带 semantic-aware Gaussian 的轻量模型计算初始分数。
2. 选出 Top-M 候选类别。
3. 只对 Top-M 类别运行 SAGE-IIG 模块。
4. 用式 (56) 或 (58) 得到最终类别。

该策略可以显著降低推理成本，也更符合实际实现。

## 9. 与三篇论文的对应关系

### 8.1 继承 AVGZSL 的部分

- 使用 CLIP 提取视觉特征。
- 使用 CLAP 提取音频特征。
- 使用 CLIP/CLAP 文本编码器得到类别语义嵌入。
- 使用音视频表示与类别文本表示的共享空间对齐。
- 保留 `L_ce + L_reg + L_rec` 的训练目标。
- 保留 calibrated stacking 处理 seen 类偏置。

### 8.2 继承 Semi-IIN 的部分

- 将 intra-modal 和 inter-modal 交互分离。
- 使用 IntraMASK 只建模同模态时序关系。
- 使用 InterMASK 建模跨模态关系。
- 使用 dynamic gate 在样本级选择 intra/inter 信息比例。
- 通过 case-wise gate 提升对模态噪声和跨模态互补的适应性。

### 8.3 引入 QA-TIGER 的部分

- 将 question-aware fusion 改造成 semantic-aware early fusion。
- 将 question feature 替换为 class semantic prototype。
- 使用多个 Gaussian experts 对时间轴进行连续软选择。
- 为 audio 和 visual 分别生成 Gaussian experts。
- 使用 router 动态决定不同专家的重要性。
- 用高斯中心分散思想降低专家冗余。

## 10. 为什么这是合理的新创新

### 9.1 原 Semi-IIN-like 方案的不足

Semi-IIN-like Sequential AVGZSL 已经能建模帧序列，并区分 intra/inter 交互。但它仍然存在一个不足：

```text
序列交互是 class-agnostic 的。
```

也就是说，模型先把视频编码成一个通用音视频表示，再与类别文本嵌入对齐。不同类别的语义并没有直接参与时间片段选择。

### 9.2 QA-TIGER 带来的增强

QA-TIGER 的思想可以补足这一点：

```text
不同语义查询应关注不同时间片段。
```

在 AVGZSL 中，不同类别就是不同语义查询。例如同一个视频中可能既有 `playing guitar` 的视觉线索，也有 `singing` 的音频线索。类别语义引导的 Gaussian experts 可以让模型对不同候选类别关注不同片段，从而更适合 generalized zero-shot 分类。

### 9.3 与 GZSL 的兼容性

该方案没有引入 unseen 类训练样本，只使用 unseen 类名称生成语义原型。因此仍符合 inductive GZSL 的基本设定。

需要注意的是：如果进一步使用无标签 unseen 测试视频参与 self-training，则应明确标注为 transductive GZSL。

## 11. 建议实验设计

### 10.1 主实验

在 VGGSound-GZSLcls、UCF-GZSLcls、ActivityNet-GZSLcls 上比较：

```text
AVGZSL baseline
Seq-IIG-AVGZSL
Seq-IIG-AVGZSL + Semantic-aware early fusion
Seq-IIG-AVGZSL + Gaussian experts
SAGE-IIG-AVGZSL full model
```

指标沿用 AVGZSL：

```text
acc_S
acc_U
HM
acc_ZSL
```

### 10.2 消融实验

建议做以下消融：

1. 去掉 semantic-aware early fusion。
2. 去掉 Gaussian experts，改为 average pooling。
3. Gaussian experts vs Top-K frame selection。
4. 单 Gaussian vs 多 Gaussian experts。
5. 共享 audio/visual Gaussian vs 模态独立 Gaussian。
6. 去掉 IntraMA，仅保留 InterMA。
7. 去掉 InterMA，仅保留 IntraMA。
8. 去掉 dynamic gate，改为 concat。
9. 不同专家数 $E=1,3,5,7$。
10. full inference vs Top-M reranking inference。

### 10.3 可视化分析

可以提供三类可视化：

1. **Gaussian temporal masks**：展示不同类别语义下模型关注的视觉帧和音频片段。
2. **Gate value distribution**：展示不同数据集或类别中 intra/inter gate 的分布。
3. **Seen vs unseen t-SNE**：沿用 AVGZSL 的可视化，展示新模型是否让 unseen 类聚类更清晰。

尤其建议展示同一个视频对不同候选类别的 Gaussian 权重差异。这能直接证明本方案的 class-conditioned temporal grounding 创新。

## 12. 预期贡献写法

英文贡献可写为：

1. We propose a semantic-aware sequential audio-visual GZSL framework that injects class semantic prototypes into audio-visual temporal encoding, enabling class-conditioned feature refinement for both seen and unseen categories.
2. We introduce semantic Gaussian experts to softly localize class-relevant audio and visual temporal segments, extending question-aware temporal grounding to generalized zero-shot recognition.
3. We combine semantic Gaussian temporal grounding with intra-inter modal masked attention and dynamic gating, allowing the model to adaptively balance modality-specific temporal cues and cross-modal complementary information.

中文贡献可写为：

1. 提出一种语义感知序列式音视频广义零样本学习框架，将类别语义原型提前注入音视频时序编码过程，使 seen/unseen 类均可进行类别条件特征调制。
2. 设计语义条件高斯专家模块，对音频片段和视觉帧进行连续软时间定位，从而捕获与候选类别相关的关键时间区域。
3. 将语义高斯时间定位与 intra/inter masked attention 及动态门控结合，使模型能够自适应平衡模态内时序线索和跨模态互补信息。

## 13. 风险与实现建议

### 12.1 主要风险

1. **计算复杂度高**：对每个类别都做 semantic-aware encoding 成本较大。
2. **类别语义过强可能导致过拟合 seen 类**：训练时只见 seen 类，模型可能学会 seen 类特定语义调制。
3. **Gaussian experts 需要序列特征质量支撑**：如果帧采样过少或 CLAP 片段过粗，高斯定位收益有限。
4. **模块较多，必须做充分消融**：否则难以证明每个创新点有效。

### 12.2 推荐实现顺序

建议按以下顺序实现：

```text
Step 1: Seq-IIG-AVGZSL
Step 2: 加入 semantic-aware early fusion，仅训练 ground-truth class conditioning
Step 3: 加入 Gaussian experts，先只做 visual/audio average 后替换为 Gaussian pooling
Step 4: 加入 router 和多专家
Step 5: 加入 Top-M reranking 推理
Step 6: 做完整消融和可视化
```

### 12.3 最小可行版本

如果希望先做一个低成本版本，可以使用：

```text
Seq-IIG-AVGZSL + Semantic Gaussian Pooling
```

最小版本只需：

- 类别语义 $s^c$ 生成 audio/visual Gaussian masks。
- 用 Gaussian masks 对音频/视觉序列加权池化。
- 将池化结果送入已有 Intra/Inter gate。

暂时不做完整 class-conditioned Transformer。这样计算量低，仍然保留 QA-TIGER 的核心思想。

## 14. 最终结论

在 `Semi-IIN-like 序列版方案` 的基础上，最合理的 QA-TIGER 融合方式是：

```text
把 question-aware temporal grounding 改造成 class-semantic-aware temporal grounding。
```

具体来说，就是用 AVGZSL 中已有的 CLIP/CLAP 类别文本嵌入作为语义查询，提前调制音视频序列，并通过多高斯专家对类别相关帧和音频片段进行连续软选择。随后再结合 Semi-IIN 的 IntraMA、InterMA 和 dynamic gate，形成一个同时具备：

- zero-shot semantic alignment；
- sequence-level intra/inter interaction；
- class-conditioned temporal grounding；
- modality-specific Gaussian expert selection；
- sample-adaptive gate fusion；

的新方案。

该方案比原 Semi-IIN-like Sequential AVGZSL 更充实，创新点也更明确：它不仅建模音视频序列交互，还让每个候选类别主动指导模型寻找自己的关键时间证据。
