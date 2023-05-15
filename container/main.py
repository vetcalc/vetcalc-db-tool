import start
import login
import delete

import argparse

parser = argparse.ArgumentParser(description="db container interface methods")

parser.add_argument("--start", 
                    nargs="?",
                    const="start",
                    help="start the db container. will fail if container already exists")

parser.add_argument("--login", 
                    nargs="?",
                    const="login",
                    help="log in to a running container. fails if container does not exist")

parser.add_argument("--stop", 
                    nargs="?",
                    const="delete",
                    help="alias for delete")

parser.add_argument("--delete", 
                    nargs="?",
                    const="delete",
                    help="stops the running container, and deletes them from the runtime. Does not delete the associated database data, however")

args = parser.parse_args()

if args.start:
    start.start_database()

if args.login:
    login.login_database()

if args.stop:
    delete.delete_database()

if args.delete:
    delete.delete_database()
