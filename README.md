# Name
This application is called vaddb as in Veterinarian Application Drug
Database.

# Why

Here are scripts for managing the Postgres database using podman.

The scripts are written in Python to promote readability, though the same
functionality could have been performed in Bash or some other POSIX shell.

Consequently, the scripts are ran with 

```
python my_script.py
```

# Setting config

The provided `example.ini` shows a usable configuration.
However, the file must be renamed or copied to `.env` for the scripts to work.

# Also Included

Is a script to convert the csv file in this folder to some python objects.
The python objects are then used to write some datbase tables in csv format.
Those csv tables are then imported into Postgres.

