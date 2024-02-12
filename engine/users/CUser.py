import re
import engine.users.common as ccommon


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
