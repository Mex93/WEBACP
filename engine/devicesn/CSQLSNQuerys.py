from engine.sql.CSQLAgent import CSqlAgent
from engine.sql.sql_data import (SQL_TABLE_NAME,
                                 SQL_TV_MODEL_INFO_FIELDS,
                                 SQL_ASSEMBLED_TV_FIELDS,
                                 )


class CSQLSNQuerys(CSqlAgent):
    def __init__(self):
        super().__init__()

    def get_device_data_log(self, device_sn: str) -> str | bool:

        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.assembled_tv} "
                        f"WHERE "
                        f"{SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn} = %s "
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (device_sn, ), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn, None)
        if sql_result is not None:
            asr_str = str()
            keys = result[0].keys()
            for key in keys:
                value = result[0].get(key, None)
                asr_str += f'{key}: {value} '
            return asr_str

        return False

    def get_device_data(self, device_sn: str):

        query_string = (f"SELECT {SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name},"
                        f"{SQL_TABLE_NAME.assembled_tv}.* "
                        f"FROM {SQL_TABLE_NAME.assembled_tv} "
                        f"JOIN {SQL_TABLE_NAME.tv_model_info_tv} ON "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id} = "
                        f"{SQL_TABLE_NAME.assembled_tv}.{SQL_ASSEMBLED_TV_FIELDS.fd_tvfk} "
                        f"WHERE "
                        f"{SQL_TABLE_NAME.assembled_tv}.{SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn} = %s OR "
                        f"{SQL_TABLE_NAME.assembled_tv}.{SQL_ASSEMBLED_TV_FIELDS.fd_tv_mac} = %s OR "
                        f"{SQL_TABLE_NAME.assembled_tv}.{SQL_ASSEMBLED_TV_FIELDS.fd_tv_mb_sn} = %s"
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (device_sn, device_sn, device_sn,),
            "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
            # print(result)

        device_sn = result[0].get(SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn, None)

        if device_sn is not None:
            return result[0]
        return False

    def is_devicesn_valid(self, device_sn: str, assy_id: int):

        query_string = (f"SELECT {SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn} "
                        f"FROM {SQL_TABLE_NAME.assembled_tv} "
                        f"WHERE "
                        f"{SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn} = %s AND "
                        f"{SQL_ASSEMBLED_TV_FIELDS.fd_assy_id} = %s "
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (device_sn, assy_id,),
            "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
            # print(result)

        new_device_sn = result[0].get(SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn, None)
        if device_sn is not None and device_sn == new_device_sn:
            return True
        return False

    def get_device_sn_from_parameters(self, sql_label: str, find_value: str):

        query_string = (f"SELECT {SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn} "
                        f"FROM {SQL_TABLE_NAME.assembled_tv} "
                        f"WHERE "
                        f"{sql_label} = %s "
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (find_value,),
            "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return None
            # print(result)

        new_device_sn = result[0].get(SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn, None)
        if new_device_sn is not None:
            return new_device_sn
        return None

    def delete_sn(self, assy_id: int):

        query_string = (f"DELETE FROM {SQL_TABLE_NAME.assembled_tv} "
                        f"WHERE "
                        f"{SQL_ASSEMBLED_TV_FIELDS.fd_assy_id} = %s"
                        )

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (assy_id, ), "_d", 1, False)  #

        return result

    def update_device_values(self, device_sn: str, device_assy_id: int, sql_labels: list, values: list):
        if device_sn and device_assy_id:

            values_list = list()
            for index, sql_label in enumerate(sql_labels):
                values_list.append(f"{sql_label} = %s")

            values_str = ','.join(values_list)

            query_string = (f"UPDATE {SQL_TABLE_NAME.assembled_tv} SET {values_str} "
                            f"WHERE "
                            f"{SQL_ASSEMBLED_TV_FIELDS.fd_assy_id} = %s"
                            )

            result = self.sql_query_and_get_result(
                self.get_sql_handle(), query_string, (*values, device_assy_id), "_u", 1, True)  #

            return result
