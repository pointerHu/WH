# Question-Aware Gaussian Experts for Audio-Visual Question Answering
**Hongyeob Kim¹\* Inyoung Jung¹\* Dayoon Suh² Youjia Zhang¹ Sangmin Lee¹ Sungeun Hong¹†**
¹Sungkyunkwan University ²Purdue University  
\*Equal Contribution. †Corresponding Author.  
CVPR 2025 Open Access Version

---

## Abstract
Audio-Visual Question Answering (AVQA) requires not only question-based multimodal reasoning but also precise temporal grounding to capture subtle dynamics for accurate prediction. However, existing methods mainly use question information implicitly, limiting focus on question-specific details. Furthermore, most studies rely on uniform frame sampling, which can miss key question-relevant frames. Although recent Top-K frame selection methods aim to address this, their discrete nature still overlooks fine-grained temporal details. This paper proposes **QA-TIGER**, a novel framework that explicitly incorporates question information and models continuous temporal dynamics. Our key idea is to use Gaussian-based modeling to adaptively focus on both consecutive and non-consecutive frames based on the question, while explicitly injecting question information and applying progressive refinement. We leverage a Mixture of Experts (MoE) to flexibly implement multiple Gaussian models, activating temporal experts specifically tailored to the question. Extensive experiments on multiple AVQA benchmarks show that QA-TIGER consistently achieves state-of-the-art performance. Code is available at https://aim-skku.github.io/QA-TIGER/

---

## 1. Introduction
Audio-Visual Question Answering (AVQA) focuses on analyzing and interpreting both audio and visual cues to provide accurate answers to questions. Recent advancements in AVQA have focused on spatial and temporal grounding [3,13,16], parameter-efficient models [5,24,37], and bias adjustments [14,28]. Despite promising results, many existing methods struggle to capture fine-grained, question-specific details and temporal cues essential for effective reasoning. We argue that two key considerations are critical for successful AVQA: (i) flexibly capturing and integrating question-relevant audio-visual cues across temporal contexts, and (ii) embedding question context explicitly within the audio-visual feature processing stages.

Most AVQA methods use uniform sampling or discrete frame selection [16,24,37], often overlooking question-specific details. These methods treat frames equally missing important, question-relevant information in both audio and visual modalities. Recent approaches such as PSTP [17] and TSPM [19] use Top-K frame selection to improve context relevance by aligning frames with the question. However, they select them based solely on visual cues, relying on discrete sampling that disrupts continuity by ignoring temporal cues. Additionally, this approach focuses mainly on visual alignment, missing crucial audio details.

In terms of question integration, most AVQA models incorporate question information only at the final reasoning stage, typically by simple multiplication [12,16,19,24]. This late-stage integration limits the model’s ability to encode question-specific features during intermediate steps, reducing the effectiveness of reasoning. Although several methods attempt to enhance reasoning by using question details in frame selection [17,19], this is done indirectly, and they fail to explicitly embed question context within the audio-visual encoding pipeline. This limited approach restricts the model’s ability to focus on relevant temporal cues progressively.

In this paper, we propose **QA-TIGER (Question-Aware Temporal Integration of Gaussian Experts for Reasoning)** as illustrated in Figure 1. To address issue (i), QA-TIGER introduces a multi-Gaussian weighting mechanism embedded within a Mixture of Experts (MoE) framework [32]. This approach assigns adaptive weights across both consecutive and non-consecutive temporal spans, thereby enabling the model to capture complex temporal dependencies more effectively. Gaussian experts are adaptively activated with well-positioned centers, reducing redundancy and simultaneously improving temporal alignment. In contrast to previous methods, which strictly align audio cues with corresponding visual frames [17,19], QA-TIGER provides explicit temporal grounding for both audio and visual modalities independently. This allows for more accurate and robust alignment with the question-relevant segments.

To address issue (ii), QA-TIGER incorporates question information early in the process, creating question-aware features that permeate both the visual and audio modalities. By embedding question context directly into each modality’s features, QA-TIGER aligns with the question context throughout the entire pipeline, unlike prior methods that add question information only at the final stage [16,17,19,24]. This approach allows the model to progressively refine its focus based on the question, resulting in deeper and more explicit integration of question relevance. Ultimately, this approach enhances accuracy and contextual alignment across all reasoning stages.

Our contributions can be summarized as follows:
- We propose QA-TIGER, a framework that adaptively models temporal dynamics using strategically positioned Gaussian experts, capturing question-relevant information across continuous temporal spans and adjusting segment importance.
- We introduce a question-aware attention mechanism that incorporates question context carefully in the audio-visual encoding process, enabling progressive refinement of temporal focus and more effective feature extraction.
- QA-TIGER achieves state-of-the-art performance across multiple benchmark datasets and provides an in-depth analysis of the impact of frame selection strategies, an area that has been previously underexplored in AVQA.

---

## 2. Related Works
Audio-Visual Question Answering (AVQA) has advanced with datasets like MUSIC-AVQA [16], AVQA [40], and Pano-AVQA [46], enabling fine-grained reasoning [18,34]. Early works have implemented spatial-temporal groundings for fine-grained audio-visual scene understanding and reasoning [16,40]. Recently, adapter-based architectures [5,24,37] have achieved impressive performance by leveraging frozen pretrained vision transformers for efficiency. COCA [14] and M2KVDG [25] achieve multimodal collaboration with causal graphs, enhancing the model’s robustness. APL [23] introduced an object-aware approach that employs adaptive-positivity learning to align question-object and audio-object semantics. Building on prior work, this study focuses on two often underexplored aspects: explicitly integrating question information and an effective frame sampling strategy to enhance temporal reasoning.

### 2.1. Question Awareness
In recent multimodal AVQA research, question-awareness [4,21,33,41] has been recognized as crucial for aligning questions with visual and auditory features. However, most AVQA models [16,23,24] only incorporate question awareness at the final reasoning stage, which limits its impact throughout the entire process. Although several methods utilize question information for key-frame selection [17,19], this is typically applied in an implicit manner, further constraining their reasoning capabilities. While models like QA-ViT [7] embed question information early in the encoding process, they primarily focus on interactions between frame tokens (i.e., patches) and the question within a single frame. In contrast, our approach explicitly embeds question information early in the process, selectively integrating modality-relevant details along the temporal axis. This ensures consistent alignment with the question context throughout the AVQA pipeline, allowing the model to progressively refine its focus on relevant temporal cues and improving the ability to leverage both visual and audio information.

### 2.2. Temporal Grounding
Understanding and reasoning over extended audio or video, often containing redundant information, is a key challenge in QA. A critical task is localizing specific temporal segments that align with a natural language query, reducing redundancy. Temporal grounding focuses on accurately identifying these relevant moments. Many existing QA methods, such as proposal-based [36,44,47] or proposal-free [6,20,29,45] models like SMIN [35], optimize multilevel interactions between the question and video segments. However, these approaches often rely on predefined knowledge, adding computational overhead. To mitigate this, many AVQA models [16,24,37,42] use uniform sampling, which overlooks question-specific details and treats the temporal dimension as discrete. Recent studies [17,19] attempt to select frames based on question relevance, yet they still treat the temporal dimension as discrete, limiting their ability to capture continuous video dynamics. In contrast, our approach embeds temporal dependencies using Gaussian distributions, enabling continuous modeling of question-relevant segments. This ensures precise alignment with both audio and visual modalities, improving temporal grounding and overall reasoning. By adapting to both consecutive and non-consecutive spans, QA-TIGER captures and utilizes relevant temporal information more effectively than methods that rely on discrete sampling.

---

## 3. Method
QA-TIGER aims to dynamically weight temporal segments based on question relevance and explicitly integrate question context, as shown in Figure 2.

### 3.1. Input Representation
The input video sequence is split into T non-overlapping 1s segments, each with paired audio and visual elements.

**Visual Representation.** Each visual segment is processed using a pretrained CLIP model [30]. The visual input is divided into M patches per segment, with a special <[BOS_never_used_51bce0c785ca2f68081bfa7d91973934]> token added at the beginning. Visual features are extracted in two forms: Frame-level features \(v={v^{t}}_{t=1}^{T} \in \mathbb{R}^{T ×D}\) are obtained from the <[BOS_never_used_51bce0c785ca2f68081bfa7d91973934]> token output for each segment t. Patch-level features \(p={p^{t}}_{t=1}^{T} \in \mathbb{R}^{T ×M' ×D}\) are obtained by merging the M patch tokens into \(M'\) tokens per segment using Token Merging (ToMe) [2], providing more spatially detailed information.

**Audio Representation.** For each segment t, we extract audio features \(a^{t} \in \mathbb{R}^{D}\) using a VGGish model [11] pretrained on AudioSet [8], following previous work. The complete set of audio features is \(a={a^{t}}_{t=1}^{T} \in \mathbb{R}^{T ×D}\).

**Question Representation.** The input question is tokenized and processed using the CLIP text encoder. We extract sentence-level features \(q_{s} \in \mathbb{R}^{D}\) from the [EOT] token. Additionally, we obtain word-level features \(q_{w} \in \mathbb{R}^{N ×D}\) by skipping CLIP’s final projection layer, where N is the number of tokens including padding.

### 3.2. Question-Aware Fusion
For effective AVQA, our question-aware attention module explicitly injects question context into both the video and audio modalities. Our question-aware fusion module operates in two main stages. First, multi-head Self-Attention (SA) enhances internal relationships within each modality by using the same input for the query, key, and value. Then, each modality undergoes two rounds of multi-head Cross-Attention (CA): visual features v use audio features a as the key and value, with v as the query, and then apply word-level question feature \(q_{w}\) as the key and value to align with question information. Similarly, audio features a use visual features v and question features \(q_{w}\) sequentially as key and value, with a as the query. This dual CA application per modality enables explicit question-informed crossmodal interactions. Finally, the outputs from the SA and two CA layers are combined with residual connections to enhance temporal coherence and retain alignment with the question as follows:
\[v_{q}=v+SA(v,v,v)+CA(v,a,a)+CA(v,q_{w},q_{w}) \tag{1}\]
\[a_{q}=a+SA(a,a,a)+CA(a,v,v)+CA(a,q_{w},q_{w}) \tag{2}\]

The result is two question-aligned multimodal features, \(v_{q}={v_{q}^{t}}_{t=1}^{T} \in \mathbb{R}^{T ×D}\) for visual and \(a_{q}={a_{q}^{t}}_{t=1}^{T} \in \mathbb{R}^{T ×D}\) for audio. Unlike prior approaches that integrate question information only in the final stages, our method introduces question context from the start, allowing QA-TIGER to dynamically refine focus on relevant temporal cues throughout AVQA processing.

Once the question-aware visual features \(v_{q}\) and audio features \(a_{q}\) are obtained, we further refine the patch-level visual features to align finer spatial details with the question context. This refinement ensures that finer spatial details in the visual data align more closely with the question context embedded in the modality-specific features. The process is formulated as follows:
\[p_{v}=p+SA(p, p, p)+CA\left(v_{q}, p, p\right) \tag{3}\]
\[p_{a}=p+SA(p, p, p)+CA\left(a_{q}, p, p\right) \tag{4}\]

### 3.3. Temporal Integration of Gaussian Experts
To capture temporal dependencies in the video, we leverage the Mixture of Experts (MoE) framework [32], integrating multiple Gaussian distributions across the timeline. This approach enables the model to focus on distinct temporal segments relevant to the question.

**Gaussian Generation.** To produce question-relevant Gaussian distributions, we first generate a condensed, question-focused representation for each modality. This process aligns the visual and audio features with the question, to capture the temporal relevance of frames in both modalities. Using a cross-attention mechanism, we apply the sentence-level question feature \(q_{s}\) to the question-aware features \(v_{q}\) and \(a_{q}\), yielding D-dimensional aggregated representations for each modality:
\[v_{q}^{\prime }=CA(q_{s},v_{q},v_{q}),\ a_{q}^{\prime }=CA(q_{s},a_{q},a_{q}) \tag{5}\]

In contrast to prior work [39], which used a single Gaussian mask across the temporal domain, we generate multiple Gaussian distributions to capture a broader range of key frames, especially in cases where temporal variations are complex and challenging. The Gaussian distributions \(g={g^{i}}_{i=1}^{E}\) represent distinct temporal segments relevant to the question, where E is the total number of Gaussian experts (i.e., Gaussian distributions):
\[g_{v}=\mathcal{N}\left(\mu_{v}^{i},\left(\sigma_{v}^{i}\right)^{2}\right),\ g_{a}=\mathcal{N}\left(\mu_{a}^{i},\left(\sigma_{a}^{i}\right)^{2}\right) \tag{6}\]

Here, \({\mu^{i}}_{i=1}^{E}\) and \({\sigma^{i}}_{i=1}^{E}\) denote the Gaussian centers and standard deviations, generated through a linear layer with an input dimension of D and an output dimension of two. To minimize conflicts across time segments and enhance temporal focus, the Gaussian centers are distributed along the timeline, with a predicted offset by a linear layer added to the initial centers. This ensures that each expert mainly covers a distinct segment, aligning with question-relevant frames and reducing redundancy.

**Integrating Temporal Information.** To selectively capture relevant segments over time, we adapt the MoE framework, which combines multiple specialized “experts,” each trained to focus on specific temporal patterns. Instead of selecting discrete experts, our model adjusts the influence of each expert based on their context-dependent weights. These experts act as Gaussian distributions along the timeline, providing soft masks that help capture temporal dependencies in alignment with the question.

The router assigns routing values \(r_{v}={r_{v}^{i}}_{i=1}^{E}\) and \(r_{a}={r_{a}^{i}}_{i=1}^{E}\) for each expert based on the cross-attention outputs \(v_{q}'\) and \(a_{q}'\), respectively:
\[r_{v}=Softmax\left(v_{q}' \cdot W\right),\ r_{a}=Softmax\left(a_{q}' \cdot W\right) \tag{7}\]
where \(W \in \mathbb{R}^{D ×E}\) is a learnable weight matrix that dynamically controls the influence of each expert. The resulting expert weights allow the model to emphasize question-relevant time segments more effectively. The outputs from all experts are then combined through a weighted summation, producing a temporally integrated representation that captures question-specific insights across frames. This integration is expressed as follows:
\[\tilde {v}_{p_{v}}=\mathcal {G}_{v}(p_{v}),\ \tilde {v}_{p_{a}}=\mathcal {G}_{v}(p_{a}),\ \tilde {a}=\mathcal {G}_{a}(a_{q}) \tag{8}\]
\[\mathcal{G}_{m}(x)=\sum_{i=1}^{E} g_{m}^{i} r_{m}^{i} \mathcal{E}_{m}^{i}(x) \tag{9}\]

In this setup, \(E_{m}^{i}(x)\) represents the output of the i-th expert for input x. The temporal visual features \(\tilde{v}_{p_{v}} \in \mathbb{R}^{D}\) and \(\tilde{v}_{p_{a}} \in \mathbb{R}^{D}\) are derived by applying the experts to modality-specific patch features \(p_{v}\) and \(p_{a}\), respectively. Similarly, the temporal audio feature \(\tilde{a} \in \mathbb{R}^{D}\) is obtained by applying experts to the question-aware audio feature \(a_{q}\). This arrangement allows the model to maintain temporal coherence, aligning with question-relevant segments and minimizing redundancy.

### 3.4. Question-Guided Reasoning and Prediction
The question-guided reasoning module combines audio and visual features from the temporal integration module, allowing the model to evaluate each input’s importance in relation to the question context. To ensure a balanced representation, we use averaged features as a residual connection, preventing over-reliance on any single input type. First, the final visual feature \(F_{v} \in \mathbb{R}^{D}\) is obtained as follows:
\[F_{v}=Avg(\tilde {v}_{p_{a}},\tilde {v}_{p_{v}})+CA(q_{s},[\tilde {v}_{p_{a}},\tilde {v}_{p_{v}}],[\tilde {v}_{p_{a}},\tilde {v}_{p_{v}}]) \tag{10}\]
where \([\cdot, \cdot]\) denotes concatenation. This process yields a question-aligned visual feature that balances information across both temporal visual representations. Next, the final audio-visual representation \(F_{v a} \in \mathbb{R}^{D}\) is obtained by fusing the temporal audio feature \(\tilde{a}\) with \(F_{v}\) as follows:
\[F_{v a}=Avg\left(\tilde{a}, F_{v}\right)+CA\left(q_{s},\left[\tilde{a}, F_{v}\right],\left[\tilde{a}, F_{v}\right]\right) \tag{11}\]

This step ensures that both audio and visual features contribute to the final representation in a question-aware manner. Finally, answer prediction is performed by applying a linear layer and a Softmax layer to \(F_{v a}\) yielding probabilities over C answer choices. The model is trained using cross-entropy loss: \(L_{q a}=-\sum_{c=1}^{C} y_{c} log P_{c}\), with the answer selected as the class with the highest probability.

---

## 4. Experiments
### 4.1. Datasets
Experiments are conducted on MUSIC-AVQA [16], MUSIC-AVQA-R [28], and MUSIC-AVQA-v2.0 [26] datasets.
- **MUSIC-AVQA**: Audio-visual reasoning benchmark for 22 musical instruments, covering audio-only, visual-only, and audio-visual questions with existential, location, and temporal reasoning types.
- **MUSIC-AVQA-R**: Focuses on rare and out-of-distribution samples to evaluate model robustness.
- **MUSIC-AVQA-v2.0**: Enhances diversity in ensemble scenarios and multi-instrument cases to address dataset bias.

Dataset statistics are shown in Table 1.

**Table 1. Statistics of QA pairs for MUSIC-AVQA, MUSIC-AVQA-R, and MUSIC-AVQA-v2.0**
| Dataset | #Videos | Train | Val | Test |
|---------|---------|-------|-----|------|
| MUSIC-AVQA [16] | 9288 | 31904 | 4568 | 9129 |
| MUSIC-AVQA-R [28] | 9288 | - | - | 211572 |
| MUSIC-AVQA-v2.0 [26] | 10492 | 37408 | 5346 | 10819 |

### 4.2. Implementation Details
Videos are sampled at 1 fps. Audio features are extracted using VGGish [11]. Visual and question features are processed using CLIP-ViT-L/14 [30]. Visual features undergo token reduction via ToMe [2]. All features are linearly transformed to 512 dimensions for consistency. The number of experts is set to 7. All attention modules use 8 heads with dropout probability 0.1. Adam optimizer is used with initial learning rate 1e-4, decayed by 0.1 every 8 epochs. The model is trained for 15 epochs with batch size 32 on a single NVIDIA RTX A6000.

### 4.3. Quantitative Results and Analysis
We compare QA-TIGER with existing AVQA methods on audio-only (A-QA), visual-only (V-QA), and audio-visual (AV-QA) tasks, evaluated by question type and overall mean. QA-TIGER is trained on MUSIC-AVQA [16] training set, validated on validation set, and tested on both MUSIC-AVQA [16] and MUSIC-AVQA-R [28]. For MUSIC-AVQA-v2.0 [26], we train on both biased and balanced training sets and test accordingly.

- **MUSIC-AVQA**: QA-TIGER achieves overall accuracy 77.62%, outperforming previous state-of-the-art TSPM [19] (76.79%), with strong performance in complex reasoning tasks: AV-Counting 78.58%, AV-Local 72.50% (Table 2).
- **MUSIC-AVQA-R**: Without explicit bias handling, QA-TIGER achieves 67.99% overall accuracy with balanced performance across all question types, demonstrating strong temporal modeling and question-aware feature extraction (Table 3).
- **MUSIC-AVQA-v2.0**: Regardless of training set type, QA-TIGER outperforms existing models [16,24,28] on biased test set (Table 4a). On balanced test set, QA-TIGER trained on balanced dataset leads in audio-only (79.90%) and visual-only (86.95%) tasks, achieving 76.43% overall accuracy, surpassing LAST-Att. LAST-Att additionally uses Audio Spectrogram Transformer [9] audio encoder yet performs worse on audio-only tasks, validating QA-TIGER's generalization robustness.
- **Inference Speed**: Under identical conditions, TSPM takes 1.767s while QA-TIGER takes 1.737s, maintaining comparable efficiency. QA-TIGER processes full temporal information without extra overhead, demonstrating its efficiency in handling temporal dynamics.

**Table 2. Experimental results (%) on MUSIC-AVQA test set (Top 2 highlighted)**
| Method | Audio-only QA | | | Visual-only QA | | | Audio-visual QA | | | | | | Mean |
|--------|---------------|---|---|----------------|---|---|-----------------|---|---|---|---|---|---|------|
| | Count | Compare | Mean | Count | Local | Mean | Exist | Count | Local | Compare | Temporal | Mean | |
| FCNLSTM [10] | 70.45 | 66.22 | 68.88 | 63.89 | 46.74 | 55.21 | 82.01 | 59.34 | 46.28 | 62.15 | 47.33 | 60.06 | 60.34 |
| BiLSTM [38] | 70.35 | 47.92 | 62.05 | 64.64 | 64.33 | 64.48 | 78.39 | 56.91 | 45.85 | 53.09 | 49.76 | 57.10 | 59.92 |
| HCAttn [27] | 70.25 | 54.91 | 64.57 | 64.05 | 66.37 | 65.22 | 79.10 | 59.97 | 49.51 | 55.25 | 56.43 | 60.19 | 62.30 |
| MCAN [43] | 77.50 | 55.24 | 69.25 | 71.56 | 70.93 | 71.24 | 80.40 | 64.91 | 54.48 | 57.22 | 47.57 | 61.58 | 65.49 |
| PSAC [22] | 75.64 | 66.06 | 72.09 | 68.64 | 69.79 | 69.22 | 77.59 | 63.42 | 55.02 | 61.17 | 59.47 | 63.52 | 66.54 |
| HME [1] | 74.76 | 63.56 | 70.61 | 67.97 | 69.46 | 68.76 | 80.30 | 63.19 | 53.18 | 62.69 | 59.83 | 64.05 | 66.45 |
| HCRN [15] | 68.59 | 50.92 | 62.05 | 64.39 | 61.81 | 63.08 | 54.47 | 53.38 | 41.53 | 52.11 | 47.69 | 50.26 | 55.73 |
| AVSD [31] | 72.41 | 61.90 | 68.52 | 67.39 | 74.19 | 70.83 | 81.61 | 63.89 | 58.79 | 61.52 | 61.41 | 65.49 | 67.44 |
| Pano-AVQA [46] | 74.36 | 64.56 | 70.73 | 69.39 | 75.65 | 72.56 | 81.21 | 64.91 | 59.33 | 64.22 | 63.23 | 66.64 | 68.93 |
| ST-AVQA [16] | 78.18 | 67.05 | 74.06 | 71.56 | 76.38 | 74.00 | 81.81 | 70.80 | 64.51 | 66.01 | 63.23 | 69.54 | 71.52 |
| COCA [14] | 79.35 | 67.68 | 75.42 | 75.10 | 75.43 | 75.23 | 83.50 | 66.63 | 69.72 | 64.12 | 65.57 | 69.96 | 72.33 |
| PSTP-Net [17] | 73.97 | 65.59 | 70.91 | 77.15 | 77.36 | 77.26 | 76.18 | 72.23 | 71.80 | 71.79 | 69.00 | 72.57 | 73.52 |
| LAVISH [24] | 82.09 | 65.56 | 75.97 | 78.98 | 81.43 | 80.22 | 81.71 | 75.51 | 66.13 | 63.77 | 67.96 | 71.26 | 74.46 |
| APL [23] | 82.40 | 70.71 | 78.09 | 76.52 | 82.74 | 79.69 | 82.99 | 73.29 | 66.68 | 64.76 | 65.95 | 70.96 | 74.53 |
| TSPM [19] | 84.07 | 64.65 | 76.91 | 82.29 | 84.90 | 83.61 | 82.19 | 76.21 | 71.85 | 65.76 | 71.17 | 73.51 | 76.79 |
| **QA-TIGER** | **84.86** | **67.85** | **78.58** | **83.96** | **86.29** | **85.14** | **83.10** | **78.58** | **72.50** | 63.94 | 69.59 | **73.74** | **77.62** |

**Table 4. Experimental results (%) on MUSIC-AVQA-v2.0**
(a) Biased test set
| Test | Train | Method | Audio-only | Visual-only | AV | Mean |
|------|-------|--------|------------|-------------|----|------|
| Biased | Biased | ST-AVQA [16] | 76.86 | 77.70 | 69.59 | 73.07 |
| | | LAVISH [24] | 76.73 | 80.96 | 70.80 | 74.59 |
| | | **QA-TIGER** | **79.13** | **84.83** | **72.37** | **76.93** |
| | Balanced | ST-AVQA [16] | 76.18 | 77.20 | 67.96 | 71.92 |
| | | LAVISH [24] | 75.56 | 80.83 | 69.27 | 73.51 |
| | | LAST [26] | 77.10 | 82.99 | 70.86 | 75.24 |
| | | LAST-Att [26] | 77.29 | 83.47 | 71.05 | 75.45 |
| | | **QA-TIGER** | 77.07 | **85.93** | 71.20 | **76.57** |

(b) Balanced test set
| Test | Train | Method | Audio-only | Visual-only | AV | Mean |
|------|-------|--------|------------|-------------|----|------|
| Balanced | Biased | ST-AVQA [16] | 73.34 | 76.82 | 64.51 | 69.40 |
| | | LAVISH [24] | 73.14 | 79.70 | 65.01 | 70.39 |
| | | **QA-TIGER** | **77.57** | **84.84** | **67.43** | **73.91** |
| | Balanced | ST-AVQA [16] | 75.50 | 77.67 | 66.32 | 71.02 |
| | | LAVISH [24] | 76.15 | 81.32 | 68.28 | 73.18 |
| | | LAST [26] | 78.08 | 83.29 | 69.72 | 74.85 |
| | | LAST-Att [26] | 78.56 | 84.07 | 70.30 | 75.44 |
| | | **QA-TIGER** | **79.90** | **86.95** | 70.22 | **76.43** |

### 4.4. Qualitative Results of Temporal Gaussian
To verify that QA-TIGER accurately identifies question-relevant temporal segments, we conduct qualitative analysis (Figure 3). Audio Gaussians are more prominent for audio-only questions (Figure 3a), while visual Gaussians dominate visual-only questions (Figure 3b). For audio-visual questions, both modalities show similar Gaussian distributions (Figure 3c), demonstrating adaptive focus based on question type.

### 4.5. Question-Aware Fusion Visualization
To validate the question-aware fusion module, we perform word-level visualization. For the question "Is there the sound of saxophone and piano?", visual attention first focuses on "piano" with weak visual cues, then shifts to "saxophone" with strong features. Audio attention consistently focuses on "piano" to compensate for weak visual cues, while "saxophone" is mainly handled by vision. Results show the module dynamically adapts to different questions, emphasizing question-relevant elements across modalities.

---

## 5. In-Depth Analysis
### 5.1. Ablation Study
We validate module effectiveness on MUSIC-AVQA (Table 5). Baseline with uniform sampling achieves reasonable accuracy. Adding Gaussian experts improves performance via enhanced temporal modeling. Question-aware fusion alone also brings significant gains. Combining both modules achieves optimal performance, proving the synergistic benefit of early question context integration.

**Table 5. Ablation study of the framework**
| Question-Aware Fusion | Gaussian Experts | Audio-only | Visual-only | AV | Mean |
|-----------------------|------------------|------------|-------------|----|------|
| | | 75.05 | 81.79 | 71.82 | 75.04 |
| ✓ | | 77.59 | 84.56 | 72.37 | 76.53 |
| | ✓ | 76.35 | 82.74 | 72.78 | 76.05 |
| ✓ | ✓ | 78.58 | 85.14 | 73.74 | 77.62 |

### 5.2. Frame Sampling
After applying question-aware fusion, we compare traditional sampling strategies with Gaussian modeling (Figure 5). Uniform sampling performs poorly due to inability to focus on question-relevant frames. Top-K sampling improves performance but lacks full temporal context. Weighted Gaussian with disjoint center constraints reduces redundancy and improves accuracy. Gaussian experts with MoE framework achieve highest accuracy by dynamically assigning specialized experts.

### 5.3. Number of Experts
We analyze the impact of expert count. 7 experts are selected as accuracy increases with expert number. Even with minimum experts, accuracy surpasses TSPM [19] (76.79%), validating QA-TIGER's superiority (Figure 6).

---

## 6. Conclusion
This paper presents QA-TIGER, addressing limitations of traditional methods in modeling complex temporal dynamics and integrating question-relevant features. By employing multi-Gaussian modeling in an MoE framework, QA-TIGER adaptively captures fine-grained temporal dependencies while reducing redundancy via well-positioned Gaussian centers. We also explicitly incorporate question context early in encoding, ensuring progressive refinement throughout processing. Extensive experiments demonstrate state-of-the-art performance across multiple datasets. Future work will explore adaptive expert selection for different question types to further improve generalization.

---

## Acknowledgment
This work was partly supported by the National Research Foundation of Korea (NRF) and the Ministry of Science and ICT (MSIT), Digital-related Global Research Support Project (RS2023-00211348, RS-2024-004253535) supervised by the Institute for Information & Communications Technology Planning & Evaluation (IITP).

---

## References
[1] Chenyou Fan, Xiaofan Zhang, Shu Zhang, Wensheng Wang, Chi Zhang, Heng Huang. Heterogeneous Memory Enhanced Multimodal Attention Model for Video Question Answering. CVPR, 1999-2000, 2019.
[2] Daniel Bolya, Cheng-Yang Fu, Xiaoliang Dai, Peizhang Zhang, Christoph Feichtenhofer, Judy Hoffman. Token Merging: Your ViT But Faster. ICLR, 2023.
[3] Sihan Chen, Xingjian He, Longteng Guo, Xinxin Zhu, Weining Wang, Jinhui Tang, Jing Liu. Valor: Vision-Audio-Language Omni-Perception Pretraining Model and Dataset. arXiv preprint arXiv:2304.08348, 2023.
[4] Zailong Chen, Lei Wang, Peng Wang, Peng Gao. Question-Aware Global-Local Video Understanding Network for Audio-Visual Question Answering. IEEE TCSVT, 2023.
[5] Haoyi Duan, Yan Xia, Zhou Mingze, Li Tang, Jieming Zhu, Zhou Zhao. Cross-Modal Prompt: Adapt Large Pretrained Models for Audio-Visual Downstream Tasks. NeurIPS, 2024.
[6] Xiang Fang, Daizong Liu, Pan Zhou, Guoshun Nan. Grounding Before Seeing: An Efficient Pipeline for Temporal Sentence Grounding in Compressed Videos. CVPR, 2448-2460, 2023.
[7] Roy Ganz, Yair Kittenplon, Aviad Aberdam, Elad Ben Avraham, Oren Nuriel, Shai Mazor, Ron Litman. Question-Aware Vision Transformers for Multimodal Reasoning. CVPR, 2024.
[8] Jort F. Gemmeke, Daniel P. W. Ellis, Dylan Freedman, Aren Jansen, Wade Lawrence, R. Channing Moore, Manoj Plakal, Marvin Ritter. Audio Set: An Ontology and Human-Labeled Dataset for Audio Events. ICASSP, 2017.
[9] Yuan Gong, Yu-An Chung, James Glass. AST: Audio Spectrogram Transformer. INTERSPEECH, 571-575, 2021.
[10] Justin Johnson, Haytham M. Fayek. Temporal Reasoning for Audio Question Answering. IEEE TASLP, 28:2283-2294, 2020.
[11] Shawn Hershey, Sourish Chaudhuri, Daniel P. W. Ellis, Jort F. Gemmeke, Aren Jansen, Channing Moore, Manoj Plakal, Devi Platt, Rif A. Saurous, Bryan Seybold, Malcolm Slaney, Ron Weiss, Kevin Wilson. CNN Architectures for Large-Scale Audio Classification. ICASSP, 131-135, 2017.
[12] Ziru Huang, Jia Li, Wenjie Zhao, Yunhui Guo, Yapeng Tian. AV-Mamba: Cross-Modal Selective State Space Model for Audio-Visual Question Answering. CVPRW, 2024.
[13] Yuanyuan Jiang, Jianqin Yin. CLIP-Based TASS: Target-Aware Single-Stream Network for Audio-Visual Question Answering. arXiv preprint arXiv:2405.07451, 2024.
[14] Mingrui Lao, Nan Pu, Yu Liu, Kai He, Erwin M. Bakker, Michael S. Lew. COCA: Collaborative Causal Regularization for Audio-Visual Question Answering. AAAI, 12995-13003, 2023.
[15] Thao Minh Le, Vuong Le, Svetha Venkatesh, Truyen Tran. Hierarchical Conditional Relation Networks for Video Question Answering. CVPR, 9972-9981, 2020.
[16] Guangyao Li, Yake Wei, Yapeng Tian, Chenliang Xu, Ji-Rong Wen, Di Hu. Learning to Answer Questions in Dynamic Audio-Visual Scenarios. CVPR, 19108-19118, 2022.
[17] Guangyao Li, Wenxuan Hou, Di Hu. Progressive Spatio-Temporal Perception for Audio-Visual Question Answering. ACM MM, 7808-7816, 2023.
[18] Guangyao Li, Yixin Xu, Di Hu. Multi-Scale Attention for Audio Question Answering. arXiv preprint arXiv:2305.17999, 2023.
[19] Guangyao Li, Henghui Du, Di Hu. Boosting Audio-Visual Question Answering via Key Semantic-Aware Cues. ACM MM, 2024.
[20] Kun Li, Dan Guo, Meng Wang. Proposal-Free Video Grounding with Context Pyramid Networks. AAAI, 1902-1910, 2021.
[21] Linjie Li, Zhe Gan, Yu Cheng, Jingjing Liu. Relation-Aware Graph Attention Network for Visual Question Answering. ICCV, 10313-10322, 2019.
[22] Xiangpeng Li, Jingkuan Song, Lianli Gao, Xianglong Liu, Wenbing Huang, Xiangnan He, Chuang Gan. Beyond RNNs: Positional Self-Attention with Co-Attention for Video Question Answering. AAAI, 8658-8665, 2019.
[23] Zhangbin Li, Dan Guo, Jinxing Zhou, Jing Zhang, Meng Wang. Object-Aware Adaptive-Positivity Learning for Audio-Visual Question Answering. AAAI, 2024.
[24] Yan-Bo Lin, Yi-Lin Sung, Jie Lei, Mohit Bansal, Gedas Bertasius. Vision Transformers are Parameter-Efficient Audio-Visual Learners. CVPR, 2299-2309, 2023.
[25] Hongcheng Liu, Pingjie Wang, Yu Wang, Yanfeng Wang. M2K-VDG: Model Adaptive Multimodal Knowledge Anchor Enhanced Video Dialogue Generation. arXiv preprint arXiv:2402.11875, 2024.
[26] Xiulong Liu, Zhikang Dong, Peng Zhang. Addressing Data Bias in MUSIC-AVQA: Constructing a Balanced Dataset for Unbiased Question Answering. WACV, 4478-4487, 2024.
[27] Jiasen Lu, Jianwei Yang, Dhruv Batra, Devi Parikh. Hierarchical Question-Image Co-Attention for Visual Question Answering. NeurIPS, 2024.
[28] Jie Ma, Min Hu, Pinghui Wang, Wangchun Sun, Lingyun Song, Hongbin Pei, Jun Liu, Youtian Du. Watch, Listen and Answer: Overcoming Bias in Audio-Visual Question Answering. NeurIPS, 2024.
[29] Jonghwan Mun, Minsu Cho, Bohyung Han. Local-Global Video-Text Interactions for Temporal Grounding. CVPR, 10810-10819, 2020.
[30] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, Ilya Sutskever. Learning Transferable Visual Models From Natural Language Supervision. ICML, 8748-8765, 2021.
[31] Idan Schwartz, Alexander G. Schwing, Tamir Hazan. A Simple Baseline for Audio-Visual Scene-Aware Dialog. CVPR, 12548-12558, 2019.
[32] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, Jeff Dean. Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer. ICLR, 2017.
[33] Enxin Song, Wenhao Chai, Tian Ye, Jenq-Neng Hwang, Xi Li, Gaoang Wang. MovieChat+: Question-Aware Sparse Memory for Long Video Question Answering. arXiv preprint arXiv:2404.17176, 2024.
[34] Grant Van Horn, Rui Qian, Kimberly Wilber, Hartwig Adam, Oisin Mac Aodha, Serge Belongie. Exploring Fine-Grained Audio-Visual Classification with the SSW60 Dataset. ECCV, 271-282, 2022.
[35] Hao Wang, Zheng-Jun Zha, Liang Li, Dong Liu, Jiebo Luo. Structured Multi-Level Interaction Network for Video Moment Retrieval with Language Query. CVPR, 7026-7035, 2021.
[36] Jingwen Wang, Lin Ma, Wenhao Jiang. Temporal Sentence Grounding in Videos with Contextual Boundary-Aware Prediction. AAAI, 12168-12175, 2020.
[37] Kai Wang, Yapeng Tian, Dimitrios Hatzinakos. Empowering Pretrained Vision Transformers as Efficient Audio-Visual Learners via Cross-Modal Adapters. CVPR, 1837-1846, 2024.
[38] Zihan Wang, Bo Yang. Attention-Based Bidirectional Long Short-Term Memory Networks for Relation Classification. ACL, 207-212, 2016.
[39] Junbin Xiao, Angela Yao, Yicong Li, Tat-Seng Chua. Can I Trust Your Answer? Visually Grounded Video Question Answering. CVPR, 13204-13214, 2024.
[40] Pinci Yang, Xin Wang, Xuguang Duan, Hong Chen, Runze Hou, Cong Jin, Wenwu Zhu. AVQA: Audio-Visual Question Answering Dataset for Videos. ACM MM, 3480-3491, 2022.
[41] Tianhao Yang, Zheng-Jun Zha, Hongtao Xie, Meng Wang, Hanwang Zhang. Question-Aware Tube-Switch Network for Video Question Answering. ACM MM, 1184-1192, 2019.
[42] Qilang Ye, Zitong Yu, Xin Liu. Diversified Question Answering via Key Audio-Visual Cue Text. arXiv preprint arXiv:2403.06679, 2024.
[43] Zhou Yu, Jun Yu, Yuhao Cui, Dacheng Tao, Qi Tian. Deep Modular Co-Attention Networks for Visual Question Answering. CVPR, 6281-6290, 2019.
[44] Yitian Yuan, Lin Ma, Jingwen Wang, Wei Liu, Wenwu Zhu. Semantic Conditioned Dynamic Modulation for Temporal Sentence Grounding in Videos. NeurIPS, 2019.
[45] Yitian Yuan, Tao Mei, Wenwu Zhu. To Find Where You Talk: Temporal Sentence Localization in Video with Attention Based Location Regression. AAAI, 9159-9165, 2019.
[46] Heeseung Yun, Youngjae Yu, Wonsuk Yang, Kangil Lee, Gunhee Kim. Pano-AVQA: Grounded Audio-Visual Question Answering on 360° Videos. ICCV, 2031-2041, 2021.
[47] Songyang Zhang, Houwen Peng, Jianlong Fu, Jiebo Luo. Learning 2D Temporal Adjacent Networks for Moment Localization with Natural Language. AAAI, 12870-12870, 2020.
