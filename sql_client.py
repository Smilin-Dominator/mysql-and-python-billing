from connector import main
import getpass
import mysql.connector
import pandas as pd
import logging
import hashlib

log_format = '%(asctime)s (%(filename)s): %(message)s'  # this basically says that the time and date come first, error next
logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)


def init(raw):
    global mydb
    credz = raw.split(',')
    mydb = mysql.connector.connect(
        auth_plugin='mysql_native_password',
        host=credz[0],
        user=credz[1],
        port=credz[2],
        password=credz[3],
        database=credz[4]
    )
    auth()


def auth():
    badPass = True
    while badPass:
        passwd = getpass.getpass("Master Password: ")
        pass_read = open('./credentials/passwd.txt', 'r')
        check_pass_file = pass_read.read().split(',')
        salt1 = check_pass_file[0]
        salt2 = check_pass_file[1]
        hash_check = check_pass_file[2]
        pass_check = salt1 + passwd + salt2
        pass_hash = hashlib.sha512(pass_check.encode()).hexdigest()
        if pass_hash == hash_check:
            print("Success!")
            pass_read.close()
            main()
            break
        else:
            logging.warning("Wrong Pass")
            badPass = True

help_string = "\nhelp --> displays this\nshow all --> selects all the dolls\nbye --> exits\nadd --> adds an " \
              "item\nremove --> removes an item\nchange --> alters an item\nadd id --> adds item with ID\n custom -->" \
              "executes your custom query\n"

command_legend = {
    "help": help_string,
    "show all": "SELECT * FROM paddigurlTest",
    "bye": 'quit',
    "add": "INSERT INTO paddigurlTest(name, price) ",
    "add id": "INSERT INTO paddigurlTest(id, name, price) ",
    "remove": 'DELETE FROM paddigurlTest WHERE id = ',
    "change": "UPDATE paddigurlTest SET ",
    "custom": "Enter Your Command:"
}


def main():
    mycursor = mydb.cursor()
    exit = False
    while not exit:
        command = input("\nSmilin_DB> ")
        try:
            command_check = command_legend[command]
            if command_check.startswith("\nhelp -->"):
                print(command_check)
                logging.info("Requested Help")
            elif command == 'bye':
                print("See Ya!\n")
                logging.info("Exited Gracefully;")
                break
            elif command == 'show all':
                mycursor.execute(command_check)
                scrape = mycursor.fetchall()
                out_prep = pd.DataFrame(scrape, columns=['id', 'name', 'price'])
                out = out_prep.to_string(index=False)
                logging.info("Showed All Entries")
                print(f"\n{out}\n")
            elif command == "add":
                name_to_add = input("\nName: ")
                price_to_add = int(input("Price: "))
                append_add = command_check + f"VALUES('{name_to_add}',{price_to_add})"
                mycursor.execute(append_add)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                logging.info(f"Added Entry;\nName: {name_to_add}\nPrice: {price_to_add}")
            elif command == "remove":
                id_of_removal = int(input("\nID: "))
                mycursor.execute(command_legend["show all"])
                get_all = mycursor.fetchall()
                for i in range(len(get_all)):
                    if get_all[i][0] == id_of_removal:
                        logging.warning(f"Proceeding To Delete Item:\nID: {id_of_removal}\nName: {get_all[i][1]}\nPrice: {get_all[i][2]}")
                        mycursor.execute(f"INSERT INTO paddigurlRemoved(id, name, price) VALUES({id_of_removal}, '{get_all[i][1]}', {get_all[i][2]})")
                del_string = command_check + f"{id_of_removal};"
                mycursor.execute(del_string)
                mydb.commit()
                print("Success!")
                logging.info("Successfully Deleted It!")
            elif command == "change":
                id_of_change = int(input("ID: "))
                mycursor.execute(command_legend["show all"])
                get_all = mycursor.fetchall()
                for i in range(len(get_all)):
                    if get_all[i][0] == id_of_change:
                        logging.warning(
                            f"Proceeding To Delete Item:\nID: {id_of_change}\nName: {get_all[i][1]}\nPrice: {get_all[i][2]}")
                        print(f"\nCurrent Name: {get_all[i][1]}\nCurrent Price: {get_all[i][2]}\n")
                name_to_change = input("New Name: ")
                price_to_change = int(input("New Price: "))
                new_str = command_check + f"name = '{name_to_change}', price = {price_to_change} WHERE id = {id_of_change};"
                mycursor.execute(new_str)
                print("Success!")
            elif command == "add id":
                id_to_add = int(input("ID: "))
                name_to_add = input("Name: ")
                price_to_add = int(input("Price: "))
                append_add = command_check + f"VALUES({id_to_add}, '{name_to_add}', {price_to_add})"
                mycursor.execute(append_add)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                logging.info(f"Added Entry;\nID: {id_to_add}\nName: {name_to_add}\nPrice: {price_to_add}")
            elif command == "custom":
                print(command_check)
                execute_order = input(r"")
                mycursor.execute(execute_order)
                if 'SELECT' in execute_order:
                    it_vol2 = pd.DataFrame(mycursor.fetchall(), columns=['id', 'name', 'price'])
                    print(it_vol2.to_string(index=False))
                else:
                    print("Successful!")
        except Exception as e:
            print("\nCorrect Command or Error?")
            logging.error(e)
            exit = False
