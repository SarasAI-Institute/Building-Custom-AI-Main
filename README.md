# Build Custom AI · course labs

Build RiskLens across five modules: visual inspection → grounded retrieval → a trained Analyst → measured compression → an integrated, defensible system.

| Module | Model lab in Colab | CPU practice | Worked solutions |
|---|---|---|---|
| 1. Visual inspection | [Open lab](https://colab.research.google.com/github/SarasAI-Institute/Building-Custom-AI-Main/blob/codex/competency-colab-refresh/modules/module01/lab.ipynb) | [Practice](modules/module01/practice.ipynb) | [Solutions](modules/module01/solutions.ipynb) |
| 2. Grounded retrieval | [Open lab](https://colab.research.google.com/github/SarasAI-Institute/Building-Custom-AI-Main/blob/codex/competency-colab-refresh/modules/module02/lab.ipynb) | [Practice](modules/module02/practice.ipynb) | [Solutions](modules/module02/solutions.ipynb) |
| 3. Fine-tuning | [Open lab](https://colab.research.google.com/github/SarasAI-Institute/Building-Custom-AI-Main/blob/codex/competency-colab-refresh/modules/module03/lab.ipynb) | [Practice](modules/module03/practice.ipynb) | [Solutions](modules/module03/solutions.ipynb) |
| 4. Compression | [Open lab](https://colab.research.google.com/github/SarasAI-Institute/Building-Custom-AI-Main/blob/codex/competency-colab-refresh/modules/module04/lab.ipynb) | [Practice](modules/module04/practice.ipynb) | [Solutions](modules/module04/solutions.ipynb) |
| 5. Integration | [Open lab](https://colab.research.google.com/github/SarasAI-Institute/Building-Custom-AI-Main/blob/codex/competency-colab-refresh/modules/module05/lab.ipynb) | [Practice](modules/module05/practice.ipynb) | [Solutions](modules/module05/solutions.ipynb) |

## Start here

1. Read [Colab setup and saved-artifact handoffs](docs/COLAB.md).
2. Use the CPU practice for a quick local/Colab start, then follow the model lab in order. GPU labs download public models/data. Module 3 training and Module 4 folding require explicit first-run choices; Module 5 requires your actual evaluated components.
3. Check the [lesson map](docs/LESSON_MAP.md) for section/video placement.
4. Build your continuing assessed notebook in the [capstone repository](https://github.com/SarasAI-Institute/Building-Custom-AI-Capstone).

Practice is formative. Assessment uses five competencies and 24 Met / Not Yet criteria; there are no averaged weekly point grades here. See [practice-to-capstone alignment](docs/ASSESSMENT.md). A synthetic example or a mock integration test is not project evidence.

## What is maintained

`modules/module01`–`module05` hold the canonical labs. Each has `lab.ipynb`, `practice.ipynb`, `solutions.ipynb` and a short route guide. `templates/` holds explicit integration configuration schemas. `scripts/`, `tests/` and GitHub Actions validate notebooks and the evaluation contracts. Old `week1`–`week4` links redirect to these modules; [migration notes](docs/MIGRATION.md) explain the changes.

Read the [validation record](docs/VALIDATION.md) before assuming a hardware run has passed. It distinguishes executed CPU tests from model/API probes and the remaining T4 rehearsal. No paid API key or hosting subscription is required by the CPU exercises. Preserve your real artifacts outside Colab's temporary disk.

## Maintainer checks

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/check_notebooks.py
python scripts/run_cpu_notebooks.py
```

The optional `scripts/smoke_training.py` additionally needs the model libraries pinned in `scripts/runtime_setup.py` and a compatible local PyTorch installation. It trains and reloads a tiny random model on CPU to check current APIs; it makes no claim about Analyst quality or GPU quantization.
