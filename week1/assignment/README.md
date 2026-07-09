# Week 1 Assignment · From Tokens to Your First AI Inspector

**Status:** ungraded practice · **Time:** ~60–90 min · **Compute:** free Colab T4 (auto-falls back to a 256M model on CPU)

## What this is

A hands-on replay of the live session's full arc — foundations to a measured defect detector —
in **12 tasks across five parts**. This is the widest assignment of the course on purpose:
Week 1 is the foundations week, and everything later (RAG's embeddings, fine-tuning's chat
templates, the capstone's JSON contracts) leans on what your hands learn here.

| Part | Tasks | What you build |
|---|---|---|
| 1 · Foundations | 1–3 | tokenizer exploration · embedding-geometry proof (`cos(crack, fracture) > cos(crack, banana)`) · `pipeline()` one-liner |
| 2 · Meet the VLM | 4–6 | load VLM + processor · `ask_vlm()` chat-message call · a verdict parser that survives **negations** ("no defects found" ≠ DEFECTIVE) |
| 3 · Prompting ladder | 7–9 | accuracy loop · zero-shot baseline · domain prompt · **few-shot with example images** — all iterated on the dev set only |
| 4 · Structured output | 10 | JSON contract + defensive parsing (the capstone's Stage-1 interface) |
| 5 · Measure like a pro | 11–12 | one timed pass over the frozen test set ($/1k images) · precision/recall + confusion matrix + interpretation |

## Learning outcomes

By the end you can:
1. **Show what a model actually sees** — sub-word tokens, and why token count ≠ word count.
2. **Prove meaning-is-geometry numerically** with embedding cosine similarity — the fact Week 2's retrieval engine is built on.
3. **Call a VLM** through the chat-message API, including **multi-image few-shot** messages.
4. **Parse model output defensively** — negation-safe verdicts and fallback-safe JSON.
5. **Run the frozen-split discipline end to end**: iterate on dev, commit, one timed test pass, report precision/recall + confusion matrix + cost per 1k images.

## Files

| File | What it is |
|---|---|
| `week1_assignment.ipynb` | **Start here.** 12 tasks with `...` placeholders; setup + dataset adapter given; self-check cell after nearly every task |
| `week1_assignment_solution.ipynb` | Reference implementation — for *checking*, not starting |

## How to work

1. GPU runtime (Colab T4). Run the given setup cells; they must pass before Task 1.
2. Work the tasks in order — later tasks reuse earlier functions (`parse_verdict` feeds the
   accuracy loop; the dev/test split gates Parts 3–5).
3. Fill each `...`, then run the **self-check cell** below it — instant feedback.
4. Stuck 15+ minutes? Read *that one task* in the solution notebook, close it, write your own.
5. Finish with the two reflection answers in the final cell — they're the week's actual lesson.

**Done when:** all self-checks pass, the confusion matrix renders, and your reflection answers
say which error type (missed defect vs. false alarm) costs a factory more — and why 10 test
images make every metric noisy by ±10 points.

## Ties into

- **Live session notebook:** `../week1_foundations_and_vlm_defect_detection.ipynb`
- **Concept deck:** `../week1_concepts.pptx`
- **Graded increment 1:** the same discipline on a bigger frozen split.
