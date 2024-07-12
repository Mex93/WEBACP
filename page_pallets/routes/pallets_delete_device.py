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

from engine.pallets.CSQLPalletQuerys import CSQLPalletQuerys

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


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

                        result_log = csql.get_pallet_devices_data_log(pallet_sn)
                        if result:
                            cdebug.debug_sql_print(f'{account_name}[{account_idx}]',
                                                   'Запрос списка девайсов перед удалением устройства паллета',
                                                   result_log)

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
