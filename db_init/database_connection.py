import psycopg2
import config as h

def execute(sql, dry_run=False):
    conn = _create_db_connection()

    if conn is not None:
        try:
            _execute_transaction(conn, sql, dry_run)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            conn.close()


def _create_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(**h.config["db_connection"])
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        return conn
       

def _execute_transaction(conn, sql, dry_run):
   with conn:
        with conn.cursor() as curs:
            query = curs.mogrify(*sql)
            if dry_run:
                print(query)
            if not dry_run:
                curs.execute(*sql)
                conn.commit()


