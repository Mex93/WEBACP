from engine.users.users_log.enums import LOG_TYPE, LOG_SUBTYPE, LOG_OBJECT_TYPE
from engine.sql.sql_data import SQL_TABLE_NAME, SQL_USERS_FIELDS, SQL_LOG_FIELDS
from engine.common import get_inet_ipaddress
from engine.debug.CDebug import CDebug


class CSQLUserLogQuerys:

    def __init__(self, db_handle, user_account_index):
        self.__db_handle = db_handle
        self.__user_account_index = user_account_index

        self.__cdebug = CDebug()
        self.__cdebug.debug_system_on(True)

    def add_log(self,
                log_object_type: LOG_OBJECT_TYPE,
                log_type: LOG_TYPE,
                log_sub_type: LOG_SUBTYPE,
                text: str):
        user_id = self.__user_account_index
        if user_id > 0:
            ip = get_inet_ipaddress()
            query_string = (f"INSERT INTO {SQL_TABLE_NAME.user_logs} "
                            f"({SQL_LOG_FIELDS.lfd_log_object},"
                            f"{SQL_LOG_FIELDS.lfd_log_type},"
                            f"{SQL_LOG_FIELDS.lfd_log_sub_type},"
                            f"{SQL_LOG_FIELDS.lfd_log_user_id}, "
                            f"{SQL_LOG_FIELDS.lfd_log_text}, "
                            f"{SQL_LOG_FIELDS.lfd_log_ip}) "
                            f"VALUES "

                            f"('{log_object_type}', "
                            f"'{log_type}', "
                            f"'{log_sub_type}', "
                            f"'%s', "
                            f"'{text}', "
                            f"'{ip}' "
                            f") RETURNING  {SQL_LOG_FIELDS.lfd_log_index};")

            result = (self.__db_handle.sql_query_and_get_result
                      (self.__db_handle.get_sql_handle(), query_string, (user_id, ), "_i"))

            self.__cdebug.debug_print(
                f"CSQLUserLogQuerys -> [add_log]: [{text}]")
            return result

        return False

    def get_last_login_log(self, count: int) -> bool | tuple:
        query = (f"SELECT {SQL_LOG_FIELDS.lfd_log_ip},"
                 f"{SQL_LOG_FIELDS.lfd_log_mac},"
                 f"{SQL_LOG_FIELDS.lfd_log_date} "
                 f"FROM "
                 f"{SQL_TABLE_NAME.user_logs} "
                 f"WHERE "
                 f"{SQL_LOG_FIELDS.lfd_log_user_id} = %s AND "
                 f"{SQL_LOG_FIELDS.lfd_log_object} = {LOG_OBJECT_TYPE.LGOT_USER} AND "
                 f"({SQL_LOG_FIELDS.lfd_log_type} = {LOG_TYPE.LGT_USER_LOGIN} OR "
                 f"{SQL_LOG_FIELDS.lfd_log_sub_type} = {LOG_TYPE.LGT_USER_LOGOUT}) "
                 f"ORDER BY {SQL_LOG_FIELDS.lfd_log_index} DESC "
                 f""
                 f"LIMIT {count}")

        result = self.__db_handle.sql_query_and_get_result(
            self.__db_handle.get_sql_handle(), query, (self.__user_account_index,), "_1")

        return result
