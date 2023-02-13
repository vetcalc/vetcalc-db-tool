import csv
import database_connection as dc
import sql_statements as ss


TABLE_FOLDER = "for_database_import"

def main():
    dc.execute(ss.AnimalSql().create_table())
    dc.execute(ss.DrugSql().create_table())
    dc.execute(ss.MethodSql().create_table())
    dc.execute(ss.CombinationSql().create_table())
    
    write_table_to_database(f"{TABLE_FOLDER}/animals.csv", ss.AnimalSql().insert_row)
    write_table_to_database(f"{TABLE_FOLDER}/drugs.csv", ss.DrugSql().insert_row)
    write_table_to_database(f"{TABLE_FOLDER}/methods.csv", ss.MethodSql().insert_row)
    write_table_to_database(f"{TABLE_FOLDER}/combinations.csv", ss.CombinationSql().insert_row)

    return


def write_table_to_database(filename, insert, dry_run=False):
    with open(filename, newline = "") as file:
        reader = csv.reader(file)
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            dc.execute(insert(row), dry_run)

    return


if __name__ == "__main__":
    main()

