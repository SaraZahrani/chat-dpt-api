import os
import openai
import tiktoken

from db.postgres import get_introspection, connect

openai.api_key = "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"


def create_message(query, db_connection, introspection, history="", history_mode=False):
    schema = introspection

    message = [
        {"role": "system",
         "content": "You are a database developer that only responds in " + db_connection.info.dbname + " without formatting"},
        {"role": "system", "content": "uuids should be generated with gen_random_uuid()"},
        {"role": "system", "content": "queries on strings should be case insensitive"},
        {"role": "system", "content": "database: " + schema.__str__()},
        {"role": "user", "content": query}]

    return message


def calculate_token(messages, model):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0

    for message in messages:
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))

            if key == "name":
                num_tokens += -1
    num_tokens += 2
    return num_tokens


def get_sql_query(db_connection, query):
    try:
        introspection = get_introspection()
        messages = create_message(query, db_connection, introspection)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= messages,
            temperature=0
        )

        # print(response)
        sql_query = response['choices'][0]['message'].content
        mum_of_token = calculate_token(messages, 'gpt-3.5-turbo')

        return {'query': sql_query, 'token': mum_of_token}
    except Exception as e:
        print(e.__str__())


if __name__ == '__main__':
    introspection = get_introspection()
    db_connection = connect()
    m = create_message("add new student", db_connection, introspection)
    token = calculate_token(m, 'gpt-3.5-turbo-0301')
    print(token)
