#!/usr/bin/env python3
import sys,os,base64,shutil,subprocess,importlib.util
from pathlib import Path

BASE=Path(__file__).resolve().parent
R="\033[0m";W="\033[97m";G="\033[92m";Y="\033[93m"

def install_viewer():
    try:
        if shutil.which("chafa") or shutil.which("viu"):
            return
        subprocess.run(["pkg","install","chafa","viu","-y"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=False)
    except Exception:
        pass

def show_profile():
    image_file=BASE/".khan_profile.jpg"
    try:
        data="".join(PROFILE_B64.split())
        if not data or "PASTE_YOUR_EXISTING" in data:
            print(f"{Y}PROFILE_B64 missing hai.{R}")
            return False
        try:
            raw=base64.b64decode(data,validate=False)
        except Exception as e:
            print(f"{Y}Base64 error: {e}{R}")
            return False
        if not raw.startswith(b"\xff\xd8"):
            print(f"{Y}Profile image JPEG nahi hai.{R}")
            return False
        image_file.write_bytes(raw)
        shown=False
        if shutil.which("chafa"):
            result=subprocess.run(["chafa","--format","symbols","--size","50x20",str(image_file)],check=False)
            if result.returncode==0:
                shown=True
        if not shown and shutil.which("viu"):
            result=subprocess.run(["viu","-w","50",str(image_file)],check=False)
            if result.returncode==0:
                shown=True
        if shown:
            print()
            return True
        print(f"{Y}Image viewer available nahi hai.{R}")
        print(f"{W}Run: pkg install chafa viu -y{R}")
        return False
    except Exception as e:
        print(f"{Y}Picture error: {e}{R}")
        return False
    finally:
        try:
            if image_file.exists():
                image_file.unlink()
        except Exception:
            pass

def setup_dependencies():
    try:
        subprocess.run(["pkg","install","chafa","viu","libjpeg-turbo","libpng","freetype","zlib","-y"],check=False)
    except Exception:
        pass

def startup():
    os.system("clear")
    install_viewer()
    show_profile()
    print()
    print(f"{W}Starting Khan.py...{R}")
    print(f"{W}Python: {sys.version.split()[0]}{R}")
    print()
    print(f"{W}Starting Cython...{R}")
    print()

def get_python_version():
    return f"{sys.version_info.major}{sys.version_info.minor}"

SO_FILES={
    "310":BASE/"RTRT11.cpython-310.so",
    "311":BASE/"RTTR111.cpython-311.so",
    "313":BASE/"TRRT11.cpython-313.so",
}

def load_cython():
    pyver=get_python_version()
    so_file=SO_FILES.get(pyver)
    if so_file is None:
        print(f"{Y}ERROR: Python {pyver} supported nahi hai.{R}")
        print(f"{W}Supported: Python 3.10 / 3.11 / 3.13{R}")
        sys.exit(1)
    if not so_file.exists():
        print(f"{Y}ERROR: {so_file.name} nahi mili.{R}")
        sys.exit(1)
    print(f"{W}Python {sys.version_info.major}.{sys.version_info.minor} detected{R}")
    print(f"{W}Loading: {so_file.name}{R}")
    print()
    module_name=so_file.name.split(".")[0]
    try:
        spec=importlib.util.spec_from_file_location(module_name,so_file)
        if spec is None or spec.loader is None:
            raise ImportError("SO loader create nahi hua")
        module=importlib.util.module_from_spec(spec)
        sys.modules[module_name]=module
        spec.loader.exec_module(module)
        print(f"{G}✓ {module_name} loaded{R}")
        print()
        return module
    except Exception as e:
        print(f"{Y}✗ {module_name} LOAD ERROR:{R}")
        print(e)
        sys.exit(1)

def run_main(module):
    try:
        if not hasattr(module,"main"):
            print(f"{Y}✗ {module.__name__}.main() nahi mila{R}")
            sys.exit(1)
        module.main()
    except KeyboardInterrupt:
        print("\nProgram stopped.")
    except Exception as e:
        print(f"{Y}✗ PROGRAM ERROR:{R}")
        print(e)
        sys.exit(1)

def main():
    startup()
    module=load_cython()
    run_main(module)

if __name__=="__main__":
    main()
