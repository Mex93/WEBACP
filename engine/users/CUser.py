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
        if re.search(r'[^a-zA-Z0-9]', text):
            return False
        return True

    @staticmethod
    def is_email_valid(text: str) -> bool:
        if re.search(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', text):
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
    def check_user_email(user_email: str) -> bool:
        if isinstance(user_email, str):
            lenpass = len(user_email)
            if ccommon.MIN_USER_EMAIL_LEN <= lenpass <= ccommon.MAX_USER_EMAIL_LEN:
                if CUser.is_email_valid(user_email):
                    return True

        return False

    @staticmethod
    def check_user_firstname(user_nickname: str) -> bool:
        if isinstance(user_nickname, str):
            lenpass = len(user_nickname)
            if ccommon.MIN_USER_FIRSTNAME_LASTNAME_LEN <= lenpass <= ccommon.MAX_USER_FIRSTNAME_LASTNAME_LEN:
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
    def check_login_params(email: str, password: str) -> str | bool:
        if email == "" or password == "":
            return f"errorcode: check_login_params -> [1]"

        if CUser.check_user_email(email) is False:
            return f"errorcode: check_login_params -> [2]"

        if CUser.check_user_password(password) is False:
            return f"errorcode: check_login_params -> [3]"

        return True

    @staticmethod
    def check_repass_params(email: str, old_pass: str, new_pass: str, re_pass: str) -> str | bool:
        if email == "" or old_pass == "" or new_pass == "" or re_pass == "":
            return f"errorcode: check_repass_params -> [1]"

        if CUser.check_user_email(email) is False:
            return f"errorcode: check_repass_params -> [2]"

        if CUser.check_user_password(old_pass) is False:
            return f"errorcode: check_repass_params -> [3]"

        if CUser.check_user_password(new_pass) is False:
            return f"errorcode: check_repass_params -> [4]"

        if CUser.check_user_password(re_pass) is False:
            return f"errorcode: check_repass_params -> [5]"

        return True
