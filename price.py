from connector import log_format
import logging

logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

temp = open('tmp.txt', 'r') 
tot = 0
price_unchained = (temp.read().splitlines())
try:
  desired_array = [int(numeric_string) for numeric_string in price_unchained]
  for i in range(0, len(desired_array)):
      tot = tot + desired_array[i]
except Exception as err2:
  print(err2)
  logging.error(err2)

print(f'\nTotal:', str(tot))
logging.info(f'Total: Rs. {tot}')
cu = int(input('Cash Given: Rs. '))
logging.info(f'Cash Given: Rs. {cu}')
try:
  bal = int(cu - tot)
except Exception as e:
  print(f"Error: {e}")
  logging.error(e)
if bal == 0:
  print('\nNo Balance!')
  logging.info('No Balance')
else:
  print(f'Balance: Rs. {bal}')
  logging.info(f'Balance: Rs. {str(bal)}\n')