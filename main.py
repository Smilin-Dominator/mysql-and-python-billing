# This Program was made by the one and only
# Devisha Padmaperuma!

import os
import random

key = 2
while key == 2:
    print("Welcome! If Something Doesn't Seem Right, Check The Logs!\n")
    messageOfTheSecond = {
        1: "Nobody Pray for Me, It Been That Day For Me, Yeah!",
        2: "I remember syrup sandwiches and crime allowances",
        3: "Pull up to your block, and break it, now we playing Tetris",
        4: "AM to the PM, PM to the AM rock.",
        5: "If I quit your BM, I still ride Mercedes.",
        6: "If I quit the Season, I still be the greatest",
    }
    randomNumGen = random.randint(1, len(messageOfTheSecond) + 1)
    print(f"Message Of The Second: {messageOfTheSecond[randomNumGen]}")
    check = os.path.exists('bills/')
    if check == False:
        print("Bills DIR not Found, Creating....")
        os.mkdir("bills/")
        print('Success!\n')
    else:
        print("Bills DIR Found..Proceeding...\n")
    os.system('connector.py')
    key = int(input("Would You Like To Stop, Or Continue? (1/2)\n: "))
    if key == 1:
        os.remove('tmp.txt')
        quit()