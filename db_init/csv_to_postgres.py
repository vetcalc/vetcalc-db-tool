import csv
import database_connection as dc
import sql_statements as ss
import config as h

TABLE_FOLDER = h.config["db_conversion"]["for_import_folder"]

def main():
    dc.execute(ss.AnimalSql().create_table())
    dc.execute(ss.DrugSql().create_table())
    dc.execute(ss.MethodSql().create_table())
    dc.execute(ss.UnitSql().create_table())
    dc.execute(ss.DosageSql().create_table())
    dc.execute(ss.ConcentrationSql().create_table())
    dc.execute(ss.DosagesJoinMethodsSql().create_table())
    
    write_table_to_database(f"{TABLE_FOLDER}/animals.csv", ss.AnimalSql().insert_row)
    write_table_to_database(f"{TABLE_FOLDER}/drugs.csv", ss.DrugSql().insert_row)
    write_table_to_database(f"{TABLE_FOLDER}/methods.csv", ss.MethodSql().insert_row)
    write_table_to_database(f"{TABLE_FOLDER}/units.csv", ss.UnitSql().insert_row)
    write_table_to_database(f"{TABLE_FOLDER}/dosages.csv", ss.DosageSql().insert_row)
    write_table_to_database(f"{TABLE_FOLDER}/concentrations.csv", ss.ConcentrationSql().insert_row)
    write_table_to_database(f"{TABLE_FOLDER}/dosages_join_methods.csv", ss.DosagesJoinMethodsSql().insert_row)

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

