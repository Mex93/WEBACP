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

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()

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
                device_data = csql.get_device_data_log(device_sn)
                data = csql.delete_sn(assy_id)
                if data:
                    response_for_client.update({"error_text": f"Устройство '{device_sn}' успешно удалено!"})
                    response_for_client.update({"result": True})

                    if device_data:
                        cdebug.debug_sql_print(f'{account_name}[{account_idx}]', 'Удаление SN устройства', device_data)

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
