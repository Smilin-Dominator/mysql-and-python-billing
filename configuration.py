import os

class vars:
    log_format = '%(asctime)s (%(filename)s): %(message)s'  # this basically says that the time and date come first, error next

class commands:

    def sql_tables(mycursor, mydb):
        print("[*] Creating Tables")
        print("[*] Creating 'paddigurlTest'")
        mycursor.execute("""
            CREATE TABLE paddigurlTest (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(256),
                price INT
            )
        """)
        print("[*] Creating 'paddigurlRemoved'")
        mycursor.execute("""
            CREATE TABLE paddigurlRemoved (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(256),
                price INT
            )
                    """)
        print("[*] Creating 'paddigurlHashes'")
        mycursor.execute("""
            CREATE TABLE paddigurlHashes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filepath TEXT,
                hash MEDIUMTEXT,
                filecontents LONGTEXT
            )
                    """)
        mydb.commit()
        print("[*] Success!")
        os.system('cls')