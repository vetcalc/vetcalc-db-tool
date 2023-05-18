# VetCalc Database

##  What

Here is a compose specification for starting a Postgres database container.

In addition are some scripts to fill the container with drug data
found in `db_init/drugs.csv`

## Setting config

The config is specified as environment variables in `.env`.
A complete example is found in `example.env`.

Setting the environment variables is operating system dependent.
In **Linux**, one can set the env var with 

```
set -a
. ./env
set +a
```

The database files are stored in the `data` folder by default, and may need
to be created if not already present.

## Running the container and filling it

Start the database container with `./s_up.sh`. And stop the container with `./s_down.sh`.
These helper scripts are only tested on Linux.

> ###**IMPORTANT**
>
> The first time the database is initalized, run `./s_login.sh`
>
> After entering the database container, the command `ALTER USER user PASSWORD 'password';`
> must be ran, replacing `user` with the user environment variable and `password`
> with the password environement variable.
>
> Failure to set the password like so will you unable to connect to the database from outside
> the container.

Once the container is running, move to the `db_init` directory 
and run

```
pip install -r requirements.txt
python main.py --init
``` 

This will install the needed python packages, and then run the
initialization process.

