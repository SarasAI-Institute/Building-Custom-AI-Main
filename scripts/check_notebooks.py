"""Validate every notebook and local Markdown link without executing learner TODOs."""
from pathlib import Path
import ast, json, re
import nbformat
ROOT=Path(__file__).resolve().parents[1]
errors=[];code_count=0
for path in sorted(ROOT.rglob("*.ipynb")):
    if any(x in path.parts for x in [".git",".venv","artifacts"]): continue
    nb=nbformat.read(path,as_version=4)
    try:nbformat.validate(nb)
    except Exception as exc: errors.append(f"{path}: {exc}")
    for index,cell in enumerate(nb.cells):
        if cell.cell_type=="code":
            code_count+=1
            try:ast.parse(cell.source)
            except SyntaxError as exc:errors.append(f"{path} cell {index}: {exc}")
            if cell.get("outputs") or cell.get("execution_count") is not None:
                errors.append(f"{path} cell {index}: committed execution output")
        else:
            for target in re.findall(r"\[[^]]*\]\(([^)]+)\)",cell.source):
                if target.startswith(("https:","http:","#","mailto:")):continue
                if not (path.parent/target.split("#")[0]).exists():errors.append(f"Broken link in {path}: {target}")
for path in ROOT.rglob("*.md"):
    for target in re.findall(r"\[[^]]*\]\(([^)]+)\)",path.read_text()):
        if target.startswith(("https:","http:","#","mailto:")):continue
        if not (path.parent/target.split("#")[0]).exists():errors.append(f"Broken link in {path}: {target}")
if errors:raise SystemExit("\n".join(errors))
print(f"Notebook schema, {code_count} Python cells, clean outputs and local links passed")
