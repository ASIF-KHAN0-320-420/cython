import sys, importlib.util as u
from pathlib import Path as P
print(f"Your Python: {sys.version}")
v=f"{sys.version_info.major}{sys.version_info.minor}"
print(f"Looking for: {v}.so")
for n in [f"{v}.so","310.so","311.so","313.so"]:
 p=P(n)
 if p.exists():
  print(f"Found {n}, trying to load...")
  try:
   s=u.spec_from_file_location("k",str(p))
   m=u.module_from_spec(s)
   s.loader.exec_module(m)
   print(f"Loaded {n} OK")
   break
  except Exception as e:
   print(f"Error in {n}: {e}")
 else:
  print(f"{n} not found")
else:
 print("No .so loaded!")
 print("Check: python --version")
 print("You need .so for your version")
