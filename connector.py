import mysql.connector
import logging
import time
import os

log_format = '%(asctime)s : %(message)s'  # this basically says that the time and date come first, error next
logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

mydb = mysql.connector.connect(
    auth_plugin='mysql_native_password',
    host="192.168.10.5",
    user="smilin_dominator",
    password="Barney2356",
    database='miscellaneous'
)  # connection time..

customerName = input("Customer: ")  # Optional, if you're in a hurry, just leave blank
if not customerName:  # ' ' => blank
    customerName = '(Not Specified)'
logging.info(f"\nSold the following to {customerName}")  # you'll see this often, in case any bills go missing
                                                         # logs are the go-to place

myFormat = "{:<25}{:<15}{:<15}{:<15}"  # format for the .format() :)
fileHeaderFormat = "{:^70}"
formPrep = myFormat.format('Name', 'Price (Rs.)', 'Quantity', 'Total (Rs.)')  # headers

idInput = 69420666  # well, had to declare it as something -\_/-
ar = []  # declared as empty, will get filled in the process
while idInput != ' ':
    try:
        idInput = input("\nID: ")  # ID As In The First Column
        if '' == idInput:  # if you just hit enter
            fileTime = str(time.strftime('%I.%M %p'))  # eg: 07.10 PM
            fileName = f"[BILL]-{customerName}-{fileTime}.txt"  # format of the filename
            filePath = os.path.join('./bills', fileName)  # adds it into the bills DIR
            fileOpen = open(filePath, 'w+')  # Opens the bill file for writing
            print('\n')  # just a spacer
            print(formPrep)
            fileOpen.write(f"{fileHeaderFormat.format(70 * '-')}")
            fileOpen.write(f"\n{fileHeaderFormat.format('Paddy Enterprises (Pvt) Ltd.')}")
            fileOpen.write(f"\n{fileHeaderFormat.format(70 * '-')}")
            fileOpen.write(f'\n\nDate: {str(time.strftime("%d/%m/%Y"))}')  # eg: 02/05/2021
            fileOpen.write(f'\nTime: {str(fileTime)}')  # uses the variable set earlier
            fileOpen.write(f'\nCustomer: {customerName}\n')
            fileOpen.write(f'\n{formPrep}')
            for i in range(len(ar)):  # for loop to write the output of each, in the format
                final = myFormat.format(ar[i][0], ar[i][1], ar[i][2], ar[i][3])
                print(final)
                fileOpen.write(f'\n{final}')  # mirrors the print output to the file
            tot = 0
            price_unchained = []  # blank array, like the earlier one
            for i in range(len(ar)):
                fin = int(ar[i][3])
                price_unchained.append(fin)  # appends to the array
            for i in range(0, len(price_unchained)):
                tot = tot + price_unchained[i]  # paradox alert! this variable is dynamic, it remembers the past state.
            print(f'\nSubtotal: Rs. {str(tot)}')
            fileOpen.write(f'\n\nSubtotal: Rs. {str(tot)}')
            logging.info(f'Subtotal: Rs. {tot}')  # Three simultaneous actions here lol
            passOff = False
            while not passOff:
                discountInput = int(input("Discount (%): "))
                if discountInput >= 0:
                    discountSum = tot * (100 - discountInput) / 100
                    if discountSum >= 0:
                        discountTotal = round(discountSum)
                        print(f"Total: Rs. {discountTotal}")
                        fileOpen.write(f"\nDiscount: {discountInput}%")
                        fileOpen.write(f"\nTotal: Rs. {discountTotal}")
                        logging.info(f"Discount: {discountInput}%")
                        logging.info(f"Total: Rs. {discountTotal}")
                        passOff = True
                    else:
                        print("[ Try Again, The Discount Sum is Negative ]")
                        passOff = False
                else:
                    print("[ Try Again, Its Either 0 or An Integer ]")
                    passOff = False
            while not passOff:
                cashGiven = int(input('Cash Given: Rs. '))
                bal = int(cashGiven - discountTotal)
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
            quit()
        elif idInput == 'Kill':  # had to add an emergency kill function :)
            killPass = input("Enter Password: ")
            if killPass == '627905':  # alter the code here if you want
                quit()
            else:
                print("\n[ Wrong Password ]\n")  # thats the wrong number! (ooohhhh)
        elif idInput == 'del':
            print(f"\n{formPrep}")
            for i in range(len(ar)):  # reuse
                final = myFormat.format(ar[i][0], ar[i][1], ar[i][2], ar[i][3])
                print(final)
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
        elif idInput == '--':
            print(f'\n{formPrep}')
            for i in range(len(ar)):  # reuse
                final = myFormat.format(ar[i][0], ar[i][1], ar[i][2], ar[i][3])
                print(final)
            tot = 0
            price_unchained = []  # blank array, like the earlier one
            for i in range(len(ar)):
                fin = int(ar[i][3])
                price_unchained.append(fin)  # appends to the array
            for i in range(0, len(price_unchained)):
                tot = tot + price_unchained[i]  # paradox alert! this variable is dynamic, it remembers the past state.
            print(f'\nTotal: {str(tot)}')
        elif idInput == 'update':
            print(f'\n{formPrep}')
            for i in range(len(ar)):  # reuse
                final = myFormat.format(ar[i][0], ar[i][1], ar[i][2], ar[i][3])
                print(final)
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
                                logging.info(f"Updated: {updateValue}, {ar[i][1]}\nSet Quantity {oldQuan} => {newQuan}\nUpdated Total => {newTot}")
                                ar = [tuple(entry) for entry in tempList]
                            elif update_key_check[0] == '-':
                                newQuanCheck = oldQuan - upQuan
                                if newQuanCheck > 0:
                                    newQuan = newQuanCheck
                                else:
                                    print("[ The Value Is Either Negative or 0, And Has Been Set To 1 ]")
                                    print("[ If Your Intention Was To Delete This, Use The 'del' Command Instead ]")
                                    newQuan = 1
                                newTot = newQuan * tempList[i][1]
                                tempList[i][2] = newQuan
                                tempList[i][3] = newTot
                                logging.info(f"Updated: {updateValue}, {ar[i][1]}\nSet Quantity {oldQuan} => {newQuan}\nUpdated Total => {newTot}")
                                ar = [tuple(entry) for entry in tempList]
                            print("Success!")
                            break
                    break
                except Exception as e:
                    logging.error(e)
                    theLoop = True
        else:
            sql_select_Query = f"select * from paddigurlTest WHERE id = {idInput}"  # This Will Be Sent To The Database
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
                        tempList = [list(item) for item in ar]
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
                            # Appending to the blank array ...
                            tuppence = (name, price, quantity, total)
                            ar.append(tuppence)
                            # and now its done.... (suspense)
                            logging.info(  # have to have a backup:)
                                f'Sold {quantity} Of Item;\n{records}, bringing the total to Rs. {total}'
                            )
                    else:
                        # Appending to the blank array ...
                        tuppence = (name, price, quantity, total)
                        ar.append(tuppence)
                        # and now its done.... (suspense)
                        logging.info(  # have to have a backup:)
                            f'Sold {quantity} Of Item;\n{records}, bringing the total to Rs. {total}'
                        )
            else:
                print("\nDid You Enter The Right ID / Command?")  # congratulations! you're a failure!
                logging.warning(f"Entered Wrong ID: {idInput}")
    except Exception as rim:
        logging.error(rim)  # rim alert
