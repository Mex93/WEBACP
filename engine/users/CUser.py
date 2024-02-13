import re
import engine.users.common as ccommon
from engine.users.enums import USER_ALEVEL


class CUser:

    def __init__(self):
        pass

    @staticmethod
    def is_password_valid(text: str) -> bool:
        if re.search(r'[^a-zA-Z0-9]', text):
            return False
        return True

    @staticmethod
    def is_nickname_valid(text: str) -> bool:
        if re.search(r'[^a-zA-Z0-9@]', text):
            return False
        return True

    @staticmethod
    def is_firstname_valid(text: str) -> bool:
        if re.search(r'[^а-яА-Я0-9]', text):
            return False
        return True

    @staticmethod
    def check_user_password(user_pass: str) -> bool:
        if isinstance(user_pass, str):
            lenpass = len(user_pass)
            if ccommon.MIN_USER_PASSWORD_LEN <= lenpass <= ccommon.MAX_USER_PASSWORD_LEN:
                if CUser.is_password_valid(user_pass):
                    return True

        return False

    @staticmethod
    def check_user_nickname(user_nickname: str) -> bool:
        if isinstance(user_nickname, str):
            lenpass = len(user_nickname)
            if ccommon.MIN_USER_NICKNAME_LEN <= lenpass <= ccommon.MAX_USER_NICKNAME_LEN:
                if CUser.is_nickname_valid(user_nickname):
                    return True

        return False

    @staticmethod
    def check_user_firstname(user_nickname: str) -> bool:
        if isinstance(user_nickname, str):
            lenpass = len(user_nickname)
            if ccommon.MIN_USER_FIRSTNAME_LEN <= lenpass <= ccommon.MAX_USER_FIRSTNAME_LEN:
                if CUser.is_nickname_valid(user_nickname):
                    return True

        return False

    @staticmethod
    def check_alevel_for_user(alevel: int) -> bool:
        for level in USER_ALEVEL:
            if level != alevel:
                continue
            else:
                return True
        return False

    @staticmethod
    def check_login_params(nickname: str, password: str) -> tuple[bool, list]:
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
