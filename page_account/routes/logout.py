
from engine.pages.enums import PAGE_ID

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE, USER_SECTION_ACCESS_TYPE

from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData

from engine.users.CSQLUserQuerys import CSQLUserQuerys
from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_OBJECT_TYPE, LOG_SUBTYPE

cdebug = CDebug()
cdebug.debug_system_on(True)
cpages = CPages(cdebug)

cuser_access = CUserAccess()
cuser = CUser()

cdebug = CDebug()
cdebug.debug_system_on(True)

def logout():
    email = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    user_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)

    cdebug.debug_print(f"logout -> [{email}:{user_idx}] -> [Вышел из своего аккаунта]")

    csql = CSQLUserQuerys()
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LOCAL)
        if result_connect is True:
            #################################
            log_unit = CSQLUserLogQuerys(csql, user_idx)
            text = f"Пользователь ID: [{user_idx}] вышел из своего аккаунта"
            log_unit.add_log(
                LOG_OBJECT_TYPE.LGOT_USER,
                LOG_TYPE.LGT_USER_LOGOUT,
                LOG_SUBTYPE.LGST_DELETE,
                text)
            #################################
    except NotConnectToDB as err:
        cdebug.debug_print(
            f"logout -> [{email}:{user_idx}] -> [Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        cdebug.debug_print(
            f"logout -> [{email}:{user_idx}] -> [Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        cdebug.debug_print(
            f"logout -> [{email}:{user_idx}] -> [Исключение] [ErrorSQLData: '{err}']")
    finally:
        csql.disconnect_from_db()
        cuser_access.delete_all_user_sessions()
        return cpages.redirect_on_page(PAGE_ID.LOGIN)
