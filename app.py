from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
from engine_scripts.py.users.CUserSessions import CUserSessions

from engine_scripts.py.pages.CPages import CPages
from engine_scripts.py.pages.enums import PAGE_ID

import engine_scripts.py.pages.login.login_actions as login_actions
from engine_scripts.py.debug.CDebug import CDebug

import json
import engine_scripts.py.sql.config as sql_config
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from engine_scripts.py.sql.sql_data import SQL_TABLE_NAME, SQL_USERS_FIELDS
from engine_scripts.py.users.common import MAX_USER_NICKNAME_LEN

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

cuser_sessions = CUserSessions()
cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)


@app.route('/logo.ico')
def favicon():
    return url_for('static', filename='/static/img/logo.ico')


db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return cpages.set_render_page(PAGE_ID.INDEX)


@app.route('/account')
def account_main():
    if cuser_sessions.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.LOGIN)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_MAIN)


@app.route('/config')
def account_config():
    # if cuser_sessions.is_sessions_start() is False:
    # return cpages.redirect_on_page(PAGE_ID.LOGIN)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_CONFIG)


@app.route('/ulogout')
def logout():
    # if cuser_sessions.is_sessions_start() is False:
    #     return cpages.redirect_on_page(PAGE_ID.LOGIN)

    return cpages.set_render_page(PAGE_ID.LOGOUT)


@app.route('/ulogin', methods=['POST', 'GET'])
def ulogin():
    if cuser_sessions.is_sessions_start() is True:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == 'POST':
        # получаем данные от кнопок и полей
        user_name = request.form['user_name']
        user_pass = request.form['user_pass']
        user_save_me = get_checkbox_state(request.form.get('user_save_me'))

        print(user_name)
        print(user_pass)
        print(user_save_me)
        result = login_actions.set_login(user_name, user_pass, bool(user_save_me))
        print(result)
        if isinstance(result, tuple):
            error_text = result[1]
            return cpages.set_render_page(PAGE_ID.LOGIN, errors=error_text)
            # cpages.set_render_page(PAGE_ID.LOGIN, errors=error_text)
            # render_template("login.html", errors=error_text)

    return cpages.set_render_page(PAGE_ID.LOGIN)


@app.route('/about')
def about():
    return cpages.set_render_page(PAGE_ID.ABOUT)


# @app.errorhandler(404)
# def page_not_found(error_str):
#
#     return cpages.set_render_page(PAGE_ID.PAGE_NOT_FOUND)


@app.route('/user/<string:name>/<int:uid>')
def user(name=str, uid=int):
    return "User Page Name: " + str(name) + " ID:" + str(uid)


def get_checkbox_state(value):
    if value == 'on':
        value = True
    else:
        value = False
    return value


if __name__ == "__main__":
    app.run(debug=True)
