from enum import IntEnum


class PAGE_ID(IntEnum):
    NONE = 0,
    ACCOUNT_LOGIN = 1,
    ACCOUNT_LOGOUT = 2,
    ACCOUNT_MAIN = 3,
    ACCOUNT_CONFIG = 4,

    ASR_FIND = 5,

    TEMPLATES_FIND = 6,
    DEVICESN_FIND = 7,

    INDEX = 8,
    ABOUT = 9,
    PAGE_NOT_FOUND = 10,
