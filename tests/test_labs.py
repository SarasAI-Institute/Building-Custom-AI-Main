"""Execute actual notebook functions with deterministic fixtures; no model mocks imply model quality."""
from pathlib import Path
import ast, json, random, re, math, time
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
def functions(module,names,extra=None):
    nb=json.loads((ROOT/f"modules/module{module:02d}/lab.ipynb").read_text())
    nodes=[]
    for c in nb["cells"]:
        if c["cell_type"]=="code":
            nodes.extend(n for n in ast.parse("".join(c["source"])).body if isinstance(n,ast.FunctionDef) and n.name in names)
    assert {n.name for n in nodes}==set(names)
    scope={"np":np,"random":random,"re":re,"math":math,"json":json,"time":time,"Path":Path,"SIM_THRESHOLD":.9}
    scope.update(extra or {})
    exec(compile(ast.Module(body=nodes,type_ignores=[]),"notebook_functions","exec"),scope)
    return scope

def test_actual_chunk_boundaries_and_empty():
    f=functions(2,["chunk"])["chunk"]
    rows=f(" ".join(map(str,range(13))),"a",5,2)
    assert [(x["start_word"],x["end_word"]) for x in rows]==[(0,5),(3,8),(6,11),(9,13)]
    assert f("","a")==[]
    with pytest.raises(ValueError):f("x","a",5,5)

def test_actual_all_source_metric():
    f=functions(2,["source_scores"])["source_scores"]
    assert f(["a","b"],[{"source":"a"}])["all_source_success"]==0
    assert f(["a","b"],[{"source":"a"}])["source_recall"]==.5
    assert f([],[])["source_recall"] is None

def test_actual_dedup_and_frozen_splits():
    f=functions(3,["deduplicate_rows","prepare_splits"])
    rows=[{"row_id":str(i),"seed_id":str(i)} for i in range(40)]
    kept,vectors,dropped=f["deduplicate_rows"](rows,np.eye(40))
    split=f["prepare_splits"](kept,vectors)
    assert len(split["test"])==12 and len(split["train"])>=15
    assert set(x["row_id"] for x in split["train"]).isdisjoint(x["row_id"] for x in split["test"])
    assert split["maximum_cosines"]["train_test"]==0
    kept,_,dropped=f["deduplicate_rows"](rows[:2],np.array([[1.,0.],[1.,0.]]))
    assert len(kept)==1 and dropped[0]["row_id"]=="1"

def test_actual_format_agrees_across_modules():
    from risklens_support import REQUIRED_SECTIONS,format_ok
    from test_support import report
    for module in [3,4,5]:
        f=functions(module,["format_ok"],{"REQUIRED":REQUIRED_SECTIONS})["format_ok"]
        for text in [report(),report("MED"),report()+"\n**Severity:** HIGH",None]:assert f(text)==format_ok(text)

def test_actual_inspection_parser():
    f=functions(5,["parse_inspection"])["parse_inspection"]
    assert f('{"verdict":"GOOD","defect_type":null,"description":"No crack visible."}')["parse_status"]=="valid"
    assert f('{"verdict":"DEFECTIVE","defect_type":null,"description":"Crack"}')["verdict"]=="PARSE_ERROR"
    assert f("bad output")["raw"]=="bad output"

def test_actual_pipeline_routes_and_preserves_errors():
    calls=[]
    scope=functions(5,["make_input","analyze_product_trace","analyze_product"],{
        "sync":lambda:None,"CONFIG":{"retrieval_k":4},"analyst_4bit":object(),"format_ok":lambda text:True})
    scope["inspect"]=lambda image:{"verdict":"GOOD","description":"fixture","defect_type":None}
    scope["retrieve"]=lambda *args:calls.append("retrieve") or [{"source":"a","text":"fixture evidence"}]
    scope["chat"]=lambda *args:calls.append("analyst") or {"text":"fixture report"}
    image=type("Image",(),{"info":{"product_id":"A"}})()
    result=scope["analyze_product"](image)
    assert calls==[] and result["evidence"]==result["report"]=="" and result["note"]["verdict"]=="GOOD"
    scope["inspect"]=lambda image:{"verdict":"DEFECTIVE","description":"visible crack","defect_type":"crack"}
    result=scope["analyze_product"](image)
    assert calls==["retrieve","analyst"] and result["evidence"]=="[a] fixture evidence"
    assert "Defect note from visual inspection" in result["trace"]["analyst_input"]
    scope["retrieve"]=lambda *args:[]
    result=scope["analyze_product"](image)
    assert result["trace"]["status"]=="no_matching_evidence" and result["report"]==""
    def fail(image):raise RuntimeError("fixture failure")
    scope["inspect"]=fail
    result=scope["analyze_product"](image)
    assert result["trace"]["status"]=="runtime_error" and "fixture failure" in result["trace"]["error"]

def test_actual_benchmark_counts_new_ids():
    f=functions(4,["latency_summary"])["latency_summary"]
    records=[{"status":"ok","seconds":2,"new_tokens_including_eos":3},{"status":"ok","seconds":1,"new_tokens_including_eos":2}]
    assert f(records)["generated_tokens_per_s"]==pytest.approx(5/3)
    with pytest.raises(ValueError):f([{"status":"generation_error"}])

def test_actual_gate_rejects_incomplete_candidate():
    f=functions(4,["practice_gate"])["practice_gate"]
    reference={"complete_generation":True,"mean_cosine_proxy":.8,"format_rate":.9}
    gate={"max_format_drop_pts":5,"max_content_drop_pts":5}
    assert f(reference,{**reference,"format_rate":.85},gate)["passes"]
    assert not f(reference,{**reference,"complete_generation":False},gate)["passes"]
