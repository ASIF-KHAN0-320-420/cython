# Simple Login System - AS1F MAFIA
import os
import sys
import time

PASSWORD = "AS1F-KHAN0" # yahan apna password rakh lo

def clear():
    os.system('clear')

def login():
    clear()
    print(" AS1F-MAFIA LOGIN SYSTEM\n")
    tries = 0
    while True:
        try:
            pwd = input(" ╰─➤ Enter Password » ").strip()
        except KeyboardInterrupt:
            sys.exit()

        if pwd == PASSWORD:
            print(" ✓ Login Success")
            time.sleep(0.8)
            break
        else:
            print(" ✗ Wrong Password! Dobara try karo\n")
            tries += 1
            if tries >= 5:
                print(" 5 bar galat, exit...")
                sys.exit()

def main_menu():
    clear()
    print("Login ke baad Main Menu yahan ayega...")
    print("\n[1] Option 1")
    print("[2] Option 2")
    print("[0] Exit")

    # Yahan apna TRRT11 wala import lagana hai to try/except se lagao
    try:
        # Agar python version 3.13 hai to ye chalega
        import TRRT11
    except ModuleNotFoundError:
        print("\n [!] TRRT11 module load nahi hua.")
        print(" python3.13 se chalao: python3.13 Khan.py")
        print(" ya python3 --version check karo")

if __name__ == "__main__":
    login()
    input("Press Enter for Main Menu...")
    main_menu()
