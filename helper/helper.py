import tiktoken


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