import mysql.connector
import os
import logging

log_format = '%(asctime)s : %(message)s'
logcon = logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

tmp = open('tmp.txt', 'w+') #Temporary File To Write The Amounts

mydb = mysql.connector.connect(
  auth_plugin='mysql_native_password',
  host="192.168.10.5",
  user="smilin_dominator",
  password="Barney2356",
  database='miscellaneous'
) # The Credentials For The Database

times = int(input("How Many Items? : "))
logging.warning(f'Chose {times} Items')
for i in range(times): #It'll keep repeating for the amount of items
  try:
    id = input("\nID: ") # ID As In The First Column
    if id == 'stop':
      break
    else:
      sql_select_Query = f"select * from paddigurlTest WHERE id = {id}" # This Will Be Sent To The Database
      cursor = mydb.cursor() # This Is As If You Were Entering It Yourself
      cursor.execute(sql_select_Query) # Executes
      records = cursor.fetchall() # Gets All The Outputs
      for row in records: 
        print(f"\nName  : {row[1]}")
        print(f"Price : {row[2]}")
        tmp.writelines(f'{row[2]}\n')
        logging.info(f'Sold Item;\n{records}')
      tmp.flush()
  except Exception as rim:
    print('An Error Occured!\n\n', rim)
    logging.error("MySQL Error:\n\n",rim)