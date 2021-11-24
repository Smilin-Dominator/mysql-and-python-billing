# This Program was made completely (100%) by the one and only
# Devisha Padmaperuma!
# Don't even think of stealing my code!

# File Imports
from configuration import variables, commands, errors, execheck, print, info, input
from security import init5_security, key_security
import bank_transfer
import setup

# Included Imports
import logging
from subprocess import getoutput, call
from os import path, mkdir, system
from random import randint
from sys import exit
from time import time, strftime

# Modules Needed To Be Installed By Pip
try:
    from mysql.connector import connect
    from mysql.connector import Error as MSError
    import rsa
    from yaml import load, FullLoader
except ModuleNotFoundError:
    setup.main()

 
def startup() -> None:
    """

    Startup

    It basically uses all the main functions (down below and in security),
    performs background checks such as for log.txt and credentials and ensures
    that everything is fine when starting.
    The most important service is connecting to the SQL Database and passing
    it as a parameter to all the functions that need it.

    """

    # Starts timing the boot
    initial_time = time()

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
        mydb = connect(
            auth_plugin='mysql_native_password',
            host=credz[0],
            user=credz[1],
            port=credz[2],
            password=credz[3],
            database=credz[4]
        )
    except MSError:
        print("[*] MySQL Database Not Connecting")
        # If the docker-compose.yml exists, the PC thinks that the server is a container.
        if path.exists('docker-compose.yml'):
            print("[*] (Realization) Docker Container, Attempting To Start It")
            check = getoutput("docker start Maria")
            newcheck = check.splitlines()
            for line in newcheck:
                if line.startswith("Error"):
                    raise errors.dockerError("Unable To Start Docker Container...", check)
            else:
                print("[*] Successful!, Rerun This File...")
                exit(1)
        else:
            raise errors.mysqlConnectionError("Couldn't Connect To Database..")

    mycursor = mydb.cursor()
    # the 6th Option is during setup and is for Setting up tables
    if len(credz) == 6:
        if credz[5] == 'y':
            commands().sql_tables(mycursor, mydb)
    else:
        system('cls')

    print("[white on cyan]Welcome! If Something Doesn't Seem Right, Check The Logs![/white on cyan]\n")

    # Logs Boot Time Taken
    logging.info("Booting Up Took: %f Seconds" % (time() - initial_time))

    # Final Phase - Main Program
    main(messageOfTheSecond, mycursor, mydb)


def read_config(mycursor, count):
    """

    Read Config

    It pretty much just does what its name says. It goes
    through the YAML file which holds all the configuration
    options.

    """

    while True:
        try:
            # Third Phase - Checks For Updates
            if sum(1 for _ in open('./credentials/options.yml')) < 5:
                commands().write_conifguration_file()
            config = load(open('./credentials/options.yml', 'r'), FullLoader)
            if config["check_for_updates"] and count == 0:
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


def main(messageOfTheSecond, mycursor, mydb):
    """

    Main

    Main takes your input and leads you to wherever you want to go.
    Instead of importing everything in the start (messy), I do lazy
    imports here, which in turn is cleaner and faster.

    """

    # Count keeps track of how many times the menu is run
    count = 0

    key = '2'
    while key != '1':
        # Gets the values for these from the read config function above
        (transactions, vat, discount) = read_config(mycursor, count)
        randomNumGen = randint(1, len(messageOfTheSecond))  # RNG, unscripted order
        print(
            f"\n[white on grey54]Random Line from HUMBLE.:[/white on grey54] [white on magenta]"
            f"{messageOfTheSecond[randomNumGen]}[/white on magenta]"
        )  # pulls from the Dictionary
        if transactions:
            # If transactions mode is true, this will pop up and there will be a prompt for has or hasn't transferred 
            tra = f"[red]7 - Transactions[/red]"
        else:
            # If transactions if false, it just puts ""
            tra = ""
        # The Main Options
        print(
            f"\n\n[red]1 - Exit\n[/red][green]2 - Make A Bill\n[/green]"
            f"[yellow]3 - Create Master Bill & Sales Reports[/yellow]\n[cyan]4 - SQL Client\n[/cyan]"
            f"[blue]5 - Verifier[/blue]\n[magenta]6 - Configure Options\n[/magenta]"
            f"{tra}"
        )
        date = strftime('%c')
        time_prompt = strftime('%I:%M %p')
        # The main prompt
        key = input(
            f"\n[white on green][{date}][/white on green]-[white on cyan][{time_prompt}][/white on cyan]\n"
            f"[white on magenta]SmilinPython>[/white on magenta]"
        )
        try:
            match key:
                case '1':
                    logging.info("Exiting Gracefully;")
                    system("cls")
                    exit(0)
                case '2':
                    logging.info("Transferring to (connector.py)")
                    import connector
                    connector.main(transactions, mydb, vat, discount)
                case '3':
                    logging.info("Transferring to (master-bill.py)")
                    import master_bill
                    master_bill.main()
                    input("(enter to continue...)")
                case '4':
                    logging.info("Transferring to (sql-client.py)")
                    import sql_client
                    sql_client.auth(mydb)
                case '5':
                    logging.info("Transferring to (verify.py)")
                    import verify
                    verify.main(mydb, mycursor)
                case '6':
                    commands().configuration_file_interface()
                case '7':
                    if transactions:
                        bank_transfer.interface(mycursor, mydb)
                        input("(enter to continue..)")
            count += 1
            system('cls')
        except ValueError:
            raise errors.valueErrors("Entered A Non Integer During The Main Prompt")


def init0():
    """

    Init0

    This checks if log.txt and the credentials directory exist.
    If its not an exe file (execheck) and log.txt is empty it launches
    first time setup.
    If its an exe file and its the first time, it'll just make log.txt

    """

    f = execheck()
    try:
        firstTime = sum(1 for _ in open('log.txt')) == 0
    except FileNotFoundError:
        firstTime = True
    check = path.exists('./credentials')
    if not check:
        mkdir('./credentials')
        info('Made Directory "./Credentials"')
    if firstTime and (not f):
        setup.main()
    elif firstTime and f:
        system("touch log.txt")


def init1():
    """

    Init1

    The phase that gets the SQL credentials.
    If the keys aren't present it'll either be recovered (if deleted)
    or just generate new ones.
    Either way, it'll go to setup.sql() which will either decrypt your
    credentials (if there) or perform a first time setup

    """

    keycheck1 = path.exists('./credentials/private.pem')
    keycheck2 = path.exists('./credentials/public.pem')
    if (not keycheck1) or (not keycheck2):
        key_security()
    return setup.sql(logging, rsa)


def init3():
    """

    Init3

    This phase is an optional phase that checks for updates from origin/main (git).
    The option to turn it off is "check_for_updates"

    """
    call(['git', 'fetch'], shell=True)
    raw = getoutput('git status')
    check = raw.splitlines()
    if \
            check[1] == "Your branch is up to date with 'origin/main'." \
                    or check[1].startswith("Your branch is ahead of 'origin/main'") \
                    or not check[1].startswith("On branch main") \
                    or check[1].startswith("fatal: not a git repository"):
        print("[*] No Update Found, Continuing...")
    else:
        print("Update Found... Updating...\n", override="blue")
        call(
            'git pull https://Smilin-Dominator@github.com/Smilin-Dominator'
            '/mysql-and-python-billing.git', shell=True)
        print("\n[*] Success!")


def init5(mycursor, conf: bool):
    """

    init5

    This is the section i've spent the most time
    on, surprisingly. This and security.py used to be the same
    and the class was originally here, but I shifted them to another file
    conf is the config option used to pursue further checks. So basically
    it'll always check for missing directories and all. But if you enable
    the option, it'll check the contents of the files and check its integrity

    """

    check = path.exists('bills/')
    varTime = time.strftime("%d_of_%B")
    varPath = f'./bills/{varTime}'
    checkmate = path.exists(varPath)
    checksales = path.exists('./sales_reports')
    if not check:
        mkdir("bills/")  # Makes the DIR
        logging.info("Making the Bills Directory")
        print("[*] Making Directory 'bills/'...")
    if not checkmate:
        mkdir(varPath)
        logging.info(f"Making A Directory For Today's Date ({varPath})")
        print(f"[*] Making A Directory For Today..({varPath})\n")
    if not checksales:
        mkdir('./sales_reports')
        logging.info("Making the Sales Report Directory.")
        print("[*] Making Directory 'sales-reports/'...")
    init5_security(mycursor, conf)


if __name__ == "__main__":
    startup()
