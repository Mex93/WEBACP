from enum import IntEnum


class SQL_CONNECT_DATA_TYPE(IntEnum):
    DATA_NONE = 0,
    PORT = 1,
    DB_NAME = 2,
    USER_NAME = 3,
    HOST = 4,
    PASSWORD = 5


class CONNECT_DB_TYPE(IntEnum):
    NONE = 0,
    LOCAL = 1,
    LINE = 2
