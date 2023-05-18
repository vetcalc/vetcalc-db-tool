# VetCalc Database

##  What

Here is a compose specification for starting a Postgres database container.

In addition are some scripts to fill the container with drug data
found in `db_init/drugs.csv`

## Setting config

The password for the database should be specified in `db.env` with
`POSTGRES_PASSWORD=replace-me-with-your-password`

A second set of configuration, used by `db_init/main.py` should be
specified in `.env`. A complete working example is shown in `example.ini`.

The section named `db_connection` should have the relevant information
from `db.env` and the `compose.yaml` file for the `db_init/main.py`
to connect to the datbase running in the container.

The database files are stored in the `data` folder by default, and may need
to be created if not already present.

## Running the container and filling it

Start the database container with `podman-compose up -d` if you use podman.
or `docker-compose up -d` if you use docker.

Once the container is running, move to the `db_init` directory 
and run

```
pip install -r requirements.txt
``` 

to ensure that the needed packages are installed.

Then run

```
python main.py --init
```

to initialize the database with drug information.

You can verify that the initialize worked by connecting to the database with

```
podman exec -it vetcalc_db_postgres_1 psql -U postgres -d vcdb
```

(or the docker equivalent).

Note that `vetcalc_db_postgres_1`, `postgres`, and `vcdb` are subject to
change if the configuration in `compose.yaml` is modified accordingly.


