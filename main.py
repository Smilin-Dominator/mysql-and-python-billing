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
import mysql.connector

print("Welcome! If Something Doesn't Seem Right, Check The Logs!\n")

log_format = '%(asctime)s (%(filename)s): %(message)s'  # this basically says that the time and date come first, error next
logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

mydb = mysql.connector.connect(
    auth_plugin='mysql_native_password',
    host="178.79.168.171",
    user="smilin_dominator",
    password="Barney2356",
    database='miscellaneous'
)
mycursor = mydb.cursor()

def main(messageOfTheSecond):
    key = 2
    while key != '1':
        randomNumGen = random.randint(1, len(messageOfTheSecond))  # RNG, unscripted order
        print(f"Random Line from HUMBLE.: {messageOfTheSecond[randomNumGen]}")  # pulls from the Dictionary
        print("Commands:\n\n1 to Exit\n2 to make another bill\n3 for Master Bill\n4 for the SQL Client\n5 for The Verifier")
        date = time.strftime('%c')
        time_prompt = time.strftime('%I:%M %p')
        key = input(f"\n[{date}]-[{time_prompt}]\nSmilinPython> ")
        try:
            if key == '1':
                logging.info("Exiting Gracefully;")
                quit()
            elif key == '2':
                logging.info("Transferring to (connector.py)")
                os.system('python3 connector.py')
            elif key == '3':
                logging.info("Transferring to (master-bill.py)")
                os.system("python3 master-bill.py")
            elif key == '4':
                logging.info("Transferring to (sql-client.py)")
                os.system("python3 sql-client.py")
            elif key == '5':
                logging.info("Transferring to (verify.py)")
                os.system("python3 verify.py")
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
checkHash = os.path.exists('./hashes.txt')

if not check:
    os.mkdir("bills/")  # Makes the DIR
    logging.info("Making the Bills Directory")
    print("Making Directory 'bills/'...")
if not checkmate:
    os.mkdir(varPath)
    logging.info(f"Making A Directory For Today's Date ({varPath})")
    print(f"Making A Directory For Today..({varPath})\n")
if not checksales:
    os.mkdir('./sales_reports')
    logging.info("Making the Sales Report Directory.")
    print("Making Directory 'sales-reports/'...")
if not checkPass:
    check_log = open('log.txt', 'r')
    crit = check_log.read().splitlines()
    critical = []
    for i in range(len(crit)):
        try:
            if "Systemdump--Ignore--These" in crit[i]:
                signature = crit[i+1]
                if signature == str(hashlib.md5("McDonalds_Im_Loving_It".encode()).hexdigest()):
                    salt1 = crit[i+2]
                    salt2 = crit[i+3]
                    hash = crit[i+4]
                    critical_ar = (salt1, salt2, hash)
                    critical.append(critical_ar)
                else:
                    print("Authenticity Not Recognized.. Reset log.txt and passwd.txt, Data Might've been breached")
                    quit(66)
        except Exception as e:
            logging.warning(e)
    if not critical:
        print("No Password Set.. Creating File..")
        pas_enter = getpass.getpass("Enter Password: ")
        pas = open('./passwd.txt', 'w+')
        salt1 = ''.join(random.choices(string.ascii_letters + string.hexdigits, k=95))
        salt2 = ''.join(random.choices(string.digits + string.octdigits, k=95))
        pass_write = str(salt1 + pas_enter + salt2)
        hashpass = hashlib.sha512(pass_write.encode()).hexdigest()
        signature = hashlib.md5("McDonalds_Im_Loving_It".encode()).hexdigest()
        logging.info(f"Systemdump--Ignore--These\n{signature}\n{salt1}\n{salt2}\n{hashpass}")
        pas.write(f'{salt1},{salt2},{hashpass}')
        print("Success!")
    else:
        print("Foolish Cow Lad. You really think deleting the 'passwd.txt' file gets rid of the password!"
              "\nYour level of stupidity is egregious, your lack of braincells causes global warming."
              "\nYou really think that I, Devisha Padmaperuma would allow a little vulnerability like that"
              " to exist!")
        pas = open('./passwd.txt', 'w+')
        pas.write(f"{critical[0][0]},{critical[0][1]},{critical[0][2]}")
        print("Successfully Recovered Password!")
        pas.flush()
        pas.close()

if not checkHash:
    print("No Hash File Found...")
    mycursor.execute("SELECT filepath, hash FROM paddigurlHashes;")
    scrape = mycursor.fetchall()
    if not scrape:
        print("No Attempt Of Espionage...")
        print("Proceeding To Make File....")
        write_hi = open('hashes.txt', 'w')
        write_hi.write('\n')
        write_hi.close()
    else:
        print("Act Of Espionage Detected..")
        print("Remaking The File...")
        write_hi = open('hashes.txt', 'a')
        for i in range(len(scrape)):
            write_hi.write(f"\n{scrape[i][0]},{scrape[i][1]}")
        print("Thought you could pull a fast one, Fool?\nNo Way.")
        write_hi.flush()
        write_hi.close()

if not firstTime:
    system = sys.platform
    if system in ['linux', 'darwin']:  # darwin => mac
        print("Initializing First Time Setup..")
        print(f"OS: {system}")
        os.system('bash setup.sh')
        print("Success.. Run This File Again.")
    elif system == 'win32':
        print("Initializing First Time Setup..")
        print(f"OS: {system}")
        os.system('./setup.ps1')
        print("Success.. Run This File Again.")
        quit(2)
main(messageOfTheSecond)
