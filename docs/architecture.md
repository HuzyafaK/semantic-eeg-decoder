# Architecture Overview

This document describes the high-level architecture of our EEG-to-Text system and the design decisions behind it. The goal is to enable a clear understanding of how raw EEG signals are transformed into semantically meaningful linguistic representations, while intentionally omitting proprietary implementation details.

---

## 1. System Goal

The system aims to decode imagined or internally formulated speech from EEG signals by learning a shared semantic space between neural activity and language. The current implementation focuses on **retrieval-based decoding**, with **generation** explored as an auxiliary and ongoing research direction.

---

## 2. Data Modality

* **EEG Channels**: 122 channels (derived from the original 128-channel setup; non-neural reference, marker, and timestamp channels are excluded)
* **Temporal Resolution**: Fixed-length time windows per trial (e.g., 1651 timesteps in the ChiSCO dataset)
* **Input Representation**: Preprocessed EEG tensors (band-pass filtered, normalized, and segmented)

---

## 3. High-Level Pipeline

```
EEG Signals
    ↓
Preprocessing & Normalization
    ↓
Neural Encoder (EEG Encoder)
    ↓
Latent Semantic Embedding Space
    ↓
[ A ] Retrieval Head  →  Top-K Text Candidates
[ B ] Generation Head →  Semantically Aligned Text (Research / In-Progress)
```

The system is intentionally modular, allowing independent experimentation with encoding, retrieval, and generation components.

---

## 4. EEG Encoder

The EEG encoder is responsible for transforming multichannel temporal EEG signals into a compact semantic embedding.

Key characteristics:

* Operates on **122 × T** EEG input tensors
* Captures both spatial (cross-channel) and temporal structure
* Produces a fixed-dimensional embedding per trial
* Trained to maximize semantic alignment with corresponding text representations

The encoder is the core intellectual contribution of the system and is therefore not released in full detail.

---

## 5. Semantic Alignment Objective

The model is trained using a contrastive or similarity-based objective that aligns EEG embeddings with text embeddings derived from a pretrained language model.

Properties:

* Encourages semantically similar thoughts to cluster in embedding space
* Enables cross-subject generalization when trained on multiple subjects
* Supports retrieval without explicit language generation

---

## 6. Retrieval-Based Decoding

In the primary evaluation setup:

* Each EEG embedding is matched against a candidate set of text embeddings
* Similarity metrics (e.g., cosine similarity) are used for ranking
* Performance is reported using Top-K retrieval accuracy

This approach provides:

* Stable and interpretable decoding
* Lower risk of hallucination compared to free-form generation
* A strong foundation for assistive communication systems

---

## 7. Generation Path (Exploratory)

A generation module is explored to map EEG-derived embeddings into natural language outputs.

Current status:

* Uses frozen or lightly adapted large language models
* EEG embeddings are projected into the language model’s latent space
* Outputs show semantic alignment but are not yet production-ready

Generation is presented as **ongoing research**, not as the primary demonstrated capability.

---

## 8. Cross-Subject Considerations

Training across multiple subjects improves the geometry of the shared embedding space.

Observed behavior:

* Strong semantic clustering across subjects
* Limited zero-shot performance on completely unseen subjects
* Practical usage likely requires light subject-specific adaptation

---

## 9. Design Philosophy

* **Modularity**: Encoder, retrieval, and generation are decoupled
* **Interpretability First**: Retrieval prioritized over unconstrained generation
* **Research Transparency**: Architectural intent shared without exposing proprietary internals
* **Scalability**: Designed to support future datasets, subjects, and modalities

---

## 10. Scope & Limitations

* This document intentionally omits layer-level details and training hyperparameters
* The released repository focuses on demonstration and structure, not full reproducibility
* Results and metrics are selectively disclosed to protect ongoing research

For questions or research collaboration inquiries, contact: **[info@excelleve.com](mailto:info@excelleve.com)**
