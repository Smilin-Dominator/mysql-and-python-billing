import os
import time
from pathlib import Path

print("Welcome To The Master Bill Creator!\n")
key = input("Today or Update Specific Day?\n\nT for Today\nEnter the Directory Name (Eg: 01_of_June) for Specific Day\n\n: ")
if key == 'T':
    var_time = time.strftime("%d_of_%B")
else:
    var_time = key
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

master_bill_header = "{:^50}"
master_bill_path = os.path.join(var_path + 'master_bill.txt')
bill_prep = my_format.format("Name", "Grand Total (Rs.)")

master_bill = open(master_bill_path, 'w+')
master_bill.write(f"{master_bill_header.format(50 * '-')}")
master_bill.write(f"\n{master_bill_header.format('Paddy Enterprises (Pvt) Ltd.')}")
master_bill.write(f"\n{master_bill_header.format(50 * '-')}")
master_bill.write(f"\n{master_bill_header.format('Daily Sales Report')}")
master_bill.write(f"\n{master_bill_header.format(50 * '-')}")
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
split_week = [all_dirs_check[i:i + 7] for i in range(0, len(all_dirs_check), 7)]
for i in range(len(split_week)):
    start = split_week[i][0]
    end = split_week[i][len(split_week[i]) - 1]
    sales_file = f"sales-report_from_{start}_to_{end}.txt"
    sales_report = open(f"./sales_reports/{sales_file}", 'w+')
    for dir in split_week[i]:
        newdir = Path.joinpath(Path.cwd(), 'bills', dir, 'master_bill.txt')
        finder = open(newdir, 'r')
        finderread = finder.read().splitlines()
        for line in finderread:
            if line.startswith("Total For The Day"):
                price_get = line.split(' ')
                tot = float(price_get[11])
                glink = (dir, tot)
                total_ar.append(glink)
                break
    sales_report.write(f"{master_bill_header.format(50 * '-')}")
    sales_report.write(f"\n{master_bill_header.format('Paddy Enterprises (Pvt) Ltd.')}")
    sales_report.write(f"\n{master_bill_header.format(50 * '-')}")
    sales_report.write(f"\n{master_bill_header.format('Weekly Sales Report')}")
    sales_report.write(f"\n{master_bill_header.format(50 * '-')}")
    sales_report.write(f'\n\nDate: {str(time.strftime("%d/%m/%Y"))}')
    sales_report.write(f"\nTime: {str(time.strftime('%I.%M %p'))}")
    sales_report.write(f'\n\n{my_format.format("Day", "Total Sales")}')
    grandest_total = 0
    for i in range(len(total_ar)):
        date_prep = total_ar[i][0].split(f"{Path.joinpath(Path(), 'bills')}")
        date = date_prep[0].replace("_", " ")
        price = str(total_ar[i][1])
        sales_report.write(f'\n{my_format.format(date, f"Rs. {price}")}')
        grandest_total = grandest_total + total_ar[i][1]
    sales_report.write(f'\n\n{my_format.format("Total Sales", f"Rs: {grandest_total}")}')
    total_ar = []

