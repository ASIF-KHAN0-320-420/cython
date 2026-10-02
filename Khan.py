import sys
import os
import base64
import shutil
import subprocess
import importlib.util
from pathlib import Path

BASE = Path(__file__).resolve().parent

R = "\033[0m"
W = "\033[97m"
G = "\033[92m"
Y = "\033[93m"

# ============================================================
# PASTE / KEEP YOUR EXISTING PROFILE_B64 HERE
# ============================================================

PROFILE_B64 = r"""
PASTE_YOUR_EXISTING_PROFILE_B64_HERE
"""

# ============================================================
# INSTALL IMAGE VIEWER
# ============================================================

def install_viewer():
    try:
        if shutil.which("chafa") or shutil.which("viu"):
            return

        print(f"{Y}Installing image viewer...{R}")

        subprocess.run(
            ["pkg", "install", "chafa", "viu", "-y"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

    except Exception:
        pass


# ============================================================
# SHOW PROFILE IMAGE
# ============================================================

def show_profile():
    image_file = BASE / ".khan_profile.jpg"

    try:
        data = "".join(PROFILE_B64.split())

        if not data or "PASTE_YOUR_EXISTING" in data:
            print(f"{Y}PROFILE_B64 missing hai.{R}")
            return

        raw = base64.b64decode(data, validate=False)

        if not raw.startswith(b"\xff\xd8"):
            print(f"{Y}Profile image JPEG nahi hai.{R}")
            return

        image_file.write_bytes(raw)

        print()
        print(f"{W}Loading profile...{R}")
        print()

        # CHAfA first
        if shutil.which("chafa"):
            result = subprocess.run(
                [
                    "chafa",
                    "--format", "symbols",
                    "--size", "50x20",
                    str(image_file)
                ],
                check=False
            )

            if result.returncode == 0:
                print()
                return

        # VIU fallback
        if shutil.which("viu"):
            subprocess.run(
                [
                    "viu",
                    "-w", "50",
                    str(image_file)
                ],
                check=False
            )

            print()
            return

        print(f"{Y}chafa/viu install nahi hai.{R}")
        print("Run: pkg install chafa viu -y")

    except Exception as e:
        print(f"{Y}Picture error: {e}{R}")

    finally:
        try:
            if image_file.exists():
                image_file.unlink()
        except Exception:
            pass


# ============================================================
# DEPENDENCIES
# ============================================================

def setup_dependencies():
    try:
        subprocess.run(
            ["pkg", "install", "chafa", "viu",
             "libjpeg-turbo", "libpng",
             "freetype", "zlib", "-y"],
            check=False
        )
    except Exception:
        pass


# ============================================================
# START
# ============================================================

print()
print(f"{W}Starting Khan.py...{R}")
print(f"{W}Python: {sys.version.split()[0]}{R}")
print()

# Install viewer BEFORE picture
install_viewer()

# ============================================================
# PICTURE MUST APPEAR BEFORE CYTHON MENU
# ============================================================

show_profile()

print()
print(f"{W}Starting Cython...{R}")
print()

# ============================================================
# PYTHON VERSION
# ============================================================

PYVER = f"{sys.version_info.major}{sys.version_info.minor}"

SO_FILES = {
    "310": BASE / "RTRT11.cpython-310.so",
    "311": BASE / "RTTR111.cpython-311.so",
    "313": BASE / "TRRT11.cpython-313.so",
}

SO_FILE = SO_FILES.get(PYVER)

if SO_FILE is None:
    print(f"{Y}ERROR: Python {PYVER} supported nahi hai.{R}")
    print("Supported: Python 3.10 / 3.11 / 3.13")
    sys.exit(1)

if not SO_FILE.exists():
    print(f"{Y}ERROR: {SO_FILE.name} nahi mili.{R}")
    sys.exit(1)

print(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")
print(f"Loading: {SO_FILE.name}")
print()

# ============================================================
# LOAD CYTHON SO
# ============================================================

MODULE_NAME = SO_FILE.name.split(".")[0]

try:
    spec = importlib.util.spec_from_file_location(
        MODULE_NAME,
        SO_FILE
    )

    if spec is None or spec.loader is None:
        raise ImportError("SO loader create nahi hua")

    MODULE = importlib.util.module_from_spec(spec)

    sys.modules[MODULE_NAME] = MODULE

    spec.loader.exec_module(MODULE)

    print(f"{G}✓ {MODULE_NAME} loaded{R}")
    print()

except Exception as e:
    print(f"{Y}✗ {MODULE_NAME} LOAD ERROR:{R}")
    print(e)
    sys.exit(1)

# ============================================================
# RUN MAIN MENU
# ============================================================

try:
    if not hasattr(MODULE, "main"):
        print(f"{Y}✗ {MODULE_NAME}.main() nahi mila{R}")
        sys.exit(1)

    # Picture already displayed above.
    # Ab Cython ka MAIN MENU chalega.
    MODULE.main()

except KeyboardInterrupt:
    print("\nProgram stopped.")

except Exception as e:
    print(f"{Y}✗ PROGRAM ERROR:{R}")
    print(e)
    sys.exit(1)

اہم: "PASTE_YOUR_EXISTING_PROFILE_B64_HERE" کو literally نہ چھوڑنا۔ اپنی موجودہ پوری "PROFILE_B64" والی value اسی جگہ رکھنی ہے۔

اس ترتیب میں flow یہ ہوگا:

"PROFILE_B64 → JPEG → chafa/viu → Picture → Cython load → [01] [02] [03] menu"

اگر اس کے بعد بھی صرف menu آئے اور picture نہ آئے تو Termux میں یہ دو commands چلا کر output بھیج دو:

which chafa
which viu

اور:

pkg install chafa viu -y

پھر "python Khan.py" چلانا۔
