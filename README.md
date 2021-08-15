# MySQL and Python Billing 
[![Publish](https://github.com/Smilin-Dominator/mysql-and-python-billing/actions/workflows/release.yml/badge.svg)](https://github.com/Smilin-Dominator/mysql-and-python-billing/actions/workflows/release.yml)
[![Syntax Highlighting](https://github.com/Smilin-Dominator/mysql-and-python-billing/actions/workflows/main.yml/badge.svg)](https://github.com/Smilin-Dominator/mysql-and-python-billing/actions/workflows/main.yml)
# Logs

(22nd May)
><font size="6">I made this random program to test out if I could extract data from a MySQL Server
>And Add Them All And Get The Balance. And it succeeded! After 3 Days of trying I gave up on it
>But then randomly picked it up 3 weeks later, and fixed the bugs!</font><br>

(29th May)
><font size="6">Added a billing system. So now all progress is logged properly, and saved. Instead
>of specifying how many items there can be, you keep on adding items, and when you're done, hit enter in the ID input
>(without any text) and it'll process the data and create an invoice.</font>

(12th June)
><font size="6">Hello, my silent friend (get the reference?) its been a while. I added many new files, including a master-bill
> maker, an SQL Client and a File Integrity checker. Added new features like Password Recovery, automatic setup scripts
> deleting and updating capabilities and making sales reports. Today, I added a new feature I just learned, Classes. So to reduce
> the repetitive commands, which were copy+pasted everywhere, can now be in a centralized class! It reduces cluttering and makes editing
> the code easier!</font>

(7th July)
><font size="6">The credentials are now entered on your first setup, and stored in a file (Encrypted of Course)
> and each time you run Main.py its Decrypted, instead of making the rest of the files (connector, verify) also decrypt it 
> main.py sends the credentials as a CL Argument. And the RSA Key is now stored in the logs, so whenever its deleted
>  you can recover it. And I added different phases to main.py, Init0 which checks your log file, Init1 which looks for
>  your SQL Credentials, Init3 which checks for code updates and Init5 which checks the integrity of all the files in ./credentials</font>

(15th July)
><font size="6">The program can run two ways, either as a compiled .exe file, or from source. If its compiled, you don't need to install python or anything, just the file and README.md (For reference). If you're Git Cloning and running the .py files, then you have to install the requirements (main.py will do it for you) and all. So its all upto your preference.</font>

(18th July)
><font size="6">Successfully made GitHub actions compile two versions of the program (Linux and Windows), it now auto publishes them to a 
> release draft. GitHub Actions is very hard and lacks a lot of documentation, specially for Python. Also created a docker-compose.yml format
> in configuration.py so you get the option to create a docker container at startup.</font>

# How To Use It?
***DELETE THIS FILE WHEN YOU'VE READ IT, ANYONE OTHER UNTRUSTED PARTY WHO READS THIS IS A THREAT***
### Prerequisites
- Running From Source
    - <font size="6">Download [Python 3.9.4](https://www.python.org/downloads/release/python-394/) and install it.

    - Then you're good to go! Just go to the directory where you downloaded it (via Powershell) and type
    `python main.py`, it'll check for log.txt, if it's not present, it'll run
    the shell script related to your OS! **Do Not Delete Your log.txt, If you want you may clear it, but not delete it.**</font>
- Running The .exe
    - <font size="6">Download The Latest (main.zip) From The GitHub Page
        **(Optional: Read README.md, its the manual)**
    - Open Powershell and Type `./main.exe` And It Should Setup Everything</font>
- Notes Common To Both
    - If you have a MySQL Server instance, don't create a docker container, but if you don't install [docker-compose](https://docs.docker.com/compose/install/) and then run the program.

### Scenarios and Combatting Them
<font size="6">Here are some scenarios you are quite likely to encounter, even if you don't you'll know
how to deal with them.<br>
##### Problem 1
Customer walks in, with a large number of items that you can't sit and peacefully count
since there's 10 Customers waiting behind him.<br>*Earlier: You had to count the amount of items and input it, and then only enter the IDs*<br>
*Now: Its looped, until you hit 'enter' or type 'Kill', you can keep adding items*
##### Problem 2
Customer brings 10 Dolls, and decides to get another bunch instead of the type she just got.
<br>*Earlier: You had to restart it, losing all your progress*
<br>*Now: You can use the 'del' function, to delete the type you don't want, and add the new type*
##### Problem 3
Customer doesn't wanna spend **too much**, so each time you add something, they want to see
the bill.
<br>*Earlier: You'll mess up the whole operation by just viewing and not entering a cash given value.*
<br>*Now: type '--' to see the Invoice and the total, but not check out, if you want to checkout, press (enter)*
##### Problem 4
Customer brings a total of 7 dolls from 2 types (5 Dolls = A, 2 Dolls = B), he wants to transfer
remove two dolls from Doll A and get 1 more of Doll B.
<br>*Earlier: I actually didn't think of this back then, but most likely restart*
<br>*Now: Use the 'update' function. You can remove 2 from DollA and add 2 to Doll B*
##### Problem 5
You leave for a well deserved coffee break, totally unaware that some dude just deleted your passwd.txt file.
<br>*Earlier: He could immediately delete the password file, set the password to something else and do damage*
<br>*Now: The password's hash and it's salts are stored in the (log.txt) file, along with an MD5 hash, which proves that
my program did that. If the password file has a different value than the one stored in the (log.txt), it'll rebuild it
with the correct password.*
##### Problem 6
You give your computer to someone, they look at the bills and just alter the values.
<br>*Earlier: Well, you're screwed*
<br>*A Little Bit Later: You're still screwed, but unlike earlier, the file verification will tell you if a file is different. So no accidental
fraud. But if this is on my server, don't worry, I'll make a backup script!*
<br>*Now: along with the hashes, the file's content is also stored in the database (its official, im crazy), so if the verifier flags the file as
altered or deleted, it'll rebuild it.*
##### Problem 7
File verification is going perfectly fine! Until someone comes along and deletes the hash file and rehashes the files to his version.
<br>*Earlier: Well, you're screwed, and unaware that you're screwed*
<br>*Now: All the hashes are stored in a MariaDB database (paddigurlHashes), and if the file is missing, but the hashes
still exist, it'll rebuild the file. If the file's hashes are different, it'll also rebuild the file with the correct hashes.*
#### Conclusion
Hope these scenarios helped you! I'll add more along with the new features that I add!
<br>***Note: for a more detailed explanation of the functions, check the list below!***
</font>

# Function List (connector.py)
- ID Prompt (ID: )
    - When it prompts for the ID, you may enter the ID number, and proceed.
    - If you want to view the current total enter '--' instead of an ID when prompted.
    - Once you're certain that all the items are in order, press (enter) without any text, to proceed to the invoice
    - You may enter any of the following to get to the following (#Rhymes)
        - del
        - Kill
        - update
- View Display ([shows the bill])
    - To enter this screen, type '--' in the ID prompt
    - **If you only want to see the total, and not checkout yet, please use this instead of (enter)**
    - It'll show you all the items in the cart and the subtotal.
- Invoice Prompt (Cash Given: )
    - To enter this screen , press (enter) without any other input in the ID Prompt.
    - Enter the discount %, if there's no discount, enter 0 (Even if you don't it'll automatically assign 0)
    - After it returns the Total, enter the amount of cash given, if the balance is negative, it keeps asking you for the correct amount, until you give the correct amount.
    - Afterwards, it returns the balance, then goes back to main.py
       > Note, If you selected "Bank Transfer Mode" it'll ask you if they have transfered or not, instead of asking for amount payed and balance.
- Delete Prompt (The (Name) To Be Removed: )
    - To enter this screen, type 'del' in the ID prompt.
    - Enter the item name of what you wish to delete (The names will be displayed)
    - If successful, it'll say so. Or else, it'll loop until you provide the correct name.
- Kill Prompt (Enter Password: )
    - To enter this screen, type 'Kill' in the ID Prompt.
    - You will have to enter the password you set in (main.py). Once you set it, there is no way to reset or recover it. As it's stored
      as a hash in (passwd.txt), it has 2 salts, on either side of the text.
    - It covers the input, so it looks like you're not typing anything, but you are.  
    - If successful, it'll kill the process, make sure you delete the Bill manually, if you tried to checkout before doing the above.
- Update Prompt (What Would You Like To Update? (Name): )
    - To enter this screen, type 'update' in the ID Prompt.
    - You'll be prompted to enter the name of the Item, (all items are shown above the prompt)
    - Afterwards, it'll ask you to input the quantity you want to add / substract
    - You have to enter '+' for addition and '-' for substraction, leave a space and enter the amount you want to add.
        - **Note: The Space Is Very Important**
        - Examples:
            - To add 20:
                - `+ 20`
            - Not:
                - `+20`

# Function List (main.py)
- Random Line From HUMBLE:
    - Just as advertised, it just displays a random line from HUMBLE by Kendrick Lamar
- Enter Password:
    - If this is your first time setup, or if you deleted ./credentials/passwd.txt, this prompt will appear.
    - It covers the input, so it looks like you're not typing anything, but you are.
    - It'll then generate salts and hash it, and store it in (passwd.txt)
- The Main Prompt:
    - If you press 2, it'll loop back to (connector.py)
    - If you press 1, the program will stop and write all changes and the bills to the system.
    - If you press 3, it'll run  (master-bill.py) and get the total of all bills made today.
        - Don't worry about accidentally running it, it'll always rewrite the file, so run it as many
          times as you want.
        - It'll automatically generate a weekly sales report (./sales_reports/**) With The Grand Totals Of 7 Days.
          If there's < 7 Days after the initial, It'll have no issue, it'll mention them.
    - If you press 4, it'll take you to (sql-client.py) where you can view and alter entries.
    - If you press 5, it'll take you to (verify.py) where you can verify your bills.
    - If you press 6, it'll allow you to edit your config file.
    - If you selected 'Bank Transfer Mode' there'll be a number 7, which will allow you to track who sent transfers and didn't.
# Function List (sql-client.py)
- Master Password: 
    - Enter the master password you set in (main.py)
- Smilin_DB>
    - This is where you enter all the commands.
    - help
        - this will print a list of all the commands.
    - bye
        - adios (it'll quit and return to main.py)
    - show all
        - yeah there's a space in between.
        - this will print all the entries in the Table.
    - add
        - adds an item, prompts for Name and Price (ID asigned automatically)
    - remove
        - removes an item from the DB, there will be a gap. The previous item will be completely removed, and it will be
          added to another table called paddigurlRemoval, so the ID will always be there.
    - change
        - alters an item, prompts you for the ID, once you enter it, it'll display
          the current Name and Price.
        - You then get prompted for the new name and price.
    - add id
        - same as add, but you enter an ID
    - custom
      - You execute custom Queries here, it takes your raw input and executes it.

# Function List (verify.py)
- "Verify or Hash or Quit? (v/h/q): "
  - If you press 'v', it'll use its existing registry of Hashes and verify if the files hashes are the same
    - If they are it'll say '<file> Is The Same'
    - If they aren't it'll say '<file> Has Been Tampered'
  - If you press 'h', it'll hash all the new bills and store the hashes (skipping existing ones)

# Configuration Options (./credentials/options.txt)
- check_for_updates
  - Set `check_for_updates=True` if you want the program to check for updates, and auto-update, each time you run (main.py)
  - Set `check_for_updates=False` if you want the program to ignore the updates, so you can manually `git pull origin` whenever.
- check_file_integrity
    - Set `check_file_integrity=True` if you want the program to check if the password and hash file have been tampered with **while they're not deleted**.
    - Set `check_file_integrity=False` if you don't want the program to check if the password and hash files have been tampered with while they're not deleted.
    > Regardless Of What You Choose, If One Of The Two Aforementioned Files Are Absent, It'll Detect It And Recover.