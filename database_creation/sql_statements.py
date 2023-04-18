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
        return (s.SQL(("DROP TABLE IF EXISTS {tbl} CASCADE;"
           "CREATE TABLE {tbl}("
           "animal_id bigserial PRIMARY KEY, "
           "name text UNIQUE NOT NULL, "
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
                "VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s);")).format(tbl=s.Identifier(self.table_name)),
                ([values[1], values[2], values[3], values[4], values[5], values[6], values[7]])
                )


    def update_row(self, values):
        return (s.SQL(("UPDATE {tbl} " 
                "SET temperature_low = %s, "
                "temperature_high = %s, "
                "heart_rate_low = %s, "
                "heart_rate_high = %s, "
                "respiratory_rate_low = %s, "
                "respiratory_rate_high = %s "
                "WHERE  name = %s;")).format(tbl=s.Identifier(self.table_name)),
                ([values[2], values[3], values[4], values[5], values[6], values[7], values[1]])
                )

class DrugSql:

    def __init__(self):
        self.table_name = "drugs"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl} CASCADE;"
            "CREATE TABLE {tbl}("
            "drug_id bigserial PRIMARY KEY, "
            "name text UNIQUE NOT NULL"
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {tbl}" 
                "(drug_id, name) "
                "VALUES (DEFAULT, %s);")).format(tbl=s.Identifier(self.table_name)),
                ([values[1]])
                )


class MethodSql:

    def __init__(self):
        self.table_name = "methods"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl} CASCADE;"
            "CREATE TABLE {tbl}("
            "method_id bigserial PRIMARY KEY, "
            "name text UNIQUE NOT NULL"
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {tbl}" 
                "(method_id, name) "
                "VALUES (DEFAULT, %s);")).format(tbl=s.Identifier(self.table_name)),
                ([values[1]])
                )


class UnitSql:

    def __init__(self):
        self.table_name = "units"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl} CASCADE;"
            "CREATE TABLE {tbl}("
            "unit_id bigserial PRIMARY KEY, "
            "name text UNIQUE NOT NULL"
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {tbl}" 
                "(unit_id, name) "
                "VALUES (DEFAULT, %s);")).format(tbl=s.Identifier(self.table_name)),
                ([values[1]])
                )


class ConcentrationSql:

    def __init__(self):
        self.table_name = "concentrations"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl} CASCADE;"
            "CREATE TABLE {tbl}("
            "concentration_id bigserial PRIMARY KEY, "
            "value real, "
            "unit_id bigint REFERENCES units, "
            "dosage_id bigint REFERENCES dosages ON DELETE CASCADE"
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        value = None if values[1] == "None" else values[1]

        return (s.SQL(("INSERT INTO {tbl}" 
                "(concentration_id, value, unit_id, dosage_id) "
                "VALUES (DEFAULT, %s, %s, %s);")).format(tbl=s.Identifier(self.table_name)),
                ([value, strip(values[2]), strip(values[3])])
                )


class DosageSql:

    def __init__(self):
        self.table_name = "dosages"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl} CASCADE;"
            "CREATE TABLE {tbl}("
            "dosage_id bigserial PRIMARY KEY, "
            "animal_id bigint REFERENCES animals, "
            "drug_id bigint REFERENCES drugs, "
            "dose_low real NOT NULL, "
            "dose_high real NOT NULL, "
            "dose_unit_id bigint REFERENCES units, "
            "notes text"
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        notes = None if values[6] == "None" else values[6]

        return (s.SQL(("INSERT INTO {tbl}" 
                "(dosage_id, animal_id, drug_id, dose_low, dose_high, dose_unit_id, notes) "
                "VALUES (DEFAULT, %s, %s, %s, %s, %s, %s);")).format(tbl=s.Identifier(self.table_name)),
                ([strip(values[1]), strip(values[2]), values[3], values[4], strip(values[5]), notes])
                )


class DosagesJoinMethodsSql:

    def __init__(self):
        self.table_name = "delivery"


    def create_table(self):
        return (s.SQL(("DROP TABLE IF EXISTS {tbl} CASCADE;"
            "CREATE TABLE {tbl}("
            "dosage_id bigint REFERENCES dosages ON DELETE CASCADE, "
            "method_id bigint REFERENCES methods, "
            "PRIMARY KEY (dosage_id, method_id) "
            ");")).format(tbl=s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {tbl}" 
                "(dosage_id, method_id) "
                "VALUES (%s, %s);")).format(tbl=s.Identifier(self.table_name)),
                (strip(values[0]), strip(values[1]))
                )


