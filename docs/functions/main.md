# Function List (main.py)
- Random Line From HUMBLE:
    - Just as advertised, it just displays a random line from HUMBLE by Kendrick Lamar
- Enter Password:
    - If this is your first time setup, or if you deleted ./credentials/passwd.txt, this prompt will appear.
    - It covers the input, so it looks like you're not typing anything, but you are.
    - It'll then generate salts and hash it, and store it in (passwd.txt)
- The Main Prompt:
    - If you press 1, it'll stop the program.
    - If you press 2, it'll loop back to (connector.py)
    - If you press 3, it'll run  (master-bill.py) and get the total of all bills made today.
        - Don't worry about accidentally running it, it'll always rewrite the file, so run it as many
          times as you want.
        - It'll automatically generate a weekly sales report (./sales_reports/**) With The Grand Totals Of 7 Days.
          If there's < 7 Days after the initial, It'll have no issue, it'll mention them.
    - If you press 4, it'll take you to (sql-client.py) where you can view and alter entries.
    - If you press 5, it'll take you to (verify.py) where you can verify your bills.
    - If you press 6, it'll take you to an interface, allowing you to modify your configuration.
    - If you selected 'Bank Transfer Mode' there'll be a number 7, which will allow you to track who sent transfers and didn't.
      - There's two functions, view transactions and edit transactions.
      - In view, it displays all the transactions (If there are multiple under the same name, it'll display the time)
      - In edit, it shows you the transactions, prompts you for a name, and you can edit if they've transfered or not.
