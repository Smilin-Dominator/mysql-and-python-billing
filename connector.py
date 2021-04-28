#!/usr/bin/env python3.7.9
import mysql.connector

mydb = mysql.connector.connect( 
  host="192.168.0.101",
  user="smilin_dominator",
  password="CaptainPrice@2356",
  database='Miscellaneous'
) # The Credz

id = input("ID: ") # ID As In The First Column
sql_select_Query = f"select * from paddigurlTest WHERE id = {id}" # This Will Be Sent To The Database
cursor = mydb.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()
for row in records:
  print(row[1])