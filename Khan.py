#!/usr/bin/env python3

import sys
import os
import base64
import shutil
import subprocess
import importlib.util
from pathlib import Path

BASE = Path(__file__).resolve().parent

# ============================================================
# APNI EXISTING PROFILE_B64 YAHAN WAHI RAKHNA HAI
# ============================================================

PROFILE_B64 = r"""
PASTE_YOUR_EXISTING_PROFILE_B64_HERE
"""


# ============================================================
# COMMAND RUNNER
# ============================================================

def run_cmd(cmd, silent=False):
    try:
        return subprocess.run(
            cmd,
            check=False,
            stdout=subprocess.DEVNULL if silent else None,
            stderr=subprocess.DEVNULL if silent else None
        )
    except Exception:
        return None


# ============================================================
# INSTALL IMAGE VIEWER
# ============================================================

print()
print("Starting Khan.py...")
print(f"Python: {sys.version.split()[0]}")
print()

run_cmd(["pkg", "update", "-y"])

run_cmd([
    "pkg", "install",
    "libjpeg-turbo",
    "libpng",
    "freetype",
    "zlib",
    "viu",
    "-y"
])

# chafa available ho to install ho jayega.
# Agar package available na ho to bhi program continue karega.
run_cmd(["pkg", "install", "chafa", "-y"])


# ============================================================
# SHOW PROFILE IMAGE
# ============================================================

def show_profile():
    image = BASE / ".khan_profile.jpg"

    try:
        data = "".join(PROFILE_B64.split())

        if not data or "PASTE_YOUR_EXISTING" in data:
            print("PROFILE_B64 empty hai.")
            return

        raw = base64.b64decode(data, validate=False)

        if not raw.startswith(b"\xff\xd8"):
            print("ERROR: PROFILE_B64 valid JPEG nahi hai.")
            return

        image.write_bytes(raw)

        print()
        print("==========================================")
        print("              ASIF-KHAN0")
        print("==========================================")
        print()

        # CHAFА first
        if shutil.which("chafa"):
            result = subprocess.run(
                [
                    "chafa",
                    "--format", "symbols",
                    "--size", "50x20",
                    str(image)
                ],
                check=False
            )

            if result.returncode == 0:
                print()
                image.unlink(missing_ok=True)
                return

        # VIU fallback
        if shutil.which("viu"):
            result = subprocess.run(
                [
                    "viu",
                    "-w",
                    "50",
                    str(image)
                ],
                check=False
            )

            if result.returncode == 0:
                print()
                image.unlink(missing_ok=True)
                return

        print()
        print("ERROR: chafa aur viu dono available nahi hain.")
        print("Run:")
        print("pkg install chafa viu -y")

    except Exception as e:
        print()
        print("Picture Error:", e)

    finally:
        try:
            image.unlink(missing_ok=True)
        except Exception:
            pass


# ============================================================
# SHOW IMAGE FIRST
# ============================================================

show_profile()


# ============================================================
# OPTIONAL PILLOW
# ============================================================
# Pillow fail ho bhi jaye to picture/menu band nahi hoga.

print()
print("Checking Pillow...")

try:
    import PIL
    from PIL import Image
    print("Pillow OK")
except Exception:
    print("Pillow installed nahi hai.")
    print("Picture display ke liye Pillow required nahi hai.")

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-cache-dir",
                "Pillow"
            ],
            check=False
        )
    except Exception:
        pass


# ============================================================
# PYTHON VERSION
# ============================================================

PYVER = f"{sys.version_info.major}{sys.version_info.minor}"


# ============================================================
# CYTHON SO FILES
# ============================================================

SO_FILES = {
    "310": BASE / "RTRT11.cpython-310.so",
    "311": BASE / "RTTR111.cpython-311.so",
    "313": BASE / "TRRT11.cpython-313.so",
}


SO_FILE = SO_FILES.get(PYVER)


if SO_FILE is None:
    print()
    print(f"ERROR: Python {PYVER} supported nahi hai.")
    print("Supported:")
    print("Python 3.10")
    print("Python 3.11")
    print("Python 3.13")
    sys.exit(1)


if not SO_FILE.exists():
    print()
    print(f"ERROR: {SO_FILE.name} nahi mili.")
    print(f"Required file:")
    print(SO_FILE)
    sys.exit(1)


print()
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

    print(f"✓ {MODULE_NAME} loaded")
    print()

except Exception as e:
    print()
    print(f"✗ {MODULE_NAME} LOAD ERROR:")
    print(e)
    sys.exit(1)


# ============================================================
# RUN MAIN
# ============================================================

try:
    if not hasattr(MODULE, "main"):
        print(f"✗ {MODULE_NAME}.main() nahi mila")
        sys.exit(1)

    MODULE.main()

except KeyboardInterrupt:
    print()
    print("Program stopped.")

except Exception as e:
    print()
    print("✗ PROGRAM ERROR:")
    print(e)
    sys.exit(1)

Important: Is version mein image Pillow se pehle show hogi. Agar Pillow install fail bhi ho, "chafa"/"viu" ki wajah se picture aur Cython menu rukega nahi.

Lekin ek cheez zaroori hai: "PASTE_YOUR_EXISTING_PROFILE_B64_HERE" ki jagah aapka wahi poora "/9j/4AAQ..." Base64 hona chahiye. Aapke pehle wale Base64 ka poora data mujhe is waqt current message mein available nahi hai, isliye main usko guess karke nahi bharunga.
