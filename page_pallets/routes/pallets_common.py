from flask import json

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.sql_data import SQL_PALLET_SN_FIELDS, SQL_PALLET_SCANNED_FIELDS
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData

from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_SUBTYPE, LOG_OBJECT_TYPE

from engine.pallets.CSQLPalletQuerys import CSQLPalletQuerys
from engine.pallets.CPallet import CPallet

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
                            print(device)
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
                                            print(device)
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

                response_for_client.update({"pallet_data":
                    {
                        'pallet_sn': pallet_find_sn,
                        'assy_id': pallet_find_sn_sql_id,
                        'create_date': pallet_create_date,
                        'completed_check': pallet_completed_check,
                        'completed_date': pallet_completed_date,
                        'assembled_line': pallet_assembled_line
                    }
                })

                #################################
                text = f"Пользователь ID: [{account_name}[{account_idx}]] произвёл поиск паллета '{pallet_find_sn}']"
                # CSQLUserLogQuerys.send_log(
                #     account_idx,
                #     LOG_OBJECT_TYPE.LGOT_USER,
                #     LOG_TYPE.LGT_PALLETS,
                #     LOG_SUBTYPE.LGST_FIND,
                #     text)

                cdebug.debug_print(
                    f"get_pallet_sn_data AJAX -> [Получение информации о паллете] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Удачно] -> [Список предоставлен '{pallet_find_sn}'] ")
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
