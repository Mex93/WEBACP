


def is_devicesn_valid(text: str):
    lenght = len(text)
    if not lenght:
        return False

    if lenght < 3:
        return False

    return True
