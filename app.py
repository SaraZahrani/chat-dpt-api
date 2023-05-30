from flask import Flask, request

from db.postgres import connect
from integration.opai import get_sql_query

app = Flask(__name__)


@app.route('/get_sql_query', methods=['POST'])
def get_query():
    sql_query = ''

    query = request.form['query']
    if not sql_query:
        db_connection = connect()
        result = get_sql_query(db_connection, query)

        response = result
        return response

    ##TODO handle response


@app.route('/execute_query', methods=['POST'])
def execute_query():
    pass


if __name__ == '__main__':
    app.run()
