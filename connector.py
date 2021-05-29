import mysql.connector
import logging
import time
import os

log_format = '%(asctime)s : %(message)s'
logcon = logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                             level=logging.DEBUG)

tmp = open('tmp.txt', 'w+')  # Temporary File To Write The Amounts

mydb = mysql.connector.connect(
    auth_plugin='mysql_native_password',
    host="192.168.10.5",
    user="smilin_dominator",
    password="Barney2356",
    database='miscellaneous'
)  # connection time..

id = 69

customerName = input("Customer: ") # Optional, if you're in a hurry, just leave blank
if customerName == ' ':
    customerName = '(Not Entered)'
logging.info(f"Sold the following to {customerName}")

ar = []
while id != ' ':
    try:
        id = input("\nID: ")  # ID As In The First Column
        if id == '':
            fileName = str(time.strftime('%d-%m-%y_%H:%M')) + '.txt'
            filePath = os.path.join('./bills' + fileName)
            fileOpen = open(filePath, 'w+')
            myformat = "{:<25}{:<15}{:<15}{:<15}"
            print('\n')
            formPrep = myformat.format('Name', 'Price', 'Quantity', 'Total')
            print(formPrep)
            fileOpen.write(f'Date: {str(time.strftime("%m/%d/%Y"))}')
            fileOpen.write(f'Time: {str(time.strftime("%H.%m %p"))}')
            fileOpen.write(f'Customer: {customerName}\n')
            fileOpen.write(formPrep)
            for i in range(len(ar)):
                final = myformat.format(ar[i][0], ar[i][1], ar[i][2], ar[i][3])
                print(final)
                fileOpen.write(final)
            fileOpen.flush()
            break
        else:
            sql_select_Query = f"select * from paddigurlTest WHERE id = {id}"  # This Will Be Sent To The Database
            cursor = mydb.cursor()  # This Is As If You Were Entering It Yourself
            cursor.execute(sql_select_Query)  # Executes
            records = cursor.fetchall()  # Gets All The Outputs
            for row in records:
                name = row[1]
                price = row[2]
                print(f"\nName  : {name}")
                print(f"Price : {price}")
                quantity = int(input("\nQuantity: "))
                total = int(price) * quantity
                # Appending to the blank arrays ...
                tuppence = (name, price, quantity, total)
                ar.append(tuppence)
                # and now its done.... (suspense)
                tmp.writelines(f'{total}\n')
                logging.info(
                    f'Sold {quantity} Of Item;\n{records}, bringing the total to Rs. {total}')
            tmp.flush()
    except Exception as rim:
        print('An Error Occured!\n\n', rim)
        logging.error("Error:\n\n", rim)
tmp.close()
fileOpen.close()