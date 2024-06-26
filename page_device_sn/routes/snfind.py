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

from engine.common import convert_date_from_sql_format
from captha_main import SIMPLE_CAPTCHA

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
                dkeys = data.keys()
                count = 0
                if len(dkeys):
                    for sql_field in dkeys:
                        arr_index = CDeviceSN.get_array_index_from_sql_label(sql_field)
                        if arr_index == -1:
                            continue

                        value_type = CDeviceSN.get_value_type(arr_index)
                        current_value = data.get(sql_field, None)
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

                        result_arr.append([text_id, text_name, is_editable, current_value, value_type])
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
