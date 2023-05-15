# local modules
import table_writing as tw
import make_objects as mo
import subprocess as sp
import config as h

TABLE_FOLDER = h.config["db_conversion"]["for_import_folder"]

def main():

    # create a folder to hold the import files if not exists
    sp.run(["mkdir", TABLE_FOLDER])

    entities = mo.make_entities()
    tw.write_tables_as_csv(entities)

if __name__ == "__main__":
    main()
