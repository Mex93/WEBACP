from flask import Flask
from flask_wtf.csrf import CSRFProtect

from datetime import timedelta

import engine.sql.config as sql_config

# Импорт эскизов
from page_account.account import bp_page_account

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=1)

app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{sql_config.db_standart_connect_params[sql_config.KEY_VALUE_NAME_USER]}:"
    f"{sql_config.db_standart_connect_params[sql_config.KEY_VALUE_NAME_PASS]}@"
    f"{sql_config.db_standart_connect_params[sql_config.KEY_VALUE_NAME_HOST]}:"
    f"{sql_config.db_standart_connect_params[sql_config.KEY_VALUE_NAME_PORT]}/"
    f"{sql_config.db_standart_connect_params[sql_config.KEY_VALUE_NAME_DATABASE]}")
app.config['WTF_CSRF_SECRET_KEY'] = 'er09gjurewaiugyhw4e0p9tg24hrgrw0we8twgegdrsghhf'
# Соединение эскизов
app.register_blueprint(bp_page_account, url_prefix='/account')

csrf = CSRFProtect(app)
