import sys, importlib.util
from pathlib import Path
v=f"{sys.version_info.major}{sys.version_info.minor}"
for n in [f"{v}.so","310.so","311.so","313.so"]:
 p=Path(n)
 if p.exists():
  try:
   s=importlib.util.spec_from_file_location("k",str(p))
   m=importlib.util.module_from_spec(s)
   s.loader.exec_module(m)
   break
  except: pass
