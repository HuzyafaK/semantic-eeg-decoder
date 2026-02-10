# ChiSCO-CLIP

**Semantic decoding of imagined speech from EEG via contrastive alignment and LLM prefix tuning.**

ChiSCO-CLIP is an internal research system developed at **Excelleve** for decoding *imagined speech semantics* from non-invasive EEG. The system aligns EEG signals to a shared semantic space defined by text embeddings and optionally translates those embeddings into natural language using a lightweight adapter to a frozen Large Language Model (LLM).

This repository is intended to document the **architecture, methodology, and demo interface**. Core training and inference code is not publicly released.

---

## Overview

* **Modality:** Non-invasive EEG (imagined speech)
* **Goal:** Decode *semantic intent* rather than exact phoneme or syntax
* **Key idea:** Treat EEG-to-language as a *semantic retrieval and alignment* problem, not direct sequence decoding
* **Approach:** CLIP-style contrastive learning + prototype banks + LLM prefix tuning

---

## Model Architecture

```
Raw EEG (128 channels, 1651 timesteps)
        │
        ▼
Channel Selection (122 EEG channels)
        │
        ▼
1D CNN Encoder (temporal feature extraction)
        │
        ▼
Temporal Projection + Positional Encoding
        │
        ▼
Transformer Encoder (time tokens)
        │
        ▼
Mean Pooling (robust temporal aggregation)
        │
        ▼
EEG Semantic Embedding (512-D, normalized)
        │
        ├──────────────► Semantic Retrieval (Prototype Bank)
        │
        └──────────────► Semantic Prefix Adapter
                              │
                              ▼
                     Frozen LLM (Qwen)
                              │
                              ▼
                    Semantically Aligned Text
```

---

## Training Strategy

### 1. EEG–Text Semantic Alignment

* A dual-encoder framework aligns EEG embeddings with text embeddings produced by a frozen language model encoder.
* All trials corresponding to the same sentence form a **semantic prototype**, encouraging subject-invariant clustering.

### 2. Prototype-Based Supervision

* Unique training sentences are encoded into a **prototype bank**.
* EEG embeddings are trained via cross-entropy / contrastive loss to retrieve the correct prototype.

### 3. EEG-to-Text Generation (Optional)

* A lightweight **Semantic Prefix Adapter** maps EEG embeddings into prefix tokens.
* These prefixes steer a frozen LLM to generate text aligned with EEG semantics.
* No full LLM fine-tuning is performed.

---

## Dataset

This work uses the **ChiSCO (Chinese Imagined Speech Corpus)** dataset:

* High-density EEG (128 channels; 122 used in our models)
* Imagined speech tasks with thousands of unique sentences
* Publicly available for academic research

### Dataset Citation (BibTeX)

```bibtex
@article{zhang2024chisco,
  title   = {ChiSCO: An EEG-Based Brain--Computer Interface Dataset for Imagined Speech Decoding},
  author  = {Zhang, Z. and others},
  journal = {Scientific Data},
  year    = {2024}
}
```

---

## Research Status

* Strong **cross-subject semantic alignment** when training on multiple subjects
* High **Top-K retrieval accuracy** on seen subjects
* Generation captures **pragmatic intent** even when exact wording differs
* Zero-shot generalization to unseen subjects remains limited

---

## FAQ

**Q: Does this work on new people?**
**A:** In preliminary calibration experiments we measured that short, targeted adaptation markedly improves retrieval performance: most users achieved **significant Top-K (e.g., Top-5) retrieval improvement** within minutes to tens of minutes of calibration. Zero-shot performance remains limited; we are expanding these tests and can provide calibration curves on request.

---

## Demo

This repository accompanies an internal demo that visualizes:

* Raw EEG signals
* Learned EEG embeddings
* Top-K semantic retrieval results
* Semantically aligned text generation (research preview)

The demo is illustrative and does not expose model weights or training code.

---

## License & Use

This repository is released under the **MIT License** for documentation and interface code only.

Model weights, training scripts, and full inference pipelines are **not** included and are available only under separate agreement.

```
MIT License

Copyright (c) 2026 Excelleve

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Contact

For research collaboration, investment discussions, or access requests:

📧 **[info@excelleve.com](mailto:info@excelleve.com)**

---

*ChiSCO-CLIP is an active research project. Details may evolve as experiments continue.*
