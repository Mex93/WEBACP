from flask import url_for, request

from __init__ import app

from engine.users.enums import USER_SECTIONS_TYPE
from engine.common import get_current_unix_time
from engine.users.common import MAX_ACTIVITY_TIME_LEFT, MAX_CHECK_PERMISSIONS_TIME_LEFT
from engine.users.CSQLUserQuerys import CSQLUserQuerys
from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_OBJECT_TYPE, LOG_SUBTYPE
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData
from engine.sql.sql_data import SQL_TABLE_NAME, SQL_USERS_FIELDS

from engine.users.CUserAccess import CUserAccess
from engine.debug.CDebug import CDebug
from engine.pages.CPages import CPages
from engine.pages.enums import PAGE_ID
from engine.users.common import MAX_USER_SESSION_LIFE_TIME

cdebug = CDebug()
cpages = CPages(cdebug)

cuser_access = CUserAccess()


@app.route('/logo.ico')
def favicon():
    return url_for('static', filename='/img/logo.ico')


@app.route('/config_db.png')
def conf_db_png():
    return url_for('static', filename='/img/config_db.png')


@app.before_request
def check_user():
    if cuser_access.is_sessions_start() is True:

        current_unix_time = get_current_unix_time()
        # глушилка флудами запросов
        # чекер уходящих запросов юзеру, что бы по 10 запровос за п=раз не делать в before request
        # потому что декоратор вызывает функцию для КАЖДОГО запроса, даже на нахождение favicon
        anti_session_flood = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACCOUNT_CHECK_SESSIONS)
        if isinstance(anti_session_flood, int):
            if anti_session_flood < current_unix_time:
                anti_session_flood = current_unix_time + 2
                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_CHECK_SESSIONS, anti_session_flood)
                # print("чекер времени")

                email = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
                user_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
                # Жизнь времени сессии юзера в 1 час примерно
                session_save_me_time = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACCOUNT_SAVE_ME_START_TIME)
                if isinstance(session_save_me_time, int) is False:
                    session_save_me_time = current_unix_time + MAX_USER_SESSION_LIFE_TIME
                    cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_SAVE_ME_START_TIME,
                                                 session_save_me_time)

                if session_save_me_time != 0:
                    if session_save_me_time < current_unix_time:

                        cdebug.debug_print(
                            f"check_user -> [{email}:{user_idx}] -> [Сессии удалены] -> "
                            f"[Юзер не выбрал пункт 'Сохранить меня'. "
                            f"Время жизни сессии {MAX_USER_SESSION_LIFE_TIME/60} минут]")

                        cuser_access.delete_all_user_sessions()
                        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)
                    else:
                        cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_SAVE_ME_START_TIME,
                                                     current_unix_time +
                                                     MAX_USER_SESSION_LIFE_TIME)

                # Проверка на наличие аккаунта и совпадение ников. Так же блокировка
                account_check_time = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACCOUNT_CHECKER_ACC_FIND_TIME)
                if account_check_time:
                    if account_check_time < current_unix_time:

                        cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_CHECKER_ACC_FIND_TIME,
                                                     get_current_unix_time() +
                                                     MAX_CHECK_PERMISSIONS_TIME_LEFT)

                        csql = CSQLUserQuerys()
                        try:
                            result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LOCAL)
                            if result_connect is True:

                                result = csql.check_account_from_user_id(user_idx)
                                account_nickname = result.get(SQL_USERS_FIELDS.ufd_nickname, None)
                                if result is not False and account_nickname == email:
                                    account_disabled = result.get(SQL_USERS_FIELDS.ufd_account_disabled, None)

                                    if account_disabled is True:
                                        #################################
                                        log_unit = CSQLUserLogQuerys(csql, user_idx)
                                        text = (f"Пользователь ID: [{user_idx}] выкинут системой из "
                                                f"аккаунта из за блокировки аккаунта")
                                        log_unit.add_log(
                                            LOG_OBJECT_TYPE.LGOT_SYSTEM,
                                            LOG_TYPE.LGT_USER_LOGOUT,
                                            LOG_SUBTYPE.LGST_DELETE,
                                            text)
                                        #################################
                                        cdebug.debug_print(
                                            f"check_user -> [{email}:{user_idx}] -> [Выкинут из аккаунта] -> "
                                            f"[Аккаунт заблокирован]")

                                        cuser_access.delete_all_user_sessions()
                                        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

                                else:
                                    cdebug.debug_print(
                                        f"check_user -> [{email}:{user_idx}] -> [Выкинут из аккаунта] -> [Аккаунт не найден]")

                                    #################################
                                    log_unit = CSQLUserLogQuerys(csql, user_idx)
                                    text = (f"Пользователь ID: [{user_idx}] выкинут системой из аккаунта, "
                                            f"так как аккаунт не найден")
                                    log_unit.add_log(
                                        LOG_OBJECT_TYPE.LGOT_SYSTEM,
                                        LOG_TYPE.LGT_USER_LOGOUT,
                                        LOG_SUBTYPE.LGST_DELETE,
                                        text)
                                    #################################

                                    cuser_access.delete_all_user_sessions()
                                    return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

                        except NotConnectToDB as err:
                            cdebug.debug_print(
                                f"check_user -> [{email}:{user_idx}] -> [Исключение] [NotConnectToDB: '{err}']")

                        except ErrorSQLQuery as err:
                            cdebug.debug_print(
                                f"check_user -> [{email}:{user_idx}] -> [Исключение] [ErrorSQLQuery: '{err}']")

                        except ErrorSQLData as err:
                            cdebug.debug_print(
                                f"check_user -> [{email}:{user_idx}] -> [Исключение] [ErrorSQLData: '{err}']")
                        finally:
                            csql.disconnect_from_db()

                #  Проверка на опцию таймаута из за долгого бездействия
                timeout_check = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT)
                if timeout_check is True:

                    old_time = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT_TIME)
                    if isinstance(old_time, int):
                        if old_time == 0:
                            cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT_TIME, current_unix_time +
                                                         MAX_ACTIVITY_TIME_LEFT)
                        elif old_time < current_unix_time:
                            email = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
                            user_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
                            cdebug.debug_print(f"check_user -> [{email}:{user_idx}] -> "
                                               f"[Выкинут системой из аккаунта из за TimeOut]")

                            csql = CSQLUserQuerys()
                            try:
                                result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LOCAL)
                                if result_connect is True:
                                    #################################
                                    log_unit = CSQLUserLogQuerys(csql, user_idx)
                                    text = f"Пользователь ID: [{user_idx}] выкинут системой из аккаунта из за TimeOut"
                                    log_unit.add_log(
                                        LOG_OBJECT_TYPE.LGOT_SYSTEM,
                                        LOG_TYPE.LGT_USER_LOGOUT,
                                        LOG_SUBTYPE.LGST_DELETE,
                                        text)
                                    #################################

                                    cuser_access.delete_all_user_sessions()

                            except NotConnectToDB as err:
                                cdebug.debug_print(
                                    f"check_user -> [{email}:{user_idx}] -> [Исключение] [NotConnectToDB: '{err}']")

                            except ErrorSQLQuery as err:
                                cdebug.debug_print(
                                    f"check_user -> [{email}:{user_idx}] -> [Исключение] [ErrorSQLQuery: '{err}']")

                            except ErrorSQLData as err:
                                cdebug.debug_print(
                                    f"check_user -> [{email}:{user_idx}] -> [Исключение] [ErrorSQLData: '{err}']")
                            finally:
                                csql.disconnect_from_db()
                                return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)
                        else:
                            cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT_TIME, current_unix_time +
                                                         MAX_ACTIVITY_TIME_LEFT)

# @app.errorhandler(404)
# def page_not_found(error_str):
#
#     return cpages.set_render_page(PAGE_ID.PAGE_NOT_FOUND)
