from dataclasses import dataclass
import hashlib
import logging
import time
import os
from configuration import variables, input, print, info, warning, console
from rich.table import Table
from pytablewriter import MarkdownTableWriter

logging.basicConfig(filename='log.txt', format=variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                    level=logging.DEBUG)

BUF_SIZE = 65536


def startup():
    nameOfCustomer = input(f"Customer", override="white")  # Optional, if you're in a hurry, leave blank
    if not nameOfCustomer:  # ' ' => blank
        nameOfCustomer = '(Not Specified)'
    logging.info(f"\nSold the following to {nameOfCustomer}")  # you'll see this often, in case any bills go missing
    return nameOfCustomer
    # logs are the go-to place


fileHeaderFormat = "{:^70}"  # headers
varTime = time.strftime("%d_of_%B")


# --------------------------------------- Bill Related Functions ---------------------------------------#


class printingBills(object):

    def __init__(self, ar: list[tuple[str, int, int]] = None, file = None):
        self.ar = ar
        self.file = file

    def print_bill_items(self) -> None:

        table = Table()

        table.add_column("Name", style="magenta")
        table.add_column("Price", style="cyan")
        table.add_column("Quantity", style="green")
        table.add_column("Total", style="red")

        for i in range(len(self.ar)):
            table.add_row(self.ar[i][0], str(self.ar[i][1]), str(self.ar[i][2]), str(self.ar[i][3]))

        table.add_row("", "", "", "")
        table.add_row("Subtotal", "", "", str(self.print_total()))

        console.print(table)

    def write_bill_items(self) -> None:
        table = MarkdownTableWriter(
            headers=["Name", "Price", "Quantity", "Total"],
            value_matrix=self.ar
        )
        self.file.write("\n")
        table.stream = self.file
        table.write_table()

    def print_total(self) -> int:
        tot = 0
        price_unchained = []  # blank array, like the earlier one
        for i in range(len(self.ar)):
            fin = int(self.ar[i][3])
            price_unchained.append(fin)  # appends to the array
        for i in range(0, len(price_unchained)):
            tot = tot + price_unchained[i]  # paradox alert! this variable is dynamic, it remembers the past state.
        return tot


def bill_write(ar: list, transfer: bool, vat: bool, discount: bool):
    fileTime = str(time.strftime('%I.%M_%p'))  # eg: 07.10 PM
    customerNameFormat = customerName.replace(' ', '_')
    fileName = f"[BILL]-{customerNameFormat}-{fileTime}.md"  # format of the filename
    filePath = os.path.join(f'./bills/{varTime}', fileName)  # adds it into the bills DIR
    fileOpen = open(filePath, 'w+')  # Opens the bill file for writing

    print_the_values = printingBills(ar)
    print_the_values.print_bill_items()

    fileOpen.write(f"{fileHeaderFormat.format(70 * '-')}")
    fileOpen.write(f"\n{fileHeaderFormat.format('Paddigurl Dolls')}")
    fileOpen.write(f"\n{fileHeaderFormat.format(70 * '-')}")
    fileOpen.write(f'\n\n**Date: <span style="color:blue">{str(time.strftime("%d/%m/%Y"))}</span>**<br>')  # eg: 02/05/2021
    fileOpen.write(f'\n**Time: <span style="color:red">{str(fileTime.replace("_", " "))}</span>**<br>')  # uses the variable set earlier
    fileOpen.write(f'\n**Customer: <span style="color:green">{customerName.replace("_", " ")}</span>**<br>\n')

    write_the_values = printingBills(ar, fileOpen)
    write_the_values.write_bill_items()

    var_tot = printingBills(ar).print_total()
    print(f"Subtotal: Rs. {var_tot}", override='red')
    fileOpen.write(f'\n\n**Subtotal: <span style="color:orange">Rs. {str(var_tot)}</span>**<br>')
    logging.info(f'Subtotal: Rs. {var_tot}')  # Three simultaneous actions here lol

    """
    If discount is true, it'll show the discount interface
    This also loops until the balance is greater than or equal to 0
    If it's false, it sets the Discount Total to the First Total
    
    And then there's VAT. If you enable vat, it'll calculate 15% of the Discounted Total and add it
    to the total.
    """
    discountTotal = var_tot
    if discount:
        passOff = False
        while not passOff:
            discountInput = float(input(f"Discount (%)", override="yellow"))
            if discountInput >= 0:
                discountAmount = var_tot * (discountInput / 100)
                discountSum = var_tot - discountAmount
                if discountSum >= 0:
                    discountTotal = round(discountSum, 2)
                    print(f"Discount Amount: Rs. {round(discountAmount, 2)}", override='green')
                    print(f"Subtotal w/ Discount: Rs. {round(discountTotal, 2)}", override='teal')
                    fileOpen.write(f"\n**Discount: <span style='color:orange'>{discountInput}%</span>**<br>")
                    fileOpen.write(f"\n**Discount Amount: Rs. <span style='color:red'>{round(discountAmount, 2)}</span>**<br>")
                    fileOpen.write(f"\n**Subtotal w/ Discount: Rs. <span style='color:magenta'>{round(discountTotal, 2)}</span>**<br>")
                    logging.info(f"Discount: {discountInput}%")
                    logging.info(f"Discount Amount: Rs. {round(discountAmount, 2)}")
                    logging.info(f"Subtotal w/ Discount: Rs. {round(discountTotal, 2)}")
                    passOff = True
                else:
                    warning("[ Try Again, The Discount Sum is Negative ]", override="red")
                    logging.warning("Entered Incorrect Discount %")
                    passOff = False
            else:
                warning("[ Try Again, Its Either 0 or An Integer ]", override="red")
                logging.warning("Entered Incorrect Discount %")
                passOff = False

    if vat:
        vatAmount = discountTotal * (15 / 100)
        print(f"Tax: Rs. {vatAmount}", override='magenta')
        fileOpen.write(f"\n**Tax : Rs. <span style='color:cyan'>{vatAmount}</span>**<br>")
        finalTotal = discountTotal + vatAmount
    else:
        finalTotal = discountTotal

    print(f"Grand Total: Rs. {finalTotal}", override="green")
    logging.info(f"Grand Total: Rs. {finalTotal}")
    fileOpen.write(f"\n**Grand Total: <span style='color:yellow'>Rs. {finalTotal}</span>**<br>")
    passOff = False

    """
    In the following section, it says Transfer or not transfer.
    If it's not transfer, it'll calculate the balance, and will loop until the balance is either 0 or negative.
    In the transfer mode, you just select if they have or haven't transfered
    """

    if not transfer:
        while not passOff:
            cashGiven = int(input(f'Cash Given (Rs.)', override="green"))
            bal = int(cashGiven - finalTotal)
            if bal < 0:  # loops if its a negative number!
                warning("Negative Value, Something's Off, Retry", override="red")  # something's **really** off (why doesnt MD work?)
                logging.warning('Negative Balance')
                passOff = False
            elif bal == 0:
                logging.info(f'Cash Given: Rs. {cashGiven}')
                fileOpen.write(f'\n**Cash Given: Rs. <span style="color:orange">{cashGiven}</span>**<br>')
                print('\nNo Balance!', override='green')
                logging.info('No Balance')
                fileOpen.write(f'\n**Balance: <span style="color:red">No Balance!</span>**<br>')
                break  # passes if its not
            elif bal > 0:
                logging.info(f'Cash Given: Rs. {cashGiven}')
                fileOpen.write(f'\n**Cash Given: Rs. <span style="color:orange">{cashGiven}</span>**<br>')
                print(f'Balance: Rs. {bal}', override="green")
                logging.info(f'Balance: Rs. {str(bal)}\n')
                fileOpen.write(f'\n**Balance: <span style="color:red">Rs. {bal}</span>**<br>')
                break
    else:
        hasOrHasnt = input(f'Has Transfered (y/n)', override="red")
        if hasOrHasnt == "y":
            fileOpen.write(f'\n**Transfered Cash: <span style="color:magenta">True</span>**<br>')
        else:
            fileOpen.write(f'\n**Transfered Cash: <span style="color:magenta">False</span>**<br>')
    fileOpen.flush()
    fileOpen.close()
    input("\n(enter) to proceed...")


# ------------------------------------- Miscellaneous Functions -------------------------------------------#


def kill_this():
    killPass = input("Master Password", override="red", password=True)
    pass_read = open('./credentials/passwd.txt', 'r')
    check_pass_file = pass_read.read().split(',')
    salt1 = check_pass_file[0]
    salt2 = check_pass_file[1]
    hash_check = check_pass_file[2]
    pass_check = salt1 + killPass + salt2
    pass_hash = hashlib.sha512(pass_check.encode()).hexdigest()
    if hash_check == pass_hash:
        return True
    else:
        print("\n[ Wrong Password ]\n")  # thats the wrong number! (ooohhhh)
        return False


# ------------------------------------------ Array Related Functions ----------------------------------------------#

@dataclass
class Doll:

    Name: str
    Price: int
    Quantity: int = None
    Total: int = None

    def to_tuple(self) -> tuple[str | int, ...]:
        return tuple([self.Name, self.Price, self.Quantity, self.Total])


class array_funcs(object):

    def __init__(self, ar: list[tuple[str, int, int]]):
        self.ar = ar

    def duplicate_check(self, doll: Doll):
        ar = self.ar
        quantity = int(input(f"Quantity", override="yellow"))
        print(f"\nName  : {doll.Name}", override="light_steel_blue1")
        print(f"Price : {doll.Price}", override="light_steel_blue1")
        total = int(doll.Price) * quantity
        if len(ar) > 0:
            tempList = [list(item) for item in ar]  # converts into a list, since you cant change tuples
            for _, item in enumerate(tempList):
                doll2 = Doll(item[0], item[1])
                if (doll2.Name == doll.Name) and (doll2.Price == doll.Price):
                    info(f"\nDuplicate Detected, Updating Current Entry", override="teal")
                    doll2.Total = item[3]
                    doll2.Quantity = item[2]
                    newTotal = doll2.Price * quantity + doll2.Total
                    newQuantity = doll2.Quantity + quantity
                    try:
                        newDoll = Doll(doll.Name, doll.Price, newQuantity, newTotal)
                        info(f"Success!", override="green_yellow")
                        logging.info(
                            f"Updated: {newDoll.Name}, {newDoll.Price}\nSet Quantity {doll2.Quantity} => "
                            f"{newQuantity}\nSet Total: {doll2.Total} => {newTotal}"
                        )
                        tempList[tempList.index(item)] = newDoll.to_tuple()
                        ar = [tuple(entry) for entry in tempList]
                        self.ar = ar
                        break
                    except Exception as e:
                        logging.error(e)
            else:
                doll.Quantity = quantity
                doll.Total = doll.Price * doll.Quantity
                self.ar.append((doll.Name, doll.Price, doll.Quantity, doll.Total))
        else:
            doll.Quantity = quantity
            doll.Total = doll.Price * doll.Quantity
            self.ar.append((doll.Name, doll.Price, doll.Quantity, doll.Total))

    def update_list(self):
        ar = self.ar
        printingBills(ar).print_bill_items()
        theLoop = True
        while theLoop:
            try:
                updateValue = input(f"What Would You Like To Update? (Name)", override="dark_olive_green2")
                tempList = [list(tup) for tup in ar]
                for _, item in enumerate(tempList):
                    up_name = item[0]
                    if updateValue == up_name:
                        update_key = input(
                            f"Add Or Remove How Much? (+ amount/ - amount)", override="white"
                        )
                        update_key_check = (update_key.split(' '))
                        upQuan = int(update_key_check[1])
                        oldQuan = item[2]
                        if update_key_check[0] == '+':
                            newQuan = upQuan + oldQuan
                            newTot = newQuan * item[1]
                            item[2] = newQuan
                            item[3] = newTot
                            logging.info(
                                f"Updated: {updateValue}, {ar[1]}\nSet Quantity {oldQuan} => "
                                f"{newQuan}\nUpdated Total {item[3]} => {newTot}"
                            )
                            ar = [tuple(entry) for entry in tempList]
                        elif update_key_check[0] == '-':
                            newQuanCheck = oldQuan - upQuan
                            if newQuanCheck > 0:
                                newQuan = newQuanCheck
                            else:
                                warning(f"[ The Value Is Either Negative or 0, And Will Be Set To 1 ]\n"
                                        f"[ If Your Intention Was To Delete This, Use The 'del' Command Instead ]"
                                        , override="red")
                                confirm = input(f"Proceed? (Y/N)", override="yellow")
                                if confirm == 'Y':
                                    logging.warning(f"Set {updateValue}, {item[1]}'s Quantity to 1")
                                    newQuan = 1
                                else:
                                    logging.warning(f"Didn't Change {updateValue}, {item[1]}'s Quantity")
                                    newQuan = oldQuan
                            newTot = newQuan * item[1]
                            item[2] = newQuan
                            item[3] = newTot
                            logging.info(
                                f"Updated: {updateValue}, {item[1]}\nSet Quantity {oldQuan} => {newQuan}\n"
                                f"Updated Total => {newTot}"
                            )
                        elif update_key_check[0] == 'exit':
                            break
                        info(f"Success!", override="honeydew2")
                        break
                self.ar = [tuple(entry) for entry in tempList]
                break
            except Exception as e:
                logging.error(e)
                theLoop = True

    def delete_from_list(self):
        ar = self.ar
        printingBills(ar).print_bill_items()
        theLoop = True
        while theLoop:
            try:
                delKey = input(f"The (Name) To Be Removed", override="red")
                if delKey == 'abort':
                    warning(f"Aborting...", override="light_salmon3")
                    break
                else:
                    for _, item in enumerate(ar):
                        if item[0] == delKey:
                            popTime = item
                            ar.remove(popTime)
                            break
                    info(
                        f"Success! Type  '--' in the ID prompt To See The Updated Version!", override="green"
                    )
                    logging.info(f"Successfully Deleted Entry {delKey}")
                    theLoop = False
            except Exception as e:
                logging.error(e)
                info(f"[ Error Occurred, Please Retry ]", override="red")
                theLoop = True
        self.ar = ar

    def get(self):
        return self.ar


# -------------------------------------------- Main Code --------------------------------------------------#

def main(transfer, mydb, vat, discount):
    global customerName
    customerName = startup()
    idInput = 69420666  # well, had to declare it as something -\_/-
    ar = array_funcs([])  # declared as empty, will get filled in the process
    while idInput != ' ':
        try:
            ar = array_funcs(ar.get())
            idInput = input(f"\nID", override="light_cyan3")  # ID As In The First Column
            match idInput:
                case "":  # if you just hit enter
                    bill_write(ar.get(), transfer, vat, discount)
                    break
                case 'Kill':  # had to add an emergency kill function :)
                    go = kill_this()
                    if go:
                        break
                case 'del':
                    ar.delete_from_list()
                case '--':
                    printingBills(ar.get()).print_bill_items()
                case 'update':
                    ar.update_list()
                case _:
                    proceed = int(idInput)
                    sql_select_Query = f"select * from paddigurlTest WHERE id = {proceed}"  # Sent To The Database
                    cursor = mydb.cursor()  # This Is As If You Were Entering It Yourself
                    cursor.execute(sql_select_Query)  # Executes
                    records = cursor.fetchall()[0]  # Gets All The Outputs
                    if records:  # Basically proceeds if its not empty like []
                        doll = Doll(records[1], records[2])
                        ar.duplicate_check(doll)
                    else:
                        warning(
                            f"\nDid You Enter The Right ID / Command?", override="red")  # congratulations!
                        # you're a failure!
                        logging.warning(f"Entered Wrong ID / CMD: {idInput}")
        except Exception as rim:
            logging.error(rim)  # rim alert
