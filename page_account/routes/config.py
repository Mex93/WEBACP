from flask import json
from engine.pages.enums import PAGE_ID
from page_account.account import bp_page_account

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser
from engine.debug.CDebug import CDebug

from engine.users.enums import USER_SECTIONS_TYPE, USER_SECTION_ACCESS_TYPE

from engine.users.CSQLUserQuerys import CSQLUserQuerys
from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_OBJECT_TYPE, LOG_SUBTYPE
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData

from engine.common import get_current_unix_time
from engine.users.common import MAX_ACTIVITY_TIME_LEFT

cdebug = CDebug()
cdebug.debug_system_on(True)
cpages = CPages(cdebug)

cuser_access = CUserAccess()
cuser = CUser()


def account_config():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_CONFIG)


def urepass(old_pass, new_pass, re_pass):
    email = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    user_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)

    cdebug.debug_print(f"urepass AJAX -> [{email},{user_idx}]")

    response_for_client = {
        "error_text": "",
        "result": False
    }
    if new_pass == re_pass:
        result_login_check_fields = cuser.check_repass_params(email, old_pass, new_pass, re_pass)
        if result_login_check_fields is True:  # success
            cdebug.debug_print(f"urepass AJAX -> [{email}] -> "
                               f"[Проверка введённых данных пройдена успешно. Начинаю замену пароля в БД]")
            csql = CSQLUserQuerys()
            try:
                result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LOCAL)
                if result_connect is True:
                    login_result = csql.get_repass(user_idx, old_pass, new_pass)
                    if login_result[0] is not False:
                        update_pass_result = csql.update_SQL_account_password(user_idx, new_pass)
                        if update_pass_result is not False:
                            #################################
                            log_unit = CSQLUserLogQuerys(csql, user_idx)
                            text = f"Пользователь ID: [{user_idx}] сменил пароль от своего аккаунта"
                            log_unit.add_log(
                                LOG_OBJECT_TYPE.LGOT_USER,
                                LOG_TYPE.LGT_USER_ACCOUNT,
                                LOG_SUBTYPE.LGST_UPDATE,
                                text)
                            #################################
                            response_for_client.update({"result": True})
                            cdebug.debug_print(
                                f"urepass AJAX -> [{email}] -> [Аккаунт успешно сменил пароль] -> [Ответ в JS]")
                    else:
                        response_for_client.update({"error_text": f"{login_result[1]}"})
                        cdebug.debug_print(
                            f"urepass AJAX -> [{email}] -> [Ошибка] -> [{login_result[1]}]")
                else:
                    raise NotConnectToDB("Not SQL Connect!")

            except NotConnectToDB as err:
                response_for_client.update({"error_text": "errorcode: check_login_params -> [NotConnectToDB]"})
                cdebug.debug_print(
                    f"urepass AJAX -> [{email}] -> [Исключение] [NotConnectToDB: '{err}']")

            except ErrorSQLQuery as err:
                response_for_client.update({"error_text": "errorcode: check_login_params -> [ErrorSQLQuery]"})
                cdebug.debug_print(
                    f"urepass AJAX -> [{email}] -> [Исключение] [ErrorSQLQuery: '{err}']")

            except ErrorSQLData as err:
                response_for_client.update({"error_text": "errorcode: check_login_params -> [ErrorSQLData]"})
                cdebug.debug_print(
                    f"urepass AJAX -> [{email}] -> [Исключение] [ErrorSQLData: '{err}']")
            finally:
                csql.disconnect_from_db()

        else:
            if len(result_login_check_fields) > 0:
                response_for_client.update({"error_text": result_login_check_fields})
                response_for_client.update({"result": False})
                cdebug.debug_print(f"urepass AJAX -> [{email}] -> "
                                   f"[Проверка введённых данных не пройдена] ->[{result_login_check_fields}]")
    else:
        cdebug.debug_print(
            f"urepass AJAX -> [{email}] -> [Ошибка сверки данных] -> Новый пароль и повтор не совпали")

        response_for_client.update(
            {"error_text": "Новый пароль и повтор не совпали"})

    result = json.dumps(response_for_client)
    cdebug.debug_print(f"urepass AJAX -> [{email}] -> "
                       f"[Ответ в JS] ->[{result}]")
    return result


def ucb_settings(cb_timeout):
    email = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    user_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)

    cdebug.debug_print(f"ucb_settings AJAX -> [{email},{user_idx}]")

    response_for_client = {
        "error_text": "",
        "result": False
    }

    cdebug.debug_print(f"ucb_settings AJAX -> [{email}] -> "
                       f"[Проверки на настройки чекбоксов не обнаружены] -> [Начинаю сохранение данных в аккаунт]")
    csql = CSQLUserQuerys()
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LOCAL)
        if result_connect is True:
            account_found = csql.get_nickname_from_user_id(user_idx)
            if account_found is not False:

                cb_dict = {
                    USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT: cb_timeout
                }
                update_settings_result = csql.update_SQL_account_checkboxes(user_idx, cb_dict)
                if update_settings_result is not False:

                    cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT_TIME, get_current_unix_time() +
                                                 MAX_ACTIVITY_TIME_LEFT)

                    #################################
                    log_unit = CSQLUserLogQuerys(csql, user_idx)
                    text = f"Пользователь ID: [{user_idx}] обновил настройки аккаунта (чекбоксы)"
                    log_unit.add_log(
                        LOG_OBJECT_TYPE.LGOT_USER,
                        LOG_TYPE.LGT_USER_ACCOUNT,
                        LOG_SUBTYPE.LGST_UPDATE,
                        text)
                    #################################
                    response_for_client.update({"result": True})
                    cdebug.debug_print(
                        f"ucb_settings AJAX -> [{email}] -> [Аккаунт успешно обновил настройки аккаунта (чекбоксы)] -> "
                        f"[Ответ в JS]")
                    cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT, cb_timeout)
                else:
                    response_for_client.update({"error_text": "Не найдено одно из полей настроек в объекте 'cb_dict'"})
                    cdebug.debug_print(
                        f"ucb_settings AJAX -> [{email}] -> "
                        f"[Ошибка] -> [Не найдено одно из полей настроек в объекте 'cb_dict']")
            else:
                response_for_client.update({"error_text": "Аккаунт не найден в БД"})
                cdebug.debug_print(
                    f"ucb_settings AJAX -> [{email}] -> [Ошибка] [Аккаунт не найден в БД!]")
        else:
            raise NotConnectToDB("Not SQL Connect!")

    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: check_login_params -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"ucb_settings AJAX -> [{email}] -> [Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: check_login_params -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"ucb_settings AJAX -> [{email}] -> [Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: check_login_params -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"ucb_settings AJAX -> [{email}] -> [Исключение] [ErrorSQLData: '{err}']")
    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(f"ucb_settings AJAX -> [{email}] -> "
                       f"[Ответ в JS] ->[{result}]")
    return result
