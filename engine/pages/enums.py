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
    PALLETS_FIND = 8,

    INDEX = 9,
    ABOUT = 10,
    PAGE_NOT_FOUND = 11,
