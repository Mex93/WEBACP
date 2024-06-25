from flask import json

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.templates_mask.CSQLTemplatesQuerys import CSQLTemplatesQuerys
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData

from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_SUBTYPE, LOG_OBJECT_TYPE

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def templates_delete_mask_ajax(scan_fk, model_id, model_name):
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    csql = CSQLTemplatesQuerys()
    count = 0
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:
            data = csql.is_valid_scanned_mask(scan_fk, model_id)
            if data is not False:
                if csql.delete_template(scan_fk, model_id) is True:

                    #################################
                    text = f"Пользователь ID: [{account_name}[{account_idx}]] удалил шаблон сканировки '{model_name}'[MID: {model_id}, SID: {scan_fk}]"
                    CSQLUserLogQuerys.send_log(
                        account_idx,
                        LOG_OBJECT_TYPE.LGOT_USER,
                        LOG_TYPE.LGT_SCAN_TEMPLATE,
                        LOG_SUBTYPE.LGST_DELETE,
                        text)

                    response_for_client.update({"error_text": f"Шаблон '{model_name}' успешно удалён!"})
                    response_for_client.update({"result": True})
                else:
                    response_for_client.update(
                        {"error_text": f"Ошибка удаления шаблона '{model_name}[{model_id}]'!"})
                    response_for_client.update({"result": False})
            else:
                response_for_client.update(
                    {"error_text": f"Не найдена маска сканировки для '{model_name}[{model_id}]'!"})
                response_for_client.update({"result": False})
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: templates_delete_mask_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"templates_delete_mask_ajax AJAX -> [Удаление шаблона сканировки '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: templates_delete_mask_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"templates_delete_mask_ajax AJAX -> [Удаление шаблона сканировки '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: templates_delete_mask_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"templates_delete_mask_ajax AJAX -> [Удаление шаблона сканировки '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: templates_delete_mask_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"templates_delete_mask_ajax AJAX -> [Удаление шаблона сканировки '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"templates_delete_mask_ajax AJAX -> [Удаление шаблона сканировки '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result
