from psycopg2 import sql as s

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
        return (s.SQL(("CREATE TABLE IF NOT EXISTS {}("
           "e_id bigint PRIMARY KEY, "
           "name varchar(64) NOT NULL, "
           "temperature int NOT NULL, "
           "heart_rate int NOT NULL, "
           "respiratory_rate int NOT NULL"
           ");")).format(s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {}" 
                "(e_id, name, temperature, heart_rate, respiratory_rate) "
                "VALUES (%s, %s, %s, %s, %s);")).format(s.Identifier(self.table_name)),
                (values[0].get(True), values[1], values[2], values[3], values[4])
                )


class DrugSql:

    def __init__(self):
        self.table_name = "drugs"


    def create_table(self):
        return (s.SQL(("CREATE TABLE IF NOT EXISTS {}("
           "e_id bigint PRIMARY KEY, "
           "name varchar(64) NOT NULL"
           ");")
            ).format(s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {}" 
                "(e_id, name) "
                "VALUES (%s, %s);")).format(s.Identifier(self.table_name)),
                (values[0].get(True), values[1])
                )


class MethodSql:

    def __init__(self):
        self.table_name = "methods"


    def create_table(self):
        return (s.SQL(("CREATE TABLE IF NOT EXISTS {}("
           "e_id bigint PRIMARY KEY, "
           "name varchar(64) NOT NULL"
           ");")
            ).format(s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {}" 
                "(e_id, name) "
                "VALUES (%s, %s);")).format(s.Identifier(self.table_name)),
                (values[0].get(True), values[1])
                )


class CombinationSql:

    def __init__(self):
        self.table_name = "combinations"


    def create_table(self):
        return (s.SQL(("CREATE TABLE IF NOT EXISTS {}("
           "e_id bigint PRIMARY KEY, "
           "animal bigint REFERENCES animals,"
           "for_juvenile bool NOT NULL,"
           "combined_with varchar,"
           "purpose varchar,"
           "notes varchar,"
           "reference varchar"
           ");")).format(s.Identifier(self.table_name)), None)
           
 
    def insert_row(self, values):
        return (s.SQL(("INSERT INTO {}" 
                "(e_id, animal, for_juvenile, combined_with, purpose, notes, reference) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s);")).format(s.Identifier(self.table_name)),
                (values[0].get(True), values[1].get(True), values[2], values[3], 
                 values[4], values[5], values[6])
                )

