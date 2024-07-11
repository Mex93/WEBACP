from engine.sql.CSQLAgent import CSqlAgent
from engine.sql.sql_data import (SQL_TABLE_NAME,
                                 SQL_PALLET_SCANNED_FIELDS,
                                 SQL_PALLET_SN_FIELDS,
                                 SQL_ASSEMBLED_TV_FIELDS
                                 )


class CSQLPalletQuerys(CSqlAgent):
    def __init__(self):
        super().__init__()

    def get_tv_info(self, tv_sn: str) -> bool | dict:
        """Инфа о телевизоре"""
        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.assembled_tv} "
                        f"WHERE {SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn} = %s "
                        f"LIMIT 1")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (tv_sn,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        # print(result)

        return dict(result[0])

    def get_pallet_data(self, pallet_sn: str) -> dict | bool:

        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.pallet_sn} "
                        f"WHERE "
                        f"{SQL_PALLET_SN_FIELDS.fd_pallet_code} = %s "
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (pallet_sn,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_PALLET_SN_FIELDS.fd_pallet_code, None)
        if sql_result is not None:
            return result[0]
        return False

    def is_pallet_valid(self, pallet_sn: str, sql_id: int) -> bool | int:

        query_string = (f"SELECT {SQL_PALLET_SN_FIELDS.fd_assembled_line} "
                        f"FROM {SQL_TABLE_NAME.pallet_sn} "
                        f"WHERE "
                        f"{SQL_PALLET_SN_FIELDS.fd_pallet_code} = %s AND "
                        f"{SQL_PALLET_SN_FIELDS.fd_assy_id} = %s "
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (pallet_sn, sql_id,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_PALLET_SN_FIELDS.fd_assembled_line, None)
        if sql_result is not None:
            return int(sql_result)
        return False

    def insert_scanned_tv_on_pallet(self, pallet_code: str, tv_sn: str, tv_fk: int) -> tuple | bool:
        """Вставить тв в паллет """

        query_string = (f"INSERT INTO "
                        f"{SQL_TABLE_NAME.pallet_scanned}"
                        f"("
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_pallet_code}, "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_tv_sn}, "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_tv_model_fk}"
                        f") VALUES"
                        f"(%s, %s, %s) "
                        f"RETURNING {SQL_PALLET_SCANNED_FIELDS.fd_assy_id}, {SQL_PALLET_SCANNED_FIELDS.fd_scanned_data}")  # на всякий лимит

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (pallet_code, tv_sn, tv_fk), "_i", )
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False

        sql_pass = result[0][0]  # возвращает кортеж с одним элементом
        if sql_pass is None:
            return False

        return result[0][0], result[0][1]  # index, scandate

    def get_pallet_device_count(self, pallet_sn: str) -> int | bool:

        query_string = (f"SELECT COUNT(*) as count_of_devices "
                        f"FROM {SQL_TABLE_NAME.pallet_scanned} "
                        f"WHERE "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_pallet_code} = %s "
                        "LIMIT 100")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (pallet_sn,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get('count_of_devices', None)
        if sql_result is not None:
            return int(sql_result)
        return False

    def delete_all_pallet_devices(self, pallet_sn: str) -> bool:

        query_string = (f"DELETE "
                        f"FROM {SQL_TABLE_NAME.pallet_scanned} "
                        f"WHERE "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_pallet_code} = %s "
                        )

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (pallet_sn,), "_d", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        return True

    def delete_pallet(self, pallet_sn: str, sql_id) -> bool:

        query_string = (f"DELETE "
                        f"FROM {SQL_TABLE_NAME.pallet_sn} "
                        f"WHERE "
                        f"{SQL_PALLET_SN_FIELDS.fd_pallet_code} = %s AND "
                        f"{SQL_PALLET_SN_FIELDS.fd_assy_id} = %s "
                        )

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (pallet_sn, sql_id,), "_d", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        return True

    def get_pallet_data_ex(self, assy_id: int, pallet_sn: str) -> dict | bool:

        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.pallet_sn} "
                        f"WHERE "
                        f"{SQL_PALLET_SN_FIELDS.fd_assy_id} = %s AND "
                        f"{SQL_PALLET_SN_FIELDS.fd_pallet_code} = %s "
                        "LIMIT 1")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (assy_id, pallet_sn,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_PALLET_SN_FIELDS.fd_pallet_code, None)
        if sql_result is not None:
            return result[0]
        return False

    def is_device_in_pallet(self, pallet_sn: str, device_sn: str) -> bool | None:

        query_string = (f"SELECT COUNT(*) as tv_count "
                        f"FROM {SQL_TABLE_NAME.pallet_scanned} "
                        f"WHERE "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_pallet_code} = %s AND "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_tv_sn} = %s "
                        "LIMIT 2")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (pallet_sn, device_sn,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = int(result[0].get('tv_count', None))
        if sql_result is not None:
            if sql_result > 0:
                return True
        else:
            return None
        return False

    def is_device_in_pallet_ex(self, pallet_sn: str, device_sn: str, assy_id: int) -> bool | None:

        query_string = (f"SELECT COUNT(*) as tv_count "
                        f"FROM {SQL_TABLE_NAME.pallet_scanned} "
                        f"WHERE "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_pallet_code} = %s AND "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_assy_id} = %s AND "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_tv_sn} = %s "
                        "LIMIT 2")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (pallet_sn, assy_id, device_sn,),
            "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = int(result[0].get('tv_count', None))
        if sql_result is not None:
            if sql_result > 0:
                return True

        return False

    def delete_device_from_pallet(self, device_sn: str, assy_id: int, pallete_code: str):
        """удалить тв с паллета"""
        query_string = (f"DELETE "
                        f"FROM {SQL_TABLE_NAME.pallet_scanned} "
                        f"WHERE "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_pallet_code} = %s AND "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_assy_id} = %s AND "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_tv_sn} = %s "
                        )  # на всякий лимит

        self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (pallete_code, assy_id, device_sn,),
            "_d", )  # Запрос типа аасоциативного массива

    def get_pallet_sn_from_devices(self, device_sn: str) -> dict | bool:

        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.pallet_scanned} "
                        f"WHERE "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_pallet_code} = %s"
                        "LIMIT 100")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (device_sn,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_PALLET_SCANNED_FIELDS.fd_pallet_code, None)
        if sql_result is not None:
            return result

        return False

    def get_pallet_sn_from_devices_ex(self, pallet_sn: str) -> dict | bool | None:

        query_string = (f"SELECT * "
                        f"FROM {SQL_TABLE_NAME.pallet_scanned} "
                        f"WHERE "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_tv_sn} = %s"
                        "LIMIT 5")

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (pallet_sn,), "_1", )  # Запрос типа аасоциативного массива
        if result is False:  # Errorrrrrrrrrrrrr based data
            return False
        # print(result)

        sql_result = result[0].get(SQL_PALLET_SCANNED_FIELDS.fd_pallet_code, None)
        if sql_result is not None:

            pallets = set()
            for item in result:
                pallets.add(item.get(SQL_PALLET_SN_FIELDS.fd_pallet_code, None))

            if len(pallets) > 1:
                return None

            return result

        return False

    def update_pallet_info(self, pallet_sn: str, pallet_assy: int, sql_label: str, value: any):

        query_string = (f"UPDATE {SQL_TABLE_NAME.pallet_sn} SET {sql_label} = %s "
                        f"WHERE "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_assy_id} = %s AND "
                        f"{SQL_PALLET_SCANNED_FIELDS.fd_pallet_code} = %s"
                        )

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (value, pallet_assy, pallet_sn), "_u", 1, False)  #

        return result

    def set_completed_status(self, pallet_code: str, assy_id: int) -> int | bool:

        query_string = (f"UPDATE {SQL_TABLE_NAME.pallet_sn} SET "
                        f"{SQL_PALLET_SN_FIELDS.fd_completed_date} = now() "
                        f"WHERE "
                        f"{SQL_PALLET_SN_FIELDS.fd_assy_id} = %s AND "
                        f"{SQL_PALLET_SN_FIELDS.fd_pallet_code} = %s"
                        )

        result = self.sql_query_and_get_result(
            self.get_sql_handle(), query_string, (assy_id, pallet_code, ), "_u", )
        return result

