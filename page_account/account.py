from flask import Blueprint, request, jsonify

from captha_main import SIMPLE_CAPTCHA

from engine.debug.CDebug import CDebug
from engine.pages.CPages import CPages
from engine.pages.enums import PAGE_ID
from engine.users.CUser import CUser
from engine.users.CUserAccess import CUserAccess

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
        form_dict = request.form
        if form_dict.get('yes'):
            return logout()
        else:
            return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_LOGOUT)


####

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.ACCOUNT_LOGIN)


@bp_page_account.route(f'/{page_name}', methods=['POST', 'GET'])
def ulogin():
    if cuser_access.is_sessions_start() is True:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == 'GET':
        new_captcha_dict = SIMPLE_CAPTCHA.create()
        return cpages.set_render_page(PAGE_ID.ACCOUNT_LOGIN, captcha=new_captcha_dict)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_LOGIN)


@bp_page_account.route('/login_ajax', methods=['POST', 'GET'])
def login_ajax():
    if cuser_access.is_sessions_start() is True:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        json_ajax = request.get_json()
        password = json_ajax.get('cpassword')
        email = json_ajax.get('cnickname')
        savemy = json_ajax.get('csavemy')

        c_hash = json_ajax.get('captcha_hash')
        c_text = json_ajax.get('captcha_text')

        if c_hash and c_text:
            if SIMPLE_CAPTCHA.verify(c_text, c_hash):
                if password and email:
                    if isinstance(password, str) and isinstance(email, str):
                        from page_account.routes.login import ulogin
                        return ulogin(password, email, savemy)
            else:
                response_for_client.update({"error_text": "Вы неверно ввели капчу!"})
                new_captcha_dict = SIMPLE_CAPTCHA.create()

                response_for_client.update({"new_captha": SIMPLE_CAPTCHA.captcha_html(new_captcha_dict)})
        else:
            response_for_client.update({"error_text": "Вы не ввели капчу!"})

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

    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if request.method == 'GET':
        new_captcha_dict = SIMPLE_CAPTCHA.create()
        return cpages.set_render_page(PAGE_ID.ACCOUNT_CONFIG, captcha=new_captcha_dict)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_CONFIG)


@bp_page_account.route('/repass_ajax', methods=['POST', 'GET'])
def repass_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        json_ajax = request.get_json()
        if json_ajax is not None:
            old_pass = json_ajax.get('cold_pass')
            new_pass = json_ajax.get('cnew_pass')
            re_pass = json_ajax.get('cre_pass')

            c_hash = json_ajax.get('captcha_hash')
            c_text = json_ajax.get('captcha_text')
            if c_hash and c_text:
                if SIMPLE_CAPTCHA.verify(c_text, c_hash):
                    if old_pass and new_pass and re_pass:
                        if isinstance(old_pass, str) and isinstance(new_pass, str) and isinstance(re_pass, str):
                            from page_account.routes.config import urepass
                            return urepass(old_pass, new_pass, re_pass)
                else:
                    response_for_client.update({"error_text": "Вы неверно ввели капчу!"})
                    new_captcha_dict = SIMPLE_CAPTCHA.create()

                    response_for_client.update({"new_captha": SIMPLE_CAPTCHA.captcha_html(new_captcha_dict)})
            else:
                response_for_client.update({"error_text": "Вы не ввели капчу!"})

    return jsonify(response_for_client)


@bp_page_account.route('/cb_settings_ajax', methods=['POST', 'GET'])
def ucb_settings():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if request.method == "POST":
        json_ajax = request.get_json()
        cb_timeout = json_ajax.get('cb_timeout')

        if cb_timeout is not None and isinstance(cb_timeout, bool):
            from page_account.routes.config import ucb_settings
            return ucb_settings(cb_timeout)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }
    return jsonify(response_for_client)

