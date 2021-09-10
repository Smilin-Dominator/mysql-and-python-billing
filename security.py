import logging
import hashlib
import sys
import os
import getpass
import random
import string
from configuration import variables

logging.basicConfig(filename='log.txt', format=variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                    level=logging.DEBUG)


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
                    if signature == str(hashlib.md5("McDonalds_Im_Loving_It".encode()).hexdigest()):
                        salt1 = crit[i + 2]
                        salt2 = crit[i + 3]
                        hashed_pw = crit[i + 4]
                        critical_ar = (salt1, salt2, hashed_pw)
                        critical.append(critical_ar)
                    else:
                        print("[*] Authenticity Not Recognized.. Reset log.txt and passwd.txt, Data Might've been "
                              "breached")
                        sys.exit(66)
            except Exception as e:
                logging.warning(e)
        return critical

    def pass_write(self):
        print("[*] Password File Tampered, Restoring...")
        logging.critical("Password File Tampered, Restoring...")
        pas = open('./credentials/passwd.txt', 'w+')
        pas.write(f"{self.password_array[0][0]},{self.password_array[0][1]},{self.password_array[0][2]}")
        pas.flush()
        pas.close()
        logging.info("Successfully Recovered Password!")
        return "[*] Successfully Recovered Password!"

    def hash_check(self):
        self.mycursor.execute("SELECT filepath, hash FROM paddigurlHashes;")
        grape = self.mycursor.fetchall()
        return grape

    def hash_write(self):
        print("[*] Hashes Have Been Tampered With, Restoring Previous Hashes...")
        logging.critical("Hashes Have Been Tampered With, Restoring Previous Hashes...")
        write_hash = open("./credentials/hashes.txt", 'w')
        for i in range(len(self.scraped_content)):
            write_hash.write(f"\n{self.scraped_content[i][0]},{self.scraped_content[i][1]}")
        write_hash.flush()
        write_hash.close()
        logging.info("Successfully Recovered The Hashes!")
        return "[*] Successfully Recovered The Hashes!\n"


def init5_security(mycursor, conf: bool):

    checkPass = os.path.exists('./credentials/passwd.txt')
    checkHash = os.path.exists('./credentials/hashes.txt')

    if not checkPass:
        critical = integrityCheck(check_log='./log.txt', mycursor=mycursor).pass_check()
        if not critical:
            print("[*] No Password Set.. Creating File..")
            pas_enter = getpass.getpass("[*] Enter Password: ")
            pas = open('./credentials/passwd.txt', 'w+')
            salt1 = ''.join(random.choices(string.ascii_letters + string.hexdigits, k=95))
            salt2 = ''.join(random.choices(string.digits + string.octdigits, k=95))
            pass_write = str(salt1 + pas_enter + salt2)
            hashpass = hashlib.sha512(pass_write.encode()).hexdigest()
            signature = hashlib.md5("McDonalds_Im_Loving_It".encode()).hexdigest()
            logging.info(f"Systemdump--Ignore--These\n{signature}\n{salt1}\n{salt2}\n{hashpass}")
            pas.write(f'{salt1},{salt2},{hashpass}')
            print("[*] Success!")
        else:
            print(integrityCheck(password_array=critical, mycursor=mycursor).pass_write())

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
        print("[*] No Hash File Found...")
        scrape = integrityCheck(mycursor=mycursor).hash_check()
        if not scrape:
            print("[*] No Attempt Of Espionage...")
            print("[*] Proceeding To Make File....")
            write_hi = open('./credentials/hashes.txt', 'w')
            write_hi.write('\n')
            write_hi.close()
        else:
            print(integrityCheck('none', scrape, 'none', mycursor).hash_write())

    if checkHash and conf:
        scrape = integrityCheck(mycursor=mycursor).hash_check()
        scrape_file = open('./credentials/hashes.txt', 'r')
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
            print(integrityCheck(hash_array=scrape, mycursor=mycursor).hash_write())
