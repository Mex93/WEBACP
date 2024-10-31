from flask import json

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.sql_data import SQL_ASSEMBLED_TV_FIELDS
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData

from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_SUBTYPE, LOG_OBJECT_TYPE

from engine.pallets.CSQLPalletQuerys import CSQLPalletQuerys
from engine.pallets.common import MAX_DEVICES_ON_PALLET

from engine.common import convert_date_from_sql_format

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


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
                                            is_pallet_any_device_sn = csql.get_pallet_id_from_tv_sn(devicesn)
                                            if is_pallet_any_device_sn is False:
                                                insert_result = csql.insert_scanned_tv_on_pallet(pallet_sn, devicesn,
                                                                                                 model_fk)
                                                if insert_result is not False:
                                                    if isinstance(insert_result, tuple):

                                                        result = csql.get_pallet_devices_data_log(pallet_sn)
                                                        if result:
                                                            cdebug.debug_sql_print(f'{account_name}[{account_idx}]',
                                                                                   'Запрос списка девайсов паллета после добавления нового устройства',
                                                                                   result)

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
                                                        response_for_client.update({
                                                                                       "scanned_data": convert_date_from_sql_format(
                                                                                           str(insert_result[1]))})
                                                        response_for_client.update({"result": True})
                                                        cdebug.debug_print(
                                                            f"get_pallet_sn_data AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                                                            f"[Удачно] -> [Указанное устройство '{devicesn}' успешно добавлено к паллету '{pallet_sn}'!] ")
                                            else:
                                                response_for_client.update(
                                                    {
                                                        "error_text": f"Устройство '{devicesn}' уже числится за паллетом '{is_pallet_any_device_sn}' !"})
                                                cdebug.debug_print(
                                                    f"set_pallet_add_device_ajax AJAX -> [Привязка устройства '{devicesn}' к паллету '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                                                    f"[Ошибка] [Устройство '{devicesn}' уже числится за паллетом '{is_pallet_any_device_sn}' !]")
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
