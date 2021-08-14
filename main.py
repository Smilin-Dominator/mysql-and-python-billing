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
import rsa
import base64
import subprocess
from configuration import variables, commands, colours, errors, execheck
from bank_transfer import view_bank_transactions
import setup


def startup():

    initial_time = time.time()

    messageOfTheSecond = {
        # if you don't recognize this song, stop reading this and listen
        # <https://open.spotify.com/track/7KXjTSCq5nL1LoYtL7XAwS?si=9f86d9e08cac4cd2>
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

    logging.basicConfig(filename='log.txt', format=variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                        level=logging.DEBUG)

    # Second Phase - Checks For SQL Credentials
    credz = init1()

    try:
        mydb = mysql.connector.connect(
            auth_plugin='mysql_native_password',
            host=credz[0],
            user=credz[1],
            port=credz[2],
            password=credz[3],
            database=credz[4]
        )
    except mysql.connector.Error:
        print("[*] MySQL Database Not Connecting")
        if os.path.exists('docker-compose.yml'):
            print("[*] (Realization) Docker Container, Attempting To Start It")
            check = subprocess.getoutput("docker start Maria")
            newcheck = check.splitlines()
            for line in newcheck:
                if line.startswith("Error"):
                    raise errors.dockerError("Unable To Start Docker Container...", check)
            else:
                print("[*] Successful!, Rerun This File...")
                sys.exit(1)
        else:
            raise errors.mysqlConnectionError("Couldn't Connect To Database..")

    mycursor = mydb.cursor()
    if len(credz) == 6:
        if credz[5] == 'y':
            commands.sql_tables(mycursor, mydb)
    else:
        os.system('cls')

    print(colours.BackgroundCyan, "Welcome! If Something Doesn't Seem Right, Check The Logs!", colours.ENDC, end="\n")

    # Logs Boot Time Taken
    logging.info("Booting Up Took: %f Seconds" % (time.time() - initial_time))

    # Final Phase - Main Program
    main(messageOfTheSecond, credz, mycursor)


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
                        print("[*] Authenticity Not Recognized.. Reset log.txt and passwd.txt, Data Might've been "
                              "breached")
                        sys.exit(66)
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


def read_config(mycursor):
    while True:
        try:
            # Third Phase - Checks For Updates
            config = open('./credentials/options.txt', 'r').read().splitlines()
            if config[0] == 'check_for_updates=True':
                init3()
            # Fourth Phase - Checks Integrity Of Credentials
            if config[1] == 'check_file_integrity=True':
                init5(mycursor, True)
            else:
                init5(mycursor, False)
            if config[2] == "transactions_or_cash=True":
                transactions = True
            else:
                transactions = False
            break
        except FileNotFoundError as e:
            logging.warning(e)
            print("[!] Config File Not Found!\n[*] Generating...")
            conifguration_file()
        except IndexError as e:
            logging.warning(e)
            print("[!] Not Enough Arguments!\n[*] Regenerating...")
            conifguration_file()
    return transactions


def conifguration_file():
    options = open('./credentials/options.txt', 'w+')
    f = execheck()
    if f:
        options.write("check_for_updates=False")
    else:
        up = input("[*] Check For Updates On Startup? (y/n): ")
        if up == 'y':
            options.write("check_for_updates=True")
        else:
            options.write("check_for_updates=False")
    incheck = input("[*] Check Password Integrity On Startup? (y/n): ")
    if incheck == 'y':
        options.write("\ncheck_file_integrity=True")
    else:
        options.write("\ncheck_file_integrity=False")
    incheck = input("[*] Transaction Mode? (y/n): ")
    if incheck == 'y':
        options.write("\ntransactions_or_cash=True")
    else:
        options.write("\ntransactions_or_cash=False")
    options.flush()
    options.close()


def main(messageOfTheSecond, credz, mycursor):
    key = 2
    while key != '1':
        transactions = read_config(mycursor)
        randomNumGen = random.randint(1, len(messageOfTheSecond))  # RNG, unscripted order
        print(
            f"\n{colours.BackgroundDarkGray}Random Line from HUMBLE.:{colours.ENDC} {colours.BackgroundLightMagenta}"
            f"{messageOfTheSecond[randomNumGen]}{colours.ENDC}")  # pulls from the Dictionary
        if transactions:
            tra = f"{colours.Red}7 - Transactions{colours.ENDC}"
        else:
            tra = ""
        print(
            f"\n\n{colours.Red}1 - Exit{colours.ENDC}\n{colours.Green}2 - Make A Bill{colours.ENDC}\n"
            f"{colours.LightYellow}3 - Create Master Bill & Sales Reports{colours.ENDC}\n{colours.Cyan}4 - SQL Client{colours.ENDC}\n"
            f"{colours.LightGray}5 - Verifier{colours.ENDC}\n{colours.LightMagenta}6 - Configure Options{colours.ENDC}\n"
            f"{tra}"
        )
        date = time.strftime('%c')
        time_prompt = time.strftime('%I:%M %p')
        key = input(
            f"\n{colours.BackgroundLightGreen}[{date}]{colours.ENDC}-{colours.BackgroundLightCyan}[{time_prompt}]{colours.ENDC}\n"
            f"{colours.BackgroundLightMagenta}SmilinPython>{colours.ENDC} ")
        ncredz = ' '.join(credz).replace(' ', ',')
        try:
            if key == '1':
                logging.info("Exiting Gracefully;")
                os.system("cls")
                sys.exit()
            elif key == '2':
                logging.info("Transferring to (connector.py)")
                import connector
                connector.init(ncredz, transactions)
            elif key == '3':
                logging.info("Transferring to (master-bill.py)")
                import master_bill
                master_bill.main()
                input("(enter to continue...)")
            elif key == '4':
                logging.info("Transferring to (sql-client.py)")
                import sql_client
                sql_client.init(ncredz)
            elif key == '5':
                logging.info("Transferring to (verify.py)")
                import verify
                verify.init(ncredz)
            elif key == '6':
                conifguration_file()
            elif key == '7' and transactions:
                view_bank_transactions()
            os.system('cls')
        except ValueError:
            raise errors.valueErrors("Entered A Non Integer During The Main Prompt")


def init0():
    f = execheck()
    firstTime = os.path.exists('./log.txt')
    check = os.path.exists('./credentials')
    if not check:
        os.mkdir('./credentials')
        print('[*] Made Directory "./Credentials"..')
    if not firstTime and not f:
        setup.main()
    elif not firstTime and f:
        os.system("touch log.txt")


def init1():
    keycheck1 = os.path.exists('./credentials/private.pem')
    keycheck2 = os.path.exists('./credentials/public.pem')
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
        create_container = input("[*] Would You Like To Create A Docker Container? (y/n): ")
        if create_container == 'y':
            print("[*] Creating Docker Image..")
            try:
                user = input("Username: ")
                password = input("Password: ")
                db = 'paddigurl'
                port = 3306
                host = '127.0.0.1'
                with open("docker-compose.yml", 'w') as docker:
                    port = int(port)
                    dc = variables.docker_compose % (user, password)
                    docker.write(dc)
                    docker.close()
                subprocess.run("docker-compose up -d", shell=True)
                time.sleep(10)
            except subprocess.SubprocessError:
                print("[*] An Error Occured, Is docker-compose Installed?")
        else:
            host = input("Host: ")
            port = input("Port (default = 3306): ")
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
        st = f"{host},{user},{port},{password},{db}".encode()
        with open('./credentials/mysql.txt', 'wb+') as mcdonalds:
            var = rsa.encrypt(st, pubKey)
            mcdonalds.write(var)
        print("[*] Successfully Wrote The Changes To The File..")
        if create_container == 'n':
            conf = input("[*] Create Tables? (y/n): ")
        else:
            conf = 'y'
        return [host, user, port, password, db, conf]
    else:
        with open("./credentials/mysql.txt", 'rb') as fillet:
            privKey = rsa.PrivateKey.load_pkcs1(open("./credentials/private.pem", 'rb').read())
            a = fillet.read()
            b = rsa.decrypt(a, privKey).decode('utf-8')
            return b.split(',')


def init3():
    subprocess.run('git fetch', stdout=subprocess.DEVNULL)
    raw = subprocess.check_output('git status')
    check = raw.decode().splitlines()
    if \
            check[1] == "Your branch is up to date with 'origin/main'." \
            or check[1].startswith("Your branch is ahead of 'origin/main'") \
            or check[1].startswith("fatal: not a git repository"):
        print("[*] No Update Found, Continuing...")
    else:
        print("[*] Update Found... Updating...\n")
        print(subprocess.check_output(
            'git pull https://Smilin-Dominator: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@github.com/Smilin-Dominator'
            '/mysql-and-python-billing.git').decode())
        print("\n[*] Success!")


def init5(mycursor, conf):
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

    if checkPass and conf:
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

    if checkHash and conf:
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


if __name__ == "__main__":
    startup()
