import add_addendum
import csv_from_input
import csv_to_postgres

import argparse

parser = argparse.ArgumentParser(description="db data creation scripts")

parser.add_argument("--init", 
                    nargs="?",
                    const="init",
                    help="performs all the steps to fill the database with starting data")

args = parser.parse_args()

if args.init:
    confirmation = input((
        "Are you certain you want to initialize the database?\n"
        "Doing so will reset the entire database.\n"
        "Any new data will be lost or replaced with the data defined in drugs.csv\n"
        "[y/N]: "))

    if confirmation.lower() == "y":
        print("initializing/resetting the database")
        csv_from_input.main()
        csv_to_postgres.main()
        add_addendum.main()

    else:
        print("aborting the process")


