

from engine.sql.CSQLAgent import CSqlAgent
from engine.sql.sql_data import SQL_TABLE_NAME, SQL_ASR_FIELDS, SQL_TV_MODEL_INFO_FIELDS

PROGRAM_TIME_TYPE = "0300"  # Russia
SALT_LEN = 30


class CSQLASRQuerys(CSqlAgent):
    def __init__(self):
        super().__init__()

    def get_asr_data_from_name(self, asr_name: str) -> str | bool:

        query_string = (f"SELECT "
                        f"{SQL_TABLE_NAME.asr_tv}.*, "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name},"
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_vendor_code} "
                        f"FROM {SQL_TABLE_NAME.asr_tv} "
                        f"JOIN {SQL_TABLE_NAME.tv_model_info_tv} "
                        f"ON {SQL_TABLE_NAME.asr_tv}.{SQL_ASR_FIELDS.asr_fd_tv_fk}= "
                        f"{SQL_TABLE_NAME.tv_model_info_tv}.{SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_id} "
                        f"WHERE {SQL_ASR_FIELDS.asr_fd_tv_asr} = %s " 
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (asr_name,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_ASR_FIELDS.asr_fd_tv_asr, None)
        if sql_result is not None:
            return result
        return False
