#!/usr/bin/env python3

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent

print("Starting Khan.py...")

try:
    import TRRT11

    print("✓ TRRT11 loaded")
    print("Available:", dir(TRRT11))

except Exception as e:
    print("✗ LOAD ERROR:", e)
    sys.exit(1)

print("Khan.py finished loading.")
