from __init__ import app, cpages, cuser_sessions, request, csql, cuser

from engine.pages.enums import PAGE_ID
from engine.common import get_checkbox_state, convert_date_from_sql_format
from engine.pages.login import login_actions as login
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData
from engine.sql.sql_data import SQL_USERS_FIELDS
from engine.users.enums import USER_ALEVEL
name = cpages.get_page_route_name_from_page_id(PAGE_ID.LOGIN)


@app.route(f'/{name}', methods=['POST', 'GET'])
def ulogin():
    if cuser_sessions.is_sessions_start() is True:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == 'POST':
        # получаем данные от кнопок и полей
        user_name = request.form['user_name']
        user_pass = request.form['user_pass']
        user_save_me = get_checkbox_state(request.form.get('user_save_me'))

        result = login.check_login_params(user_name, user_pass, bool(user_save_me))
        if isinstance(result, tuple) and result[0] is False:
            error_text = result[1]
            return cpages.set_render_page(PAGE_ID.LOGIN, errors=error_text)
            # cpages.set_render_page(PAGE_ID.LOGIN, errors=error_text)
            # render_template("login.html", errors=error_text)

        try:
            result = csql.connect_to_db(CONNECT_DB_TYPE.LOCAL)
            if result is True:
                login_result = csql.get_login(user_name, user_pass)
                if login_result is not False:
                    query_data = login_result[1]
                    account_disabled = query_data.get(SQL_USERS_FIELDS.ufd_account_disabled, None)

                    if account_disabled is True:

                        account_disable_aindex = query_data.get(SQL_USERS_FIELDS.ufd_account_dis_aindex, None)
                        account_disable_date = query_data.get(SQL_USERS_FIELDS.ufd_account_dis_date, None)
                        admin_name = csql.get_nickname_from_user_id(account_disable_aindex)
                        cpages.set_render_page(PAGE_ID.LOGIN,
                                               errors=("Ваш аккаунт отключен администратором!",
                                                       f"Администратор: '{admin_name}'",
                                                       f"Дата отключения: {account_disable_date}"))

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
                        cuser.update_SQL_account_lastlogin(sql_user_index)

                        #  ----------------------------------------------------------------------------------------

                        #################################
                        text = f"Пользователь ID: [{sql_user_index}] авторизировался в свой аккаунт"

                        self.__cuser_log_sql.add_log(
                            WindowLogin,
                            LOG_OBJECT_TYPE.LGOT_USER,
                            LOG_TYPE.LGT_USER_LOGIN,
                            LOG_SUBTYPE.LGST_ADD,
                            text)
                        #################################

                        self.__cmainmenu.set_blocked_main_toolbars(False)
                        self.__cmainmenu.reopen_access_toolbars_for_user()
                        user.set_login_state(True)

                        self.__cmainmenu.set_insert_user_content_on_all_pages(self.__clinesql)
                        self.__cmainmenu.set_open_menu(PAGE_ID.PAGE_ACCOUNT_MAIN)
                else:
                    return cpages.set_render_page(PAGE_ID.LOGIN,
                                                  errors="Указанное совпадение логина и пароля не обнаружено")
            else:
                raise NotConnectToDB("Not SQL Connect!")
        except NotConnectToDB as err:
            print(err)
        except ErrorSQLQuery as err:
            print(err)
        except ErrorSQLData as err:
            print(err)
        finally:
            csql.disconnect_from_db()

    return cpages.set_render_page(PAGE_ID.LOGIN)
