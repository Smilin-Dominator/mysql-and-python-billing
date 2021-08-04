import os
import time
from pathlib import Path


def input_screen():
    print("Welcome To The Master Bill Creator!\n")
    key = input("Today or All?\n\nT for Today\nAnything Else for All\n\n: ")
    return key


my_format = "{:<25}{:<25}"
master_bill_header = "{:^50}"


class master_bill(object):

    def __init__(self, var_path, bill, main_ar):
        self.var_path = var_path
        self.bill = bill
        self.main_ar = main_ar

    def bill_write(self):
        master_bill_path = os.path.join(self.var_path + '/master_bill.txt')
        bill_prep = my_format.format("Name", "Grand Total (Rs.)")
        master_bill_file = open(master_bill_path, 'w+')
        master_bill_file.write(f"{master_bill_header.format(50 * '-')}")
        master_bill_file.write(f"\n{master_bill_header.format('Paddy Enterprises (Pvt) Ltd.')}")
        master_bill_file.write(f"\n{master_bill_header.format(50 * '-')}")
        master_bill_file.write(f"\n{master_bill_header.format('Daily Sales Report')}")
        master_bill_file.write(f"\n{master_bill_header.format(50 * '-')}")
        master_bill_file.write(f'\n\nDate: {str(time.strftime("%d/%m/%Y"))}')
        master_bill_file.write(f"\nTime: {str(time.strftime('%I.%M %p'))}")
        master_bill_file.write(f'\n\n{bill_prep}')
        print(bill_prep)
        total = 0
        for i in range(len(self.main_ar)):
            printable = my_format.format(self.main_ar[i][0], self.main_ar[i][1])
            print(printable)
            master_bill_file.write(f"\n{printable}")
            price_to_add = float(self.main_ar[i][1])
            total = total + price_to_add
        print("\n")
        master_bill_file.write("\n\n")
        master_bill_file.write(my_format.format("Total For The Day", total))
        master_bill_file.flush()
        master_bill_file.close()
        return my_format.format("Total For The Day", total)

    def bill_collect(self):
        temp_path = os.path.join(self.var_path + '/' + self.bill)
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
        return append_tup


def sales_reports(multiverse):
    total_ar = []
    split_week = [multiverse[i:i + 7] for i in range(0, len(multiverse), 7)]
    for i in range(len(split_week)):
        start = split_week[i][0]
        end = split_week[i][len(split_week[i]) - 1]
        sales_file = f"sales-report_from_{start}_to_{end}.txt"
        sales_report = open(f"./sales_reports/{sales_file}", 'w+')
        for directory in split_week[i]:
            newdir = Path.joinpath(Path.cwd(), 'bills', directory, 'master_bill.txt')
            finder = open(newdir, 'r')
            finderread = finder.read().splitlines()
            for line in finderread:
                if line.startswith("Total For The Day"):
                    price_get = line.split(' ')
                    tot = float(price_get[11])
                    glink = (directory, tot)
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
        for j in range(len(total_ar)):
            date_prep = total_ar[j][0].split(f"{Path.joinpath(Path(), 'bills')}")
            date = date_prep[0].replace("_", " ")
            price = str(total_ar[j][1])
            sales_report.write(f'\n{my_format.format(date, f"Rs. {price}")}')
            grandest_total = grandest_total + total_ar[j][1]
        sales_report.write(f'\n\n{my_format.format("Total Sales", f"Rs: {grandest_total}")}')
        total_ar = []


def main():
    multiverse = os.listdir('./bills')
    main_ar = []
    key = input_screen()
    if key == 'T':
        var_time = time.strftime("%d_of_%B")
        var_path = f'./bills/{var_time}/'
        ls_l = os.listdir(var_path)
        for bill in ls_l:
            if bill.startswith("[BILL]"):
                to_write = master_bill(var_path, bill, 'none').bill_collect()
                main_ar.append(to_write)
        print(master_bill(var_path, 'none', main_ar).bill_write())
        sales_reports(multiverse)
    else:
        for directory in multiverse:
            var_path = os.path.join('./bills/', directory)
            ls_l = os.listdir(var_path)
            for bill in ls_l:
                if bill.startswith("[BILL]"):
                    to_write = master_bill(var_path, bill, 'none').bill_collect()
                    main_ar.append(to_write)
            print(master_bill(var_path, 'none', main_ar).bill_write())
            print("\n")
            main_ar = []
        sales_reports(multiverse)
