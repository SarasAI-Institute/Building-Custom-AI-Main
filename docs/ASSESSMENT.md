# Practice and assessed evidence

The [capstone rubric](https://github.com/SarasAI-Institute/Building-Custom-AI-Capstone/blob/codex/competency-colab-refresh/RUBRICS.md) governs assessment. Practice tasks have no invented point total or extra pass threshold. All 24 criteria must be Met across five competencies. Review C1.1, C2.3, C3.2, C4.2 and C5.1 first in their respective modules.

| Module | This lab teaches | What to add in the capstone |
|---|---|---|
| 1 | Tokens/embeddings/attention, VLM calls, frozen split, valid/invalid metrics, prompts and resolution | Repair all three planted bugs; ≥40 test images/≥20 each; ≥3 prompts including few-shot; actual token observations; F1 improvement; ≥3 errors/borderline cases; ≥3 measured resolutions |
| 2 | Real reviews, practice catalogue, chunking, retrieval, citations, refusal, graph design, quality review | Four official docs unchanged + ≥2 authored linked docs; ≥100 real reviews; ≥20 pre-index gold/≥3 multi-hop; recall@1,2,4,8 and improvement at 4; ≥4 meaningful refusals/5 unsupported questions; both judge axes; measured upgrade beyond prefix |
| 3 | Teacher collection/review, split control, actual QLoRA train/save/reload, comparison and ablation | ≥150 real teacher pairs before filtering; ≥25 frozen held-out test rows; max train/test cosine ≤.90; actual dataset card, logs and adapter; independent stronger judge; wins/losses/ties and denominator; one-variable trained ablation using the same frozen test protocol |
| 4 | Distillation/parallelism/merging concepts, two compressed arms, frozen quality gate, speed/footprint/cost | Actual trained Stage 3 reference, frozen gate, ≥2 compressed arms, full comparison and measured limits; evidence-based accept/reject/fallback; standalone Module 4 checkpoint |
| 5 | Exact artifact handoff, product-aware evidence, real integration, batch traces | `analyze_product(image)` contract, ≥3 demos including GOOD and two DEFECTIVE, ≥10 real batch cases, failures, 100× traffic reasoning, clean saved-weight rerun, full ledger, ≤300-word reflection and written walkthrough/defense |

The Module 3 practice dataset is explicitly synthetic; it does not satisfy teacher-data evidence. Its small split and validation-based ablation illustrate engineering mechanics. The capstone requires the larger frozen evaluation and full judge comparison. A failed compression gate can support competent reasoning but is not a deployment approval.
