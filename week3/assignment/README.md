# Week 3 Assignment · Fine-Tune an Analyst — Data, Discipline, Proof

**Status:** ungraded practice · **Time:** ~75–90 min (incl. a few minutes of training) · **Compute:** GPU required (free T4 is enough)

## What this is

The live session's fine-tuning loop rebuilt by hand — **12 tasks in four parts** — with the
emphasis where professionals put it: the dataset and the eval, not the trainer call. You write
your **own** generator vocabulary (different from the lecture's, on purpose), certify your split
clean, train a QLoRA adapter, and prove the improvement with two independent metrics.

| Part | Tasks | What you build |
|---|---|---|
| 1 · Baseline first | 1–3 | the `chat()` helper · a strict **format checker** (with truth table) · the measured *before* |
| 2 · The dataset | 4–7 | your generator (≥4 products / ≥8 defects / ≥5 causes) · scale to 60 pairs · embedding dedup · **decontaminated** split |
| 3 · Training | 8–9 | LoRA config with **hand-computed trainable-parameter accounting** · the SFT run (paged optimizer, fp16/bf16 detection) |
| 4 · Proof | 10–12 | `disable_adapter()` A/B · a **blind win-rate judge with randomized A/B order** · save the artifacts Week 4 needs |

## Learning outcomes

By the end you can:
1. **Measure before training** — a deterministic format metric and a captured baseline.
2. **Design diverse synthetic data** and run the full hygiene chain: format compliance → dedup → split → decontamination (as an *action*, with a printed certificate).
3. **Configure LoRA knowingly**: r, alpha, target modules — and verify <5% trainable parameters by counting them yourself.
4. **Prove improvement honestly**: adapters-off comparison, plus a blind pairwise judge with randomized position (the fix most tutorials skip).
5. **Hand off artifacts**: adapter + frozen test set, the exact contract Week 4 consumes.

## Files

| File | What it is |
|---|---|
| `week3_assignment.ipynb` | **Start here.** 12 tasks with `...` placeholders + self-checks |
| `week3_assignment_solution.ipynb` | Reference implementation — your vocabulary *should* differ |

## How to work

1. GPU runtime mandatory (asserted). Run the given setup (4-bit base + report contract).
2. Parts gate each other: the format checker (Task 2) validates your generator (Task 4);
   the hygiene self-check must certify the split before Task 9 trains.
3. Training takes a few minutes — read the loss-curve note while it runs.
4. Don't skip Task 11's randomization — position bias is real and the caveat cell explains it.

**Done when:** the split certificate prints, training completes, both eval numbers exist, and
`analyst-lora-adapter/` + `week3_test_rows.json` are on disk (Week 4 picks them up automatically).

## Ties into

- **Live session notebook:** `../week3_finetuning_analyst_qlora.ipynb` · **Deck:** `../week3_concepts.pptx`
- **Graded increment 3:** full-size Analyst with teacher-generated data, dataset card, rubric + win-rate on the frozen set.
