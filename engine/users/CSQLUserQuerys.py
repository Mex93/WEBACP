from werkzeug import security

from engine.sql.CSQLAgent import CSqlAgent
from engine.sql.sql_data import SQL_TABLE_NAME, SQL_USERS_FIELDS

PROGRAM_TIME_TYPE = "0300"  # Russia


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
                        f"WHERE {SQL_USERS_FIELDS.ufd_account_dis_aindex} = %s "
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
            self.get_sql_handle(), query, (user_id, admin_level), "_u")

        return result

    def update_SQL_account_lastlogin(self, user_id: int):
        query = (f"UPDATE {SQL_TABLE_NAME.user_accounts} SET "
                 f"{SQL_USERS_FIELDS.ufd_last_login_date} = now() "
                 f"WHERE {SQL_USERS_FIELDS.ufd_index} = %s")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query, (user_id,), "_u")

        return result
