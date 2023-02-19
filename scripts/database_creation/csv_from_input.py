# local modules
import table_writing as tw
import make_objects as mo
import id_replacement as ri

def main():
    entities = mo.make_entities()
    # ri.replace_with_ids(entities)
    # tw.write_tables_as_csv(entities)

if __name__ == "__main__":
    main()
