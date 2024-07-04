from flask import json

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

from engine.common import get_current_unix_time
from engine.users.common import MAX_ACTIVITY_TIME_LEFT, MAX_CHECK_PERMISSIONS_TIME_LEFT, MAX_USER_SESSION_LIFE_TIME

from captha_main import SIMPLE_CAPTCHA

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
                        account_disable_date = str(query_data.get(SQL_USERS_FIELDS.ufd_account_dis_date, None))
                        account_disable_date = convert_date_from_sql_format(account_disable_date)
                        admin_name = csql.get_nickname_from_user_id(account_disable_aindex)

                        response_for_client.update({"error_text": (
                            f"Ваш аккаунт отключен администратором!\n"
                            f"Администратор: '{admin_name}'\n"
                            f"Дата отключения: {account_disable_date}\n")})
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
                            if account_disable_aindex is not None and account_disable_date is not None:
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_DIS_AINDEX,
                                                             account_disable_aindex)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_DIS_DATE, account_disable_date)
                            # main

                            nickname = query_data.get(SQL_USERS_FIELDS.ufd_nickname, None)
                            firstname = query_data.get(SQL_USERS_FIELDS.ufd_firtname, None)
                            lastname = query_data.get(SQL_USERS_FIELDS.ufd_lastname, None)
                            if nickname is not None and firstname is not None and lastname is not None:
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.NICKNAME,
                                                             nickname)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.FIRSTNAME,
                                                             firstname)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.LASTNAME,
                                                             lastname)
                                cdebug.debug_print(
                                    f"ulogin AJAX -> [{email}] -> [Получение основной информации аккаунта] -> "
                                    f"[ID:{sql_user_index} {nickname}, {firstname}, {lastname}]")

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
                            #
                            access_config_serial_find = query_data.get(SQL_USERS_FIELDS.ufd_user_access_sn_find, None)

                            if None not in (access_config_serial_edit,
                                            access_config_serial_del,
                                            access_config_serial_find,
                                            access_config_serial_add):
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SN_EDIT,
                                                             access_config_serial_edit)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SN_DELETE,
                                                             access_config_serial_del)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SN_ADD,
                                                             access_config_serial_add)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SN_FIND,
                                                             access_config_serial_find)
                                cdebug.debug_print(
                                    f"ulogin AJAX -> [{email}] -> [Получение прав доступа аккаунта] -> [SN]"
                                    f"[{access_config_serial_edit}, "
                                    f"{access_config_serial_del}, "
                                    f"{access_config_serial_find}, "
                                    f"{access_config_serial_add}]")

                            #  ----------------------------------------------------------------------------------------
                            access_config_scan_add = query_data.get(SQL_USERS_FIELDS.ufd_user_access_scan_add, None)
                            #
                            access_config_scan_delete = query_data.get(SQL_USERS_FIELDS.ufd_user_access_scan_delete, None)
                            #
                            access_config_scan_edit = query_data.get(SQL_USERS_FIELDS.ufd_user_access_scan_edit, None)
                            #
                            access_config_scan_find = query_data.get(SQL_USERS_FIELDS.ufd_user_access_scan_find, None)

                            if None not in (access_config_scan_add,
                                            access_config_scan_delete,
                                            access_config_scan_edit,
                                            access_config_scan_find):
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SCAN_ADD,
                                                             access_config_scan_add)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SCAN_DELETE,
                                                             access_config_scan_delete)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SCAN_EDIT,
                                                             access_config_scan_edit)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_SCAN_FIND,
                                                             access_config_scan_find)

                                cdebug.debug_print(
                                    f"ulogin AJAX -> [{email}] -> [Получение прав доступа аккаунта] -> [TEMPLATE]"
                                    f"[{access_config_scan_add}, "
                                    f"{access_config_scan_delete}, "
                                    f"{access_config_scan_find}, "
                                    f"{access_config_scan_edit}]")

                            #  ----------------------------------------------------------------------------------------
                            access_config_asr_delete = query_data.get(SQL_USERS_FIELDS.ufd_user_access_asr_delete, None)
                            #
                            access_config_asr_edit = query_data.get(SQL_USERS_FIELDS.ufd_user_access_asr_edit, None)
                            #
                            access_config_asr_add = query_data.get(SQL_USERS_FIELDS.ufd_user_access_asr_add, None)
                            #
                            access_config_asr_find = query_data.get(SQL_USERS_FIELDS.ufd_user_access_asr_find, None)

                            if None not in (access_config_asr_delete,
                                            access_config_asr_edit,
                                            access_config_asr_add,
                                            access_config_asr_find):
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_ASR_DELETE,
                                                             access_config_asr_delete)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_ASR_EDIT,
                                                             access_config_asr_edit)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_ASR_ADD,
                                                             access_config_asr_add)
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_ASR_FIND,
                                                             access_config_asr_find)
                                cdebug.debug_print(
                                    f"ulogin AJAX -> [{email}] -> [Получение прав доступа аккаунта] -> [ASR]"
                                    f"[{access_config_asr_delete}, "
                                    f"{access_config_asr_edit}, "
                                    f"{access_config_asr_find}, "
                                    f"{access_config_asr_add}]")

                                #  ----------------------------------------------------------------------------------------
                                access_config_pallet_delete = query_data.get(SQL_USERS_FIELDS.
                                                                             ufd_user_access_pallet_delete, None)
                                #
                                access_config_pallet_edit = query_data.get(SQL_USERS_FIELDS.
                                                                           ufd_user_access_pallet_edit, None)
                                #
                                access_config_pallet_add_tv = query_data.get(SQL_USERS_FIELDS.
                                                                             ufd_user_access_pallet_add_tv, None)
                                #
                                access_config_pallet_find = query_data.get(SQL_USERS_FIELDS.
                                                                           ufd_user_access_pallet_find, None)

                                if None not in (access_config_pallet_delete,
                                                access_config_pallet_edit,
                                                access_config_pallet_add_tv,
                                                access_config_pallet_find):
                                    cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_PALLET_DELETE,
                                                                 access_config_pallet_delete)
                                    cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_PALLET_EDIT,
                                                                 access_config_pallet_edit)
                                    cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_PALLET_ADD_TV,
                                                                 access_config_pallet_add_tv)
                                    cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCESS_PALLET_FIND,
                                                                 access_config_pallet_find)
                                    cdebug.debug_print(
                                        f"ulogin AJAX -> [{email}] -> [Получение прав доступа аккаунта] -> [PALLETS]"
                                        f"[{access_config_pallet_delete}, "
                                        f"{access_config_pallet_edit}, "
                                        f"{access_config_pallet_add_tv}, "
                                        f"{access_config_pallet_find}]")

                            #  ----------------------------------------------------------------------------------------
                            # last login
                            csql.update_SQL_account_lastlogin(sql_user_index)

                            #  ----------------------------------------------------------------------------------------

                            #################################
                            log_unit = CSQLUserLogQuerys(csql, sql_user_index)
                            text = f"Пользователь ID: [{email}[{sql_user_index}]] авторизировался в свой аккаунт"
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
                            unix_time = get_current_unix_time()
                            # Чекер таймаута в настройках
                            cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_TIMEOUT_EXIT_TIME,
                                                         unix_time +
                                                         MAX_ACTIVITY_TIME_LEFT)
                            # Чекер валидности аккаунта
                            cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_CHECKER_ACC_FIND_TIME,
                                                         unix_time +
                                                         MAX_CHECK_PERMISSIONS_TIME_LEFT)
                            # saveme start time session
                            if savemy is False:  # save me не выбрано, установка времени жизни сессии в 1 час
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_SAVE_ME_START_TIME,
                                                             unix_time +
                                                             MAX_USER_SESSION_LIFE_TIME)
                            else:  # установлено - запоминаем
                                cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_SAVE_ME_START_TIME,
                                                             0)

                            # чекер уходящих запросов юзеру, что бы по 10 запровос за п=раз не делать в before request
                            # потому что декоратор вызывает функцию для КАЖДОГО запроса, даже на нахождение favicon
                            cuser_access.set_session_var(USER_SECTIONS_TYPE.ACCOUNT_CHECK_SESSIONS,
                                                         unix_time +
                                                         2)

                        else:
                            cdebug.debug_print(
                                f"ulogin AJAX -> [{email}] -> [Получение данных аккаунта] -> Не найден ID пользователя")

                            response_for_client.update(
                                {"error_text": "Не найден ID пользователя"})
                else:
                    cdebug.debug_print(
                        f"ulogin AJAX -> [{email}] -> [Ошибка] [Указанное совпадение логина и пароля не обнаружено]")
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
                f"ulogin AJAX -> [{email}] -> [Исключение] [Error Data: '{err}']")
        finally:
            csql.disconnect_from_db()
    else:
        if len(result_login_check_fields) > 0:
            response_for_client.update({"error_text": "Ошибка авторизации. Возможно ошибка в Email или пароле!"})
            response_for_client.update({"result": False})
            cdebug.debug_print(f"ulogin AJAX -> [{email}] -> "
                               f"[Проверка введённых данных не пройдена] ->[{result_login_check_fields}]")

    new_captcha_dict = SIMPLE_CAPTCHA.create()
    response_for_client.update({"new_captha": SIMPLE_CAPTCHA.captcha_html(new_captcha_dict)})

    result = json.dumps(response_for_client)
    cdebug.debug_print(f"ulogin AJAX -> [{email}] -> "
                       f"[Ответ в JS] ->[{result}]")
    return result
