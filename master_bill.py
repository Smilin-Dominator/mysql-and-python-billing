import logging
import os
import time
import glob
from pathlib import Path
from configuration import print, input, console
from rich.table import Table


def input_screen():
    print("Welcome To The Master Bill Creator!\n", override="cyan")
    key = input("[plum1]Today or All?[/plum1]\n\n[khaki1]T for Today[/khaki1]\n[light_goldenrod2]"
                "Anything Else for All[/light_goldenrod2]\n\n")
    return key


my_format = "{:<25}{:<25}"
master_bill_header = "{:^50}"


class master_bill(object):

    def __init__(self, var_path: str =None, bill=None, main_ar=None):
        self.var_path = var_path
        self.bill = bill
        self.main_ar = main_ar
        self.day = self.var_path[8:].replace("_", " ")

    def bill_write(self) -> None:
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

        tab = Table(title=f"Master Bill Of {self.day}")
        tab.add_column("Name")
        tab.add_column("Grand Total (Rs.)")

        total = 0
        for _, data in enumerate(self.main_ar):
            printable = my_format.format(data[0], data[1])
            tab.add_row(data[0], data[1])
            master_bill_file.write(f"\n{printable}")
            price_to_add = float(data[1])
            total = total + price_to_add

        master_bill_file.write("\n\n")
        master_bill_file.write(my_format.format("Total For The Day", total))
        master_bill_file.flush()
        master_bill_file.close()

        tab.add_row("\n", "\n")
        tab.add_row("Total For The Day", str(total))

        console.print(tab)

    def bill_collect(self):
        temp_path = os.path.join(self.var_path + '/' + self.bill)
        temp_file = open(temp_path, 'r')
        temp_read = temp_file.read().splitlines()

        grand_total = " ".join([e for e in temp_read if e.startswith('**Grand Total:')])
        grand_total = grand_total.strip("**Grand Total: <span style='color:yellow'>").strip("</span>**<br>")[3:]

        name = " ".join([e for e in temp_read if e.startswith('**Customer')])
        name = name.strip('**Customer: <span style="color:green">').strip('</span>**<br>')

        append_tup = (name, grand_total)
        return append_tup


def delete_previous(start: str):
    hits = glob.glob(f"./sales_reports/sales-report_from_{start}*")
    logging.info(f"Found file(s) with start date \"{hits}\": {hits}")
    for file in hits:
        logging.warning(f"Removing file: {file}")
        os.remove(file)


def sales_reports(multiverse: list):
    total_ar = []
    split_week = [multiverse[i:i + 7] for i in range(0, len(multiverse), 7)]
    for i in range(len(split_week)):
        start = split_week[i][0]
        end = split_week[i][len(split_week[i]) - 1]
        sales_file = f"sales-report_from_{start}_to_{end}.txt"
        delete_previous(start)
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
                to_write = master_bill(var_path=var_path, bill=bill).bill_collect()
                main_ar.append(to_write)
        master_bill(var_path=var_path, main_ar=main_ar).bill_write()
        sales_reports(multiverse)
    else:
        for directory in multiverse:
            var_path = os.path.join('./bills/', directory)
            ls_l = os.listdir(var_path)
            for bill in ls_l:
                if bill.startswith("[BILL]"):
                    to_write = master_bill(var_path=var_path, bill=bill).bill_collect()
                    main_ar.append(to_write)
            master_bill(var_path=var_path, main_ar=main_ar).bill_write()
            print("\n")
            main_ar = []
        sales_reports(multiverse)
