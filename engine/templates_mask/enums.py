from enum import IntEnum


class MaksArrIndex(IntEnum):
    TEXT_ID = 0,
    SQL_LABEL_CHECK = 1,
    SQL_LABEL_TEMPLATE = 2,
    FIELD_NAME = 3,
    FIELD_ID = 4,
    VALUE_CURRENT = 5,
    CHECK_STATE = 6,
    TABLE_TYPE = 7,
    REQ_FIELD = 8,
    VAR_TYPE = 9,

class TableType(IntEnum):
    TABLE_MODELS = 0,
    TABLE_SCANS = 1,
