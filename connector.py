import getpass
import hashlib
import logging
import time
import os
from configuration import colours, variables

logging.basicConfig(filename='log.txt', format=variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                    level=logging.DEBUG)

BUF_SIZE = 65536


def startup():
    nameOfCustomer = input(f"{colours.White}Customer: {colours.ENDC}")  # Optional, if you're in a hurry, leave blank
    if not nameOfCustomer:  # ' ' => blank
        nameOfCustomer = '(Not Specified)'
    logging.info(f"\nSold the following to {nameOfCustomer}")  # you'll see this often, in case any bills go missing
    return nameOfCustomer
    # logs are the go-to place


myFormat = "{:<25}{:<15}{:<15}{:<15}"  # format for the .format() :)
fileHeaderFormat = "{:^70}"  # headers
varTime = time.strftime("%d_of_%B")


# --------------------------------------- Bill Related Functions ---------------------------------------#


class printingBills(object):

    def __init__(self, ar: list[tuple[str, int, int]] = None, new_format: str = None, file=None):
        self.ar = ar
        self.form = new_format
        self.formPrep = self.form.format('Name', 'Price (Rs.)', 'Quantity', 'Total (Rs.)')
        self.file = file

    def print_bill_items(self):
        print(f'\n{self.formPrep}')
        for i in range(len(self.ar)):
            final = self.form.format(self.ar[i][0], self.ar[i][1], self.ar[i][2], self.ar[i][3])
            print(colours.LightCyan, final, colours.ENDC)
        return ''

    def write_bill_items(self):
        self.file.write(f'\n{self.formPrep}')
        for i in range(len(self.ar)):
            final = self.form.format(self.ar[i][0], self.ar[i][1], self.ar[i][2], self.ar[i][3])
            self.file.write(f'\n{final}')
        return ''

    def print_total(self):
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
    fileName = f"[BILL]-{customerNameFormat}-{fileTime}.txt"  # format of the filename
    filePath = os.path.join(f'./bills/{varTime}', fileName)  # adds it into the bills DIR
    fileOpen = open(filePath, 'w+')  # Opens the bill file for writing

    print_the_values = printingBills(ar, myFormat)
    print(print_the_values.print_bill_items())

    fileOpen.write(f"{fileHeaderFormat.format(70 * '-')}")
    fileOpen.write(f"\n{fileHeaderFormat.format('Paddigurl Dolls - 0777710090')}")
    fileOpen.write(f"\n{fileHeaderFormat.format(70 * '-')}")
    fileOpen.write(f'\n\nDate: {str(time.strftime("%d/%m/%Y"))}')  # eg: 02/05/2021
    fileOpen.write(f'\nTime: {str(fileTime.replace("_", " "))}')  # uses the variable set earlier
    fileOpen.write(f'\nCustomer: {customerName.replace("_", " ")}\n')

    write_the_values = printingBills(ar, myFormat, fileOpen)
    write_the_values.write_bill_items()

    var_tot = printingBills(ar, myFormat).print_total()
    print(f"{colours.Red}Subtotal: Rs. {var_tot}{colours.ENDC}")
    fileOpen.write(f'\n\nSubtotal: Rs. {str(var_tot)}')
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
            discountInput = float(input(f"{colours.LightYellow}Discount (%): {colours.ENDC}"))
            if discountInput >= 0:
                discountAmount = var_tot * (discountInput / 100)
                discountSum = var_tot - discountAmount
                if discountSum >= 0:
                    discountTotal = round(discountSum, 2)
                    print(f"{colours.LightGreen}Discount Amount: Rs. {round(discountAmount, 2)}{colours.ENDC}")
                    print(f"{colours.LightGray}Subtotal w/ Discount: Rs. {round(discountTotal, 2)}{colours.ENDC}")
                    fileOpen.write(f"\nDiscount: {discountInput}%")
                    fileOpen.write(f"\nDiscount Amount: Rs. {round(discountAmount, 2)}")
                    fileOpen.write(f"\nSubtotal w/ Discount: Rs. {round(discountTotal, 2)}")
                    logging.info(f"Discount: {discountInput}%")
                    logging.info(f"Discount Amount: Rs. {round(discountAmount, 2)}")
                    logging.info(f"Subtotal w/ Discount: Rs. {round(discountTotal, 2)}")
                    passOff = True
                else:
                    print(colours.Red, "[ Try Again, The Discount Sum is Negative ]", colours.ENDC)
                    logging.warning("Entered Incorrect Discount %")
                    passOff = False
            else:
                print("[ Try Again, Its Either 0 or An Integer ]")
                logging.warning("Entered Incorrect Discount %")
                passOff = False

    if vat:
        vatAmount = discountTotal * (15 / 100)
        print(f"{colours.LightMagenta}Tax: Rs. {vatAmount}{colours.ENDC}")
        fileOpen.write(f"\nTax : Rs. {vatAmount}")
        finalTotal = discountTotal + vatAmount
    else:
        finalTotal = discountTotal

    print(f"{colours.LightGreen}Grand Total: Rs. {finalTotal}{colours.ENDC}")
    logging.info(f"Grand Total: Rs. {finalTotal}")
    fileOpen.write(f"\nGrand Total: Rs. {finalTotal}")
    passOff = False

    """
    In the following section, it says Transfer or not transfer.
    If it's not transfer, it'll calculate the balance, and will loop until the balance is either 0 or negative.
    In the transfer mode, you just select if they have or haven't transfered
    """

    if not transfer:
        while not passOff:
            cashGiven = int(input(f'{colours.LightRed}Cash Given: Rs. {colours.ENDC}'))
            bal = int(cashGiven - finalTotal)
            if bal < 0:  # loops if its a negative number!
                print(colours.Red, "Negative Value, Something's Off, Retry",
                      colours.ENDC)  # something's **really** off (why doesnt MD work?)
                logging.warning('Negative Balance')
                passOff = False
            elif bal == 0:
                logging.info(f'Cash Given: Rs. {cashGiven}')
                fileOpen.write(f'\n\nCash Given: Rs. {cashGiven}')
                print(colours.Green, '\nNo Balance!', colours.ENDC)
                logging.info('No Balance')
                fileOpen.write(f'\nNo Balance!')
                break  # passes if its not
            elif bal > 0:
                logging.info(f'Cash Given: Rs. {cashGiven}')
                fileOpen.write(f'\nCash Given: Rs. {cashGiven}')
                print(f'{colours.Green}Balance: Rs. {bal}{colours.ENDC}')
                logging.info(f'Balance: Rs. {str(bal)}\n')
                fileOpen.write(f'\nBalance: Rs. {bal}')
                break
    else:
        hasOrHasnt = input(f'{colours.LightRed}Has Transfered (y/n): {colours.ENDC}')
        if hasOrHasnt == "y":
            fileOpen.write(f'\nTransfered Cash: True')
        else:
            fileOpen.write(f'\nTransfered Cash: False')
    input("\n(enter) to proceed...")


# ------------------------------------- Miscellaneous Functions -------------------------------------------#


def kill_this():
    killPass = str(getpass.getpass("Enter Password: "))
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

class array_funcs(object):

    def __init__(self, ar: list[tuple[str, int, int]]):
        self.ar = ar

    def duplicate_check(self, records: list[int, str, int]):
        ar = self.ar
        quantity = int(input(f"{colours.LightYellow}Quantity: {colours.ENDC}"))
        for row in records:
            name = row[1]  # gets the element from the data
            price = row[2]  # and its in a fixed format, which is what matters
            print(f"\n{colours.LightGreen}Name  : {name}{colours.ENDC}")
            print(f"{colours.LightGreen}Price : {price}{colours.ENDC}")
            total = int(price) * quantity
            if len(ar) > 0:
                tempList = [list(item) for item in ar]  # converts into a list, since you cant change tuples
                for i in range(len(tempList)):
                    checkName = tempList[i][0]
                    checkPrice = tempList[i][1]
                    if checkName == name and checkPrice == price:
                        print(f"\n{colours.DarkGray}[!] Duplicate Detected, Updating Current Entry{colours.ENDC}")
                        currentTotal = tempList[i][3]
                        currentQuantity = tempList[i][2]
                        newTotal = int(price) * quantity + currentTotal
                        newQuantity = int(currentQuantity) + quantity
                        try:
                            tempList[i][3] = newTotal
                            tempList[i][2] = newQuantity
                            print(f"{colours.Green}[!] Success!{colours.ENDC}")
                            logging.info(
                                f"Updated: {checkName}, {checkPrice}\nSet Quantity {currentQuantity} => "
                                f"{newQuantity}\nSet Total: {currentTotal} => {newTotal}"
                            )
                            ar = [tuple(entry) for entry in tempList]
                            self.ar = ar
                            break
                        except Exception as e:
                            logging.error(e)
                else:
                    self.ar.append((name, price, quantity, total))
            else:
                self.ar.append((name, price, quantity, total))

    def update_list(self):
        ar = self.ar
        print(printingBills(ar, myFormat).print_bill_items())
        theLoop = True
        while theLoop:
            try:
                updateValue = input(f"{colours.Yellow}[*] What Would You Like To Update? (Name): {colours.ENDC}")
                tempList = [list(tup) for tup in ar]
                for i in range(len(tempList)):
                    up_name = tempList[i][0]
                    if updateValue == up_name:
                        update_key = input(
                            f"{colours.White}[+] Add Or Remove How Much? (+ amount/ - amount): {colours.ENDC}")
                        update_key_check = (update_key.split(' '))
                        upQuan = int(update_key_check[1])
                        oldQuan = tempList[i][2]
                        if update_key_check[0] == '+':
                            newQuan = upQuan + oldQuan
                            newTot = newQuan * tempList[i][1]
                            tempList[i][2] = newQuan
                            tempList[i][3] = newTot
                            logging.info(
                                f"Updated: {updateValue}, {ar[i][1]}\nSet Quantity {oldQuan} => "
                                f"{newQuan}\nUpdated Total {tempList[i][3]} => {newTot}"
                            )
                            ar = [tuple(entry) for entry in tempList]
                        elif update_key_check[0] == '-':
                            newQuanCheck = oldQuan - upQuan
                            if newQuanCheck > 0:
                                newQuan = newQuanCheck
                            else:
                                print(f"{colours.Red}[ The Value Is Either Negative or 0, And Will Be Set To 1 ]")
                                print(
                                    f"[ If Your Intention Was To Delete This, Use The 'del' Command Instead ]{colours.ENDC}")
                                confirm = input(f"{colours.Yellow}[!] Proceed? (Y/N): {colours.ENDC}")
                                if confirm == 'Y':
                                    logging.warning(f"Set {updateValue}, {ar[i][1]}'s Quantity to 1")
                                    newQuan = 1
                                else:
                                    logging.warning(f"Didn't Change {updateValue}, {ar[i][1]}'s Quantity")
                                    newQuan = oldQuan
                            newTot = newQuan * tempList[i][1]
                            tempList[i][2] = newQuan
                            tempList[i][3] = newTot
                            logging.info(
                                f"Updated: {updateValue}, {ar[i][1]}\nSet Quantity {oldQuan} => {newQuan}\n"
                                f"Updated Total => {newTot}"
                            )
                        elif update_key_check[0] == 'exit':
                            break
                        print(f"{colours.LightGreen}[#] Success!{colours.ENDC}")
                        break
                self.ar = [tuple(entry) for entry in tempList]
                break
            except Exception as e:
                logging.error(e)
                theLoop = True

    def delete_from_list(self):
        ar = self.ar
        print(printingBills(ar, myFormat).print_bill_items())
        theLoop = True
        while theLoop:
            try:
                delKey = input(f"{colours.Yellow}[!] The (Name) To Be Removed: {colours.ENDC}")
                if delKey == 'abort':
                    print(f"{colours.LightRed}[!] Aborting...{colours.ENDC}")
                    break
                else:
                    for i in range(len(ar)):
                        if ar[i][0] == delKey:
                            popTime = ar[i]
                            ar.remove(popTime)
                            break
                    print(
                        f"\n{colours.Green}[*] Success! Type  '--' in the ID prompt To See The Updated Version!{colours.ENDC}")
                    logging.info(f"Successfully Deleted Entry {delKey}")
                    theLoop = False
            except Exception as e:
                logging.error(e)
                print(f"{colours.Red}[ Error Occurred, Please Retry ]{colours.ENDC}")
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
            idInput = input(f"\n{colours.LightCyan}ID: {colours.ENDC}")  # ID As In The First Column
            if '' == idInput:  # if you just hit enter
                bill_write(ar.get(), transfer, vat, discount)
                break
            elif idInput == 'Kill':  # had to add an emergency kill function :)
                go = kill_this()
                if go:
                    break
            elif idInput == 'del':
                ar.delete_from_list()
            elif idInput == '--':
                print(printingBills(ar.get(), myFormat).print_bill_items())
                print(
                    f"{colours.LightMagenta}Subtotal: {printingBills(ar.get(), myFormat).print_total()}{colours.ENDC}"
                )
            elif idInput == 'update':
                ar.update_list()
            else:
                proceed = int(idInput)
                sql_select_Query = f"select * from paddigurlTest WHERE id = {proceed}"  # Sent To The Database
                cursor = mydb.cursor()  # This Is As If You Were Entering It Yourself
                cursor.execute(sql_select_Query)  # Executes
                records = cursor.fetchall()  # Gets All The Outputs
                if records:  # Basically proceeds if its not empty like []
                    ar.duplicate_check(records)
                else:
                    print(
                        f"\n{colours.Red}Did You Enter The Right ID / Command?{colours.ENDC}")  # congratulations!
                    # you're a failure!
                    logging.warning(f"Entered Wrong ID / CMD: {idInput}")
        except Exception as rim:
            logging.error(rim)  # rim alert
