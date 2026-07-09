# Week 1 — Foundations & Custom Vision with VLMs

> From "what is a token?" to a **measured visual defect detector** in one week — using a
> Vision-Language Model instead of training a CNN, because in 2026 that's how custom vision
> systems actually get built.

## Learning outcomes

By the end of this week you can:

1. **Explain the Transformer stack from the bottom up** — tokens → embeddings → attention —
   and show, with code, that meaning is geometry (`cos(crack, fracture) ≫ cos(crack, banana)`).
2. **Adapt an open Vision-Language Model to a custom visual task** through the chat-message
   API: zero-shot prompting → domain prompting → few-shot with example images → structured
   JSON output that downstream code can parse.
3. **Evaluate like a professional**: freeze a held-out image split *before* iterating, tune
   prompts on dev only, run the test set once, and report accuracy, defect-class
   precision/recall, a confusion matrix, and cost per 1,000 images.

## This week's materials

| File | What it is | When to use it |
|---|---|---|
| [`week1_foundations_and_vlm_defect_detection.ipynb`](week1_foundations_and_vlm_defect_detection.ipynb) | The live-session notebook, fully annotated — every cell explained | During/after the session; works as complete self-study |
| [`week1_workbook.ipynb`](week1_workbook.ipynb) | The live-coding workbook — the same notebook with the core cells left as TODOs | What we code together in the session |
| [`week1_concepts.pptx`](week1_concepts.pptx) | The concept deck (Transformer in 3 ideas · what a VLM is · variable image sizes · frozen-split evaluation) | Opened before each coding block in the session |
| [`assignment/`](assignment/) | **Ungraded practice** — 12 tasks across 5 parts with self-checks, plus a full solution notebook | After the session, ~60–90 min |

## The live session (2 hours)

**Title:** From Transformers to Vision-Language Models on Hugging Face

1. **Foundations refresher** *(deck + code)* — tokens, embeddings, attention; the Hugging Face
   ecosystem (`pipeline()`, the Hub, model cards).
2. **Meet the VLM** *(deck + code)* — how images become tokens, the input/output contract,
   why resolution is the cost dial; loading SmolVLM2 and writing `ask_vlm()`.
3. **The prompting ladder** *(code)* — zero-shot → domain prompt → few-shot with images,
   every rung measured on a dev set.
4. **Structured output** *(code)* — JSON verdicts with defensive parsing: the pipeline contract.
5. **Evaluate like a professional** *(deck + code)* — the frozen split, one timed test pass,
   precision/recall and what they cost a factory.

## Before the session (10 minutes, do this the day before)

1. Open the notebook in Colab and switch the runtime to **GPU (T4)**.
2. Run the **setup cells** (installs → model load → dataset download). This pre-caches
   ~4.5 GB of model weights and ~150 MB of images so the session has zero dead air.
3. Have the concept deck downloaded if you want to follow the slides locally.

## Data & models this week

- **Model:** [`HuggingFaceTB/SmolVLM2-2.2B-Instruct`](https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct)
  (a 256M fallback is wired in for CPU-only machines).
- **Data:** the bottle category of **MVTec AD** (industrial defect-detection benchmark) via a
  Hub mirror — the notebook downloads *only* that category (~150 MB), by path pattern.
  Two conventions worth knowing before you look at it: the *train* split contains only good
  units, and the repo carries segmentation masks we deliberately never fetch.

## After the session

1. **Do the [assignment](assignment/)** — it replays the session's full arc with your hands on
   the keyboard (12 tasks, self-checks after each). Solutions included; use them to *check*,
   not to start.
2. **Start capstone Stage 1** — this week's graded increment: diagnose the 3 planted bugs in
   the baseline inspector, beat it on your own frozen split (≥40 images), and run the
   resolution-budget experiment. Deliverables D1.1–D1.7, worth 25 points.
   See `capstone/README.md` + `RUBRICS.md § Week 1`.


---
*Next week: the model meets your company's knowledge — RAG, KAG & GraphRAG.*
