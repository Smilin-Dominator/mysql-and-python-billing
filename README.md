# MySQL and Python Billing Logs

(22nd May)
><font size="9">I made this random program to test out if I could extract data from a MySQL Server
>And Add Them All And Get The Balance. And it succeeded! After 3 Days of trying I gave up on it
>But then randomly picked it up 3 weeks later, and fixed the bugs!</font><br>

(29th May)
><font size="9">Added a billing system. So now all progress is logged properly, and saved. Instead
>of specifying how many items there can be, you keep on adding items, and when you're done, hit enter in the ID input
>(without any text) and it'll process the data and create an invoice.</font>
# How To Use It?

<font size="9">Replace the SQL Credentials and Query to your own. If you want to, tweak any setting, just make sure
you know what you're doing, or else, you'll be doomed!</font>

### Running
<font size="9">Run main.py in a directory where you have full permissions. It should automatically make a 
DIR called 'bills', remember all the soft copies of the bills will be written over there
. Then enter the IDs, once your done, hit enter when it prompts for the ID again.<br>
In case you accidentally put the wrong amount (for the Cash Recieved), the computer calculates the balance before writing it,
so if it detects that its < 0, it'll loop (without writing the output) until the balance gets an answer >= 0, and only then, will
it write the amount of cash recieved and the balance.</font>