from engine.sql.CSQLAgent import CSqlAgent
from engine.sql.sql_data import (SQL_TABLE_NAME,
                                 SQL_TV_MODEL_INFO_FIELDS,
                                 SQL_MASK_FIELDS,
                                 SQL_ASSEMBLED_TV_FIELDS,
                                 SQL_PALLET_SCANNED_FIELDS)


class CSQLTemplatesQuerys(CSqlAgent):
    def __init__(self):
        super().__init__()

    def get_model_data_log(self, scan_fk: int, model_fk: int) -> str | bool:

        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.tv_scan_type} "
                        f"JOIN {SQL_TABLE_NAME.tv_model_info_tv} ON "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk} = "
                        f"{SQL_TABLE_NAME.tv_scan_type}.{SQL_MASK_FIELDS.mfd_scan_type_id} "
                        f"WHERE "
                        f"{SQL_TABLE_NAME.tv_scan_type}.{SQL_MASK_FIELDS.mfd_scan_type_id} = %s AND "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk} = %s AND "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id} = %s"
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (scan_fk, scan_fk, model_fk,),
            "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk, None)
        if sql_result is not None:
            template_str = str()
            keys = result[0].keys()
            for key in keys:
                value = result[0].get(key, None)
                template_str += f'{key}: {value} '
            return template_str

        return False

    def get_tv_list(self) -> list | bool:

        query_string = (f"SELECT "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id}, "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name}, "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk}, "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_serial_number_template}, "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_last_update_time} "
                        f"FROM {SQL_TABLE_NAME.tv_model_info_tv} "
                        f"ORDER BY {SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id} DESC "
                        "LIMIT 100")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id, None)
        if sql_result is not None:
            return result
        return False

    def is_any_model_used_on_devices(self, model_id: int) -> list | bool:

        query_string = (f"SELECT COUNT(*) as cout_of_tv "
                        f"FROM {SQL_TABLE_NAME.assembled_tv} "
                        f"WHERE {SQL_ASSEMBLED_TV_FIELDS.fd_tvfk} = %s "
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (model_id,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get('cout_of_tv', None)

        if isinstance(sql_result, int):
            if sql_result > 0:
                return True
        return False

    def is_model_in_any_pallet(self, model_id: int) -> dict | bool:

        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.pallet_scanned} "
                        f"WHERE {SQL_PALLET_SCANNED_FIELDS.fd_tv_model_fk} = %s "
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (model_id,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_PALLET_SCANNED_FIELDS.fd_pallet_code, None)
        if sql_result is not None:
            return dict(sql_result)

        return False

    def get_scanned_params(self, scan_fk: int, model_fk: int) -> dict | bool:

        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.tv_scan_type} "
                        f"JOIN {SQL_TABLE_NAME.tv_model_info_tv} ON "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk} = "
                        f"{SQL_TABLE_NAME.tv_scan_type}.{SQL_MASK_FIELDS.mfd_scan_type_id} "
                        f"WHERE "
                        f"{SQL_TABLE_NAME.tv_scan_type}.{SQL_MASK_FIELDS.mfd_scan_type_id} = %s AND "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk} = %s AND "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id} = %s"
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (scan_fk, scan_fk, model_fk,),
            "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
            # print(result)

        par_0 = result[0].get(SQL_MASK_FIELDS.mfd_scan_type_id, None)
        par_1 = result[0].get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk, None)
        par_2 = result[0].get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id, None)
        if None not in (par_0, par_1, par_2):
            return result[0]
        return False

    def is_valid_scanned_mask(self, scan_fk: int, model_fk: int) -> list | bool:

        query_string = (f"SELECT "
                        f"{SQL_TABLE_NAME.tv_scan_type}.{SQL_MASK_FIELDS.mfd_scan_type_id},"
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk},"
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id} "
                        f"FROM {SQL_TABLE_NAME.tv_scan_type} "
                        f"JOIN {SQL_TABLE_NAME.tv_model_info_tv} ON "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk} = "
                        f"{SQL_TABLE_NAME.tv_scan_type}.{SQL_MASK_FIELDS.mfd_scan_type_id} "
                        f"WHERE "
                        f"{SQL_TABLE_NAME.tv_scan_type}.{SQL_MASK_FIELDS.mfd_scan_type_id} = %s AND "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk} = %s AND "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id} = %s"
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (scan_fk, scan_fk, model_fk,),
            "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        par_0 = result[0].get(SQL_MASK_FIELDS.mfd_scan_type_id, None)
        par_1 = result[0].get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk, None)
        par_2 = result[0].get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id, None)
        if None not in (par_0, par_1, par_2):
            return True
        return False

    def delete_template(self, scan_fk: int, model_fk: int):

        handle = self.get_sql_handle()
        try:

            query_string = (f"DELETE FROM {SQL_TABLE_NAME.tv_model_info_tv}"
                            f" WHERE "
                            f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id} = %s"
                            )

            result = self.sql_query_and_get_result(
                handle, query_string, (model_fk,), "_d", 1, True)  #

            if result is False:
                raise "Error"

            query_string = (f"DELETE FROM {SQL_TABLE_NAME.tv_scan_type}"
                            f" WHERE "
                            f"{SQL_MASK_FIELDS.mfd_scan_type_id} = %s"
                            )

            result = self.sql_query_and_get_result(
                handle, query_string, (scan_fk,), "_d", 1, True)  #

            if result is False:
                raise "Error"
        except Exception as err:
            handle.rollback()
            print(f"Ошибка трансакции удаления шаблона: '{err}'")
            return False
        else:
            handle.commit()

        return True

    def update_template_values(self, table_name: str, scan_fk: int, template_str: str, values_list: list):

        if template_str and scan_fk and len(values_list) and table_name:
            target_value = str()
            if table_name == SQL_TABLE_NAME.tv_scan_type:
                target_value = SQL_MASK_FIELDS.mfd_scan_type_id
            elif table_name == SQL_TABLE_NAME.tv_model_info_tv:
                target_value = SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk

            query_string = (f"UPDATE {table_name} SET {template_str} "
                            f" WHERE "
                            f"{target_value} = %s"
                            )
            result = self.sql_query_and_get_result(
                self.get_sql_handle(), query_string, (*values_list, scan_fk,), "_u", 1, False)  #

            return result

    def update_state_values(self, table_name: str, scan_fk: int, state_str: str, values_list: list):

        if state_str and scan_fk and len(values_list) and table_name:
            target_value = str()
            if table_name == SQL_TABLE_NAME.tv_scan_type:
                target_value = SQL_MASK_FIELDS.mfd_scan_type_id
            elif table_name == SQL_TABLE_NAME.tv_model_info_tv:
                target_value = SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk

            query_string = (f"UPDATE {table_name} SET {state_str} "
                            f" WHERE "
                            f"{target_value} = %s"
                            )

            result = self.sql_query_and_get_result(
                self.get_sql_handle(), query_string, (*values_list, scan_fk,), "_u", 1, False)  #

            return result

    def update_template_edit_date(self, model_id_fk: int):

        if model_id_fk:
            query_string = (f"UPDATE {SQL_TABLE_NAME.tv_model_info_tv} SET last_updated_time = now()"
                            f" WHERE "
                            f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id} = %s"
                            )
            result = self.sql_query_and_get_result(
                self.get_sql_handle(), query_string, (model_id_fk,), "_u", 1, False)  #

            return result

    def is_device_name_already(self, text: str) -> bool:

        query_string = (f"SELECT {SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name} "
                        f"FROM {SQL_TABLE_NAME.tv_model_info_tv} "
                        f"WHERE "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name} = %s"
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (text,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
            # print(result)

        name = result[0].get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name, None)
        if name is not None:
            return True
        return False

    def is_device_vendor_code_already(self, text: str) -> bool:

        query_string = (f"SELECT {SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_vendor_code} "
                        f"FROM {SQL_TABLE_NAME.tv_model_info_tv} "
                        f"WHERE "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_vendor_code} = %s"
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (text,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
            # print(result)

        name = result[0].get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_vendor_code, None)
        if name is not None:
            return True
        return False

    def get_last_modelid_index(self) -> None | int:

        query_string = (f"SELECT MAX({SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id}) as max_value "
                        f"FROM {SQL_TABLE_NAME.tv_model_info_tv} "
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return None
            # print(result)

        return result[0].get('max_value', None)

    def get_last_scan_mask_index(self) -> None | int:

        query_string = (f"SELECT MAX({SQL_MASK_FIELDS.mfd_scan_type_id}) as max_value "
                        f"FROM {SQL_TABLE_NAME.tv_scan_type} "
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return None
            # print(result)

        return result[0].get('max_value', None)

    def insert_modelid_data(self, modelid_data_list: list, modelid_index: int, scan_mask_index: int) -> bool:
        if len(modelid_data_list) > 0 and modelid_index > 0 and scan_mask_index > 0:
            fields = list()
            values = list()
            for item in modelid_data_list:
                fields.append(item[0])
                values.append(item[1])

            len_values = len(values)
            if (len(fields) > 0 and len_values > 0) and (len(fields) == len_values):

                str_formats = list()
                for item in range(len_values):
                    str_formats.append("%s")

                query_string = (f"INSERT INTO {SQL_TABLE_NAME.tv_model_info_tv} "
                                f"({SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id}, "
                                f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk}, "
                                f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_last_update_time}, "
                                f"{', '.join(fields)})"
                                f"VALUES (%s, %s, now(), {','.join(str_formats)}) RETURNING "
                                f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id}")

                result = self.sql_query_and_get_result(
                    self.get_sql_handle(), query_string, (modelid_index, scan_mask_index, *values), "_i", 1, True)
                if result:
                    return True
                    # print(result)

        return False

    def insert_scanmask_data(self, scanmask_data_list: list, scan_mask_index: int) -> bool:
        if len(scanmask_data_list) > 0 and scan_mask_index > 0:
            fields = list()
            values = list()
            for item in scanmask_data_list:
                fields.append(item[0])
                values.append(item[1])

            len_values = len(values)
            if (len(fields) > 0 and len_values > 0) and (len(fields) == len_values):

                str_formats = list()
                for item in range(len_values):
                    str_formats.append("%s")

                query_string = (f"INSERT INTO {SQL_TABLE_NAME.tv_scan_type} "
                                f"({SQL_MASK_FIELDS.mfd_scan_type_id}, "
                                f"{', '.join(fields)})"
                                f"VALUES (%s, {','.join(str_formats)}) RETURNING "
                                f"{SQL_MASK_FIELDS.mfd_scan_type_id}")

                result = self.sql_query_and_get_result(
                    self.get_sql_handle(), query_string, (scan_mask_index, *values), "_i", 1, True)
                if result:
                    return True
                    # print(result)

        return False
