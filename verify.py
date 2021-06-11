#!/usr/bin/env conda run -n mysql-and-python-billing python
import hashlib
import logging
import os

log_format = '%(asctime)s (%(filename)s): %(message)s'  # this basically says that the time and date come first, error next
logging.basicConfig(filename='log.txt', format=log_format, datefmt='[%Y-%m-%d] [%H:%M:%S]', level=logging.DEBUG)

print("Welcome To The Verifier!\n\n'Nobody Will Tamper With Your Data!' \n- People Before Their Data Got Tampered\n")
print("This Will Verify The Hashes Of Your Bills, Not The Master Bills And Sales Reports, as they're Dynamic")


def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'r') as red:
        while True:
            check = red.read(65536)
            if not check:
                break
            sha256.update(check.encode())
        return sha256.hexdigest()


# ---------Hash------------#
def hash():
    hashwrite = open('./hashes.txt', 'a')
    read_hash = open("hashes.txt", 'r')
    multiverse = os.listdir('bills')
    read_the_file = read_hash.read().splitlines()
    for dir in multiverse:
        bill_path = os.path.join('./bills', dir)
        ls_l = os.listdir(bill_path)
        for file in ls_l:
            the_new = os.path.join(bill_path, file)
            hash = hash_file(the_new)
            for data in read_the_file:
                if file.startswith('master_bill'):
                    print("Skipping Master Bill..")
                    break
                if hash in data:
                    print("Skipping Adding Existing Entry....")
                    break
            else:
                hashwrite.write(f"\n{the_new},{hash}")
                print(f"Hashed {file} .. {hash}")
                logging.info(f"Hashed {file} .. {hash}")

# -------Verify------------#
def verify():
    read_hash = open("hashes.txt", 'r')
    read = read_hash.read().splitlines()
    col = []
    for i in range(len(read)):
        zee = read[i].split(',')
        try:
            hashest = hash_file(zee[0])
            if str(hashest) == str(zee[1]):
                print(f"{zee[0]} Is The Same")
                logging.info(f"{zee[0]} Is The Same")
            else:
                print(f"{zee[0]} Has Been Tampered")
                logging.critical(f"{zee[0]} Has Been Tampered")
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
