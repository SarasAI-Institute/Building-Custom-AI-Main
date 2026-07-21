# Week 2 Assignment · Build RAG From Parts — and Prove It Works

**Status:** ungraded practice · **Time:** ~60–90 min · **Compute:** free Colab T4

## What this is

Every part of a RAG system, built by hand and **measured before it's trusted** — 11 tasks in
four parts over a corpus of 24 customer reviews + 4 internal docs (specs + a returns policy)
about fictional products. Fictional matters: anything specific the bare model claims later is
guaranteed hallucination, which makes the final comparison undeniable.

| Part | Tasks | What you build |
|---|---|---|
| 1 · Corpus & index | 1–3 | uniform corpus shaping · embeddings **with unit-norm verification** · FAISS index |
| 2 · Retrieval, measured | 4–6 | `retrieve()` with the BGE prefix · **recall@k on a 6-question gold set** · a with/without-prefix A/B |
| 3 · Grounded generation | 7–9 | the `generate()` chat helper · grounded prompt with citations · a 3-question **refusal-rule stress test** |
| 4 · Evaluation | 10–11 | the with/without-retrieval table · an LLM **faithfulness judge** (with its honest caveats) |

## Learning outcomes

By the end you can:
1. **Build and verify a vector index** — including why unit-norm vectors make inner product = cosine.
2. **Measure retrieval in isolation** with recall@k, and read the diagnostic (recall@1 vs @5 → reranker vs. fix embeddings).
3. **Measure config choices instead of assuming them** (the BGE-prefix A/B).
4. **Write grounded prompts** whose refusal rule survives adversarial unanswerable questions.
5. **Score faithfulness with an LLM judge** — and recite why a same-family judge is only a smoke detector.

## Files

| File | What it is |
|---|---|
| `week2_assignment.ipynb` | **Start here.** 11 tasks with `...` placeholders + self-checks |
| `week2_assignment_solution.ipynb` | Reference implementation |

## How to work

1. GPU runtime; run the given setup (corpus + generator load).
2. Work in order — `retrieve()` feeds recall@k, which feeds the prefix A/B; `generate()` feeds
   everything in Parts 3–4.
3. Fill each `...`, run the self-check under it. The retrieval check is *semantic*: "leaks
   liquid everywhere" must find "seal drips" with no shared keywords.
4. If the refusal stress test fails, tighten your RULES block and re-run — that loop is the skill.

**Done when:** all self-checks pass, your refusal rate is ≥2/3, and you can answer the
reflection: what did your recall@1 vs recall@5 gap tell you to fix first?

## Ties into

- **Live session notebook:** `../week2_rag_kag_graphrag.ipynb` · **Deck:** `../week2_concepts.pptx`
- **Graded increment 2:** full capstone corpus, ≥20-question frozen gold set, recall@k table,
  faithfulness + answer-relevance via `ragas`.
