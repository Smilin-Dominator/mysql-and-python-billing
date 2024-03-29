"""
MySQL And Python Billing
Copyright (C) 2021 Devisha Padmaperuma

MySQL And Python Billing is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MySQL And Python Billing is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with MySQL And Python Billing.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
from hashlib import sha256
from os import path, listdir, mkdir
from configuration import Variables, input, info, error, print
from json import loads, dumps, JSONDecodeError
from formats import HashFileRow

logging.basicConfig(filename='log.txt', format=Variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                    level=logging.DEBUG)


def hash_file(filepath: str):
    sha = sha256()
    if path.exists(filepath):
        with open(filepath, 'r') as red:
            while True:
                check = red.read(65536)
                if not check:
                    break
                sha.update(check.encode())
            return sha.hexdigest()
    else:
        return False


# ---------Hash------------#

class FileOps:

    def __init__(self):
        try:
            self.file = open("credentials/hashes.json", "r+")
            self.json = loads(self.file.read())
        except FileNotFoundError:
            self.file = open("credentials/hashes.json", "w+")
            self.json = []
        except JSONDecodeError:
            self.file = open("credentials/hashes.json", "w+")
            self.json = []

    def __add__(self, filename: str, filehash: str) -> None:
        self.json.append(
            {
                "Filename": filename,
                "Hash": filehash
            }
        )

    def __update__(self):
        self.json = loads(self.file.read())

    def __get__(self) -> list:
        return self.json

    def __write__(self) -> None:
        self.file = open("credentials/hashes.json", "w+")
        self.file.write(dumps(self.json, indent=4))
        self.file.flush()
        self.file.close()

    def __del__(self):
        logging.info(f"Destroying Class {self.__class__}")


def make_hash(mydb, mycursor):
    hashfile = FileOps()
    multiverse = listdir('bills')
    for directory in multiverse:
        bill_path = path.join('./bills/', directory)
        ls_l = listdir(bill_path)
        for file in ls_l:
            the_new = path.join(bill_path + '/' + file)
            filehash = hash_file(the_new)
            if the_new.endswith('master_bill.txt'):
                info("Skipping Master Bill..")
                continue
            else:
                for f in hashfile.__get__():
                    fil = HashFileRow(filepath=f["Filename"], filehash=f["Hash"])
                    if filehash == fil.filehash:
                        info("Skipping Adding Existing Entry....")
                        break
                else:
                    hashfile.__add__(the_new, filehash)
                    query = "INSERT INTO paddigurlHashes(`filepath`, `hash`, `filecontents`) VALUES(%s, %s, %s)"
                    values = (the_new, filehash, open(the_new, 'r').read())
                    mycursor.execute(query, values)
                    info(f"Hashed {the_new} .. {filehash}", override="cyan")
                    logging.info(f"Hashed .. {the_new} .. {filehash}")
        mydb.commit()
    hashfile.__write__()


# -------Verify------------#
def recover(mycursor, file: HashFileRow):
    mycursor.execute(f"SELECT filecontents FROM paddigurlHashes WHERE `hash` = '{file.filehash}';")
    attempted_recovery = mycursor.fetchall()
    recovered = ''.join(attempted_recovery[0])
    recover_write = open(file.filepath, 'w')
    recover_write.write(recovered)
    recover_write.flush()
    recover_write.close()
    logging.info("Successful Recovery...")


def verify(mycursor):
    hashfile = FileOps()
    for file in hashfile.__get__():
        fil = HashFileRow(filepath=file["Filename"], filehash=file["Hash"])
        try:
            hashest = hash_file(fil.filepath)
            if hashest:
                if str(hashest) == fil.filehash:
                    info(f"File {fil.filepath} Is Safe", "green")
                    logging.info(f"{fil.filepath} Is Safe")
                else:
                    error(f"File {fil.filepath} Has Been Tampered")
                    logging.critical(f"File {fil.filepath} Has Been Tampered")
                    info(f"Recovering Data...")
                    recover(mycursor, fil)
                    info(f"Success...", "green")
            else:
                error(f"File {fil.filepath} Has Been Deleted....", override="red")
                dir_check = fil.filepath.split("[BILL]")
                if not path.exists(dir_check[0]):
                    error(f"Entire Directory Deleted... Restoring..")
                    mkdir(dir_check[0])
                logging.critical(f"File {fil.filepath} Has Been Deleted")
                recover(mycursor, fil)
                info(
                        f"[white on black][*] Attempting Recovery....\n[/white on black]"
                        f"[green][*] Success...[/green]"
                    )
        except Exception as e:
            logging.error(e)


def main(mydb, mycursor):
    print("[green on white]Welcome To The Verifier![/green on white]\n\n[red]'Nobody Will Tamper With Your Data!'[/red]"
          "[orange_red1]\n- People Before Their Data Got Tampered[/orange_red1]\n")
    print("[honeydew2]This Will Verify The Hashes Of Your Bills, Not The Master Bills And Sales Reports"
          ", as they're Dynamic[/honeydew2]")
    key = input("[dark_sea_green1]Verify or Hash or Quit? (v/h/q): [/dark_sea_green1]")
    if key == 'v':
        verify(mycursor)
        input("(enter to continue...)")
    elif key == 'h':
        make_hash(mydb, mycursor)
        input("(enter to continue...)")
