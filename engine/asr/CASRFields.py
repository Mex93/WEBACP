from engine.asr.enums import ASRFieldsType
from engine.sql.sql_data import SQL_ASR_FIELDS, SQL_TV_MODEL_INFO_FIELDS
from engine.asr.HTMLFieldsName import HTMLFieldsName


class CASRFields:
    def __init__(self):
        self.__ASRFieldsAssoc = (
            (HTMLFieldsName.tv_field_asr_name, SQL_ASR_FIELDS.asr_fd_tv_asr_name, ASRFieldsType.ASR_NAME, "ASR_NAME", "ASR"),
            (HTMLFieldsName.tv_field_asr_id, SQL_ASR_FIELDS.asr_fd_tv_asr_id, ASRFieldsType.ASR_ID, "ASR_SQL_ID", "ID ASR в БД"),
            (HTMLFieldsName.tv_field_tv_fk, SQL_ASR_FIELDS.asr_fd_tv_fk, ASRFieldsType.TV_ID, "ASR_TV_FK", "ID модели телевизора в БД"),
            (HTMLFieldsName.tv_fild_model_name, SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name, ASRFieldsType.TV_NAME, "ASR_MODEL_NAME", "Название модели"),
            (HTMLFieldsName.tv_fild_model_type_name, SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_model_type_name, ASRFieldsType.MODEL_TYPE_NAME, "ASR_MODEL_TYPE_NAME", "Тип модели"),
            (HTMLFieldsName.tv_fild_vendor_code, SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_vendor_code, ASRFieldsType.VENDOR_CODE, "ASR_VENDOR_CODE", "Vendor Code"),
            (HTMLFieldsName.tv_field_line_id, SQL_ASR_FIELDS.asr_fd_line_fk, ASRFieldsType.LINE_ID, "ASR_LINE_ID", "Номер линии"),
            (HTMLFieldsName.tv_field_wf, SQL_ASR_FIELDS.asr_fd_wifi_module_sn, ASRFieldsType.WM_MODULE, "ASR_WF", "WIFI Модуль"),
            (HTMLFieldsName.tv_field_bt, SQL_ASR_FIELDS.asr_fd_bt_module_sn, ASRFieldsType.BT_MODULE, "ASR_BT", "BT Модуль"),
            (HTMLFieldsName.tv_field_mac, SQL_ASR_FIELDS.asr_fd_ethernet_mac, ASRFieldsType.MB_MAC, "ASR_MAC", "MAC"),
            (HTMLFieldsName.tv_field_panel, SQL_ASR_FIELDS.asr_fd_lcm_sn, ASRFieldsType.PANEL_SN, "ASR_PANEL", "Номер панели"),
            (HTMLFieldsName.tv_field_oc, SQL_ASR_FIELDS.asr_fd_oc_sn, ASRFieldsType.OC_SN, "ASR_OC", "Номер стекла"),
            (HTMLFieldsName.tv_field_mb, SQL_ASR_FIELDS.asr_fd_mainboard_sn, ASRFieldsType.MB_SN, "ASR_MB", "Номер материнской платы"),
            (HTMLFieldsName.tv_field_pb, SQL_ASR_FIELDS.asr_fd_powerboard_sn, ASRFieldsType.PB_SN, "ASR_PB", "Номер блока питания"),
            (HTMLFieldsName.tv_field_tcon, SQL_ASR_FIELDS.asr_fd_tcon_sn, ASRFieldsType.TCON_SN, "ASR_TCON", "Номер TCON"),
            (HTMLFieldsName.tv_field_scan_date, SQL_ASR_FIELDS.asr_fd_timestamp_st10, ASRFieldsType.SCAN_DATE, "ASR_SCAN_DATE", "Дата сканировки"),
            (HTMLFieldsName.tv_field_ops, SQL_ASR_FIELDS.asr_fd_ops_sn, ASRFieldsType.OPS_SN, "ASR_OPS", "Номер OPS"),
        )

    def get_html_field_name_from_sql_name(self, sql_name):
        for item in self.__ASRFieldsAssoc:
            if item[1].find(sql_name, 0, len(sql_name)) != -1:
                return item[0]
        return None

    def get_html_field_name_from_field_type(self, field_type):
        for item in self.__ASRFieldsAssoc:
            if item[2] == field_type:
                return item[0]
        return None

    def get_field_type_id_from_field_name(self, field_name: str) -> None | int:
        for item in self.__ASRFieldsAssoc:
            if item[1].find(field_name, 0, len(field_name)) != -1:
                return item[2].value
        return None

    def get_asr_field_name_from_type_id(self, field_id: int) -> None | str:
        for item in self.__ASRFieldsAssoc:
            if item[2].value == field_id:
                return item[1]
        return None

    def get_assoc_tuple(self):
        return self.__ASRFieldsAssoc

    @staticmethod
    def get_types_tuple():
        return (
            ASRFieldsType.ASR_ID,
            ASRFieldsType.ASR_NAME,
            ASRFieldsType.TV_ID,
            ASRFieldsType.LINE_ID,
            ASRFieldsType.WM_MODULE,
            ASRFieldsType.BT_MODULE,
            ASRFieldsType.MB_MAC,
            ASRFieldsType.PANEL_SN,
            ASRFieldsType.OC_SN,
            ASRFieldsType.MB_SN,
            ASRFieldsType.PB_SN,
            ASRFieldsType.TCON_SN,
            ASRFieldsType.SCAN_DATE,
            ASRFieldsType.OPS_SN,
            ASRFieldsType.TV_NAME,
            ASRFieldsType.MODEL_TYPE_NAME,
            ASRFieldsType.VENDOR_CODE
        )