import tiktoken

def count_tokens(text):
    encodings = tiktoken.get_encoding("cl100k_base")
    tokens = encodings.encode(text)

    return len(tokens)