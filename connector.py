import mysql.connector
import logging

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
)  # connection time

id = 69
while id != ' ':
    try:
        id = input("\nID: ")  # ID As In The First Column
        if id == '':
            tmp.flush()
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
                tmp.writelines(f'{int(price) * quantity}\n')
                logging.info(
                    f'Sold {quantity} Of Item;\n{records}, bringing the total to Rs. {str(int(price) * quantity)}')
            tmp.flush()
    except Exception as rim:
        print('An Error Occured!\n\n', rim)
        logging.error("Error:\n\n", rim)
