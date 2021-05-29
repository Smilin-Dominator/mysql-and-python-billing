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
if customerName == ' ':
    customerName = '(Not Specified)'
logging.info(f"Sold the following to {customerName}")

id = 69
ar = []
while id != ' ':
    try:
        id = input("\nID: ")  # ID As In The First Column
        if id == '':
            fileTime = str(time.strftime('%I_%M_%p'))
            fileName = f"[BILL]-{customerName}-{fileTime}.txt"
            fileOpen = open(fileName, 'w+')
            myFormat = "{:<25}{:<15}{:<15}{:<15}"
            print('\n')
            formPrep = myFormat.format('Name', 'Price', 'Quantity', 'Total')
            print(formPrep)
            fileOpen.write(f'Date: {str(time.strftime("%m/%d/%Y"))}')
            fileOpen.write(f'\nTime: {str(time.strftime("%H.%m %p"))}')
            fileOpen.write(f'\nCustomer: {customerName}\n')
            fileOpen.write(formPrep)
            for i in range(len(ar)):
                final = myFormat.format(ar[i][0], ar[i][1], ar[i][2], ar[i][3])
                print(final)
                fileOpen.write(f'{final}\n')
            tot = 0
            price_unchained = []
            for i in range(len(ar)):
                price = ar[i][1]
                quantity = ar[i][2]
                fin = int(price) * int(quantity)
                price_unchained.append(fin)
            for i in range(0, len(price_unchained)):
                tot = tot + price_unchained[i]
            print(f'\nTotal:', str(tot))
            fileOpen.write(f"\nTotal:', {str(tot)}")
            logging.info(f'Total: Rs. {tot}')

            cu = int(input('Cash Given: Rs. '))
            logging.info(f'Cash Given: Rs. {cu}')
            fileOpen.write(f'\nCash Given: Rs. {cu}')
            bal = int(cu - tot)
            if bal < 0:
                print("Negative Value, Something's Off")
                logging.info('Negative Balance')
                fileOpen.write('\nNegative Balance')
            elif bal == 0:
                print('\nNo Balance!')
                logging.info('No Balance')
                fileOpen.write(f'\nNo Balance!')
            else:
                print(f'Balance: Rs. {bal}')
                logging.info(f'Balance: Rs. {str(bal)}\n')
                fileOpen.write(f'\nBalance: Rs. {bal}')
            break
        elif id == 'Kill':
            killPass = input("Enter Password: ")
            if killPass == '627905':
                quit()
            else:
                print("\n[ Wrong Password ]\n")
        else:
            sql_select_Query = f"select * from paddigurlTest WHERE id = {id}"  # This Will Be Sent To The Database
            cursor = mydb.cursor()  # This Is As If You Were Entering It Yourself
            cursor.execute(sql_select_Query)  # Executes
            records = cursor.fetchall()  # Gets All The Outputs
            if records: # Basically proceeds if its not empty like []
                quantity = int(input("Quantity: "))
                for row in records:
                    name = row[1]
                    price = row[2]
                    print(f"\nName  : {name}")
                    print(f"Price : {price}")
                    total = int(price) * quantity
                    # Appending to the blank array ...
                    tuppence = (name, price, quantity, total)
                    ar.append(tuppence)
                    # and now its done.... (suspense)
                    logging.info(
                        f'Sold {quantity} Of Item;\n{records}, bringing the total to Rs. {total}')
            else:
                print("\nDid You Enter The Right ID?\n")
                logging.warning(f"Entered Wrong ID: {id}")
    except Exception as rim:
        logging.error("Error:\n\n", rim)