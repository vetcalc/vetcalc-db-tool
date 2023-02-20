# local modules
import table_writing as tw
import make_objects as mo

def main():
    entities = mo.make_entities()
    tw.write_tables_as_csv(entities)

if __name__ == "__main__":
    main()
