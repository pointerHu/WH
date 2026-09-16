# 将 Semi-IIN 创新点迁移到 Audio-Visual GZSL 的可行方案

## 1. 任务上下文

本文件基于工作区中的两篇论文材料整理：

- `Audio-Visual_Generalized_Zero-Shot_Learning.md`
- `Semi-IIN论文完整.md`

目标是：以第一篇 Audio-Visual Generalized Zero-Shot Learning using Pre-Trained Large Multi-Modal Models 作为 audio-visual generalized zero-shot learning baseline，选择性引入第二篇 Semi-IIN 的创新点，设计合理、可实验验证的改进方案，并给出证据。

核心判断是：不能把 Semi-IIN 整个模型机械搬到 AVGZSL 中，而应迁移其适配音视频 GZSL 的思想，尤其是：

1. intra-modal 与 inter-modal 信息分离建模。
2. 动态 gate 选择 intra/inter 信息比例。
3. top-k 高置信伪标签自训练。

其中，前两点最适合作为主创新；第三点适合作为半监督增强模块或附加实验。

## 2. AVGZSL Baseline 的关键机制

第一篇论文的核心方法可以概括为：

1. 使用 CLIP 提取视觉特征和 CLIP 文本类别嵌入。
2. 使用 CLAP 提取音频特征和 CLAP 文本类别嵌入。
3. 冻结 CLIP/CLAP，仅训练轻量前馈网络。
4. 将音频和视觉特征直接拼接后输入音视频分支：

```text
o = O_enc(concat(v, a))
theta_o = O_proj(o)
```

5. 将 CLIP 文本嵌入和 CLAP 文本嵌入拼接后输入文本分支：

```text
w = W_enc(concat(w_v, w_a))
theta_w = W_proj(w)
```

6. 训练目标包括：

```text
L = L_ce + L_rec + L_reg
```

7. 测试时计算音视频输出嵌入 `theta_o` 与所有类别文本嵌入 `theta_w` 的距离，选择最近类别。

## 3. AVGZSL 的可改进点

AVGZSL 的优势是简单、参数少、依赖强预训练特征；但它也有一个明显可改进位置：

原模型对音频和视觉采用固定拼接融合：

```text
concat(v, a)
```

这种融合默认所有样本都需要相同的音视频融合方式。但论文自己的消融显示，不同数据集、不同场景下音频和视觉贡献不同：

- VGGSound-GZSLcls 中，音频单模态比视觉单模态更强，因为数据集本身强调声音信息。
- UCF-GZSLcls 和 ActivityNet-GZSLcls 中，视觉单模态通常比音频单模态更强。
- 使用双模态整体上最好，但不同模态的有效性并不恒定。

这说明 AVGZSL 具备引入“样本自适应模态交互选择”的合理动机。

## 4. Semi-IIN 的可迁移创新点

Semi-IIN 原任务是 multimodal sentiment analysis，不是 zero-shot learning。但它的以下思想具有跨任务迁移价值。

### 4.1 Intra-modal 与 Inter-modal 分离建模

Semi-IIN 设计了两个分支：

- IntraMA：关注同一模态内部的信息交互。
- InterMA：关注不同模态之间的信息交互。

其动机是：有些样本中跨模态交互会引入噪声，有些样本又必须依赖跨模态互补信息。

迁移到 AVGZSL 时，可以将这一思想改写为：

- intra branch：分别保留音频自身判别信息和视觉自身判别信息。
- inter branch：建模音频与视觉之间的互补或冲突关系。

### 4.2 Gate 动态选择

Semi-IIN 不直接拼接 intra/inter 分支，而是使用 gate 动态融合：

```text
G = sigmoid(Z_intra W_1 + Z_inter W_2 + b)
Z = G * Z_inter + (1 - G) * Z_intra
```

迁移到 AVGZSL 时，gate 可以用于控制当前样本更依赖：

- 音频/视觉自身信息；
- 还是音视频跨模态交互信息。

这比 AVGZSL 的固定 concat 更灵活。

### 4.3 Self-training 伪标签

Semi-IIN 使用 self-training：

1. 先用有标签数据训练模型。
2. 对无标签数据生成预测。
3. 选择每类 top-k 高置信样本。
4. 将伪标签样本加入训练。

迁移到 AVGZSL 时可作为半监督增强，但必须注意 zero-shot learning 的设定边界。若无标签数据包含 unseen 类测试样本，则应明确称为 transductive GZSL；若保持 inductive GZSL，则伪标签只能来自 seen 类无标签样本或严格不泄漏测试标签的外部数据。

## 5. 推荐主方案：Intra-Inter Gated AVGZSL

建议将方法命名为：

```text
Intra-Inter Gated Audio-Visual GZSL
```

或：

```text
IIG-AVGZSL
```

### 5.1 总体结构

保留 AVGZSL 的 CLIP/CLAP 特征提取、文本语义分支和原始损失函数，只替换音视频融合部分。

原 AVGZSL：

```text
o = O_enc(concat(v, a))
theta_o = O_proj(o)
```

改为：

```text
z_intra = F_intra(v, a)
z_inter = F_inter(v, a)
g = sigmoid(W_g [z_intra, z_inter] + b_g)
z = g * z_inter + (1 - g) * z_intra
theta_o = O_proj(z)
```

文本分支保持：

```text
w = W_enc(concat(w_v, w_a))
theta_w = W_proj(w)
```

最终仍然对齐：

```text
theta_o <-> theta_w
```

### 5.2 Intra Branch 设计

输入：

```text
v: CLIP visual feature, 512 dim
a: CLAP audio feature, 1024 dim
```

先映射到同一维度：

```text
h_v = MLP_v(v)
h_a = MLP_a(a)
```

然后得到 intra 表示：

```text
z_intra = MLP_intra(concat(h_v, h_a))
```

含义：

- `h_v` 保留视觉自身类别判别信息。
- `h_a` 保留音频自身类别判别信息。
- `z_intra` 表示“不强制跨模态交互”的模态内信息整合。

### 5.3 Inter Branch 设计

建议从轻量实现开始，不直接上复杂 token-level attention。

可选实现：

```text
z_inter = MLP_inter(concat(h_v, h_a, h_v * h_a, |h_v - h_a|))
```

其中：

- `h_v * h_a` 表示音视频一致性或共现关系。
- `|h_v - h_a|` 表示音视频差异或冲突。

这种设计比直接 concat 多了显式交互项，但仍然保持轻量，符合 AVGZSL 原论文“简单模型 + 强预训练特征”的风格。

### 5.4 Gate 融合

```text
g = sigmoid(W_g concat(z_intra, z_inter) + b_g)
z = g * z_inter + (1 - g) * z_intra
```

其中 `g` 可以是：

- 标量 gate：每个样本一个融合权重，最简单、最稳。
- 向量 gate：每个特征维度一个融合权重，表达能力更强。

建议第一版使用向量 gate，但同时做标量 gate 消融。

### 5.5 损失函数

主方案中建议保留 AVGZSL 原始损失：

```text
L = L_ce + L_rec + L_reg
```

原因：

- AVGZSL 的消融显示 `L_ce + L_rec + L_reg` 整体效果最好。
- 引入 gate 后先不改损失，可以更清楚判断结构改动是否有效。

可选增加 gate 正则：

```text
L_gate = mean(g * log(g) + (1 - g) * log(1 - g))
```

但不建议第一版加入。因为 AVGZSL 数据量有限，额外正则可能引入新的超参数不稳定性。

## 6. 增强方案：Semi-supervised AVGZSL

在主方案稳定后，可以加入 Semi-IIN 的 self-training 思想。

### 6.1 训练流程

第一阶段：

```text
用 seen 类有标签训练集训练 IIG-AVGZSL
```

第二阶段：

```text
用训练好的模型预测无标签视频
```

第三阶段：

```text
按类别选择 top-k 高置信样本，或设置置信度阈值 tau
```

第四阶段：

```text
用有标签样本 + 伪标签样本继续训练
```

### 6.2 伪标签置信度

AVGZSL 的分类基于 `theta_o` 与 `theta_w` 的距离或相似度，因此置信度可定义为：

```text
p(y | x) = softmax(sim(theta_o, theta_w^j) / tau)
```

选择：

```text
max_j p(y=j | x)
```

最高的样本作为伪标签候选。

### 6.3 伪标签损失

建议只对伪标签样本使用分类损失，不使用 reconstruction/regression：

```text
L = L_ce + L_rec + L_reg + lambda_u * L_ce_pseudo
```

原因是 Semi-IIN 中也只对伪标签样本回传分类任务损失，这样可以降低错误伪标签对连续空间回归目标的破坏。

## 7. 不建议直接照搬的部分

### 7.1 不建议直接使用完整 Semi-IIN Token-level MA

Semi-IIN 的 IntraMA/InterMA 是 token-level masked attention，输入包括文本 token、音频帧、视觉帧，并依赖序列结构。

AVGZSL 当前输入是：

- 一个 CLIP 中间帧视觉全局向量；
- 一个 CLAP 音频全局向量；
- 类别文本全局嵌入。

因此，若直接套用 Semi-IIN 的 token-level mask attention，会出现问题：

- 没有足够 token 序列支撑 mask attention。
- 参数量和复杂度增加，与 AVGZSL 的轻量设计冲突。
- 很难证明性能提升来自合理交互，而不是额外参数。

### 7.2 更强但代价更高的版本

如果希望更接近 Semi-IIN，可以改造特征提取：

- CLIP 提取多帧视觉序列，而不是单帧。
- CLAP 提取多个音频片段序列，而不是整段全局向量。
- 对音频 token 和视觉 token 使用 IntraMA/InterMA。

但这已经是较大改动，不适合作为第一版方案。

### 7.3 如果输入是帧序列：Semi-IIN-like 序列版方案

如果 AVGZSL 的输入不再是单个全局视觉向量和单个全局音频向量，而是帧序列或片段序列，那么可以设计一个更接近 Semi-IIN 的版本。此时 Semi-IIN 的 token-level IntraMA/InterMA 就有了合理使用条件。

建议命名为：

```text
Seq-IIG-AVGZSL
```

或：

```text
Semi-IIN-inspired Sequential AVGZSL
```

#### 7.3.1 输入形式

视觉输入由单帧改为多帧：

```text
V = [v_1, v_2, ..., v_Tv], v_t in R^512
```

其中每个 `v_t` 可以由 CLIP image encoder 提取。

音频输入由整段全局向量改为多个音频片段：

```text
A = [a_1, a_2, ..., a_Ta], a_t in R^1024
```

其中每个 `a_t` 可以由 CLAP audio encoder 对滑动窗口音频片段提取，例如每 1-2 秒一个片段。

类别文本仍然使用 CLIP/CLAP 文本编码器生成类别语义嵌入：

```text
w_v = CLIP_text(class prompt)
w_a = CLAP_text(class prompt)
```

注意：GZSL 的文本输入是类别原型，不是每个视频样本的自然语言 token 序列。因此，文本分支不需要完全照搬 Semi-IIN 的 text-token 处理方式，而应继续承担类别语义锚点的作用。

#### 7.3.2 序列编码

先将不同维度的音频、视觉 token 映射到统一 hidden dimension：

```text
h_v^t = Linear_v(v_t), h_v^t in R^d
h_a^t = Linear_a(a_t), h_a^t in R^d
```

加入模态类型 embedding 和位置 embedding：

```text
H_v = [h_v^1, ..., h_v^Tv] + type_v + pos_v
H_a = [h_a^1, ..., h_a^Ta] + type_a + pos_a
```

拼接为音视频 token 序列：

```text
Z = [cls; H_a; H_v]
```

这里的 `cls` 用于聚合最终音视频表示，对应 Semi-IIN 中特殊 token 聚合信息的思想。

#### 7.3.3 IntraMA：模态内时序建模

IntraMA 只允许同一模态内部互相注意：

```text
audio token <-> audio token
visual token <-> visual token
cls token <-> all tokens
```

它的作用是：

- 在视觉帧内部寻找关键动作帧、物体帧或场景帧。
- 在音频片段内部寻找关键声音片段。
- 避免一开始就让噪声模态干扰另一模态。

可写为：

```text
Z_intra = TransformerBlock(Z, mask = IntraMASK)
```

其中 `IntraMASK` 屏蔽音频 token 到视觉 token 的直接注意力，以及视觉 token 到音频 token 的直接注意力。

#### 7.3.4 InterMA：跨模态交互建模

InterMA 主要允许音频和视觉之间互相注意：

```text
audio token <-> visual token
cls token <-> all tokens
```

它的作用是：

- 建模某个声音片段和某些视觉帧之间的对应关系。
- 捕获音视频互补信息，例如画面中出现动作但声音提供类别线索。
- 识别音视频冲突，例如视觉不明显但音频强相关，或音频背景噪声干扰视觉判断。

可写为：

```text
Z_inter = TransformerBlock(Z, mask = InterMASK)
```

#### 7.3.5 Gate 融合

取两个分支的 `cls` token 作为最终候选表示：

```text
z_intra = Z_intra[cls]
z_inter = Z_inter[cls]
```

然后沿用 Semi-IIN 的动态门控思想：

```text
g = sigmoid(W_g concat(z_intra, z_inter) + b_g)
z = g * z_inter + (1 - g) * z_intra
theta_o = O_proj(z)
```

这里 `g` 的解释更清楚：

- `g` 高：当前样本更依赖跨模态交互。
- `g` 低：当前样本更依赖模态内时序线索。

#### 7.3.6 文本语义分支保持 AVGZSL 风格

类别文本嵌入仍然按 AVGZSL 的方式处理：

```text
w = W_enc(concat(w_v, w_a))
theta_w = W_proj(w)
```

不建议把类别文本原型和音视频 token 混在同一个 Transformer 中做强交互，原因是：

- GZSL 需要所有类别的稳定语义原型。
- 如果每个视频样本都动态改变类别文本表示，可能破坏 seen/unseen 类共享语义空间。
- AVGZSL 的优势正是 CLIP/CLAP 已经提供对齐良好的类别语义嵌入。

更稳妥的做法是：音视频分支用 Semi-IIN-like 序列交互，文本分支继续作为固定语义锚点，最后在共同 embedding space 中对齐。

#### 7.3.7 损失函数

继续使用 AVGZSL 原始目标：

```text
L = L_ce + L_rec + L_reg
```

其中：

- `L_ce` 让音视频序列表示靠近正确类别。
- `L_reg` 对齐 `theta_o` 和 `theta_w`。
- `L_rec` 约束投影空间保留类别语义。

如果加入 self-training，则使用：

```text
L = L_ce + L_rec + L_reg + lambda_u * L_ce_pseudo
```

仍建议伪标签样本只参与分类损失。

#### 7.3.8 与轻量版方案的区别

轻量版 IIG-AVGZSL：

```text
输入：全局音频向量 + 全局视觉向量
交互：MLP 显式交互项 + gate
优点：改动小，计算量低，适合第一版实验
```

序列版 Seq-IIG-AVGZSL：

```text
输入：音频片段序列 + 视觉帧序列
交互：IntraMA/InterMA masked attention + gate
优点：更接近 Semi-IIN，能定位关键帧/关键声音片段，解释性更强
代价：特征提取、显存、训练时间、超参数复杂度显著增加
```

#### 7.3.9 何时值得使用序列版

以下情况建议使用序列版：

1. 数据集中视频较长，单帧 CLIP 表示容易漏掉关键动作或物体。
2. 类别依赖短时声音事件，例如敲击、鸣叫、爆炸、乐器声。
3. 音视频存在时间错位，简单全局平均会稀释关键线索。
4. 需要论文中提供 attention 可视化，展示模型关注了哪些帧和音频片段。

以下情况不建议优先使用序列版：

1. 数据量较小，Transformer 容易过拟合。
2. 只有预提取全局 CLIP/CLAP 特征，无法重新抽取序列特征。
3. 算力有限，无法承受多帧 CLIP 和多片段 CLAP 特征提取。
4. 目标只是提出一个稳健可复现的 baseline 改进。

#### 7.3.10 推荐实验路线

建议按复杂度逐步推进：

```text
Step 1: AVGZSL baseline
Step 2: 全局特征轻量版 IIG-AVGZSL
Step 3: 多帧/多片段平均池化版 AVGZSL
Step 4: 序列版 Seq-IIG-AVGZSL with IntraMA only
Step 5: 序列版 Seq-IIG-AVGZSL with InterMA only
Step 6: 序列版 Seq-IIG-AVGZSL with IntraMA + InterMA + gate
Step 7: 加入 self-training
```

这样可以证明性能提升不是简单来自“用了更多帧”，而是来自 intra/inter 分离交互和 gate 动态选择。

#### 7.3.11 论文方法表述版本：Semi-IIN-like Sequential AVGZSL

本节给出一个更接近论文方法部分的正式写法。该方案以 AVGZSL 的 CLIP/CLAP 语义对齐框架为基础，引入 Semi-IIN 的 intra-modal masked attention、inter-modal masked attention 和动态 gate 机制，用于处理音视频帧序列输入。

##### 7.3.11.1 问题定义

在 generalized zero-shot learning 设置中，类别集合被划分为 seen classes 和 unseen classes：

$$
\mathcal{Y}=\mathcal{Y}^{s}\cup \mathcal{Y}^{u}, \quad
\mathcal{Y}^{s}\cap \mathcal{Y}^{u}=\emptyset .
\tag{10}
$$

训练阶段只能使用 seen 类有标签样本：

$$
\mathcal{D}^{s}=\{(X_i^{v},X_i^{a},y_i)\}_{i=1}^{N}, \quad y_i\in \mathcal{Y}^{s},
\tag{11}
$$

其中 $X_i^{v}$ 表示第 $i$ 个视频样本的视觉帧序列，$X_i^{a}$ 表示对应音频序列。测试阶段需要在 seen 和 unseen 类共同组成的类别空间 $\mathcal{Y}^{s}\cup \mathcal{Y}^{u}$ 中完成分类。

与 AVGZSL 一致，模型目标是学习一个音视频映射函数：

$$
h:(X_i^{v},X_i^{a})\rightarrow \theta_{o_i},
\tag{12}
$$

使音视频表示 $\theta_{o_i}$ 在共享嵌入空间中接近其类别语义表示 $\theta_{w_i}$。测试时，对所有候选类别 $c\in \mathcal{Y}^{s}\cup \mathcal{Y}^{u}$ 计算距离，并选择最近类别：

$$
\hat{y}_i=\arg\min_{c\in \mathcal{Y}^{s}\cup \mathcal{Y}^{u}}
\left\|\theta_{o_i}-\theta_{w}^{c}\right\|_2 .
\tag{13}
$$

##### 7.3.11.2 序列特征提取

对于视觉模态，不再只取视频中间帧，而是从视频中采样 $T_v$ 帧，并使用 CLIP image encoder 提取帧级视觉特征：

$$
v_i^t=E_{CLIP}^{img}(x_{i,t}^{v})\in \mathbb{R}^{d_v}, \quad t=1,\ldots,T_v .
\tag{14}
$$

由此得到视觉序列：

$$
V_i=[v_i^1,v_i^2,\ldots,v_i^{T_v}]\in \mathbb{R}^{T_v\times d_v}.
\tag{15}
$$

对于音频模态，将原始音频划分为 $T_a$ 个片段，并使用 CLAP audio encoder 提取片段级音频特征：

$$
a_i^t=E_{CLAP}^{aud}(x_{i,t}^{a})\in \mathbb{R}^{d_a}, \quad t=1,\ldots,T_a .
\tag{16}
$$

得到音频序列：

$$
A_i=[a_i^1,a_i^2,\ldots,a_i^{T_a}]\in \mathbb{R}^{T_a\times d_a}.
\tag{17}
$$

其中 AVGZSL 原论文中通常有 $d_v=512$，$d_a=1024$。为了进行统一的序列交互，将两种模态映射到共同 hidden dimension $d_h$：

$$
\hat{v}_i^t=f_v(v_i^t)\in \mathbb{R}^{d_h}, \quad
\hat{a}_i^t=f_a(a_i^t)\in \mathbb{R}^{d_h}.
\tag{18}
$$

其中 $f_v$ 和 $f_a$ 可以由 Linear-BN-ReLU-Dropout 或轻量 MLP 实现。

参考 Semi-IIN 的 modal-type embedding 和 positional encoding，为不同模态加入模态类型嵌入和位置编码：

$$
\bar{v}_i^t=\hat{v}_i^t+e_v+p_v^t,
\tag{19}
$$

$$
\bar{a}_i^t=\hat{a}_i^t+e_a+p_a^t,
\tag{20}
$$

其中 $e_v,e_a\in \mathbb{R}^{d_h}$ 是可学习的模态类型嵌入，$p_v^t,p_a^t\in \mathbb{R}^{d_h}$ 是位置编码。

然后引入一个可学习的聚合 token $z_{cls}$，构造音视频序列输入：

$$
Z_i^0=[z_{cls};\bar{a}_i^1,\ldots,\bar{a}_i^{T_a};
\bar{v}_i^1,\ldots,\bar{v}_i^{T_v}]
\in \mathbb{R}^{T\times d_h},
\tag{21}
$$

其中 $T=1+T_a+T_v$。该设计对应 Semi-IIN 中使用特殊 token 聚合全局信息的思想，但这里不加入情感任务中的 `val` token，因为 AVGZSL 的目标是类别语义对齐而非情感强度回归。

##### 7.3.11.3 Intra-modal Masked Attention

Semi-IIN 的关键思想之一是将模态内交互和模态间交互分开学习。对于 audio-visual GZSL，模态内交互用于建模视觉帧内部的时序关系和音频片段内部的时序关系，避免跨模态噪声过早传播。

定义 token 的模态索引函数 $m(r)$：

$$
m(r)=
\begin{cases}
cls, & r=0,\\
a, & 1\le r\le T_a,\\
v, & T_a<r<T.
\end{cases}
\tag{22}
$$

IntraMASK 定义为：

$$
M_{intra}(r,s)=
\begin{cases}
0, & r=0 \text{ or } s=0,\\
0, & m(r)=m(s),\\
-\infty, & m(r)\ne m(s),\ r\ne0,\ s\ne0.
\end{cases}
\tag{23}
$$

也就是说，`cls` token 可以聚合所有 token，同一模态内部 token 可以互相注意，但音频 token 和视觉 token 之间的直接注意力被屏蔽。

对于第 $l$ 层 IntraMAU，参考 Transformer 和 Semi-IIN 的写法：

$$
\tilde{Z}_{intra}^{l}
=
\text{IntraMA}\left(\text{LN}(Z_{intra}^{l-1})\right)
+\text{LN}(Z_{intra}^{l-1}),
\tag{24}
$$

$$
Z_{intra}^{l}
=
\text{FFN}\left(\text{LN}(\tilde{Z}_{intra}^{l})\right)
+\text{LN}(\tilde{Z}_{intra}^{l}).
\tag{25}
$$

其中：

$$
\text{IntraMA}(X)
=
\text{softmax}
\left(
\frac{QK^{T}}{\sqrt{d_k}}+M_{intra}
\right)V,
\tag{26}
$$

$$
Q=XW_Q,\quad K=XW_K,\quad V=XW_V.
\tag{27}
$$

经过 $L$ 层后，取 `cls` token 作为模态内分支表示：

$$
z_{intra}=Z_{intra}^{L}[0]\in \mathbb{R}^{d_h}.
\tag{28}
$$

##### 7.3.11.4 Inter-modal Masked Attention

InterMA 用于显式建模音频片段和视觉帧之间的互补关系。与 IntraMA 相反，InterMA 主要允许跨模态 token 交互，并屏蔽同模态内部 token 的直接注意力。

InterMASK 定义为：

$$
M_{inter}(r,s)=
\begin{cases}
0, & r=0 \text{ or } s=0,\\
0, & m(r)\ne m(s),\ r\ne0,\ s\ne0,\\
-\infty, & m(r)=m(s),\ r\ne0,\ s\ne0.
\end{cases}
\tag{29}
$$

其中 `cls` token 仍然可以访问所有 token。音频 token 和视觉 token 之间允许互相注意，同一模态内部 token 的注意力被屏蔽，从而鼓励该分支专注于跨模态互补信息。

第 $l$ 层 InterMAU 写为：

$$
\tilde{Z}_{inter}^{l}
=
\text{InterMA}\left(\text{LN}(Z_{inter}^{l-1})\right)
+\text{LN}(Z_{inter}^{l-1}),
\tag{30}
$$

$$
Z_{inter}^{l}
=
\text{FFN}\left(\text{LN}(\tilde{Z}_{inter}^{l})\right)
+\text{LN}(\tilde{Z}_{inter}^{l}).
\tag{31}
$$

其中：

$$
\text{InterMA}(X)
=
\text{softmax}
\left(
\frac{QK^{T}}{\sqrt{d_k}}+M_{inter}
\right)V.
\tag{32}
$$

经过 $L$ 层后，取 `cls` token 得到跨模态分支表示：

$$
z_{inter}=Z_{inter}^{L}[0]\in \mathbb{R}^{d_h}.
\tag{33}
$$

##### 7.3.11.5 Intra-Inter Dynamic Gate

仅使用 IntraMA 可能忽略音视频互补线索；仅使用 InterMA 又可能在某些样本中引入跨模态噪声。参考 Semi-IIN 的动态 gate 机制，使用样本自适应门控融合两类信息：

$$
g_i=\sigma(z_{intra}W_1+z_{inter}W_2+b_g),
\tag{34}
$$

$$
z_i=g_i\odot z_{inter}+(1-g_i)\odot z_{intra},
\tag{35}
$$

其中 $W_1,W_2\in \mathbb{R}^{d_h\times d_h}$，$b_g\in \mathbb{R}^{d_h}$，$\odot$ 表示逐元素乘法。$g_i$ 可以理解为第 $i$ 个样本对跨模态交互信息的依赖程度：

- 当 $g_i$ 较大时，模型更依赖 InterMA 捕获的音视频互补关系。
- 当 $g_i$ 较小时，模型更依赖 IntraMA 捕获的模态内时序线索。

随后将融合表示投影到 AVGZSL 的输出嵌入空间：

$$
\theta_{o_i}=O_{proj}(z_i)\in \mathbb{R}^{d_{out}}.
\tag{36}
$$

##### 7.3.11.6 类别语义分支

为了保持 AVGZSL 的零样本语义迁移能力，类别文本分支仍然使用 CLIP 和 CLAP 的文本编码器生成类别原型。对于任意类别 $c$，分别得到：

$$
w_{v}^{c}=E_{CLIP}^{txt}(prompt(c))\in \mathbb{R}^{d_v},
\tag{37}
$$

$$
w_{a}^{c}=E_{CLAP}^{txt}(prompt(c))\in \mathbb{R}^{d_a}.
\tag{38}
$$

参考 AVGZSL，将两种文本类别嵌入融合为统一类别语义表示：

$$
w^{c}=W_{enc}([w_{v}^{c};w_{a}^{c}])\in \mathbb{R}^{d_h},
\tag{39}
$$

$$
\theta_{w}^{c}=W_{proj}(w^{c})\in \mathbb{R}^{d_{out}}.
\tag{40}
$$

这里不建议让类别文本 token 与音视频序列 token 直接共同进入同一个 InterMA Transformer。原因是 GZSL 需要对 seen/unseen 类共享稳定类别原型；如果类别原型随每个样本动态变化，可能削弱 AVGZSL 中 CLIP/CLAP 文本空间提供的零样本泛化能力。

##### 7.3.11.7 分类与训练目标

给定一个训练样本 $(X_i^{v},X_i^{a},y_i)$，首先计算音视频序列表示 $\theta_{o_i}$，再计算所有 seen 类的类别语义表示：

$$
\Theta_{w}^{s}=[\theta_{w}^{1},\theta_{w}^{2},\ldots,\theta_{w}^{K_s}]
\in \mathbb{R}^{K_s\times d_{out}}.
\tag{41}
$$

参考 AVGZSL 的 cross-entropy loss，定义 seen 类分类概率：

$$
p(y=k|X_i^{v},X_i^{a})
=
\frac{
\exp(\theta_{o_i}^{T}\theta_{w}^{k}/\tau)
}{
\sum_{j=1}^{K_s}\exp(\theta_{o_i}^{T}\theta_{w}^{j}/\tau)
},
\tag{42}
$$

其中 $\tau$ 是温度系数，若不额外调参可设为 $1$。分类损失为：

$$
L_{ce}
=
-\frac{1}{N}\sum_{i=1}^{N}
\log p(y=y_i|X_i^{v},X_i^{a}).
\tag{43}
$$

为了继承 AVGZSL 的语义对齐目标，保留 regression loss：

$$
L_{reg}
=
\frac{1}{N}\sum_{i=1}^{N}
\left\|\theta_{o_i}-\theta_{w}^{y_i}\right\|_2^2.
\tag{44}
$$

同时保留 reconstruction loss。令 $D_o$ 和 $D_w$ 分别为音视频嵌入解码器和文本嵌入解码器：

$$
\rho_{o_i}=D_o(\theta_{o_i}), \quad
\rho_{w_i}=D_w(\theta_{w}^{y_i}).
\tag{45}
$$

重构目标为：

$$
L_{rec}
=
\frac{1}{N}\sum_{i=1}^{N}
\left\|\rho_{o_i}-w^{y_i}\right\|_2^2
+
\frac{1}{N}\sum_{i=1}^{N}
\left\|\rho_{w_i}-w^{y_i}\right\|_2^2.
\tag{46}
$$

最终训练目标为：

$$
L
=
L_{ce}+\lambda_{reg}L_{reg}+\lambda_{rec}L_{rec}.
\tag{47}
$$

为了与 AVGZSL baseline 保持公平，第一版可以设置：

$$
\lambda_{reg}=1,\quad \lambda_{rec}=1.
\tag{48}
$$

##### 7.3.11.8 推理阶段

推理时，模型需要在 seen 和 unseen 类的联合类别空间中预测：

$$
\Theta_w=[\theta_w^1,\theta_w^2,\ldots,\theta_w^{K_s+K_u}].
\tag{49}
$$

分类规则可沿用 AVGZSL 的最近邻距离：

$$
\hat{y}_i
=
\arg\min_{c\in \mathcal{Y}^{s}\cup \mathcal{Y}^{u}}
\left\|\theta_{o_i}-\theta_{w}^{c}\right\|_2.
\tag{50}
$$

也可以使用相似度最大化：

$$
\hat{y}_i
=
\arg\max_{c\in \mathcal{Y}^{s}\cup \mathcal{Y}^{u}}
\theta_{o_i}^{T}\theta_w^c.
\tag{51}
$$

若模型存在 seen 类偏置，可继续使用 AVGZSL 中的 calibrated stacking。对于 seen 类 $c\in\mathcal{Y}^{s}$，对其分数施加校准项：

$$
s_c'=
\begin{cases}
s_c-\gamma, & c\in \mathcal{Y}^{s},\\
s_c, & c\in \mathcal{Y}^{u},
\end{cases}
\tag{52}
$$

其中 $\gamma$ 在验证集上根据 HM 选择。

##### 7.3.11.9 可选半监督扩展

如果进一步引入 Semi-IIN 的 self-training 思想，可以使用训练好的模型 $\phi$ 对无标签视频集合 $\mathcal{D}^{u}$ 生成伪标签：

$$
\hat{y}_i=\arg\max_{c}p(y=c|X_i^{v},X_i^{a}),
\tag{53}
$$

$$
q_i=\max_{c}p(y=c|X_i^{v},X_i^{a}).
\tag{54}
$$

对每个类别选择 top-k 置信度最高样本，或选择 $q_i>\delta$ 的样本构成伪标签集合 $\tilde{\mathcal{D}}$。半监督训练目标为：

$$
L_{semi}
=
L_{ce}+L_{reg}+L_{rec}
+\lambda_u L_{ce}^{pseudo},
\tag{55}
$$

其中：

$$
L_{ce}^{pseudo}
=
-\frac{1}{|\tilde{\mathcal{D}}|}
\sum_{(X_i^v,X_i^a,\hat{y}_i)\in \tilde{\mathcal{D}}}
\log p(y=\hat{y}_i|X_i^{v},X_i^{a}).
\tag{56}
$$

与 Semi-IIN 一致，建议伪标签样本只回传分类损失，不参与 $L_{reg}$ 和 $L_{rec}$，以降低错误伪标签对语义嵌入空间的破坏。

需要注意：如果无标签集合包含 unseen 测试类样本，则该设置应明确标注为 transductive GZSL；如果希望保持 inductive GZSL，则无标签数据不能包含测试集 unseen 样本的分布信息。

##### 7.3.11.10 方法优势总结

该序列版方案与两篇论文的结合点如下：

1. 继承 AVGZSL 的 CLIP/CLAP 特征和双文本类别嵌入，使模型仍然具备 zero-shot 类别迁移能力。
2. 将 AVGZSL 的单帧/全局音频输入扩展为视觉帧序列和音频片段序列，使模型能捕获关键帧与关键声音事件。
3. 借鉴 Semi-IIN 的 IntraMA/InterMA，将模态内时序线索和跨模态互补线索分开学习。
4. 借鉴 Semi-IIN 的 gate 机制，根据样本动态选择 intra-modal 或 inter-modal 信息，缓解固定拼接融合的不足。
5. 保留 AVGZSL 的 semantic alignment loss，使改进集中在音视频融合模块，不破坏原 baseline 的核心训练范式。

## 8. 证据链

### 8.1 来自 AVGZSL 的证据

1. AVGZSL 使用 CLIP/CLAP 作为冻结特征提取器，并利用二者文本编码器生成类别标签嵌入。

意义：新方案应继续保留这一强 baseline，不应破坏 CLIP/CLAP 语义空间。

2. AVGZSL 的音视频融合是直接 concat 后送入前馈网络。

意义：融合模块是最自然、改动最小的创新插入点。

3. AVGZSL 的消融表明，音频和视觉在不同数据集中的贡献不同。

意义：固定拼接不一定对所有样本最优，引入动态 gate 有合理依据。

4. AVGZSL 使用 `L_ce + L_rec + L_reg`，并证明完整训练目标整体表现最好。

意义：第一版结构改进应保留原损失，避免同时改变太多因素。

5. AVGZSL 原文强调简单模型在 CLIP/CLAP 特征下已经能超过更复杂方法。

意义：迁移 Semi-IIN 时应选择轻量 gate，而不是引入大型复杂 attention。

### 8.2 来自 Semi-IIN 的证据

1. Semi-IIN 的核心贡献是分别捕获 intra-modal 与 inter-modal 信息，再通过 gate 动态选择。

意义：这正好对应 AVGZSL 中音频、视觉贡献不稳定的问题。

2. Semi-IIN 消融显示，仅加入 MA 就能从 baseline 提升到更好结果：

```text
Baseline: MAE 0.509, Corr 0.793, Acc-2 83.97/86.85
Semi-IIN only MA: MAE 0.499, Corr 0.800, Acc-2 85.04/87.26
```

意义：分离 intra/inter 交互本身有效。

3. Semi-IIN 的 gate 融合优于 dot/add/concat：

```text
dot:    MAE 0.506, Corr 0.794, Acc-2 84.07/87.01
add:    MAE 0.512, Corr 0.794, Acc-2 83.45/86.85
concat: MAE 0.506, Corr 0.794, Acc-2 83.64/86.65
gate:   MAE 0.499, Corr 0.800, Acc-2 85.04/87.26
```

意义：动态选择比静态融合更有效，支持用 gate 替代 AVGZSL 的固定 concat。

4. Semi-IIN 的 case study 说明，有些样本中 inter-modal 分支会被无关视觉/音频信号干扰，而有些样本中 inter-modal 分支能修正单模态误判。

意义：AVGZSL 中也存在类似情况，例如声音主导类别、视觉主导动作类别、音视频冲突样本。

5. Semi-IIN 的 self-training 带来小幅提升：

```text
Baseline: MAE 0.509, Acc-2 83.97/86.85
Semi only: MAE 0.507, Acc-2 84.54/86.74
MA + Semi: MAE 0.497, Acc-2 84.98/87.70
```

意义：self-training 可作为增强模块，但其收益弱于结构上的 intra/inter + gate。

## 9. 建议实验设计

### 9.1 主实验

在 VGGSound-GZSLcls、UCF-GZSLcls、ActivityNet-GZSLcls 上对比：

```text
AVGZSL baseline
AVGZSL + intra/inter dual branch
AVGZSL + intra/inter dual branch + scalar gate
AVGZSL + intra/inter dual branch + vector gate
AVGZSL + gate + self-training
```

### 9.2 指标

沿用 AVGZSL：

```text
acc_S
acc_U
HM
acc_ZSL
```

重点关注：

- `HM`：GZSL 综合性能。
- `acc_U`：是否提升 unseen 类泛化。
- `acc_S`：是否因强调 unseen 而损伤 seen 类。

### 9.3 消融实验

建议至少做：

1. 无 gate，只 concat `z_intra` 和 `z_inter`。
2. scalar gate vs vector gate。
3. inter branch 使用 `concat(h_v, h_a)` vs `concat(h_v, h_a, h_v*h_a, |h_v-h_a|)`。
4. 是否加入 self-training。
5. 不同伪标签阈值或 top-k。

### 9.4 可解释性分析

可以画出不同数据集或类别上的 gate 均值：

```text
mean(g) on VGGSound
mean(g) on UCF
mean(g) on ActivityNet
```

预期：

- 声音强相关类别中，模型可能更依赖 audio/intra 信息。
- 动作视觉强相关类别中，模型可能更依赖 visual/intra 或 audio-visual inter 信息。
- 音视频互补类别中，inter gate 权重更高。

这可以作为论文中的可解释性证据。

## 10. 预期贡献写法

可以将改进贡献写成：

1. We propose an intra-inter gated fusion module for audio-visual generalized zero-shot learning, which separately models modality-specific and cross-modal interactive information.
2. We introduce a sample-adaptive gating mechanism to dynamically balance intra-modal and inter-modal cues, improving robustness under varying audio-visual reliability.
3. We further explore a confidence-based self-training strategy for semi-supervised audio-visual GZSL while preserving the semantic alignment framework based on CLIP and CLAP.

中文表述：

1. 提出一种面向音视频广义零样本学习的 intra-inter 门控融合模块，分别建模模态内判别信息和跨模态互补信息。
2. 引入样本级动态门控机制，自适应控制模态内信息与模态间交互信息的比例，缓解固定拼接融合在音视频贡献不均衡场景下的局限。
3. 在不破坏 CLIP/CLAP 语义对齐框架的前提下，探索基于高置信伪标签的半监督训练策略，以进一步利用无标签音视频数据。

## 11. 最终结论

最可行的方案是：

```text
AVGZSL + lightweight intra/inter branch + dynamic gate
```

而不是：

```text
AVGZSL + full Semi-IIN token-level architecture
```

原因是 AVGZSL 当前基于 CLIP/CLAP 全局特征，缺少 Semi-IIN 所需的 token/sequence 结构。轻量 intra/inter gate 既能继承 Semi-IIN 的核心思想，又符合 AVGZSL 原论文强调的简单、高效、强预训练特征范式。

如果需要进一步扩展，可以加入：

```text
confidence-based self-training
```

但必须明确其 inductive 或 transductive GZSL 设定，避免使用 unseen 测试信息造成不公平比较。
