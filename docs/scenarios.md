# Scenarios and Combatting Them
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