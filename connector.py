#!/usr/bin/env python3.7.9
import mysql.connector

tmp = open('tmp', 'w+') #Temporary File To Write The Stuff
temp = open('tmp', 'r') #Same, but to read

mydb = mysql.connector.connect( 
  host="192.168.0.101",
  user="smilin_dominator",
  password="CaptainPrice@2356",
  database='Miscellaneous'
) # The Credentials For The Database

times = int(input("How Many Items? : "))
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
        tmp.write(f'\n{row[2]}')
  except mysql.connector.Error as rim:
    print('An Error Occured!\n\n', rim)

price_unchained = temp.read()
for line in price_unchained:
  try:
    total += int(line)
  except ValueError as e:
    print(f'Error Occured:\n\n{e}')

print(f'\nTotal: {total}')
cu = int(input('Cash Given: '))
bal = int(cu - total)
if bal == 0:
  print('\nNo Balance!')
else:
  print(f'Balance: {bal}')