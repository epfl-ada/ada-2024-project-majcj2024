import tiktoken

def tokenize_text(s):
    """
    tokenize_text - tokenizes a given text with the gpt-4o encoding model.

    Inputs: - s (str): text to be tokenized

    Outputs: - tokens (list of int): tokenized text
    """
    enc = tiktoken.encoding_for_model('gpt-4o')
    tokens = enc.encode(str(s))
    return tokens