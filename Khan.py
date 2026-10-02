#!/usr/bin/env python3
import sys
import subprocess
import importlib.util
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent
print("Starting Khan.py...")
print(f"Python: {sys.version.split()[0]}")

PYVER = f"{sys.version_info.major}{sys.version_info.minor}"

try:
    from PIL import Image
    print("✓ Pillow OK")
except ImportError:
    print("Pillow install ho raha hai...")
    try:
        subprocess.run(["pkg", "update", "-y"], check=True)
        subprocess.run(
            ["pkg", "install", "libjpeg-turbo", "libpng", "freetype", "zlib", "-y"],
            check=True
        )
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade",
             "pip", "setuptools", "wheel"],
            check=True
        )
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--no-cache-dir", "Pillow"],
            check=True
        )
        from PIL import Image
        print("✓ Pillow installed")
    except subprocess.CalledProcessError as e:
        print("✗ Pillow installation failed")
        print(e)
        sys.exit(1)

SO_FILES = {
    "313": BASE / "TRRT11.cpython-313.so",
}

LOGO_FILE = BASE / "logo.png"

def show_banner():
    if not LOGO_FILE.exists():
        print("[ BANNER NOT FOUND ]")
        return

    try:
        img = Image.open(LOGO_FILE).convert("RGB")

        term_width = shutil.get_terminal_size((80, 24)).columns
        width = min(term_width, 80)

        ratio = img.height / img.width
        height = max(1, int(width * ratio * 0.45))

        img = img.resize((width, height))

        print()

        for y in range(0, height - 1, 2):
            line = []

            for x in range(width):
                r1, g1, b1 = img.getpixel((x, y))
                r2, g2, b2 = img.getpixel((x, min(y + 1, height - 1)))

                line.append(
                    f"\033[38;2;{r1};{g1};{b1}m"
                    f"\033[48;2;{r2};{g2};{b2}m▀"
                )

            print("".join(line) + "\033[0m")

        print()

    except Exception as e:
        print(f"[ BANNER ERROR ] {e}")

show_banner()

SO_FILE = SO_FILES.get(PYVER)

if SO_FILE is None:
    print(f"ERROR: Python {PYVER} supported nahi hai.")
    print("Supported: Python 3.10 / 3.11 / 3.13")
    sys.exit(1)

if not SO_FILE.exists():
    print(f"ERROR: {SO_FILE.name} nahi mili.")
    sys.exit(1)

print(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")
print(f"Loading: {SO_FILE.name}")

MODULE_NAME = SO_FILE.name.split(".")[0]

try:
    spec = importlib.util.spec_from_file_location(MODULE_NAME, SO_FILE)

    if spec is None or spec.loader is None:
        raise ImportError("SO loader create nahi hua")

    MODULE = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = MODULE
    spec.loader.exec_module(MODULE)

    print(f"✓ {MODULE_NAME} loaded")

except Exception as e:
    print(f"✗ {MODULE_NAME} LOAD ERROR:")
    print(e)
    sys.exit(1)

try:
    if not hasattr(MODULE, "main"):
        print(f"✗ {MODULE_NAME}.main() nahi mila")
        sys.exit(1)

    MODULE.main()

except KeyboardInterrupt:
    print("\nProgram stopped.")

except Exception as e:
    print("✗ PROGRAM ERROR:")
    print(e)
    sys.exit(1)
