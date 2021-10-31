import hashlib
import logging
import os
from configuration import variables, input, info, error, print

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

def make_hash(mydb, mycursor):
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
                    info("Skipping Master Bill..")
                    break
                if filehash in data:
                    info("Skipping Adding Existing Entry....")
                    break
            else:
                hashwrite.write(f"\n{the_new},{filehash}")
                query = "INSERT INTO paddigurlHashes(`filepath`, `hash`, `filecontents`) VALUES(%s, %s, %s)"
                values = (the_new, filehash, open(the_new, 'r').read())
                mycursor.execute(query, values)
                info(f"Hashed {file} .. {filehash}", override="cyan")
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
                    info(f"File {zee[0]} Is Safe", "green")
                    logging.info(f"{zee[0]} Is Safe")
                else:
                    error(f"File {zee[0]} Has Been Tampered")
                    logging.critical(f"File {zee[0]} Has Been Tampered")
                    info(f"Recovering Data...")
                    mycursor.execute(f"SELECT filecontents FROM paddigurlHashes WHERE `hash` = '{str(zee[1])}';")
                    attempted_recovery = mycursor.fetchall()
                    recovered = ''.join(attempted_recovery[0])
                    recover_write = open(zee[0], 'w')
                    recover_write.write(recovered)
                    recover_write.flush()
                    recover_write.close()
                    logging.info("Successful Recovery...")
                    info(f"Success...", "green")
            else:
                error(f"File {zee[0]} Has Been Deleted....", override="red")
                dir_check = zee[0].split("[BILL]")
                if not os.path.exists(dir_check[0]):
                    error(f"Entire Directory Deleted... Restoring..")
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
