import tiktoken


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
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print(
            "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return num_tokens_from_messages(message, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
        )
        return num_tokens_from_messages(message, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )

    return (
        len(encoding.encode(message)) + 3
    )  # every reply is primed with <|start|>assistant<|message|>


def split_string_by_token_length(context: dict, long_string: str) -> list[str]:
    token_length = token_limit(context["model"]) 
    - num_tokens_from_messages(context["system_prompts"]["question_generator"]),


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


# import config
# context = config.load_config()
# context['model'] = "gpt-3.5-turbo-16k"
# print(split_string_by_token_length(context, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"))
