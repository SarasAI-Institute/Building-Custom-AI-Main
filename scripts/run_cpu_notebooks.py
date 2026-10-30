"""Execute all worked CPU notebooks in clean temporary directories."""
from pathlib import Path
import tempfile
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
for path in sorted(ROOT.glob("modules/module*/solutions.ipynb")):
    with tempfile.TemporaryDirectory() as directory:
        notebook=nbformat.read(path,as_version=4)
        NotebookClient(notebook,timeout=120,kernel_name="python3",resources={"metadata":{"path":directory}}).execute()
    print(f"PASS {path.relative_to(ROOT)}")
