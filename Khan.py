#!/usr/bin/env python3

import sys
import platform
import importlib.util
from pathlib import Path

BASE = Path(__file__).resolve().parent

PYVER = f"{sys.version_info.major}{sys.version_info.minor}"
ARCH = platform.machine()

print()
print(f"Python  : {sys.version.split()[0]}")
print(f"Version : {PYVER}")
print(f"Arch    : {ARCH}")
print()

# Python version ke mutabiq possible .so files
candidates = [
    BASE / f"TRRT11.cpython-{PYVER}-{ARCH}-linux-android.so",
    BASE / f"TRRT11.cpython-{PYVER}.so",
    BASE / f"RTRT11.cpython-{PYVER}-{ARCH}-linux-android.so",
    BASE / f"RTRT11.cpython-{PYVER}.so",
]

so_path = None

for file in candidates:
    if file.exists():
        so_path = file
        break

if so_path is None:
    print("ERROR: Matching .so file nahi mili.")
    print()
    print("Repository mein available .so files:")

    for file in sorted(BASE.glob("*.so")):
        print(f"  {file.name}")

    print()
    print(f"Python {PYVER} ke liye compatible file chahiye.")
    sys.exit(1)

# Filename se actual extension-module name
module_name = so_path.name.split(".cpython-", 1)[0]

print(f"SO      : {so_path.name}")
print(f"Module  : {module_name}")
print()

try:
    spec = importlib.util.spec_from_file_location(
        module_name,
        so_path
    )

    if spec is None or spec.loader is None:
        raise ImportError("Python loader create nahi kar saka.")

    module = importlib.util.module_from_spec(spec)

    sys.modules[module_name] = module

    spec.loader.exec_module(module)

    print(f"✓ {so_path.name} successfully loaded")
    print(f"✓ Module: {module_name}")

except Exception as e:
    print("SO LOAD ERROR:")
    print(e)
    sys.exit(1)
