from werkzeug import security
from flask import request

from engine.sql.CSQL import csql_eng, ErrorSQLData, ErrorSQLQuery, NotConnectToDB
import engine.sql.enums as cenum
from engine.sql.config import db_standart_connect_params, db_assembly_connect_params
from engine.sql.sql_data import SQL_TABLE_NAME, SQL_USERS_FIELDS
# from engine_scripts.py.sql.sql_data import

PROGRAM_TIME_TYPE = "0300"  # Russia


class SqlAgent_Main(csql_eng):
    def __init__(self):
        super().__init__()

        self.__connect_handle = False
        self.__sql_object = None

        self.__sql_data_line = db_assembly_connect_params
        self.__sql_data_local = db_standart_connect_params
        self.__sql_time = PROGRAM_TIME_TYPE

    def get_sql_handle(self):
        return self.__connect_handle

    def connect_to_db(self, connect_db_type: cenum.CONNECT_DB_TYPE) -> bool:
        if self.__connect_handle is False:

            if connect_db_type == cenum.CONNECT_DB_TYPE.LINE:
                self.set_connect_data(self.__sql_data_line)
            if connect_db_type == cenum.CONNECT_DB_TYPE.LOCAL:
                self.set_connect_data(self.__sql_data_local)
            else:
                raise ErrorSQLData("Error SQL | db changed connect type!")
            if self.is_valid_saved_connect_data() is False:  # Saved in config data is NOT correct
                raise ErrorSQLData("Error SQL | incomming connections data!")

            connect_handle = self.sql_connect(self.__sql_time)
            if connect_handle is False:  # Connecting not successful
                raise NotConnectToDB("Error SQL | db not connect!")

            self.__connect_handle = connect_handle
            self.__sql_object = self
            return True

        return False

    def disconnect_from_db(self) -> bool:
        if self.__connect_handle is not False:
            self.__sql_object.sql_disconnect()
            self.__connect_handle = False
            self.__sql_object = None
            return True
        return False

    def get_login(self, nickname: str, password: str):
        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.user_accounts} "
                        f"WHERE {SQL_USERS_FIELDS.ufd_nickname} = %s "
                        f"LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (nickname, ), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_pass = result[0].get(SQL_USERS_FIELDS.ufd_md5pass, None)
        if sql_pass is not None:
            # print(security.generate_password_hash(password))
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
            self.get_sql_handle(), query_string, (uid, ), "_1", )  # Запрос типа аасоциативного массива
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
            self.get_sql_handle(), query, (user_id, ), "_u")

        return result

    def add_log(self,
                incomming_window,
                log_object_type: LOG_OBJECT_TYPE,
                log_type: LOG_TYPE,
                log_sub_type: LOG_SUBTYPE,
                text: str):
        user_id = self.__cuser.get_account_index()
        if user_id > 0:
            mac = self.get_current_mac()
            ip = self.get_inet_ipaddress()
            query_string = (f"INSERT INTO {SQL_TABLE_NAME.user_logs} "
                            f"({SQL_LOG_FIELDS.lfd_log_object},"
                            f"{SQL_LOG_FIELDS.lfd_log_type},"
                            f"{SQL_LOG_FIELDS.lfd_log_sub_type},"
                            f"{SQL_LOG_FIELDS.lfd_log_user_id}, "
                            f"{SQL_LOG_FIELDS.lfd_log_text}, "
                            f"{SQL_LOG_FIELDS.lfd_log_ip}, "
                            f"{SQL_LOG_FIELDS.lfd_log_mac}) "
                            f"VALUES "

                            f"('{log_object_type}', "
                            f"'{log_type}', "
                            f"'{log_sub_type}', "
                            f"{user_id}, "
                            f"'{text}', "
                            f"'{ip}', "
                            f"'{mac}') RETURNING  {SQL_LOG_FIELDS.lfd_log_index};")

            result = (self.__sql_object.sql_query_and_get_result
                      (self.__sql_object.get_main_sql_handle(), query_string, "_i"))

            # self.__cdbug.debug_print(f"Log Query: '{query_string}'")
            self.__cdbug.debug_print(f"Log ['{incomming_window}']: '{text}'")
            return result

        return False

    @staticmethod
    def get_inet_ipaddress():
        return request.remote_addr

    def get_last_login_log(self, count: int, aindex: int) -> bool | tuple:
        query = (f"SELECT {SQL_LOG_FIELDS.lfd_log_ip},"
                 f"{SQL_LOG_FIELDS.lfd_log_mac},"
                 f"{SQL_LOG_FIELDS.lfd_log_date} "
                 f"FROM "
                 f"{SQL_TABLE_NAME.user_logs} "
                 f"WHERE "
                 f"{SQL_LOG_FIELDS.lfd_log_user_id} = {aindex} AND "
                 f"{SQL_LOG_FIELDS.lfd_log_object} = {LOG_OBJECT_TYPE.LGOT_USER} AND "
                 f"({SQL_LOG_FIELDS.lfd_log_type} = {LOG_TYPE.LGT_USER_LOGIN} OR "
                 f"{SQL_LOG_FIELDS.lfd_log_sub_type} = {LOG_TYPE.LGT_USER_LOGOUT}) "
                 f"ORDER BY {SQL_LOG_FIELDS.lfd_log_index} DESC "
                 f""
                 f"LIMIT {count}")

        result = self.__sql_object.sql_query_and_get_result(
            self.__sql_object.get_main_sql_handle(), query, "_1")

        return result
