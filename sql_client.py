import getpass
import logging
import hashlib
from configuration import variables, colours

logging.basicConfig(filename='log.txt', format=variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                    level=logging.DEBUG)


def auth(mydb):
    badPass = True
    while badPass:
        passwd = getpass.getpass(f"{colours.Red}[*] Master Password: {colours.ENDC}")
        pass_read = open('./credentials/passwd.txt', 'r')
        (salt1, salt2, hash_check) = pass_read.read().split(',')
        pass_check = salt1 + passwd + salt2
        pass_hash = hashlib.sha512(pass_check.encode()).hexdigest()
        if pass_hash == hash_check:
            pass_read.close()
            main(mydb)
            break
        else:
            logging.warning("Wrong Pass")
            badPass = True


help_string = f"""
    {colours.Cyan}Getting Data:{colours.ENDC}{colours.Green}
        show all        -> shows all dolls
        show specific   -> allows you to set one condition
        show advanced   -> allows you to set multiple conditions
        show custom     -> write your own search query (for the paddigurlTest table only){colours.ENDC}
        
    {colours.Cyan}Inserting Data:{colours.ENDC}{colours.Green}
        add             -> adds an item, prompts for Name and Price
        add id          -> adds an item, prompts for ID, Name and Price
        add multiple    -> adds items(s), prompts for Name and Price{colours.ENDC}
        
    {colours.Cyan}Modifying Data:{colours.ENDC}{colours.Green}
        update          -> Update the name and price of an item
        delete          -> removes an item from paddigurlTest and adds it to paddigurlRemoved{colours.ENDC}
    
    {colours.Cyan}Miscellaneous:{colours.ENDC}{colours.Green}
        help            -> displays this
        bye             -> quit{colours.ENDC}
"""

theformat = "{:<2}{:^40}{:>5}"


class commands:
    select_equals = "SELECT * FROM %s WHERE %s = '%s';"
    select_greater = "SELECT * FROM %s WHERE %s > '%s';"
    select_greatere = "SELECT * FROM %s WHERE %s >= '%s';"
    select_lesser = "SELECT * FROM %s WHERE %s < '%s';"
    select_lessere = "SELECT * FROM %s WHERE %s <= '%s';"
    select_not_equals = "SELECT * FROM %s WHERE %s != '%s';"
    select_all = "SELECT * FROM %s;"
    insert = "INSERT INTO %s(%s) VALUES(%s);"
    insert_multiple = "INSERT INTO %s(%s) VALUES %s"
    update = "UPDATE %s SET %s = %s;"
    delete = "DELETE FROM %s WHERE %s = %s;"


def print_items(items):
    print("\n")
    print(theformat.format(f"{colours.LightRed}ID{colours.ENDC}", f"{colours.LightMagenta}Name{colours.ENDC}",
                           f"{colours.LightGray}Price{colours.ENDC}"))
    for id, name, price in items:
        id = f"{colours.Red}{id}{colours.ENDC}"
        name = f"{colours.Yellow}{name}{colours.ENDC}"
        price = f"{colours.Green}{price}{colours.ENDC}"
        print(theformat.format(id, name, price))


"""
Get Items. This is the single most Jam-Packed function in this file.

If the Condition, Value and Operation are present, it'll execute execute the single condition mode (show specific)
If the query is present it'll execute either (show specific) or (show custom)
If neither are there, it'll execute (show all)
"""


def get_items(cursor, table: str = None, operation: str = None, condition: str = None, value: str = None,
              query: str = None):
    if (condition is not None) and (value is not None) and (operation is not None):
        if operation == "=":
            cursor.execute(commands.select_equals % (table, condition, value))
        elif operation == ">":
            cursor.execute(commands.select_greater % (table, condition, value))
        elif operation == ">=":
            cursor.execute(commands.select_greatere % (table, condition, value))
        elif operation == "<":
            cursor.execute(commands.select_lesser % (table, condition, value))
        elif operation == "<=":
            cursor.execute(commands.select_lessere % (table, condition, value))
        elif operation == "!=":
            cursor.execute(commands.select_not_equals % (table, condition, value))
        else:
            print("INVALID OPERATOR")
    elif query is not None:
        cursor.execute(query)
    else:
        cursor.execute(commands.select_all % table)
    return cursor.fetchall()


def main(mydb):
    mycursor = mydb.cursor()
    while True:
        command = input(f"\n{colours.LightRed}Smilin_DB> {colours.ENDC}")

        # -------- Miscellaneous -----------#
        if command == "help":
            print(help_string)
        elif command == "bye":
            break

        # ---------- Get Data ----------------#
        elif command == "show all":
            rows = get_items(cursor=mycursor, table="paddigurlTest")
            print_items(rows)
        elif command == "show specific":
            field = input(f"{colours.Cyan}[*] Field: {colours.ENDC}")
            operator = input(f"{colours.Red}[*] Operator (>, =, <, !=, <=, >=): {colours.ENDC}")
            value = input(f"{colours.Yellow}[*] Value: {colours.ENDC}")
            print_items(
                get_items(cursor=mycursor, table="paddigurlTest", operation=operator, condition=field, value=value)
            )
        elif command == "show advanced":
            query = "SELECT * FROM paddigurlTest WHERE "
            print(
                f"{colours.LightGreen}[*] Enter The Fields And Their Values (When Done Select ';' as Seperator){colours.ENDC}")
            i = 0
            while True:
                try:
                    field = input(f"{colours.Cyan}[*] Field {i + 1}: {colours.ENDC}")
                    operator = input(f"{colours.Red}[*] Operator (>, =, <, !=, <=, >=): {colours.ENDC}")
                    value = input(f"{colours.Yellow}[*] Value: {colours.ENDC}")
                    seperator = input(f"{colours.White}[*] Seperator (NOT, AND, OR, ;): {colours.ENDC}")
                    i += 1
                    if seperator == ";":
                        query += f"`{field}` {operator} '{value}';"
                        break
                    else:
                        query += f"`{field}` {operator} '{value}' {seperator} "
                except KeyboardInterrupt:
                    break
            print_items(get_items(cursor=mycursor, query=query))
        elif command == "show custom":
            query = input(f"{colours.Cyan}[*] Query: {colours.ENDC}")
            print_items(get_items(cursor=mycursor, query=query))

        # -------------- Insert Data --------------------#
        elif command == "add":
            name = input(f"{colours.Green}[*] Name: {colours.ENDC}")
            price = int(input(f"{colours.Yellow}[*] Price: {colours.ENDC}"))
            mycursor.execute(commands.insert % ("paddigurlTest", "name, price", f"'{name}', {price}"))
            mydb.commit()
            print(f"{colours.LightGreen}[!] Success! Inserted {mycursor.rowcount} Row(s)!")
        elif command == "add id":
            id = int(input(f"{colours.Green}[*] ID: {colours.ENDC}"))
            name = input(f"{colours.Green}[*] Name: {colours.ENDC}")
            price = int(input(f"{colours.Yellow}[*] Price: {colours.ENDC}"))
            mycursor.execute(commands.insert % ("paddigurlTest", "id, name, price", f"{id}, '{name}', {price}"))
            mydb.commit()
            print(f"{colours.LightGreen}[!] Success! Inserted {mycursor.rowcount} Row(s)!")
        elif command == "add multiple":
            values = ""
            print(f"{colours.White}[*] Enter The Values Below (Ctrl+C when Done){colours.ENDC}")
            while True:
                try:
                    name = input(f"{colours.Green}[*] Name: {colours.ENDC}")
                    price = int(input(f"{colours.Yellow}[*] Price: {colours.ENDC}"))
                    values += f"('{name}', {price}),"
                except KeyboardInterrupt:
                    values = values[:-1]
                    values += ";"
                    break
            mycursor.execute(commands.insert_multiple % ("paddigurlTest", "name, price", f"{values}"))
            mydb.commit()
            print(f"{colours.LightGreen}[!] Success! Inserted {mycursor.rowcount} Row(s)!")

        # -------------- Modifying Data -------------------#
        elif command == "update":
            pass
        elif command == "delete":
            pass
