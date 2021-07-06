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
from shred.shredders import FileShredder
import rsa


def startup():
    global mycursor
    print("Welcome! If Something Doesn't Seem Right, Check The Logs!\n")

    log_format = '%(asctime)s (%(filename)s): %(message)s'  # this basically says that the time and date come first, error next
    logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

    mydb = mysql.connector.connect(
        auth_plugin='mysql_native_password',
        host="remotemysql.com",
        user="ki474LQWR4",
        password="owlXZM9I3W",
        database='ki474LQWR4'
    )
    mycursor = mydb.cursor()
    main(messageOfTheSecond)


class integrityCheck(object):

    def __init__(self, check_log, hash_array, password_array):
        self.check_the_pass = check_log
        self.scraped_content = hash_array
        self.password_array = password_array

    def pass_check(self):
        read_the_pass = open(self.check_the_pass, 'r')
        crit = read_the_pass.read().splitlines()
        critical = []
        for i in range(len(crit)):
            try:
                if "Systemdump--Ignore--These" in crit[i]:
                    signature = crit[i + 1]
                    if signature == str(hashlib.md5("McDonalds_Im_Loving_It".encode()).hexdigest()):
                        salt1 = crit[i + 2]
                        salt2 = crit[i + 3]
                        hashed_pw = crit[i + 4]
                        critical_ar = (salt1, salt2, hashed_pw)
                        critical.append(critical_ar)
                    else:
                        print("Authenticity Not Recognized.. Reset log.txt and passwd.txt, Data Might've been breached")
                        quit(66)
            except Exception as e:
                logging.warning(e)
        return critical

    def pass_write(self):
        print("Password File Tampered, Restoring...")
        logging.critical("Password File Tampered, Restoring...")
        pas = open('./passwd.txt', 'w+')
        pas.write(f"{self.password_array[0][0]},{self.password_array[0][1]},{self.password_array[0][2]}")
        pas.flush()
        pas.close()
        logging.info("Successfully Recovered Password!")
        return "Successfully Recovered Password!"

    def hash_check(self):
        mycursor.execute("SELECT filepath, hash FROM paddigurlHashes;")
        grape = mycursor.fetchall()
        return grape

    def hash_write(self):
        print("Hashes Have Been Tampered With, Restoring Previous Hashes...")
        logging.critical("Hashes Have Been Tampered With, Restoring Previous Hashes...")
        write_hash = open("hashes.txt", 'w')
        for i in range(len(self.scraped_content)):
            write_hash.write(f"\n{self.scraped_content[i][0]},{self.scraped_content[i][1]}")
        write_hash.flush()
        write_hash.close()
        logging.info("Successfully Recovered The Hashes!")
        return "Successfully Recovered The Hashes!\n"


def main(messageOfTheSecond):
    key = 2
    while key != '1':
        randomNumGen = random.randint(1, len(messageOfTheSecond))  # RNG, unscripted order
        print(f"\nRandom Line from HUMBLE.: {messageOfTheSecond[randomNumGen]}")  # pulls from the Dictionary
        print(
            "Commands:\n\n1 - Exit\n2 - Make A Bill\n3 - Create Master Bill & Sales Reports\n4 - SQL Client\n5 - Verifier")
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

if not firstTime:
    shredder = FileShredder()
    system = sys.platform
    if system in ['linux', 'darwin']:  # darwin => mac
        print("Initializing First Time Setup..")
        input("[ Read The README.md File, Once Done, Hit Enter, It'll Be Shredded ]")
        shredder.destroy('README.md', rew=500)
        shredder.remove('README.md')
        print(f"OS: {system}")
        os.system('bash setup.sh')
        print("Success.. Run This File Again.")
    elif system == 'win32':
        print("Initializing First Time Setup..")
        input("[ Read The README.md File, Once Done, Hit Enter, It'll Be Shredded ]")
        shredder.destroy('README.md', rew=500)
        shredder.remove('README.md')
        print(f"OS: {system}")
        os.system('./setup.ps1')
        print("Success.. Run This File Again.")
        quit(2)

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
    critical = integrityCheck('./log.txt', 'none', 'none').pass_check()
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
        print(integrityCheck('none', 'none', critical).pass_write())

if checkPass:
    critical = integrityCheck('./log.txt', 'none', 'none').pass_check()
    read_pass = open('passwd.txt', 'r')
    read_pass_re = read_pass.read()
    read_pass_tup = tuple(read_pass_re.split(','))
    if read_pass_tup == (critical[0][0], critical[0][1], critical[0][2]):
        print("Password Check Successful.. Proceeding..")
    else:
        print(integrityCheck('none', 'none', critical).pass_write())

if not checkHash:
    print("No Hash File Found...")
    scrape = integrityCheck('none', 'none', 'none').hash_check()
    if not scrape:
        print("No Attempt Of Espionage...")
        print("Proceeding To Make File....")
        write_hi = open('hashes.txt', 'w')
        write_hi.write('\n')
        write_hi.close()
    else:
        print(integrityCheck('none', scrape, 'none').hash_write())

if checkHash:
    scrape = integrityCheck('none', 'none', 'none').hash_check()
    scrape_file = open('hashes.txt', 'r')
    scrape2 = scrape_file.read().splitlines()
    hash_check_ar = []
    for i in range(len(scrape2)):
        if scrape2[i] == '':
            pass
        else:
            split = tuple(scrape2[i].split(','))
            hash_check_ar.append(split)
    if hash_check_ar == scrape:
        print("Hashes Match.. Proceeding...\n")
    else:
        print(integrityCheck('none', scrape, 'none').hash_write())


startup()