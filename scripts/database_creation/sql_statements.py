from psycopg2 import sql as s
from entity_id import strip
'''
NOTE:
    The sql statements crafted here are for use with psycopg2.
    That is why they use %s for variable substitution.

    see https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
    for more information
'''

class AnimalSql:

    def __init__(self):
        self.table_name = "animals"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS{tbl};"
           "CREATE TABLE {tbl}("
           "animal_id serial PRIMARY KEY, "
           "name text NOT NULL, "
           "temperature_low real NOT NULL, "
           "temperature_high real NOT NULL, "
           "heart_rate_low real NOT NULL, "
           "heart_rate_high real NOT NULL, "
           "respiratory_rate_low real NOT NULL, "
           "respiratory_rate_high real NOT NULL"
           ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {tbl}" 
                "(animal_id, name, temperature_low, temperature_high, heart_rate_low, heart_rate_high, respiratory_rate_low, respiratory_rate_high) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);")).format(tbl=s.Identifier(self.table_name)),
                (strip(values[0]), values[1], values[2], values[3], values[4], values[5], values[6], values[7])
                )


class DrugSql:

    def __init__(self):
        self.table_name = "drugs"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl};"
            "CREATE TABLE {tbl}("
            "drug_id serial PRIMARY KEY, "
            "name text NOT NULL"
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {tbl}" 
                "(drug_id, name) "
                "VALUES (%s, %s);")).format(tbl=s.Identifier(self.table_name)),
                (strip(values[0]), values[1])
                )


class MethodSql:

    def __init__(self):
        self.table_name = "methods"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl};"
            "CREATE TABLE {tbl}("
            "method_id serial PRIMARY KEY, "
            "name text NOT NULL"
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {tbl}" 
                "(method_id, name) "
                "VALUES (%s, %s);")).format(tbl=s.Identifier(self.table_name)),
                (strip(values[0]), values[1])
                )


class UnitSql:

    def __init__(self):
        self.table_name = "units"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl};"
            "CREATE TABLE {tbl}("
            "unit_id serial PRIMARY KEY, "
            "name text NOT NULL"
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {tbl}" 
                "(unit_id, name) "
                "VALUES (%s, %s);")).format(tbl=s.Identifier(self.table_name)),
                (strip(values[0]), values[1])
                )


class ConcentrationSql:

    def __init__(self):
        self.table_name = "concentrations"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl};"
            "CREATE TABLE {tbl}("
            "concentration_id serial PRIMARY KEY, "
            "value real, "
            "unit_id int REFERENCES units, "
            "dosage_id int REFERENCES dosages"
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        if values[1] == "None":
            value = None
        else:
            value = values[1]

        return (s.SQL(("INSERT INTO {tbl}" 
                "(concentration_id, name, unit_id, dosage_id) "
                "VALUES (%s, %s, %s, %s);")).format(tbl=s.Identifier(self.table_name)),
                (strip(values[0]), value, strip(values[2]), strip(values[3]),)
                )





class DosageSql:

    def __init__(self):
        self.table_name = "dosages"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl};"
            "CREATE TABLE IF NOT EXISTS {tbl}("
            "dosage_id serial PRIMARY KEY, "
            "animal_id int REFERENCES animals, "
            "drug_id int REFERENCES drugs, "
            "dose_low real NOT NULL, "
            "dose_high real NOT NULL, "
            "dose_unit_id REFERENCES units, "
            "notes text"
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {tbl}" 
                "(e_id, animal, for_juvenile, combined_with, purpose, notes, reference) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s);")).format(tbl=s.Identifier(self.table_name)),
                (strip(values[0]), strip(values[1]), strip(values[2]), values[3], 
                 values[4], strip(values[5]), values[6])
                )


class DosagesJoinMethodsSql:

    def __init__(self):
        self.table_name = "delivery"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl};"
            "CREATE TABLE {tbl}("
            "dosage_id int REFERENCES dosages, "
            "method_id int REFERENCES methods "
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {tbl}" 
                "(dosage_id, method_id) "
                "VALUES (%s, %s);")).format(tbl=s.Identifier(self.table_name)),
                (strip(values[0]), strip(values[1]))
                )


