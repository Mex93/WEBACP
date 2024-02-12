from engine.users.CUser import CUser


def check_login_params(nickname: str, password: str, remember_me: bool) -> tuple[bool, list]:
    error_messages = list()
    if nickname == "" or password == "":
        error_messages.append("Одно из полей не заполнено!")

    if CUser.check_user_nickname(nickname) is False:
        error_messages.append("Login указан не верно!")

    if CUser.check_user_password(password) is False:
        error_messages.append("Пароль указан не верно!")

    if len(error_messages) > 0:
        return False, error_messages

    return True, []
