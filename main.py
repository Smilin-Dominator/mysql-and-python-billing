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
import base64
import subprocess


def startup():

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
    # First Boot - Checks For Log.txt
    init0()

    log_format = '%(asctime)s (%(filename)s): %(message)s'  # this basically says that the time and date come first, error next
    logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

    # Second Phase - Checks For SQL Credentials
    credz = init1(logging)

    mydb = mysql.connector.connect(
        auth_plugin='mysql_native_password',
        host=credz[0],
        user=credz[1],
        password=credz[2],
        database=credz[3]
    )

    mycursor = mydb.cursor()
    if len(credz) == 5:
        if credz[4] == 'y':
            print("[*] Creating Tables")
            print("[*] Creating 'paddigurlTest'")
            mycursor.execute("""
                CREATE TABLE paddigurlTest (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(256),
                    price INT
                )
            """)
            print("[*] Creating 'paddigurlRemoved'")
            mycursor.execute("""
                CREATE TABLE paddigurlRemoved (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(256),
                    price INT
                )
                        """)
            print("[*] Creating 'paddigurlHashes'")
            mycursor.execute("""
                CREATE TABLE paddigurlHashes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    filepath TEXT,
                    hash MEDIUMTEXT,
                    filecontents LONGTEXT
                )
                        """)
            mydb.commit()
            print("[*] Success!")
            os.system('cls')
    else:
        os.system('cls')

    print("Welcome! If Something Doesn't Seem Right, Check The Logs!\n")

    # Third Phase - Checks For Updates
    init3()

    # Fourth Phase - Checks Integrity Of Credentials
    init5(mycursor)

    # Final Phase - Main Program
    main(messageOfTheSecond, credz)


class integrityCheck(object):

    def __init__(self, check_log, hash_array, password_array, mycursor):
        self.check_the_pass = check_log
        self.scraped_content = hash_array
        self.password_array = password_array
        self.mycursor = mycursor

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
                        print("[*] Authenticity Not Recognized.. Reset log.txt and passwd.txt, Data Might've been breached")
                        quit(66)
            except Exception as e:
                logging.warning(e)
        return critical

    def pass_write(self):
        print("[*] Password File Tampered, Restoring...")
        logging.critical("Password File Tampered, Restoring...")
        pas = open('./credentials/passwd.txt', 'w+')
        pas.write(f"{self.password_array[0][0]},{self.password_array[0][1]},{self.password_array[0][2]}")
        pas.flush()
        pas.close()
        logging.info("Successfully Recovered Password!")
        return "[*] Successfully Recovered Password!"

    def hash_check(self):
        self.mycursor.execute("SELECT filepath, hash FROM paddigurlHashes;")
        grape = self.mycursor.fetchall()
        return grape

    def hash_write(self):
        print("[*] Hashes Have Been Tampered With, Restoring Previous Hashes...")
        logging.critical("Hashes Have Been Tampered With, Restoring Previous Hashes...")
        write_hash = open("./credentials/hashes.txt", 'w')
        for i in range(len(self.scraped_content)):
            write_hash.write(f"\n{self.scraped_content[i][0]},{self.scraped_content[i][1]}")
        write_hash.flush()
        write_hash.close()
        logging.info("Successfully Recovered The Hashes!")
        return "[*] Successfully Recovered The Hashes!\n"


def main(messageOfTheSecond, credz):
    key = 2
    while key != '1':
        randomNumGen = random.randint(1, len(messageOfTheSecond))  # RNG, unscripted order
        print(f"\nRandom Line from HUMBLE.: {messageOfTheSecond[randomNumGen]}")  # pulls from the Dictionary
        print(
            "Commands:\n\n1 - Exit\n2 - Make A Bill\n3 - Create Master Bill & Sales Reports\n4 - SQL Client\n5 - Verifier")
        date = time.strftime('%c')
        time_prompt = time.strftime('%I:%M %p')
        key = input(f"\n[{date}]-[{time_prompt}]\nSmilinPython> ")
        ncredz = ' '.join(credz).replace(' ', ',')
        try:
            if key == '1':
                logging.info("Exiting Gracefully;")
                quit()
            elif key == '2':
                logging.info("Transferring to (connector.py)")
                os.system(f'python3 connector.py {ncredz}')
            elif key == '3':
                logging.info("Transferring to (master-bill.py)")
                os.system("python3 master-bill.py")
            elif key == '4':
                logging.info("Transferring to (sql-client.py)")
                os.system(f"python3 sql-client.py {ncredz}")
            elif key == '5':
                logging.info("Transferring to (verify.py)")
                os.system(f"python3 verify.py {ncredz}")
        except Exception as e:
            logging.error(e)


def init0():
    firstTime = os.path.exists('./log.txt')
    if not firstTime:
        shredder = FileShredder()
        system = sys.platform
        if system in ['linux', 'darwin']:  # darwin => mac
            print("[*] Initializing First Time Setup..")
            input("[ Read The README.md File, Once Done, Hit Enter, It'll Be Shredded ]")
            shredder.destroy('README.md', rew=500)
            shredder.remove('README.md')
            print("[*] Successfully Shredded README.md")
            print(f"[*] OS: {system}")
            os.system('bash setup.sh')
            print("[*] Success.. Run This File Again.")
        elif system == 'win32':
            print("[*] Initializing First Time Setup..")
            input("[ Read The README.md File, Once Done, Hit Enter, It'll Be Shredded ]")
            shredder.destroy('README.md', rew=500)
            shredder.remove('README.md')
            print("[*] Successfully Shredded README.md")
            print(f"[*] OS: {system}")
            os.system('./setup.ps1')
            print("[*] Success.. Run This File Again.")
            quit(2)


def init1(logging):
    check = os.path.exists('./credentials')
    keycheck1 = os.path.exists('./credentials/private.pem')
    keycheck2 = os.path.exists('./credentials/public.pem')
    if not check:
        os.mkdir('./credentials')
        print('[*] Made Directory "./Credentials"..')
    if not keycheck1 or (not keycheck2):
        with open('log.txt', 'r') as truth:
            a = truth.read().splitlines()
            for line in a:
                if 'Binary_Data' in line:
                    print("[*] Found Existing Public Key..")
                    print("[*] Recovering..")
                    b = line.split('Binary_Data:')
                    pubkey = open('./credentials/public.pem', 'w+')
                    out = ''.join(b[1]).replace("b'", "").replace("'", "")
                    dec = base64.b64decode(out).decode()
                    pubkey.write(dec)
                    print("[*] Successfully Recovered Public Key!")
                    pubkey.close()
                elif "Binary-Data" in line:
                    print("[*] Found Existing Private Key..")
                    print("[*] Recovering...")
                    b = line.split('Binary-Data:')
                    privkey = open('./credentials/private.pem', 'w+')
                    out = ''.join(b[1]).replace("b'", "").replace("'", "")
                    dec = base64.b64decode(out).decode()
                    privkey.write(dec)
                    print("[*] Successfully Recovered Private Key!")
                    privkey.close()
            else:
                print("[*] No Attempt Of Fraud, Continuing..")
    check_for_file = os.path.exists('./credentials/mysql.txt')
    if not check_for_file:
        print("[*] No MySQL Configuration File Detected, Enter The Details Below.")
        host = input("Host: ")
        user = input("Username: ")
        password = input("Password: ")
        db = input("Database: ")
        print("[*] Generating Keys....")
        pubKey, privKey = rsa.newkeys(1096)
        print("[*] Writing Public Key..")
        with open('./credentials/public.pem', 'w') as pop:
            pubStr = pubKey.save_pkcs1()
            pop.write(pubStr.decode('utf-8'))
            encoded = base64.b64encode(pubStr)
            logging.info(f"Binary_Data:{encoded}")
            pop.close()
        print("[*] Writing Private Key..")
        with open('./credentials/private.pem', 'w') as pop:
            privStr = privKey.save_pkcs1()
            pop.write(privStr.decode('utf-8'))
            encoded = base64.b64encode(privStr)
            logging.info(f"Binary-Data:{encoded}")
            pop.close()
        logging.info("Wrote RSA Keys")
        print("[*] Success.. Final Touches...")
        st = f"{host},{user},{password},{db}".encode()
        logging.info(st)
        with open('./credentials/mysql.txt', 'wb+') as mcdonalds:
            var = rsa.encrypt(st, pubKey)
            mcdonalds.write(var)
        print("[*] Successfully Wrote The Changes To The File..")
        conf = input("[*] Create Tables? (y/n): ")
        return [host, user, password, db, conf]
    else:
        with open("./credentials/mysql.txt", 'rb') as fillet:
            privKey = rsa.PrivateKey.load_pkcs1(open("./credentials/private.pem", 'rb').read())
            a = fillet.read()
            b = rsa.decrypt(a, privKey).decode('utf-8')
            return b.split(',')


def init3():
    subprocess.run('git fetch')
    raw = subprocess.check_output('git status')
    check = raw.decode().splitlines()
    if check[1] == "Your branch is up to date with 'origin/main'.":
        print("[*] No Update Found, Continuing...")
    else:
        print("[*] Update Found... Updating...")
        print(subprocess.check_output('git pull origin main').decode())
        print("[*] Success!")


def init5(mycursor):
    check = os.path.exists('bills/')
    varTime = time.strftime("%d_of_%B")
    varPath = f'./bills/{varTime}'
    checkmate = os.path.exists(varPath)
    checksales = os.path.exists('./sales_reports')
    checkPass = os.path.exists('./credentials/passwd.txt')
    checkHash = os.path.exists('./credentials/hashes.txt')

    if not check:
        os.mkdir("bills/")  # Makes the DIR
        logging.info("Making the Bills Directory")
        print("[*] Making Directory 'bills/'...")
    if not checkmate:
        os.mkdir(varPath)
        logging.info(f"Making A Directory For Today's Date ({varPath})")
        print(f"[*] Making A Directory For Today..({varPath})\n")
    if not checksales:
        os.mkdir('./sales_reports')
        logging.info("Making the Sales Report Directory.")
        print("[*] Making Directory 'sales-reports/'...")

    if not checkPass:
        critical = integrityCheck('./log.txt', 'none', 'none', mycursor).pass_check()
        if not critical:
            print("[*] No Password Set.. Creating File..")
            pas_enter = getpass.getpass("[*] Enter Password: ")
            pas = open('./credentials/passwd.txt', 'w+')
            salt1 = ''.join(random.choices(string.ascii_letters + string.hexdigits, k=95))
            salt2 = ''.join(random.choices(string.digits + string.octdigits, k=95))
            pass_write = str(salt1 + pas_enter + salt2)
            hashpass = hashlib.sha512(pass_write.encode()).hexdigest()
            signature = hashlib.md5("McDonalds_Im_Loving_It".encode()).hexdigest()
            logging.info(f"Systemdump--Ignore--These\n{signature}\n{salt1}\n{salt2}\n{hashpass}")
            pas.write(f'{salt1},{salt2},{hashpass}')
            print("[*] Success!")
        else:
            print(integrityCheck('none', 'none', critical, mycursor).pass_write())

    if checkPass:
        critical = integrityCheck('./log.txt', 'none', 'none', mycursor).pass_check()
        read_pass = open('./credentials/passwd.txt', 'r')
        read_pass_re = read_pass.read()
        read_pass_tup = tuple(read_pass_re.split(','))
        if read_pass_tup == (critical[0][0], critical[0][1], critical[0][2]):
            print("[*] Password Check Successful.. Proceeding..")
        else:
            print(integrityCheck('none', 'none', critical, mycursor).pass_write())

    if not checkHash:
        print("[*] No Hash File Found...")
        scrape = integrityCheck('none', 'none', 'none', mycursor).hash_check()
        if not scrape:
            print("[*] No Attempt Of Espionage...")
            print("[*] Proceeding To Make File....")
            write_hi = open('./credentials/hashes.txt', 'w')
            write_hi.write('\n')
            write_hi.close()
        else:
            print(integrityCheck('none', scrape, 'none', mycursor).hash_write())

    if checkHash:
        scrape = integrityCheck('none', 'none', 'none', mycursor).hash_check()
        scrape_file = open('./credentials/hashes.txt', 'r')
        scrape2 = scrape_file.read().splitlines()
        hash_check_ar = []
        for i in range(len(scrape2)):
            if scrape2[i] == '':
                pass
            else:
                split = tuple(scrape2[i].split(','))
                hash_check_ar.append(split)
        if hash_check_ar == scrape:
            print("[*] Hashes Match.. Proceeding...\n")
        else:
            print(integrityCheck('none', scrape, 'none', mycursor).hash_write())


startup()