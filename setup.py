from subprocess import run, DEVNULL, SubprocessError
from time import sleep
from os import path
from base64 import b64encode
from security import create_new_passsword
from configuration import Variables, console, print, input, warning, error, write_conifguration_file


def main():
    print("[bold green]Welcome to 'mysql_and_python_billing'; Written In Python by the One and Only Devisha "
          "Padmaperuma![/bold green]")
    print("\nSetting Up The Configuration File", override="tan")
    write_conifguration_file()
    print("\nCreating The New Password", override="tan")
    create_new_passsword()
    with console.status("[bold green]Initializing..", spinner='dots12') as _:
        console.log("Created Log.txt")
        sleep(1)
        console.log("Created New Password")
        sleep(1)
        console.log("All Tasks Successful!")


def sql(logging, rsa):
    check_for_file = path.exists('./credentials/mysql.txt')
    if not check_for_file:
        warning("No MySQL Configuration File Detected, Enter The Details Below.", "bold yellow")
        create_container = input("Would you like to create a docker container? (y/n)", "italic green")
        if create_container == 'y':
            console.log("Creating Docker Image..")
            try:
                user = input("Username", "bold red")
                password = input("Password", "bold red", password=True)
                db = 'paddigurl'
                port = 3306
                host = '127.0.0.1'
                with open("docker-compose.yml", 'w') as docker:
                    port = int(port)
                    dc = Variables.docker_compose % (user, password)
                    docker.write(dc)
                    docker.close()
                run("docker-compose up -d", shell=True)
                sleep(10)
            except SubprocessError:
                error("An Error Occured (Is Docker-Compose Installed?)")
        else:
            host = input("Host", "bold red")
            port = input(prompt="Port", override="bold red", default="3306")
            user = input("Username", "bold red")
            password = input("Password", "bold red", password=True)
            db = input("Database", "bold red")
        with console.status("[bold green]Registering Credentials..", spinner='dots11') as _:
            if (not path.exists("./credentials/public.pem")) and (not path.exists("./credentials/private.pem")):
                pubKey, privKey = rsa.newkeys(1096)
                sleep(2)
                console.log("Generated Keys....")
                with open('./credentials/public.pem', 'w') as pop:
                    pubStr = pubKey.save_pkcs1()
                    pop.write(pubStr.decode('utf-8'))
                    encoded = b64encode(pubStr)
                    logging.info(f"Binary_Data:{encoded}")
                    pop.close()
                sleep(2)
                console.log("Wrote Public Key..")
                with open('./credentials/private.pem', 'w') as pop:
                    privStr = privKey.save_pkcs1()
                    pop.write(privStr.decode('utf-8'))
                    encoded = b64encode(privStr)
                    logging.info(f"Binary-Data:{encoded}")
                    pop.close()
                sleep(2)
                console.log("Wrote Private Key..")
                logging.info("Wrote RSA Keys")
            else:
                pubKey = rsa.PublicKey.load_pkcs1(open("./credentials/public.pem", 'rb').read())
                console.log("Not Generating Keys As They Already Exist!")
            st = f"{host},{user},{port},{password},{db}".encode()
            with open('./credentials/mysql.txt', 'wb+') as mcdonalds:
                var = rsa.encrypt(st, pubKey)
                mcdonalds.write(var)
            sleep(1)
            console.log("Successfully Encrypted Credentials")
        if create_container == 'n':
            conf = input("Create Tables? (y/n)", "blue")
        else:
            conf = 'y'
        return [host, user, port, password, db, conf]
    else:
        with open("./credentials/mysql.txt", 'rb') as fillet:
            privKey = rsa.PrivateKey.load_pkcs1(open("./credentials/private.pem", 'rb').read())
            a = fillet.read()
            b = rsa.decrypt(a, privKey).decode('utf-8')
            return b.split(',')
