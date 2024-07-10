from flask import Blueprint, request, jsonify

from captha_main import SIMPLE_CAPTCHA
from engine.debug.CDebug import CDebug
from engine.pages.CPages import CPages
from engine.pages.enums import PAGE_ID
from engine.users.CUser import CUser
from engine.users.CUserAccess import CUserAccess
from engine.users.enums import USER_SECTIONS_TYPE, USER_SECTION_ACCESS_TYPE
from engine.pallets.common import is_palletsn_valid, is_devicesn_valid
from engine.pallets.common import is_cirylic

bp_page_pallets = Blueprint('pallets', __name__, template_folder='templates', static_folder='static')

cdebug = CDebug()
cdebug.debug_system_on(True)

cuser = CUser()
cuser_access = CUserAccess()
cpages = CPages(cdebug)

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.PALLETS_FIND)


@bp_page_pallets.route(f'/{page_name}', methods=['POST', 'GET'])
def pallets_main():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.PALLETS) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == 'GET':
        new_captcha_dict = SIMPLE_CAPTCHA.create()

        return cpages.set_render_page(PAGE_ID.PALLETS_FIND, captcha=new_captcha_dict)

    return cpages.set_render_page(PAGE_ID.PALLETS_FIND)


@bp_page_pallets.route('/pallet_find_data_ajax', methods=['POST', 'GET'])
def get_pallet_find_data_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.PALLETS) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_PALLET_FIND) is False:
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
                    if is_palletsn_valid(dsn_device) and not is_cirylic(dsn_device):
                        from page_pallets.routes.pallets_common import get_pallet_sn_data
                        return get_pallet_sn_data(dsn_device)
                    else:
                        response_for_client.update({"error_text": "Вы неверно ввели номер паллета/SN устройства!"})
                else:
                    response_for_client.update({"error_text": "Вы неверно ввели номер паллета/SN устройства!"})
            else:
                response_for_client.update({"error_text": "Вы неверно ввели капчу!"})
            new_captcha_dict = SIMPLE_CAPTCHA.create()
            response_for_client.update({"new_captha": SIMPLE_CAPTCHA.captcha_html(new_captcha_dict)})
        else:
            response_for_client.update({"error_text": "Вы не ввели капчу!"})

    return jsonify(response_for_client)

@bp_page_pallets.route('/pallet_delete_all_ajax', methods=['POST', 'GET'])
def pallet_delete_all_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.PALLETS) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_PALLET_DELETE_ALL) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        json_ajax = request.get_json()
        pallet_sn = json_ajax.get('pallet_sn')
        pallet_sql_id = int(json_ajax.get('pallet_sql_id'))

        if pallet_sn and isinstance(pallet_sn, str) and pallet_sql_id and isinstance(pallet_sql_id, int):
            if is_palletsn_valid(pallet_sn) and not is_cirylic(pallet_sn):
                from page_pallets.routes.pallets_common import set_pallet_delete_all_ajax
                return set_pallet_delete_all_ajax(pallet_sn, pallet_sql_id)
            else:
                response_for_client.update({"error_text": "Вы неверно ввели номер паллета/SN устройства!"})
        else:
            response_for_client.update({"error_text": "Вы неверно ввели номер паллета/SN устройства!"})

    return jsonify(response_for_client)

@bp_page_pallets.route('/pallet_add_device_ajax', methods=['POST', 'GET'])
def pallet_add_device_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.PALLETS) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_PALLET_ADD_TV) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        json_ajax = request.get_json()
        pallet_sn = json_ajax.get('pallet_sn')
        pallet_sql_id = int(json_ajax.get('pallet_sql_id'))
        device_sn = json_ajax.get('device_sn')

        if (pallet_sn and isinstance(pallet_sn, str) and
                pallet_sql_id and isinstance(pallet_sql_id, int) and
                device_sn and isinstance(device_sn, str)):
            if is_palletsn_valid(pallet_sn) and is_devicesn_valid(device_sn) and not is_cirylic(pallet_sn) and not is_cirylic(device_sn):
                from page_pallets.routes.pallets_common import set_pallet_add_device_ajax
                device_sn = device_sn.upper()
                return set_pallet_add_device_ajax(pallet_sn, pallet_sql_id, device_sn)
            else:
                response_for_client.update({"error_text": "Вы неверно ввели номер SN устройства!"})
        else:
            response_for_client.update({"error_text": "Вы неверно ввели номер SN устройства!"})

    return jsonify(response_for_client)

@bp_page_pallets.route('/pallet_delete_device_ajax', methods=['POST', 'GET'])
def pallet_delete_device_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.PALLETS) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_PALLET_DELETE_DEVICE) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        json_ajax = request.get_json()
        pallet_sn = json_ajax.get('pallet_sn')
        pallet_sql_id = int(json_ajax.get('pallet_sql_id'))
        device_sn = json_ajax.get('device_sn')
        device_assy = int(json_ajax.get('device_assy'))

        if (pallet_sn and isinstance(pallet_sn, str) and
                pallet_sql_id and isinstance(pallet_sql_id, int) and
                device_sn and isinstance(device_sn, str) and
                device_assy and isinstance(device_assy, int)):
            if is_palletsn_valid(pallet_sn) and is_devicesn_valid(device_sn) and not is_cirylic(pallet_sn) and not is_cirylic(device_sn):
                from page_pallets.routes.pallets_common import set_pallet_delete_device_ajax

                return set_pallet_delete_device_ajax(pallet_sn, pallet_sql_id, device_sn, device_assy)
            else:
                response_for_client.update({"error_text": "Ошибка номера SN устройства!"})
        else:
            response_for_client.update({"error_text": "Ошибка номера SN устройства!"})

    return jsonify(response_for_client)
