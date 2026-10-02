import sys, importlib.util
from pathlib import Path
v=str(sys.version_info.major)+str(sys.version_info.minor)
# Try current python version first, then all built versions
for n in [f'{v}.so', "TRRT1310.so", "TRRT1311.so", "TRRT1313.so"]:
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
