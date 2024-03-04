from flask import json

from engine.common import get_checkbox_state, convert_date_from_sql_format

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.users.CSQLUserQuerys import CSQLUserQuerys
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData
from engine.sql.sql_data import SQL_LOG_FIELDS

from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def account_logs_ajax():

    response_for_client = {
        "error_text": "",
        "result": False
    }
    count = 0
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)

    if account_idx:

        csql = CSQLUserQuerys()
        try:
            result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LOCAL)
            if result_connect is True:
                log_unit = CSQLUserLogQuerys(csql, account_idx)
                query_data = log_unit.get_last_login_log(30)
                if len(query_data) > 0:

                    logs = list()
                    for log_field in query_data:
                        date = str(log_field.get(SQL_LOG_FIELDS.lfd_log_date, None))
                        if date is not None:
                            date = convert_date_from_sql_format(date)

                        ip = log_field.get(SQL_LOG_FIELDS.lfd_log_ip, None)
                        tindex = log_field.get(SQL_LOG_FIELDS.lfd_log_index, None)

                        obj = (tindex, date, ip)
                        logs.append(obj)
                        count += 1

                    response_for_client.update({"error_text": "Записи найдены"})
                    response_for_client.update({"result": True})
                    response_for_client.update({"logs": logs})

                else:
                    response_for_client.update({"error_text": "Последние записи активности не найдены"})
                    response_for_client.update({"result": True})
            else:
                raise NotConnectToDB("Not SQL Connect!")
        except NotConnectToDB as err:
            response_for_client.update({"error_text": "errorcode: account_main -> [NotConnectToDB]"})
            cdebug.debug_print(
                f"account_main AJAX -> [Получение логов] -> [IDX:{account_idx}, {account_name}] -> "
                f"[Исключение] [NotConnectToDB: '{err}']")

        except ErrorSQLQuery as err:
            response_for_client.update({"error_text": "errorcode: account_main -> [ErrorSQLQuery]"})
            cdebug.debug_print(
                f"account_main AJAX -> [Получение логов] -> [IDX:{account_idx}, {account_name}] -> "
                f"[Исключение] [ErrorSQLQuery: '{err}']")

        except ErrorSQLData as err:
            response_for_client.update({"error_text": "errorcode: account_main -> [ErrorSQLData]"})
            cdebug.debug_print(
                f"account_main AJAX -> [Получение логов] -> [IDX:{account_idx}, {account_name}] -> "
                f"[Исключение] [ErrorSQLData: '{err}']")

        except Exception as err:

            response_for_client.update({"error_text": "errorcode: account_main -> [Error Data]"})
            cdebug.debug_print(
                f"account_main AJAX -> [Получение логов] -> [IDX:{account_idx}, {account_name}] -> "
                f"[Исключение] [Error Data: '{err}']")

        finally:
            csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(f"account_main AJAX -> [Получение логов] -> [IDX:{account_idx}, {account_name}] -> "
                       f"[Ответ в JS] -> [{count}]")
    return result
