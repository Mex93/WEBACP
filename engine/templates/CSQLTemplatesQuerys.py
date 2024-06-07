from engine.sql.CSQLAgent import CSqlAgent
from engine.sql.sql_data import (SQL_TABLE_NAME, SQL_ASR_FIELDS,
                                 SQL_TV_MODEL_INFO_FIELDS,
                                 SQL_ASSEMBLED_TV_FIELDS)

PROGRAM_TIME_TYPE = "0300"  # Russia
SALT_LEN = 30


class CSQLTemplatesQuerys(CSqlAgent):
    def __init__(self):
        super().__init__()

    def get_tv_list(self) -> list | bool:

        query_string = (f"SELECT "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id}, "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name}, "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_scan_type_fk}, "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_serial_number_template}, "
                        f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_last_update_time} "
                        f"FROM {SQL_TABLE_NAME.tv_model_info_tv} "
                        "LIMIT 100")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, ( ), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id, None)
        if sql_result is not None:
            return result
        return False

    # def check_asr_data(self, asr_name: str, asr_id: int) -> dict | bool:
    #
    #     query_string = (f"SELECT "
    #                     f"{SQL_ASR_FIELDS.asr_fd_tv_asr_id}, "
    #                     f"{SQL_ASR_FIELDS.asr_fd_tv_asr_name}, "
    #                     f"{SQL_ASR_FIELDS.asr_fd_tv_fk}, "
    #                     f"{SQL_ASR_FIELDS.asr_fd_mainboard_sn}, "
    #                     f"{SQL_ASR_FIELDS.asr_fd_ethernet_mac} "
    #                     f"FROM {SQL_TABLE_NAME.asr_tv} "
    #                     f"WHERE "
    #                     f"{SQL_ASR_FIELDS.asr_fd_tv_asr_name} = %s  AND "
    #                     f"{SQL_ASR_FIELDS.asr_fd_tv_asr_id} = %s "
    #                     "LIMIT 1")
    #
    #     result = self.sql_query_and_get_result(
    #         self.get_sql_handle(), query_string, (asr_name, asr_id,), "_1", )  # Запрос типа аасоциативного массива
    #     if result is False:  # Errorrrrrrrrrrrrr based data
    #         return False
    #     # print(result)
    #
    #     sql_result = result[0].get(SQL_ASR_FIELDS.asr_fd_tv_asr_name, None)
    #     if sql_result is not None:
    #         return result
    #     return False
    #
    # def is_tv_one_way(self, tv_fk: int) -> bool:
    #
    #     query_string = (f"SELECT "
    #                     f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_software_type_fk} "
    #                     f"FROM {SQL_TABLE_NAME.tv_model_info_tv} "
    #                     f"WHERE "
    #                     f"{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id} = %s "
    #                     "LIMIT 1")
    #
    #     result = self.sql_query_and_get_result(
    #         self.get_sql_handle(), query_string, (tv_fk,), "_1", )  # Запрос типа аасоциативного массива
    #     if result is False:  # Errorrrrrrrrrrrrr based data
    #         return False
    #     # print(result)
    #
    #     sql_result = result[0].get(SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_software_type_fk, None)
    #
    #     if sql_result is None:
    #         return False
    #
    #     if sql_result == 2:
    #         return True
    #     return False
    #
    # def check_asr_data_in_assembled_table(self, mainboard_sn: str, mac: str) -> dict | bool:
    #
    #     query_string = (f"SELECT "
    #                     f"{SQL_ASSEMBLED_TV_FIELDS.fd_tv_mac}, "
    #                     f"{SQL_ASSEMBLED_TV_FIELDS.fd_tv_mb_sn}, "
    #                     f"{SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn} "
    #                     f"FROM {SQL_TABLE_NAME.assembled_tv} "
    #                     f"WHERE "
    #                     f"{SQL_ASSEMBLED_TV_FIELDS.fd_tv_mac} = %s  OR "
    #                     f"{SQL_ASSEMBLED_TV_FIELDS.fd_tv_mb_sn} = %s "
    #                     "LIMIT 1")
    #
    #     result = self.sql_query_and_get_result(
    #         self.get_sql_handle(), query_string, (mac, mainboard_sn,), "_1", )  #
    #     # Запрос типа аасоциативного массива
    #     if result is False:  # Errorrrrrrrrrrrrr based data
    #         return False
    #     # print(result)
    #
    #     sql_result = result[0].get(SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn, None)
    #     if sql_result is not None:
    #         return result
    #     return False
    #
    # def delete_asr(self, asr_id: str, asr_name: str):
    #
    #     query_string = (f"DELETE FROM {SQL_TABLE_NAME.asr_tv}"
    #                     f" WHERE "
    #                     f"{SQL_ASR_FIELDS.asr_fd_tv_asr_id} = %s AND "
    #                     f"{SQL_ASR_FIELDS.asr_fd_tv_asr_name} = %s"
    #                     )
    #
    #     result = self.sql_query_and_get_result(
    #         self.get_sql_handle(), query_string, (asr_id, asr_name, ), "_d", )  #
    #
    #     return result
    #
    # def update_asr(self, asr_id: str, asr_name: str, update_string: str, update_values: list):
    #
    #     query_string = (f"UPDATE {SQL_TABLE_NAME.asr_tv} SET {update_string} "
    #                     f" WHERE "
    #                     f"{SQL_ASR_FIELDS.asr_fd_tv_asr_id} = %s AND "
    #                     f"{SQL_ASR_FIELDS.asr_fd_tv_asr_name} = %s"
    #                     )
    #     result = self.sql_query_and_get_result(
    #         self.get_sql_handle(), query_string, (*update_values, asr_id, asr_name), "_u", )  #
    #
    #     return result
