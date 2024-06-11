from engine.sql.sql_data import SQL_MASK_FIELDS

from engine.templates_mask.enums import MaksArrIndex


class CMask:
    __params_list = \
        (
            ['wifi_module', SQL_MASK_FIELDS.mfd_scan_wifi_module_sn, SQL_MASK_FIELDS.mfd_wifi_module_sn_template,
             'WIFI модуль', 1, None, None],

            ['bt_module', SQL_MASK_FIELDS.mfd_scan_bt_module_sn, SQL_MASK_FIELDS.mfd_bt_module_sn_template, 'BT модуль',
             2, None, None],

            ['ethernet_mac', SQL_MASK_FIELDS.mfd_scan_ethernet_mac, SQL_MASK_FIELDS.mfd_ethernet_mac_sn_template, 'MAC',
             3, None, None],

            ['lcm_sn', SQL_MASK_FIELDS.mfd_scan_lcm_sn, SQL_MASK_FIELDS.mfd_lcm_sn_template, 'PANEL', 4, None, None],

            ['oc_sn', SQL_MASK_FIELDS.mfd_scan_oc_sn, SQL_MASK_FIELDS.mfd_oc_sn_template, 'OC', 5, None, None],

            ['mainboard_sn', SQL_MASK_FIELDS.mfd_scan_mainboard_sn, SQL_MASK_FIELDS.mfd_mainboard_sn_template, 'MB', 6, None, None],

            ['powerboard_sn', SQL_MASK_FIELDS.mfd_scan_powerboard_sn, SQL_MASK_FIELDS.mfd_powerboard_sn_template, 'PB',
             7, None, None],

            ['tcon_sn', SQL_MASK_FIELDS.mfd_scan_tcon_sn, SQL_MASK_FIELDS.mfd_tcon_sn_template, 'PB', 8, None, None],

            ['ops_sn', SQL_MASK_FIELDS.mfd_scan_ops_sn, SQL_MASK_FIELDS.mfd_ops_sn_template, 'OPS SN', 9, None, None],

            ['ops_mac', SQL_MASK_FIELDS.mfd_scan_ops_mac, SQL_MASK_FIELDS.mfd_ops_mac_template, 'OPS MAC', 10, None, None],

            ['mac_usbc', SQL_MASK_FIELDS.mfd_scan_mac_usbc, SQL_MASK_FIELDS.mfd_mac_usbc_template, 'USB-C MAC', 11, None, None],

            ['storage_sn', SQL_MASK_FIELDS.mfd_scan_storage_sn, SQL_MASK_FIELDS.mfd_storage_template, 'Storage', 12, None, None],
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
                if (item[MaksArrIndex.SQL_LABEL_TEMPLATE].find(text_id) == -1 and
                        item[MaksArrIndex.SQL_LABEL_CHECK].find(text_id) == -1):
                    continue
                return index
        return -1

    @classmethod
    def is_sql_field_check(cls, arr_index: int, text: str):
        if 0 <= arr_index < cls.get_len():
            if cls.__params_list[arr_index][MaksArrIndex.SQL_LABEL_CHECK].find(text) != -1:
                return True
        return False

    @classmethod
    def is_sql_field_template(cls, arr_index: int, text: str):
        if 0 <= arr_index < cls.get_len():
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
    def set_value(cls, arr_index: int, cvalue: str) -> bool:
        if 0 <= arr_index < cls.get_len():
            cls.__params_list[arr_index][MaksArrIndex.VALUE_CURRENT] = cvalue
            return True

    @classmethod
    def set_current_state(cls, arr_index: int, cstate: bool) -> bool:
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
