from enum import IntEnum


class EDIT_FIELD(IntEnum):
    EDITED = 0,
    NO_EDIT = 1,


class INPUT_TYPE(IntEnum):
    CHECKBOX = 0,
    INPUT = 1


class CHECK_COMPONENTS(IntEnum):
    CHECK = 0,
    NO_CHECK = 1,


class PARAMS_ARRAY(IntEnum):
    TEXT_ID = 0,
    TEXT_NAME = 1,
    SQL_LABEL = 2,
    VALUE_TYPE = 3,
    EDIT_STATUS = 4,
    INPUT_TYPE = 5,
    CHECK_COMPONENTS_STATUS = 6,
