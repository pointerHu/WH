September 25, 2026

The Editors  
*Information Fusion*

Dear Editor,

We would like to submit our manuscript entitled **“SGTG: Semantic-Guided Gaussian Temporal Grounding for Audio-Visual Generalized Zero-Shot Learning”** for consideration as a Research Article in **Information Fusion**.

Audio-visual generalized zero-shot learning aims to recognize both seen and unseen classes by combining audio, visual, and class-semantic information. Existing methods may miss brief discriminative events, dilute useful evidence through global temporal aggregation, and remain vulnerable to ambiguous class embeddings, weak audio-visual correspondence, and modality-specific noise. To address these challenges, we propose SGTG, which uses class semantics as active conditioning signals for temporal evidence selection, modality interaction, and adaptive fusion throughout the recognition pipeline.

**Key Contributions**

**Discriminative Semantic Prototype Optimization (DSPO).** Fine-grained visual and auditory descriptions are encoded using CLIP and CLAP, and the resulting class prototypes are jointly optimized for class separability and semantic preservation. This provides discriminative and transferable semantic references for unseen-class recognition.

**Class-Conditioned Gaussian Temporal Aggregation (CGTA).** Candidate-class semantics condition the audio and visual sequences. Independent Gaussian experts with adaptive routing continuously localize and aggregate class-relevant temporal evidence, reducing the influence of irrelevant segments.

**Decoupled Modality Interaction and Gated Fusion (DMIF).** Separate intra-modal and inter-modal branches model complementary relationships, while a sample- and class-conditioned gate combines their representations with direct temporal evidence to suppress modality interference and preserve useful information.

**Comprehensive evaluation.** Experiments and ablation studies on three established audio-visual generalized zero-shot learning benchmarks evaluate the main comparison, temporal aggregation strategies, expert counts, prototype objectives, interaction and gating, text encoders, and fine-grained descriptions.

**Relevance to Information Fusion**

SGTG is directly aligned with the scope of *Information Fusion* because it studies how semantic, audio, and visual evidence should be selected, organized, and combined when audio-visual correspondence is weak, discriminative evidence is temporally sparse, and target classes are unseen. Its central claim is that class semantics should serve as active control signals for both temporal evidence selection and multimodal fusion, rather than only as targets for final matching.
The manuscript compares SGTG with five conventional zero-shot methods and 14 audio-visual generalized zero-shot methods. Five representative comparison references are: (1) Mercea et al., AVCA, CVPR 2022, DOI 10.1109/CVPR52688.2022.01030; (2) Mercea et al., TCaF, ECCV 2022, DOI 10.1007/978-3-031-20044-1_28; (3) Kurzendörfer et al., ClipClap-GZSL, CVPRW 2024, DOI 10.1109/CVPRW63382.2024.00269; (4) Li et al., MDST++, *IEEE Transactions on Circuits and Systems for Video Technology*, 2025, DOI 10.1109/TCSVT.2025.3574499; and (5) Ma et al., SGPAN, ICASSP 2026, DOI 10.1109/ICASSP55912.2026.11463644.

The experiments use the class-based variants of VGGSound-GZSL, UCF-GZSL, and ActivityNet-GZSL, derived from VGGSound, UCF101, and ActivityNet and containing 276, 51, and 200 classes, respectively. We report mean class accuracy for seen classes (S), mean class accuracy for unseen classes (U), their harmonic mean (HM), and conventional zero-shot mean class accuracy (ZSL); HM is the principal measure of balanced seen/unseen recognition. SGTG achieves HM scores of 22.78%, 60.63%, and 31.49% on the three benchmarks, improving on the strongest HM baseline reported for each dataset by 7.05, 2.39, and 4.38 percentage points. Removing DSPO, CGTA, or DMIF reduces HM on all three benchmarks, and the additional ablations support the roles of semantic prototype optimization, class-conditioned temporal grounding, and adaptive fusion.

The closest methodological connections are EZ-AVGZL, QA-TIGER, and Semi-IIN. EZ-AVGZL motivates discriminative class-embedding optimization, whereas SGTG uses optimized prototypes to condition continuous temporal grounding and fusion. QA-TIGER develops question-conditioned Gaussian expert integration for audio-visual question answering, while SGTG adapts Gaussian integration to transferable candidate-class semantics for generalized zero-shot recognition. Semi-IIN separates intra-modal and inter-modal attention for sentiment analysis; SGTG applies this separation to temporally grounded evidence and additionally retains a direct temporal-evidence branch under dynamic gating.

No part of this work has been previously published. This manuscript is not an extension of a previously published conference or journal paper; the contributions described above are presented in this original submission.

Thank you for considering our manuscript. We would be pleased to provide any further information required for its evaluation.

Sincerely yours,

**Jing Yang**  
Corresponding author  
State Key Laboratory of Public Big Data, Guizhou University  
Guiyang 550025, China  
Email: jyang23@gzu.edu.cn
