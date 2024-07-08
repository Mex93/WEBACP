import re


def is_cirylic(text: str):
    return bool(re.search('[а-яА-Я]', text))


def is_palletsn_valid(text: str):
    lenght = len(text)
    if not lenght:
        return False

    if lenght < 3:
        return False

    return True
