import connector
from connector import temp, log_format
import logging

logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

tot = 0
price_unchained = temp.readlines()
try:
    ar = []
    for line in price_unchained:
        try:
            if line.isdigit() == True:
                ar.append(line)
        except Exception as ex:
            logging.error(ex)
    desired_array = [int(numeric_string) for numeric_string in ar]
    for i in range(0, len(desired_array)):
        tot = tot + desired_array[i]
except Exception as eeee:
  print(eeee)
  logging.error(eeee)

print(f'\nTotal:', str(tot))
logging.info(f'Total: Rs. {tot}')
cu = int(input('Cash Given: Rs. '))
logging.info(f'Cash Given: Rs. {cu}')
bal = int(cu - tot)
if bal == 0:
  print('\nNo Balance!')
  logging.info('No Balance')
else:
  print(f'Balance: Rs. {bal}')
  logging.info(f'Balance: Rs. {str(bal)}\n')