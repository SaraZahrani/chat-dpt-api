
from flask import Flask

from db.clickhouse import connect

app = Flask(__name__)


@app.post('/get_sql_query')
def get_sql_query(query):
    sql_query = ''
    if not sql_query:
        db_connection = connect()
        result = get_sql_query(db_connection, query)

        sql_query = result.content

        return {"query": sql_query}

