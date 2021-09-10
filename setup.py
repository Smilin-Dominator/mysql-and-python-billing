import sys
import subprocess
from configuration import commands


def main():
    system = sys.platform
    print("[*] Initializing First Time Setup..")
    commands().write_conifguration_file()
    print("[*] Initializing Environment Setup..")
    print(f"[*] OS: {system}\n")
    subprocess.call("pip3 install -r requirements.txt", shell=True)
    print("\n[*] Making Log.txt\n")
    subprocess.call("touch log.txt", shell=True)
    print("[*] Success! Resuming...")
