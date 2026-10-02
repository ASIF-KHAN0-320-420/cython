import sys
import os
import base64
import shutil
import subprocess
import importlib.util
from pathlib import Path

BASE = Path(__file__).resolve().parent


# ============================================================
# PROFILE IMAGE
# ============================================================

PROFILE_B64 = r"""
PASTE_THE_EXACT_PROFILE_B64_YOU_SENT_HERE
"""


# ============================================================
# COMMAND
# ============================================================

def cmd(command):
    try:
        return subprocess.run(
            command,
            check=False
        )
    except Exception:
        return None


# ============================================================
# IMAGE VIEWER INSTALL
# ============================================================

print()
print("Starting Khan.py...")
print(f"Python: {sys.version.split()[0]}")
print()

cmd(["pkg", "update", "-y"])

cmd([
    "pkg", "install",
    "libjpeg-turbo",
    "libpng",
    "freetype",
    "zlib",
    "viu",
    "-y"
])

# Chafa optional hai
cmd(["pkg", "install", "chafa", "-y"])


# ============================================================
# SHOW PROFILE
# ============================================================

def show_profile():

    image = BASE / ".profile_khan.jpg"

    try:
        data = "".join(PROFILE_B64.split())

        if not data:
            print("PROFILE_B64 empty hai.")
            return

        raw = base64.b64decode(data)

        if not raw.startswith(b"\xff\xd8"):
            print("PROFILE_B64 valid JPEG nahi hai.")
            return

        image.write_bytes(raw)

        print()
        print("==============================================")
        print("              ASIF-KHAN0")
        print("==============================================")
        print()

        # ----------------------------------------------------
        # CHАFA
        # ----------------------------------------------------

        if shutil.which("chafa"):

            result = subprocess.run(
                [
                    "chafa",
                    "--format",
                    "symbols",
                    "--size",
                    "50x20",
                    str(image)
                ],
                check=False
            )

            if result.returncode == 0:
                print()
                return

        # ----------------------------------------------------
        # VIU FALLBACK
        # ----------------------------------------------------

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
                return

        print()
        print("ERROR: chafa/viu available nahi hai.")
        print("Run: pkg install chafa viu -y")

    except Exception as e:
        print()
        print("PICTURE ERROR:", e)

    finally:
        try:
            image.unlink(missing_ok=True)
        except Exception:
            pass


# ============================================================
# PICTURE FIRST
# ============================================================

show_profile()


# ============================================================
# OPTIONAL PILLOW
# ============================================================

try:
    from PIL import Image
    print("Pillow OK")
except Exception:
    print("Pillow available nahi hai.")
    print("Picture ke liye Pillow required nahi hai.")


# ============================================================
# PYTHON VERSION
# ============================================================

PYVER = f"{sys.version_info.major}{sys.version_info.minor}"


# ============================================================
# CYTHON FILES
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
    print("Supported: Python 3.10 / 3.11 / 3.13")
    sys.exit(1)


if not SO_FILE.exists():

    print()
    print(f"ERROR: {SO_FILE.name} nahi mili.")
    sys.exit(1)


print()
print(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")
print(f"Loading: {SO_FILE.name}")
print()


# ============================================================
# LOAD SO
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
