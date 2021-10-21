import logging
import os
import sys
import yaml
from rich.console import Console
from rich import print
from rich.prompt import Prompt


def execheck():
    f = os.listdir()
    for i in range(len(f)):
        if f[i].endswith('.exe'):
            return True
    else:
        return False


class variables:
    log_format = '%(asctime)s (%(filename)s): %(message)s'  # this basically says that the time and date come first,
    # error next

    docker_compose = """# Devisha's Docker MariaDB Creation File!
version: '3.1'

services:

    Maria:
        container_name: Maria
        image: mariadb:latest
        restart: always
        environment:
            MARIADB_ROOT_PASSWORD: 123
            MARIADB_DATABASE: paddigurl
            MARIADB_USER: %s
            MARIADB_PASSWORD: %s
        ports:
            - 3306:3306
    """


# ------------- Text Funcs ----------------#

console = Console(color_system="truecolor")


def error(msg: str, override: str = None) -> None:
    if override is None:
        print(f"[*] [white on red]{msg}[/white on red]")
    else:
        print(f"[*] [{override}]{msg}[/{override}]")
    logging.error(f"{msg}\nLocals: {locals()}")


def warning(msg: str, override: str = None) -> None:
    if override is None:
        print(f"[*] [white on yellow]{msg}[/white on yellow]")
    else:
        print(f"[*] [{override}]{msg}[/{override}]")
    logging.warning(msg)


def info(msg: str, override: str = None) -> None:
    if override is not None:
        print(f"[*] [{override}]{msg}[/{override}]")
    else:
        print(f"[*] {msg}")


def input(prompt: str, override: str = None, default=None) -> str:
    if default is None:
        if override is not None:
            return Prompt.ask(f"[{override}]{prompt}[/{override}]")
        else:
            return Prompt.ask(f"{prompt}")
    else:
        if override is not None:
            return Prompt.ask(f"[{override}]{prompt}[/{override}]", default=default)
        else:
            return Prompt.ask(f"{prompt}", default=default)


# ------------------------------------------#


class commands:

    def sql_tables(self, mycursor, mydb):
        info("Creating Tables")
        info("Creating 'paddigurlTest'")
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
        input("(enter to continue...)")
        os.system('cls')

    def write_conifguration_file(self):
        options = open('./credentials/options.yml', 'w+')
        f = execheck()
        ops = {
            "check_for_updates": None,
            "check_file_integrity": None,
            "transactions": None,
            "vat": None,
            "discount": None
        }
        if f:
            ops["check_for_updates"] = False
        else:
            up = input("Check For Updates On Startup? (y/n)", "bold blue")
            if up == 'y':
                ops["check_for_updates"] = True
            else:
                ops["check_for_updates"] = False
        incheck = input("Check File Integrity On Startup? (y/n)", "bold blue")
        if incheck == 'y':
            ops["check_file_integrity"] = True
        else:
            ops["check_file_integrity"] = False
        incheck = input("Transaction Mode? (y/n)", "bold blue")
        if incheck == 'y':
            ops["transactions"] = True
        else:
            ops["transactions"] = False
        incheck = input("Add VAT To Total? (y/n)", "bold blue")
        if incheck == 'y':
            ops["vat"] = True
        else:
            ops["vat"] = False
        incheck = input("Enable Discount? (y/n)", "bold blue")
        if incheck == 'y':
            ops["discount"] = True
        else:
            ops["discount"] = False
        yaml.dump(ops, options)
        options.flush()
        options.close()

    def configuration_file_status(self, items: dict):
        return """
            1) Check For Updates: %s
            2) Check File Integrity: %s
            3) Transaction Mode: %s
            4) VAT Enabled: %s
            5) Discount Enabled: %s
            ...
            99) Done
        """ % (items["check_for_updates"], items["check_file_integrity"], items["transactions"], items["vat"],
               items["discount"])

    def configuration_file_interface(self):

        """
        This Interface Activates Only If there are no errors
        And You Clicked 6) on (main.py)

        What makes this unique is that unlike the previous, it shows you the status of each one, and you just
        have to toggle the options as True or False.

        At the end, you'll see a for loop. That's part of an illusion used to print the same lines updated,
        without going further down, basically Rewriting the input.
        CURSOR_UP_ONE and ERASE_LINE are sequences I use to show the illusion.
        """

        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE = '\x1b[2K'
        dictionary = yaml.load(open("credentials/options.yml", "r"), yaml.FullLoader)
        while True:
            print(self.configuration_file_status(dictionary))
            choice = input(f"{colours.Yellow}[*] What Would You Like To Update?: {colours.ENDC}")
            if choice == "99":
                yaml.dump(dictionary, open("credentials/options.yml", "w"))
                break
            elif choice == "1":
                if dictionary["check_for_updates"]:
                    dictionary["check_for_updates"] = False
                else:
                    dictionary["check_for_updates"] = True
            elif choice == "2":
                if dictionary["check_file_integrity"]:
                    dictionary["check_file_integrity"] = False
                else:
                    dictionary["check_file_integrity"] = True
            elif choice == "3":
                if dictionary["transactions"]:
                    dictionary["transactions"] = False
                else:
                    dictionary["transactions"] = True
            elif choice == "4":
                if dictionary["vat"]:
                    dictionary["vat"] = False
                else:
                    dictionary["vat"] = True
            elif choice == "5":
                if dictionary["discount"]:
                    dictionary["discount"] = False
                else:
                    dictionary["discount"] = True
            for i in range(10):
                sys.stdout.write(CURSOR_UP_ONE)
                sys.stdout.write(ERASE_LINE)


class colours:
    Default = "\033[39m"
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    LightGray = "\033[37m"
    DarkGray = "\033[90m"
    LightRed = "\033[91m"
    LightGreen = "\033[92m"
    LightYellow = "\033[93m"
    LightBlue = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan = "\033[96m"
    White = "\033[97m"
    ENDC = '\033[0m'

    BackgroundDefault = "\033[49m"
    BackgroundBlack = "\033[40m"
    BackgroundRed = "\033[41m"
    BackgroundGreen = "\033[42m"
    BackgroundYellow = "\033[43m"
    BackgroundBlue = "\033[44m"
    BackgroundMagenta = "\033[45m"
    BackgroundCyan = "\033[46m"
    BackgroundLightGray = "\033[47m"
    BackgroundDarkGray = "\033[100m"
    BackgroundLightRed = "\033[101m"
    BackgroundLightGreen = "\033[102m"
    BackgroundLightYellow = "\033[103m"
    BackgroundLightBlue = "\033[104m"
    BackgroundLightMagenta = "\033[105m"
    BackgroundLightCyan = "\033[106m"
    BackgroundWhite = "\033[107m"


class errors(object):
    class dockerError(Exception):

        def __init__(self, scenario: str, message: str):
            self.scenario = scenario
            self.message = message
            self.string = "[ Docker Error: %s ]\n[ Error Message: { %s } ]"
            self.var = self.string % (self.scenario, self.message)
            print(self.var)
            logging.error(self.var)
            sys.exit(5)

    class mysqlConnectionError(Exception):

        def __init__(self, scenario: str):
            self.scenario = scenario
            self.string = "[ MySQL Connection Error: %s ]"
            self.var = self.string % self.scenario
            print(self.var)
            logging.error(self.var)
            sys.exit(5)

    class valueErrors(Exception):

        def __init__(self, scenario: str):
            self.scenario = scenario
            self.string = "[ Value Error: %s ]"
            self.var = self.string % self.scenario
            print(self.var)
            logging.error(self.var)
            input("(enter to continue...)")
            os.system('cls')
