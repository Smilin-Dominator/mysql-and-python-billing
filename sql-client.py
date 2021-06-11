import getpass
import mysql.connector
import pandas as pd
import logging

log_format = '%(asctime)s : %(message)s'  # this basically says that the time and date come first, error next
logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

logging.info("\n\nSQL Client")
badPass = True
while badPass:
    password = getpass.getpass("Enter The Password: ")
    try:
        mydb = mysql.connector.connect(
            auth_plugin='mysql_native_password',
            host="178.79.168.171",
            user="smilin_dominator",
            password=password,
            database='miscellaneous'
        )  # connection time..
        print("Succeeded...")
        break
    except Exception as e:
        print(f"Error:\n\n{e}\n\n")
        badPass = True

help_string = "\nhelp --> displays this\nshow all --> selects all the dolls\nbye --> exits\nadd --> adds an item\nremove --> removes an item\n"

command_legend = {
    "help": help_string,
    "show all": "SELECT * FROM paddigurlTest",
    "bye": 'quit',
    "add": "INSERT INTO paddigurlTest(name, price) ",
    "remove": 'DELETE FROM paddigurlTest WHERE id = '
}

mycursor = mydb.cursor()
exit = False
while not exit:
    command = input("\nDeviSQL> ")
    try:
        command_check = command_legend[command]
        if command_check.startswith("help -->"):
            print(command_check)
        elif command == 'bye':
            print("See Ya!\n")
            quit(80085)
        elif command == 'show all':
            mycursor.execute(command_check)
            scrape = mycursor.fetchall()
            out_prep = pd.DataFrame(scrape, columns=['id', 'name', 'price'])
            out = out_prep.to_string(index=False)
            print(f"\n{out}\n")
        elif command == "add":
            name_to_add = input("\nName: ")
            price_to_add = int(input("Price: "))
            append_add = command_check + f"VALUES('{name_to_add}',{price_to_add})"
            mycursor.execute(append_add)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        elif command == "remove":
            id_of_removal = int(input("\nID: "))
            del_string = command_check + f"{id_of_removal};"
            mycursor.execute(del_string)
            mycursor.execute("SET @count = 0;")
            mycursor.execute("UPDATE paddigurlTest SET id = @count:= @count + 1;")
            mycursor.execute("ALTER TABLE paddigurlTest AUTO_INCREMENT = 1;")
            mydb.commit()
            print(mycursor.rowcount, "record removed.")
    except Exception as e:
        print("\nCorrect Command?\n")
        logging.error(e)
        exit = False
