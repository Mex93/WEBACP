from flask import request, flash, render_template
import json
from __init__ import csrf

from engine.pages.enums import PAGE_ID
from engine.common import get_checkbox_state, convert_date_from_sql_format
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData
from engine.sql.sql_data import SQL_USERS_FIELDS
from engine.users.enums import USER_ALEVEL

from engine.sql.QuerysLibs.CSQLUserQuerys import CSQLUserQuerys

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.debug.CDebug import CDebug
from engine.users.CUser import CUser

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def ulogin():
    if cuser_access.is_sessions_start() is True:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    password = request.args['cpassword']
    email = request.args['cnickname']
    savemy = request.args['csavemy']

    print(password, email, savemy)

    response_for_client = {
        "error_text": "",
        "result": False
    }

    result_login_check_fields = cuser.check_login_params(email, password)
    if result_login_check_fields is True:  # success
        savemy = get_checkbox_state(request.form.get('csavemy'))

        csql = CSQLUserQuerys()
        try:
            result = csql.connect_to_db(CONNECT_DB_TYPE.LOCAL)
            if result is True:
                login_result = csql.get_login(email, password)
                if login_result is not False:
                    query_data = login_result[1]
                    print(query_data)
                    account_disabled = query_data.get(SQL_USERS_FIELDS.ufd_account_disabled, None)

                    if account_disabled is True:

                        account_disable_aindex = query_data.get(SQL_USERS_FIELDS.ufd_account_dis_aindex, None)
                        account_disable_date = query_data.get(SQL_USERS_FIELDS.ufd_account_dis_date, None)
                        admin_name = csql.get_nickname_from_user_id(account_disable_aindex)

                        response_for_client.update({"error_text": (
                                                            "Ваш аккаунт отключен администратором!",
                                                         f"Администратор: '{admin_name}'",
                                                         f"Дата отключения: {account_disable_date}")})
                    else:

                        # alevel
                        sql_user_index = query_data.get(SQL_USERS_FIELDS.ufd_index, None)

                        alevel = query_data.get(SQL_USERS_FIELDS.ufd_admin_level, None)
                        if cuser.check_alevel_for_user(alevel) is not True:
                            alevel = USER_ALEVEL.ULEVEL_NONE
                            csql.update_SQL_account_alevel(alevel, sql_user_index)

                        # blocked
                        account_disable_aindex = query_data.get(SQL_USERS_FIELDS.ufd_account_dis_aindex, None)
                        account_disable_date = query_data.get(SQL_USERS_FIELDS.ufd_account_dis_date, None)

                        # main

                        nickname = query_data.get(SQL_USERS_FIELDS.ufd_nickname, None)
                        firstname = query_data.get(SQL_USERS_FIELDS.ufd_firtname, None)
                        lastname = query_data.get(SQL_USERS_FIELDS.ufd_lastname, None)
                        last_login_date = str(query_data.get(SQL_USERS_FIELDS.ufd_last_login_date, None))
                        last_login_date = convert_date_from_sql_format(last_login_date)
                        # user.set_last_login_current_time(last_login_date)

                        user_timeout_exit = query_data.get(SQL_USERS_FIELDS.ufd_account_timeout_exit, None)

                        # accessssssss evil suka

                        access_config_serial_edit = query_data.get(SQL_USERS_FIELDS.ufd_user_access_sn_edit, None)
                        #
                        access_config_serial_del = query_data.get(SQL_USERS_FIELDS.ufd_user_access_sn_delete, None)
                        #
                        access_config_serial_add = query_data.get(SQL_USERS_FIELDS.ufd_user_access_sn_add, None)
                        #  ----------------------------------------------------------------------------------------
                        access_config_scan_add = query_data.get(SQL_USERS_FIELDS.ufd_user_access_scan_add, None)
                        #
                        access_config_scan_delete = query_data.get(SQL_USERS_FIELDS.ufd_user_access_scan_delete, None)
                        #
                        access_config_scan_edit = query_data.get(SQL_USERS_FIELDS.ufd_user_access_scan_edit, None)
                        #  ----------------------------------------------------------------------------------------
                        access_config_asr_delete = query_data.get(SQL_USERS_FIELDS.ufd_user_access_asr_delete, None)
                        #
                        access_config_asr_edit = query_data.get(SQL_USERS_FIELDS.ufd_user_access_asr_edit, None)
                        #
                        access_config_asr_add = query_data.get(SQL_USERS_FIELDS.ufd_user_access_asr_add, None)
                        #  ----------------------------------------------------------------------------------------
                        # last login
                        # cuser.update_SQL_account_lastlogin(sql_user_index)

                        #  ----------------------------------------------------------------------------------------

                        #################################
                        text = f"Пользователь ID: [{sql_user_index}] авторизировался в свой аккаунт"

                        # self.__cuser_log_sql.add_log(
                        #     WindowLogin,
                        #     LOG_OBJECT_TYPE.LGOT_USER,
                        #     LOG_TYPE.LGT_USER_LOGIN,
                        #     LOG_SUBTYPE.LGST_ADD,
                        #     text)
                        #################################
                        response_for_client.update({"result": True})
                else:
                    response_for_client.update({"error_text": "Указанное совпадение логина и пароля не обнаружено"})
            else:
                raise NotConnectToDB("Not SQL Connect!")
        except NotConnectToDB as err:
            print(err)
            response_for_client.update({"error_text": "errorcode: check_login_params -> [NotConnectToDB]"})

        except ErrorSQLQuery as err:
            print(err)
            response_for_client.update({"error_text": "errorcode: check_login_params -> [ErrorSQLQuery]"})

        except ErrorSQLData as err:
            print(err)
            response_for_client.update({"error_text": "errorcode: check_login_params -> [ErrorSQLData]"})

        finally:
            csql.disconnect_from_db()
    else:
        if len(result_login_check_fields) > 0:
            response_for_client.update({"error_text": result_login_check_fields})
            response_for_client.update({"result": False})

    result = json.dumps(response_for_client)
    return result
