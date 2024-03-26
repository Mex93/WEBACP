from flask import json

from captha_main import SIMPLE_CAPTCHA

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser
from engine.debug.CDebug import CDebug

from engine.users.enums import USER_SECTIONS_TYPE

from engine.asr.CSQLASRQuerys import CSQLASRQuerys
from engine.users.CSQLUserQuerys import CSQLUserQuerys
from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_OBJECT_TYPE, LOG_SUBTYPE
from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData
from engine.sql.sql_data import (SQL_ASR_FIELDS,
                                 SQL_TV_MODEL_INFO_FIELDS,
                                 SQL_ASSEMBLED_TV_FIELDS)

from engine.common import convert_date_from_sql_format

from engine.tv_models.CModels import CModels
from engine.asr.CASRFields import CASRFields, ASRFieldsType

cdebug = CDebug()
cdebug.debug_system_on(True)
cpages = CPages(cdebug)

cuser_access = CUserAccess()
cuser = CUser()


def asr_del_ajax(asr_name, asr_id):
    nickname = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    acc_index = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)

    cdebug.debug_print(f"asr_del_ajax AJAX -> [{acc_index},{nickname}: {asr_name}]")

    response_for_client = {
        "error_text": "",
        "result": False
    }

    if acc_index > 0 and nickname:
        line_csql = CSQLASRQuerys()
        user_csql = CSQLUserQuerys()
        try:
            result_connect = line_csql.connect_to_db(CONNECT_DB_TYPE.LINE)
            if result_connect is True:
                result = line_csql.check_asr_data(asr_name, asr_id)
                if result is not False:

                    result = result[0]

                    sql_assy_id = result.get(SQL_ASR_FIELDS.asr_fd_tv_asr_id, None)
                    sql_asr_name = result.get(SQL_ASR_FIELDS.asr_fd_tv_asr_name, None)
                    sql_mb_sn = result.get(SQL_ASR_FIELDS.asr_fd_mainboard_sn, None)
                    sql_mac = result.get(SQL_ASR_FIELDS.asr_fd_ethernet_mac, None)

                    start_next = False
                    if (sql_assy_id == asr_id) and (sql_asr_name == asr_name):

                        if sql_mb_sn or sql_mac:
                            result_assembled = line_csql.check_asr_data_in_assembled_table(sql_mb_sn, sql_mac)
                            if result_assembled:
                                result_assembled = result_assembled[0]
                                assembled_tv_sn = result_assembled.get(SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn, None)

                                response_for_client.update(
                                    {"error_text": f"MAC или SN МП из ASR: '{sql_asr_name}' найден в собранном телевизоре SN: '{assembled_tv_sn}'!"})
                                cdebug.debug_print(
                                    f"asr_del_ajax AJAX -> [{nickname}] -> [Ошибка] "
                                    f"[MAC или SN материнской платы из ASR '{sql_asr_name}' найден в собранном телевизоре SN: '{assembled_tv_sn}']]")
                            else:
                                start_next = True

                        #  ----------------------------------------------------------------------------------------
                        if start_next is True:
                            result_delete = line_csql.delete_asr(asr_id, asr_name)
                            if result_delete:
                                # print("ASR " + str(asr_id), str(asr_name))

                                #################################
                                try:
                                    log_connect = user_csql.connect_to_db(CONNECT_DB_TYPE.LOCAL)
                                    if log_connect is True:

                                        log_unit = CSQLUserLogQuerys(user_csql, acc_index)
                                        text = f"Пользователь ID: [{acc_index}] удалил ASR {asr_name} ID:{asr_id}"
                                        log_unit.add_log(
                                            LOG_OBJECT_TYPE.LGOT_USER,
                                            LOG_TYPE.LGT_ASR,
                                            LOG_SUBTYPE.LGST_DELETE,
                                            text)
                                        #################################
                                    else:
                                        response_for_client.update(
                                            {"error_text": "errorcode: asr_del_ajax -> [Log] [Нет подключения к User DB!]"})
                                        cdebug.debug_print(
                                            f"asr_del_ajax AJAX -> [{nickname}] -> [Исключение] [Нет подключения к User DB!]")

                                except Exception as err:
                                    response_for_client.update({"error_text": "errorcode: asr_del_ajax -> [Log] [Exception]"})
                                    cdebug.debug_print(
                                        f"asr_del_ajax AJAX -> [{nickname}] -> [Исключение] [Exception: '{err}']")
                                finally:
                                    user_csql.disconnect_from_db()

                                response_for_client.update({"result": True})
                                cdebug.debug_print(
                                    f"asr_del_ajax AJAX -> [{nickname}] -> [ASR успешно удалён] -> [Ответ в JS]")
                            else:
                                cdebug.debug_print(
                                    f"asr_del_ajax AJAX -> [{nickname}] -> [Ошибка] [Ошибка в процессе удаления]")
                                response_for_client.update({"error_text": "Ошибка в процессе удаления 'result_delete'"})
                else:
                    cdebug.debug_print(
                        f"asr_del_ajax AJAX -> [{nickname}] -> [Ошибка] [Указанный ASR не обнаружен]")
                    response_for_client.update({"error_text": "Указанное совпадение ASR не обнаружено"})
            else:
                raise NotConnectToDB("Not SQL Connect!")

        except NotConnectToDB as err:
            response_for_client.update({"error_text": "errorcode: asr_del_ajax -> [NotConnectToDB]"})
            cdebug.debug_print(
                f"asr_del_ajax AJAX -> [{nickname}] -> [Исключение] [NotConnectToDB: '{err}']")

        except ErrorSQLQuery as err:
            response_for_client.update({"error_text": "errorcode: asr_del_ajax -> [ErrorSQLQuery]"})
            cdebug.debug_print(
                f"asr_del_ajax AJAX -> [{nickname}] -> [Исключение] [ErrorSQLQuery: '{err}']")

        except ErrorSQLData as err:
            response_for_client.update({"error_text": "errorcode: asr_del_ajax -> [ErrorSQLData]"})
            cdebug.debug_print(
                f"asr_del_ajax AJAX -> [{nickname}] -> [Исключение] [ErrorSQLData: '{err}']")

        except Exception as err:
            response_for_client.update({"error_text": "errorcode: asr_del_ajax -> [Error Data]"})
            cdebug.debug_print(
                f"asr_del_ajax AJAX -> [{nickname}] -> [Исключение] [Alt Errors: '{err}']")
        finally:
            line_csql.disconnect_from_db()

    else:
        response_for_client.update({"error_text": "errorcode: asr_del_ajax -> [Empty Data]"})
        cdebug.debug_print(
            f"asr_del_ajax AJAX -> [{acc_index},{nickname}] -> [Ошибка] [Empty Data]")

    result = json.dumps(response_for_client)
    cdebug.debug_print(f"asr_del_ajax AJAX -> [{nickname}] -> "
                       f"[Ответ в JS] ->[{result}]")
    return result


def asr_find_ajax(asr_name):
    nickname = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    acc_index = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)

    cdebug.debug_print(f"asr_find_ajax AJAX -> [{acc_index},{nickname}: {asr_name}]")

    response_for_client = {
        "error_text": "",
        "result": False
    }

    if acc_index > 0 and nickname:
        line_csql = CSQLASRQuerys()
        user_csql = CSQLUserQuerys()
        try:
            result_connect = line_csql.connect_to_db(CONNECT_DB_TYPE.LINE)
            if result_connect is True:
                result = line_csql.get_asr_data_from_name(asr_name)
                if result is not False:

                    result = result[0]
                    asr_dict = dict()
                    index = 0

                    asr_unit = CASRFields()
                    for key, value in result.items():

                        if key == SQL_ASR_FIELDS.asr_fd_timestamp_st10:
                            if value:
                                value = convert_date_from_sql_format(str(value))

                        elif key == SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name:
                            new_name, type_name = CModels.get_parced_name_and_type(value)

                            html_label = asr_unit.get_html_field_name_from_field_type(ASRFieldsType.MODEL_TYPE_NAME)
                            if html_label is not None:
                                asr_dict.update({f"{html_label}": type_name})
                                # print(type_name)
                                value = new_name

                        new_key = asr_unit.get_html_field_name_from_sql_name(key)
                        # print(key, new_key)
                        if new_key is not None:
                            asr_dict.update({f"{new_key}": value})

                        # print(key, value)
                        index += 1

                    if index > 5:
                        #  ----------------------------------------------------------------------------------------

                        #################################
                        try:
                            log_connect = user_csql.connect_to_db(CONNECT_DB_TYPE.LOCAL)
                            if log_connect is True:

                                log_unit = CSQLUserLogQuerys(user_csql, acc_index)
                                text = f"Пользователь ID: [{acc_index}] запросил информацию ASR {asr_name}"
                                log_unit.add_log(
                                    LOG_OBJECT_TYPE.LGOT_USER,
                                    LOG_TYPE.LGT_ASR,
                                    LOG_SUBTYPE.LGST_FIND,
                                    text)
                                #################################
                            else:
                                response_for_client.update(
                                    {"error_text": "errorcode: asr_find_ajax -> [Log] [Нет подключения к User DB!]"})
                                cdebug.debug_print(
                                    f"asr_find_ajax AJAX -> [{nickname}] -> [Исключение] [Нет подключения к User DB!]")

                        except Exception as err:
                            response_for_client.update({"error_text": "errorcode: asr_find_ajax -> [Log] [Exception]"})
                            cdebug.debug_print(
                                f"asr_find_ajax AJAX -> [{nickname}] -> [Исключение] [Exception: '{err}']")
                        finally:
                            user_csql.disconnect_from_db()
                        # TODO развернуть словарь, что бы значения названия и типа были вверху
                        # JS почему то преобразует словарь в объект с конца
                        response_for_client.update({"asr_data": asr_dict})
                        assoc_tup = asr_unit.get_assoc_tuple()
                        response_for_client.update({"assoc_tup": assoc_tup})
                        response_for_client.update({"result": True})
                        cdebug.debug_print(
                            f"asr_find_ajax AJAX -> [{nickname}] -> [ASR успешно предоставлен] -> [Ответ в JS]")
                else:
                    cdebug.debug_print(
                        f"asr_find_ajax AJAX -> [{nickname}] -> [Ошибка] [Указанный ASR не обнаружен]")
                    response_for_client.update({"error_text": "Указанное совпадение ASR не обнаружено"})
            else:
                raise NotConnectToDB("Not SQL Connect!")

        except NotConnectToDB as err:
            response_for_client.update({"error_text": "errorcode: asr_find_ajax -> [NotConnectToDB]"})
            cdebug.debug_print(
                f"asr_find_ajax AJAX -> [{nickname}] -> [Исключение] [NotConnectToDB: '{err}']")

        except ErrorSQLQuery as err:
            response_for_client.update({"error_text": "errorcode: asr_find_ajax -> [ErrorSQLQuery]"})
            cdebug.debug_print(
                f"asr_find_ajax AJAX -> [{nickname}] -> [Исключение] [ErrorSQLQuery: '{err}']")

        except ErrorSQLData as err:
            response_for_client.update({"error_text": "errorcode: asr_find_ajax -> [ErrorSQLData]"})
            cdebug.debug_print(
                f"asr_find_ajax AJAX -> [{nickname}] -> [Исключение] [ErrorSQLData: '{err}']")

        except Exception as err:
            response_for_client.update({"error_text": "errorcode: asr_find_ajax -> [Error Data]"})
            cdebug.debug_print(
                f"asr_find_ajax AJAX -> [{nickname}] -> [Исключение] [Alt Errors: '{err}']")
        finally:
            line_csql.disconnect_from_db()

    else:
        response_for_client.update({"error_text": "errorcode: asr_find_ajax -> [Empty Data]"})
        cdebug.debug_print(
            f"asr_find_ajax AJAX -> [{acc_index},{nickname}] -> [Ошибка] [Empty Data]")

    new_captcha_dict = SIMPLE_CAPTCHA.create()
    response_for_client.update({"new_captha": SIMPLE_CAPTCHA.captcha_html(new_captcha_dict)})

    result = json.dumps(response_for_client)
    cdebug.debug_print(f"asr_find_ajax AJAX -> [{nickname}] -> "
                       f"[Ответ в JS] ->[{result}]")
    return result
