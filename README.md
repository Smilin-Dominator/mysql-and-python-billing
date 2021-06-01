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

### Prerequisites
<font size="6">You should have an 'Anaconda' Environment, with Python 3.7.10<br>Here's how you make one
- Download the latest version for your OS [here](https://www.anaconda.com/products/individual).
- After installation open up powershell, type this; `conda env list`
- If you see something similar to this;
    ```
    C:\Users\Devisha> conda env list
    # conda environments:
    #
    base                  *  C:\Users\Devisha\anaconda3
    ```
  then the installation was successful!
- Then you're good to go! Just run main.py, it'll check for log.txt, if it's not present, it'll run
  the shell script related to your OS! **Do Not Delete Your log.txt, If you want you may clear it, but not delete it.**

### Condensed
<font size="6">In the ID Screen, enter an ID, if you want to check
the invoice use '--', if you want to delete an item from the current list type 'del' and
follow the on-screen prompt, if you want to update the quantity of an item, type
update, and interact with the prompt. If for whatever reason, you want to kill the process, use
Kill, and enter the password '627905'. Once you're 100% sure you're done adding the items and everything
hit (enter) without any other input in the ID Screen to create the bill, you may enter a discount here.</font>

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
#### Conclusion
Hope these scenarios helped you! I'll add more along with the new features that I add!
<br>***Note: for a more detailed explanation of the functions, check the list below!***
</font>

# Function List
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
    - ***(Quick Tip: The bill (located in ./bills/) will finish writing to the disk only after the program stops, so whenever free, stop when prompted.)***
- Delete Prompt (The (Name) To Be Removed: )
    - To enter this screen, type 'del' in the ID prompt.
    - Enter the item name of what you wish to delete (The names will be displayed)
    - If successful, it'll say so. Or else, it'll loop until you provide the correct name.
- Kill Prompt (Enter Password: )
    - To enter this screen, type 'Kill' in the ID Prompt.
    - You'll be prompted to enter the password, the default is '627905', feel free to change it (connector.py)
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
