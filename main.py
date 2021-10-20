# This Program was made completely (100%) by the one and only
# Devisha Padmaperuma!
# Don't even think of stealing my code!

# File Imports
from configuration import variables, commands, colours, errors, execheck
from security import init5_security, key_security
import bank_transfer
import setup

# Included Imports
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
    import yaml
except ModuleNotFoundError:
    setup.main()


"""

Startup

It basically uses all the main functions (down below and in security),
performs background checks such as for log.txt and credentials and ensures
that everything is fine when starting.
The most important service is connecting to the SQL Database and passing
it as a parameter to all the functions that need it.

"""
 
def startup() -> None:

    # Starts timing the boot
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
        # Connecting to the MariaDB Database
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
        # If the docker-compose.yml exists, the PC thinks that the server is a container.
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
    # the 6th Option is during setup and is for Setting up tables
    if len(credz) == 6:
        if credz[5] == 'y':
            commands().sql_tables(mycursor, mydb)
    else:
        os.system('cls')

    print(colours.BackgroundCyan, "Welcome! If Something Doesn't Seem Right, Check The Logs!", colours.ENDC, end="\n")

    # Logs Boot Time Taken
    logging.info("Booting Up Took: %f Seconds" % (time.time() - initial_time))

    # Final Phase - Main Program
    main(messageOfTheSecond, mycursor, mydb)

"""

Read Config

It pretty much just does what its name says. It goes
through the YAML file which holds all the configuration
options.

"""

def read_config(mycursor):
    while True:
        try:
            # Third Phase - Checks For Updates
            config = yaml.load(open('./credentials/options.yml', 'r'), yaml.FullLoader)
            if config["check_for_updates"]:
                init3()
            # Fourth Phase - Checks Integrity Of Credentials
            if config['check_file_integrity']:
                init5(mycursor, True)
            else:
                init5(mycursor, False)
            if config['transactions']:
                transactions = True
            else:
                transactions = False
            if config['vat']:
                vat = True
            else:
                vat = False
            if config['discount']:
                discount = True
            else:
                discount = False
            break
        except FileNotFoundError as e:
            # This triggers if its a first time setup or if the file is deleted
            logging.warning(e)
            print("[!] Config File Not Found!\n[*] Generating...")
            commands().write_conifguration_file()
        except KeyError as e:
            # This triggers is there's a missing value, field, etc..
            logging.error(e)
            print("[!] Not Enough Arguments!\n[*] Regenerating...")
            commands().write_conifguration_file()
    return [transactions, vat, discount]


"""

Main

Main takes your input and leads you to wherever you want to go.
Instead of importing everything in the start (messy), I do lazy
imports here, which in turn is cleaner and faster.

"""


def main(messageOfTheSecond, mycursor, mydb):
    key = 2
    while key != '1':
        # Gets the values for these from the read config function above
        (transactions, vat, discount) = read_config(mycursor)
        randomNumGen = random.randint(1, len(messageOfTheSecond))  # RNG, unscripted order
        print(
            f"\n{colours.BackgroundDarkGray}Random Line from HUMBLE.:{colours.ENDC} {colours.BackgroundLightMagenta}"
            f"{messageOfTheSecond[randomNumGen]}{colours.ENDC}"
        )  # pulls from the Dictionary
        if transactions:
            # If transactions mode is true, this will pop up and there will be a prompt for has or hasn't transferred 
            tra = f"{colours.Red}7 - Transactions{colours.ENDC}"
        else:
            # If transactions if false, it just puts ""
            tra = ""
        # The Main Options
        print(
            f"\n\n{colours.Red}1 - Exit{colours.ENDC}\n{colours.Green}2 - Make A Bill{colours.ENDC}\n"
            f"{colours.LightYellow}3 - Create Master Bill & Sales Reports{colours.ENDC}\n{colours.Cyan}4 - SQL Client{colours.ENDC}\n"
            f"{colours.LightGray}5 - Verifier{colours.ENDC}\n{colours.LightMagenta}6 - Configure Options{colours.ENDC}\n"
            f"{tra}"
        )
        date = time.strftime('%c')
        time_prompt = time.strftime('%I:%M %p')
        # The main prompt
        key = input(
            f"\n{colours.BackgroundLightGreen}[{date}]{colours.ENDC}-{colours.BackgroundLightCyan}[{time_prompt}]{colours.ENDC}\n"
            f"{colours.BackgroundLightMagenta}SmilinPython>{colours.ENDC} ")
        try:
            if key == '1':
                logging.info("Exiting Gracefully;")
                os.system("cls")
                sys.exit(0)
            elif key == '2':
                logging.info("Transferring to (connector.py)")
                import connector
                connector.main(transactions, mydb, vat, discount)
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
                commands().configuration_file_interface()
            elif key == '7' and transactions:
                bank_transfer.interface(mycursor, mydb)
                input("(enter to continue..)")
            os.system('clear')
        except ValueError:
            raise errors.valueErrors("Entered A Non Integer During The Main Prompt")

"""

Init0

This checks if log.txt and the credentials directory exist.
If its not an exe file (execheck) and log.txt isn't present it launches
first time setup.
If its an exe file and its the first time, it'll just make log.txt

"""


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


"""

Init1

The phase that gets the SQL credentials.
If the keys aren't present it'll either be recovered (if deleted)
or just generate new ones.
Either way, it'll go to setup.sql() which will either decrypt your
credentials (if there) or perform a first time setup

"""


def init1():
    keycheck1 = os.path.exists('./credentials/private.pem')
    keycheck2 = os.path.exists('./credentials/public.pem')
    if (not keycheck1) or (not keycheck2):
        key_security()
    return setup.sql(logging, rsa)


"""

Init3

This phase is an optional phase that checks for updates from origin/main (git).
The option to turn it off is "check_for_updates"

"""


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


"""

init5

This is the section i've spent the most time
on, surprisingly. This and security.py used to be the same
and the class was originally here, but I shifted them to another file
conf is the config option used to pursue further checks. So basically
it'll always check for missing directories and all. But if you enable
the option, it'll check the contents of the files and check its integrity

"""


def init5(mycursor, conf: bool):
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
