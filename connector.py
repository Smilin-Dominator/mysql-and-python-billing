import getpass
import hashlib
import mysql.connector
import logging
import time
import os

log_format = '%(asctime)s (%(filename)s): %(message)s'   # this basically says that the time and date come first, error next
logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

mydb = mysql.connector.connect(
    auth_plugin='mysql_native_password',
    host="178.79.168.171",
    user="smilin_dominator",
    password="Barney2356",
    database='miscellaneous'
)  # connection time..

BUF_SIZE = 65536
customerName = input("Customer: ")  # Optional, if you're in a hurry, just leave blank
if not customerName:  # ' ' => blank
    customerName = '(Not Specified)'
logging.info(f"\nSold the following to {customerName}")  # you'll see this often, in case any bills go missing
                                                         # logs are the go-to place

myFormat = "{:<25}{:<15}{:<15}{:<15}"  # format for the .format() :)
fileHeaderFormat = "{:^70}" # headers
varTime = time.strftime("%d_of_%B")


class printingBills(object):

    def __init__(self, ar, myFormat, file):
        self.ar = ar
        self.form = myFormat
        self.formPrep = self.form.format('Name', 'Price (Rs.)', 'Quantity', 'Total (Rs.)')
        self.file = file

    def print_bill_items(self):
        print(f'\n{self.formPrep}')
        for i in range(len(self.ar)):
            final = self.form.format(self.ar[i][0], self.ar[i][1], self.ar[i][2], self.ar[i][3])
            print(final)
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
        if self.file == 'none':
            return f"Subtotal: Rs. {tot}"
        else:
            return tot


def update_list(ar):
    print(printingBills(ar, myFormat, 'none').print_bill_items())
    theLoop = True
    while theLoop:
        try:
            updateValue = input("What Would You Like To Update? (Name): ")
            tempList = [list(tup) for tup in ar]
            for i in range(len(tempList)):
                up_name = tempList[i][0]
                if updateValue == up_name:
                    update_key = input("Add Or Remove How Much? (+ amount/ - amount): ")
                    update_key_check = (update_key.split(' '))
                    upQuan = int(update_key_check[1])
                    oldQuan = tempList[i][2]
                    if update_key_check[0] == '+':
                        newQuan = upQuan + oldQuan
                        newTot = newQuan * tempList[i][1]
                        tempList[i][2] = newQuan
                        tempList[i][3] = newTot
                        logging.info(
                            f"Updated: {updateValue}, {ar[i][1]}\nSet Quantity {oldQuan} => {newQuan}\nUpdated Total => {newTot}")
                        ar = [tuple(entry) for entry in tempList]
                    elif update_key_check[0] == '-':
                        newQuanCheck = oldQuan - upQuan
                        if newQuanCheck > 0:
                            newQuan = newQuanCheck
                        else:
                            print("[ The Value Is Either Negative or 0, And Will Be Set To 1 ]")
                            print("[ If Your Intention Was To Delete This, Use The 'del' Command Instead ]")
                            confirm = input("Proceed? (Y/N): ")
                            if confirm == 'Y':
                                logging.warning(f"Set {updateValue}, {ar[i][1]}'s Quantity to 1")
                                newQuan = 1
                            elif confirm == 'N':
                                logging.warning(f"Didn't Change {updateValue}, {ar[i][1]}'s Quantity")
                                newQuan = oldQuan
                        newTot = newQuan * tempList[i][1]
                        tempList[i][2] = newQuan
                        tempList[i][3] = newTot
                        logging.info(
                            f"Updated: {updateValue}, {ar[i][1]}\nSet Quantity {oldQuan} => {newQuan}\nUpdated Total => {newTot}")
                    elif update_key_check[0] == 'exit':
                        break
                    print("Success!")
                    break
            return [tuple(entry) for entry in tempList]
        except Exception as e:
            logging.error(e)
            theLoop = True


def delete_from_list(ar):
    print(printingBills(ar, myFormat, 'none').print_bill_items())
    theLoop = True
    while theLoop:
        try:
            delKey = input("The (Name) To Be Removed: ")
            if delKey == 'abort':
                print("Aborting...")
                break
            else:
                for i in range(len(ar)):
                    if ar[i][0] == delKey:
                        popTime = ar[i]
                        ar.remove(popTime)
                        break
                print("\nSuccess! Type  '--' in the ID prompt To See The Updated Version!")
                logging.info(f"Successfully Deleted Entry {delKey}")
                theLoop = False
        except Exception as e:
            logging.error(e)
            print("[ Error Occurred, Please Retry ]")
            theLoop = True
    return ar


def kill_this():
    killPass = str(getpass.getpass("Enter Password: "))
    pass_read = open('./passwd.txt', 'r')
    check_pass_file = pass_read.read().split(',')
    salt1 = check_pass_file[0]
    salt2 = check_pass_file[1]
    hash_check = check_pass_file[2]
    pass_check = salt1 + killPass + salt2
    pass_hash = hashlib.sha512(pass_check.encode()).hexdigest()
    if hash_check == pass_hash:
        quit()
    else:
        print("\n[ Wrong Password ]\n")  # thats the wrong number! (ooohhhh)


def bill_write(ar):
    fileTime = str(time.strftime('%I.%M_%p'))  # eg: 07.10 PM
    customerNameFormat = customerName.replace(' ', '_')
    fileName = f"[BILL]-{customerNameFormat}-{fileTime}.txt"  # format of the filename
    filePath = os.path.join(f'./bills/{varTime}', fileName)  # adds it into the bills DIR
    fileOpen = open(filePath, 'w+')  # Opens the bill file for writing

    print_the_values = printingBills(ar, myFormat, 'none')
    print(print_the_values.print_bill_items())

    fileOpen.write(f"{fileHeaderFormat.format(70 * '-')}")
    fileOpen.write(f"\n{fileHeaderFormat.format('Paddy Enterprises (Pvt) Ltd.')}")
    fileOpen.write(f"\n{fileHeaderFormat.format(70 * '-')}")
    fileOpen.write(f'\n\nDate: {str(time.strftime("%d/%m/%Y"))}')  # eg: 02/05/2021
    fileOpen.write(f'\nTime: {str(fileTime.replace("_", " "))}')  # uses the variable set earlier
    fileOpen.write(f'\nCustomer: {customerName.replace("_", " ")}\n')

    write_the_values = printingBills(ar, myFormat, fileOpen)
    write_the_values.write_bill_items()

    var_tot = printingBills(ar, myFormat, 'var').print_total()
    print(printingBills(ar, myFormat, 'none').print_total())
    fileOpen.write(f'\n\nSubtotal: Rs. {str(var_tot)}')
    logging.info(f'Subtotal: Rs. {var_tot}')  # Three simultaneous actions here lol

    passOff = False
    while not passOff:
        discountInput = float(input("Discount (%): "))
        if discountInput >= 0:
            discountAmount = var_tot * (discountInput / 100)
            discountSum = var_tot - discountAmount
            if discountSum >= 0:
                discountTotal = round(discountSum, 2)
                print(f"Discount Amount: Rs. {round(discountAmount, 2)}")
                print(f"Subtotal w/ Discount: Rs. {round(discountTotal, 2)}")
                fileOpen.write(f"\nDiscount: {discountInput}%")
                fileOpen.write(f"\nDiscount Amount: Rs. {round(discountAmount, 2)}")
                fileOpen.write(f"\nSubtotal w/ Discount: Rs. {round(discountTotal, 2)}")
                logging.info(f"Discount: {discountInput}%")
                logging.info(f"Discount Amount: Rs. {round(discountAmount, 2)}")
                logging.info(f"Subtotal w/ Discount: Rs. {round(discountTotal, 2)}")
                passOff = True
            else:
                print("[ Try Again, The Discount Sum is Negative ]")
                logging.warning("Entered Incorrect Discount %")
                passOff = False
        else:
            print("[ Try Again, Its Either 0 or An Integer ]")
            logging.warning("Entered Incorrect Discount %")
            passOff = False
    vatAmount = discountTotal * (15 / 100)
    finalTotal = discountTotal + vatAmount
    print(f"Tax: Rs. {vatAmount}")
    print(f"Grand Total: Rs. {finalTotal}")
    logging.info(f"Tax: Rs. {vatAmount}")
    logging.info(f"Grand Total: Rs. {finalTotal}")
    fileOpen.write(f"\nTax : Rs. {vatAmount}")
    fileOpen.write(f"\nGrand Total: Rs. {finalTotal}")
    passOff = False
    while not passOff:
        cashGiven = int(input('Cash Given: Rs. '))
        bal = int(cashGiven - finalTotal)
        if bal < 0:  # loops if its a negative number!
            print("Negative Value, Something's Off, Retry")  # something's **really** off (why doesnt MD work?)
            logging.warning('Negative Balance')
            passOff = False
        elif bal == 0:
            logging.info(f'Cash Given: Rs. {cashGiven}')
            fileOpen.write(f'\n\nCash Given: Rs. {cashGiven}')
            print('\nNo Balance!')
            logging.info('No Balance')
            fileOpen.write(f'\nNo Balance!')
            break  # passes if its not
        elif bal > 0:
            logging.info(f'Cash Given: Rs. {cashGiven}')
            fileOpen.write(f'\nCash Given: Rs. {cashGiven}')
            print(f'Balance: Rs. {bal}')
            logging.info(f'Balance: Rs. {str(bal)}\n')
            fileOpen.write(f'\nBalance: Rs. {bal}')
            break
    input("\n(enter) to proceed...")
    quit()


def appending_to_ar(name, price, quantity, total):
    tuppence = (name, price, quantity, total)
    # and now its done.... (suspense)
    logging.info(  # have to have a backup:)
        f'Sold {quantity} Of Item;\n\nName: {name}\nPrice: {price}\n\nbringing the total to Rs. {total}'
    )
    return tuppence


def main():
    idInput = 69420666  # well, had to declare it as something -\_/-
    ar = []  # declared as empty, will get filled in the process
    while idInput != ' ':
        try:
            idInput = input("\nID: ")  # ID As In The First Column
            if '' == idInput:  # if you just hit enter
                bill_write(ar)
            elif idInput == 'Kill':  # had to add an emergency kill function :)
                kill_this()
            elif idInput == 'del':
                ar = delete_from_list(ar)
            elif idInput == '--':
                print(printingBills(ar, myFormat, 'none').print_bill_items())
                print(printingBills(ar, myFormat, 'none').print_total())
            elif idInput == 'update':
                ar = update_list(ar)
            else:
                proceed = int(idInput)
                sql_select_Query = f"select * from paddigurlTest WHERE id = {proceed}"  # This Will Be Sent To The Database
                cursor = mydb.cursor()  # This Is As If You Were Entering It Yourself
                cursor.execute(sql_select_Query)  # Executes
                records = cursor.fetchall()  # Gets All The Outputs
                if records:  # Basically proceeds if its not empty like []
                    quantity = int(input("Quantity: "))
                    for row in records:
                        name = row[1]  # gets the element from the data
                        price = row[2]  # and its in a fixed format, which is what matters
                        print(f"\nName  : {name}")
                        print(f"Price : {price}")
                        total = int(price) * quantity
                        if len(ar) > 0:
                            tempList = [list(item) for item in ar]  # converts into a list, since you cant change tuples
                            for i in range(len(tempList)):
                                checkName = tempList[i][0]
                                checkPrice = tempList[i][1]
                                if checkName == name and checkPrice == price:
                                    print("\nDuplicate Detected, Updating Current Entry")
                                    currentTotal = tempList[i][3]
                                    currentQuantity = tempList[i][2]
                                    newTotal = int(price) * quantity + currentTotal
                                    newQuantity = int(currentQuantity) + quantity
                                    try:
                                        tempList[i][3] = newTotal
                                        tempList[i][2] = newQuantity
                                        print("Success!")
                                        logging.info(f"Updated: {checkName}, {checkPrice}\nSet Quantity {currentQuantity} => {newQuantity}\nSet Total: {currentTotal} => {newTotal}")
                                        ar = [tuple(entry) for entry in tempList]
                                        break
                                    except Exception as e:
                                        logging.error(e)
                                        break
                            else:
                                ar.append(appending_to_ar(name, price, quantity, total))
                        else:
                            ar.append(appending_to_ar(name, price, quantity, total))
                else:
                    print("\nDid You Enter The Right ID / Command?")  # congratulations! you're a failure!
                    logging.warning(f"Entered Wrong ID / CMD: {idInput}")
        except Exception as rim:
            logging.error(rim)  # rim alert

main()
