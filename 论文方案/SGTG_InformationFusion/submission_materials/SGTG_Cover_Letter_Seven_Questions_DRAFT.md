# Cover Letter — DRAFT; Question 7 requires author confirmation

SGTG: Semantic-Guided Gaussian Temporal Grounding for Audio-Visual Generalized Zero-Shot Learning

## 1. Comparison with the state of the art and five key references

Yes. Section 4.2 and Table 2 compare SGTG with representative conventional zero-shot and audio-visual generalized zero-shot methods, including recent baselines. The comparisons report all four evaluation metrics on the same three benchmark variants. Five key comparison references are listed below; these are comparison methods actually included in the manuscript, not additional experiments.

[1] O.-B. Mercea, L. Riesch, A. S. Koepke, and Z. Akata. Audio-Visual Generalised Zero-Shot Learning With Cross-Modal Attention and Language. CVPR, 2022, pp. 10553–10563. DOI: 10.1109/CVPR52688.2022.01030. [AVCA]

[2] O.-B. Mercea, T. Hummel, A. S. Koepke, and Z. Akata. Temporal and Cross-modal Attention for Audio-Visual Zero-Shot Learning. Computer Vision – ECCV 2022, pp. 488–505. DOI: 10.1007/978-3-031-20044-1_28. [TCaF]

[3] D. Kurzendörfer, O.-B. Mercea, A. S. Koepke, and Z. Akata. Audio-Visual Generalized Zero-Shot Learning using Pre-Trained Large Multi-Modal Models. CVPRW, 2024, pp. 2627–2638. DOI: 10.1109/CVPRW63382.2024.00269. [ClipClap-GZSL]

[4] W. Li, P. Wang, X. Wang, W. Zuo, X. Fan, and Y. Tian. Multi-Timescale Motion-Decoupled Spiking Transformer for Audio-Visual Zero-Shot Learning. IEEE Transactions on Circuits and Systems for Video Technology, 35(11), 2025, pp. 10772–10786. DOI: 10.1109/TCSVT.2025.3574499. [MDST++]

[5] S. Ma, W. Li, H. Tang, Y. Chai, J. Chu, and X. Wang. Semantic-Guided Pseudo-Feature Attention Network for Audio-Visual Zero-Shot Learning. ICASSP, 2026, pp. 12497–12501. DOI: 10.1109/ICASSP55912.2026.11463644. [SGPAN]

## 2. Common public datasets and the datasets used in this study

The benchmarks used in this area include VGGSound-GZSL, UCF-GZSL, and ActivityNet-GZSL. Our experiments use their class-based variants, denoted by the superscript cls in the manuscript, derived from VGGSound, UCF101, and ActivityNet, respectively. They contain 276, 51, and 200 classes. Following the two-stage protocol in Section 4.1, the final seen/unseen test-class counts are 207/69, 42/9, and 150/50. Table 1 specifies the training, validation, and test-class splits. These counts refer to the benchmark variants evaluated here, not the full parent datasets.

## 3. Standard validation measures and those used in this study

We use the established metrics adopted by the audio-visual generalized zero-shot baselines: mean class accuracy for seen classes (S), mean class accuracy for unseen classes (U), and their harmonic mean (HM). We also report conventional zero-shot mean class accuracy (ZSL), for which both the candidate labels and evaluated samples are restricted to unseen classes. HM is the principal measure of balanced seen/unseen recognition. Hyperparameters and the seen-class calibration coefficient are selected using validation data under the two-stage protocol described in Section 4.1.

## 4. Main claim and significance to the Information Fusion community

Our main claim is that class semantics can serve as active conditioning signals for temporal evidence selection and modality fusion, rather than only as targets for final matching. SGTG combines Discriminative Semantic Prototype Optimization (DSPO), Class-Conditioned Gaussian Temporal Aggregation (CGTA), and Decoupled Modality Interaction and Gated Fusion (DMIF). It selects class-relevant evidence independently along the audio and visual timelines, models intra-modal and inter-modal relationships separately, and adaptively combines these representations with direct temporal evidence. For the Information Fusion community, this connects evidence selection with conditional fusion under weak audio-visual correspondence, modality noise, and unseen-class transfer.

## 5. Evidence supporting the claim and its implications

Table 2 reports HM scores of 22.78%, 60.63%, and 31.49% on VGGSound-GZSL, UCF-GZSL, and ActivityNet-GZSL class-based variants, respectively. These exceed the strongest HM baseline reported for each dataset by 7.05, 2.39, and 4.38 percentage points. The corresponding unseen-class accuracies are 16.87%, 46.97%, and 23.61%. The component ablations in Table 3 show HM decreases when DSPO, CGTA, or DMIF is removed. Tables 4–9 further examine temporal aggregation, expert counts, prototype objectives, interaction and gating, text encoders, and descriptions. Together, these results support improved balance between seen- and unseen-class recognition among the compared methods; they do not imply that SGTG is best on every individual metric.

## 6. Closest related work and the relationship to this manuscript

The closest methodological connections are discussed explicitly in Sections 2 and 3. Mo and Morgado’s Audio-Visual Generalized Zero-Shot Learning the Easy Way (EZ-AVGZL; DOI: 10.1007/978-3-031-73209-6_22) motivates discriminative class embeddings, whereas SGTG couples optimized embeddings to continuous temporal grounding and fusion control. Kim et al.’s Question-Aware Gaussian Experts for Audio-Visual Question Answering (QA-TIGER; DOI: 10.1109/CVPR52734.2025.01277) provides question-conditioned Gaussian expert integration; SGTG adapts this idea to transferable candidate-class semantics for generalized zero-shot recognition. Lin et al.’s Semi-IIN (DOI: 10.1609/aaai.v39i2.32131) separates intra-modal and inter-modal attention for sentiment analysis; SGTG applies decoupled interaction to grounded evidence and retains a direct temporal-evidence branch. AVCA, TCaF, and ClipClap-GZSL are important task baselines. The contribution is the coordinated use of semantic conditioning across evidence selection and fusion, not a claim to have invented each underlying component independently.

## 7. Previous publication and substantive additions beyond prior work

[AUTHOR CONFIRMATION REQUIRED BEFORE SUBMISSION: Confirm whether any part of SGTG has been published previously and whether it extends or overlaps with KA-GZSL or another manuscript. If yes, identify the earlier work and explain the substantive new contributions. Also confirm the current submission status and approval of the final manuscript by all authors. The supplied source files do not establish these facts, so no assertion of prior non-publication, exclusive submission, or unanimous approval has been inserted.]

