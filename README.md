# Name
This application is called vaddb as in Veterinarian Application Drug
Database.

# Why

Here are scripts for managing the Postgres database using podman.

The scripts are written in Python to promote readability, though the same
functionality could have been performed in Bash or some other POSIX shell.

The scripts are combined togethere with main.py
Consequently, the help for the scripts is printed with

```
python main.py -h
```

when **inside** the `container` folder.

For example, to start the database container, do

```
cd container
python main.py --start
cd -
```

# Setting config

The provided `example.ini` shows a usable configuration.
However, the file must be renamed or copied to `.env` for the scripts to work.

# Also Included

Is a script to convert the csv file in this folder to some python objects.
The python objects are then used to write some datbase tables in csv format.
Those csv tables are then imported into Postgres.

The scripts for the conversion start with the `main.py` inside `database_creation`

**NOTE** the datbase container inside `container` directory must be started
for the conversion scripts to have something to connect to.

Run the main conversion with

```
cd database_creation
python main.py --init
cd -
```

