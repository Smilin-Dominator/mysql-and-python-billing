# MySQL and Python Billing Logs

(22nd May)
><font size="6">I made this random program to test out if I could extract data from a MySQL Server
>And Add Them All And Get The Balance. And it succeeded! After 3 Days of trying I gave up on it
>But then randomly picked it up 3 weeks later, and fixed the bugs!</font><br>

(29th May)
><font size="6">Added a billing system. So now all progress is logged properly, and saved. Instead
>of specifying how many items there can be, you keep on adding items, and when you're done, hit enter in the ID input
>(without any text) and it'll process the data and create an invoice.</font>
# How To Use It?

<font size="6">Replace the SQL Credentials and Query to your own. If you want to, tweak any setting, just make sure
you know what you're doing, or else, you'll be doomed!<br>
Be sure to read the guide below before using the program!</font>

### Detailed Guide
<font size="6">Run main.py in a directory where you have full permissions. It should automatically make a 
DIR called 'bills', remember all the soft copies of the bills will be written over there
. Then enter the IDs, once your done, hit enter when it prompts for the ID again.<br>
Beware when entering the discount percentage, if you enter anything other than an integer > 0, it'll default to 0.In case you accidentally put the wrong amount (for the Cash Recieved), the computer calculates the balance before writing it,
so if it detects that its < 0, it'll loop (without writing the output) until the balance gets an answer >= 0, and only then, will
it write the amount of cash recieved and the balance.<br>
Also, if you want to view the output without checking out, type '--' into the ID prompt. <br>**Why Did I Add This?** If you press (enter), it creates a bill file,
so if you check about 1 minute afterwards, it creates a new file, as the name contains the Hour and Minute!<br>
In case you add the same item more than 1x, the Program will detect it, take the previous entry, add to it and reappend it.</font>

### Function List
- ID Prompt (ID: )
    - When it prompts for the ID, you may enter the ID number, and proceed.
    - If you want to view the current total enter '--' instead of an ID when prompted.
    - Once you're certain that all the items are in order, press (enter) without any text, to proceed to the invoice
    - You may enter any of the following to get to the following (#Rhymes)
        - del
        - Kill
- View Display ([shows the bill])
    - To enter this screen, type '--' in the ID prompt
    - **If you only want to see the total, and not checkout yet, please use this instead of (enter)**
    - It'll show you all the items in the cart and the subtotal.
- Invoice Prompt (Cash Given: )
    - To enter this screen , press (enter) without any other input in the ID Prompt.
    - Enter the discount %, if there's no discount, enter 0 (Even if you don't it'll automatically assign 0)
    - After it returns the Total, enter the amount of cash given, if the balance is negative, it keeps asking you for the correct amount, until you give the correct amount.
    - Afterwards, it returns the balance, then goes back to main.py
    - ***(Quick Tip: The bill (located in ./bills/) will finish writing to the disk only after the program stops, so whenever free, stop when prompted.)***
- Delete Prompt (The (Name) To Be Removed: )
    - To enter this screen, type 'del' in the ID prompt.
    - Enter the item name of what you wish to delete (The names will be displayed)
    - If successful, it'll say so. Or else, it'll loop until you provide the correct name.
- Kill Prompt (Enter Password: )
    - To enter this screen, type 'Kill' in the ID Prompt.
    - You'll be prompted to enter the password, the default is '627905', feel free to change it (connector.py)
    - If successful, it'll kill the process, make sure you delete the Bill manually, if you tried to checkout before doing the above.