"""Run this cell first in a fresh Colab session, before importing model libraries."""
import importlib.metadata as _metadata
import platform as _platform
import subprocess as _subprocess
import sys as _sys
import tempfile as _tempfile
from pathlib import Path as _Path

COURSE_PACKAGES = [
    "transformers==5.22.0", "trl==1.17.0", "peft==0.21.2",
    "accelerate==1.15.0", "datasets==5.1.0", "sentence-transformers==6.2.0",
    "faiss-cpu==1.15.1", "num2words==0.5.14",
    "pillow==13.0.0", "scikit-learn==1.9.1", "matplotlib==3.11.2", "requests==2.34.2",
]
if _sys.version_info < (3, 11):
    raise RuntimeError("Use a current Colab Python 3.11+ runtime.")
try:
    _torch_version = _metadata.version("torch")
except _metadata.PackageNotFoundError as _error:
    raise RuntimeError("Use Colab's preinstalled matched PyTorch/torchvision runtime; see docs/COLAB.md.") from _error
_constraints = ["torch==" + _torch_version]
try:
    _constraints.append("torchvision==" + _metadata.version("torchvision"))
except _metadata.PackageNotFoundError:
    raise RuntimeError("The vision labs need a matching torchvision installation; use a fresh Colab runtime.")
if _platform.system() == "Linux":
    COURSE_PACKAGES.append("bitsandbytes==0.50.2")
_before = {}
for _name in ["transformers", "trl", "peft", "datasets", "sentence_transformers", "numpy"]:
    if _name in _sys.modules:
        _before[_name] = getattr(_sys.modules[_name], "__version__", None)
with _tempfile.TemporaryDirectory() as _temporary:
    _constraint_file = _Path(_temporary) / "preserve-colab-torch.txt"
    _constraint_file.write_text("\n".join(_constraints))
    _subprocess.run([_sys.executable, "-m", "pip", "install", "--quiet", "--upgrade-strategy", "only-if-needed",
                     "-c", str(_constraint_file), *COURSE_PACKAGES], check=True)
if _before:
    raise RuntimeError("Packages installed. Restart the Colab session once, then run from the setup cell again before importing models.")
print("Course stack installed; existing PyTorch/torchvision CUDA wheels preserved.")
print("If installation failed, stop here. Start a fresh GPU runtime and inspect the resolver message.")
