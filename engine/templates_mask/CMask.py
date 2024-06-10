from engine.sql.sql_data import SQL_MASK_FIELDS

from engine.templates_mask.enums import MaksArrIndex


class CMask:
    __params_list = \
        (
            ['wifi_module', SQL_MASK_FIELDS.mfd_scan_wifi_module_sn, SQL_MASK_FIELDS.mfd_wifi_module_sn_template,
             'WIFI модуль', 1],

            ['bt_module', SQL_MASK_FIELDS.mfd_scan_bt_module_sn, SQL_MASK_FIELDS.mfd_bt_module_sn_template, 'BT модуль',
             2],

            ['ethernet_mac', SQL_MASK_FIELDS.mfd_scan_ethernet_mac, SQL_MASK_FIELDS.mfd_ethernet_mac_sn_template, 'MAC',
             3],

            ['lcm_sn', SQL_MASK_FIELDS.mfd_scan_lcm_sn, SQL_MASK_FIELDS.mfd_lcm_sn_template, 'PANEL', 4],

            ['oc_sn', SQL_MASK_FIELDS.mfd_scan_oc_sn, SQL_MASK_FIELDS.mfd_oc_sn_template, 'OC', 5],

            ['mainboard_sn', SQL_MASK_FIELDS.mfd_scan_mainboard_sn, SQL_MASK_FIELDS.mfd_mainboard_sn_template, 'MB', 6],

            ['powerboard_sn', SQL_MASK_FIELDS.mfd_scan_powerboard_sn, SQL_MASK_FIELDS.mfd_powerboard_sn_template, 'PB',
             7],

            ['tcon_sn', SQL_MASK_FIELDS.mfd_scan_tcon_sn, SQL_MASK_FIELDS.mfd_tcon_sn_template, 'PB', 8],

            ['ops_sn', SQL_MASK_FIELDS.mfd_scan_ops_sn, SQL_MASK_FIELDS.mfd_ops_sn_template, 'OPS SN', 9],

            ['ops_mac', SQL_MASK_FIELDS.mfd_scan_ops_mac, SQL_MASK_FIELDS.mfd_ops_mac_template, 'OPS MAC', 10],

            ['mac_usbc', SQL_MASK_FIELDS.mfd_scan_mac_usbc, SQL_MASK_FIELDS.mfd_mac_usbc_template, 'USB-C MAC', 11],

            ['storage_sn', SQL_MASK_FIELDS.mfd_scan_storage_sn, SQL_MASK_FIELDS.mfd_storage_template, 'Storage', 12],
        )

    @classmethod
    def get_arr(cls):
        return cls.__params_list

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
        if 0 <= arr_index < len(cls.__params_list):
            if cls.__params_list[MaksArrIndex.SQL_LABEL_CHECK].find(text) != -1:
                return True

    @classmethod
    def is_sql_field_template(cls, arr_index: int, text: str):
        if 0 <= arr_index < len(cls.__params_list):
            if cls.__params_list[MaksArrIndex.SQL_LABEL_TEMPLATE].find(text) != -1:
                return True

    @classmethod
    def get_sql_template_label(cls, arr_index: int) -> str:
        if 0 <= arr_index < len(cls.__params_list):
            return cls.__params_list[arr_index][MaksArrIndex.SQL_LABEL_TEMPLATE]

    @classmethod
    def get_sql_check_label(cls, arr_index: int) -> str:
        if 0 <= arr_index < len(cls.__params_list):
            return cls.__params_list[arr_index][MaksArrIndex.SQL_LABEL_CHECK]

    @classmethod
    def get_text_id(cls, arr_index: int) -> str:
        if 0 <= arr_index < len(cls.__params_list):
            return cls.__params_list[arr_index][MaksArrIndex.TEXT_ID]

    @classmethod
    def get_text_name(cls, arr_index: int) -> str:
        if 0 <= arr_index < len(cls.__params_list):
            return cls.__params_list[arr_index][MaksArrIndex.FIELD_NAME]

    @classmethod
    def get_field_id(cls, arr_index: int) -> int:
        if 0 <= arr_index < len(cls.__params_list):
            return cls.__params_list[arr_index][MaksArrIndex.FIELD_ID]


class CMaskUnit:
    objects = list()

    def __init__(self, field_id: int, cvalue: any, field_type: int):

        is_unit_find = self.get_unit_id_from_field_id(field_id)
        if is_unit_find is None:  # Не найден юнит
            self.field_type = field_type
            self.field_id = field_id
            self.cvalue = cvalue
            self.objects.append(self)
        else:


    @classmethod
    def get_unit_id_from_field_id(cls, field_id: int) -> any:
        if len(cls.objects) > 0:
            for unit in cls.objects:
                if unit.field_id == field_id:
                    return unit
        return None
