from __init__ import app
from flask import url_for

from engine.users.enums import USER_SECTIONS_TYPE
from engine.common import get_current_unix_time
from engine.users.common import MAX_ACTIVITY_TIME_LEFT
from engine.users.CSQLUserQuerys import CSQLUserQuerys
from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_OBJECT_TYPE, LOG_SUBTYPE
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData

from engine.users.CUserAccess import CUserAccess
from engine.debug.CDebug import CDebug
from engine.pages.CPages import CPages
from engine.pages.enums import PAGE_ID

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
        timeout_check = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT)
        if timeout_check is True:
            current_unix_time = get_current_unix_time()
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
                            text = f"Пользователь ID: [{user_idx}] выкинут системой из аккаунта из за TimeOut]"
                            log_unit.add_log(
                                LOG_OBJECT_TYPE.LGOT_SYSTEM,
                                LOG_TYPE.LGT_USER_LOGOUT,
                                LOG_SUBTYPE.LGST_DELETE,
                                text)
                            #################################
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
                        cuser_access.delete_all_user_sessions()
                        return cpages.redirect_on_page(PAGE_ID.LOGIN)
                else:
                    cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT_TIME, current_unix_time +
                                                 MAX_ACTIVITY_TIME_LEFT)

# @app.errorhandler(404)
# def page_not_found(error_str):
#
#     return cpages.set_render_page(PAGE_ID.PAGE_NOT_FOUND)
