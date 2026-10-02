#!/usr/bin/env python3
import os,sys,base64,importlib
from pathlib import Path
RESET="\033[0m";BOLD="\033[1m";GREEN="\033[1;92m";RED="\033[1;91m";CYAN="\033[1;96m";YELLOW="\033[1;93m"
PROFILE_B64="""[BASE64_PLACEHOLDER_1]"""
def get_hidden_dir():
    home=Path.home()
    hidden=home/".as1f_mafia_core"
    try:
        hidden.mkdir(parents=True,exist_ok=True)
        (hidden/".nomedia").touch(exist_ok=True)
        return hidden
    except:
        hidden2=Path.cwd()/".as1f_core_system"
        hidden2.mkdir(parents=True,exist_ok=True)
        return hidden2
HIDDEN_DIR=get_hidden_dir()
def show_dp_mandatory():
    try:
        from PIL import Image,ImageDraw,ImageFilter
        import shutil,subprocess
        profile_path=HIDDEN_DIR/".profile_lock.jpg"
        banner_path=HIDDEN_DIR/".banner_lock.png"
        profile_path.write_bytes(base64.b64decode(PROFILE_B64))
        im=Image.open(profile_path).convert("RGB")
        w,h=im.size
        W=720
        inner_w=640
        inner_h=int(inner_w*h/w)
        pad_top=70
        pad_bottom=90
        H=inner_h+pad_top+pad_bottom
        frame=Image.new("RGB",(W,H),(0,0,0))
        d=ImageDraw.Draw(frame)
        d.rectangle([0,0,W-1,H-1],outline=(15,85,160),width=5)
        d.rectangle([14,14,W-15,H-15],outline=(8,45,95),width=3)
        d.rectangle([26,26,W-27,H-50],fill=(5,5,10))
        top_bar=Image.new("RGB",(160,12),(180,165,30))
        top_bar=top_bar.filter(ImageFilter.GaussianBlur(radius=2.5))
        frame.paste(top_bar,((W-160)//2,8))
        dp_resized=im.resize((inner_w,inner_h),Image.LANCZOS)
        px=(W-inner_w)//2
        py=pad_top-15
        frame.paste(dp_resized,(px,py))
        bottom_bar=Image.new("RGB",(60,12),(20,90,180))
        bottom_bar=bottom_bar.filter(ImageFilter.GaussianBlur(radius=1))
        frame.paste(bottom_bar,((W-60)//2,H-58))
        gray=Image.new("RGB",(110,12),(40,40,40))
        gray=gray.filter(ImageFilter.GaussianBlur(radius=1))
        frame.paste(gray,((W-110)//2,H-34))
        frame.save(banner_path)
        os.system("clear")
        if shutil.which("viu"):
            subprocess.run(["viu","-w","70",str(banner_path)],check=False)
        elif shutil.which("chafa"):
            subprocess.run(["chafa","-s","70x25",str(banner_path)],check=False)
        return True
    except Exception as e:
        print(f"{RED}DP Error: {e}{RESET}")
        return False
def load_version_module():
    version=f"{sys.version_info.major}.{sys.version_info.minor}"
    modules={"3.10":"RTRT11","3.11":"RTTR111","3.13":"TRRT11"}
    module_name=modules.get(version)
    if not module_name:
        print(f"{RED}✗ Unsupported Python version: {version}{RESET}")
        print(f"{YELLOW}Supported: Python 3.10, 3.11, 3.13{RESET}")
        return None
    base_dir=Path(__file__).resolve().parent
    if str(base_dir) not in sys.path:
        sys.path.insert(0,str(base_dir))
    try:
        module=importlib.import_module(module_name)
        print(f"{GREEN}✓ Loaded {module_name} for Python {version}{RESET}")
        return module
    except ImportError as e:
        print(f"{RED}✗ Could not load {module_name}{RESET}")
        print(f"{RED}{e}{RESET}")
        return None
print(f"{YELLOW}{BOLD} AS1F-MAFIA LOGIN SYSTEM {RESET}")
show_dp_mandatory()
PASSWORD="AS1F-KHAN0"
hidden=get_hidden_dir()
auth_file=hidden/".auth_lock"
if not auth_file.exists():
    auth_file.write_text(PASSWORD)
    print(f"{GREEN}✓ First install - Password: {PASSWORD}{RESET}")
logged_in=False
for i in range(3):
    try:
        inp=input(f"{CYAN}╰─➤ Enter Password » {RESET}").strip()
        if inp==auth_file.read_text().strip():
            print(f"{GREEN}✓ Login Success{RESET}")
            logged_in=True
            break
        print(f"{RED}✗ Wrong! DP phir se show hogi{RESET}")
        show_dp_mandatory()
    except:
        sys.exit(0)
if not logged_in:
    sys.exit(0)
print(f"{YELLOW}Login ke baad DP lazmi show...{RESET}")
show_dp_mandatory()
input(f"{CYAN}Press Enter for Main Menu...{RESET}")
TRRT11=load_version_module()
if TRRT11 is None:
    sys.exit(1)
try:
    if not hasattr(TRRT11,"start_program"):
        print(f"{RED}✗ start_program() module mein nahi mila.{RESET}")
        sys.exit(1)
    TRRT11.start_program()
except Exception as e:
    print(f"{RED}✗ Program Error: {e}{RESET}")
    sys.exit(1)
