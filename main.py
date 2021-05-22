import os

key = 2
while key == 2:
    print('Welcome! To The Terminal! ')
    os.system('price.py')
    key = int(input("Would You Like To Stop, Or Continue? (1/2)\n: "))
    if key == 1:
        os.remove('tmp.txt')
        quit()