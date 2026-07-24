# Week 3 — Custom Behavior: Fine-Tuning SLMs with QLoRA

> Weeks 1–2 changed what the model *knows*. This week you change how it **behaves** — training
> the capstone's Analyst to write your report format, every time, on a free T4. The technique
> is QLoRA; the real lesson is that **the dataset and the eval decide everything**.

## Learning outcomes

By the end of this week you can:

1. **Fine-tune a Small Language Model with QLoRA** — 4-bit NF4 base + LoRA adapters via
   `peft` + `trl`'s `SFTTrainer` — and explain exactly why it fits in 16 GB (the three QLoRA
   tricks: NF4, double quantization, paged optimizers).
2. **Engineer training data with hygiene**: diverse synthetic generation, embedding dedup,
   a decontaminated train/test split with a printed leakage certificate.
3. **Prove the improvement honestly**: format adherence (deterministic), a rubric-score judge
   (with its bias caveats), and a blind win-rate vs the base model — with randomized A/B
   position and `disable_adapter()` used correctly (the "trap" every tutorial gets wrong).

## This week's materials

| File | What it is | When to use it |
|---|---|---|
| [`week3_finetuning_analyst_qlora.ipynb`](week3_finetuning_analyst_qlora.ipynb) | The live-session notebook, fully annotated | During/after the session; complete self-study |
| [`week3_workbook.ipynb`](week3_workbook.ipynb) | The live-coding workbook — core cells left as TODOs | What we code together in the session |
| [`week3_concepts.pptx`](week3_concepts.pptx) | Concept deck (RAG-vs-fine-tune decision · LoRA/QLoRA · data hygiene · DPO) | Opened before each coding block |
| [`assignment/`](assignment/) | **Ungraded practice** — 12 tasks with self-checks + solution notebook | After the session, ~75–90 min |

## The live session (2 hours)

**Title:** Fine-Tuning Small Language Models with LoRA & QLoRA

1. **The decision framework** *(deck)* — facts → RAG; behavior/format → fine-tuning; the
   capstone needs both.
2. **QLoRA mechanics** *(deck + code)* — 4-bit load, the four LoRA numbers that matter,
   trainable-parameter accounting.
3. **The dataset is the product** *(code)* — synthetic generation with deliberate diversity,
   dedup, split, decontamination-as-an-action.
4. **Train** *(code)* — `SFTTrainer`, reading the loss curve, the memorization warning.
5. **Prove it** *(code)* — format adherence, rubric judge, blind randomized win-rate; save the
   adapter + frozen test set (Week 4 re-scores them after compression).
6. **DPO preview** *(deck)* — preference pairs, no reward model; the natural next step.

## Before the session (5 minutes, the day before)

1. Colab, runtime → **GPU (T4)** — this week training actually runs, GPU is mandatory.
2. Run the setup cells to pre-cache the base model (~1.2 GB in 4-bit) and the embedder.

## Data & models this week

- **Base model:** [`Qwen/Qwen2.5-1.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct), loaded 4-bit
- **Stack:** `peft` (LoRA) · `trl` (`SFTTrainer`) · `bitsandbytes` (NF4) · `sentence-transformers` (hygiene checks)
- **Data:** generated in-notebook (a curated synthetic generator — the session is honest about
  why, and the capstone requires a real teacher model instead)

## After the session

1. **Do the [assignment](assignment/)** — 12 tasks: your own generator vocabulary, the full
   hygiene chain, a short QLoRA run, and the honest A/B with a blind randomized judge.
2. **Capstone Stage 3** — this week's graded increment: ≥150 teacher-model pairs, complete
   dataset card with leakage certificate, QLoRA fine-tune, three-way eval, one training
   ablation. Deliverables D3.1–D3.7, worth 25 points — see `capstone/README.md`.
3. **Keep your artifacts** — `analyst-lora-adapter/` and `week3_test_rows.json` are Week 4's
   inputs. Don't lose them to a recycled Colab runtime: download or push to the Hub.

## Read before next week (~45 min)

- **Distillation** — Hinton et al. 2015, [arXiv:1503.02531](https://arxiv.org/abs/1503.02531)
- **LLM.int8()** — Dettmers et al. 2022, [arXiv:2208.07339](https://arxiv.org/abs/2208.07339)
  *(next week we compress your Analyst until it's cheap enough to ship)*

---
*Next week: distill, merge, quantize & ship — the Analyst goes to production.*
