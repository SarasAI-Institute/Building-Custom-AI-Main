import json, math, sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import risklens_support as s

def report(severity="MEDIUM"):
    return "## ROOT CAUSE ANALYSIS\n**Product:** X\n**Defect:** crack\n**Severity:** "+severity+"\n**Evidence:** [a] crack\n**Probable cause:** Unknown\n**Recommended action:** Inspect"

def test_report_contract():
    assert all(s.format_ok(report(x)) for x in ["LOW","MEDIUM","HIGH"])
    assert not s.format_ok(report("MED"))
    assert not s.format_ok(report()+"\n**Severity:** HIGH")
    assert not s.format_ok(None)

def test_input_roundtrip():
    text=s.make_input("A crack; cause unknown","[a] Observed crack")
    assert s.split_input({"input":text})==("A crack; cause unknown","[a] Observed crack")
    with pytest.raises(TypeError):s.make_input({},"x")
    with pytest.raises(ValueError):s.split_input({"input":"other"})

def test_freeze_detects_mutation_and_preserves_original(tmp_path):
    path=tmp_path/"freeze.json";first=s.freeze_record(path,{"ids":[1,2]})
    assert s.freeze_record(path,{"ids":[1,2]})==first
    with pytest.raises(ValueError):s.freeze_record(path,{"ids":[2,1]})
    assert json.loads(path.read_text())==first
    bad=dict(first);bad["payload"]={"ids":[3]};path.write_text(json.dumps(bad))
    with pytest.raises(ValueError):s.freeze_record(path,{"ids":[1,2]})

def test_ledger_preserves_strings_and_history(tmp_path,monkeypatch):
    monkeypatch.setattr(s,"METRICS_FILE",str(tmp_path/"metrics.json"))
    s.record_metrics("stage3",judge="real-id",win_rate="17/25")
    s.record_metrics("stage3",judge="real-id",win_rate="18/25")
    assert json.loads((tmp_path/"metrics.json").read_text())["stage3"]["win_rate"]=="18/25"
    history=[json.loads(x) for x in (tmp_path/"metrics_history.jsonl").read_text().splitlines()]
    assert history[0]["metrics"]["win_rate"]=="17/25" and len(history)==2
    with pytest.raises(ValueError):s.record_metrics("bad",value=float("nan"))
    assert len((tmp_path/"metrics_history.jsonl").read_text().splitlines())==2

def test_inspection_keeps_invalid_in_denominator():
    rows=[{"truth":"defective","prediction":"defective"},{"truth":"defective","prediction":"invalid"},{"truth":"good","prediction":"good"},{"truth":"good","prediction":"invalid"}]
    metrics=s.inspection_metrics(rows)
    assert metrics["accuracy"]==.5 and metrics["defect_f1"]==pytest.approx(2/3)
    assert metrics["invalid_count"]==2
    with pytest.raises(ValueError):s.inspection_metrics([])

def test_split_pixel_identity_and_counts():
    from PIL import Image
    images=[Image.new("RGB",(2,2),(i,0,0)) for i in range(44)]
    tests=[(x,"good" if i<20 else "defective") for i,x in enumerate(images[:40])]
    dev=[(x,"good") for x in images[40:]]
    assert s.validate_image_split(tests,dev)["test_counts"]=={"good":20,"defective":20}
    with pytest.raises(ValueError):s.validate_image_split(tests,[(images[0],"good")])
    with pytest.raises(ValueError):s.validate_image_split(tests[:-1],dev)

def test_recall_means_all_sources_and_keeps_hits():
    gold=[{"q":"q","sources":["a","b"]}]
    def retrieve(q,k):return [{"source":x,"text":x,"score":1.} for x in ["a","b"][:k]]
    table,rows=s.recall_table(retrieve,gold)
    assert table=={"recall@1":0.,"recall@2":1.,"recall@4":1.,"recall@8":1.}
    assert rows[1]["hits"][1]["text"]=="b"
    with pytest.raises(ValueError):s.recall_table(lambda q,k:[{"source":"a"}]*(k+1),gold)

def test_refusal_is_not_automatic_credit():
    result=s.refusal_diagnostic("I cannot answer. Your serial is 999 [fake].",[{"source":"a"}])
    assert result["phrase_match"] and result["unknown_citations"]==["fake"]
    assert result["meaningful_refusal"] is None and result["claim_support"] is None

@pytest.mark.parametrize("values",[[],[0],[float("inf")],[float("nan")],[True]])
def test_latency_rejects_bad_values(values):
    with pytest.raises(ValueError):s.latency_summary(values)

def test_latency_and_cost_units():
    result=s.latency_summary([1,2,3,4])
    assert result["p50_s"]==2.5 and result["p95_s"]==pytest.approx(3.85)
    assert s.cost_per_1000(2,.36)==pytest.approx(.2)
    assert s.cost_per_1000(2,.36,.5)==pytest.approx(.4)
    with pytest.raises(ValueError):s.cost_per_1000(2,None)

def test_quality_gate_boundary_and_rejection():
    reference={"format_rate":.9,"content_cosine":.8};gate={"max_format_drop_pts":5,"max_content_drop_pts":5}
    assert s.quality_gate(reference,{"format_rate":.85,"content_cosine":.75},gate)["verdict"]=="PASS"
    assert s.quality_gate(reference,{"format_rate":.849,"content_cosine":.8},gate)["verdict"]=="FAIL"
    with pytest.raises(ValueError):s.quality_gate(reference,{"format_rate":.8,"content_cosine":float("nan")},gate)
