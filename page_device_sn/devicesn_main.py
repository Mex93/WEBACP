from flask import Blueprint, request, jsonify

from captha_main import SIMPLE_CAPTCHA
from engine.debug.CDebug import CDebug
from engine.pages.CPages import CPages
from engine.pages.enums import PAGE_ID
from engine.users.CUser import CUser
from engine.users.CUserAccess import CUserAccess
from engine.users.enums import USER_SECTIONS_TYPE, USER_SECTION_ACCESS_TYPE
from engine.devicesn.common import is_devicesn_valid
from engine.devicesn.common import is_cirylic

bp_page_devicesn = Blueprint('devicesn', __name__, template_folder='templates', static_folder='static')

cdebug = CDebug()
cdebug.debug_system_on(True)

cuser = CUser()
cuser_access = CUserAccess()
cpages = CPages(cdebug)

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.DEVICESN_FIND)


@bp_page_devicesn.route(f'/{page_name}', methods=['POST', 'GET'])
def dsn_find():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.SN) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == 'GET':
        new_captcha_dict = SIMPLE_CAPTCHA.create()

        return cpages.set_render_page(PAGE_ID.DEVICESN_FIND, captcha=new_captcha_dict)

    return cpages.set_render_page(PAGE_ID.DEVICESN_FIND)

@bp_page_devicesn.route('/dsn_find_ajax', methods=['POST', 'GET'])
def get_device_sn_data_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.SN) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_SN_EDIT) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        json_ajax = request.get_json()
        dsn_device = json_ajax.get('csn_device')

        c_hash = json_ajax.get('captcha_hash')
        c_text = json_ajax.get('captcha_text')

        if c_hash and c_text:
            if SIMPLE_CAPTCHA.verify(c_text, c_hash) is False:  # не забыть поправить на true
                if dsn_device and isinstance(dsn_device, str):
                    if is_devicesn_valid(dsn_device) and not is_cirylic(dsn_device):
                        from page_device_sn.routes.snfind import get_device_sn_data
                        return get_device_sn_data(dsn_device)
                    else:
                        response_for_client.update({"error_text": "Вы неверно ввели серийный номер/mac/sn mb!"})
                else:
                    response_for_client.update({"error_text": "Вы неверно ввели серийный номер/mac/sn mb!"})
            else:
                response_for_client.update({"error_text": "Вы неверно ввели капчу!"})
            new_captcha_dict = SIMPLE_CAPTCHA.create()
            response_for_client.update({"new_captha": SIMPLE_CAPTCHA.captcha_html(new_captcha_dict)})
        else:
            response_for_client.update({"error_text": "Вы не ввели капчу!"})

    return jsonify(response_for_client)


@bp_page_devicesn.route('/dsn_delete_sn_ajax', methods=['POST', 'GET'])
def delete_sn_ajax_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.SN) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_SN_DELETE) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        json_ajax = request.get_json()
        dsn_device = json_ajax.get('serial_number')
        dassy_id = json_ajax.get('assy_id')
        if dsn_device and isinstance(dsn_device, str) and isinstance(dassy_id, int) and dassy_id > 0:
            if is_devicesn_valid(dsn_device):
                from page_device_sn.routes.snfind import set_delete_sn_ajax_ajax
                return set_delete_sn_ajax_ajax(dsn_device, dassy_id)
            else:
                response_for_client.update({"error_text": "Вы неверно ввели серийный номер/mac/sn mb!"})
        else:
            response_for_client.update({"error_text": "Вы неверно ввели серийный номер/mac/sn mb!"})

    return jsonify(response_for_client)


@bp_page_devicesn.route('/dsn_save_edit_sn_ajax', methods=['POST', 'GET'])
def save_edit_sn_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.SN) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_SN_EDIT) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        json_ajax = request.get_json()
        dsn_device = json_ajax.get('serial_number')
        dassy_id = json_ajax.get('assy_id')
        arr = json_ajax.get('arr')

        if (dsn_device and isinstance(dsn_device, str) and
                isinstance(dassy_id, int) and dassy_id > 0 and
                isinstance(arr, list) and arr):
            if is_devicesn_valid(dsn_device):
                from page_device_sn.routes.snfind import set_save_edit_sn_ajax
                return set_save_edit_sn_ajax(dsn_device, dassy_id, arr)
            else:
                response_for_client.update({"error_text": "Вы неверно ввели серийный номер/mac/sn mb!"})
        else:
            response_for_client.update({"error_text": "Вы неверно ввели серийный номер/mac/sn mb!"})

    return jsonify(response_for_client)

