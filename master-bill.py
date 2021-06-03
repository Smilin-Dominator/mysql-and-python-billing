import os
import time

print("Welcome To The Master Bill Creator!")
var_time = time.strftime("%d_of_%B")
var_path = f'./bills/{var_time}/'
ls_l = os.listdir(var_path)
my_format = "{:<25}{:<25}"

main_ar = []
for bill in ls_l:
    temp_path = os.path.join(var_path + bill)
    temp_file = open(temp_path, 'r')
    temp_read = temp_file.read().splitlines()
    grand_total_raw = [e for e in temp_read if e.startswith('Grand Total: Rs.')]
    grand_total_prep = ' '.join(grand_total_raw)
    grand_total_rebuild = grand_total_prep.split(' ')
    grand_total = int(grand_total_rebuild[3])
    name_raw = [e for e in temp_read if e.startswith('Customer: ')]
    name_prep = ' '.join(name_raw)
    name_rebuild = name_prep.split(' ')
    name = name_rebuild[1]
    append_tup = (name, grand_total)
    main_ar.append(append_tup)
    break

for data in main_ar:
    pr
