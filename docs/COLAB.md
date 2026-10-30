# Run in Colab and keep your work

## Start a new session
1. Open the notebook's Colab link and save a copy to your Drive. Choose **Runtime → Change runtime type → Python 3 / GPU** for model labs. A T4-class GPU is the target, not a guarantee of availability.
2. Run the setup cell **before** importing model libraries. It pins the course's user-space packages while constraining the existing matched PyTorch/torchvision installation. Do not independently upgrade CUDA wheels. If the resolver fails, stop and retain its message; do not continue in a mixed environment.
3. If the cell asks for a restart because model libraries were already imported, restart the session, then run from the top. GPU-dependent labs stop explicitly without CUDA. The small CPU examples are not substitutes for GPU measurements.
4. Read the configuration choices before **Run all**. Training, folding, external judges and artifact restores are intentional decisions, not hidden fallback actions. Download costs, disk use and runtime depend on the chosen models/data and available hardware. Never put tokens in a notebook; use Colab Secrets for optional authenticated Hub access.

The reviewed package set is in `scripts/runtime_setup.py`. The verification record distinguishes CPU execution, network probes and pending GPU work. Pins improve repeatability; they do not guarantee that every future Colab base image is compatible. Save the actual Python, torch, CUDA, GPU and package versions from your run.

## Continue across modules

| Module | Required input | Preserve for the next module |
|---|---|---|
| 1 | Public model and image dataset access | Image identities/split, development experiments, selected prompt, processor settings, exact model revision, full test outputs |
| 2 | Public real-review stream and practice specifications | Frozen corpus/gold, source provenance, embedding revision, chunk settings, retrieval/generation outputs |
| 3 | A deliberately selected practice or reviewed teacher dataset | Entire `analyst-lora-adapter/`, `analyst_data_split_v1.json`, dataset card, training/evaluation/ablation records |
| 4 | Actual Module 3 adapter, tokenizer, manifest and frozen split | `analyst-merged/`, complete `analyst_compression_v1/` including plan, all arms, gates, cost assumptions and human decision |
| 5 | All selected real components, applicable images, external product IDs | Config, source mapping, image manifest, complete pipeline trace, batch and human review files |

Keep these folders outside `/content` before ending the runtime. Either download them or copy them to a chosen Drive folder after mounting Drive yourself. Restore them into the working directory before running the next lab. Do not commit model weights, customer data, access tokens or measured personal artifacts into this teaching repository.

For a **first Module 3 run**, choose `TRAIN_MODE="train"`; reruns use `"load"` with the matching saved folder. For its optional ablation, choose the explicit new-run mode shown in that section. For a **first Module 4 fold**, choose `FOLD_MODE="create"`; reruns use `"load"`. Existing artifacts are protected against accidental replacement. Use a new run directory for a new experiment. Model resolution must use the saved base commit on reload, not whatever `main` points to later.

Module 4 evaluates the trained reference, folded half precision, folded INT8 and folded NF4 on the same frozen rows. INT8 and NF4 are the two compressed arms; half precision supplies the footprint denominator. The gate compares format percentage points and 100 × raw cosine difference, with human claim/severity/action review still required. Predeclare price/source, tolerances and intended arm. A missing price remains missing; it is not a free-GPU price assumption.

Module 5 requires a completed decision tied to the exact plan and checkpoint hashes. Set `decision` to `ACCEPT` or a justified `FALLBACK`, record `chosen_arm` and `chosen_artifact`, and complete human/runtime review. This lab's loader supports evaluated passing folded half/INT8/NF4 arms. If none is usable, stop and document the failure rather than label an untested artifact deployable. Other fallback architectures require their own validated loader.

## Common stops and recovery

- **Missing artifact:** restore the whole directory, including tokenizer, manifest and split; do not create an empty file to bypass the check.
- **Out of memory:** release old models/restart; use batch size 1 or a smaller documented workload and record the change. Do not silently compare different hardware or precision settings.
- **Dataset or Hub access error:** inspect the reported public URL/revision, retry later or preserve a downloaded snapshot. Do not replace real reviews with fabricated data and keep the original label.
- **Incomplete saved run:** keep its failures, inspect them and create a new named run. A partial result is not a successful benchmark.
- **Invalid generated JSON or report:** retain raw output as an error. A parser must not turn malformed output into a confident GOOD prediction.
- **Changed split/plan:** restore the intended snapshot or explicitly version a new experiment; never tune against the final test.

Primary runtime references: [Colab FAQ](https://research.google.com/colaboratory/faq.html), [Transformers installation](https://huggingface.co/docs/transformers/installation), [bitsandbytes requirements](https://huggingface.co/docs/bitsandbytes/installation), [TRL SFT](https://huggingface.co/docs/trl/sft_trainer). GPU availability and performance must be measured in the actual course runtime.
