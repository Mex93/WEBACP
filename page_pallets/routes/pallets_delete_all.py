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

                result = csql.get_pallet_data_log(pallet_sn, pallet_sql_id)
                if result:
                    cdebug.debug_sql_print(f'{account_name}[{account_idx}]',
                                           'Полное удаление паллета',
                                           result)
                csql.delete_pallet(pallet_sn, pallet_sql_id)

                if csql.get_pallet_device_count(pallet_sn):

                    result = csql.get_pallet_devices_data_log(pallet_sn)
                    if result:
                        cdebug.debug_sql_print(f'{account_name}[{account_idx}]',
                                               'Полное удаление всех девайсов паллета',
                                               result)

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
