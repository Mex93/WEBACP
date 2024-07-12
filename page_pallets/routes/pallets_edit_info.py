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
from engine.pallets.CPallet import CPallet

from engine.common import convert_date_from_sql_format, get_current_data_stamp

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def set_pallet_save_info_ajax(pallet_sn, pallet_sql_id, text_id, new_value, old_value):
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    count = 0

    csql = CSQLPalletQuerys()
    try:
        find_arr_index = CPallet.get_array_index_from_text_id(text_id)
        if (
                find_arr_index != -1 and
                new_value != old_value and
                CPallet.is_field_editable(find_arr_index)):

            value_type = CPallet.get_value_type(find_arr_index)

            new_value = value_type(new_value)  # не ошибка!!! value_type хранит ссылку на функцию str, int итд

            if type(new_value) is value_type:
                result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
                if result_connect is True:
                    pallet_line = csql.is_pallet_valid(pallet_sn, pallet_sql_id)
                    if pallet_line is not False:
                        # input_type = CPallet.get_input_type(find_arr_index)

                        sql_label = CPallet.get_sql_label(find_arr_index)
                        text_name = CPallet.get_text_name(find_arr_index)
                        csql.update_pallet_info(pallet_sn, pallet_sql_id, sql_label, new_value)

                        if text_id == 'completed_check':
                            csql.set_completed_status(pallet_sn, pallet_sql_id)
                            response_for_client.update({"reload_completed_date": convert_date_from_sql_format(get_current_data_stamp())})

                        result_log = csql.get_pallet_data_log(pallet_sn, pallet_sql_id)
                        if result_log:
                            cdebug.debug_sql_print(f'{account_name}[{account_idx}]',
                                                   'Запрос инфы паллета при изменение данных',
                                                   result_log)

                        #################################
                        text = f"Пользователь ID: [{account_name}[{account_idx}]] изменил свойство '{text_name}' паллета '{pallet_sn}' на '{old_value} -> {new_value}']"
                        CSQLUserLogQuerys.send_log(
                            account_idx,
                            LOG_OBJECT_TYPE.LGOT_USER,
                            LOG_TYPE.LGT_PALLETS,
                            LOG_SUBTYPE.LGST_UPDATE,
                            text)

                        response_for_client.update(
                            {
                                "error_text": f"Свойство успешно изменено!"})
                        response_for_client.update({"result": True})
                        cdebug.debug_print(
                            f"set_pallet_delete_device_ajax AJAX -> [Сохранение параметров паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                            f"[Удачно] -> [Свойство успешно изменено. '{text_name}' на '{old_value} -> {new_value}'] ")
                        # input_type = CPallet.get_input_type(find_arr_index)
                    else:
                        response_for_client.update({"reset_pallet": True})
                        response_for_client.update(
                            {"error_text": f"Указанный паллет '{pallet_sn}' не найден!"})
                        cdebug.debug_print(
                            f"set_pallet_save_info_ajax AJAX -> [Сохранение параметров паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                            f"[Ошибка] [Паллет '{pallet_sn}' не найден!]")
                else:
                    raise NotConnectToDB("Not SQL Connect!")
            else:
                response_for_client.update({"reset_pallet": True})
                response_for_client.update(
                    {"error_text": f"Выбранное поле(2) паллета '{pallet_sn}' нельзя редактировать!"})
                cdebug.debug_print(
                    f"set_pallet_save_info_ajax AJAX -> [Сохранение параметров паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Ошибка] [Выбранное поле паллета '{pallet_sn}' нельзя редактировать!]")

        else:
            response_for_client.update({"reset_pallet": True})
            response_for_client.update(
                {"error_text": f"Выбранное поле(1) паллета '{pallet_sn}' нельзя редактировать!"})
            cdebug.debug_print(
                f"set_pallet_save_info_ajax AJAX -> [Сохранение параметров паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
                f"[Ошибка] [Выбранное поле паллета '{pallet_sn}' нельзя редактировать!]")

    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_save_info_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"set_pallet_save_info_ajax AJAX -> [Сохранение параметров паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_save_info_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"set_pallet_save_info_ajax AJAX -> [Сохранение параметров паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: set_pallet_save_info_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"set_pallet_save_info_ajax AJAX -> [Сохранение параметров паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: set_pallet_save_info_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"set_pallet_save_info_ajax AJAX -> [Сохранение параметров паллета '{pallet_sn} [{pallet_sql_id}]] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"set_pallet_save_info_ajax AJAX -> [Сохранение параметров паллета '{pallet_sn} [{pallet_sql_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result
