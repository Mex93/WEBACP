from flask import json

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.sql_data import SQL_TV_MODEL_INFO_FIELDS
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData

from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_SUBTYPE, LOG_OBJECT_TYPE

from engine.devicesn.CSQLSNQuerys import CSQLSNQuerys
from engine.devicesn.CSN import CDeviceSN

from engine.common import convert_date_from_sql_format
from captha_main import SIMPLE_CAPTCHA

from engine.tv_models.CModels import CModels
from engine.devicesn.common import is_cirylic

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def get_device_sn_data(device_sn):
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
            data = csql.get_device_data(device_sn)
            if data is not False:
                result_arr = list()
                dkeys: dict = data.keys()
                count = 0
                if len(dkeys):
                    for sql_field in dkeys:
                        arr_index = CDeviceSN.get_array_index_from_sql_label(sql_field)
                        if arr_index == -1:
                            continue

                        value_type = CDeviceSN.get_value_type(arr_index)
                        current_value = data.get(sql_field, None)

                        if sql_field == SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name:
                            if current_value:
                                new_arr_index = CDeviceSN.get_array_index_from_text_id('model_type_name')
                                if new_arr_index != -1:
                                    current_value, type_name = CModels.get_parced_name_and_type(current_value)
                                    params_dict = {
                                        "text_id": CDeviceSN.get_text_id(new_arr_index),
                                        "text_name": CDeviceSN.get_text_name(new_arr_index),
                                        "is_editable": CDeviceSN.is_field_editable(new_arr_index),
                                        "current_value": type_name,
                                        "value_type": 'string'
                                    }

                                    result_arr.append(params_dict)

                        if current_value is None:
                            if value_type == str:
                                current_value = ''
                            elif value_type == int:
                                current_value = -1337
                            else:
                                current_value = ''

                        text_id = CDeviceSN.get_text_id(arr_index)
                        text_name = CDeviceSN.get_text_name(arr_index)
                        is_editable = CDeviceSN.is_field_editable(arr_index)
                        if value_type == str:
                            value_type = 'string'
                        elif value_type == int:
                            value_type = 'integer'
                        elif value_type == 'date':
                            if text_id == 'packing_data' or text_id == 'scanned_date' or text_id == 'first_scan_date':
                                current_value = convert_date_from_sql_format(str(current_value))

                            value_type = 'date'
                        else:
                            value_type = 'string'

                        params_dict = {
                            "text_id": text_id,
                            "text_name": text_name,
                            "is_editable": is_editable,
                            "current_value": current_value,
                            "value_type": value_type
                        }

                        result_arr.append(params_dict)
                        count += 1
                if count:
                    response_for_client.update({"error_text": "Список параметров предоставлен"})
                    response_for_client.update({"result": True})
                    response_for_client.update({"arr": result_arr})

                    #################################
                    text = f"Пользователь ID: [{account_name}[{account_idx}]] произвёл поиск SN устройства '{device_sn}']"
                    CSQLUserLogQuerys.send_log(
                        account_idx,
                        LOG_OBJECT_TYPE.LGOT_USER,
                        LOG_TYPE.LGT_SN,
                        LOG_SUBTYPE.LGST_FIND,
                        text)

                    cdebug.debug_print(
                        f"get_device_sn_data AJAX -> [Получение списка параметров устройства SN:] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Удачно] -> [Список предоставлен '{device_sn}'] ")
                else:
                    response_for_client.update(
                        {"error_text": f"Не найден список ключей из запроса SQL для '{device_sn}'!"})
                    cdebug.debug_print(
                        f"get_device_sn_data AJAX -> [Получение списка параметров устройства SN:] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Ошибка] -> [Не найден список ключей из запроса SQL!] -> '{device_sn}' ")

            else:
                response_for_client.update({"error_text": f"Не найдено устройство '{device_sn}'!"})
                cdebug.debug_print(
                    f"get_device_sn_data AJAX -> [Получение списка параметров устройства SN:] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Ошибка] -> [Не найдено устройство '{device_sn}'] ")
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: get_device_sn_data -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"get_device_sn_data AJAX -> [Получение списка параметров устройства SN: '{device_sn}'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: get_device_sn_data -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"get_device_sn_data AJAX -> [Получение списка параметров устройства SN: '{device_sn}'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: get_device_sn_data -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"get_device_sn_data AJAX -> [Получение списка параметров устройства SN: '{device_sn}'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: get_device_sn_data -> [Error Data]"})
        cdebug.debug_print(
            f"get_device_sn_data AJAX -> [Получение списка параметров устройства SN: '{device_sn}'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    new_captcha_dict = SIMPLE_CAPTCHA.create()
    response_for_client.update({"new_captha": SIMPLE_CAPTCHA.captcha_html(new_captcha_dict)})

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"get_device_sn_data AJAX -> [Получение списка параметров устройства SN: '{device_sn}'] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result


def set_delete_sn_ajax_ajax(device_sn: str, assy_id: int):
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
                data = csql.delete_sn(assy_id)
                if data:

                    response_for_client.update({"error_text": f"Устройство '{device_sn}' успешно удалено!"})
                    response_for_client.update({"result": True})

                    #################################
                    text = f"Пользователь ID: [{account_name}[{account_idx}]] удалил готовое устройство из базы '{device_sn}'[{assy_id}]]"
                    CSQLUserLogQuerys.send_log(
                        account_idx,
                        LOG_OBJECT_TYPE.LGOT_USER,
                        LOG_TYPE.LGT_SN,
                        LOG_SUBTYPE.LGST_DELETE,
                        text)

                    cdebug.debug_print(
                        f"set_delete_sn_ajax_ajax AJAX -> [Удаление устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Удачно] -> [Устройство успешно удалено '{device_sn}'[{assy_id}]] ")
                else:
                    response_for_client.update({"error_text": f"Не найдено устройство '{device_sn}'!"})
                    cdebug.debug_print(
                        f"set_delete_sn_ajax_ajax AJAX -> [Удаление устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Ошибка] -> [Не найдено устройство '{device_sn}'[{assy_id}]] ")
            else:
                response_for_client.update({"error_text": f"Не найдено устройство '{device_sn}'!"})
                cdebug.debug_print(
                    f"set_delete_sn_ajax_ajax AJAX -> [Удаление устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Ошибка] -> [Не найдено устройство '{device_sn}'[{assy_id}]] ")
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: set_delete_sn_ajax_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"set_delete_sn_ajax_ajax AJAX -> [Удаление устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: set_delete_sn_ajax_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"set_delete_sn_ajax_ajax AJAX -> [Удаление устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: set_delete_sn_ajax_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"set_delete_sn_ajax_ajax AJAX -> [Удаление устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: set_delete_sn_ajax_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"set_delete_sn_ajax_ajax AJAX -> [Удаление устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"set_delete_sn_ajax_ajax AJAX -> [Удаление устройства SN: '{device_sn}'[{assy_id}]] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result


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

                            index = CDeviceSN.get_array_index_from_text_id('device_sn')
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
