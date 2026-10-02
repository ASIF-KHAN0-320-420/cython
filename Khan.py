#!/usr/bin/env python3

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent

print()
print("Starting Khan.py...")
print(f"Python: {sys.version.split()[0]}")
print()

# Current Python version
PYVER = f"{sys.version_info.major}{sys.version_info.minor}"

# Python version ke mutabiq SO
SO_FILES = {
    "313": BASE / "RTRT11.so",
    "311": BASE / "RTTR111.so",
    "310": BASE / "TRRT11.so",
}

SO_FILE = SO_FILES.get(PYVER)

if SO_FILE is None:
    print(f"ERROR: Python {PYVER} supported nahi hai.")
    print("Supported: Python 3.13 / 3.11 / 3.10")
    sys.exit(1)

if not SO_FILE.exists():
    print(f"ERROR: {SO_FILE.name} nahi mili.")
    print()
    print("Required file:")
    print(SO_FILE.name)
    sys.exit(1)

print(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")
print(f"Loading: {SO_FILE.name}")
print()

try:
    import TRRT11

    print("✓ TRRT11 loaded")
    print()

except Exception as e:
    print("✗ TRRT11 LOAD ERROR:")
    print(e)
    sys.exit(1)

try:
    TRRT11.main()

except KeyboardInterrupt:
    print("\nProgram stopped.")

except Exception as e:
    print("✗ PROGRAM ERROR:")
    print(e)
    sys.exit(1)
