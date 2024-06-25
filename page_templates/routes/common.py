from flask import json

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser
from engine.common import convert_date_from_sql_format

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.templates_mask.CSQLTemplatesQuerys import CSQLTemplatesQuerys

from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData
from engine.sql.sql_data import SQL_TV_MODEL_INFO_FIELDS
from engine.tv_models.CModels import CModels

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
            if data is not False:

                result_arr = list()
                for item in data:
                    model_name = item.get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name, None)
                    model_id = item.get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id, None)
                    model_scan_fk = item.get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk, None)
                    last_update_time = item.get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_last_update_time, None)
                    if last_update_time is not None:
                        last_update_time = convert_date_from_sql_format(str(last_update_time))
                    serial_number = item.get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_serial_number_template, None)

                    if None not in (model_name, model_id, model_scan_fk, last_update_time):
                        count += 1
                        model_name, model_type_name = CModels.get_parced_name_and_type(model_name)

                        result_arr.append({
                            'model_name': model_name,
                            'model_type_name': model_type_name,
                            'model_id': model_id,
                            'model_scan_fk': model_scan_fk,
                            'last_update_time': last_update_time,
                            'serial_number': serial_number,
                        })
                    else:
                        continue
                if count:
                    response_for_client.update({"error_text": "Список моделей предоставлен"})
                    response_for_client.update({"result": True})
                    response_for_client.update({"arr": result_arr})

            else:
                response_for_client.update({"error_text": "Не найден список Моделей устройств!"})
                response_for_client.update({"result": False})
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
    cdebug.debug_print(
        f"templates_get_models_list_ajax AJAX -> [Получение списка моделей устройств] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result

