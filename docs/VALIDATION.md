# Validation record · 30 October 2026

This record separates executable checks from full GPU acceptance. No test output is invented or included as learner evidence.

## Executed in an isolated local environment

- Python 3.12.14 on macOS ARM64; no CUDA device available.
- 23 teaching-repository CPU tests and 19 capstone CPU tests passed. Tests exercise actual notebook helper functions, frozen manifests, invalid predictions, strict report format, retrieval metrics, refusal diagnostics, timing/cost/gates and integration routing/failure cases.
- All five worked CPU notebooks (20 exercises) executed from clean kernels without errors. Notebook schemas, 184 code cells and local documentation links passed structural checks.
- The actual Module 2 loader streamed 120 real reviews at dataset revision `2b6d039ed471f2ba5fd2acb718bf33b0a7e5598e`, with source row and product provenance retained.
- Current model libraries imported successfully: torch 2.15.0, torchvision 0.29.2, transformers 5.22.0, TRL 1.17.0, PEFT 0.21.2, accelerate 1.15.0, datasets 5.1.0, sentence-transformers 6.2.0, faiss-cpu 1.15.1.
- Real CPU SFT of a tiny randomly initialized Qwen2 with LoRA completed one step; two trainable parameter tensors changed. Saved and freshly reloaded adapter produced matching logits and generated token IDs. This checks the current trainer/tokenizer/PEFT API path, not pretrained quality, 4-bit training or T4 memory.
- The public SmolVLM-256M-Instruct processor/model loaded at revision `7e3e67edbbed1bf9888184d9df282b700a323964` and generated five new tokens on CPU from a synthetic image. This verifies the small fallback path, not the 2.2B model or defect accuracy.
- BGE-small-en-v1.5 at revision `5c38ec7c405ec4b44b94cc5a9bb96e735b38267a` embedded the actual practice inputs. Deduplication retained 40 of 140 rows; the split retained 22 train / 6 validation / 12 test. Maximum train/test cosine was 0.8938393208179619. These are practice results, not the capstone's ≥150 teacher/≥25 test evidence.
- Public model and dataset revision endpoints resolved. The MVTec mirror contained 209 training GOOD bottle images and 63 defective test bottle images; a downloaded image decoded as 900×900 RGB.
- All 24 consolidated rubric Met descriptions were compared with their module PDFs and matched. Seven supplied reference PDFs are retained unchanged with SHA-256 hashes.

## Required GPU acceptance before calling the whole model path validated

Use a fresh Colab GPU runtime, record the hardware and exact installed versions, then save genuine outputs for these checks:

1. Run setup with the existing matched torch/torchvision wheels. Exercise the 2.2B VLM on real images; verify parsing, frozen split, all prompts and three actual processor resolutions.
2. Run review retrieval and grounded generation, including unknown-citation and unsupported-question cases.
3. Train the actual 1.5B NF4 QLoRA Analyst, inspect nonignored labels, save/reload and compare baseline/tuned outputs. Run the one-variable ablation and an independent stronger judge for assessed evidence.
4. Restore the exact artifact, fold it, load the Stage 3 reference plus half/INT8/NF4 arms sequentially, and measure quality, allocation, real generated tokens, p50/p95 and cost assumptions. Verify failures and the fallback decision.
5. Keep the VLM resident with the chosen Analyst; run actual integrated cases and ≥10 real batch examples, including GOOD short-circuit, malformed output, missing evidence and failure records. Verify clean-runtime restoration from saved weights.

This environment cannot certify Colab T4 memory, CUDA/bitsandbytes kernels, a complete learner submission or production latency. The repository includes CI for CPU/structural checks; it does not silently claim GPU CI. Practice TODO cells and assessed starter TODOs intentionally stop until completed.

## Reproduce

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/check_notebooks.py
```

In the teaching repository additionally run `python scripts/run_cpu_notebooks.py`; install the pinned model stack before `python scripts/smoke_training.py`. Network-dependent probes require public Hub access. See `docs/COLAB.md` for the actual runtime and artifact procedure.

Course placement uses the saved 29 October Monday mapping. A fresh live board read on 30 October was unavailable because the desktop browser was locked/disconnected. Assessment content uses the supplied official v2.0 files.
