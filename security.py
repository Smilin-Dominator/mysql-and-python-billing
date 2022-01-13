"""
MySQL And Python Billing
Copyright (C) 2021 Devisha Padmaperuma

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
from hashlib import md5, sha512
from sys import exit
from os import path
from base64 import b64decode
from random import choices
from string import ascii_letters, hexdigits, octdigits, digits
from configuration import Variables, warning, info, input, error
from verify import FileOps
from formats import HashFileRow
from json import loads, JSONDecodeError

logging.basicConfig(filename='log.txt', format=Variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                    level=logging.DEBUG)


# --------- Integrity Check Functions -------------- #

def create_new_passsword() -> None:
    pas_enter = input(prompt="Enter A Password", override="red", password=True)
    pas = open('./credentials/passwd.txt', 'w+')
    salt1 = ''.join(choices(ascii_letters + hexdigits, k=95))
    salt2 = ''.join(choices(digits + octdigits, k=95))
    pass_write = str(salt1 + pas_enter + salt2)
    hashpass = sha512(pass_write.encode()).hexdigest()
    signature = md5("McDonalds_Im_Loving_It".encode()).hexdigest()
    enc = "\n".join([signature, salt1, salt2, hashpass])
    logging.info(f"Systemdump--Ignore--These\n{enc}")
    pas.write(','.join([salt1, salt2, hashpass]))
    info("Success!", "green")


def check_password() -> tuple or bool:
    lines = open("log.txt", "r").read().splitlines()
    output = []
    for idx, line in enumerate(lines):
        if "Systemdump--Ignore--These" in line:
            signature = lines[idx + 1]
            if signature == "d4ef6be5817ba1e665dacb292acb365c": # MD5 Hash of 'McDonalds_Im_Loving_It'
                salt1 = lines[idx + 2]
                salt2 = lines[idx + 3]
                pw = lines[idx + 4]
                return salt1, salt2, pw
            else:
                error("Authenticity Is Questionable, Exiting")
                exit(66)
    else:
        return False


def recover_password(recovered: tuple[str, str, str]):
    warning("Password File has been Tampered With! Restoring...")
    with open("./credentials/passwd.txt", "w") as fil:
        fil.write(','.join(recovered))
        fil.flush()
        fil.close()
    info("Successfully Recovered Password!", "green")


def get_hashes(cursor) -> list[HashFileRow]:
    cursor.execute("SELECT filepath, hash FROM paddigurlHashes;")
    results = cursor.fetchall()
    output = []
    for filepath, hash in results:
        output.append(HashFileRow(filepath=filepath, filehash=hash))
    return output


def write_hashes(files: list[HashFileRow]):
    warning("The Hashes Have Been Tampered With! Restoring the previous hashes...")
    writer = FileOps()
    for file in files:
        writer.__add__(file.filepath, file.filehash)
    writer.__write__()
    info("Successfully Recovered The Hashes!")


# --------- Main Function ---------------------- #

def init5_security(mycursor, conf: bool):

    checkPass = path.exists('./credentials/passwd.txt')
    checkHash = path.exists('./credentials/hashes.json')

    if not checkPass:
        critical = check_password()
        if not critical:
            warning("No Password Set.. Creating File..")
            create_new_passsword()
        else:
            recover_password(critical)

    if checkPass and conf:
        critical = check_password()
        read_pass = open('./credentials/passwd.txt', 'r')
        read_pass_re = read_pass.read()
        read_pass_tup = tuple(read_pass_re.split(','))
        if read_pass_tup == (critical[0], critical[1], critical[2]):
            logging.info("[*] Password Check Successful.. Proceeding..")
        else:
            recover_password(critical)

    if not checkHash:
        warning("No Hash File Found...")
        scrape = get_hashes(mycursor)
        if not scrape:
            info("No Attempt Of Espionage...", "green")
            info("Proceeding To Make File....", "bold green")
            write_hi = open('./credentials/hashes.json', 'w')
            write_hi.write('\n')
            write_hi.close()
        else:
            write_hashes(scrape)

    if checkHash and conf:
        db_rows = get_hashes(mycursor)
        try:
            hash_file_rows: list[dict] = loads(open('./credentials/hashes.json', 'r').read())
            for el in db_rows:
                for row in hash_file_rows:
                    if row["Filename"] == el.filepath:
                        if row["Hash"] == el.filehash:
                            break
                else:
                    write_hashes(db_rows)
        except JSONDecodeError:
            write_hashes(db_rows)
        except ValueError:
            write_hashes(db_rows)


def key_security():
    with open('log.txt', 'r') as truth:
        a = truth.read().splitlines()
        for line in a:
            if 'Binary_Data' in line:
                info("Found Existing Public Key..")
                info("Recovering..")
                b = line.split('Binary_Data:')
                pubkey = open('./credentials/public.pem', 'w+')
                out = ''.join(b[1]).replace("b'", "").replace("'", "")
                dec = b64decode(out).decode()
                pubkey.write(dec)
                info("Successfully Recovered Public Key!", "green")
                pubkey.close()
            elif "Binary-Data" in line:
                info("Found Existing Private Key..")
                info("Recovering...")
                b = line.split('Binary-Data:')
                privkey = open('./credentials/private.pem', 'w+')
                out = ''.join(b[1]).replace("b'", "").replace("'", "")
                dec = b64decode(out).decode()
                privkey.write(dec)
                info("Successfully Recovered Private Key!", "green")
                privkey.close()
        else:
            info("No Attempt Of Fraud, Continuing..")