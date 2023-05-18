import csv
import database_connection as dc
import sql_statements as ss
import config as h

TABLE_FOLDER = h.config["db_conversion"]["addendum_folder"]


def main():
    write_table_to_database(f"{TABLE_FOLDER}/animals.csv", ss.AnimalSql().update_row)
    return

def write_table_to_database(filename, operate, dry_run=False):
    with open(filename, newline = "") as file:
        reader = csv.reader(file)
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            dc.execute(operate(row), dry_run)
    return


if __name__ == "__main__":
    main()

