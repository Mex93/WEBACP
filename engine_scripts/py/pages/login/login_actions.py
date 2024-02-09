from engine_scripts.py.users.CUser import CUser

def set_login(nickname: str, password: str, remember_me: bool):

    if nickname == "" or password == "":
        return False, "Ничего не указано!"

    if CUser.check_user_nickname(nickname) is False:
        return False, "Login указан не верно!"

    if CUser.check_user_password(password) is False:
        return False, "Пароль указан не верно!"

    return True
