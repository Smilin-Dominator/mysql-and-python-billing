# This Program was made completely (100%) by the one and only
# Devisha Padmaperuma!
# Don't even think of stealing my code!

import os
import random

print("Welcome! If Something Doesn't Seem Right, Check The Logs!\n")

messageOfTheSecond = {  # if you don't recognize this song, stop reading this and listen <https://open.spotify.com/track/7KXjTSCq5nL1LoYtL7XAwS?si=9f86d9e08cac4cd2>
        1: "Nobody Pray for Me, It Been That Day For Me, Yeah!",  # actually who are you? Why are you reading this?
        2: "I remember syrup sandwiches and crime allowances",  # how did you find this document?
        3: "Pull up to your block, and break it, now we playing Tetris",  # Are you male, female or NON-BINARY (or HEXADECIMAL?!)
        4: "AM to the PM, PM to the AM rock.",  # lol just kidding, had to mention that.
        5: "If I quit your BM, I still ride Mercedes.",
        6: "If I quit the Season, I still be the greatest",  # 5 & 6 are the best lines in the song
        7: "My Left Stroke Just Went Viral",
        8: "Right Stroke Put Lil' Baby In A Spiral",
        9: "Soprano C, We Like To Keep It On A High Note",
        10: "You Do Not Amaze Me, Ayy, Obama Just Paged Me, Ayy",
        11: "This, That, Grey Poupon, That Evian, That Ted Talk",
        12: "Watch My Soul Speak. You, Let The Meds Talk"
}


def main(messageOfTheSecond):
    key = 2
    while key == 2:
        randomNumGen = random.randint(1, len(messageOfTheSecond)) # RNG, unscripted order
        print(f"Message Of The Second: {messageOfTheSecond[randomNumGen]}")  # pulls from the Dictionary
        os.system("connector.py")
        key = int(input("Would You Like To Stop, Or Continue? (1/2)\n: "))
        if key == 1:
            quit()


check = os.path.exists('bills/')
if not check:
    print("Bills DIR not Found, Creating....")
    os.mkdir("bills/")  # Makes the DIR
    print('Success!\n')
    main(messageOfTheSecond)
else:
    print("Bills DIR Found..Proceeding...\n")
    main(messageOfTheSecond)
