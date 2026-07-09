# 🏭 Build Custom AI: From Foundations to Custom Small Models

**A 4-week, hands-on program on building custom AI systems for internal use — taught live, built on the Hugging Face ecosystem, evaluated like production software.**

*SarasAI · instructor: Luka Anicin*

---

## What this course is

Most AI courses teach you to call an API. This one teaches you to **build the model layer yourself**: adapt open Vision-Language Models to your product images, connect language models to your company's knowledge, fine-tune Small Language Models to your format on a free GPU, and compress the result until it's cheap enough to actually ship.

Everything runs on a **single free-tier GPU (Colab T4, 16 GB)**. Every technique is taught by building a real component of one system:

```
photo ──▶ VLM inspector ──▶ defect note ──▶ RAG evidence ──▶ fine-tuned Analyst ──▶ risk report
```

By Week 4 you will have built **RiskLens** — a multi-modal product-risk pipeline: a VLM that spots visual defects, a retrieval system that gathers evidence from reviews and specs, and a QLoRA-fine-tuned, quantized "Analyst" SLM that writes the root-cause report.

## Who it's for

Engineers and technically-minded builders who can write Python. No deep-learning background required — Week 1 builds the foundations you need. If you already know Transformers, the weekly assignments and capstone will still stretch you: this course's bar is *measured, production-honest work*, not demos.

## Program structure

| Week | Live session (2h) | Technique | You ship |
|---|---|---|---|
| **1** | From Transformers to Vision-Language Models | VLM adaptation, prompting ladder, frozen-split evaluation | A measured visual defect detector |
| **2** | Custom Knowledge: RAG, KAG & GraphRAG | Embeddings, retrieval, grounding, recall@k + faithfulness | A cited, refusal-safe evidence engine |
| **3** | Fine-Tuning SLMs with LoRA & QLoRA | Synthetic data with hygiene, PEFT training, honest A/B evals | The fine-tuned Analyst |
| **4** | Distill, Merge, Quantize & Ship | Compression, quality gates, serving economics | The assembled, deployable pipeline |
| **5** | Capstone delivery | — | Final run + hidden-holdout scorecard |

**Each week contains:**
- 📓 **Live-session notebook** — the 2-hour workshop, fully annotated so it works as self-study
- 🎞 **Concept deck** — the theory slides opened before each coding block
- ✏️ **Ungraded assignment** — 11–12 tasks with self-checks + a full solution notebook
- 🏗 **Capstone increment** — the week's graded deliverables in your capstone notebook

Weeks are released one at a time. **Currently available: Week 1.**

## The evaluation thread (what makes this course different)

One rule runs through all four weeks: **no deliverable is "done" without a measured number on a frozen held-out set** — a split you built *before* you started iterating, and never tuned against. You'll freeze image splits, author gold question sets before building the index, certify train/test splits leakage-free, and commit quality-gate thresholds before seeing the numbers. The grading rubric pays for this discipline explicitly: an honest 78% outscores a leaked 95%.

## The capstone (graded — 100 points, 25/week, Satisfactory ≥ 70)

You inherit a *partially working* pipeline with deliberately weak baselines and planted bugs, and replace one stage per week with your own measured build. One notebook, submitted as the same link every week; a hidden holdout set scores your final system on data you've never seen. Details: `capstone/README.md` and `capstone/RUBRICS.md` *(released with Week 1's session)*.

## Setup

1. **GPU:** a free [Google Colab](https://colab.research.google.com) T4 is enough for everything (Kaggle's free tier also works). Paid options (Colab Pro, RunPod) only buy comfort.
2. **Hugging Face account:** free — [huggingface.co/join](https://huggingface.co/join). You'll pull all models and data from the Hub.
3. **Open the week's notebook in Colab**, switch the runtime to GPU (`Runtime → Change runtime type → T4`), and run the setup cells top to bottom. Every notebook installs its own dependencies and detects your GPU's capabilities automatically.

No local installation is required for any part of the course.

## Repository layout

```
├── README.md                  <- you are here
├── Custom-AI-Curriculum.md    <- the full program curriculum
├── week1/                     <- Foundations & Custom Vision with VLMs
│   ├── README.md              <- week overview: outcomes, materials, how to work
│   ├── week1_*.ipynb          <- the live-session notebook (fully annotated)
│   ├── week1_workbook.ipynb   <- live-coding workbook (TODO version used in the session)
│   ├── week1_concepts.pptx    <- the concept deck
│   └── assignment/            <- ungraded practice: tasks + solutions + README
├── week2/ … week4/            <- released weekly
├── capstone/                  <- the graded project: starter notebook + rubric
└── course_setup/              <- instructor-only: hidden holdout + scoring (not published)
```

## House rules

- **Run the numbers.** Every claim you make about your model should have a metric behind it — the notebooks show you how, every single week.
- **Assignments are ungraded but not optional** in spirit: the capstone assumes the muscle memory they build.
- **Use the solutions well.** Stuck 15+ minutes → read *that one task's* solution, close it, write your own version.

---

*Questions? Reach out to your instructor or post in the course forum.*
