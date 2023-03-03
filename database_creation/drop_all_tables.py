import database_connection as dc
from psycopg2 import sql
import sql_statements as ss

def main():
    dc.execute((sql.SQL("DROP TABLE {tbl}").format(tbl=sql.Identifier(ss.DosagesJoinMethodsSql().table_name)), None))
    dc.execute((sql.SQL("DROP TABLE {tbl}").format(tbl=sql.Identifier(ss.ConcentrationSql().table_name)), None))
    dc.execute((sql.SQL("DROP TABLE {tbl}").format(tbl=sql.Identifier(ss.DosageSql().table_name)), None))
    dc.execute((sql.SQL("DROP TABLE {tbl}").format(tbl=sql.Identifier(ss.AnimalSql().table_name)), None))
    dc.execute((sql.SQL("DROP TABLE {tbl}").format(tbl=sql.Identifier(ss.DrugSql().table_name)), None))
    dc.execute((sql.SQL("DROP TABLE {tbl}").format(tbl=sql.Identifier(ss.MethodSql().table_name)), None))
    dc.execute((sql.SQL("DROP TABLE {tbl}").format(tbl=sql.Identifier(ss.UnitSql().table_name)), None))
    return

if __name__ == "__main__":
    main()
