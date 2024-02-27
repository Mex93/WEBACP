from flask import Blueprint, request, jsonify

from engine.debug.CDebug import CDebug
from engine.pages.CPages import CPages
from engine.pages.enums import PAGE_ID
from engine.users.CUser import CUser
from engine.users.CUserAccess import CUserAccess
from engine.common import get_checkbox_state

bp_page_account = Blueprint('account', __name__, template_folder='templates', static_folder='static')

cdebug = CDebug()
cdebug.debug_system_on(True)

cuser = CUser()
cuser_access = CUserAccess()
cpages = CPages(cdebug)

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.ACCOUNT_LOGOUT)


@bp_page_account.route(f'/{page_name}', methods=['POST', 'GET'])
def logout():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    from page_account.routes.logout import logout
    if request.method == "POST":
        if 'yes' in request.form:
            return logout()
        elif 'no' in request.form:
            return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_LOGOUT)


####

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.ACCOUNT_LOGIN)


@bp_page_account.route(f'/{page_name}', methods=['POST', 'GET'])
def ulogin():
    if cuser_access.is_sessions_start() is True:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_LOGIN)


@bp_page_account.route('/login_ajax', methods=['POST', 'GET'])
def login_ajax():
    if cuser_access.is_sessions_start() is True:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == "POST":
        json_ajax = request.get_json()
        password = json_ajax['cpassword']
        email = json_ajax['cnickname']
        savemy = json_ajax['csavemy']

        if password and email:
            from page_account.routes.login import ulogin
            return ulogin(password, email, savemy)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }
    return jsonify(response_for_client)


##########


# page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.ACCOUNT_MAIN)
@bp_page_account.route('/account_logs_ajax', methods=['POST', 'GET'])
def account_logs():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if request.method == "POST":
        from page_account.routes.main import account_logs_ajax
        return account_logs_ajax()

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }
    return jsonify(response_for_client)


@bp_page_account.route('/')
def account_main():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_MAIN)


##########

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.ACCOUNT_CONFIG)


@bp_page_account.route(f'/{page_name}')
def account_config():
    from page_account.routes.config import account_config

    return account_config()


@bp_page_account.route('/repass_ajax', methods=['POST', 'GET'])
def repass_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if request.method == "POST":
        json_ajax = request.get_json()
        old_pass = json_ajax['cold_pass']
        new_pass = json_ajax['cnew_pass']
        re_pass = json_ajax['cre_pass']
        if old_pass and new_pass and re_pass:
            from page_account.routes.config import urepass
            return urepass(old_pass, new_pass, re_pass)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }
    return jsonify(response_for_client)


@bp_page_account.route('/cb_settings_ajax', methods=['POST', 'GET'])
def ucb_settings():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if request.method == "POST":
        json_ajax = request.get_json()
        cb_timeout = json_ajax['cb_timeout']

        if cb_timeout is not None and isinstance(cb_timeout, bool):
            from page_account.routes.config import ucb_settings
            return ucb_settings(cb_timeout)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }
    return jsonify(response_for_client)

