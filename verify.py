import hashlib
import logging
import os
from configuration import variables, colours

logging.basicConfig(filename='log.txt', format=variables.log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]',
                    level=logging.DEBUG)


def hash_file(filepath: str):
    sha256 = hashlib.sha256()
    if os.path.exists(filepath):
        with open(filepath, 'r') as red:
            while True:
                check = red.read(65536)
                if not check:
                    break
                sha256.update(check.encode())
            return sha256.hexdigest()
    else:
        return False


# ---------Hash------------#

def hash(mydb, mycursor):
    hashwrite = open('./credentials/hashes.txt', 'a')
    read_hash = open("./credentials/hashes.txt", 'r')
    multiverse = os.listdir('bills')
    read_the_file = read_hash.read().splitlines()
    for directory in multiverse:
        bill_path = os.path.join('./bills/', directory)
        ls_l = os.listdir(bill_path)
        for file in ls_l:
            the_new = os.path.join(bill_path + '/' + file)
            filehash = hash_file(the_new)
            for data in read_the_file:
                if the_new.endswith('master_bill.txt'):
                    print(f"{colours.Blue}[*] Skipping Master Bill..{colours.ENDC}")
                    break
                if filehash in data:
                    print(f"{colours.LightCyan}[*] Skipping Adding Existing Entry....{colours.ENDC}")
                    break
            else:
                hashwrite.write(f"\n{the_new},{filehash}")
                mycursor.execute(
                    f"INSERT INTO paddigurlHashes(filepath, hash, filecontents) VALUES('{the_new}', '{filehash}', '{open(the_new, 'r').read()}')")
                print(f"{colours.Blue}[*] Hashed {file} .. {filehash}{colours.ENDC}")
                logging.info(f"Hashed .. {file} .. {filehash}")
        mydb.commit()


# -------Verify------------#
def verify(mycursor):
    read_hash = open("./credentials/hashes.txt", 'r')
    read = read_hash.read().splitlines()
    read.remove('')
    for i in range(len(read)):
        zee = read[i].split(',')
        try:
            hashest = hash_file(zee[0])
            if hashest:
                if str(hashest) == str(zee[1]):
                    print(f"{colours.Green}[*] File {zee[0]} Is Safe{colours.ENDC}")
                    logging.info(f"{zee[0]} Is Safe")
                else:
                    print(f"{colours.BackgroundRed}[*] File {zee[0]} Has Been Tampered{colours.ENDC}")
                    logging.critical(f"File {zee[0]} Has Been Tampered")
                    print(f"{colours.LightBlue}[*] Recovering Data...{colours.ENDC}")
                    mycursor.execute(f"SELECT filecontents FROM paddigurlHashes WHERE `hash` = '{str(zee[1])}';")
                    attempted_recovery = mycursor.fetchall()
                    recovered = ''.join(attempted_recovery[0])
                    recover_write = open(zee[0], 'w')
                    recover_write.write(recovered)
                    recover_write.flush()
                    recover_write.close()
                    logging.info("Successful Recovery...")
                    print(f"{colours.Green}[*] Success...{colours.ENDC}")
            else:
                print(f"{colours.Red}[*] File {zee[0]} Has Been Deleted....{colours.ENDC}")
                dir_check = zee[0].split("[BILL]")
                if not os.path.exists(dir_check[0]):
                    print(f"{colours.BackgroundRed}[*] Entire Directory Deleted... Restoring{colours.ENDC}")
                    os.mkdir(dir_check[0])
                logging.critical(f"File {zee[0]} Has Been Deleted")
                mycursor.execute(f"SELECT filecontents FROM paddigurlHashes WHERE `hash` = '{str(zee[1])}';")
                attempted_recovery = mycursor.fetchall()
                recovered = ''.join(attempted_recovery[0])
                recover_write = open(zee[0], 'w')
                recover_write.write(recovered)
                recover_write.flush()
                recover_write.close()
                logging.info("Successful Recovery...")
                print(
                    f"{colours.DarkGray}[*] Attempting Recovery....{colours.ENDC}\n{colours.Green}"
                    f"[*] Success...{colours.ENDC}"
                )
        except Exception as e:
            logging.error(e)


def main(mydb, mycursor):
    print("Welcome To The Verifier!\n\n'Nobody Will Tamper With Your Data!' \n- People Before Their Data Got Tampered\n")
    print("This Will Verify The Hashes Of Your Bills, Not The Master Bills And Sales Reports, as they're Dynamic")
    key = input("Verify or Hash or Quit? (v/h/q): ")
    if key == 'v':
        verify(mycursor)
        input("(enter to continue...)")
    elif key == 'h':
        hash(mydb, mycursor)
        input("(enter to continue...)")
