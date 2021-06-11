import getpass
import mysql.connector
import pandas as pd
import logging
import hashlib

log_format = '%(asctime)s (%(filename)s): %(message)s'  # this basically says that the time and date come first, error next
logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

badPass = True
while badPass:
    passwd = getpass.getpass("Master Password: ")
    pass_read = open('./passwd.txt', 'r')
    check_pass_file = pass_read.read().split(',')
    salt1 = check_pass_file[0]
    salt2 = check_pass_file[1]
    hash_check = check_pass_file[2]
    pass_check = salt1 + passwd + salt2
    pass_hash = hashlib.sha512(pass_check.encode()).hexdigest()
    if pass_hash == hash_check:
        print("Success!")
        mydb = mysql.connector.connect(
            auth_plugin='mysql_native_password',
            host="178.79.168.171",
            user="smilin_dominator",
            password="Barney2356",
            database='miscellaneous'
        )
        pass_read.close()
        break
    else:
        logging.warning("Wrong Pass")
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
        if command_check.startswith("\nhelp -->"):
            print(command_check)
            logging.info("Requested Help")
        elif command == 'bye':
            print("See Ya!\n")
            logging.info("Exited Gracefully;")
            quit(80085)
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
            print(get_all)
            for i in range(len(get_all)):
                if get_all[i][0] == id_of_removal:
                    logging.warning(f"Proceeding To Delete Item:\nID: {id_of_removal}\nName: {get_all[i][1]}\nPrice: {get_all[i][2]}")
            del_string = command_check + f"{id_of_removal};"
            mycursor.execute(del_string)
            mycursor.execute("SET @count = 0;")
            mycursor.execute("UPDATE paddigurlTest SET id = @count:= @count + 1;")
            mycursor.execute("ALTER TABLE paddigurlTest AUTO_INCREMENT = 1;")
            mydb.commit()
            print("Success!")
            logging.info("Successfully Deleted It!")
    except Exception as e:
        print("\nCorrect Command or Error?\n")
        logging.error(e)
        exit = False
