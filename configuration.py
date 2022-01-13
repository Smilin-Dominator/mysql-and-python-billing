"""
MySQL And Python Billing
Copyright (C) 2021 Devisha Padmaperuma

MySQL And Python Billing is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MySQL And Python Billing is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with MySQL And Python Billing.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
from os import listdir, system
from sys import stdout
from yaml import load, dump, FullLoader
from rich.console import Console
from rich.prompt import Prompt


def execheck():
    f = listdir()
    for i in range(len(f)):
        if f[i].endswith('.exe'):
            return True
    else:
        return False


class Variables:
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

console = Console(color_system="256")


def print(prompt, override: str = None) -> None:
    if override is not None:
        console.print(f"[{override}]{prompt}[/{override}]")
    else:
        console.print(f"{prompt}")


def error(msg: str, override: str = None) -> None:
    if override is None:
        print(f"[white on red][@] {msg}[/white on red]")
    else:
        print(f"[{override}][@] {msg}[/{override}]")
    logging.error(f"{msg}\nLocals: {locals()}")


def warning(msg: str, override: str = None) -> None:
    if override is None:
        print(f"[white on yellow][!] {msg}[/white on yellow]")
    else:
        print(f"[{override}][!] {msg}[/{override}]")
    logging.warning(msg)


def info(msg: str, override: str = None) -> None:
    if override is not None:
        print(f"[{override}][?] {msg}[/{override}]")
    else:
        print(f"[?] {msg}")


def input(prompt: str, override: str = None, default=None, password=False) -> str:
    if default is None:
        if override is not None:
            return Prompt.ask(f"[{override}]{prompt}[/{override}]", password=password)
        else:
            return Prompt.ask(f"{prompt}", password=password)
    else:
        if override is not None:
            return Prompt.ask(f"[{override}]{prompt}[/{override}]", default=default, password=password)
        else:
            return Prompt.ask(f"{prompt}", default=default, password=password)


# ---------- Creating The Tables in SQL ----------------- #
def sql_tables(mycursor, mydb):
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
    system('cls')


# ----------- Configuration File Options ----------------- #

def write_conifguration_file():
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
        up = input("Check For Updates On Startup? (y/n)", "bold blue", "y")
        if up == 'y':
            ops["check_for_updates"] = True
        else:
            ops["check_for_updates"] = False
    incheck = input("Check File Integrity On Startup? (y/n)", "bold blue", "y")
    if incheck == 'y':
        ops["check_file_integrity"] = True
    else:
        ops["check_file_integrity"] = False
    incheck = input("Transaction Mode? (y/n)", "bold blue", "n")
    if incheck == 'y':
        ops["transactions"] = True
    else:
        ops["transactions"] = False
    incheck = input("Add VAT To Total? (y/n)", "bold blue", "n")
    if incheck == 'y':
        ops["vat"] = True
    else:
        ops["vat"] = False
    incheck = input("Enable Discount? (y/n)", "bold blue", "y")
    if incheck == 'y':
        ops["discount"] = True
    else:
        ops["discount"] = False
    dump(ops, options)
    options.flush()
    options.close()


def configuration_file_status(items: dict):
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


def configuration_file_interface():

    """
    This Interface Activates Only If there are no errors
    And You Clicked 6) on (main.py)

    What makes this unique is that unlike the previous, it shows you the status of each one, and you just
    have to toggle the options as True or False.

    At the end, you'll see a for loop. That's part of an illusion used to print the same lines updated,
    without going further down, basically Rewriting the input.
    cursor_up and erase_line are sequences I use to show the illusion.
    """

    cursor_up = '\x1b[1A'
    erase_line = '\x1b[2K'
    dictionary = load(open("credentials/options.yml", "r"), FullLoader)
    while True:
        print(configuration_file_status(dictionary))
        choice = input(f"What Would You Like To Update?", override="yellow")
        match choice:
            case "99":
                dump(dictionary, open("credentials/options.yml", "w"))
                break
            case "1":
                if dictionary["check_for_updates"]:
                    dictionary["check_for_updates"] = False
                else:
                    dictionary["check_for_updates"] = True
            case "2":
                if dictionary["check_file_integrity"]:
                    dictionary["check_file_integrity"] = False
                else:
                    dictionary["check_file_integrity"] = True
            case "3":
                if dictionary["transactions"]:
                    dictionary["transactions"] = False
                else:
                    dictionary["transactions"] = True
            case "4":
                if dictionary["vat"]:
                    dictionary["vat"] = False
                else:
                    dictionary["vat"] = True
            case "5":
                if dictionary["discount"]:
                    dictionary["discount"] = False
                else:
                    dictionary["discount"] = True
        for i in range(10):
            stdout.write(cursor_up)
            stdout.write(erase_line)


# ----------------- Custom Errors ----------------------------- #

class Errors(object):

    class DockerError(Exception):

        def __init__(self, scenario: str, message: str):
            self.scenario = scenario
            self.message = message
            self.string = "[ Docker Error: %s ]\n[ Error Message: { %s } ]"
            self.var = self.string % (self.scenario, self.message)
            print(self.var)
            logging.error(self.var)
            exit(5)

    class MySQLConnectionError(Exception):

        def __init__(self, scenario: str):
            self.scenario = scenario
            self.string = "[ MySQL Connection Error: %s ]"
            self.var = self.string % self.scenario
            print(self.var)
            logging.error(self.var)
            exit(5)

    class ValueErrors(Exception):

        def __init__(self, scenario: str):
            self.scenario = scenario
            self.string = "[ Value Error: %s ]"
            self.var = self.string % self.scenario
            print(self.var)
            logging.error(self.var)
            input("(enter to continue...)")
            system('cls')
