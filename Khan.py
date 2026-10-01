import sys,importlib.util as u
from pathlib import Path as P
v=f"{sys.version_info.major}{sys.version_info.minor}"
for n in [f"{v}.so","310.so","311.so","313.so"]:
 p=P(n)
 if p.exists():
  try: s=u.spec_from_file_location("k",str(p));m=u.module_from_spec(s);s.loader.exec_module(m);break
  except:pass
