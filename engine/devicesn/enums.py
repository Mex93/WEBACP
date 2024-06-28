from enum import IntEnum, auto


class EDIT_FIELD(IntEnum):
    EDITED = 0,
    NO_EDIT = 1,

class CHECK_COMPONENTS(IntEnum):
    CHECK = 0,
    NO_CHECK = 1,


class PARAMS_ARRAY(IntEnum):
    TEXT_ID = 0,
    SQL_LABEL = 1,
    EDIT_STATUS = 2,
    VALUE_TYPE = 3,
    TEXT_NAME = 4,
    CHECK_COMPONENTS_STATUS = 5,
