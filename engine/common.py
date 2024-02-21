from flask import request

from datetime import datetime
import time


def get_checkbox_state(value):
    if value == 'on':
        value = True
    else:
        value = False
    return value


def get_current_unix_time() -> int:
    return int(int(datetime.now().timestamp()))


def get_data_stamp_from_unix_time(cur_unix_time,
                                  stamp_format: str = "%Y-%m-%d %H:%M:%S %z") -> str:
    """
    Получит временной штамп исходя из полученного unix time сначала эпохи
    Вернёт полученный штамп в виде строки указанного формата в параметрах

    :param timezone_str:
    :param stamp_format:
    :param cur_unix_time:
    :return:
    """
    s = time.strftime(stamp_format, time.gmtime(cur_unix_time))  # смещение для UTC
    return s


def convert_date_from_sql_format(date: str):
    string = date.split(".")[0]
    if string is False:
        string = ""
    return string


def get_empty_spaces_string(count: int) -> str:
    string = ""
    for index in range(count):
        string += " "
    return string


def get_current_data_stamp():
    unix = get_current_unix_time()
    return get_data_stamp_from_unix_time(unix)

def get_inet_ipaddress():
    return request.remote_addr


