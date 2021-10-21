import os
from configuration import errors, input, warning, error, print
from verify import hash_file


def view_bank_transactions():
    has = []
    has_not = []
    files = []
    combined = []
    file_prefix = "./bills/%s/%s"
    dir_prefix = "./bills/%s"
    for d in os.listdir("./bills/"):
        for file in os.listdir(dir_prefix % d):
            with open(file_prefix % (d, file), "r") as f:
                a = f.read().splitlines()
                has_or_not = a[len(a) - 1]
                if has_or_not.startswith("Transfered Cash: "):
                    has_or_not = ''.join(has_or_not.split("Transfered Cash: "))
                    name = ''.join(a[6].split("Customer: "))
                    time = ''.join(a[5].split("Time: "))
                    if has_or_not == "True":
                        files.append(file_prefix % (d, file))
                        if name in combined:
                            name = name + " - " + time
                        has.append(name)
                        combined.append(name)
                    else:
                        files.append(file_prefix % (d, file))
                        if name in combined:
                            name = name + " - " + time
                        has_not.append(name)
                        combined.append(name)
    print(f"[green]Transfered:[/green]")
    for name in has:
        print(f"[blue]\t%s[/blue]" % name)
    print(f"[red]Has Not Transfered:[/red]")
    for name in has_not:
        print(f"[blue]\t%s[/blue]" % name)
    return [combined, files]


def edit_bank_transactions(mycursor, mydb):
    names, files = view_bank_transactions()
    try:
        name = input(f"Which Transaction Would You Like To Change (name)", "white")
        if name in names:
            choice = int(input(f"Has Transferred or Hasn't Transfered? (1/2)", "green"))
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
            new_hash = hash_file(file)
            new_contents = "\n".join(con)
            string = "UPDATE `paddigurlHashes` SET hash = \"%s\", filecontents = \"%s\" WHERE filepath = \"%s\"" % (new_hash, new_contents, file)
            mycursor.execute(string)
            mydb.commit()
            with open("credentials/hashes.txt", "r") as r:
                lines = r.read().splitlines()
                for line in lines:
                    values = line.split(",")
                    if values[0] == file:
                        lines.remove(line)
                        lines.append("%s,%s" % (file, new_hash))
                r.close()
            with open("credentials/hashes.txt", "w") as w:
                w.write("\n".join(lines))
        else:
            warning(f"Invalid Name!")
    except KeyboardInterrupt:
        error(f"Successfully Aborted!")


def interface(mycursor, mydb):
    try:
        choice = int(input(f"View Transactions or Edit Transactions? (1/2)", "yellow"))
        if choice == 1:
            view_bank_transactions()
        else:
            edit_bank_transactions(mycursor, mydb)
    except ValueError:
        raise errors.valueErrors("Expected Integer")
