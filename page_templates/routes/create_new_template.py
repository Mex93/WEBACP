from flask import json

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.templates_mask.CSQLTemplatesQuerys import CSQLTemplatesQuerys
from engine.templates_mask.CMask import CMask
from engine.templates_mask.common import is_cirylic
from engine.templates_mask.enums import TableType

from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData
from engine.sql.sql_data import SQL_TV_MODEL_INFO_FIELDS, SQL_MASK_FIELDS

from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_SUBTYPE, LOG_OBJECT_TYPE

from engine.tv_models.CModels import CModels
from engine.tv_models.enums import MODELS_TYPE

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def templates_create_mask_get_elements_ajax():
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    count = 0
    csql = CSQLTemplatesQuerys()
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:

            arr_len = CMask.get_len()
            arr_results = list()
            count = 0
            for i in range(0, arr_len):
                cvalue = CMask.get_sql_template_label(i)
                cstate = CMask.get_sql_check_label(i)
                # print(cvalue, cstate)
                # если не заданы значения из бд (на всякий случай)

                text_id = CMask.get_text_id(i)
                field_id = CMask.get_field_id(i)
                text_name = CMask.get_text_name(i)
                requared_once = CMask.get_requared_field(i)

                arr_results.append([text_id, field_id, text_name, cvalue, cstate, requared_once])
                count += 1

            if count:
                response_for_client.update({"error_text": "Список параметров для создания модели предоставлен"})
                response_for_client.update({"result": True})
                response_for_client.update({"arr": arr_results})

                cdebug.debug_print(
                    f"templates_create_mask_get_elements_ajax AJAX -> [Получение списка параметров создания модели] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Успешно] [Список параметров для создания модели предоставлен]")

            else:
                response_for_client.update({"error_text": "Не найден список параметров для создания модели!"})
                cdebug.debug_print(
                    f"templates_create_mask_get_elements_ajax AJAX -> [Получение списка параметров создания модели] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Ошибка] [Не найден список параметров для создания модели!]")
        else:
            raise NotConnectToDB("Not SQL Connect!")

    except NotConnectToDB as err:
        response_for_client.update(
            {"error_text": "errorcode: templates_create_mask_get_elements_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"templates_create_mask_get_elements_ajax AJAX -> [Получение списка параметров создания модели] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update(
            {"error_text": "errorcode: templates_create_mask_get_elements_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"templates_create_mask_get_elements_ajax AJAX -> [Получение списка параметров создания модели] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update(
            {"error_text": "errorcode: templates_create_mask_get_elements_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"templates_create_mask_get_elements_ajax AJAX -> [Получение списка параметров создания модели] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: templates_create_mask_get_elements_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"templates_create_mask_get_elements_ajax AJAX -> [Получение списка параметров создания модели] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"templates_create_mask_get_elements_ajax AJAX -> [Получение списка параметров создания модели] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result


def templates_create_mask_set_add_ajax(create_parameters: list):
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    count = 0
    csql = CSQLTemplatesQuerys()
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:

            result_s = True
            is_field_requared_list = list()
            table_models_list = list()
            table_scans_list = list()
            count = 0
            model_name = None
            vendor_code = None

            for item in create_parameters:
                text_id, text_name, state_check, current_value = item

                if text_id == 'device_name':
                    if not current_value:
                        is_field_requared_list.append(text_name)
                        result_s = False
                        continue
                    else:
                        if is_cirylic(current_value):
                            is_field_requared_list.append(text_name)
                            result_s = False
                            continue

                        if CModels.get_model_type_from_model_name(current_value) == MODELS_TYPE.NONE:
                            is_field_requared_list.append(text_name)
                            result_s = False
                            continue

                        model_name = current_value
                        table_scans_list.append([SQL_MASK_FIELDS.mfd_scan_name, current_value])
                        table_models_list.append([SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name, current_value])
                        count += 1
                        continue
                elif text_id == 'vendor_code':
                    if not current_value:
                        is_field_requared_list.append(text_name)
                        result_s = False
                        continue
                    else:
                        if is_cirylic(current_value):
                            is_field_requared_list.append(text_name)
                            result_s = False
                            continue

                        vendor_code = current_value
                        table_models_list.append([SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_vendor_code, current_value])
                        count += 1
                        continue

                if not text_id or not text_name:
                    result_s = False
                    break

                arr_index = CMask.get_field_arr_index_from_text_id(text_id)
                if arr_index == -1:
                    result_s = False
                    break

                table_type = CMask.get_current_table(arr_index)

                sql_template_field = CMask.get_sql_template_label(arr_index)
                sql_state_field = CMask.get_sql_check_label(arr_index)
                requared_once = CMask.get_requared_field(arr_index)

                if current_value is not None:
                    if requared_once:
                        if not current_value:
                            result_s = False
                            is_field_requared_list.append(text_name)
                            continue
                    # проверка на тип в строке число или буква
                    type_of_string_value = CMask.get_field_var_type(arr_index)
                    if current_value:
                        if type_of_string_value is not None:
                            if type_of_string_value == int:
                                if isinstance(current_value, str):
                                    if not current_value.isnumeric():
                                        is_field_requared_list.append(text_name)
                                        result_s = False
                                        continue
                                    new_value_double = int(current_value)
                                    if new_value_double < 1 or new_value_double > 200:
                                        is_field_requared_list.append(text_name)
                                        result_s = False
                                        continue
                                else:
                                    is_field_requared_list.append(text_name)
                                    result_s = False
                                    continue

                            elif type_of_string_value == str:
                                if isinstance(current_value, str):
                                    if is_cirylic(current_value):
                                        is_field_requared_list.append(text_name)
                                        result_s = False
                                        continue
                                else:
                                    is_field_requared_list.append(text_name)
                                    result_s = False
                                    continue
                            else:
                                is_field_requared_list.append(text_name)
                                result_s = False
                                continue

                    if sql_template_field is not None:
                        if type_of_string_value == int:
                            current_value = int(current_value)
                        elif type_of_string_value == str:
                            current_value = str(current_value)

                        if table_type == TableType.TABLE_MODELS:
                            table_models_list.append([sql_template_field, current_value])

                        elif table_type == TableType.TABLE_SCANS:
                            table_scans_list.append([sql_template_field, current_value])

                if state_check is not None:
                    # проверка на обязательные поля
                    if requared_once:
                        if not state_check:
                            result_s = False
                            is_field_requared_list.append(text_name)
                            continue

                    if sql_state_field is not None:
                        if table_type == TableType.TABLE_MODELS:
                            table_models_list.append([sql_state_field, bool(state_check)])
                        elif table_type == TableType.TABLE_SCANS:
                            table_scans_list.append([sql_state_field, bool(state_check)])

            # print(table_scans_list)
            # print(table_models_list)

            if result_s and count:
                result_s = False
                if model_name is not None and vendor_code is not None:

                    if not csql.is_device_name_already(model_name):
                        if not csql.is_device_vendor_code_already(vendor_code):

                            max_index_in_modelid_table = csql.get_last_modelid_index()
                            max_index_in_scan_mask_table = csql.get_last_scan_mask_index()
                            # print(max_index_in_modelid_table, max_index_in_scan_mask_table)
                            if None not in (max_index_in_modelid_table, max_index_in_scan_mask_table) and (
                                    isinstance(max_index_in_modelid_table, int) and isinstance(max_index_in_scan_mask_table, int)
                            ):
                                max_index_in_modelid_table += 1
                                max_index_in_scan_mask_table += 1

                                handle = csql.get_sql_handle()
                                try:
                                    is_success_model_table = csql.insert_modelid_data(
                                        table_models_list,
                                        max_index_in_modelid_table,
                                        max_index_in_scan_mask_table)
                                    is_success_scan_table = csql.insert_scanmask_data(
                                        table_scans_list,
                                        max_index_in_scan_mask_table)

                                    if is_success_model_table and is_success_scan_table:
                                        result_s = True
                                    else:
                                        raise ValueError("Error in create table")
                                except:
                                    handle.rollback()
                                    response_for_client.update({"error_text": "Ошибка в обработке данных таблиц!"})
                                else:
                                    handle.commit()

                                if not result_s:
                                    response_for_client.update({"result": False})
                                    response_for_client.update({"error_text": "Ошибка в обработке данных индексов создания таблиц!"})
                                    cdebug.debug_print(
                                        f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели сканировки] -> [IDX:{account_idx}, {account_name}] -> "
                                        f"[Ошибка создания]")
                                else:

                                    scan_data = csql.get_model_data_log(max_index_in_scan_mask_table, max_index_in_modelid_table)
                                    if scan_data:
                                        cdebug.debug_sql_print(f'{account_name}[{account_idx}]',
                                                               'Создание новой модели',
                                                               scan_data)
                                #################################
                                    text = (f"Пользователь ID: [{account_name}[{account_idx}]] создал новую модель "
                                            f"'{model_name}'[MID: {max_index_in_modelid_table}, SID: {max_index_in_scan_mask_table}]")
                                    CSQLUserLogQuerys.send_log(
                                        account_idx,
                                        LOG_OBJECT_TYPE.LGOT_USER,
                                        LOG_TYPE.LGT_SCAN_TEMPLATE,
                                        LOG_SUBTYPE.LGST_ADD,
                                        text)

                                    response_for_client.update({"error_text": f"Модель устройства '{model_name}' успешно создана!"})
                                    response_for_client.update({"result": True})
                                    response_for_client.update({"arr_result": [max_index_in_modelid_table,
                                                                               max_index_in_scan_mask_table]})
                                    cdebug.debug_print(
                                        f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели устройства] -> [IDX:{account_idx}, {account_name}] -> "
                                        f"[Удачное создание] -> ['{model_name}' SID: {max_index_in_scan_mask_table}, MID: {max_index_in_modelid_table}]")

                            else:
                                response_for_client.update({"error_text": "Ошибка в обработке данных индексов!"})
                                cdebug.debug_print(
                                    f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели устройства] -> [IDX:{account_idx}, {account_name}] -> "
                                    f"[Ошибка создания] -> [Ошибка в обработке данных индексов!]")
                        else:
                            response_for_client.update({"error_text": f"Указанное вами название Vendor Code уже существует '{vendor_code}'!"})
                            cdebug.debug_print(
                                f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели устройства] -> [IDX:{account_idx}, {account_name}] -> "
                                f"[Ошибка создания] -> [Указанное вами название Vendor Code уже существует '{vendor_code}'!]")
                    else:
                        response_for_client.update({"error_text": f"Указанное вами название устройства уже существует '{model_name}'!"})
                        cdebug.debug_print(
                            f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели устройства] -> [IDX:{account_idx}, {account_name}] -> "
                            f"[Ошибка создания] -> [Указанное вами название устройства уже существует '{model_name}']")
                else:
                    response_for_client.update({"error_text": "Ошибка в обработке данных Названия устройства или Кода производителя!"})
                    cdebug.debug_print(
                        f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели устройства] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Ошибка создания] -> [Ошибка в обработке данных Названия устройства или Кода производителя!]")
            else:

                if len(is_field_requared_list) > 0:
                    response_for_client.update({"error_text": f"Ошибка в полях: {','.join(is_field_requared_list)}"})
                else:
                    response_for_client.update({"error_text": "Вы ошиблись во вводе параметров!"})

                cdebug.debug_print(
                    f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели устройства] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Ошибка создания] -> [Ошибка ввода параметров]")
        else:
            raise NotConnectToDB("Not SQL Connect!")

    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: templates_create_mask_set_add_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели устройства] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: templates_create_mask_set_add_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели устройства] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: templates_create_mask_set_add_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели устройства] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: templates_create_mask_set_add_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели устройства] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"templates_create_mask_set_add_ajax AJAX -> [Создание новой модели устройства] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result
