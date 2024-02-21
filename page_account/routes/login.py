from flask import request, json

from engine.pages.enums import PAGE_ID
from engine.common import get_checkbox_state, convert_date_from_sql_format
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData
from engine.sql.sql_data import SQL_USERS_FIELDS
from engine.users.enums import USER_ALEVEL

from engine.users.CSQLUserQuerys import CSQLUserQuerys
from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_OBJECT_TYPE, LOG_SUBTYPE

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.enums import USER_SECTIONS_TYPE
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def ulogin(password, email, savemy):
    if cuser_access.is_sessions_start() is True:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    cdebug.debug_print(f"ulogin AJAX -> [{password},{email},{savemy}]")

    response_for_client = {
        "error_text": "",
        "result": False
    }

    result_login_check_fields = cuser.check_login_params(email, password)
    if result_login_check_fields is True:  # success
        savemy = get_checkbox_state(request.form.get('csavemy'))
        cdebug.debug_print(f"ulogin AJAX -> [{email}] -> "
                           f"[Проверка введённых данных пройдена успешно. Начинаю подгрузку из БД]")
        csql = CSQLUserQuerys()
        try:
            result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LOCAL)
            if result_connect is True:
                login_result = csql.get_login(email, password)
                if login_result is not False:
                    query_data = login_result[1][0]
                    cdebug.debug_print(
                        f"ulogin AJAX -> [{email}] -> [Найдено совпадение логина и пароля аккаунта. Начинаю загрузку]")
                    cdebug.debug_print(
                        f"ulogin AJAX -> [{email}] -> [{query_data}]")

                    account_disabled = query_data.get(SQL_USERS_FIELDS.ufd_account_disabled, None)

                    if account_disabled is True:

                        account_disable_aindex = query_data.get(SQL_USERS_FIELDS.ufd_account_dis_aindex, None)
                        account_disable_date = query_data.get(SQL_USERS_FIELDS.ufd_account_dis_date, None)
                        admin_name = csql.get_nickname_from_user_id(account_disable_aindex)

                        response_for_client.update({"error_text": (
                            "Ваш аккаунт отключен администратором!",
                            f"Администратор: '{admin_name}'",
                            f"Дата отключения: {account_disable_date}")})
                        cdebug.debug_print(
                            f"ulogin AJAX -> [{email}] -> [Аккаунт заблокирован [{admin_name} {account_disable_date}]")
                    else:
                        cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_DISABLED, account_disabled)

                        cdebug.debug_print(
                            f"ulogin AJAX -> [{email}] -> [Получение данных аккаунта]")
                        # alevel
                        sql_user_index = query_data.get(SQL_USERS_FIELDS.ufd_index, None)
                        if sql_user_index is not None:

                            cuser_access.set_session_var(USER_SECTIONS_TYPE.ACC_INDEX, sql_user_index)

                            alevel = query_data.get(SQL_USERS_FIELDS.ufd_admin_level, None)
                            if alevel is not None:
                                if cuser.check_alevel_for_user(alevel) is not True:
                                    alevel = USER_ALEVEL.ULEVEL_NONE
                                    csql.update_SQL_account_alevel(alevel, sql_user_index)

                            cuser_access.set_session_var(USER_SECTIONS_TYPE.ALEVEL, alevel)

                            # blocked
                            account_disable_aindex = query_data.get(SQL_USERS_FIELDS.ufd_account_dis_aindex, None)
                            account_disable_date = query_data.get(SQL_USERS_FIELDS.ufd_account_dis_date, None)
                            if account_disable_aindex and account_disable_date is not None:
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_DIS_AINDEX,
                                                             account_disable_aindex)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_DIS_DATE, account_disable_date)
                            # main

                            nickname = query_data.get(SQL_USERS_FIELDS.ufd_nickname, None)
                            firstname = query_data.get(SQL_USERS_FIELDS.ufd_firtname, None)
                            lastname = query_data.get(SQL_USERS_FIELDS.ufd_lastname, None)
                            if nickname and firstname and lastname is not None:
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.NICKNAME,
                                                             nickname)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.FIRSTNAME,
                                                             firstname)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.LASTNAME,
                                                             lastname)

                            last_login_date = str(query_data.get(SQL_USERS_FIELDS.ufd_last_login_date, None))
                            last_login_date = convert_date_from_sql_format(last_login_date)
                            if last_login_date is not None:
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.LAST_LOGIN_DATE,
                                                             last_login_date)
                            # user.set_last_login_current_time(last_login_date)

                            user_timeout_exit = query_data.get(SQL_USERS_FIELDS.ufd_account_timeout_exit, None)
                            if user_timeout_exit is not None:
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT,
                                                             user_timeout_exit)
                            # accessssssss evil suka

                            access_config_serial_edit = query_data.get(SQL_USERS_FIELDS.ufd_user_access_sn_edit, None)
                            #
                            access_config_serial_del = query_data.get(SQL_USERS_FIELDS.ufd_user_access_sn_delete, None)
                            #
                            access_config_serial_add = query_data.get(SQL_USERS_FIELDS.ufd_user_access_sn_add, None)

                            if (access_config_serial_edit
                                    and access_config_serial_del
                                    and access_config_serial_add
                                    is not None):
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SN_EDIT,
                                                             access_config_serial_edit)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SN_DELETE,
                                                             access_config_serial_del)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SN_ADD,
                                                             access_config_serial_add)

                            #  ----------------------------------------------------------------------------------------
                            access_config_scan_add = query_data.get(SQL_USERS_FIELDS.ufd_user_access_scan_add, None)
                            #
                            access_config_scan_delete = query_data.get(SQL_USERS_FIELDS.ufd_user_access_scan_delete,
                                                                       None)
                            #
                            access_config_scan_edit = query_data.get(SQL_USERS_FIELDS.ufd_user_access_scan_edit, None)

                            if (access_config_scan_add
                                    and access_config_scan_delete
                                    and access_config_scan_edit
                                    is not None):
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SCAN_ADD,
                                                             access_config_scan_add)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SCAN_DELETE,
                                                             access_config_scan_delete)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SCAN_EDIT,
                                                             access_config_scan_edit)

                            #  ----------------------------------------------------------------------------------------
                            access_config_asr_delete = query_data.get(SQL_USERS_FIELDS.ufd_user_access_asr_delete, None)
                            #
                            access_config_asr_edit = query_data.get(SQL_USERS_FIELDS.ufd_user_access_asr_edit, None)
                            #
                            access_config_asr_add = query_data.get(SQL_USERS_FIELDS.ufd_user_access_asr_add, None)

                            if (access_config_asr_delete
                                    and access_config_asr_edit
                                    and access_config_asr_add
                                    is not None):
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_ASR_DELETE,
                                                             access_config_asr_delete)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_ASR_EDIT,
                                                             access_config_asr_edit)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_ASR_ADD,
                                                             access_config_asr_add)

                            #  ----------------------------------------------------------------------------------------
                            # last login
                            csql.update_SQL_account_lastlogin(sql_user_index)

                            #  ----------------------------------------------------------------------------------------

                            #################################
                            log_unit = CSQLUserLogQuerys(csql, sql_user_index)
                            text = f"Пользователь ID: [{sql_user_index}] авторизировался в свой аккаунт"
                            log_unit.add_log(
                                LOG_OBJECT_TYPE.LGOT_USER,
                                LOG_TYPE.LGT_USER_LOGIN,
                                LOG_SUBTYPE.LGST_ADD,
                                text)
                            #################################
                            response_for_client.update({"result": True})
                            cdebug.debug_print(
                                f"ulogin AJAX -> [{email}] -> [Аккаунт успешно загружен] -> [Ответ в JS]")

                            cuser_access.sessions_start()

                        else:
                            cdebug.debug_print(
                                f"ulogin AJAX -> [{email}] -> [Получение данных аккаунта] -> Не найден ID пользователя")

                            response_for_client.update(
                                {"error_text": "Не найден ID пользователя"})
                else:
                    response_for_client.update({"error_text": "Указанное совпадение логина и пароля не обнаружено"})
            else:
                raise NotConnectToDB("Not SQL Connect!")
        except NotConnectToDB as err:
            response_for_client.update({"error_text": "errorcode: check_login_params -> [NotConnectToDB]"})
            cdebug.debug_print(
                f"ulogin AJAX -> [{email}] -> [Исключение] [NotConnectToDB: '{err}']")

        except ErrorSQLQuery as err:
            response_for_client.update({"error_text": "errorcode: check_login_params -> [ErrorSQLQuery]"})
            cdebug.debug_print(
                f"ulogin AJAX -> [{email}] -> [Исключение] [ErrorSQLQuery: '{err}']")

        except ErrorSQLData as err:
            response_for_client.update({"error_text": "errorcode: check_login_params -> [ErrorSQLData]"})
            cdebug.debug_print(
                f"ulogin AJAX -> [{email}] -> [Исключение] [ErrorSQLData: '{err}']")
        finally:
            csql.disconnect_from_db()
    else:
        if len(result_login_check_fields) > 0:
            response_for_client.update({"error_text": result_login_check_fields})
            response_for_client.update({"result": False})
            cdebug.debug_print(f"ulogin AJAX -> [{email}] -> "
                               f"[Проверка введённых данных не пройдена] ->[{result_login_check_fields}]")

    result = json.dumps(response_for_client)
    cdebug.debug_print(f"ulogin AJAX -> [{email}] -> "
                       f"[Ответ в JS] ->[{result}]")
    return result
