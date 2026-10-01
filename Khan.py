import sys
import importlib.util
from pathlib import Path

ver = f"{sys.version_info.major}{sys.version_info.minor}"  # 310, 311, 313
so_file = Path(f"{ver}.so")

# exact version pehle try karo
candidates = [so_file, Path("310.so"), Path("311.so"), Path("313.so")]

for p in candidates:
    if p.exists():
        print(f"Trying {p} for Python {sys.version_info.major}.{sys.version_info.minor}")
        try:
            spec = importlib.util.spec_from_file_location("core", str(p))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            break
        except Exception as e:
            print(f"{p} failed: {e}")
            continue
else:
    print("Koi .so load nahi hua - python version check karo")
