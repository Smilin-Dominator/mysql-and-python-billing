import os
from configuration import colours


def view_bank_transactions():
    has = []
    has_not = []
    file_prefix = "bills/%s/%s"
    dir_prefix = "bills/%s"
    for d in os.listdir("bills/"):
        for file in os.listdir(dir_prefix % d):
            with open(file_prefix % (d, file), "r") as f:
                a = f.read().splitlines()
                has_or_not = a[len(a) - 1]
                if has_or_not.startswith("Transfered Cash: "):
                    has_or_not = ''.join(has_or_not.split("Transfered Cash: "))
                    name = ''.join(a[6].split("Customer: "))
                    if has_or_not == "True":
                        has.append(name)
                    else:
                        has_not.append(name)
    print(f"{colours.LightGreen}Transfered:{colours.ENDC}")
    for name in has:
        print(f"{colours.LightBlue}\t%s{colours.ENDC}" % name)
    print(f"{colours.Red}Has Not Transfered:{colours.ENDC}")
    for name in has_not:
        print(f"{colours.LightBlue}\t%s{colours.ENDC}" % name)
    input("(enter to continue...)")



