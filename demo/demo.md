# Demo — semantic-eeg-decoder (ChiSCO-CLIP)

This document describes the offline demo package, how to run/replay it, and a recommended script for investor/research walkthroughs. The demo is intentionally reproducible with precomputed artifacts and does **not** require the proprietary encoder implementation or raw EEG files.

---

## What the demo shows (core claims)

* Offline inference using precomputed EEG embeddings mapped into a semantic space.
* Retrieval-first decoding (Top‑K semantic retrieval from a text prototype gallery).
* Optional LLM-based language realization shown as a downstream, labelled feature.
* Diagnostic alignment metrics (cosine similarities) for interpretability.

The demo proves **semantic intent alignment**, not live real-time EEG acquisition.

---

## Demo assets included (public-safe)

* `demo_video.mp4` — 2–3 minute narrated screen recording of the demo UI and workflow. Use as the primary asset for remote demos.
* `demo_screenshots/` — a set of 3–5 PNG screenshots (UI, Top‑K table, generation panel, embedding map).
* `golden_samples/` — 5–10 curated trials represented as non-reversible precomputed embeddings and metadata:

  * `sample_embeddings.npy` — precomputed L2-normalized embeddings (shape: N × D)
  * `sample_metadata.json` — masked metadata (trial id, anonymized subject tag, human-readable ground-truth sentence)
* `sample_outputs.json` — saved retrieval outputs and generation outputs used to render UI visuals in the video. This is the canonical playback file used by the demo UI.
* `demo_instructions.md` — (this file) runbook describing how to replay and talk through the demo.

> No raw EEG, training code, or model checkpoints are provided in the public demo.

---

## How to replay the demo (local, reproducible)

### Option A — Play the recorded demo video (fastest)

1. Open `demo/demo_video.mp4`. This contains the narrated walkthrough showing UI interaction, retrieval outputs, and an explanation of metrics. Use this for remote or async investor outreach.

### Option B — Reproduce visuals from precomputed artifacts (interactive)

If you want an interactive local playback (no proprietary model required):

1. Clone the repo and place the `demo/` folder at the repo root.
2. Open a Python environment and install the minimal requirements in `requirements-demo.txt` (streamlit or gradio, numpy, pandas). No model dependencies.
3. Use the included `sample_outputs.json` and `sample_embeddings.npy` to render the UI (a simple script is provided only as pseudocode in `demo/demo_instructions.md` to avoid shipping proprietary UI code).

Minimal pseudocode to render the Top‑K table locally (public-safe):

```python
# load precomputed outputs (already contains top-k sentences and cosines)
import json
with open('demo/sample_outputs.json') as f:
    outputs = json.load(f)
# outputs is an ordered list of demo events; each event contains:
# - metadata: {trial_id, subject_mask}
# - top_k: [ {text: str, cosine: float}, ... ]
# - generated: {text: str, cosine: float}
# render with any simple frontend or print to console
print(outputs[0]['top_k'])
```

> This public pseudocode intentionally avoids referencing encoder code or model APIs.

---

## UI states to highlight during a live walkthrough

1. **EEG input panel** — show that the UI accepts a selected `golden` sample and displays trial metadata (masked). Explain that the demo uses precomputed embeddings in public mode.
2. **Top‑K retrieval table (center)** — emphasize ranking, cosine values, and highlight the ground-truth when present. This is the single most persuasive artifact.
3. **Embedding alignment visualization (optional)** — show UMAP/PCA where EEG embedding sits relative to text prototypes (if included in screenshots). Point out clustering of semantically similar prototypes.
4. **Generation panel (right)** — collapsible; emphasize that generation is LLM-assisted and downstream, and show cosine between EEG embedding and generated text.
5. **Metrics panel** — show Top‑K badges (no raw tables). If asked, say that numeric calibration curves are available under NDA.

---

## Recommended live demo script (2–3 minutes)

Use this script verbatim for investor walkthroughs. Keep it tight.

1. **Hook (10s)** — “We map imagined-speech EEG into a shared semantic embedding space. Today I’ll show a frozen offline demo that proves semantic intent decoding.”

2. **Play or run sample (30–45s)** — Select a `golden` sample, click `Run Semantic Decoding` (or play recorded event). Show the Top‑K table filling in; wait a second to highlight the correct item in Top‑5.

3. **Explain the metric (20s)** — “This is retrieval-first: we measure how often the correct semantic match appears in the top K candidates. That’s our primary validated signal — interpretable, measurable, and robust.”

4. **Show generation (20s)** — Collapse/expand the generation panel: “Once semantic intent is stable, an adapter maps embeddings into a frozen LLM to realize language. Generation is downstream and improves with scale.”

5. **Close with roadmap (15s)** — “Current demo is offline on precomputed embeddings. Next steps are more subjects, faster calibration, and controlled clinical pilots. We can share calibration curves and logs under NDA.”

---

## Talking points for likely investor questions

* **Q: Is this live?** A: The public demo uses precomputed embeddings for reproducible playback. The research prototype supports live inference with proprietary encoder and low-latency runtime.

* **Q: Why retrieval?** A: Retrieval proves semantic alignment cleanly and avoids hallucination; generation is a controlled downstream step.

* **Q: How confident are you?** A: We have measured calibration gains (short adaptation times); detailed curves are available under NDA.

* **Q: Data & privacy?** A: We never publish raw EEG; demo assets are non-reversible embeddings and masked metadata only.

---

## What NOT to do during a demo

* Don’t imply clinical readiness or real-time bedside capability. This is a research prototype.
* Don’t show raw EEG traces (they are not in repo).
* Don’t promise zero-shot performance on unseen users. Instead, emphasize calibration results are available under NDA.

---

## How to request deeper access

For research partnerships, calibration logs, or model access, email **[info@excelleve.com](mailto:info@excelleve.com)** with affiliation and purpose. We typically proceed under an NDA or research collaboration agreement.

---

## Troubleshooting quick notes

* If screenshots don’t match demo video: ensure you use the `golden_samples` and `sample_outputs.json` included in the demo folder.
* If running the local renderer, a simple Python script that reads `sample_outputs.json` is sufficient — you do not need any model weights.

---

## Appendix: demo event JSON schema (for integrators)

Each event in `sample_outputs.json` contains the following keys (public-safe):

```
{
  "trial_id": "demo_01",
  "subject_mask": "Sx",
  "top_k": [ {"text": "...", "cosine": 0.82}, ... ],
  "generated": {"text": "...", "cosine": 0.76},
  "timestamp": "2026-02-10T12:34:56Z"
}
```

No raw EEG is included. The `cosine` values are precomputed similarity scores used to render the UI.

Which would you like?
