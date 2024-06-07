from flask import json

from engine.common import get_checkbox_state, convert_date_from_sql_format

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.templates.CSQLTemplatesQuerys import CSQLTemplatesQuerys
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData
from engine.sql.sql_data import SQL_LOG_FIELDS

from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def templates_get_models_list_ajax():

    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    count = 0
    csql = CSQLTemplatesQuerys()
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:
            data = csql.get_tv_list()
            if data is True:

                response_for_client.update({"error_text": "Записи найдены"})
                response_for_client.update({"result": True})
                response_for_client.update({"arr": data})

            else:
                response_for_client.update({"error_text": "Не найден список Моделей устройств!"})
                response_for_client.update({"result": True})
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: templates_get_models_list_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"templates_get_models_list_ajax AJAX -> [Получение списка моделей устройств] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: templates_get_models_list_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"templates_get_models_list_ajax AJAX -> [Получение списка моделей устройств] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: templates_get_models_list_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"templates_get_models_list_ajax AJAX -> [Получение списка моделей устройств] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: templates_get_models_list_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"templates_get_models_list_ajax AJAX -> [Получение списка моделей устройств] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(f"templates_get_models_list_ajax AJAX -> [Получение списка моделей устройств] -> [IDX:{account_idx}, {account_name}] -> "
                       f"[Ответ в JS] -> [{count}]")
    return result
