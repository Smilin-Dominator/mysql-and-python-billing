#!/usr/bin/env conda run -n mysql-and-python-billing python

# This Program was made completely (100%) by the one and only
# Devisha Padmaperuma!
# Don't even think of stealing my code!

import getpass
import logging
import os
import random
import string
import sys
import time
import hashlib

print("Welcome! If Something Doesn't Seem Right, Check The Logs!\n")

log_format = '%(asctime)s (%(filename)s): %(message)s'  # this basically says that the time and date come first, error next
logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)


def main(messageOfTheSecond):
    key = 2
    while key != '1':
        randomNumGen = random.randint(1, len(messageOfTheSecond))  # RNG, unscripted order
        print(f"Random Line from HUMBLE.: {messageOfTheSecond[randomNumGen]}")  # pulls from the Dictionary
        print("Commands:\n\n1 to Exit\n2 to make another bill\n3 for Master Bill\n4 for the SQL Client\n")
        date = time.strftime('%c')
        time_prompt = time.strftime('%I:%M %p')
        key = input(f"\n[{date}]-[{time_prompt}]\nSmilinPython> ")
        try:
            if key == '1':
                quit()
            elif key == '2':
                os.system('python3 connector.py')
            elif key == '3':
                os.system("python3 master-bill.py")
            elif key == '4':
                os.system("python3 sql-client.py")
        except Exception as e:
            logging.error(e)


messageOfTheSecond = {
    # if you don't recognize this song, stop reading this and listen <https://open.spotify.com/track/7KXjTSCq5nL1LoYtL7XAwS?si=9f86d9e08cac4cd2>
    1: "Nobody Pray for Me, It Been That Day For Me, Yeah!",  # actually who are you? Why are you reading this?
    2: "I remember syrup, sandwiches and crime allowances",  # how did you find this document?
    3: "Pull up to your block, and break it, now we playing Tetris",
    4: "AM to the PM, PM to the AM, rock.",
    5: "If I quit your BM, I still ride Mercedes.",
    6: "If I quit the Season, I still be the greatest",  # 5 & 6 are the best lines in the song
    7: "My Left Stroke Just Went Viral",
    8: "Right Stroke Put Lil' Baby In A Spiral",
    9: "Soprano C, We Like To Keep It On A High Note",
    10: "You Do Not Amaze Me, Ayy, Obama Just Paged Me, Ayy",
    11: "This, That, Grey Poupon, That Evian, That Ted Talk",
    12: "Watch My Soul Speak. You, Let The Meds Talk"
}

check = os.path.exists('bills/')
varTime = time.strftime("%d_of_%B")
varPath = f'./bills/{varTime}'
checkmate = os.path.exists(varPath)
checksales = os.path.exists('./sales_reports')
firstTime = os.path.exists('./log.txt')
checkPass = os.path.exists('./passwd.txt')

if not check:
    os.mkdir("bills/")  # Makes the DIR
    print("Making Directory 'bills/'...")
if not checkmate:
    os.mkdir(varPath)
    print(f"Making A Directory For Today..({varPath})\n")
if not checksales:
    os.mkdir('./sales_reports')
    print("Making Directory 'sales-reports/'...")
if not checkPass:
    print("No Password Set.. Creating File..")
    pas_enter = getpass.getpass("Enter Password: ")
    pas = open('./passwd.txt', 'w+')
    salt1 = ''.join(random.choices(string.ascii_letters + string.hexdigits, k=95))
    salt2 = ''.join(random.choices(string.digits + string.octdigits, k=95))
    pass_write = str(salt1 + pas_enter + salt2)
    hashpass = hashlib.sha512(pass_write.encode()).hexdigest()
    pas.write(f'{salt1},{salt2},{hashpass}')
    print("Success!")

if not firstTime:
    system = sys.platform
    if system in ['linux', 'darwin']:  # darwin => mac
        print("Initializing First Time Setup..")
        print(f"OS: {system}")
        os.system('bash setup.sh')
        print("Success.. Run This File Again.")
        quit()
    elif system == 'win32':
        print("Initializing First Time Setup..")
        print(f"OS: {system}")
        os.system('./setup.ps1')
        print("Success.. Run This File Again.")
        quit()
main(messageOfTheSecond)
