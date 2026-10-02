
# Auto loader for TRRT1 - Built versions: 310, 311, 313
# Termux compatible - loads 310, 311, 313
import sys, importlib.util
from pathlib import Path
v=str(sys.version_info.major)+str(sys.version_info.minor)
# Try current python version first, then all built versions
for n in [f'{v}.so', "310.so", "311.so", "313.so"]:
    p=Path(__file__).parent/n
    if not p.exists(): p=Path(n)
    if p.exists():
        try:
            s=importlib.util.spec_from_file_location('TRRT1', str(p))
            m=importlib.util.module_from_spec(s)
            s.loader.exec_module(m)
            break
        except Exception as e:
            print(f'Fail {n}: {e}')
