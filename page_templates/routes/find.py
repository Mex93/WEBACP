from flask import json

from engine.common import get_checkbox_state, convert_date_from_sql_format

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.templates_mask.CSQLTemplatesQuerys import CSQLTemplatesQuerys
from engine.templates_mask.CMask import CMask
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData
from engine.sql.sql_data import SQL_TV_MODEL_INFO_FIELDS
from engine.tv_models.CModels import CModels

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def templates_edit_mask_ajax(scan_fk, model_id, model_name):
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    csql = CSQLTemplatesQuerys()
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:
            data = csql.get_scanned_params(scan_fk)
            if data is not False:
                result_arr = list()
                # fields_arr = CMask.get_arr()
                params_list = list()
                count = 0
                result_dict = dict()
                for item in data:
                    #print(item)
                    find_index = CMask.get_field_arr_index(item)
                    if find_index == -1:
                        # print(f"Пропущен: {item}")
                        continue
                    sql_check = CMask.get_sql_check_label(find_index)
                    sql_template = CMask.get_sql_template_label(find_index)

                    text_id = CMask.get_text_id(find_index)
                    field_id = CMask.get_field_id(find_index)
                    text_name = CMask.get_text_name(find_index)

                    cur_value = None

                    if CMask.is_sql_field_template(find_index, sql_template):
                        cur_value = data.get(sql_template, None)
                    elif CMask.is_sql_field_check(find_index, sql_check):
                        cur_value = data.get(sql_check, None)

                    if cur_value is None:
                        continue

                    result_dict.update({field_id: cur_value})


                    params_list.append([text_id, sql_name, text_name, field_type, cur_value])
                    count += 1

                if count:
                    response_for_client.update({"error_text": "Список сканировки предоставлен"})
                    response_for_client.update({"result": True})
                    response_for_client.update({"arr": params_list})
            else:
                response_for_client.update({"error_text": f"Не найден список сканировки для '{model_name}[{model_id}]'!"})
                response_for_client.update({"result": True})
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: templates_edit_mask_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"templates_edit_mask_ajax AJAX -> [Получение списка сканировки '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: templates_edit_mask_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"templates_edit_mask_ajax AJAX -> [Получение списка сканировки '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: templates_edit_mask_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"templates_edit_mask_ajax AJAX -> [Получение списка сканировки '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: templates_edit_mask_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"templates_edit_mask_ajax AJAX -> [Получение списка сканировки '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"templates_edit_mask_ajax AJAX -> [Получение списка сканировки '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result


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
                    serial_number = item.get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_serial_number_template, None)

                    if None not in (model_name, model_id, model_scan_fk, last_update_time, serial_number):
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
    cdebug.debug_print(
        f"templates_get_models_list_ajax AJAX -> [Получение списка моделей устройств] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result
