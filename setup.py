import sys
import subprocess
from main import conifguration_file
from shred.shredders import FileShredder

def main():
    shredder = FileShredder()
    system = sys.platform
    print("[*] Initializing First Time Setup..")
    input("[ Read The README.md File, Once Done, Hit Enter, It'll Be Shredded ]")
    shredder.destroy('README.md', rew=500)
    shredder.remove('README.md')
    print("[*] Successfully Shredded README.md")
    conifguration_file()
    print("[*] Initializing Environment Setup..")
    print(f"[*] OS: {system}\n")
    subprocess.call("pip3 install -r requirements.txt", shell=True)
    print("\n[*] Making Log.txt\n")
    subprocess.call("touch log.txt", shell=True)
    print("\n[*] Success!")
    sys.exit(0)