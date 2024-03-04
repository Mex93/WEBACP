from enum import IntEnum, auto


class LOG_TYPE(IntEnum):
    LGT_NONE = 0,
    LGT_ASR = 1,
    LGT_SN = 2,
    LGT_SCAN_TEMPLATE = 3,
    LGT_USER_ACCOUNT = 4,
    LGT_USER_LOGIN = 5,
    LGT_USER_LOGOUT = 6,


class LOG_SUBTYPE(IntEnum):
    LGST_NONE = 0,
    LGST_UPDATE = 1,
    LGST_ADD = 2,
    LGST_EDIT = 3,
    LGST_DELETE = 4,
    LGST_FIND = 5,


class LOG_OBJECT_TYPE(IntEnum):
    LGOT_NONE = 0,
    LGOT_USER = 1,
    LGOT_SYSTEM = 2,
