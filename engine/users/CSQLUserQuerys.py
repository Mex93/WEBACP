from werkzeug import security

from engine.sql.CSQLAgent import CSqlAgent
from engine.sql.sql_data import SQL_TABLE_NAME, SQL_USERS_FIELDS
from engine.users.enums import USER_SECTIONS_TYPE

PROGRAM_TIME_TYPE = "0300"  # Russia
SALT_LEN = 30


class CSQLUserQuerys(CSqlAgent):
    def __init__(self):
        super().__init__()

    def get_login(self, nickname: str, password: str):
        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.user_accounts} "
                        f"WHERE {SQL_USERS_FIELDS.ufd_nickname} = %s "
                        f"LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (nickname,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_pass = result[0].get(SQL_USERS_FIELDS.ufd_md5pass, None)
        if sql_pass is not None:
            hash_pass = security.check_password_hash(sql_pass, password)
            # print(hash_pass)
            if hash_pass is True:
                return True, result
        return False

    def get_nickname_from_user_id(self, uid: int) -> str | bool:

        query_string = (f"SELECT {SQL_USERS_FIELDS.ufd_nickname} "
                        f"FROM {SQL_TABLE_NAME.user_accounts} "
                        f"WHERE {SQL_USERS_FIELDS.ufd_index} = %s "
                        f"LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (uid,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_USERS_FIELDS.ufd_nickname, None)
        if sql_result is not None:
            return sql_result
        return False

    def update_SQL_account_alevel(self, user_id: int, admin_level: int):
        query = (f"UPDATE {SQL_TABLE_NAME.user_accounts} SET "
                 f"{SQL_USERS_FIELDS.ufd_admin_level} = %s "
                 f"WHERE {SQL_USERS_FIELDS.ufd_index} = %s")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query, (admin_level, user_id, ), "_u")

        return result

    def update_SQL_account_lastlogin(self, user_id: int):
        query = (f"UPDATE {SQL_TABLE_NAME.user_accounts} SET "
                 f"{SQL_USERS_FIELDS.ufd_last_login_date} = now() "
                 f"WHERE {SQL_USERS_FIELDS.ufd_index} = %s")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query, (user_id,), "_u")

        return result

    def update_SQL_account_password(self, user_id: int, password: str):
        if password is False or user_id is False:
            return False
        global SALT_LEN
        hash_pass = security.generate_password_hash(password, method="pbkdf2:sha256", salt_length=SALT_LEN)

        query = (f"UPDATE {SQL_TABLE_NAME.user_accounts} SET "
                 f"{SQL_USERS_FIELDS.ufd_md5pass} = %s "
                 f"WHERE {SQL_USERS_FIELDS.ufd_index} = %s")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query, (hash_pass, user_id,), "_u")

        return result

    def get_repass(self, u_id: int, password: str, new_pass: str):
        global SALT_LEN

        query_string = (f"SELECT {SQL_USERS_FIELDS.ufd_index}, {SQL_USERS_FIELDS.ufd_md5pass} "
                        f"FROM {SQL_TABLE_NAME.user_accounts} "
                        f"WHERE {SQL_USERS_FIELDS.ufd_index} = %s "
                        f"LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (u_id,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_pass = result[0].get(SQL_USERS_FIELDS.ufd_md5pass, None)
        if sql_pass is not None:
            hash_pass = security.check_password_hash(sql_pass, password)
            # print(hash_pass)
            if hash_pass is False:
                return False, "Старый пароль не совпадает с указанным"

            old_pass_hach = security.check_password_hash(sql_pass, new_pass)
            if old_pass_hach is True:
                return False, "Старый и новый пароли не должны совпадать"

            return True, "Проверка пароля успешно пройдена"

        return False, "Аккаунт не найден"

    def update_SQL_account_checkboxes(self, user_id: int, users_cb: dict):
        query = (f"UPDATE {SQL_TABLE_NAME.user_accounts} SET "
                 f"{SQL_USERS_FIELDS.ufd_account_timeout_exit} = %s "
                 f"WHERE {SQL_USERS_FIELDS.ufd_index} = %s")

        u_cb_timeout_exit = users_cb.get(USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT, None)
        if u_cb_timeout_exit is None:
            return False
        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query, (u_cb_timeout_exit, user_id, ), "_u")

        return result
