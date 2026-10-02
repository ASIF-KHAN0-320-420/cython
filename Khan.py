#!/usr/bin/env python3

import sys
import subprocess
import importlib.util
from pathlib import Path

BASE = Path(__file__).resolve().parent

def run(cmd):
    subprocess.run(cmd, check=True)

run(["pkg", "update", "-y"])
run(["pkg", "install", "libjpeg-turbo", "libpng", "freetype", "zlib", "viu", "-y"])
run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
run([sys.executable, "-m", "pip", "install", "--no-cache-dir", "Pillow"])
run([sys.executable, "-c", "from PIL import Image; print('Pillow OK')"])

PYVER = f"{sys.version_info.major}{sys.version_info.minor}"

SO_FILES = {
    "310": BASE / "RTRT11.cpython-310.so",
    "311": BASE / "RTTR111.cpython-311.so",
    "313": BASE / "TRRT11.cpython-313.so",
}

SO_FILE = SO_FILES.get(PYVER)

if SO_FILE is None:
    print(f"ERROR: Python {PYVER} supported nahi hai.")
    sys.exit(1)

if not SO_FILE.exists():
    print(f"ERROR: {SO_FILE.name} nahi mili.")
    sys.exit(1)

MODULE_NAME = SO_FILE.name.split(".")[0]

try:
    spec = importlib.util.spec_from_file_location(MODULE_NAME, SO_FILE)

    if spec is None or spec.loader is None:
        raise ImportError("SO loader create nahi hua")

    MODULE = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = MODULE
    spec.loader.exec_module(MODULE)

except Exception as e:
    print(f"✗ {MODULE_NAME} LOAD ERROR: {e}")
    sys.exit(1)

try:
    if not hasattr(MODULE, "main"):
        print(f"✗ {MODULE_NAME}.main() nahi mila")
        sys.exit(1)

    MODULE.main()

except KeyboardInterrupt:
    print("\nProgram stopped.")

except Exception as e:
    print(f"✗ PROGRAM ERROR: {e}")
    sys.exit(1)
