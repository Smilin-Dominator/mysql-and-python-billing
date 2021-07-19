import os


class vars:

    log_format = '%(asctime)s (%(filename)s): %(message)s'  # this basically says that the time and date come first, error next

    def execheck():
        f = os.listdir()
        for i in range(len(f)):
            if f[i].endswith('.exe'):
                return True
        else:
            return False

    docker_compose = """
        # Use root/example as user/password credentials
        version: '3.1'

        services:

        db:
            image: mariadb
            restart: always
            environment:
                MARIADB_ROOT_PASSWORD: 123
                MARIADB_DATABASE: %s
                MARIADB_USER: %s
                MARIADB_PASSWORD: %s
            ports:
                - %d:%d
    """

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

class colours:

    Default      = "\033[39m"
    Black        = "\033[30m"
    Red          = "\033[31m"
    Green        = "\033[32m"
    Yellow       = "\033[33m"
    Blue         = "\033[34m"
    Magenta      = "\033[35m"
    Cyan         = "\033[36m"
    LightGray    = "\033[37m"
    DarkGray     = "\033[90m"
    LightRed     = "\033[91m"
    LightGreen   = "\033[92m"
    LightYellow  = "\033[93m"
    LightBlue    = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan    = "\033[96m"
    White        = "\033[97m"
    ENDC         = '\033[0m'

    BackgroundDefault      = "\033[49m"
    BackgroundBlack        = "\033[40m"
    BackgroundRed          = "\033[41m"
    BackgroundGreen        = "\033[42m"
    BackgroundYellow       = "\033[43m"
    BackgroundBlue         = "\033[44m"
    BackgroundMagenta      = "\033[45m"
    BackgroundCyan         = "\033[46m"
    BackgroundLightGray    = "\033[47m"
    BackgroundDarkGray     = "\033[100m"
    BackgroundLightRed     = "\033[101m"
    BackgroundLightGreen   = "\033[102m"
    BackgroundLightYellow  = "\033[103m"
    BackgroundLightBlue    = "\033[104m"
    BackgroundLightMagenta = "\033[105m"
    BackgroundLightCyan    = "\033[106m"
    BackgroundWhite        = "\033[107m"