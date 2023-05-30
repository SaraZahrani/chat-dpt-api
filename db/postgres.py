#!/usr/bin/python
import psycopg2


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="postgres",
            user="sarah",
            password="1234")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return conn
            # conn.close()
            # print('Database connection closed.')


def get_introspection():
    conn = connect()
    cur = conn.cursor()

    cur.execute('SELECT table_name, column_name, data_type as column_type, column_default, is_nullable as column_is_nullable '
                'FROM information_schema.columns where table_schema = \'public\'')

    result = cur.fetchall()

    dict = {}
    for tup in result:
        if not dict.keys().__contains__(tup[0]):
            dict[tup[0]] = {'columns': {
                tup[1]: {
                    'type': tup[2],
                    'description': tup[3],
                    'required': tup[4]
                }
            }}
        else:
            new_columns = dict.get(tup[0])
            new_columns.get('columns').update({
                tup[1]: {
                    'type': tup[2],
                    'description': tup[3],
                    'required': tup[4]
                }
            })

            dict.get(tup[0]).update(new_columns)
    cur.close()

    return dict


def run_sql_query(query):
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(query)
        cur.close()
        return True

    except Exception as e:
        print(e.__str__())
        return False
