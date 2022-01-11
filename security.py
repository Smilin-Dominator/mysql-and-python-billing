import logging
from hashlib import md5, sha512
from sys import exit
from os import path
from base64 import b64decode
from random import choices
from string import ascii_letters, hexdigits, octdigits, digits
from configuration import Variables, warning, info, input
from pydantic import BaseModel
from verify import FileOps

logging.basicConfig(filename='log.txt', format=Variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                    level=logging.DEBUG)


class HashFileRow(BaseModel):
    filepath: str
    hash: str


class integrityCheck(object):

    def __init__(self, check_log=None, hash_array=None, password_array=None, mycursor=None):
        self.check_the_pass = check_log
        self.scraped_content = hash_array
        self.password_array = password_array
        self.mycursor = mycursor

    def pass_check(self):
        read_the_pass = open(self.check_the_pass, 'r')
        crit = read_the_pass.read().splitlines()
        critical = []
        for i in range(len(crit)):
            try:
                if "Systemdump--Ignore--These" in crit[i]:
                    signature = crit[i + 1]
                    if signature == str(md5("McDonalds_Im_Loving_It".encode()).hexdigest()):
                        salt1 = crit[i + 2]
                        salt2 = crit[i + 3]
                        hashed_pw = crit[i + 4]
                        critical_ar = (salt1, salt2, hashed_pw)
                        critical.append(critical_ar)
                    else:
                        warning("Authenticity Not Recognized.. Reset log.txt and passwd.txt, Data Might've been "
                              "breached")
                        exit(66)
            except Exception as e:
                logging.warning(e)
        return critical

    def pass_write(self):
        warning("Password File Tampered, Restoring...")
        logging.critical("Password File Tampered, Restoring...")
        pas = open('./credentials/passwd.txt', 'w+')
        pas.write(f"{self.password_array[0][0]},{self.password_array[0][1]},{self.password_array[0][2]}")
        pas.flush()
        pas.close()
        logging.info("Successfully Recovered Password!")
        return "Successfully Recovered Password!"

    def hash_check(self):
        self.mycursor.execute("SELECT filepath, hash FROM paddigurlHashes;")
        grape = self.mycursor.fetchall()
        out = []
        for filepath, hash in grape:
            out.append(HashFileRow(filepath=filepath, hash=hash))
        return out

    def hash_write(self):
        warning("Hashes Have Been Tampered With, Restoring Previous Hashes...")
        logging.critical("Hashes Have Been Tampered With, Restoring Previous Hashes...")
        write_hash = FileOps()
        for _, data in enumerate(self.scraped_content):
            write_hash.__add__(data.filepath, data.hash)
        write_hash.__write__()
        logging.info("Successfully Recovered The Hashes!")
        return "Successfully Recovered The Hashes!\n"


def init5_security(mycursor, conf: bool):

    checkPass = path.exists('./credentials/passwd.txt')
    checkHash = path.exists('./credentials/hashes.json')

    if not checkPass:
        critical = integrityCheck(check_log='./log.txt', mycursor=mycursor).pass_check()
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
            info(integrityCheck(password_array=critical, mycursor=mycursor).pass_write(), "green")

    if checkPass and conf:
        critical = integrityCheck(check_log="./log.txt", mycursor=mycursor).pass_check()
        read_pass = open('./credentials/passwd.txt', 'r')
        read_pass_re = read_pass.read()
        read_pass_tup = tuple(read_pass_re.split(','))
        if read_pass_tup == (critical[0][0], critical[0][1], critical[0][2]):
            logging.info("[*] Password Check Successful.. Proceeding..")
        else:
            print(integrityCheck(password_array=critical, mycursor=mycursor).pass_write())

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
        scrape = integrityCheck(mycursor=mycursor).hash_check()
        scrape_file = open('./credentials/hashes.json', 'r')
        scrape2 = scrape_file.read().splitlines()
        hash_check_ar = []
        for i in range(len(scrape2)):
            if scrape2[i] == '':
                pass
            else:
                split = tuple(scrape2[i].split(','))
                hash_check_ar.append(split)
        if hash_check_ar == scrape:
            logging.info("[*] Hashes Match.. Proceeding...\n")
        else:
            info(integrityCheck(hash_array=scrape, mycursor=mycursor).hash_write(), "green")


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