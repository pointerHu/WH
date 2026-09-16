# SCER-AVGZSL：基于语义校准与证据路由的音视频广义零样本学习

## 新命名方案表

| 层级     | 中文名称                                     | English name                                                                              | 缩写                  | 功能说明                                                                                 |
| -------- | -------------------------------------------- | ----------------------------------------------------------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------- |
| 整体方法 | 基于语义校准与证据路由的音视频广义零样本学习 | Semantic Calibration and Evidence Routing for Audio-Visual Generalized Zero-Shot Learning | **SCER-AVGZSL** | 将类别语义校准、连续时序证据路由和可靠性感知关系融合统一到一个可迁移的音视频语义空间中。 |
| 模块一   | 类别语义结构校准                             | Class Semantic Structure Calibration                                                      | **CSSC**        | 在扩大类别判别间隔的同时保持原始语言空间的相对语义拓扑，生成可用于查询和分类的类别原型。 |
| 模块二   | 类别条件连续时序证据路由                     | Class-Conditioned Temporal Evidence Routing                                               | **CTER**        | 以候选类别原型为条件，为音频和视觉序列生成多区域连续时间分布并聚合类别相关证据。         |
| 模块三   | 可靠性感知交互分解与证据融合                 | Reliability-aware Interaction Decomposition and Evidence Fusion                           | **RIDE**        | 在严格的模态内和跨模态可见性边界下建模两类关系，并按样本—类别条件自适应融合多源证据。   |

## 关键设计说明

1. 早期条件化阶段只让类别语义分别作用于视觉序列和音频序列，不在该阶段进行音视频交叉注意力；跨模态信息交换统一留给后续关系分解模块，因此模态内分支具有明确的信息边界。
2. 每个高斯专家的权重先在时间轴上归一化，专家路由再在专家轴上归一化，二者的加权和构成合法的类别条件时间分布；训练时用真实已见类别的中心分散正则抑制专家塌缩。
3. 类别原型阶段只使用全部类别的名称和类别级描述，主网络阶段固定优化后的原型并仅使用已见类别音视频样本；训练分数的归一化范围为已见类别，推理时才扩展到已见与未见类别的并集。

## 3 方法

### 3.1 问题定义

音视频广义零样本学习（Audio-Visual Generalized Zero-Shot Learning, AVGZSL）要求模型根据视频中的视觉和音频信号，在训练阶段未出现过的类别上进行识别。设完整类别词典为 \(\mathcal{Y}\)，将其划分为互不相交的已见类别集合 \(\mathcal{Y}^{s}\) 和未见类别集合 \(\mathcal{Y}^{u}\)：

$$
\mathcal{Y}=\mathcal{Y}^{s}\cup\mathcal{Y}^{u},
\qquad
\mathcal{Y}^{s}\cap\mathcal{Y}^{u}=\varnothing .
\tag{1}
$$

训练集仅包含已见类别的音视频样本：

$$
\mathcal{D}^{s}=\left\{\left(U_i^{v},U_i^{a},y_i\right)\right\}_{i=1}^{N},
\qquad y_i\in\mathcal{Y}^{s},
\tag{2}
$$

其中，\(U_i^{v}\) 和 \(U_i^{a}\) 分别为第 \(i\) 个样本的原始视觉序列与原始音频序列，\(y_i\) 为真实类别，\(N\) 为训练样本数。类别名称、类别级属性和自然语言描述对 \(\mathcal{Y}^{s}\cup\mathcal{Y}^{u}\) 均可获得，它们是零样本迁移所允许的侧信息；但训练过程中不使用 \(\mathcal{Y}^{u}\) 的音频、视觉样本、样本标签、伪标签或样本统计量。

测试时，候选集合同时包含已见和未见类别。令 \(s_{i,c}\) 表示样本 \(i\) 在候选类别 \(c\) 条件下得到的音视频—语义匹配分数，则广义零样本预测写为

$$
\hat y_i=\arg\max_{c\in\mathcal{Y}^{s}\cup\mathcal{Y}^{u}}s_{i,c}.
\tag{3}
$$

与只在最终层匹配类别文本的做法不同，SCER-AVGZSL 将同一个类别原型依次用于语义结构校准、时间证据路由、关系可靠性判断和最终对齐，从而使未见类别也能沿着同一计算链路获得类别条件表示。

### 3.2 框架概述

给定一个视频，首先将其切分为 \(T\) 个不重叠且时间对齐的片段。冻结的视觉和音频预训练编码器分别输出片段级序列，轻量投影层将两种模态映射到共同维度。对于每个类别，模型从类别名称及固定模板组织的类别级描述中构建全局语义原型和属性语义 token；CSSC 在仅使用文本侧信息的独立阶段优化这些原型，使其同时具备清晰的分类间隔和可迁移的语义邻域关系。

主网络阶段固定 CSSC 输出的原型。对一个样本和一个候选类别，CTER 先将该类别的全局原型及属性 token 注入视觉、音频两个序列，但暂不发生跨模态信息交换；随后由两个模态各自预测多个高斯时间专家，得到连续、可归一化的类别相关时间分布，并增强被路由到的局部 token。RIDE 接收增强后的两种序列，在一个模态内分支和一个跨模态分支中使用不同的注意力可见性矩阵，分别形成模态特定关系表示与跨模态互补表示，同时保留高斯分支直接产生的局部摘要。最后，语义感知门控根据三类表示和候选原型预测融合权重，得到类别条件音视频表示并映射到统一语义空间。

训练时对每个已见候选类别计算分数，使用类别级监督对齐目标以及回归、语义重构和专家分散正则优化主网络。推理时将同一流程应用于 \(\mathcal{Y}^{s}\cup\mathcal{Y}^{u}\) 的全部类别，并在最终决策前对已见类别分数进行校准。整体数据流可以概括为

```text
冻结的音视频序列 → 共同维度投影
                         ↑
全部类别文本 → CSSC 类别原型 → CTER 连续证据路由
                                      ↓
                         RIDE 关系分解与可靠融合
                                      ↓
                         统一语义空间匹配与 GZSL 推理
```

CSSC 的输出是 CTER 的必要条件，CTER 产生的类别增强序列又是 RIDE 两个关系分支的唯一时序输入；因此三个模块不是独立并列的附加层，而是围绕类别条件证据建模形成的递进过程。

### 3.3 音视频与类别语义表示

#### 3.3.1 片段级音视频序列

为保留动作和声音事件的起始、持续与结束过程，将每个视频划分为 \(T\) 个不重叠片段。第 \(t\) 个片段的视觉帧和同步音频分别记为 \(x_{i,t}^{v}\) 与 \(x_{i,t}^{a}\)。采用冻结的 CLIP 图像编码器和 CLAP 音频编码器提取片段特征：

$$
f_{i,t}^{v}=E_{\mathrm{CLIP}}^{\mathrm{img}}(x_{i,t}^{v})\in\mathbb{R}^{d_v^0},
\qquad
f_{i,t}^{a}=E_{\mathrm{CLAP}}^{\mathrm{aud}}(x_{i,t}^{a})\in\mathbb{R}^{d_a^0},
\quad t=1,\ldots,T .
\tag{4}
$$

其中，\(d_v^0\) 和 \(d_a^0\) 为两个预训练编码器的原始输出维度。仅训练维度适配层和后续任务网络，预训练编码器参数在所有阶段保持冻结。设共同隐藏维度为 \(d\)，令可训练投影 \(P_v:\mathbb{R}^{d_v^0}\to\mathbb{R}^{d}\) 和 \(P_a:\mathbb{R}^{d_a^0}\to\mathbb{R}^{d}\)，\(\epsilon_v,\epsilon_a\in\mathbb{R}^{d}\) 为模态类型嵌入，\(\rho_t\in\mathbb{R}^{d}\) 为时间位置编码，则

$$
v_{i,t}=P_v f_{i,t}^{v}+\epsilon_v+\rho_t,
\qquad
a_{i,t}=P_a f_{i,t}^{a}+\epsilon_a+\rho_t .
\tag{5}
$$

由此得到 \(V_i=[v_{i,1};\ldots;v_{i,T}]\in\mathbb{R}^{T\times d}\) 和 \(A_i=[a_{i,1};\ldots;a_{i,T}]\in\mathbb{R}^{T\times d}\)。视觉与音频共享同一时间索引，但不假设它们必须在相同片段提供同等强度的类别证据；这种独立性由后续 CTER 的模态独立参数化保留。

#### 3.3.2 多粒度类别语义

对每个类别 \(c\in\mathcal{Y}\)，从类别名称及固定模板组织的类别级文本中整理六类描述：名称、动作过程、声音属性、典型场景、主体/物体以及与易混类别的区分线索。记描述集合为

$$
\mathcal{P}_c=\left\{\chi_{c,1},\ldots,\chi_{c,K_p}\right\},
\qquad c\in\mathcal{Y},
\tag{6}
$$

其中 \(K_p\) 为每类描述数量，所有类别采用相同的描述模板和筛选规则。设 CLIP 和 CLAP 文本编码器的输出维度分别为 \(d_{\mathrm{txt}}^{v}\) 和 \(d_{\mathrm{txt}}^{a}\)，并记 \(d_{\mathrm{text}}=d_{\mathrm{txt}}^{v}+d_{\mathrm{txt}}^{a}\)。对每条描述分别使用两个文本编码器，先独立归一化以平衡两种语义空间的尺度，再拼接并二次归一化为语义 token：

$$
\zeta_{c,k}=\operatorname{Norm}\!\left(
\left[
\operatorname{Norm}\!\left(E_{\mathrm{CLIP}}^{\mathrm{txt}}(\chi_{c,k})\right);
\operatorname{Norm}\!\left(E_{\mathrm{CLAP}}^{\mathrm{txt}}(\chi_{c,k})\right)
\right]\right)\in\mathbb{R}^{d_{\mathrm{text}}},
\quad k=1,\ldots,K_p .
\tag{7}
$$

其中 \(\operatorname{Norm}(x)=x/(\lVert x\rVert_2+\varepsilon)\) 表示带数值稳定项的 \(\ell_2\) 归一化，\([\cdot;\cdot]\) 表示特征维拼接。保留同一类别的描述级 token 集合

$$
S_c=[\zeta_{c,1};\ldots;\zeta_{c,K_p}]\in\mathbb{R}^{K_p\times d_{\mathrm{text}}},
\tag{8}
$$

并以其均值构造类别级初始语义原型

$$
\bar w_c=\operatorname{Norm}\!\left(\frac{1}{K_p}\sum_{k=1}^{K_p}\zeta_{c,k}\right)\in\mathbb{R}^{d_{\mathrm{text}}} .
\tag{9}
$$

其中，\(\bar w_c\) 表示类别的整体初始语义，\(S_c\) 保留动作、声音和场景等属性层次的细粒度差异。后续 CSSC 只更新类别级向量，属性 token 作为条件编码的补充语义，不与类别原型混为同一概念。

### 3.4 类别语义结构校准（CSSC）

预训练语言空间能够表达类别之间的语义邻近关系，却未必为当前类别词典提供足够清晰的分类边界。CSSC 的目标是在不抹平语义拓扑的前提下，拉开最容易混淆的类别。为每个类别引入可优化向量 \(u_c\)，并以 \(\bar w_c\) 初始化；其在前向计算中始终归一化为

$$
u_c\leftarrow \bar w_c,
\qquad
w_c=\operatorname{Norm}(u_c),
\qquad c\in\mathcal{Y} .
\tag{10}
$$

首先约束每个类别与其最近邻之间至少保持一个距离间隔。令 \([x]_+=\max(x,0)\)，类别分离损失定义为

$$
\mathcal{L}_{\mathrm{sep}}=
\frac{1}{|\mathcal{Y}|}
\sum_{c\in\mathcal{Y}}
\left[m_{\mathrm{sep}}-
\min_{j\in\mathcal{Y}\setminus\{c\}}\lVert w_c-w_j\rVert_2\right]_+,
\tag{11}
$$

其中 \(m_{\mathrm{sep}}>0\) 为最近邻分离间隔。单独增大距离会将语义相关类推向近似均匀的几何布局，因此进一步保持初始语义空间中的相对邻域排序。定义

$$
\operatorname{Dist}_{c,c'}^{0}=\lVert \bar w_c-\bar w_{c'}\rVert_2,
\qquad
\operatorname{Dist}_{c,c'}^{w}=\lVert w_c-w_{c'}\rVert_2,
\qquad
\mathcal{R}=\left\{(c,c',c''):\operatorname{Dist}_{c,c'}^{0}<\operatorname{Dist}_{c,c''}^{0},\ c'\ne c,\ c''\ne c,\ c'\ne c''\right\} .
\tag{12}
$$

对每个三元组，若初始空间中 \(c'\) 比 \(c''\) 更接近 \(c\)，则优化后仍要求 \(c'\) 保持更近，并留出 \(m_{\mathrm{sem}}\) 的排序间隔：

$$
\mathcal{L}_{\mathrm{sem}}=
\frac{1}{|\mathcal{R}|}
\sum_{(c,c',c'')\in\mathcal{R}}
\left[m_{\mathrm{sem}}+\operatorname{Dist}_{c,c'}^{w}-\operatorname{Dist}_{c,c''}^{w}\right]_+ .
\tag{13}
$$

综合两种约束，CSSC 的文本侧目标为

$$
\mathcal{L}_{\mathrm{proto}}=
\lambda_{\mathrm{sep}}\mathcal{L}_{\mathrm{sep}}+
\lambda_{\mathrm{sem}}\mathcal{L}_{\mathrm{sem}} .
\tag{14}
$$

其中 \(\lambda_{\mathrm{sep}}\) 和 \(\lambda_{\mathrm{sem}}\) 控制判别边界与语义保持的相对强度。该阶段的优化变量仅为 \(\{u_c\}_{c\in\mathcal{Y}}\)，初始文本特征和预训练编码器均不更新；类别数较大时可在每次迭代固定采样一组三元组近似 \(\mathcal{R}\)，但三元组的排序方向不变。

优化结束后记所得原型为 \(w_c^{\ast}\)。为了同时提供全局类别方向和属性级查询，构造类别语义库

$$
B_c=\left[P_s w_c^{\ast};\,P_d \zeta_{c,1};\ldots;P_d \zeta_{c,K_p}\right]
\in\mathbb{R}^{(K_p+1)\times d},
\tag{15}
$$

其中 \(P_s,P_d:\mathbb{R}^{d_{\mathrm{text}}}\to\mathbb{R}^{d}\) 为主网络中的可训练语义适配层。CSSC 阶段结束后 \(w_c^{\ast}\) 固定，\(P_s,P_d\) 在主网络阶段随其他任务参数更新。这样，原型的类别间结构不会被已见音视频样本重新塑形，而属性 token 仍能适配共同隐藏空间。

### 3.5 类别条件连续时序证据路由（CTER）

#### 3.5.1 语义条件化

当候选类别改变时，模型应当从同一音视频中读取不同的判别证据。CTER 首先在每个模态内部建立时间上下文，再将候选类别的语义库作为键和值注入该模态；此处不执行音视频交叉注意力，以保证后续 RIDE 的模态内分支不含未声明的跨模态信息。令 \(R_i^{v}=V_i\)、\(R_i^{a}=A_i\)，对 \(r\in\{v,a\}\) 定义

$$
\bar R_{i}^{r}=R_i^{r}+\operatorname{SA}_{r}(R_i^{r},R_i^{r},R_i^{r}),
\qquad
X_{i,c}^{r}=\operatorname{LN}\!\left(
\bar R_{i}^{r}+\operatorname{CA}_{r}(\bar R_{i}^{r},B_c,B_c)
\right)\in\mathbb{R}^{T\times d} .
\tag{16}
$$

\(\operatorname{SA}(Q,K,V)\) 和 \(\operatorname{CA}(Q,K,V)\) 分别表示多头自注意力和交叉注意力，第一参数为查询，后两参数为键和值；\(\operatorname{LN}\) 表示层归一化。由于 \(B_c\) 含有 \(w_c^{\ast}\) 与 \(S_c\) 的投影，视觉帧和音频片段可以在不同时间位置关注不同粒度的类别属性。\(X_{i,c}^{v}\) 与 \(X_{i,c}^{a}\) 因而是显式的样本—类别条件序列，但仍分别保留视觉和音频的信息边界。

#### 3.5.2 多高斯时间专家与路由

类别条件化只完成相关性重估，还需要将相关性转化为连续时间权重。首先用全局类别原型作为查询，对每个模态的条件序列聚合类别上下文：

$$
h_{i,r}^{c}=\operatorname{CA}\!\left(P_q w_c^{\ast},X_{i,c}^{r},X_{i,c}^{r}\right)\in\mathbb{R}^{d},
\qquad r\in\{v,a\},
\tag{17}
$$

其中 \(P_q:\mathbb{R}^{d_{\mathrm{text}}}\to\mathbb{R}^{d}\) 为查询投影层。令高斯专家数为 \(K_g\ge2\)，第 \(e\) 个专家的初始中心为 \(\bar\mu_e=(e-\tfrac12)/K_g\)。为了让专家从不同时间区域开始搜索，同时允许类别条件上下文进行连续修正，中心和尺度分别定义为

$$
\mu_{i,r,e}^{c}=\operatorname{clip}_{[0,1]}\!\left(
\bar\mu_e+\Delta_{\mu}\tanh\!\left(\phi_{\mu}^{r,e}[h_{i,r}^{c};w_c^{\ast}]\right)\right),
\tag{18}
$$

$$
\sigma_{i,r,e}^{c}=\sigma_{\min}+
(\sigma_{\max}-\sigma_{\min})\operatorname{sigmoid}\!\left(
\phi_{\sigma}^{r,e}[h_{i,r}^{c};w_c^{\ast}]\right),
\tag{19}
$$

其中 \(\phi_{\mu}^{r,e}\) 和 \(\phi_{\sigma}^{r,e}\) 是模态—专家特定的可学习标量映射，\(0<\sigma_{\min}<\sigma_{\max}\)，\(\Delta_{\mu}\) 控制中心偏移范围，\(\operatorname{clip}_{[0,1]}\) 将中心限制在归一化时间区间内。令 \(\xi_t=(t-\tfrac12)/T\)，第 \(e\) 个专家在第 \(t\) 个片段上的高斯权重为

$$
g_{i,r,e}^{c}(t)=
\frac{\exp\!\left(-\frac{(\xi_t-\mu_{i,r,e}^{c})^2}{2(\sigma_{i,r,e}^{c})^2}\right)}
{\displaystyle\sum_{t'=1}^{T}\exp\!\left(-\frac{(\xi_{t'}-\mu_{i,r,e}^{c})^2}{2(\sigma_{i,r,e}^{c})^2}\right)},
\qquad \sum_{t=1}^{T}g_{i,r,e}^{c}(t)=1 .
\tag{20}
$$

不同样本和候选类别对各时间区域的需求不同，因此由路由器在专家维度上预测权重

$$
\boldsymbol{\pi}_{i,r}^{c}=\operatorname{Softmax}_{e}\!\left(
W_{\pi}^{r}[h_{i,r}^{c};w_c^{\ast}]
\right)\in\mathbb{R}^{K_g},
\tag{21}
$$

其中 \(\operatorname{Softmax}_{e}\) 明确沿 \(K_g\) 个专家的索引归一化，可学习矩阵 \(W_{\pi}^{r}\) 的输出维度为 \(K_g\)。综合时间权重与专家路由，得到类别条件的整体时间分布

$$
\omega_{i,r}^{c}(t)=\sum_{e=1}^{K_g}\pi_{i,r,e}^{c}g_{i,r,e}^{c}(t),
\qquad \sum_{t=1}^{T}\omega_{i,r}^{c}(t)=1 .
\tag{22}
$$

利用 \(\omega\) 对相关片段进行软增强，同时保留一条不经过深层关系变换的直接局部摘要：

$$
\widetilde X_{i,c}^{r}(t)=\left[1+\kappa T\omega_{i,r}^{c}(t)\right]X_{i,c}^{r}(t),
\qquad
z_{i,r}^{G,c}=\sum_{t=1}^{T}\omega_{i,r}^{c}(t)X_{i,c}^{r}(t)\in\mathbb{R}^{d},
\tag{23}
$$

其中 \(\kappa\ge0\) 为增强强度，上标 \(G\) 表示由高斯时间分布直接汇聚的证据。由于视觉和音频分别预测 \(\mu\)、\(\sigma\) 和 \(\boldsymbol{\pi}\)，两种模态可以关注不同的时间区域；多个均匀初始化的专家则能够覆盖一个事件的多个连续阶段。为抑制多个专家退化到同一中心，在训练目标中对真实类别加入中心分散项：

$$
\mathcal{L}_{\mathrm{div}}=
\frac{1}{N}\sum_{i=1}^{N}\frac{1}{2}\sum_{r\in\{v,a\}}
\frac{2}{K_g(K_g-1)}\sum_{1\le e<e'\le K_g}
\exp\!\left(-\frac{|\mu_{i,r,e}^{y_i}-\mu_{i,r,e'}^{y_i}|}{\eta}\right),
\tag{24}
$$

其中 \(\eta>0\) 控制惩罚衰减。该项只读取已见训练样本的真实类别条件中心，不引入任何未见类别音视频信息。

### 3.6 可靠性感知交互分解与证据融合（RIDE）

#### 3.6.1 受控 token 布局与注意力可见性

CTER 输出的 \(\widetilde X_{i,c}^{a}\) 和 \(\widetilde X_{i,c}^{v}\) 仍然是两个独立序列。RIDE 为模态内关系和跨模态关系建立不同的聚合 token，并分别用上标 \(I\) 和 \(C\) 标记这两条路径。模态内分支使用音频聚合 token \(c_a\) 和视觉聚合 token \(c_v\)，跨模态分支只使用联合聚合 token \(c_{av}\)；三者均为可学习的 \(d\) 维向量：

$$
Z_{i,c}^{I,0}=\left[c_a;\widetilde X_{i,c}^{a};c_v;\widetilde X_{i,c}^{v}\right],
\qquad
Z_{i,c}^{C,0}=\left[c_{av};\widetilde X_{i,c}^{a};\widetilde X_{i,c}^{v}\right].
\tag{25}
$$

前者长度为 \(2T+2\)，后者长度为 \(2T+1\)，所有 token 均位于 \(\mathbb{R}^{d}\)，相应掩码满足 \(M_I\in\mathbb{R}^{(2T+2)\times(2T+2)}\) 和 \(M_C\in\mathbb{R}^{(2T+1)\times(2T+1)}\)。在模态内分支中，令 \(\operatorname{grp}(p)\in\{a,v\}\) 表示位置 \(p\) 所属的模态组，其中 \(c_a\) 与音频 token 同组，\(c_v\) 与视觉 token 同组。以行索引为查询、列索引为键，模态内掩码定义为

$$
M_I(p,q)=
\begin{cases}
0,&\operatorname{grp}(p)=\operatorname{grp}(q),\\
-\infty,&\operatorname{grp}(p)\ne\operatorname{grp}(q).
\end{cases}
\tag{26}
$$

该块对角结构使两个聚合 token 也不能跨组访问，因而模态内表示不存在经由共享 token 产生的间接跨模态泄漏。跨模态分支中，位置 0 为联合聚合 token，普通 token 的模态标记记为 \(\operatorname{mod}(p)\in\{a,v\}\)。其掩码为

$$
M_C(p,q)=
\begin{cases}
0,&p=0\ \text{或}\ q=0,\\
0,&\operatorname{mod}(p)\ne\operatorname{mod}(q),\\
-\infty,&\text{其他情况}.
\end{cases}
\tag{27}
$$

因此普通音频 token 与视觉 token 直接交互，联合 token 可以读取并汇总两种模态；同一模态普通 token 之间不在该分支重复建模。联合 token 所形成的信息交换是跨模态路径的显式设计，而不是模态内路径的隐式信息通道。

#### 3.6.2 掩码关系编码

对分支 \(b\in\{I,C\}\)，定义带掩码的多头注意力为

$$
\operatorname{MA}_{b}(Z;M_b)=
\operatorname{Softmax}_{\mathrm{key}}\!\left(
\frac{(ZW_{Q}^{b})(ZW_{K}^{b})^{\top}}{\sqrt{d_k}}+M_b
\right)ZW_{V}^{b},
\tag{28}
$$

其中 \(W_Q^b,W_K^b\in\mathbb{R}^{d\times d_k}\)、\(W_V^b\in\mathbb{R}^{d\times d}\) 为可学习投影，\(\operatorname{Softmax}_{\mathrm{key}}\) 对每个查询行的可见键归一化。下式为简洁起见省略样本和候选类别下标，采用预归一化残差 Transformer 更新两条分支：

$$
\bar Z_b^{\ell}=Z_b^{\ell-1}+\operatorname{MA}_b\!\left(\operatorname{LN}(Z_b^{\ell-1});M_b\right),
\qquad
Z_b^{\ell}=\bar Z_b^{\ell}+\operatorname{FFN}_b\!\left(\operatorname{LN}(\bar Z_b^{\ell})\right),
\quad \ell=1,\ldots,L .
\tag{29}
$$

其中 \(L\) 为关系编码层数，\(\operatorname{LN}\) 和 \(\operatorname{FFN}\) 分别表示层归一化和逐 token 前馈网络。由于两条分支共享输入但不共享掩码和参数，它们分别学习稳定的模态内演化与跨模态互补关系。

#### 3.6.3 可靠性感知融合

经过 \(L\) 层更新，从模态内分支读取两个独立聚合 token，从跨模态分支读取联合 token，并通过可训练投影 \(P_I,P_C,P_G\) 映射到同一融合维度 \(d_f\)：

$$
z_{i,c}^{I}=P_I\left[Z_{i,c}^{I,L}[0];Z_{i,c}^{I,L}[T+1]\right],
\qquad
z_{i,c}^{C}=P_C Z_{i,c}^{C,L}[0],
\tag{30}
$$

其中 \(P_I:\mathbb{R}^{2d}\to\mathbb{R}^{d_f}\) 包含拼接后的维度适配，\(P_C:\mathbb{R}^{d}\to\mathbb{R}^{d_f}\) 处理联合 token，二者输出均属于 \(\mathbb{R}^{d_f}\)。为了不让深层关系编码稀释局部时间证据，保留两个模态的 CTER 直接摘要，并构造交互统计量

$$
z_{i,c}^{G}=P_G\left[
z_{i,v}^{G,c};z_{i,a}^{G,c};
z_{i,v}^{G,c}\odot z_{i,a}^{G,c};
\left|z_{i,v}^{G,c}-z_{i,a}^{G,c}\right|
\right]\in\mathbb{R}^{d_f} .
\tag{31}
$$

式（31）中的 \(P_G:\mathbb{R}^{4d}\to\mathbb{R}^{d_f}\) 为可训练投影，\(\odot\) 表示逐元素乘法，\(|\cdot|\) 表示逐元素绝对值，分号表示特征拼接。

三种表示分别编码模态内稳定线索、跨模态互补关系和被连续时间分布直接选出的局部证据。它们对不同样本和候选类别的重要性并不固定，因此使用候选原型参与门控：

$$
\boldsymbol{\gamma}_{i,c}=\operatorname{Softmax}_{3}\!\left(
\Psi_{\gamma}\left[z_{i,c}^{I};z_{i,c}^{C};z_{i,c}^{G};P_gw_c^{\ast}\right]
\right)\in\mathbb{R}^{3},
\tag{32}
$$

其中 \(\Psi_{\gamma}\) 为输出三维 logits 的多层感知机，\(P_g:\mathbb{R}^{d_{\mathrm{text}}}\to\mathbb{R}^{d_f}\) 将类别原型映射到门控输入空间，\(\operatorname{Softmax}_{3}\) 沿三类证据分支归一化，且 \(\boldsymbol{\gamma}_{i,c}=[\gamma_{i,c}^{I},\gamma_{i,c}^{C},\gamma_{i,c}^{G}]\)。最终的类别条件音视频表示为

$$
z_{i,c}=\gamma_{i,c}^{I}z_{i,c}^{I}+\gamma_{i,c}^{C}z_{i,c}^{C}+\gamma_{i,c}^{G}z_{i,c}^{G}\in\mathbb{R}^{d_f} .
\tag{33}
$$

三路权重严格对应三种实际输入表示。候选类别语义同时影响时间路由和最终门控，因此相同样本在不同候选类别下可以形成不同的证据组织方式。

### 3.7 语义对齐目标与两阶段训练

#### 3.7.1 类别级音视频—语言对齐

RIDE 输出的 \(z_{i,c}\) 已经包含候选类别条件，但仍需映射到已见和未见类别共享的语义空间。分别使用音视频投影头 \(W_o\) 和文本投影头 \(W_w\) 得到单位化表示

$$
\theta_{i,c}^{o}=\operatorname{Norm}(W_o z_{i,c}),
\qquad
\theta_c^{w}=\operatorname{Norm}(W_w w_c^{\ast}),
\qquad
\theta_{i,c}^{o},\theta_c^{w}\in\mathbb{R}^{d_{\mathrm{emb}}} .
\tag{34}
$$

其中，\(W_o:\mathbb{R}^{d_f}\to\mathbb{R}^{d_{\mathrm{emb}}}\)、\(W_w:\mathbb{R}^{d_{\mathrm{text}}}\to\mathbb{R}^{d_{\mathrm{emb}}}\) 均为可学习投影，\(\theta_{i,c}^{o}\) 是样本 \(i\) 在类别 \(c\) 条件下形成的音视频表示，\(\theta_c^{w}\) 是该类别的共享语义锚点。二者的温度缩放余弦分数定义为

$$
s_{i,c}=\frac{(\theta_{i,c}^{o})^{\top}\theta_c^{w}}{\tau},
\qquad \tau>0 .
\tag{35}
$$

其中 \(\tau\) 是正温度超参数。由于编码过程本身依赖候选类别，训练时对每个样本显式计算全部已见类别 \(c\in\mathcal{Y}^{s}\) 的 \(s_{i,c}\)，并采用类别级监督对齐目标

$$
\mathcal{L}_{\mathrm{align}}=-\frac{1}{N}\sum_{i=1}^{N}
\log\frac{\exp(s_{i,y_i})}
{\displaystyle\sum_{c\in\mathcal{Y}^{s}}\exp(s_{i,c})} .
\tag{36}
$$

式（36）的分母是已见类别词典，而不是当前批次中的样本标签集合。因而同类样本在批次中重复出现不会重复构造语义负类，训练与推理使用的“候选类别打分”语义也保持一致。

仅依赖相对分类分数可能使真实类别对在嵌入空间中仍存在较大绝对偏差，因此加入真值类别上的回归约束

$$
\mathcal{L}_{\mathrm{reg}}=\frac{1}{N}\sum_{i=1}^{N}
\left\lVert\theta_{i,y_i}^{o}-\theta_{y_i}^{w}\right\rVert_2^2 .
\tag{37}
$$

此外，CSSC 通过相对距离保持语义拓扑，而共同投影头仍可能丢失初始语言信息。令 \(D_o,D_w:\mathbb{R}^{d_{\mathrm{emb}}}\to\mathbb{R}^{d_{\mathrm{text}}}\) 为两个轻量解码器，语义重构项定义为

$$
\mathcal{L}_{\mathrm{rec}}=
\frac{1}{N}\sum_{i=1}^{N}
\left\lVert D_o(\theta_{i,y_i}^{o})-\bar w_{y_i}\right\rVert_2^2
+\frac{1}{|\mathcal{Y}|}\sum_{c\in\mathcal{Y}}
\left\lVert D_w(\theta_c^{w})-\bar w_c\right\rVert_2^2 .
\tag{38}
$$

第一项要求真实类别条件下的音视频表示能够恢复对应初始语义，第二项使文本投影对完整类别词典保持可逆的语义锚定。第二项只使用类别级文本向量，即使求和包含 \(\mathcal{Y}^{u}\)，也不涉及未见类别的任何样本信息。

主网络的完整目标为

$$
\mathcal{L}_{\mathrm{main}}=
\mathcal{L}_{\mathrm{align}}
+\lambda_{\mathrm{reg}}\mathcal{L}_{\mathrm{reg}}
+\lambda_{\mathrm{rec}}\mathcal{L}_{\mathrm{rec}}
+\lambda_{\mathrm{div}}\mathcal{L}_{\mathrm{div}},
\tag{39}
$$

其中 \(\lambda_{\mathrm{reg}}\)、\(\lambda_{\mathrm{rec}}\) 和 \(\lambda_{\mathrm{div}}\) 为非负权重。四项损失分别约束类别级判别、真实类别绝对对齐、共同空间的语义可逆性和时间专家覆盖范围，作用对象互不替代。

#### 3.7.2 两阶段优化协议

记除冻结编码器和固定类别原型以外的全部主网络可训练参数为 \(\Theta\)。整个模型按以下顺序优化：

$$
\{u_c^{\star}\}_{c\in\mathcal{Y}}
=\arg\min_{\{u_c\}_{c\in\mathcal{Y}}}\mathcal{L}_{\mathrm{proto}},
\qquad
\Theta^{\star}=\arg\min_{\Theta}
\mathcal{L}_{\mathrm{main}}\!\left(\mathcal{D}^{s};\{w_c^{\ast}\}_{c\in\mathcal{Y}}\right),
\quad w_c^{\ast}=\operatorname{Norm}(u_c^{\star})\ \text{固定} .
\tag{40}
$$

第一阶段仅以所有类别的 \(\bar w_c\) 为输入更新类别向量 \(u_c\)，得到 CSSC 原型 \(w_c^{\ast}\)。第二阶段冻结 \(w_c^{\ast}\)、CLIP 和 CLAP 编码器，使用 \(\mathcal{D}^{s}\) 更新主网络参数集合 \(\Theta\)，其中包括模态投影、语义适配层、CTER 参数、RIDE 参数、对齐投影头和重构解码器。未见类别文本可以进入冻结原型库以及式（38）的纯文本重构项，但未见类别音视频从不进入任一优化步骤。

在第二阶段，对齐损失需要为每个训练样本计算所有已见候选类别；回归、音视频重构和中心分散项只在真实类别 \(y_i\) 上计算。该分工使类别间竞争与样本级辅助约束具有明确范围，也避免把未见类别错误地当作带音视频监督的负类或正类。

### 3.8 广义零样本推理

测试时固定全部模型参数。对于样本 \((U_i^v,U_i^a)\)，依次令每个 \(c\in\mathcal{Y}^{s}\cup\mathcal{Y}^{u}\) 的 \(B_c\) 和 \(w_c^{\ast}\) 进入 CTER、RIDE 与语义投影头，并根据式（35）得到统一分数。为减弱模型因只接受已见音视频监督而产生的已见类偏置，仅在推理阶段采用 calibrated stacking：

$$
s_{i,c}^{\mathrm{cal}}=s_{i,c}-\beta_{\mathrm{cal}}\,\mathbb{I}[c\in\mathcal{Y}^{s}],
\qquad \beta_{\mathrm{cal}}\ge0,
\tag{41}
$$

其中，\(\mathbb{I}[\cdot]\) 为指示函数，\(\beta_{\mathrm{cal}}\) 由与最终测试集隔离的验证协议确定，不使用测试标签或测试样本统计量。最终预测为

$$
\hat y_i=\arg\max_{c\in\mathcal{Y}^{s}\cup\mathcal{Y}^{u}}
s_{i,c}^{\mathrm{cal}} .
\tag{42}
$$

精确推理需要对 \(|\mathcal{Y}^{s}|+|\mathcal{Y}^{u}|\) 个类别执行条件编码，其复杂度随候选类别数线性增长。类别语义库、文本投影和掩码矩阵均可预先缓存；当类别词典很大时，可在部署阶段用类别无关的全局音视频表示召回 Top-\(K_{\mathrm{ret}}\) 类别，其中 \(K_{\mathrm{ret}}\) 为预设召回数，再用完整 SCER-AVGZSL 重排序。论文主算法及标准评测仍以全部候选类别的精确打分为准。

通过上述训练与推理协议，类别语义首先被校准为具有判别性且保持拓扑的查询原型，随后连续路由音视频局部证据、调节关系分支的融合比例，并最终作为已见与未见类别共享的分类锚点。由此，SCER-AVGZSL 在不接触未见类别音视频样本的前提下完成从类别语义到时序证据、从模态关系到广义零样本决策的闭环。
