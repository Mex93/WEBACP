from engine.sql.sql_data import SQL_MASK_FIELDS, SQL_TV_MODEL_INFO_FIELDS

from engine.templates_mask.enums import MaksArrIndex, TableType


class CMask:
    __params_list = \
        (
            # None за место sql филда отключает филд в морде и обработчике
            # 1 филд - сканировочное состояние(да нет)
            # 2 филд - значение шаблона
            ['device_sn', None, SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_serial_number_template,
             'Серийный номер устройства', 0, None, None, TableType.TABLE_MODELS, True, str],

            ['vendor_code', None, SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_vendor_code,
             'Vendor Code', 1, None, None, TableType.TABLE_MODELS, True, str],

            ['platform_fk', None, SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_platform_fk,
             'Номер платформы', 2, None, None, TableType.TABLE_MODELS, True, int],

            ['software_type', None, SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_software_type_fk,
             'Тип программного обеспечения', 3, None, None, TableType.TABLE_MODELS, True, int],
            ########################################################

            ['wifi_module', SQL_MASK_FIELDS.mfd_scan_wifi_module_sn, SQL_MASK_FIELDS.mfd_wifi_module_sn_template,
             'WIFI модуль', 4, None, None, TableType.TABLE_SCANS, False, str],

            ['bt_module', SQL_MASK_FIELDS.mfd_scan_bt_module_sn, SQL_MASK_FIELDS.mfd_bt_module_sn_template, 'BT модуль',
             5, None, None, TableType.TABLE_SCANS, False, str],

            ['ethernet_mac', SQL_MASK_FIELDS.mfd_scan_ethernet_mac, SQL_MASK_FIELDS.mfd_ethernet_mac_sn_template, 'MAC',
             6, None, None, TableType.TABLE_SCANS, False, str],

            ['lcm_sn', SQL_MASK_FIELDS.mfd_scan_lcm_sn, SQL_MASK_FIELDS.mfd_lcm_sn_template, 'PANEL', 7, None, None,
             TableType.TABLE_SCANS, False, str],

            ['oc_sn', SQL_MASK_FIELDS.mfd_scan_oc_sn, SQL_MASK_FIELDS.mfd_oc_sn_template, 'OC', 8, None, None,
             TableType.TABLE_SCANS, False, str],

            ['mainboard_sn', SQL_MASK_FIELDS.mfd_scan_mainboard_sn, SQL_MASK_FIELDS.mfd_mainboard_sn_template, 'MB', 9,
             None, None, TableType.TABLE_SCANS, False, str],

            ['powerboard_sn', SQL_MASK_FIELDS.mfd_scan_powerboard_sn, SQL_MASK_FIELDS.mfd_powerboard_sn_template, 'PB',
             10, None, None, TableType.TABLE_SCANS, False, str],

            ['tcon_sn', SQL_MASK_FIELDS.mfd_scan_tcon_sn, SQL_MASK_FIELDS.mfd_tcon_sn_template, 'PB', 11, None, None,
             TableType.TABLE_SCANS, False, str],

            ['ops_sn', SQL_MASK_FIELDS.mfd_scan_ops_sn, SQL_MASK_FIELDS.mfd_ops_sn_template, 'OPS SN', 12, None, None,
             TableType.TABLE_SCANS, False, str],

            ['ops_mac', SQL_MASK_FIELDS.mfd_scan_ops_mac, SQL_MASK_FIELDS.mfd_ops_mac_template, 'OPS MAC', 13, None,
             None, TableType.TABLE_SCANS, False, str],

            ['mac_usbc', SQL_MASK_FIELDS.mfd_scan_mac_usbc, SQL_MASK_FIELDS.mfd_mac_usbc_template, 'USB-C MAC', 14,
             None, None, TableType.TABLE_SCANS, False, str],

            ['storage_sn', SQL_MASK_FIELDS.mfd_scan_storage_sn, SQL_MASK_FIELDS.mfd_storage_template, 'Storage', 15,
             None, None, TableType.TABLE_SCANS, False, str],
        )

    @classmethod
    def get_arr(cls):
        return cls.__params_list

    @classmethod
    def get_len(cls):
        return len(cls.__params_list)

    @classmethod
    def get_field_arr_index(cls, text_id: str) -> int:
        if text_id:
            for index, item in enumerate(cls.__params_list, 0):
                if item[MaksArrIndex.SQL_LABEL_TEMPLATE] is not None:
                    if item[MaksArrIndex.SQL_LABEL_TEMPLATE].find(text_id) != -1:
                        return index

                if item[MaksArrIndex.SQL_LABEL_CHECK] is not None:
                    if item[MaksArrIndex.SQL_LABEL_CHECK].find(text_id) != -1:
                        return index

        return -1

    @classmethod
    def get_field_var_type(cls, arr_index: int) -> bool:
        if 0 <= arr_index < cls.get_len():
            return cls.__params_list[arr_index][MaksArrIndex.VAR_TYPE]

    @classmethod
    def get_requared_field(cls, arr_index: int) -> bool:
        if 0 <= arr_index < cls.get_len():
            return cls.__params_list[arr_index][MaksArrIndex.REQ_FIELD]

    @classmethod
    def get_field_arr_index_from_text_id(cls, text_id: str) -> int:
        if text_id:
            for index, item in enumerate(cls.__params_list, 0):
                if item[MaksArrIndex.TEXT_ID].find(text_id) == -1:
                    continue
                return index
        return -1

    @classmethod
    def is_sql_field_check(cls, arr_index: int, text: str):
        if 0 <= arr_index < cls.get_len():
            if cls.__params_list[arr_index][MaksArrIndex.SQL_LABEL_CHECK] is not None:
                if cls.__params_list[arr_index][MaksArrIndex.SQL_LABEL_CHECK].find(text) != -1:
                    return True
        return False

    @classmethod
    def is_sql_field_template(cls, arr_index: int, text: str):
        if 0 <= arr_index < cls.get_len():
            if cls.__params_list[arr_index][MaksArrIndex.SQL_LABEL_TEMPLATE] is not None:
                if cls.__params_list[arr_index][MaksArrIndex.SQL_LABEL_TEMPLATE].find(text) != -1:
                    return True
        return False

    @classmethod
    def get_sql_template_label(cls, arr_index: int) -> str:
        if 0 <= arr_index < cls.get_len():
            return cls.__params_list[arr_index][MaksArrIndex.SQL_LABEL_TEMPLATE]

    @classmethod
    def get_value(cls, arr_index: int) -> str:
        if 0 <= arr_index < cls.get_len():
            return cls.__params_list[arr_index][MaksArrIndex.VALUE_CURRENT]

    @classmethod
    def get_current_state(cls, arr_index: int) -> str:
        if 0 <= arr_index < cls.get_len():
            return cls.__params_list[arr_index][MaksArrIndex.CHECK_STATE]

    @classmethod
    def get_current_table(cls, arr_index: int) -> str:
        if 0 <= arr_index < cls.get_len():
            return cls.__params_list[arr_index][MaksArrIndex.TABLE_TYPE]

    @classmethod
    def set_value(cls, arr_index: int, cvalue: str | None) -> bool:
        if 0 <= arr_index < cls.get_len():
            cls.__params_list[arr_index][MaksArrIndex.VALUE_CURRENT] = cvalue
            return True

    @classmethod
    def set_current_state(cls, arr_index: int, cstate: bool | None) -> bool:
        if 0 <= arr_index < cls.get_len():
            cls.__params_list[arr_index][MaksArrIndex.CHECK_STATE] = cstate
            return True
        return False

    @classmethod
    def get_sql_check_label(cls, arr_index: int) -> str:
        if 0 <= arr_index < cls.get_len():
            return cls.__params_list[arr_index][MaksArrIndex.SQL_LABEL_CHECK]

    @classmethod
    def get_text_id(cls, arr_index: int) -> str:
        if 0 <= arr_index < cls.get_len():
            return cls.__params_list[arr_index][MaksArrIndex.TEXT_ID]

    @classmethod
    def get_text_name(cls, arr_index: int) -> str:
        if 0 <= arr_index < cls.get_len():
            return cls.__params_list[arr_index][MaksArrIndex.FIELD_NAME]

    @classmethod
    def get_field_id(cls, arr_index: int) -> int:
        if 0 <= arr_index < cls.get_len():
            return cls.__params_list[arr_index][MaksArrIndex.FIELD_ID]
