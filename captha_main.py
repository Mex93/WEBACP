from flask_simple_captcha import CAPTCHA

CAPTHA_CONFIG = \
    {
        'SECRET_CAPTCHA_KEY': 'LONG_KEY',
        'CAPTCHA_LENGTH': 6,
        'CAPTCHA_DIGITS': False,
        'EXPIRE_SECONDS': 600,
    }

SIMPLE_CAPTCHA = CAPTCHA(config=CAPTHA_CONFIG)
