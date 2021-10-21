import subprocess
import time
import os
import base64
from configuration import commands, variables

console = commands.console
print = commands.print
com = commands()


def main():
    print("[bold green]Welcome to my Program! Setting Up Config File")
    commands().write_conifguration_file()
    with console.status("[bold green]Initializing..") as _:
        _ if subprocess.run("pip3 install -r requirements.txt", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True).returncode == 0 else com.error(msg="While Installing Pip Packages")
        console.log("Environment Setup Complete")
        time.sleep(3)
        subprocess.call("touch log.txt", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        console.log("Created Log.txt")
        time.sleep(3)
        console.log("All Tasks Successful!")


def sql(logging, rsa):
    check_for_file = os.path.exists('./credentials/mysql.txt')
    if not check_for_file:
        print("[*] No MySQL Configuration File Detected, Enter The Details Below.")
        create_container = input("[*] Would You Like To Create A Docker Container? (y/n): ")
        if create_container == 'y':
            print("[*] Creating Docker Image..")
            try:
                user = input("Username: ")
                password = input("Password: ")
                db = 'paddigurl'
                port = 3306
                host = '127.0.0.1'
                with open("docker-compose.yml", 'w') as docker:
                    port = int(port)
                    dc = variables.docker_compose % (user, password)
                    docker.write(dc)
                    docker.close()
                subprocess.run("docker-compose up -d", shell=True)
                time.sleep(10)
            except subprocess.SubprocessError:
                print("[*] An Error Occured, Is docker-compose Installed?")
        else:
            host = input("Host: ")
            port = input("Port (default = 3306): ")
            user = input("Username: ")
            password = input("Password: ")
            db = input("Database: ")
        print("[*] Generating Keys....")
        pubKey, privKey = rsa.newkeys(1096)
        print("[*] Writing Public Key..")
        with open('./credentials/public.pem', 'w') as pop:
            pubStr = pubKey.save_pkcs1()
            pop.write(pubStr.decode('utf-8'))
            encoded = base64.b64encode(pubStr)
            logging.info(f"Binary_Data:{encoded}")
            pop.close()
        print("[*] Writing Private Key..")
        with open('./credentials/private.pem', 'w') as pop:
            privStr = privKey.save_pkcs1()
            pop.write(privStr.decode('utf-8'))
            encoded = base64.b64encode(privStr)
            logging.info(f"Binary-Data:{encoded}")
            pop.close()
        logging.info("Wrote RSA Keys")
        print("[*] Success.. Final Touches...")
        st = f"{host},{user},{port},{password},{db}".encode()
        with open('./credentials/mysql.txt', 'wb+') as mcdonalds:
            var = rsa.encrypt(st, pubKey)
            mcdonalds.write(var)
        print("[*] Successfully Wrote The Changes To The File..")
        if create_container == 'n':
            conf = input("[*] Create Tables? (y/n): ")
        else:
            conf = 'y'
        return [host, user, port, password, db, conf]
    else:
        with open("./credentials/mysql.txt", 'rb') as fillet:
            privKey = rsa.PrivateKey.load_pkcs1(open("./credentials/private.pem", 'rb').read())
            a = fillet.read()
            b = rsa.decrypt(a, privKey).decode('utf-8')
            return b.split(',')
