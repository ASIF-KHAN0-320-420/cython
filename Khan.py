#!/usr/bin/env python3

import sys
import importlib.util
from pathlib import Path

BASE = Path(__file__).resolve().parent

print()
print("Starting Khan.py...")
print(f"Python: {sys.version.split()[0]}")
print()

PYVER = f"{sys.version_info.major}{sys.version_info.minor}"

SO_FILES = {
    "310": BASE / "RTRT11.cpython-310.so",
    "311": BASE / "RTTR111.cpython-311.so",
    "313": BASE / "TRRT11.cpython-313.so",
}

SO_FILE = SO_FILES.get(PYVER)

if SO_FILE is None:
    print(f"ERROR: Python {PYVER} supported nahi hai.")
    print("Supported: Python 3.13 / 3.11 / 3.10")
    sys.exit(1)

if not SO_FILE.exists():
    print(f"ERROR: {SO_FILE.name} nahi mili.")
    sys.exit(1)

print(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")
print(f"Loading: {SO_FILE.name}")
print()

try:
    spec = importlib.util.spec_from_file_location(
        "TRRT11",
        SO_FILE
    )

    if spec is None or spec.loader is None:
        raise ImportError("SO loader create nahi hua")

    TRRT11 = importlib.util.module_from_spec(spec)
    sys.modules["TRRT11"] = TRRT11
    spec.loader.exec_module(TRRT11)

    print("✓ TRRT11 loaded")
    print()

except Exception as e:
    print("✗ TRRT11 LOAD ERROR:")
    print(e)
    sys.exit(1)

try:
    if not hasattr(TRRT11, "main"):
        print("✗ TRRT11.main() nahi mila")
        sys.exit(1)

    TRRT11.main()

except KeyboardInterrupt:
    print("\nProgram stopped.")

except Exception as e:
    print("✗ PROGRAM ERROR:")
    print(e)
    sys.exit(1)
