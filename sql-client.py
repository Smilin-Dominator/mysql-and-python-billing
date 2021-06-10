import getpass
import mysql.connector
import pandas as pd

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

help_string = "help --> displays this\nshow all --> selects all the dolls"

command_legend = {
    "help": help_string,
    "show all": "SELECT * FROM paddigurlTest",
    "bye": 'quit',
    "add": "INSERT INTO paddigurlTest(name, price) "
}

mycursor = mydb.cursor()
exit = False
while not exit:
    command = input("DeviSQL> ")
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
            name_to_add = input("Name: ")
            price_to_add = int(input("Price: "))
            append_add = command_check + f"VALUES('{name_to_add}',{price_to_add})"
            mycursor.execute(append_add)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
    except Exception as e:
        print("\nCorrect Command?\n")
        exit = False
quit(0)
