from engine.sql.sql_data import SQL_ASSEMBLED_TV_FIELDS, SQL_TV_MODEL_INFO_FIELDS
from engine.devicesn.enums import EDIT_FIELD, PARAMS_ARRAY


class CDeviceSN:
    __cparams = [
        ['db_primary_key', SQL_ASSEMBLED_TV_FIELDS.fd_assy_id, EDIT_FIELD.NO_EDIT, int, 'Порядковый номер в БД'],
        ['model_id', SQL_ASSEMBLED_TV_FIELDS.fd_tvfk, EDIT_FIELD.NO_EDIT, int, 'Номер модели в БД'],
        ['model_name', SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name, EDIT_FIELD.NO_EDIT, str, 'Название модели'],
        ['model_type_name', None, EDIT_FIELD.NO_EDIT, str, 'Тип модели'],
        ['line_number', SQL_ASSEMBLED_TV_FIELDS.fd_linefk, EDIT_FIELD.EDITED, int, 'Номер производственной линии'],
        ['device_sn', SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn, EDIT_FIELD.EDITED, str, 'Серийный номер устройства'],
        ['wifi_module_sn', SQL_ASSEMBLED_TV_FIELDS.fd_wifi_module_sn, EDIT_FIELD.EDITED, str, 'SN модуля WIFI'],
        ['bt_module_sn', SQL_ASSEMBLED_TV_FIELDS.fd_bt_module_sn, EDIT_FIELD.EDITED, str,
         'Серийный номер модуля BT'],
        ['ethernet_mac', SQL_ASSEMBLED_TV_FIELDS.fd_tv_mac, EDIT_FIELD.EDITED, str,
         'MAC адрес устройства'],
        ['panel_sn', SQL_ASSEMBLED_TV_FIELDS.fd_panel_sn, EDIT_FIELD.EDITED, str,
         'SN панели'],
        ['oc_sn', SQL_ASSEMBLED_TV_FIELDS.fd_oc_sn, EDIT_FIELD.EDITED, str,
         'SN OC'],
        ['mainboard_sn', SQL_ASSEMBLED_TV_FIELDS.fd_tv_mb_sn, EDIT_FIELD.EDITED, str,
         'SN материнской платы'],
        ['pb_sn', SQL_ASSEMBLED_TV_FIELDS.fd_pb_sn, EDIT_FIELD.EDITED, str,
         'SN блока питания'],
        ['tcon_sn', SQL_ASSEMBLED_TV_FIELDS.fd_tcon_sn, EDIT_FIELD.EDITED, str,
         'SN TCON'],
        ['first_scan_date', SQL_ASSEMBLED_TV_FIELDS.fd_first_scanned_date, EDIT_FIELD.NO_EDIT, 'date',
         'Дата полной сканировки'],
        ['scanned_date', SQL_ASSEMBLED_TV_FIELDS.fd_scanned_sn_date, EDIT_FIELD.NO_EDIT, 'date',
         'Дата присвоения SN'],
        ['packing_data', SQL_ASSEMBLED_TV_FIELDS.fd_completed_date, EDIT_FIELD.NO_EDIT, 'date',
         'Дата начала упаковки'],
        ['ops_sn', SQL_ASSEMBLED_TV_FIELDS.fd_ops_sn, EDIT_FIELD.EDITED, str,
         'SN OPS'],
        ['ops_mac', SQL_ASSEMBLED_TV_FIELDS.fd_ops_mac, EDIT_FIELD.EDITED, str,
         'OPS MAC'],
        ['usbc_mac', SQL_ASSEMBLED_TV_FIELDS.fd_usbc_mac, EDIT_FIELD.EDITED, str,
         'USB-C MAC'],
        ['storage_sn', SQL_ASSEMBLED_TV_FIELDS.fd_storage_sn, EDIT_FIELD.EDITED, str,
         'SN накопителя'],
    ]

    @classmethod
    def get_array_index_from_text_id(cls, text_id: str) -> int:
        for index, item in enumerate(cls.__cparams):
            if item[PARAMS_ARRAY.TEXT_ID] is None:
                continue
            if item[PARAMS_ARRAY.TEXT_ID].find(text_id) != -1:
                return index

    @classmethod
    def get_array_index_from_sql_label(cls, sql_label: str) -> int:
        for index, item in enumerate(cls.__cparams):
            if item[PARAMS_ARRAY.SQL_LABEL] is None:
                continue
            if item[PARAMS_ARRAY.SQL_LABEL].find(sql_label) != -1:
                return index
        return -1

    @classmethod
    def get_text_id(cls, array_index: int) -> str:
        if 0 <= array_index <= len(cls.__cparams):
            return cls.__cparams[array_index][PARAMS_ARRAY.TEXT_ID]

    @classmethod
    def get_sql_label(cls, array_index: int) -> str:
        if 0 <= array_index <= len(cls.__cparams):
            return cls.__cparams[array_index][PARAMS_ARRAY.SQL_LABEL]

    @classmethod
    def is_field_editable(cls, array_index: int) -> bool:
        if 0 <= array_index <= len(cls.__cparams):
            if cls.__cparams[array_index][PARAMS_ARRAY.EDIT_STATUS] == EDIT_FIELD.EDITED:
                return True
        return False

    @classmethod
    def get_text_name(cls, array_index: int) -> str:
        if 0 <= array_index <= len(cls.__cparams):
            return cls.__cparams[array_index][PARAMS_ARRAY.TEXT_NAME]

    @classmethod
    def get_value_type(cls, array_index: int) -> str:
        if 0 <= array_index <= len(cls.__cparams):
            return cls.__cparams[array_index][PARAMS_ARRAY.VALUE_TYPE]
