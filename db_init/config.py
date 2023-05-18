import configparser
import os

config = configparser.ConfigParser()
config.read("app.ini")


# setting other config here to use the environment variables
config.set("db_connection", "host", os.environ.get("VCDB_HOST"));
config.set("db_connection", "port", os.environ.get("VCDB_PORT"));
config.set("db_connection", "database", os.environ.get("VCDB_DB"));
config.set("db_connection", "user", os.environ.get("VCDB_USER"));
config.set("db_connection", "password", os.environ.get("VCDB_PASSWORD"));
