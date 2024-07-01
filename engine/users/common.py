from flask import request

MAX_USER_NICKNAME_LEN = 35
MIN_USER_NICKNAME_LEN = 4

MAX_USER_FIRSTNAME_LASTNAME_LEN = 20
MIN_USER_FIRSTNAME_LASTNAME_LEN = 4

MAX_USER_EMAIL_LEN = 35
MIN_USER_EMAIL_LEN = 4

MAX_USER_PASSWORD_LEN = 16
MIN_USER_PASSWORD_LEN = 6


MAX_ACTIVITY_TIME_LEFT = 10 * 600  # sec 10 min
MAX_CHECK_PERMISSIONS_TIME_LEFT = 10 * 600  # Чекер валидности аккаунта * 600
MAX_USER_SESSION_LIFE_TIME = 60 * 600  # Время сброса времени сессии для юзера через час неактивности,
# если не выбрано сохранить меня



