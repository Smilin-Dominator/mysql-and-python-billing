import os

key = 2
while key == 2:
    print('Welcome! To The Terminal! ')
    check = os.path.exists('bills/')
    if check == False:
        os.mkdir("bills/")
    os.system('price.py')
    key = int(input("Would You Like To Stop, Or Continue? (1/2)\n: "))
    if key == 1:
        os.remove('tmp.txt')
        quit()