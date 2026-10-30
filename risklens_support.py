"""Given evidence utilities for RiskLens. These helpers do not grade competencies.

This module is also embedded in the starter so a saved Colab copy is standalone.
Only standard-library imports belong here; model execution remains in the notebook.
"""

import hashlib
import json
import math
import re
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_SECTIONS = [
    "## ROOT CAUSE ANALYSIS", "**Product:**", "**Defect:**", "**Severity:**",
    "**Evidence:**", "**Probable cause:**", "**Recommended action:**",
]
REFUSAL_PHRASES = [
    "don't have enough information", "do not have enough information",
    "not enough information", "cannot answer",
]
METRICS_FILE = "capstone_metrics.json"


def stable_hash(value):
    """Hash JSON data; NaN and infinity are never valid evidence values."""
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(payload.encode()).hexdigest()


def write_json(path, value):
    """Replace a JSON file atomically after serializability validation."""
    text = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(target)


def freeze_record(path, payload):
    """Create once or verify identical content; never silently rewrite a frozen plan.

    A local timestamp supports record keeping, not independent proof of chronology.
    Preserve a dated notebook snapshot or version history as required by the rubric.
    """
    target = Path(path)
    digest = stable_hash(payload)
    if target.exists():
        record = json.loads(target.read_text())
        if record.get("sha256") != digest or stable_hash(record["payload"]) != digest:
            raise ValueError(f"Frozen record differs: {target}. Preserve it and use a new version.")
        return record
    record = {"created_utc": datetime.now(timezone.utc).isoformat(),
              "sha256": digest, "payload": payload}
    write_json(target, record)
    return record


def record_metrics(stage, **metrics):
    """Keep a latest view and an append-only JSONL history, including judge/count strings."""
    if not isinstance(stage, str) or not stage.strip():
        raise ValueError("A nonempty stage key is required")
    stable_hash(metrics)  # Validate before touching either file.
    path = Path(METRICS_FILE)
    previous = json.loads(path.read_text()) if path.exists() else {}
    entry = {"stage": stage, "recorded_utc": datetime.now(timezone.utc).isoformat(),
             "metrics": metrics}
    history = path.with_name(path.stem + "_history.jsonl")
    history.parent.mkdir(parents=True, exist_ok=True)
    with history.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False, allow_nan=False) + "\n")
    previous[stage] = metrics
    write_json(path, previous)
    print(f"Recorded {stage}; retain the ledger history and full experiment outputs.")


def show_ledger():
    path = Path(METRICS_FILE)
    print(path.read_text() if path.exists() else "No measured stage has been recorded yet.")


def make_input(defect_note, evidence):
    if not isinstance(defect_note, str) or not isinstance(evidence, str):
        raise TypeError("The Analyst expects a prose note and evidence string, not a dict.")
    return (f"Defect note from visual inspection:\n{defect_note}\n\n"
            f"Retrieved evidence:\n{evidence}\n\nWrite a root cause analysis report.")


def split_input(row):
    text = row["input"]
    prefix = "Defect note from visual inspection:\n"
    separator = "\n\nRetrieved evidence:\n"
    suffix = "\n\nWrite a root cause analysis report."
    if not isinstance(text, str) or not text.startswith(prefix) or not text.endswith(suffix):
        raise ValueError("Input does not follow make_input()")
    body = text[len(prefix):-len(suffix)]
    if separator not in body:
        raise ValueError("Missing evidence boundary")
    return tuple(body.split(separator, 1))


def format_ok(text):
    """Mechanical format only: all headers and one exact LOW/MEDIUM/HIGH severity line."""
    if not isinstance(text, str) or not all(h in text for h in REQUIRED_SECTIONS):
        return False
    lines = re.findall(r"(?m)^\*\*Severity:\*\*[^\n]*$", text)
    return len(lines) == 1 and bool(re.fullmatch(
        r"\*\*Severity:\*\*[ \t]*(LOW|MEDIUM|HIGH)[ \t]*", lines[0]))


def image_id(image):
    """Pixel identity independent of a temporary Colab/cache file path."""
    rgb = image.convert("RGB")
    h = hashlib.sha256(f"RGB:{rgb.size}".encode())
    h.update(rgb.tobytes())
    return h.hexdigest()


def validate_image_split(test_images, dev_images):
    """Check counts, duplicate pixels and overlap; timing still needs version evidence."""
    def describe(rows):
        ids, counts = [], {"good": 0, "defective": 0}
        for image, label in rows:
            if label not in counts:
                raise ValueError(f"Unknown image label {label!r}")
            ids.append(image_id(image)); counts[label] += 1
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate image pixels within a split")
        return ids, counts
    test_ids, test_counts = describe(test_images)
    dev_ids, dev_counts = describe(dev_images)
    if len(test_ids) < 40 or min(test_counts.values()) < 20:
        raise ValueError("C1.1 needs at least 40 test images and 20 per class")
    if not dev_ids or set(test_ids) & set(dev_ids):
        raise ValueError("A nonempty separate development set is required")
    return {"test_ids": test_ids, "dev_ids": dev_ids,
            "test_counts": test_counts, "dev_counts": dev_counts}


def inspection_metrics(records):
    """Defective is positive. Invalid predictions stay in accuracy and the 2x3 matrix."""
    if not records:
        raise ValueError("Cannot evaluate an empty image set")
    for row in records:
        if row["truth"] not in {"good", "defective"}:
            raise ValueError("Unknown truth label")
        if row["prediction"] not in {"good", "defective", "invalid"}:
            raise ValueError("Unknown prediction label")
    tp = sum(r["truth"] == "defective" and r["prediction"] == "defective" for r in records)
    fp = sum(r["truth"] == "good" and r["prediction"] == "defective" for r in records)
    fn = sum(r["truth"] == "defective" and r["prediction"] != "defective" for r in records)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {"n": len(records), "accuracy": sum(r["truth"] == r["prediction"] for r in records) / len(records),
            "defect_precision": precision, "defect_recall": recall,
            "defect_f1": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0,
            "invalid_count": sum(r["prediction"] == "invalid" for r in records),
            "confusion_rows_good_defective_columns_good_defective_invalid": [
                [sum(r["truth"] == t and r["prediction"] == p for r in records)
                 for p in ["good", "defective", "invalid"]] for t in ["good", "defective"]]}


def validate_corpus_gold(corpus, gold, official_docs):
    if len({d["source"] for d in corpus}) != len(corpus):
        raise ValueError("Corpus source IDs must be unique before chunking")
    by_id = {d["source"]: d for d in corpus}
    if sum(d.get("kind") == "review" for d in corpus) < 100:
        raise ValueError("C2.1 requires at least 100 real reviews")
    for doc in official_docs:
        if doc["source"] not in by_id or by_id[doc["source"]]["text"] != doc["text"]:
            raise ValueError("Official CAPSTONE_DOCS must be present verbatim")
    if sum(d.get("kind") == "doc" and d["source"] not in {o["source"] for o in official_docs}
           for d in corpus) < 2:
        raise ValueError("At least two authored documents are required")
    if len(gold) < 20 or len({g["q"] for g in gold}) != len(gold):
        raise ValueError("At least 20 distinct gold questions are required")
    for g in gold:
        if not g.get("sources") or not set(g["sources"]) <= set(by_id) or not g.get("ref"):
            raise ValueError("Every gold question needs valid source IDs and a reference")
        if g.get("multihop") and len(set(g["sources"])) < 2:
            raise ValueError("A multi-hop question requires at least two source IDs")
    if sum(bool(g.get("multihop")) for g in gold) < 3:
        raise ValueError("At least three multi-hop questions are required")
    return {"n_corpus": len(corpus), "n_gold": len(gold),
            "manual_checks": ["real review provenance", "authored facts and link", "multi-hop meaning"]}


def recall_table(retrieve_fn, gold):
    """RiskLens recall@k = fraction of questions with ALL required sources retrieved."""
    if not gold or any(not g.get("sources") for g in gold):
        raise ValueError("Nonempty gold questions and required-source sets are needed")
    table, records = {}, []
    for k in [1, 2, 4, 8]:
        successes = 0
        for g in gold:
            hits = retrieve_fn(g["q"], k)
            if len(hits) > k:
                raise ValueError("Retriever returned more than k hits")
            found = {h["source"] for h in hits}
            complete = set(g["sources"]) <= found
            successes += complete
            records.append({"q": g["q"], "k": k, "required_sources": g["sources"],
                            "hits": hits, "all_required_found": complete})
        table[f"recall@{k}"] = successes / len(gold)
    return table, records


def refusal_diagnostic(answer, hits):
    """Flag phrase/citation syntax; a human must judge support and refusal meaning."""
    if not isinstance(answer, str):
        raise TypeError("Answer must be text")
    cited = re.findall(r"\[([A-Za-z0-9_.:-]+)\]", answer)
    available = {h["source"] for h in hits}
    return {"phrase_match": any(p in answer.lower() for p in REFUSAL_PHRASES),
            "unknown_citations": sorted(set(cited) - available),
            "meaningful_refusal": None, "claim_support": None}


def latency_summary(seconds):
    if not seconds or any(isinstance(x, bool) or not math.isfinite(x) or x <= 0 for x in seconds):
        raise ValueError("Nonempty finite positive durations required")
    ordered = sorted(seconds)
    def percentile(q):
        position = (len(ordered) - 1) * q
        lower = math.floor(position); upper = math.ceil(position)
        return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)
    return {"n_runs": len(seconds), "mean_s": statistics.mean(seconds),
            "p50_s": percentile(.5), "p95_s": percentile(.95), "percentile_method": "linear",
            "sample_limit": "Descriptive sample percentiles, not a production SLA"}


def bench(fn, arg, n_runs=6, warmups=1, synchronize=None):
    """Measure completed calls; pass torch.cuda.synchronize for CUDA workloads."""
    if type(n_runs) is not int or n_runs < 1 or type(warmups) is not int or warmups < 0:
        raise ValueError("Positive run count and nonnegative warm-up count required")
    sync = synchronize or (lambda: None)
    for _ in range(warmups):
        fn(arg); sync()
    times = []
    for _ in range(n_runs):
        sync(); started = time.perf_counter(); fn(arg); sync()
        times.append(time.perf_counter() - started)
    return {**latency_summary(times), "observations_s": times, "warmups": warmups}


def cost_per_1000(mean_seconds, hourly_price, utilization=1.0):
    values = [mean_seconds, hourly_price, utilization]
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in values):
        raise ValueError("Finite explicit time, price and utilization are required")
    if mean_seconds < 0 or hourly_price < 0 or not 0 < utilization <= 1:
        raise ValueError("Nonnegative time/price and utilization in (0,1] required")
    return mean_seconds * hourly_price * 1000 / (3600 * utilization)


def quality_gate(reference, candidate, gate):
    """Compare unrounded rates; content uses cosine x100 units, not factual accuracy."""
    values = [reference[k] for k in ["format_rate", "content_cosine"]]
    values += [candidate[k] for k in ["format_rate", "content_cosine"]]
    values += [gate[k] for k in ["max_format_drop_pts", "max_content_drop_pts"]]
    if any(isinstance(x, bool) or not isinstance(x, (float, int)) or not math.isfinite(x) for x in values):
        raise ValueError("All gate measurements and tolerances must be finite numbers")
    if any(not 0 <= arm["format_rate"] <= 1 or not -1 <= arm["content_cosine"] <= 1
           for arm in [reference, candidate]) or min(values[-2:]) < 0:
        raise ValueError("Invalid rate, cosine or negative tolerance")
    fmt = 100 * (reference["format_rate"] - candidate["format_rate"])
    content = 100 * (reference["content_cosine"] - candidate["content_cosine"])
    passed = fmt <= gate["max_format_drop_pts"] + 1e-9 and content <= gate["max_content_drop_pts"] + 1e-9
    return {"format_drop_pts": fmt, "content_drop_pts": content,
            "verdict": "PASS" if passed else "FAIL"}
