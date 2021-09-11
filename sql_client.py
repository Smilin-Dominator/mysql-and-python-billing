import getpass
import pandas as pd
import logging
import hashlib
from configuration import variables, colours

logging.basicConfig(filename='log.txt', format=variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                    level=logging.DEBUG)


def auth(mydb):
    badPass = True
    while badPass:
        passwd = getpass.getpass("Master Password: ")
        pass_read = open('./credentials/passwd.txt', 'r')
        (salt1, salt2, hash_check) = pass_read.read().split(',')
        pass_check = salt1 + passwd + salt2
        pass_hash = hashlib.sha512(pass_check.encode()).hexdigest()
        if pass_hash == hash_check:
            print("Success!")
            pass_read.close()
            main(mydb)
            break
        else:
            logging.warning("Wrong Pass")
            badPass = True


help_string = """
    help            -> displays this
    show all        -> shows all dolls
    show specific   -> allows you to set one conditions
    show advanced   -> allows you to set multiple conditions
    bye             -> quit
"""

theformat = "{:<2}{:^40}{:>5}"


class commands:
    select_equals = "SELECT * FROM %s WHERE %s = %s;"
    select_greater = "SELECT * FROM %s WHERE %s > %s;"
    select_lesser = "SELECT * FROM %s WHERE %s < %s;"
    select_not_equals = "SELECT * FROM %s WHERE %s != %s;"
    select_all = "SELECT * FROM %s;"
    insert = "INSERT INTO %s(%s) VALUES(%s);"
    update = "UPDATE %s SET %s = %s;"
    delete = "DELETE FROM %s WHERE %s = %s;"


def print_items(items):
    print(theformat.format(f"{colours.LightRed}ID{colours.ENDC}", f"{colours.LightMagenta}Name{colours.ENDC}", f"{colours.LightGray}Price{colours.ENDC}"))
    for id, name, price in items:
        id = f"{colours.Red}{id}{colours.ENDC}"
        name = f"{colours.Yellow}{name}{colours.ENDC}"
        price = f"{colours.Green}{price}{colours.ENDC}"
        print(theformat.format(id, name, price))


def get_items(cursor, table: str, condition: str = None, value: str = None, query: str = None):
    if (condition is not None) and (value is not None):
        cursor.execute(commands.select % (table, condition, value))
    elif query is not None:
        cursor.execute(query)
    else:
        cursor.execute(commands.select_all % table)
    return cursor.fetchall()


def main(mydb):
    mycursor = mydb.cursor()
    while True:
        command = input("\nSmilin_DB> ")
        if command == "help":
            print(help_string)
        elif command == "show all":
            rows = get_items(cursor=mycursor, table="paddigurlTest")
            print_items(rows)
        elif command == "show specific":
            print()
        elif command == "bye":
            break
