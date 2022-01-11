import logging
from hashlib import sha512
from configuration import Variables, print, input, info, console
from rich.table import Table

logging.basicConfig(filename='log.txt', format=Variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                    level=logging.DEBUG)


def auth(mydb):
    count = 0
    badPass = True
    while badPass:
        passwd = input("Master Password", override="red", password=True)
        pass_read = open('./credentials/passwd.txt', 'r')
        (salt1, salt2, hash_check) = pass_read.read().split(',')
        pass_check = salt1 + passwd + salt2
        pass_hash = sha512(pass_check.encode()).hexdigest()
        if pass_hash == hash_check:
            pass_read.close()
            main(mydb)
            break
        else:
            count += 1
            logging.warning("Wrong Pass")
            if count >= 3:
                break
            badPass = True


help_string = f"""
    [cyan]Getting Data:[/cyan][green]
        show all        -> shows all dolls
        show specific   -> allows you to set one condition
        show advanced   -> allows you to set multiple conditions
        show custom     -> write your own search query (for the paddigurlTest and Removed table only)[/green]
        
    [cyan]Inserting Data:[/cyan][green]
        add             -> adds an item, prompts for Name and Price
        add id          -> adds an item, prompts for ID, Name and Price
        add multiple    -> adds items(s), prompts for Name and Price[/green]
        
    [cyan]Modifying Data:[/cyan][green]
        update          -> Update the name and price of an item
        delete          -> removes an item from paddigurlTest and adds it to paddigurlRemoved[/green]
    
    [cyan]Miscellaneous:[/cyan][green]
        help            -> displays this
        bye             -> quit[/green]
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
    table = Table()
    table.add_column("ID", style="cornsilk1")
    table.add_column("Name", style="light_cyan1")
    table.add_column("Price", style="cyan1")
    for ID, name, price in items:
        table.add_row(str(ID), name, str(price))
    console.print(table)

"""
Get Items. This is the single most Jam-Packed function in this file.

If the Condition, Value and Operation are present, it'll execute execute the single condition mode (show specific)
If the query is present it'll execute either (show specific) or (show custom)
If neither are there, it'll execute (show all)
"""


def get_items(cursor, table: str = None, operation: str = None, condition: str = None, value: str = None,
              query: str = None):
    if (condition is not None) and (value is not None) and (operation is not None):
        match operation:
            case "=":
                cursor.execute(commands.select_equals % (table, condition, value))
            case ">":
                cursor.execute(commands.select_greater % (table, condition, value))
            case ">=":
                cursor.execute(commands.select_greatere % (table, condition, value))
            case "<":
                cursor.execute(commands.select_lesser % (table, condition, value))
            case "<=":
                cursor.execute(commands.select_lessere % (table, condition, value))
            case "!=":
                cursor.execute(commands.select_not_equals % (table, condition, value))
            case _:
                print("INVALID OPERATOR")
    elif query is not None:
        cursor.execute(query)
    else:
        cursor.execute(commands.select_all % table)
    return cursor.fetchall()


def main(mydb):
    mycursor = mydb.cursor()
    while True:
        command = input(f"\nSmilin_DB>", override="deep_pink4")

        match command:
            # -------- Miscellaneous -----------#
            case "help":
                print(help_string)
            case "bye":
                break

            # ---------- Get Data ----------------#
            case "show all":
                rows = get_items(cursor=mycursor, table="paddigurlTest")
                print_items(rows)
            case "show specific":
                field = input(f"[*] Field", override="cyan")
                operator = input(f"[*] Operator (>, =, <, !=, <=, >=)", override="red")
                value = input(f"[*] Value", override="yellow")
                print_items(
                    get_items(cursor=mycursor, table="paddigurlTest", operation=operator, condition=field, value=value)
                )
            case "show advanced":
                query = "SELECT * FROM paddigurlTest WHERE "
                info("Enter The Fields And Their Values (When Done Select ';' as Seperator)", override="green_yellow")
                i = 0
                while True:
                    try:
                        field = input(f"[*] Field {i + 1}", override="cyan")
                        operator = input(f"[*] Operator (>, =, <, !=, <=, >=)", override="red")
                        value = input(f"[*] Value", override="cyan")
                        separator = input(f"[*] Seperator (NOT, AND, OR, ;)", override="white")
                        i += 1
                        if separator == ";":
                            query += f"`{field}` {operator} '{value}';"
                            break
                        else:
                            query += f"`{field}` {operator} '{value}' {separator} "
                    except KeyboardInterrupt:
                        break
                print_items(get_items(cursor=mycursor, query=query))
            case "show custom":
                query = input(f"[*] Query: ", override="cyan")
                print_items(get_items(cursor=mycursor, query=query))

            # -------------- Insert Data --------------------#
            case "add":
                name = input(f"[*] Name", override="green")
                price = int(input(f"[*] Price", override="yellow"))
                mycursor.execute(commands.insert % ("paddigurlTest", "name, price", f"'{name}', {price}"))
                mydb.commit()
                print(f"[!] Success! Inserted {mycursor.rowcount} Row(s)!", override="spring_green2")
            case "add id":
                ID = int(input(f"[*] ID", override="magenta"))
                name = input(f"[*] Name", override="misty_rose3")
                price = int(input(f"[*] Price", override="yellow"))
                mycursor.execute(commands.insert % ("paddigurlTest", "id, name, price", f"{ID}, '{name}', {price}"))
                mydb.commit()
                print(f"[!] Success! Inserted {mycursor.rowcount} Row(s)!", override="bright_green")
            case "add multiple":
                values = ""
                print(f"[*] Enter The Values Below (Ctrl+C when Done)", override="white")
                while True:
                    try:
                        name = input(f"[*] Name", override="pale_turquoise4")
                        price = int(input(f"[*] Price", override="steel_blue"))
                        values += f"('{name}', {price}),"
                    except KeyboardInterrupt:
                        values = values[:-1]
                        values += ";"
                        break
                mycursor.execute(commands.insert_multiple % ("paddigurlTest", "name, price", f"{values}"))
                mydb.commit()
                print(f"[!] Success! Inserted {mycursor.rowcount} Row(s)!", override="green")

            # -------------- Modifying Data -------------------#
            case "update":
                ID = int(input(f"[*] ID", override="green"))
                matches = get_items(cursor=mycursor, query="SELECT * FROM paddigurlTest WHERE ID = %d;" % ID)
                if not matches:
                    print(f"[!] No Matches!", override="red")
                    break
                else:
                    try:
                        print_items(matches)
                        print(f"\n(Ctrl+C To Abort)\n", override="red")
                        new_name = input(f"[*] New Name", override="green")
                        new_price = int(input(f"[*] New Price", override="yellow"))
                        logging.warning("Changing ID: %d\nName: %s => %s\nPrice: %d => %d" % (ID, matches[0][1], new_name, matches[0][2], new_price))
                        mycursor.execute("UPDATE paddigurlTest SET name = '%s', price = %d WHERE ID = %d;" % (new_name, new_price, ID))
                        mydb.commit()
                        print(f"[*] Success!", override="green")
                    except KeyboardInterrupt:
                        break
            case "delete":
                ID = int(input(f"[*] ID", override="green"))
                matches = get_items(cursor=mycursor, query="SELECT * FROM paddigurlTest WHERE ID = %d;" % ID)
                if not matches:
                    print(f"[!] No Matches!", override="red")
                    break
                else:
                    try:
                        print_items(matches)
                        go = input("\n[#] Proceed? (y/n)", override="yellow")
                        if go == "y":
                            mycursor.execute("DELETE FROM paddigurlTest WHERE id = %d;" % ID)
                            logging.warning("Removed ID: %d\nName: %s\nPrice: %d" % (ID, matches[0][1], matches[0][2]))
                            mycursor.execute("INSERT INTO paddigurlRemoved(id, name, price) VALUES(%d, '%s', %d);" % (ID, matches[0][1], matches[0][2]))
                            mydb.commit()
                            print(f"[*] Success!", override="green")
                        else:
                            break
                    except KeyboardInterrupt:
                        break
