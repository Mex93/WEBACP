import re
def is_devicesn_valid(text: str):
    lenght = len(text)
    if not lenght:
        return False

    if lenght < 3:
        return False

    return True

def is_cirylic(text: str):
    return bool(re.search('[а-яА-Я]', text))
