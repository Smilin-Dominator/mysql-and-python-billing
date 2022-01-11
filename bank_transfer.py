from os import listdir
from configuration import Errors, input, warning, error, print
from verify import hash_file
from bill_extractor import bill


def view_bank_transactions():
    has = []
    has_not = []
    files = []
    combined = []
    file_prefix = "./bills/%s/%s"
    dir_prefix = "./bills/%s"
    for d in listdir("./bills/"):
        for file in listdir(dir_prefix % d):
            if file.endswith(".md"):
                with open(file_prefix % (d, file), "r") as f:
                    b = bill(f)
                    has_or_not = b.transferred()
                    name = b.customer()
                    time = b.time()
                    if has_or_not:
                        files.append(file_prefix % (d, file))
                        if name in combined:
                            name = name + " - " + time
                        has.append(name)
                        combined.append(name)
                    elif not has_or_not:
                        files.append(file_prefix % (d, file))
                        if name in combined:
                            name = name + " - " + time
                        has_not.append(name)
                        combined.append(name)
                    elif has_or_not is None:
                        pass
    print(f"[green]Transferred:[/green]")
    for name in has:
        print(f"[blue]\t%s[/blue]" % name)
    print(f"[red]Has Not Transferred:[/red]")
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
                con.append(f'**Transferred Cash: <span style="color:magenta">{choice}</span>**<br>')
            with open(file, "w") as fil:
                fil.write("\n".join(con))
                fil.close()
            new_hash = hash_file(file)
            new_contents = "\n".join(con)
            string = "UPDATE `paddigurlHashes` SET `hash` = %s, `filecontents` = %s WHERE `filepath` = %s"
            values = [new_hash, new_contents, file]
            mycursor.execute(string, values)
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
        raise Errors.ValueErrors("Expected Integer")
