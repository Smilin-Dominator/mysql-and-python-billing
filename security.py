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

def check_password() -> tuple or bool:
    lines = open("log.txt", "r").read().splitlines()
    output = []
    for idx, line in enumerate(lines):
        if "Systemdump--Ignore-These" in line:
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


class integrityCheck(object):

    def __init__(self, check_log=None, hash_array=None, password_array=None, mycursor=None):
        self.check_the_pass = check_log
        self.scraped_content = hash_array
        self.password_array = password_array
        self.mycursor = mycursor

    def hash_check(self):
        self.mycursor.execute("SELECT filepath, hash FROM paddigurlHashes;")
        grape = self.mycursor.fetchall()
        out = []
        for filepath, hash in grape:
            out.append(HashFileRow(filepath=filepath, filehash=hash))
        return out

    def hash_write(self):
        warning("Hashes Have Been Tampered With, Restoring Previous Hashes...")
        logging.critical("Hashes Have Been Tampered With, Restoring Previous Hashes...")
        write_hash = FileOps()
        for _, data in enumerate(self.scraped_content):
            write_hash.__add__(data.filepath, data.filehash)
        write_hash.__write__()
        logging.info("Successfully Recovered The Hashes!")
        return "Successfully Recovered The Hashes!\n"


def init5_security(mycursor, conf: bool):

    checkPass = path.exists('./credentials/passwd.txt')
    checkHash = path.exists('./credentials/hashes.json')

    if not checkPass:
        critical = check_password()
        if not critical:
            warning("No Password Set.. Creating File..")
            pas_enter = input(prompt="Enter A Password", override="red", password=True)
            pas = open('./credentials/passwd.txt', 'w+')
            salt1 = ''.join(choices(ascii_letters + hexdigits, k=95))
            salt2 = ''.join(choices(digits + octdigits, k=95))
            pass_write = str(salt1 + pas_enter + salt2)
            hashpass = sha512(pass_write.encode()).hexdigest()
            signature = md5("McDonalds_Im_Loving_It".encode()).hexdigest()
            logging.info(f"Systemdump--Ignore--These\n{signature}\n{salt1}\n{salt2}\n{hashpass}")
            pas.write(f'{salt1},{salt2},{hashpass}')
            info("Success!", "green")
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
        scrape = integrityCheck(mycursor=mycursor).hash_check()
        if not scrape:
            info("No Attempt Of Espionage...", "green")
            info("Proceeding To Make File....", "bold green")
            write_hi = open('./credentials/hashes.json', 'w')
            write_hi.write('\n')
            write_hi.close()
        else:
            print(integrityCheck('none', scrape, 'none', mycursor).hash_write())

    if checkHash and conf:
        db_rows = integrityCheck(mycursor=mycursor).hash_check()
        try:
            hash_file_rows: list[dict] = loads(open('./credentials/hashes.json', 'r').read())
            for el in db_rows:
                for row in hash_file_rows:
                    if row["Filename"] == el.filepath:
                        if row["Hash"] == el.filehash:
                            break
                else:
                    info(integrityCheck(hash_array=db_rows, mycursor=mycursor).hash_write(), "green")
        except JSONDecodeError:
            info(integrityCheck(hash_array=db_rows, mycursor=mycursor).hash_write(), "green")
        except ValueError:
            info(integrityCheck(hash_array=db_rows, mycursor=mycursor).hash_write(), "green")


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