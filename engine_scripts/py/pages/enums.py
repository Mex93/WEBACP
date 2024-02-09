from enum import IntEnum, auto

class PAGE_ID(IntEnum):
    NONE = auto(),
    LOGIN = auto(),
    LOGOUT = auto(),
    ACCOUNT_MAIN = auto(),
    ACCOUNT_CONFIG = auto(),
    INDEX = auto(),
    ABOUT = auto(),
    PAGE_NOT_FOUND = auto()
