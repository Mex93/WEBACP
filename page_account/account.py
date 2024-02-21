from flask import Blueprint, render_template, request, jsonify


from engine.pages.CPages import CPages
from engine.debug.CDebug import CDebug
from engine.users.CUser import CUser
from engine.pages.enums import PAGE_ID
from engine.users.CUserAccess import CUserAccess

import json
from engine.common import get_checkbox_state, convert_date_from_sql_format

bp_page_account = Blueprint('account', __name__, template_folder='templates', static_folder='static')

cdebug = CDebug()
cdebug.debug_system_on(True)

cuser = CUser()
cuser_access = CUserAccess()
cpages = CPages(cdebug)

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.LOGOUT)


@bp_page_account.route(f'/{page_name}')
def logout():
    from page_account.routes.logout import logout

    return logout()


####

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.LOGIN)


@bp_page_account.route(f'/{page_name}', methods=['POST', 'GET'])
def ulogin():
    if cuser_access.is_sessions_start() is True:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    return cpages.set_render_page(PAGE_ID.LOGIN)


@bp_page_account.route('/login_ajax', methods=['POST', 'GET'])
def login_ajax():
    if cuser_access.is_sessions_start() is True:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == "POST":
        json_ajax = request.get_json()
        password = json_ajax['cpassword']
        email = json_ajax['cnickname']
        savemy = json_ajax['csavemy']
        if savemy and email:
            from page_account.routes.login import ulogin
            return ulogin(password, email, savemy)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }
    return jsonify(response_for_client)

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
