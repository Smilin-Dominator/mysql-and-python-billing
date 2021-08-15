import logging
import hashlib
import sys
from configuration import variables

logging.basicConfig(filename='log.txt', format=variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                    level=logging.DEBUG)


class integrityCheck(object):

    def __init__(self, check_log, hash_array, password_array, mycursor):
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
