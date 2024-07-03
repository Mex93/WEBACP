from flask import json

from engine.pages.CPages import CPages
from engine.users.CUserAccess import CUserAccess
from engine.users.CUser import CUser

from engine.debug.CDebug import CDebug
from engine.users.enums import USER_SECTIONS_TYPE

from engine.templates_mask.CSQLTemplatesQuerys import CSQLTemplatesQuerys
from engine.templates_mask.CMask import CMask
from engine.templates_mask.common import is_field_len, is_cirylic
from engine.templates_mask.enums import TableType

from engine.sql.enums import CONNECT_DB_TYPE
from engine.sql.CSQL import NotConnectToDB, ErrorSQLQuery, ErrorSQLData
from engine.sql.sql_data import SQL_TABLE_NAME

from engine.users.users_log.CSQLUserLogQuerys import CSQLUserLogQuerys
from engine.users.users_log.enums import LOG_TYPE, LOG_SUBTYPE, LOG_OBJECT_TYPE

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_access = CUserAccess()
cuser = CUser()


def templates_save_edit_mask_ajax(pa_array, scan_fk, model_id, model_name):
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    csql = CSQLTemplatesQuerys()
    count = 0
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:
            data = csql.is_valid_scanned_mask(scan_fk, model_id)
            if data is not False:
                state_list_scans = list()
                values_list_scans = list()
                state_list_models = list()
                values_list_models = list()
                count = 0
                print(pa_array)
                error_fields = list()
                for item in pa_array:
                    # print("ttttt " + str(item))

                    text_name, text_id, field_id, field_type, old_value, new_value = item
                    if old_value == new_value or old_value == -777 or old_value is None:
                        continue

                    if text_id == 'model_fk':  # запрет на ввод
                        error_fields.append(text_name)
                        continue

                    # костыль против ввода всего чего либо кроме цифр
                    if text_id == 'platform_fk' or text_id == 'software_type':
                        if not isinstance(new_value, str):
                            error_fields.append(text_name)
                            continue
                        if not new_value.isnumeric():
                            error_fields.append(text_name)
                            continue
                        new_value_double = int(new_value)
                        if new_value_double < 1 or new_value_double > 200:
                            error_fields.append(text_name)
                            continue
                    else:
                        if isinstance(new_value, str):
                            if is_cirylic(new_value):
                                continue

                    if text_id == 'vendor_code':
                        if csql.is_device_vendor_code_already(new_value):
                            error_fields.append(text_name)
                            continue

                    sql_field_index = CMask.get_field_arr_index_from_text_id(text_id)
                    if sql_field_index != -1:

                        table_type = CMask.get_current_table(sql_field_index)
                        if table_type == TableType.TABLE_SCANS:
                            if field_type.find("state") != -1:  # используется или нет

                                sql_field_name = CMask.get_sql_check_label(sql_field_index)
                                if sql_field_name:
                                    state_list_scans.append([sql_field_name, new_value])
                                    count += 1
                            elif field_type.find("value") != -1:  # Значение шаблона
                                if new_value is None:
                                    new_value = ''  # NoneType ошибку даст, нужна строка
                                if is_field_len(new_value):
                                    sql_field_name = CMask.get_sql_template_label(sql_field_index)
                                    if sql_field_name:
                                        values_list_scans.append([sql_field_name, new_value])
                                        count += 1
                        elif table_type == TableType.TABLE_MODELS:
                            if field_type.find("state") != -1:  # используется или нет

                                sql_field_name = CMask.get_sql_check_label(sql_field_index)
                                if sql_field_name:
                                    state_list_models.append([sql_field_name, new_value])
                                    count += 1
                            elif field_type.find("value") != -1:  # Значение шаблона
                                if new_value is None:
                                    new_value = ''  # NoneType ошибку даст, нужна строка
                                if is_field_len(new_value):
                                    sql_field_name = CMask.get_sql_template_label(sql_field_index)
                                    if sql_field_name:
                                        values_list_models.append([sql_field_name, new_value])
                                        count += 1

                if count >= len(pa_array):
                    if count > 0:

                        # models
                        if len(values_list_models):
                            sql_list_fields = list()
                            sql_list_values = list()
                            count = 0
                            for item in values_list_models:
                                sql_label = item[0]
                                values = item[1]
                                sql_list_fields.append(f"{sql_label} = %s")
                                sql_list_values.append(values)
                            sql_fields_str = ','.join(sql_list_fields)
                            if sql_fields_str:
                                csql.update_template_values(SQL_TABLE_NAME.tv_model_info_tv, scan_fk, sql_fields_str,
                                                            sql_list_values)
                                count += 1

                        if len(state_list_models):
                            sql_list_fields = list()
                            sql_list_values = list()
                            for item in state_list_models:
                                sql_label = item[0]
                                values = item[1]
                                sql_list_fields.append(f"{sql_label} = %s")
                                sql_list_values.append(values)
                            sql_fields_str = ','.join(sql_list_fields)
                            if sql_fields_str:
                                csql.update_state_values(SQL_TABLE_NAME.tv_model_info_tv, scan_fk, sql_fields_str,
                                                         sql_list_values)
                                count += 1

                        # scans
                        if len(values_list_scans):
                            sql_list_fields = list()
                            sql_list_values = list()
                            count = 0
                            for item in values_list_scans:
                                sql_label = item[0]
                                values = item[1]
                                sql_list_fields.append(f"{sql_label} = %s")
                                sql_list_values.append(values)
                            sql_fields_str = ','.join(sql_list_fields)
                            if sql_fields_str:
                                csql.update_template_values(SQL_TABLE_NAME.tv_scan_type, scan_fk, sql_fields_str,
                                                            sql_list_values)
                                count += 1

                        if len(state_list_scans):
                            sql_list_fields = list()
                            sql_list_values = list()
                            for item in state_list_scans:
                                sql_label = item[0]
                                values = item[1]
                                sql_list_fields.append(f"{sql_label} = %s")
                                sql_list_values.append(values)
                            sql_fields_str = ','.join(sql_list_fields)
                            if sql_fields_str:
                                csql.update_state_values(SQL_TABLE_NAME.tv_scan_type, scan_fk, sql_fields_str,
                                                         sql_list_values)
                                count += 1

                        if count > 0:
                            csql.update_template_edit_date(model_id)

                            scan_data = csql.get_model_data_log(scan_fk, model_id)
                            if scan_data:
                                cdebug.debug_sql_print(f'{account_name}[{account_idx}]',
                                                       'Изменение модели устройства',
                                                       scan_data)

                            #################################
                            text = f"Пользователь ID: [{account_name}[{account_idx}]] изменил модель устройства '{model_name}'[MID: {model_id}, SID: {scan_fk}]"
                            CSQLUserLogQuerys.send_log(
                                account_idx,
                                LOG_OBJECT_TYPE.LGOT_USER,
                                LOG_TYPE.LGT_SCAN_TEMPLATE,
                                LOG_SUBTYPE.LGST_EDIT,
                                text)

                            response_for_client.update(
                                {"error_text": f"Модель устройства '{model_name}[{model_id}]' изменена!"})
                            response_for_client.update({"result": True})
                            cdebug.debug_print(
                                f"templates_save_edit_mask_ajax AJAX -> [Сохранение редактирования модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
                                f"[Удачно] -> [Модель устройства для '{model_name}[{model_id}]' изменена!] ")
                        else:
                            response_for_client.update(
                                {
                                    "error_text": f"Внутренняя ошибка вычислений номеров строк SQL'{model_name}[{model_id}]'!"})
                            cdebug.debug_print(
                                f"templates_save_edit_mask_ajax AJAX -> [Сохранение редактирования модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
                                f"[Ошибка] -> [Внутренняя ошибка вычислений номеров строк SQL'{model_name}[{model_id}]'!] ")
                    else:
                        response_for_client.update(
                            {
                                "error_text": f"Внутренняя ошибка вычислений номеров строк SQL'{model_name}[{model_id}]'!"})
                        cdebug.debug_print(
                            f"templates_save_edit_mask_ajax AJAX -> [Сохранение редактирования модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
                            f"[Ошибка] -> [Внутренняя ошибка вычислений номеров строк SQL'{model_name}[{model_id}]'!] ")
                else:
                    if len(error_fields) > 0:
                        response_for_client.update(
                            {
                                "error_text": f"Возможно вы ошиблись в некоторых полях '{','.join(error_fields)}'!"})
                    else:
                        response_for_client.update(
                            {
                                "error_text": f"Возможно вы ошиблись в некоторых полях '{model_name}[{model_id}]'!"})
                    cdebug.debug_print(
                        f"templates_save_edit_mask_ajax AJAX -> [Сохранение редактирования модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Ошибка] -> [Возможно вы ошиблись в некоторых полях '{model_name}[{model_id}]'!] ")
            else:
                response_for_client.update(
                    {"error_text": f"Не найдена маска сканировки для '{model_name}[{model_id}]'!"})
                cdebug.debug_print(
                    f"templates_save_edit_mask_ajax AJAX -> [Сохранение редактирования модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Ошибка] -> [Не найдена маска сканировки для '{model_name}[{model_id}]'!] ")
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: templates_save_edit_mask_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"templates_save_edit_mask_ajax AJAX -> [Сохранение редактирования модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: templates_save_edit_mask_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"templates_save_edit_mask_ajax AJAX -> [Сохранение редактирования модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: templates_save_edit_mask_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"templates_save_edit_mask_ajax AJAX -> [Сохранение редактирования модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: templates_save_edit_mask_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"templates_save_edit_mask_ajax AJAX -> [Сохранение редактирования модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"templates_save_edit_mask_ajax AJAX -> [Сохранение редактирования модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result


def templates_get_edit_mask_ajax(scan_fk, model_id, model_name):
    response_for_client = {
        "error_text": "",
        "result": False
    }
    account_name = cuser_access.get_session_var(USER_SECTIONS_TYPE.NICKNAME)
    account_idx = cuser_access.get_session_var(USER_SECTIONS_TYPE.ACC_INDEX)
    csql = CSQLTemplatesQuerys()
    count = 0
    try:
        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
        if result_connect is True:
            data = csql.get_scanned_params(scan_fk, model_id)
            if data is not False:

                count = 0
                for item in data:
                    # print(item)
                    find_index = CMask.get_field_arr_index(item)
                    if find_index == -1:
                        # print(f"Пропущен: {item}")
                        continue
                    sql_check = CMask.get_sql_check_label(find_index)
                    sql_template = CMask.get_sql_template_label(find_index)

                    result = False
                    if sql_template is not None:
                        if CMask.is_sql_field_template(find_index, item):
                            cur_value = data.get(sql_template, '')
                            if cur_value is None:
                                cur_value = ''
                            CMask.set_value(find_index, cur_value)
                            result = True
                    else:
                        CMask.set_value(find_index, None)
                        # print(f"Включен is_sql_field_template: {sql_template}")
                    if not result:
                        if sql_check is not None:
                            if CMask.is_sql_field_check(find_index, item):
                                cur_value = data.get(sql_check, None)
                                CMask.set_current_state(find_index, cur_value)
                                result = True
                                # print(f"Включен is_sql_field_check: {sql_check}")
                        else:
                            CMask.set_current_state(find_index, None)

                    # print(sql_check, sql_template)

                    # if CMask.is_sql_field_template(find_index, item):
                    #     cur_value = data.get(sql_template, None)
                    #     CMask.set_value(find_index, cur_value)
                    #     # print(f"Включен is_sql_field_template: {sql_template}")
                    #
                    # elif CMask.is_sql_field_check(find_index, item):
                    #     cur_value = data.get(sql_check, None)
                    #     CMask.set_current_state(find_index, cur_value)
                    #     # print(f"Включен is_sql_field_check: {sql_check}")
                    if not result:
                        continue

                    count += 1

                if count:
                    arr_len = CMask.get_len()
                    arr_results = list()
                    count = 0
                    for i in range(0, arr_len):
                        cvalue = CMask.get_value(i)
                        cstate = CMask.get_current_state(i)

                        # print(cvalue, cstate)
                        # если не заданы значения из бд (на всякий случай)

                        text_id = CMask.get_text_id(i)
                        field_id = CMask.get_field_id(i)
                        text_name = CMask.get_text_name(i)
                        req_once = CMask.get_requared_field(i)

                        arr_results.append([text_id, field_id, text_name, cvalue, cstate, req_once])
                        count += 1

                    if count:
                        response_for_client.update({"error_text": "Список параметров модели устройства предоставлен"})
                        response_for_client.update({"result": True})
                        response_for_client.update({"arr": arr_results})

                        cdebug.debug_print(
                            f"templates_edit_mask_ajax AJAX -> [Получение списка параметров модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
                            f"[Удачно] -> [Список предоставлен!] ")

                    else:
                        print("Ошибка 2!")
                        response_for_client.update(
                            {"error_text": f"Не найден список параметров модели устройства для '{model_name}[{model_id}]'!"})
                        cdebug.debug_print(
                            f"templates_edit_mask_ajax AJAX -> [Получение списка параметров модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
                            f"[Ошибка] -> [Не найден список параметров модели устройства для '{model_name}[{model_id}]'!] ")
                else:
                    print("Ошибка 1!")
                    response_for_client.update(
                        {"error_text": f"Не найден список сканировки для '{model_name}[{model_id}]'!"})
                    cdebug.debug_print(
                        f"templates_edit_mask_ajax AJAX -> [Получение списка параметров модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
                        f"[Ошибка] -> [Не найден список параметров модели устройства для '{model_name}[{model_id}]'!] ")
            else:
                response_for_client.update(
                    {"error_text": f"Не найден список параметров модели устройства для '{model_name}[{model_id}]'!"})
                cdebug.debug_print(
                    f"templates_edit_mask_ajax AJAX -> [Получение списка параметров модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
                    f"[Ошибка] -> [Не найден список параметров модели устройства для '{model_name}[{model_id}]'!] ")
        else:
            raise NotConnectToDB("Not SQL Connect!")
    except NotConnectToDB as err:
        response_for_client.update({"error_text": "errorcode: templates_edit_mask_ajax -> [NotConnectToDB]"})
        cdebug.debug_print(
            f"templates_edit_mask_ajax AJAX -> [Получение списка параметров модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [NotConnectToDB: '{err}']")

    except ErrorSQLQuery as err:
        response_for_client.update({"error_text": "errorcode: templates_edit_mask_ajax -> [ErrorSQLQuery]"})
        cdebug.debug_print(
            f"templates_edit_mask_ajax AJAX -> [Получение списка параметров модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLQuery: '{err}']")

    except ErrorSQLData as err:
        response_for_client.update({"error_text": "errorcode: templates_edit_mask_ajax -> [ErrorSQLData]"})
        cdebug.debug_print(
            f"templates_edit_mask_ajax AJAX -> [Получение списка параметров модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [ErrorSQLData: '{err}']")

    except Exception as err:

        response_for_client.update({"error_text": "errorcode: templates_edit_mask_ajax -> [Error Data]"})
        cdebug.debug_print(
            f"templates_edit_mask_ajax AJAX -> [Получение списка параметров модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
            f"[Исключение] [Error Data: '{err}']")

    finally:
        csql.disconnect_from_db()

    result = json.dumps(response_for_client)
    cdebug.debug_print(
        f"templates_edit_mask_ajax AJAX -> [Получение списка параметров модели устройства '{model_name}[{model_id}]'] -> [IDX:{account_idx}, {account_name}] -> "
        f"[Ответ в JS] -> [{count}]")
    return result
