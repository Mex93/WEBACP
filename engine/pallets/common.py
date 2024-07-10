import re

MAX_DEVICES_ON_PALLET = 5 * 12


def is_cirylic(text: str):
    return bool(re.search('[а-яА-Я]', text))


def is_palletsn_valid(text: str):
    lenght = len(text)
    if not lenght:
        return False

    if lenght < 3:
        return False

    return True


def is_devicesn_valid(text: str):
    lenght = len(text)
    if not lenght:
        return False

    if lenght < 3:
        return False

    return True
