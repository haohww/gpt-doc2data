import tiktoken

result_average_token = 100


def token_limit(model: str):
    if model == "gpt-3.5-turbo-16k":
        return 16384


def get_encoding(model="gpt-3.5-turbo-16k"):
    try:
        encoding = tiktoken.encoding_for_model(model)
        return encoding
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
        return encoding


def num_tokens_from_messages(message, model="gpt-3.5-turbo-16k"):
    """Return the number of tokens used by a list of messages."""
    encoding = get_encoding(model)
    return (
        len(encoding.encode(message)) + 3
    )  # every reply is primed with <|start|>assistant<|message|>


def split_string_by_token_length(context: dict, long_string: str) -> list[str]:
    token_length = (
        token_limit(context["model"])
        - num_tokens_from_messages(context["question_generator"])
        - result_average_token * context["num_data"]
    )
    substrings = []
    current_tokens = []

    encoding = get_encoding(context["model"])
    tokens = encoding.encode(long_string)

    for token in tokens:
        if len(current_tokens) >= token_length:
            substrings.append(encoding.decode(current_tokens).strip())
            current_tokens = []
        else:
            current_tokens.append(token)

    if len(current_tokens):
        substrings.append(encoding.decode(current_tokens).strip())

    return substrings
