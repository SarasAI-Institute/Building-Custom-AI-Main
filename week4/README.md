# Week 4 — Beyond Fine-Tuning: Distill, Merge, Quantize & Ship

> Your Analyst works. This week answers the question every internal-AI project eventually
> faces: **"great demo — can it run fast, cheap, and private?"** Three compression tools, an
> honest quality gate, and the payoff: the full RiskLens pipeline, assembled and deployable.

## Learning outcomes

By the end of this week you can:

1. **Choose and apply the right compression tool**: knowledge distillation (teacher→student),
   model merging with `mergekit` (consolidation — *not* emergent magic), and quantization
   (bitsandbytes 8/4-bit, plus the GGUF pipeline for CPU/edge serving).
2. **Run a professional quality gate**: commit thresholds *before* measuring, re-score the
   frozen Week-3 test set on format **and** content, and state the verdict — even when it's ❌.
3. **Measure serving honestly**: p50/p95 latency, tokens/sec from actually-generated tokens,
   $/1k reports — and explain why 4-bit can be *slower* on a T4 while 3× smaller.
4. **Assemble and ship the pipeline**: VLM → RAG → quantized Analyst composed through clean
   contracts, wrapped in a Gradio demo.

## This week's materials

| File | What it is | When to use it |
|---|---|---|
| [`week4_distill_merge_quantize_ship.ipynb`](week4_distill_merge_quantize_ship.ipynb) | The live-session notebook, fully annotated | During/after the session; complete self-study |
| [`week4_workbook.ipynb`](week4_workbook.ipynb) | The live-coding workbook — core cells left as TODOs | What we code together in the session |
| [`week4_concepts.pptx`](week4_concepts.pptx) | Concept deck (distillation · merging honesty · precision ladder · **save formats incl. GGUF** · serving) | Opened before each coding block |
| [`assignment/`](assignment/) | **Ungraded practice** — 12 tasks with self-checks + solution notebook | After the session, ~75–100 min |

## ⚠️ Before the session (10 minutes — this week it's mandatory)

1. **Bring your Week-3 artifacts**: `analyst-lora-adapter/` and `week3_test_rows.json` must
   sit next to the notebook — the setup cell checks for both and stops early if missing
   (re-run Week 3's final cells if you lost them to a recycled runtime).
2. Colab, runtime → **GPU (T4)**; run the setup cells to pre-cache the base model (~3 GB).

## Data & models this week

- **Your own Analyst** — the star of the week: merged, quantized, gated, shipped.
- **Stack:** `peft` (`merge_and_unload`) · `bitsandbytes` (8/4-bit) · `mergekit` (TIES/SLERP/DARE,
  CPU-only) · `llama.cpp` (GGUF, walkthrough) · `gradio` (the demo).
- **Frozen data:** Week 3's saved test set — the whole point is re-scoring *the same* rows
  after compression.

## After the session

1. **Do the [assignment](assignment/)** — the compression gauntlet: half → 8-bit → 4-bit,
   with the memory/latency/quality table and a pre-committed gate.
2. **Capstone Stage 4** — this week's graded increment: ≥2 compression arms, the quality
   gate, the assembled `analyze_product()`, serving economics, and the 10-product stress
   test. Deliverables D4.1–D4.7, worth 25 points — see `capstone/README.md`.
3. **Then Week 5**: one clean run-all, the five-week metrics ledger, and your reflection —
   final delivery details in the capstone README.

## Optional reading (~30 min)

- **TIES-Merging** — Yadav et al. 2023, [arXiv:2306.01708](https://arxiv.org/abs/2306.01708)
- **AWQ** — Lin et al. 2023, [arXiv:2306.00978](https://arxiv.org/abs/2306.00978)

---
*This is the last technique week — next stop: capstone delivery. Ship something you'd demo.* 🚀
