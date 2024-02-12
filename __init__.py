
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta

import engine.sql.config as sql_config
from engine.pages.CPages import CPages
from engine.users.CUserSessions import CUserSessions
from engine.debug.CDebug import CDebug


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

cdb = SQLAlchemy(app)
cmigrate = Migrate(app, cdb)

cuser_sessions = CUserSessions()
cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
