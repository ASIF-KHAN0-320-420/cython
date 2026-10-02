#!/usr/bin/env python3

import sys
import subprocess
import importlib.util
import base64
from pathlib import Path

BASE = Path(__file__).resolve().parent

# ============================================================
# PASTE YOUR FULL PROFILE_B64 HERE
# ============================================================

PROFILE_B64 = """PASTE_YOUR_FULL_PROFILE_B64_HERE"""

# ============================================================

def run(cmd):
    subprocess.run(cmd, check=True)

def show_profile():
    try:
        image = BASE / ".profile.jpg"
        image.write_bytes(base64.b64decode(PROFILE_B64))

        if subprocess.run(
            ["sh", "-c", "command -v chafa >/dev/null 2>&1"]
        ).returncode == 0:
            subprocess.run([
                "chafa",
                "-s",
                "50x20",
                str(image)
            ])
        elif subprocess.run(
            ["sh", "-c", "command -v viu >/dev/null 2>&1"]
        ).returncode == 0:
            subprocess.run([
                "viu",
                "-w",
                "50",
                str(image)
            ])

        image.unlink(missing_ok=True)

    except Exception as e:
        print(f"Picture display error: {e}")

# Dependencies
run(["pkg", "update", "-y"])
run([
    "pkg", "install",
    "libjpeg-turbo",
    "libpng",
    "freetype",
    "zlib",
    "viu",
    "chafa",
    "-y"
])

run([
    sys.executable,
    "-m",
    "pip",
    "install",
    "--upgrade",
    "pip",
    "setuptools",
    "wheel"
])

run([
    sys.executable,
    "-m",
    "pip",
    "install",
    "--no-cache-dir",
    "Pillow"
])

run([
    sys.executable,
    "-c",
    "from PIL import Image; print('Pillow OK')"
])

# Show profile
if PROFILE_B64 != "PASTE_YOUR_FULL_PROFILE_B64_HERE":
    show_profile()

# Python version
PYVER = f"{sys.version_info.major}{sys.version_info.minor}"

SO_FILES = {
    "310": BASE / "RTRT11.cpython-310.so",
    "311": BASE / "RTTR111.cpython-311.so",
    "313": BASE / "TRRT11.cpython-313.so",
}

SO_FILE = SO_FILES.get(PYVER)

if SO_FILE is None:
    print(f"ERROR: Python {PYVER} supported nahi hai.")
    print("Supported: Python 3.10 / 3.11 / 3.13")
    sys.exit(1)

if not SO_FILE.exists():
    print(f"ERROR: {SO_FILE.name} nahi mili.")
    sys.exit(1)

MODULE_NAME = SO_FILE.name.split(".")[0]

try:
    spec = importlib.util.spec_from_file_location(
        MODULE_NAME,
        SO_FILE
    )

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
