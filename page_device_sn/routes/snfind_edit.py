from flask import json

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData

from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_SUBTYPE, LOG_OBJECT_TYPE

from engine.devicesn.CSQLSNQuerys import CSQLSNQuerys
from engine.devicesn.CSN import CDeviceSN

from engine.devicesn.common import is_cirylic

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def set_save_edit_sn_ajax(device_sn: str, assy_id: int, arr: list):
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    count = 0

    csql = CSQLSNQuerys()
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:
            data = csql.is_devicesn_valid(device_sn, assy_id)
            if data is not False:
                if len(arr):
                    count = 0
                    vars_for_update_sql_labels = list()
                    vars_for_update_values = list()
                    errors_field = list()
                    success_fields = list()
                    for item in arr:
                        text_id, _, current_value, _, var_type = item

                        arr_index = CDeviceSN.get_array_index_from_text_id(text_id)
                        if arr_index == -1:
                            continue

                        text_name = CDeviceSN.get_text_name(arr_index)

                        if isinstance(current_value, str):
                            if is_cirylic(current_value):
                                errors_field.append(text_name)
                                continue

                        text_var_type = CDeviceSN.get_value_type(arr_index)
                        if var_type == 'string' and text_var_type == str:
                            if isinstance(current_value, str):
                                pass
                            else:
                                errors_field.append(text_name)
                                continue
                        elif var_type == 'integer' and text_var_type == int:
                            if isinstance(current_value, int):
                                pass
                            else:
                                errors_field.append(text_name)
                                continue

                        else:  # даты не доступны для редактирования!!!!
                            errors_field.append(text_name)
                            continue

                        sql_label = CDeviceSN.get_sql_label(arr_index)
                        if not sql_label:
                            errors_field.append(text_name)
                            continue

                        vars_for_update_sql_labels.append(sql_label)
                        vars_for_update_values.append(current_value)
                        success_fields.append(text_name)
                        count += 1

                    if count == len(arr):
                        handle = csql.get_sql_handle()

                        if csql.update_device_values(device_sn,
                                                     assy_id,
                                                     vars_for_update_sql_labels,
                                                     vars_for_update_values):

                            handle.commit()

                            response_for_client.update({"error_text": f"Устройство '{device_sn}' успешно изменено!"})
                            response_for_client.update({"result": True})

                            for find_text_id in ('device_sn', 'model_id'):

                                index = CDeviceSN.get_array_index_from_text_id(find_text_id)
                                if index != -1:
                                    sql_find = CDeviceSN.get_sql_label(index)
                                    for item in vars_for_update_sql_labels:
                                        if item == sql_find:
                                            response_for_client.update({"reload_block": True})
                                            break

                            vars_for_update_values = map(lambda x: str(x), vars_for_update_values)

                            #################################
                            text = (f"Пользователь ID: [{account_name}[{account_idx}]] изменил значение полей"
                                    f"({','.join(success_fields)}) -> ({','.join(vars_for_update_values)}) готового изделия '{device_sn}'[{assy_id}]")
                            CSQLUserLogQuerys.send_log(
                                account_idx,
                                LOG_OBJECT_TYPE.LGOT_USER,
                                LOG_TYPE.LGT_SN,
                                LOG_SUBTYPE.LGST_UPDATE,
                                text)

                            cdebug.debug_print(
                                f"set_save_edit_sn_ajax AJAX -> [Изменение полей готового устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                                f"[Удачно] -> [Поля: '{','.join(success_fields)}] успешно изменены!] ")
                        else:
                            handle.rollback()

                            response_for_client.update(
                                {"error_text": f"Ошибка обработчика SQL!"})
                    else:
                        if len(errors_field):
                            response_for_client.update(
                                {"error_text": f"Найдены ошибки в полях: [{','.join(errors_field)}]!"})
                        else:
                            response_for_client.update(
                                {"error_text": f"Найдены ошибки в заполняемых полях!"})
            else:
                response_for_client.update({"error_text": f"Не найдено устройство '{device_sn}'!"})
                cdebug.debug_print(
                    f"set_save_edit_sn_ajax AJAX -> [Изменение полей готового устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Ошибка] -> [Не найдено устройство '{device_sn}'[{assy_id}]] ")
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: set_save_edit_sn_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"set_save_edit_sn_ajax AJAX -> [Изменение полей готового устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: set_save_edit_sn_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"set_save_edit_sn_ajax AJAX -> [Изменение полей готового устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: set_save_edit_sn_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"set_save_edit_sn_ajax AJAX -> [Изменение полей готового устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: set_save_edit_sn_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"set_save_edit_sn_ajax AJAX -> [Изменение полей готового устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"set_save_edit_sn_ajax AJAX -> [Изменение полей готового устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result
