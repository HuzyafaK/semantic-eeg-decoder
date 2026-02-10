# Methodology — ChiSCO-CLIP (semantic-eeg-decoder)

> High-level, non-proprietary description of data handling, model training strategy, evaluation protocols, and key engineering safeguards. This document intentionally avoids exposing proprietary model source code and checkpoint details.

---

## 1. Goal and scope

This document describes the experimental methodology used to learn a subject-invariant semantic embedding from non-invasive imagined-speech EEG and to evaluate retrieval-based decoding. It focuses on process and design choices rather than implementation details.

---

## 2. Dataset & splits

* **Primary dataset:** ChiSCO (public). Trials contain 128-channel recordings; we use 122 neural channels (reference/ground/marker channels excluded). Each trial is a fixed-length epoch (1651 timesteps in our pipeline).
* **Core splits:**

  * **Training pool:** mixed-subject training (e.g., S1+S2 or S1+S2+S3 depending on experiment). Mixing subjects in training is essential to promote subject-invariant features.
  * **Validation:** held-out trials from the same subjects (for checkpoint selection).
  * **Test (seen-subject):** held-out trials drawn from subjects used in training.
  * **Unseen-subject / zero-shot test:** separate subject(s) held entirely out of training for domain-shift evaluation.
* **Golden demo set:** a curated set of 5–10 trials with precomputed embeddings used for reproducible demos (no raw EEG included in the public repo).

---

## 3. Preprocessing pipeline

Principles: make preprocessing deterministic, minimal, and consistent across train/val/test.

Typical steps (applied consistently):

1. **Channel selection:** drop non-neural channels (reference, timestamp markers). Resulting shape: `122 × T`.
2. **Band-pass / notch filtering:** standard EEG filters to remove mains noise and drifts (pipeline choice depends on acquisition hardware).
3. **Per-channel normalization:** compute mean/std across training set (or streaming estimates) and apply channel-wise normalization. Save normalization params for inference.
4. **Epoching & trimming:** align and trim trials to fixed length (pad or truncate consistently).
5. **Artifact handling:** conservative heuristics (e.g., channel-level amplitude threshold, optional ICA for explicit artifact removal). Avoid subject-specific tweaked thresholds.

Notes:

* Avoid heavy augmentations that change semantic content (temporal jittering, channel shuffling are used cautiously in ablations only).
* Preprocessing code and raw data are not public; demo uses precomputed, non-reversible embeddings.

---

## 4. Model components (conceptual)

* **EEG encoder (proprietary):** transforms `122 × T` → semantic embedding (e.g., 512-D). Implemented as a convolutional front-end + temporal transformer block + pooling + projection.
* **Text encoder:** frozen, pre-trained language encoder (BERT-style) used to compute text prototypes; a projection layer maps text vectors to the same embedding dimension as EEG.
* **Prototype bank:** a saved matrix of normalized text prototype vectors for retrieval.
* **SemanticPrefix adapter (optional):** small MLP that maps EEG embeddings to prefix embeddings for a frozen LLM for generation.

All training code for these components is private.

---

## 5. Training objectives (high-level)

We combine complementary objectives to learn both global structure (which prototype) and instance-level specificity.

1. **Prototype contrastive loss (primary):**

   * For a batch of B paired (EEG_i, text_i), compute similarity logits between EEG embeddings and text prototypes. Use a cross-entropy / InfoNCE-style objective that pulls correct pairs together and pushes incorrect pairs apart. We compute bidirectional losses (EEG→Text and Text→EEG) and average them.

2. **Instance-level semantic loss (auxiliary):**

   * After optional generation or projection through the LLM adapter, compute cosine-based or MSE loss between EEG embedding and generated-text semantic projection to reduce instance-level divergence.

3. **Optional generation CE loss (phase 2):**

   * In a second phase, train the semantic-prefix adapter by minimizing LLM cross-entropy for teacher-forced generation while keeping most of the LLM frozen. Adapter training uses a very low learning rate for the encoder if it is fine-tuned.

**Loss weighting and practical notes:** balance contrastive vs generation losses empirically; prototype loss often dominates initially so tune weights conservatively. Use a small learnable temperature (logit_scale) and clamp it during training to prevent InfoNCE collapse.

---

## 6. Training regimen & engineering safeguards

High-level schedule (conceptual):

1. **Phase A — Contrastive alignment:** train encoder to align EEG ↔ text prototypes until retrieval metrics converge on validation. Freeze LLM and adapter.
2. **Phase B — Adapter + generation (optional):** train adapter to map EEG embeddings to LLM prefix tokens; optionally allow very low-LR encoder updates.

Engineering safeguards:

* **AMP (mixed precision)** & gradient accumulation for stable GPU usage.
* **Low learning rate for encoder** vs adapter/linear layers. Encoder updates if used must be small to preserve geometry.
* **Prototype caching** and deterministic ordering to ensure consistent optimization targets across epochs.
* **Clamped logit scale:** prevent temperature runaway in contrastive loss.
* **Composite checkpointing:** track retrieval@K and semantic cosine; allow fallback when one metric temporarily degrades.

---

## 7. Evaluation protocol

Primary evaluation is retrieval on a 200-way (or analogous) gallery unless otherwise noted.

Metrics:

* **Top-K retrieval accuracy (K=1,5,10)** — primary metric.
* **Mean Reciprocal Rank (MRR)** — captures ranking confidence.
* **Median rank** — robust central tendency.
* **Separation gap** — mean(sim_correct) − mean(sim_incorrect) gives geometry signal.
* **Embedding std / diversity** — monitor for mode collapse.

Cross-subject evaluation:

* **Seen-subject test:** hold out trials from subjects used in training.
* **Unseen-subject (zero-shot) test:** hold out entire subject(s) to measure domain shift.
* **Calibration experiments:** measure performance as a function of small calibration data collected from a new user (minutes of data). These curves are measured internally and available on request.

Statistical rigor:

* Use permutation testing / shuffled baselines to validate non-random learning.
* Report variance across multiple random seeds and folds if publishing.

---

## 8. Ablations & diagnostics (recommended)

* **Pooling strategies:** mean pooling (baseline), attention pooling, and their effect on overfitting.
* **Prototype size:** evaluate gallery scale sensitivity.
* **Batch composition:** subject-mixed vs subject-homogeneous batches to gauge invariance gains.
* **Temperature clamping:** ablate clamp range to show stability effect.
* **Embedding diversity regularizers:** e.g., negative std penalty or contrastive margin variants.

Record confusion matrices for top-K retrieval to understand semantic neighbor errors.

---

## 9. Failure modes & mitigations

Common failures and remedies:

* **Mode collapse (low embedding std):** increase embedding dimension, add diversity loss, or force larger batch negatives.
* **Overfitting to subjects:** increase subject diversity, use subject-mixed batches, add domain adversarial regularization.
* **Artifact leakage:** strengthen artifact rejection, or add per-channel dropout augmentation.
* **LLM hallucination in generation:** strictly gate generation behind retrieval and use constrained decoding or retrieval-augmented prompts.

---

## 10. Reproducibility & sharing policy

Public repo contains:

* Demo assets (precomputed embeddings, screenshots, demo video)
* Interface stubs
* Architecture diagram and methodology docs (this file)

Private: model code, training scripts, checkpoints, raw EEG, and calibration curves are kept offline for IP and privacy reasons. These can be shared under NDA for collaboration or due diligence.

---

## 11. Ethics & safety

* Not a clinical device; do not deploy for medical decisions.
* Data privacy: raw EEG is sensitive; do not share identifiable raw signals.
* Be explicit about generation uncertainty when showing outputs to non-technical audiences.
