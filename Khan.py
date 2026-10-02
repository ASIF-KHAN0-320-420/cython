#!/usr/bin/env python3

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent

print()
print("Starting Khan.py...")

SO_FILE = BASE / "TRRT11.so"

if not SO_FILE.exists():
    print(f"ERROR: {SO_FILE.name} nahi mili")
    sys.exit(1)

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
