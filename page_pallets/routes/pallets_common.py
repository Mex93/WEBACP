from flask import json

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.sql_data import SQL_PALLET_SN_FIELDS, SQL_PALLET_SCANNED_FIELDS, SQL_ASSEMBLED_TV_FIELDS
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData

from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_SUBTYPE, LOG_OBJECT_TYPE

from engine.pallets.CSQLPalletQuerys import CSQLPalletQuerys
from engine.pallets.CPallet import CPallet
from engine.pallets.enums import INPUT_TYPE
from engine.pallets.common import MAX_DEVICES_ON_PALLET

from engine.common import convert_date_from_sql_format
from captha_main import SIMPLE_CAPTCHA

from engine.tv_models.CModels import CModels

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def get_pallet_sn_data(pallet_sn: str):
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    count = 0
    pallet_sn = pallet_sn.upper()
    # todo придумать как убрать быдлокод в вычислении паллета и его устройств, так как повтор кода
    csql = CSQLPalletQuerys()
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:

            pallet_find_sn = None
            pallet_find_sn_sql_id = 0
            pallet_create_date = None
            pallet_completed_check = None
            pallet_completed_date = None
            pallet_assembled_line = 0

            pallet_scanned_result = False
            device_count = 0
            device_list = list()
            error_find_max_count = False
            data = csql.get_pallet_data(pallet_sn)
            if data:
                pallet_find_sn = data.get(SQL_PALLET_SN_FIELDS.fd_pallet_code, None)
                pallet_find_sn_sql_id = data.get(SQL_PALLET_SN_FIELDS.fd_assy_id, None)

                pallet_create_date = data.get(SQL_PALLET_SN_FIELDS.fd_created_data, None)
                pallet_completed_check = data.get(SQL_PALLET_SN_FIELDS.fd_completed_check, None)
                pallet_completed_date = data.get(SQL_PALLET_SN_FIELDS.fd_completed_date, None)
                pallet_assembled_line = data.get(SQL_PALLET_SN_FIELDS.fd_assembled_line, None)

                if None not in (pallet_find_sn, pallet_find_sn_sql_id, pallet_completed_check):
                    pallet_scanned_result = True

                    data = csql.get_pallet_sn_from_devices(pallet_sn)
                    if data:
                        for device in data:
                            item_device_assy = device.get(SQL_PALLET_SCANNED_FIELDS.fd_assy_id, None)
                            item_device_sn = device.get(SQL_PALLET_SCANNED_FIELDS.fd_tv_sn, None)
                            item_scanned_data = device.get(SQL_PALLET_SCANNED_FIELDS.fd_scanned_data, None)
                            item_model_fk = device.get(SQL_PALLET_SCANNED_FIELDS.fd_tv_model_fk, None)

                            if None not in (item_device_assy, item_device_sn):
                                if item_scanned_data:
                                    item_scanned_data = convert_date_from_sql_format(str(item_scanned_data))

                                obj = {
                                    'device_assy': item_device_assy,
                                    'device_sn': item_device_sn,
                                    'scanned_data': item_scanned_data,
                                    'model_fk': item_model_fk
                                }

                                device_list.append(
                                    obj)
                                device_count += 1
            else:
                data_devices = csql.get_pallet_sn_from_devices_ex(pallet_sn)
                if data_devices is not False:
                    if data_devices is not None:
                        pallet_find_sn = data_devices[0].get(SQL_PALLET_SCANNED_FIELDS.fd_pallet_code, None)
                        if pallet_find_sn:
                            data = csql.get_pallet_data(pallet_find_sn)
                            if data is not False:
                                pallet_find_sn_sql_id = data.get(SQL_PALLET_SN_FIELDS.fd_assy_id, None)
                                if pallet_find_sn_sql_id:
                                    pallet_create_date = data.get(SQL_PALLET_SN_FIELDS.fd_created_data, None)
                                    pallet_completed_check = data.get(SQL_PALLET_SN_FIELDS.fd_completed_check, None)
                                    pallet_completed_date = data.get(SQL_PALLET_SN_FIELDS.fd_completed_date, None)
                                    pallet_assembled_line = data.get(SQL_PALLET_SN_FIELDS.fd_assembled_line, None)
                                    pallet_scanned_result = True

                                    data = csql.get_pallet_sn_from_devices(pallet_find_sn)
                                    if data:
                                        for device in data:
                                            item_device_assy = device.get(SQL_PALLET_SCANNED_FIELDS.fd_assy_id, None)
                                            item_device_sn = device.get(SQL_PALLET_SCANNED_FIELDS.fd_tv_sn, None)
                                            item_scanned_data = device.get(SQL_PALLET_SCANNED_FIELDS.fd_scanned_data,
                                                                           None)
                                            item_model_fk = device.get(SQL_PALLET_SCANNED_FIELDS.fd_tv_model_fk, None)
                                            if None not in (item_device_assy, item_device_sn):
                                                if item_scanned_data:
                                                    item_scanned_data = convert_date_from_sql_format(
                                                        str(item_scanned_data))
                                                obj = {
                                                    'device_assy': item_device_assy,
                                                    'device_sn': item_device_sn,
                                                    'scanned_data': item_scanned_data,
                                                    'model_fk': item_model_fk
                                                }

                                                device_list.append(
                                                    obj)
                                                device_count += 1
                    else:
                        error_find_max_count = True

            if pallet_scanned_result:
                response_for_client.update({"error_text": "Список параметров предоставлен"})
                response_for_client.update({"result": True})
                response_for_client.update({"pallet_devices": device_list})

                if pallet_create_date:
                    pallet_create_date = convert_date_from_sql_format(str(pallet_create_date))

                if pallet_completed_date:
                    pallet_completed_date = convert_date_from_sql_format(str(pallet_completed_date))

                params_list = \
                    [
                        ['pallet_sn', pallet_find_sn],
                        ['assy_id', pallet_find_sn_sql_id],
                        ['assembled_line', pallet_assembled_line],
                        ['completed_check', pallet_completed_check],
                        ['create_date', pallet_create_date],
                        ['completed_date', pallet_completed_date],

                    ]
                params_completed = []
                count = 0
                for item in params_list:
                    array_index = CPallet.get_array_index_from_text_id(item[0])
                    if array_index != -1:

                        text_id = CPallet.get_text_id(array_index)
                        text_name = CPallet.get_text_name(array_index)
                        value_type = CPallet.get_value_type(array_index)
                        input_type = CPallet.get_input_type(array_index)
                        is_editting = CPallet.is_field_editable(array_index)
                        if is_editting:
                            is_editting = 'editable'
                        else:
                            is_editting = 'no-editable'

                        if input_type == INPUT_TYPE.CHECKBOX:
                            input_type = 'cb'
                        else:
                            input_type = 'input'

                        if value_type == str:
                            value_type = 'string'
                        elif value_type == int:
                            value_type = 'integer'
                        elif value_type == bool:
                            value_type = 'bool'

                        params_completed.append([text_id, text_name, value_type, input_type, is_editting, item[1]])
                        count += 1

                if count:
                    response_for_client.update({"pallet_data": params_completed})
                    #################################
                    text = f"Пользователь ID: [{account_name}[{account_idx}]] произвёл поиск паллета '{pallet_find_sn}']"
                    CSQLUserLogQuerys.send_log(
                        account_idx,
                        LOG_OBJECT_TYPE.LGOT_USER,
                        LOG_TYPE.LGT_PALLETS,
                        LOG_SUBTYPE.LGST_FIND,
                        text)

                    cdebug.debug_print(
                        f"get_pallet_sn_data AJAX -> [Получение информации о паллете] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Удачно] -> [Список предоставлен '{pallet_find_sn}'] ")

                else:
                    response_for_client.update(
                        {"error_text": f"Ошибка получения параметров паллета!"})
                    # другими словами - устройство не может быть привязано сразу к нескольким паллетам
                    cdebug.debug_print(
                        f"get_pallet_sn_data AJAX -> [Получение информации о паллете] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Ошибка] -> [Ошибка получения параметров паллета '{pallet_sn}'] ")
            else:
                if error_find_max_count:
                    response_for_client.update(
                        {"error_text": f"С паллетом возникла ошибка! Сообщите администратору!!!!"})
                    # другими словами - устройство не может быть привязано сразу к нескольким паллетам
                    cdebug.debug_print(
                        f"get_pallet_sn_data AJAX -> [Получение информации о паллете] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Ошибка] -> [С паллетом возникла ошибка! Вернулось множество значений при определении серийника паллета в таблице сканировки устройств '{pallet_sn}'] ")
                else:
                    response_for_client.update(
                        {"error_text": f"Указанный паллет '{pallet_sn}' не найден !"})
                    # другими словами - устройство не может быть привязано сразу к нескольким паллетам
                    cdebug.debug_print(
                        f"get_pallet_sn_data AJAX -> [Получение информации о паллете] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Ошибка] -> [Паллет не найден '{pallet_sn}'] ")
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: get_pallet_sn_data -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"get_pallet_sn_data AJAX -> [Получение информации о паллете '{pallet_sn}'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: get_pallet_sn_data -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"get_pallet_sn_data AJAX -> [Получение информации о паллете '{pallet_sn}'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: get_pallet_sn_data -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"get_pallet_sn_data AJAX -> [Получение информации о паллете '{pallet_sn}'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: get_pallet_sn_data -> [Error Data]"})
        cdebug.debug_print(
            f"get_pallet_sn_data AJAX -> [Получение информации о паллете '{pallet_sn}'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    new_captcha_dict = SIMPLE_CAPTCHA.create()
    response_for_client.update({"new_captha": SIMPLE_CAPTCHA.captcha_html(new_captcha_dict)})

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"get_pallet_sn_data AJAX -> [Получение информации о паллете '{pallet_sn}'] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result


def set_pallet_delete_all_ajax(pallet_sn: str, pallet_sql_id: int):
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    count = 0

    csql = CSQLPalletQuerys()
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:
            if csql.is_pallet_valid(pallet_sn, pallet_sql_id) is not False:
                csql.delete_pallet(pallet_sn, pallet_sql_id)

                if csql.get_pallet_device_count(pallet_sn):
                    csql.delete_all_pallet_devices(pallet_sn)

                #################################
                text = f"Пользователь ID: [{account_name}[{account_idx}]] полностью удалил паллет '{pallet_sn}' [{pallet_sql_id}]]"
                CSQLUserLogQuerys.send_log(
                    account_idx,
                    LOG_OBJECT_TYPE.LGOT_USER,
                    LOG_TYPE.LGT_PALLETS,
                    LOG_SUBTYPE.LGST_DELETE,
                    text)

                response_for_client.update(
                    {"error_text": f"Указанный паллет '{pallet_sn}' успешно удалён!"})

                response_for_client.update({"result": True})
                cdebug.debug_print(
                    f"set_pallet_delete_all_ajax AJAX -> [Удаление паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Удачно] -> [Паллет успешно удалён!] ")
            else:
                response_for_client.update(
                    {"error_text": f"Указанный паллет '{pallet_sn}' не найден!"})
                cdebug.debug_print(
                    f"set_pallet_delete_all_ajax AJAX -> [Удаление паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Исключение] [Указанный паллет '{pallet_sn}' не найден!]")
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_delete_all_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"set_pallet_delete_all_ajax AJAX -> [Удаление паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_delete_all_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"set_pallet_delete_all_ajax AJAX -> [Удаление паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_delete_all_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"set_pallet_delete_all_ajax AJAX -> [Удаление паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: set_pallet_delete_all_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"set_pallet_delete_all_ajax AJAX -> [Удаление паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"set_pallet_delete_all_ajax AJAX -> [Удаление паллета '{pallet_sn} [{pallet_sql_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result


def set_pallet_add_device_ajax(pallet_sn: str, pallet_sql_id: int, devicesn: str):
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    count = 0

    csql = CSQLPalletQuerys()
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:
            pallet_line = csql.is_pallet_valid(pallet_sn, pallet_sql_id)
            if pallet_line is not False:
                result = csql.is_device_in_pallet(pallet_sn, devicesn)
                if result is not None:
                    if not result:
                        count = csql.get_pallet_device_count(pallet_sn)
                        if type(count) is int and csql.get_pallet_device_count(pallet_sn) < MAX_DEVICES_ON_PALLET:
                            device_data = csql.get_tv_info(devicesn)
                            if type(device_data) is dict:
                                complect_check_time = device_data.get(SQL_ASSEMBLED_TV_FIELDS.fd_completed_date, None)
                                if complect_check_time is not None:
                                    device_line_fk = device_data.get(SQL_ASSEMBLED_TV_FIELDS.fd_linefk, None)
                                    if device_line_fk == pallet_line:
                                        model_fk = device_data.get(SQL_ASSEMBLED_TV_FIELDS.fd_tvfk, None)
                                        if model_fk is not None:
                                            insert_result = csql.insert_scanned_tv_on_pallet(pallet_sn, devicesn, model_fk)
                                            if insert_result is not False:
                                                if isinstance(insert_result, tuple):
                                                    #################################
                                                    text = f"Пользователь ID: [{account_name}[{account_idx}]] добавил устройство '{devicesn}' к паллету '{pallet_sn}']"
                                                    CSQLUserLogQuerys.send_log(
                                                        account_idx,
                                                        LOG_OBJECT_TYPE.LGOT_USER,
                                                        LOG_TYPE.LGT_PALLETS,
                                                        LOG_SUBTYPE.LGST_ADD,
                                                        text)

                                                    response_for_client.update(
                                                        {
                                                            "error_text": f"Указанное устройство '{devicesn}' успешно добавлено к паллету '{pallet_sn}'!"})
                                                    response_for_client.update({"assyid": insert_result[0]})
                                                    response_for_client.update({"model_fk": model_fk})
                                                    response_for_client.update({"scanned_data": convert_date_from_sql_format(str(insert_result[1]))})
                                                    response_for_client.update({"result": True})
                                                    cdebug.debug_print(
                                                        f"get_pallet_sn_data AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                                                        f"[Удачно] -> [Указанное устройство '{devicesn}' успешно добавлено к паллету '{pallet_sn}'!] ")
                                        else:
                                            response_for_client.update(
                                                {
                                                    "error_text": f"Устройство '{devicesn}' вернуло ошибку по номеру модели!"})
                                            cdebug.debug_print(
                                                f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                                                f"[Ошибка] [Устройство '{devicesn}' вернуло ошибку по номеру модели!]")
                                    else:
                                        response_for_client.update(
                                            {
                                                "error_text": f"Устройство '{devicesn}' собрано на '{device_line_fk}' сборочном конвейере!"})
                                        cdebug.debug_print(
                                            f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                                            f"[Ошибка] [Устройство '{devicesn}' собрано на '{device_line_fk}' сборочном конвейере!]")
                                else:
                                    response_for_client.update(
                                        {
                                            "error_text": f"Устройство '{devicesn}' не проходило операцию упаковки на сборочном конвейере '{pallet_line}'!"})
                                    cdebug.debug_print(
                                        f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                                        f"[Ошибка] [Устройство '{devicesn}' не проходило операцию упаковки на сборочном конвейере '{pallet_line}'!]")
                            else:
                                response_for_client.update(
                                    {
                                        "error_text": f"Устройство '{devicesn}' не найдено!"})
                                cdebug.debug_print(
                                    f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                                    f"[Ошибка] [Устройство '{devicesn}' не найдено!]")
                        else:
                            response_for_client.update(
                                {
                                    "error_text": f"В выбранном паллете '{pallet_sn}' уже максимальное количество устройств!"})
                            cdebug.debug_print(
                                f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                                f"[Ошибка] [В выбранном паллете '{pallet_sn}' уже максимальное количество устройств!]")
                    else:
                        response_for_client.update(
                            {"error_text": f"В выбранном паллете '{pallet_sn}' уже есть указанный SN '{devicesn}'!"})
                        cdebug.debug_print(
                            f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                            f"[Ошибка] [В выбранном паллете '{pallet_sn}' уже есть указанный SN '{devicesn}'!]")
                else:
                    response_for_client.update({"reset_pallet": True})
                    response_for_client.update(
                        {"error_text": f"В выбранном паллете '{pallet_sn}' произошла ошибка!"})
                    cdebug.debug_print(
                        f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Ошибка] [В выбранном паллете '{pallet_sn}' произошла ошибка!!]")
            else:
                response_for_client.update({"reset_pallet": True})
                response_for_client.update(
                    {"error_text": f"Указанный паллет '{pallet_sn}' не найден!"})
                cdebug.debug_print(
                    f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Исключение] [Указанный паллет '{pallet_sn}' не найден!]")
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_add_device_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_add_device_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_add_device_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: set_pallet_add_device_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result


def set_pallet_delete_device_ajax(pallet_sn: str, pallet_sql_id: int, devicesn: str, device_assy: int):
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    count = 0

    csql = CSQLPalletQuerys()
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:
            pallet_line = csql.is_pallet_valid(pallet_sn, pallet_sql_id)
            if pallet_line is not False:
                result = csql.is_device_in_pallet_ex(pallet_sn, devicesn, device_assy)
                if result is not None:
                    if result:
                        csql.delete_device_from_pallet(devicesn, device_assy, pallet_sn)
                        #################################
                        text = f"Пользователь ID: [{account_name}[{account_idx}]] удалил устройство '{devicesn}' с паллета '{pallet_sn}']"
                        CSQLUserLogQuerys.send_log(
                            account_idx,
                            LOG_OBJECT_TYPE.LGOT_USER,
                            LOG_TYPE.LGT_PALLETS,
                            LOG_SUBTYPE.LGST_DELETE,
                            text)

                        response_for_client.update(
                            {
                                "error_text": f"Устройство '{devicesn}' успешно удалено с паллета '{pallet_sn}'!"})
                        response_for_client.update({"result": True})
                        cdebug.debug_print(
                            f"set_pallet_delete_device_ajax AJAX -> [Удаление устройства '{devicesn}' из паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                            f"[Удачно] -> [Указанное устройство '{devicesn}' успешно удалено с паллета '{pallet_sn}'!] ")
                    else:
                        response_for_client.update(
                            {"error_text": f"В выбранном паллете '{pallet_sn}' нет указанного SN '{devicesn}'!"})
                        cdebug.debug_print(
                            f"set_pallet_delete_device_ajax AJAX -> [Удаление устройства '{devicesn}' из паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                            f"[Ошибка] [В выбранном паллете '{pallet_sn}' нет указанного SN '{devicesn}'!]")
                else:
                    response_for_client.update({"reset_pallet": True})
                    response_for_client.update(
                        {"error_text": f"В выбранном паллете '{pallet_sn}' произошла ошибка!"})
                    cdebug.debug_print(
                        f"set_pallet_delete_device_ajax AJAX -> [Удаление устройства '{devicesn}' из паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Ошибка] [В выбранном паллете '{pallet_sn}' произошла ошибка!!]")
            else:
                response_for_client.update({"reset_pallet": True})
                response_for_client.update(
                    {"error_text": f"Указанный паллет '{pallet_sn}' не найден!"})
                cdebug.debug_print(
                    f"set_pallet_delete_device_ajax AJAX -> [Удаление устройства '{devicesn}' из паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Исключение] [Указанный паллет '{pallet_sn}' не найден!]")
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_delete_device_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"set_pallet_delete_device_ajax AJAX -> [Удаление устройства '{devicesn}' из паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")
    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_delete_device_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"set_pallet_delete_device_ajax AJAX -> [Удаление устройства '{devicesn}' из паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")
    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_delete_device_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"set_pallet_delete_device_ajax AJAX -> [Удаление устройства '{devicesn}' из паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")
    except Exception as err:

        response_for_client.update({"error_text": "errorcode: set_pallet_delete_device_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"set_pallet_delete_device_ajax AJAX -> [Удаление устройства '{devicesn}' из паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")
    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"set_pallet_delete_device_ajax AJAX -> [Удаление устройства '{devicesn}' из паллета '{pallet_sn} [{pallet_sql_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result


