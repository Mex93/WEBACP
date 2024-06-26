from enum import IntEnum, auto

class PAGE_ID(IntEnum):
    NONE = auto(),
    ACCOUNT_LOGIN = auto(),
    ACCOUNT_LOGOUT = auto(),
    ACCOUNT_MAIN = auto(),
    ACCOUNT_CONFIG = auto(),

    ASR_FIND = auto(),

    TEMPLATES_FIND = auto(),
    DEVICESN_FIND = auto(),

    INDEX = auto(),
    ABOUT = auto(),
    PAGE_NOT_FOUND = auto(),

