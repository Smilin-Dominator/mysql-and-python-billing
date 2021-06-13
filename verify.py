#!/usr/bin/env conda run -n mysql-and-python-billing python
import hashlib
import logging
import os
import mysql.connector

log_format = '%(asctime)s (%(filename)s): %(message)s'  # this basically says that the time and date come first, error next
logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

print("Welcome To The Verifier!\n\n'Nobody Will Tamper With Your Data!' \n- People Before Their Data Got Tampered\n")
print("This Will Verify The Hashes Of Your Bills, Not The Master Bills And Sales Reports, as they're Dynamic")

mydb = mysql.connector.connect(
    auth_plugin='mysql_native_password',
    host="178.79.168.171",
    user="smilin_dominator",
    password="Barney2356",
    database='miscellaneous'
)
mycursor = mydb.cursor()

def hash_file(filepath):
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
def hash():
    hashwrite = open('./hashes.txt', 'a')
    read_hash = open("hashes.txt", 'r')
    multiverse = os.listdir('bills')
    read_the_file = read_hash.read().splitlines()
    for dir in multiverse:
        bill_path = os.path.join('./bills/', dir)
        ls_l = os.listdir(bill_path)
        for file in ls_l:
            the_new = os.path.join(bill_path + '/' + file)
            hash = hash_file(the_new)
            for data in read_the_file:
                if the_new.endswith('master_bill.txt'):
                    print("Skipping Master Bill..")
                    break
                if hash in data:
                    print("Skipping Adding Existing Entry....")
                    break
            else:
                hashwrite.write(f"\n{the_new},{hash}")
                mycursor.execute(f"INSERT INTO paddigurlHashes(filepath, hash, filecontents) VALUES('{the_new}', '{hash}', '{open(the_new, 'r').read()}')")
                print(f"Hashed {file} .. {hash}")
                logging.info(f"Hashed .. {file} .. {hash}")
        mydb.commit()

# -------Verify------------#
def verify():
    read_hash = open("hashes.txt", 'r')
    read = read_hash.read().splitlines()
    read.remove('')
    col = []
    for i in range(len(read)):
        zee = read[i].split(',')
        try:
            hashest = hash_file(zee[0])
            if hashest:
                if str(hashest) == str(zee[1]):
                    print(f"{zee[0]} Is The Same")
                    logging.info(f"{zee[0]} Is The Same")
                else:
                    print(f"{zee[0]} Has Been Tampered")
                    logging.critical(f"{zee[0]} Has Been Tampered")
                    print("\t\tRecovering Data...")
                    mycursor.execute(f"SELECT filecontents FROM paddigurlHashes WHERE `hash` = '{str(zee[1])}';")
                    attempted_recovery = mycursor.fetchall()
                    recovered = ''.join(attempted_recovery[0])
                    recover_write = open(zee[0], 'w')
                    recover_write.write(recovered)
                    recover_write.flush()
                    recover_write.close()
                    print("\t\tSuccess...")
            else:
                print(f"\t\tFile {zee[0]} Has Been Deleted....")
                mycursor.execute(f"SELECT filecontents FROM paddigurlHashes WHERE `hash` = '{str(zee[1])}';")
                attempted_recovery = mycursor.fetchall()
                recovered = ''.join(attempted_recovery[0])
                recover_write = open(zee[0], 'w')
                recover_write.write(recovered)
                recover_write.flush()
                recover_write.close()
                print("\t\tAttempting Recovery....\n\t\tSuccess...")
        except Exception as e:
            logging.error(e)

def main():
    key = input("Verify or Hash or Quit? (v/h/q): ")
    if key == 'v':
        verify()
    elif key == 'h':
        hash()
    elif key == 'q':
        quit()

main()
