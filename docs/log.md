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

(21st October)
><font size="6">I recently discovered this framework called "rich" for python. So I installed it, and boy was it amazing!
> I replaced all the text with the "colours" class earlier with rich. I also added functions like warn, info and all
> Instead of the old boring tables, now there's an alive one, thanks again, to rich! (when you click --)<br>
> I also changed the bill format from .txt to markdown. So now I have styled it colours and all, and of course
> changed all the other files accordingly (was quite a pain, but worth it).</font>