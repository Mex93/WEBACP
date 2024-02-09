from enum import IntEnum, auto

class USER_SESSION_TYPE(IntEnum):
    ACC_INDEX = auto(),
    NICKNAME = auto(),
    FIRSTNAME = auto(),
    LASTNAME = auto(),
    LAST_LOGIN_DATE = auto(),
    ALEVEL = auto(),

    ACCOUNT_TIMEOUT_EXIT = auto(),
    ACCOUNT_DISABLED = auto(),
    ACCOUNT_DIS_AINDEX = auto(),
    ACCOUNT_DIS_DATE = auto(),

    ACCESS_SCAN_EDIT = auto(),
    ACCESS_SCAN_DELETE = auto(),
    ACCESS_SCAN_ADD = auto(),

    ACCESS_SN_EDIT = auto(),
    ACCESS_SN_DELETE = auto(),
    ACCESS_SN_ADD = auto(),

    ACCESS_ASR_EDIT = auto(),
    ACCESS_ASR_DELETE = auto(),
    ACCESS_ASR_ADD = auto(),


