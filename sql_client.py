import getpass
import pandas as pd
import logging
import hashlib
from configuration import variables

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


help_string = "\nhelp --> displays this\nshow all --> selects all the dolls\nbye --> exits\nadd --> adds an " \
              "item\nremove --> removes an item\nchange --> alters an item\nadd id --> adds item with ID\n custom -->" \
              "executes your custom query\n"

theformat = "{:<2}{:^40}{:>5}"


class commands:
    select = "SELECT * FROM %s WHERE %s = %s;"
    select_all = "SELECT * FROM %s;"
    insert = "INSERT INTO %s(%s) VALUES(%s);"
    update = "UPDATE %s SET %s = %s;"
    delete = "DELETE FROM %s WHERE %s = %s;"


def print_items(items):
    print(theformat.format("ID", "Name", "Price"))
    for id, name, price in items:
        print(theformat.format(id, name, price))


def single_condition_get_items(cursor, table: str, condition: str = None, value: str = None):
    if (condition is not None) and (value is not None):
        cursor.execute(commands.select % (table, condition, value))
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
            rows = single_condition_get_items(mycursor, "paddigurlTest")
            print_items(rows)
        elif command == "bye":
            break
