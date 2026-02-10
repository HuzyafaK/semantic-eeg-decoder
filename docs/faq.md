# FAQ — semantic-eeg-decoder (ChiSCO-CLIP)

This FAQ addresses common technical, research, and collaboration questions about the project. It is written to be clear to technical reviewers, investors, and potential collaborators while protecting proprietary details.

---

## Q: What does this project actually do?

A: We map non-invasive imagined-speech EEG into a shared semantic embedding space aligned with language. The primary validated capability is **retrieval** (Top‑K retrieval of semantically matching sentences). Language generation from EEG is explored as a downstream, adapter-driven step and is still research-in-progress.

---

## Q: Does this work on new people (zero-shot)?

A: In preliminary calibration experiments we measured that short, targeted adaptation markedly improves retrieval performance: most users achieved significant Top‑K retrieval improvement within minutes to tens of minutes of calibration. Zero-shot performance (no calibration) on completely unseen subjects is limited. We can provide calibration curves and logs under NDA for due diligence.

---

## Q: Which dataset did you use?

A: Our experiments use the publicly available ChiSCO (Chinese Imagined Speech Corpus). We use neural channels only (122 channels after excluding non-neural channels) and fixed-length epochs (1651 timesteps in our pipeline).

---

## Q: Are you publishing training code or model weights?

A: No. For IP and privacy reasons, the core training code, model checkpoints, and raw EEG data are not published. The repository contains demo assets (precomputed, non-reversible embeddings), architecture diagrams, and interface stubs.

---

## Q: Why a retrieval-first approach instead of end-to-end generation?

A: Retrieval is measurable, interpretable, and robust for low‑SNR signals like EEG. It proves semantic alignment of embeddings; generation is a downstream realization problem that becomes feasible once the semantic manifold is stable. This lowers hallucination risk and makes evaluation cleaner.

---

## Q: What metrics do you use to evaluate performance?

A: Primary metrics are Top‑K retrieval accuracy, Mean Reciprocal Rank (MRR), median rank, and separation gap (mean correct similarity − mean incorrect similarity). We monitor embedding diversity and use permutation baselines to validate non-random learning. Demo artifacts show qualitative Top‑K examples; exact numeric tables are reserved for private discussions.

---

## Q: Is this a clinical device? Can I rely on this for medical decisions?

A: No. This is a research prototype and not a certified medical device. It should not be used for clinical decision-making or diagnosis. Any clinical deployment would require rigorous trials, regulatory approval, and domain-specific safety engineering.

---

## Q: What are the privacy and ethical considerations?

A: EEG data are sensitive. We do not publish raw EEG or identifying metadata. Any collaboration involving raw data will follow institutional privacy policies and data agreements (e.g., IRB / DUA / NDA as applicable). Generation results can hallucinate and must be presented with uncertainty when shown to non-technical audiences.

---

## Q: How can I reproduce the demo locally?

A: The public repo contains precomputed embeddings and demo instructions showing how the UI reproduces retrieval and generation visuals. Raw EEG, training code, and checkpoints are not included. If you are a validated research collaborator or investor, reach out via contact to request access under an appropriate agreement.

---

## Q: Can I get access to the models or calibration data?

A: We share additional evaluation artifacts, calibration curves, and controlled model access under NDA or research collaboration agreements. Contact `info@excelleve.com` with affiliation and the type of access requested (demo samples, logs, calibration curves, partnership discussion).

---

## Q: What hardware / compute is required to run the demo?

A: Offline inference in the demo uses precomputed embeddings and lightweight retrieval logic that can run on a laptop. The proprietary encoder training required GPUs; exact specs depend on hyperparameters and dataset scale and are not published in this repository.

---

## Q: What does “embedding cosine” indicate in the demo UI?

A: Cosine similarity is used as the primary similarity metric between L2-normalized EEG embeddings and text prototypes. Higher cosine indicates stronger semantic alignment. Cosines are relative and help rank candidates; absolute thresholds depend on the gallery and model.

---

## Q: What failure modes should we expect?

A: Common failure modes include mode-collapse (low embedding diversity), subject overfitting (weak cross-subject generalization), artifact leakage (motion/EMG correlates), and generation hallucination. The methodology includes diagnostics and mitigations for each.

---

## Q: Will you open-source the full model later?

A: We may share more under a staged plan (collaboration agreements, paper supplements, or an API) — but core training code and model weights are currently proprietary to preserve IP and patient privacy.

---

## Q: How do we cite your work or the dataset?

A: Use the CITATION.bib in the repo for dataset and project references. For the ChiSCO dataset, cite Zhang et al., Scientific Data (2024).

---

## Q: Who should I contact for partnerships or investor conversations?

A: Email: **[info@excelleve.com](mailto:info@excelleve.com)**. Please include affiliation and a brief note about whether you request (a) demo materials, (b) calibration logs, (c) partnership, or (d) commercial/licensing inquiries.
