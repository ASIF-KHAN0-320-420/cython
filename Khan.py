import sys
import platform
import importlib.util
from pathlib import Path

BASE = Path(__file__).resolve().parent

pyver = f"{sys.version_info.major}{sys.version_info.minor}"
arch = platform.machine()

so_name = f"TRRT11.cpython-{pyver}-{arch}-linux-android.so"
so_path = BASE / so_name

if not so_path.exists():
    raise RuntimeError(
        f"Python {pyver} ke liye matching module nahi mila: {so_name}"
    )

spec = importlib.util.spec_from_file_location("TRRT11", so_path)

if spec is None or spec.loader is None:
    raise ImportError(f"SO load nahi ho saki: {so_name}")

TRRT11 = importlib.util.module_from_spec(spec)
sys.modules["TRRT11"] = TRRT11
spec.loader.exec_module(TRRT11)

print(f"✓ TRRT11 loaded | Python {pyver}")
