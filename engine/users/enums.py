from enum import IntEnum, auto


class USER_SECTIONS_TYPE(IntEnum):
    ACC_INDEX = auto(),
    NICKNAME = auto(),
    FIRSTNAME = auto(),
    LASTNAME = auto(),
    LAST_LOGIN_DATE = auto(),
    ALEVEL = auto(),

    ACCOUNT_TIMEOUT_EXIT = auto(),
    ACCOUNT_TIMEOUT_EXIT_TIME = auto(),
    ACCOUNT_CHECKER_ACC_FIND_TIME = auto(),
    ACCOUNT_SAVE_ME_START_TIME = auto(),
    ACCOUNT_CHECK_SESSIONS = auto(),

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


class USER_SECTION_ACCESS_TYPE(IntEnum):
    NONE = auto(),
    ACCOUNT = auto(),
    ASR = auto(),
    SCAN_TEMPLATES = auto(),
    SN = auto(),


class USER_ALEVEL(IntEnum):
    ULEVEL_NONE = 0,
    ULEVEL_LINE_MASTER = 1,
    ULEVEL_LINE_TECHNOLOGY = 2,
    ULEVEL_SUPER = 3,
