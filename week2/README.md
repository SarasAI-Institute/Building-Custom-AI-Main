# Week 2 — Custom Knowledge: RAG, KAG & GraphRAG

> Your model's knowledge is frozen at training time — this week you connect it to **your**
> data: retrieval, grounding with citations, a refusal rule that kills hallucination, and the
> two-metric evaluation that tells you exactly where a RAG answer went wrong.

## Learning outcomes

By the end of this week you can:

1. **Build an end-to-end RAG pipeline** — chunking with overlap, normalized embeddings, a
   FAISS index, retrieval with the BGE query prefix, and grounded generation that cites its
   sources and refuses when the evidence isn't there.
2. **Distinguish RAG, KAG and GraphRAG** — and demonstrate with code when entity-graph
   expansion retrieves what pure similarity cannot (multi-hop questions).
3. **Evaluate retrieval and generation separately**: a frozen gold Q&A set authored *before*
   the index exists, recall@k with its diagnostic reading, and faithfulness + answer-relevance
   via an LLM judge — with the judge-bias caveats stated out loud.

## This week's materials

| File | What it is | When to use it |
|---|---|---|
| [`week2_rag_kag_graphrag.ipynb`](week2_rag_kag_graphrag.ipynb) | The live-session notebook, fully annotated | During/after the session; complete self-study |
| [`week2_workbook.ipynb`](week2_workbook.ipynb) | The live-coding workbook — core cells left as TODOs | What we code together in the session |
| [`week2_concepts.pptx`](week2_concepts.pptx) | Concept deck (RAG in one picture · two failure modes · GraphRAG · the frozen gold set) | Opened before each coding block |
| [`assignment/`](assignment/) | **Ungraded practice** — 11 tasks with self-checks + solution notebook | After the session, ~60–90 min |

## The live session (2 hours)

**Title:** Retrieval-Augmented Generation over Internal Documents

1. **The problem** *(deck)* — frozen knowledge, fluent guessing, why fine-tuning won't fix facts.
2. **Build the engine** *(code)* — corpus (real reviews + spec sheets), chunking, embeddings,
   FAISS, `retrieve()` with the BGE prefix.
3. **Grounded generation** *(code)* — the three-block prompt, citations, the refusal rule,
   and the with/without-retrieval comparison that sells RAG to any stakeholder.
4. **Beyond flat RAG** *(deck + code)* — where similarity breaks; a mini GraphRAG with
   entity extraction and 1-hop expansion.
5. **Evaluation** *(deck + code)* — the frozen gold set, recall@k diagnostics, faithfulness +
   answer-relevance judges and their honest caveats.

## Before the session (5 minutes, the day before)

1. Open the notebook in Colab, runtime → **GPU (T4)**.
2. Run the setup cells — this pre-caches the generator model (~3 GB) and streams the review
   corpus so the session has zero dead air.

## Data & models this week

- **Generator:** [`Qwen/Qwen2.5-1.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct)
- **Embedder:** [`BAAI/bge-small-en-v1.5`](https://huggingface.co/BAAI/bge-small-en-v1.5)
  (384-dim; remember: the query prefix matters)
- **Data:** real Amazon appliance reviews streamed from the raw Hub file (only the head is
  read — no giant download) + hand-written spec/policy docs with planted facts, so you always
  know the ground truth.

## After the session

1. **Do the [assignment](assignment/)** — 11 tasks rebuilding the engine from parts, with a
   recall@k gold set and a refusal stress test.
2. **Capstone Stage 2** — this week's graded increment: your corpus + frozen gold set, beat
   the naive baseline retriever on recall@4, refusal + judge scoring, and one measured
   retrieval upgrade. Deliverables D2.1–D2.7, worth 25 points — see `capstone/README.md`.

## Read before next week (~45 min)

- **LoRA** — Hu et al. 2021, [arXiv:2106.09685](https://arxiv.org/abs/2106.09685)
- **QLoRA** — Dettmers et al. 2023, [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)
  *(next week we train with both, on a free T4)*

---
*Next week: changing how the model **behaves** — fine-tuning the Analyst with QLoRA.*
