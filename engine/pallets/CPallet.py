from engine.sql.sql_data import SQL_PALLET_SN_FIELDS
from engine.pallets.enums import CHECK_COMPONENTS, EDIT_FIELD, INPUT_TYPE, PARAMS_ARRAY


class CPallet:
    __cparams = [
        ['pallet_sn', 'Номер паллета', SQL_PALLET_SN_FIELDS.fd_pallet_code, str, EDIT_FIELD.NO_EDIT, INPUT_TYPE.INPUT, CHECK_COMPONENTS.CHECK],
        ['assy_id', 'Номер паллета в БД', SQL_PALLET_SN_FIELDS.fd_assy_id, int, EDIT_FIELD.NO_EDIT, INPUT_TYPE.INPUT, CHECK_COMPONENTS.CHECK],
        ['completed_check', 'Статус', SQL_PALLET_SN_FIELDS.fd_completed_check, bool, EDIT_FIELD.EDITED, INPUT_TYPE.CHECKBOX, CHECK_COMPONENTS.CHECK],
        ['assembled_line', 'Сборочная линия', SQL_PALLET_SN_FIELDS.fd_assembled_line, int, EDIT_FIELD.EDITED, INPUT_TYPE.INPUT, CHECK_COMPONENTS.CHECK],
        ['create_date', 'Дата создания', SQL_PALLET_SN_FIELDS.fd_created_data, str, EDIT_FIELD.NO_EDIT, INPUT_TYPE.INPUT, CHECK_COMPONENTS.CHECK],
        ['completed_date', 'Дата закрытия', SQL_PALLET_SN_FIELDS.fd_completed_date, str, EDIT_FIELD.NO_EDIT, INPUT_TYPE.INPUT, CHECK_COMPONENTS.CHECK],
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
    def get_input_type(cls, array_index: int) -> str:
        if 0 <= array_index <= len(cls.__cparams):
            return cls.__cparams[array_index][PARAMS_ARRAY.INPUT_TYPE]

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

