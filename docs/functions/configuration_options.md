# Configuration Options (./credentials/options.yml)
- check_for_updates
  - Set to True if you want the program to check for updates, and auto-update, each time you run (main.py)
  - Set to False if you want the program to ignore the updates, so you can manually `git pull origin` whenever.
- check_file_integrity
    - Set to True if you want the program to check if the password and hash file have been tampered with **while they're not deleted**.
    - Set to False if you don't want the program to check if the password and hash files have been tampered with while they're not deleted.
      > Regardless Of What You Choose, If One Of The Two Aforementioned Files Are Absent, It'll Detect It And Recover.
- transactions
    - Set this to true to use Transactions instead of cash.
    - If selected, it'll display a 7th option in main.py
    - This will allow you to modify who's transferred or not
    - Even if you change it back to Cash, your progress with the transfers will not be affected.
- vat
    - Set to true to add 15% VAT to the bill, if false, it'll just show the grand total.
- discount
    - Set to true to show a discount screen when making a bill
