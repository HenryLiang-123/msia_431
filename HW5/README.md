## Hbase

Python script to create the table and the shell scripts are located in folder q1. Each file corresponds to its given task. `body_of_email.sh` returns the bodies of all emails for user Pete Davis (as a single text file). Its output file is `pete_emails.txt`.

 `email_month.sh` returns bodies of all emails written during Feb 2002. Its output file is `feb2002_emails.txt`.

 `user_month_body.sh` returns bodies of all emails of Pete Davis during Feb 2002. Its output file is `pete_feb2002_emails.txt`.

 ## Hive

 The SQL queries for Hive are in the folder q2. It contains the script and the output of that script. The output has 2 columns, the first is the movie id, and the second is frequency. The recommendation system was designed using the following logic: Find all pairs of movies rated by the same person with ranking higher than 3. You need to design a strategy which movie to actually recommend based on these counts.