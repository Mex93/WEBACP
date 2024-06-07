from enum import IntEnum, auto

class PAGE_ID(IntEnum):
    NONE = auto(),
    ACCOUNT_LOGIN = auto(),
    ACCOUNT_LOGOUT = auto(),
    ACCOUNT_MAIN = auto(),
    ACCOUNT_CONFIG = auto(),

    ASR_FIND = auto(),
    ASR_DEL = auto(),
    ASR_EDIT = auto(),

    TEMPLATES_FIND = auto(),

    INDEX = auto(),
    ABOUT = auto(),
    PAGE_NOT_FOUND = auto(),

