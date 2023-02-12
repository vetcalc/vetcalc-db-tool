# local modules
import table_writing as tw
import deduplication as ddp
import make_objects as mo
import id_replacement as ri
import print_debug as pd

def main():
    entities = mo.make_entities()
    ddp.dedup_entities(entities)
    ri.replace_with_ids(entities)
    # pd.show_entities(entities)
    tw.write_tables_as_csv(entities)

if __name__ == "__main__":
    main()
