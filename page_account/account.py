from flask import Blueprint, render_template, request

from engine.pages.CPages import CPages
from engine.debug.CDebug import CDebug
from engine.users.CUser import CUser
from engine.pages.enums import PAGE_ID
import json
from engine.common import get_checkbox_state, convert_date_from_sql_format

bp_page_account = Blueprint('account', __name__, template_folder='templates', static_folder='static')

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser = CUser()

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.LOGOUT)


@bp_page_account.route(f'/{page_name}')
def logout():
    from page_account.routes.logout import logout

    return logout()


####

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.LOGIN)


@bp_page_account.route(f'/{page_name}', methods=['POST', 'GET'])
def ulogin():
    from page_account.routes.login import ulogin

    return ulogin()


@bp_page_account.route('/account.py', methods=['GET', 'POST'])
def login_ajax():
    # надо как то запретить переход по прямой ссылке к файлу

    password = request.args['cpassword']
    nickname = request.args['cnickname']
    savemy = request.args['csavemy']

    print(password, nickname, savemy)

    result = json.dumps({"new_pass": 12345})
    return result


##########


# page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.ACCOUNT_MAIN)

@bp_page_account.route('/')
def account_main():
    from page_account.routes.main import account_main

    return account_main()


##########

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.ACCOUNT_CONFIG)


@bp_page_account.route(f'/{page_name}')
def account_config():
    from page_account.routes.config import account_config

    return account_config()
