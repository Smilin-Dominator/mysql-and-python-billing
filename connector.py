import mysql.connector
import logging
import time
import os

log_format = '%(asctime)s : %(message)s'
logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

mydb = mysql.connector.connect(
    auth_plugin='mysql_native_password',
    host="192.168.10.5",
    user="smilin_dominator",
    password="Barney2356",
    database='miscellaneous'
)  # connection time..

customerName = input("Customer: ")  # Optional, if you're in a hurry, just leave blank
if not customerName:  # ' ' => blank
    customerName = '(Not Specified)'
logging.info(f"Sold the following to {customerName}")  # you'll see this often, in case any bills go missing
                                                       # logs are the go-to place
id = 69  # well, had to declare it as something -\_/-
ar = []  # declared as empty, will get filled in the process
while id != ' ':
    try:
        id = input("\nID: ")  # ID As In The First Column
        if id == '':  # if you just hit enter
            fileTime = str(time.strftime('%I.%M %p'))  # eg: 07.10 PM
            fileName = f"[BILL]-{customerName}-{fileTime}.txt"  # format of the filename
            filePath = os.path.join('./bills', fileName)  # adds it into the bills DIR
            fileOpen = open(filePath, 'w+')  # Opens the bill file for writing
            myFormat = "{:<25}{:<15}{:<15}{:<15}"  # format for the .format() :)
            print('\n')  # just a spacer
            formPrep = myFormat.format('Name', 'Price', 'Quantity', 'Total')
            print(formPrep)
            fileOpen.write(f'Date: {str(time.strftime("%d/%m/%Y"))}')  # eg: 02/05/2021
            fileOpen.write(f'\nTime: {str(fileTime)}')  # uses the variable set earlier
            fileOpen.write(f'\nCustomer: {customerName}\n')
            fileOpen.write(f'\n{formPrep}')
            for i in range(len(ar)):  # for loop to write the output of each, in the format
                final = myFormat.format(ar[i][0], ar[i][1], ar[i][2], ar[i][3])
                print(final)
                fileOpen.write(f'\n{final}')  # mirrors the print output to the file
            tot = 0
            price_unchained = []  # blank array, like the earlier one
            for i in range(len(ar)):
                fin = int(ar[i][3])
                price_unchained.append(fin)  # appends to the array
            for i in range(0, len(price_unchained)):
                tot = tot + price_unchained[i]  # paradox alert! this variable is dynamic, it remembers the past state.
            print(f'\nTotal: {str(tot)}')
            fileOpen.write(f'\n\nTotal: {str(tot)}')
            logging.info(f'Total: Rs. {tot}')  # Three simultaneous actions here lol
            passOff = False
            while passOff == False:
                cu = int(input('Cash Given: Rs. '))
                bal = int(cu - tot)
                if bal < 0:  # loops if its a negative number!
                    print("Negative Value, Something's Off, Retry")  # something's **really** off (why doesnt MD work?)
                    logging.warning('Negative Balance')
                    passOff = False
                elif bal == 0:
                    logging.info(f'Cash Given: Rs. {cu}')
                    fileOpen.write(f'\nCash Given: Rs. {cu}')
                    print('\nNo Balance!')
                    logging.info('No Balance')
                    fileOpen.write(f'\nNo Balance!')
                    break  # passes if its not
                else:
                    logging.info(f'Cash Given: Rs. {cu}')
                    fileOpen.write(f'\nCash Given: Rs. {cu}')
                    print(f'Balance: Rs. {bal}')
                    logging.info(f'Balance: Rs. {str(bal)}\n')
                    fileOpen.write(f'\nBalance: Rs. {bal}')
                    break
            break
        elif id == 'Kill':  # had to add an emergency kill function :)
            killPass = input("Enter Password: ")
            if killPass == '627905':  # alter the code here if you want
                quit()
            else:
                print("\n[ Wrong Password ]\n")  # thats the wrong number! (ooohhhh)
        else:
            sql_select_Query = f"select * from paddigurlTest WHERE id = {id}"  # This Will Be Sent To The Database
            cursor = mydb.cursor()  # This Is As If You Were Entering It Yourself
            cursor.execute(sql_select_Query)  # Executes
            records = cursor.fetchall()  # Gets All The Outputs
            if records:  # Basically proceeds if its not empty like []
                quantity = int(input("Quantity: "))
                for row in records:
                    name = row[1]  # gets the element from the data
                    price = row[2]  # and its in a fixed format, which is what matters
                    print(f"\nName  : {name}")
                    print(f"Price : {price}")
                    total = int(price) * quantity
                    # Appending to the blank array ...
                    tuppence = (name, price, quantity, total)
                    ar.append(tuppence)
                    # and now its done.... (suspense)
                    logging.info(  # have to have a backup:)
                        f'Sold {quantity} Of Item;\n{records}, bringing the total to Rs. {total}')
            else:
                print("\nDid You Enter The Right ID?")  # congratulations! you're a failure!
                logging.warning(f"Entered Wrong ID: {id}")
    except Exception as rim:
        logging.error("Error:\n\n", rim)  # rim alert
