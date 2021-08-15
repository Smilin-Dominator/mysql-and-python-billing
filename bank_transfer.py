import os
from configuration import colours, errors


def view_bank_transactions():
    has = []
    has_not = []
    files = []
    combined = []
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
                        files.append(file_prefix % (d, file))
                        combined.append(name)
                    else:
                        has_not.append(name)
                        files.append(file_prefix % (d, file))
                        combined.append(name)
    print(f"{colours.LightGreen}Transfered:{colours.ENDC}")
    for name in has:
        print(f"{colours.LightBlue}\t%s{colours.ENDC}" % name)
    print(f"{colours.Red}Has Not Transfered:{colours.ENDC}")
    for name in has_not:
        print(f"{colours.LightBlue}\t%s{colours.ENDC}" % name)
    return [combined, files]


def edit_bank_transactions():
    names, files = view_bank_transactions()
    name = input("Which Transaction Would You Like To Change (name): ")
    if name in names:
        choice = int(input("[+] Has Transferred or Hasn't Transfered? (1/2): "))
        if choice == 1:
            choice = "True"
        else:
            choice = "False"
        n = names.index(name)
        file = files[n]
        with open(file, "r") as fil:
            con = fil.read().splitlines()
            con.pop()
            con.append(f"Transfered Cash: {choice}")
        with open(file, "w") as fil:
            fil.write("\n".join(con))
            fil.close()
    else:
        print("[*] Invalid Name!")


def interface():
    try:
        choice = int(input(f"{colours.Yellow}[*] View Transactions or Edit Transactions? (1/2): "))
        if choice == 1:
            view_bank_transactions()
        else:
            edit_bank_transactions()
    except ValueError:
        raise errors.valueErrors("Expected Integer")
