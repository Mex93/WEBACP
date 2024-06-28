from engine.sql.sql_data import SQL_ASSEMBLED_TV_FIELDS, SQL_TV_MODEL_INFO_FIELDS
from engine.devicesn.enums import EDIT_FIELD, PARAMS_ARRAY, CHECK_COMPONENTS


class CDeviceSN:
    __cparams = [
        ['db_primary_key', SQL_ASSEMBLED_TV_FIELDS.fd_assy_id, EDIT_FIELD.NO_EDIT, int, 'Порядковый номер в БД', CHECK_COMPONENTS.NO_CHECK],
        ['model_id', SQL_ASSEMBLED_TV_FIELDS.fd_tvfk, EDIT_FIELD.EDITED, int, 'Номер модели в БД', CHECK_COMPONENTS.NO_CHECK],
        ['model_name', SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name, EDIT_FIELD.NO_EDIT, str, 'Название модели', CHECK_COMPONENTS.NO_CHECK],
        ['model_type_name', None, EDIT_FIELD.NO_EDIT, str, 'Тип модели', CHECK_COMPONENTS.NO_CHECK],
        ['line_number', SQL_ASSEMBLED_TV_FIELDS.fd_linefk, EDIT_FIELD.EDITED, int, 'Номер производственной линии', CHECK_COMPONENTS.NO_CHECK],
        ['device_sn', SQL_ASSEMBLED_TV_FIELDS.fd_tv_sn, EDIT_FIELD.EDITED, str, 'Серийный номер устройства', CHECK_COMPONENTS.CHECK],
        ['wifi_module_sn', SQL_ASSEMBLED_TV_FIELDS.fd_wifi_module_sn, EDIT_FIELD.EDITED, str, 'SN модуля WIFI', CHECK_COMPONENTS.CHECK],
        ['bt_module_sn', SQL_ASSEMBLED_TV_FIELDS.fd_bt_module_sn, EDIT_FIELD.EDITED, str,
         'Серийный номер модуля BT', CHECK_COMPONENTS.CHECK],
        ['ethernet_mac', SQL_ASSEMBLED_TV_FIELDS.fd_tv_mac, EDIT_FIELD.EDITED, str,
         'MAC адрес устройства', CHECK_COMPONENTS.CHECK],
        ['panel_sn', SQL_ASSEMBLED_TV_FIELDS.fd_panel_sn, EDIT_FIELD.EDITED, str,
         'SN панели', CHECK_COMPONENTS.CHECK],
        ['oc_sn', SQL_ASSEMBLED_TV_FIELDS.fd_oc_sn, EDIT_FIELD.EDITED, str,
         'SN OC', CHECK_COMPONENTS.CHECK],
        ['mainboard_sn', SQL_ASSEMBLED_TV_FIELDS.fd_tv_mb_sn, EDIT_FIELD.EDITED, str,
         'SN материнской платы', CHECK_COMPONENTS.CHECK],
        ['pb_sn', SQL_ASSEMBLED_TV_FIELDS.fd_pb_sn, EDIT_FIELD.EDITED, str,
         'SN блока питания', CHECK_COMPONENTS.CHECK],
        ['tcon_sn', SQL_ASSEMBLED_TV_FIELDS.fd_tcon_sn, EDIT_FIELD.EDITED, str,
         'SN TCON', CHECK_COMPONENTS.CHECK],
        ['first_scan_date', SQL_ASSEMBLED_TV_FIELDS.fd_first_scanned_date, EDIT_FIELD.NO_EDIT, 'date',
         'Дата полной сканировки', CHECK_COMPONENTS.NO_CHECK],
        ['scanned_date', SQL_ASSEMBLED_TV_FIELDS.fd_scanned_sn_date, EDIT_FIELD.NO_EDIT, 'date',
         'Дата присвоения SN', CHECK_COMPONENTS.NO_CHECK],
        ['packing_data', SQL_ASSEMBLED_TV_FIELDS.fd_completed_date, EDIT_FIELD.NO_EDIT, 'date',
         'Дата начала упаковки', CHECK_COMPONENTS.NO_CHECK],
        ['ops_sn', SQL_ASSEMBLED_TV_FIELDS.fd_ops_sn, EDIT_FIELD.EDITED, str,
         'SN OPS', CHECK_COMPONENTS.CHECK],
        ['ops_mac', SQL_ASSEMBLED_TV_FIELDS.fd_ops_mac, EDIT_FIELD.EDITED, str,
         'OPS MAC', CHECK_COMPONENTS.CHECK],
        ['usbc_mac', SQL_ASSEMBLED_TV_FIELDS.fd_usbc_mac, EDIT_FIELD.EDITED, str,
         'USB-C MAC', CHECK_COMPONENTS.CHECK],
        ['storage_sn', SQL_ASSEMBLED_TV_FIELDS.fd_storage_sn, EDIT_FIELD.EDITED, str,
         'SN накопителя', CHECK_COMPONENTS.CHECK],
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
    def is_component_check(cls, array_index: int) -> bool:
        if 0 <= array_index <= len(cls.__cparams):

            return True if cls.__cparams[array_index][PARAMS_ARRAY.CHECK_COMPONENTS_STATUS] == CHECK_COMPONENTS.CHECK \
                else False

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
