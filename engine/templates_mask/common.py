import re

MAX_INPUT_FIELD_LEN = 64


def is_field_len(field_text: str) -> bool:
    if len(field_text) < MAX_INPUT_FIELD_LEN:
        return True
    return False


def is_cirylic(text: str):
    return bool(re.search('[а-яА-Я]', text))
