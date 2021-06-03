import os
import time
from pathlib import Path

print("Welcome To The Master Bill Creator!\n")
var_time = time.strftime("%d_of_%B")
var_path = f'./bills/{var_time}/'
ls_l = os.listdir(var_path)
my_format = "{:<25}{:<25}"
all_dirs_check = os.listdir('./bills/')

main_ar = []
for bill in ls_l:
    if bill.startswith("[BILL]"):
        temp_path = os.path.join(var_path + bill)
        temp_file = open(temp_path, 'r')
        temp_read = temp_file.read().splitlines()
        grand_total_raw = [e for e in temp_read if e.startswith('Grand Total: Rs.')]
        grand_total_prep = ' '.join(grand_total_raw)
        grand_total_rebuild = grand_total_prep.split(' ')
        grand_total = float(grand_total_rebuild[3])
        name_raw = [e for e in temp_read if e.startswith('Customer: ')]
        name_prep = ' '.join(name_raw)
        name_rebuild = name_prep.split(' ')
        name_almost = name_rebuild[1:]
        name = ' '.join(name_almost) 
        append_tup = (name, grand_total)
        main_ar.append(append_tup)

masterbill_header = "{:^50}"
master_bill_path = os.path.join(var_path + 'master_bill.txt')
bill_prep = my_format.format("Name", "Grand Total (Rs.)")

master_bill = open(master_bill_path, 'w+')
master_bill.write(f"{masterbill_header.format(50 * '-')}")
master_bill.write(f"\n{masterbill_header.format('Paddy Enterprises (Pvt) Ltd.')}")
master_bill.write(f"\n{masterbill_header.format(50 * '-')}")
master_bill.write(f'\n\nDate: {str(time.strftime("%d/%m/%Y"))}')
master_bill.write(f"\nTime: {str(time.strftime('%I.%M %p'))}")
master_bill.write(f'\n\n{bill_prep}')
print(bill_prep)

total = 0
for i in range(len(main_ar)):
    printable = my_format.format(main_ar[i][0], main_ar[i][1])
    print(printable)
    master_bill.write(f"\n{printable}")
    price_to_add = float(main_ar[i][1])
    total = total + price_to_add
print("\n")
print(my_format.format("Total For The Day", total))
master_bill.write("\n\n")
master_bill.write(my_format.format("Total For The Day", total))
master_bill.close()


total_ar = []
sales_report = open("./sales-report.txt", 'w')
for dir in all_dirs_check:
    print(all_dirs_check)
    print(dir)
    newdir = Path.joinpath(Path.cwd(), 'bills', dir, 'master_bill.txt')
    print(newdir)
    finder = open(newdir, 'r')
    finderread = finder.read().splitlines()
    print(finderread)
    for line in finderread:
        print(line)
        if line.startswith("Total For The Day"):
            price_get = line.strip()
            glink = (dir, tot)
            total_ar.append(glink)
            break
print(total_ar)