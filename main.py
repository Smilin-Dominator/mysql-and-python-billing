# This Program was made completely (100%) by the one and only
# Devisha Padmaperuma!
# Don't even think of stealing my code!

# File Imports
from configuration import variables, commands, colours, errors, execheck
from security import init5_security
import bank_transfer
import setup

# Included Imports
import base64
import subprocess
import logging
import os
import random
import sys
import time

# Modules Needed To Be Installed By Pip
try:
    import mysql.connector
    import rsa
except ModuleNotFoundError:
    setup.main()


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
    main(messageOfTheSecond, mycursor, mydb)


def read_config(mycursor):
    while True:
        try:
            # Third Phase - Checks For Updates
            config = open('./credentials/options.yml', 'r').read().splitlines()
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
            if config[3] == "vat=True":
                vat = True
            else:
                vat = False
            break
        except FileNotFoundError as e:
            logging.warning(e)
            print("[!] Config File Not Found!\n[*] Generating...")
            commands().conifguration_file()
        except IndexError as e:
            logging.warning(e)
            print("[!] Not Enough Arguments!\n[*] Regenerating...")
            commands().conifguration_file()
    return [transactions, vat]


def main(messageOfTheSecond, mycursor, mydb):
    key = 2
    while key != '1':
        (transactions, vat) = read_config(mycursor)
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
        try:
            if key == '1':
                logging.info("Exiting Gracefully;")
                os.system("cls")
                sys.exit()
            elif key == '2':
                logging.info("Transferring to (connector.py)")
                import connector
                connector.main(transactions, mydb, vat)
            elif key == '3':
                logging.info("Transferring to (master-bill.py)")
                import master_bill
                master_bill.main()
                input("(enter to continue...)")
            elif key == '4':
                logging.info("Transferring to (sql-client.py)")
                import sql_client
                sql_client.auth(mydb)
            elif key == '5':
                logging.info("Transferring to (verify.py)")
                import verify
                verify.main(mydb, mycursor)
            elif key == '6':
                commands().conifguration_file()
            elif key == '7' and transactions:
                bank_transfer.interface(mycursor, mydb)
                input("(enter to continue..)")
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
    init5_security(mycursor, conf)


if __name__ == "__main__":
    startup()
