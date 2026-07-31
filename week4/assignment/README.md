# Week 4 Assignment · The Compression Gauntlet: half → 8-bit → 4-bit

**Status:** ungraded practice · **Time:** ~75–100 min · **Compute:** GPU required (free T4 is enough)

## What this is

Compression claims are cheap — **measurements are the assignment**. You produce **three
precision variants** of an Analyst model (half, 8-bit LLM.int8, 4-bit NF4) and run all three
through the same gauntlet — memory, latency, two quality metrics on the frozen set — ending in
a gate verdict whose threshold you committed to *before seeing any number*. 12 tasks in five parts.

| Part | Tasks | What you build |
|---|---|---|
| 1 · One standalone model | 1–3 | frozen-set **contract validation** · adapter fold-in · sizing a model from its parameter count (predict, then verify) |
| 2 · Three precision arms | 4–6 | 8-bit reload · 4-bit reload · the monotonic memory ladder |
| 3 · Speed, honestly | 7–8 | `bench()` with p50/p95 + **true token counts** · all three arms |
| 4 · The gate | 9–11 | format re-score · embedding **content score** · verdict + the full deliverable table |
| 5 · Ship it | 12 | the GGUF pipeline (incl. the build step) + a mergekit YAML + its acceptance test |

Fully standalone: Week-3 artifacts (`analyst-lora-adapter/`, `week3_test_rows.json`) are picked
up if present; labeled fallbacks otherwise.

## Learning outcomes

By the end you can:
1. **Validate eval inputs before trusting eval outputs** (the frozen-set contract check).
2. **Size any model from its parameter count** — and confirm the prediction against `get_memory_footprint()`.
3. **Produce and compare three precision arms**, and explain why memory savings are guaranteed but speed is not (bitsandbytes dequant overhead on a T4).
4. **Benchmark honestly**: percentiles over runs, tokens/sec from actually-generated tokens.
5. **Run a two-metric quality gate** (format + content score) with a pre-committed threshold, and assemble the memory/latency/quality deliverable table.
6. **Write the GGUF export pipeline precisely** — including the `cmake` build step everyone forgets.

## Files

| File | What it is |
|---|---|
| `week4_assignment.ipynb` | **Start here.** 12 tasks with `...` placeholders + self-checks |
| `week4_assignment_solution.ipynb` | Reference implementation |

## How to work

1. GPU runtime. If you finished Week 3's assignment, its saved artifacts make this benchmark *your* model.
2. Parts 1–2 are quick; Task 9 is the slow cell (18 generations) — start it, then read ahead.
3. The final table prints from **your** measurements; that table plus the verdict line is the artifact to keep.

**Done when:** the three-arm table is filled, both quality deltas have a ✅/❌ verdict, and your
reflection answers when you'd ship a slower-but-smaller model anyway.

## Ties into

- **Live session notebook:** `../week4_distill_merge_quantize_ship.ipynb` · **Deck:** `../week4_concepts.pptx`
- **Graded increment 4:** same discipline on your real Analyst + $/1k economics + the assembled pipeline.
