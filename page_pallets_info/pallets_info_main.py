from flask import Blueprint, request, jsonify

from engine.debug.CDebug import CDebug
from engine.pages.CPages import CPages
from engine.pages.enums import PAGE_ID
from engine.pallets.common import is_palletsn_valid
from engine.pallets.common import is_cirylic

bp_page_pallets_info = Blueprint('ex', __name__, template_folder='templates', static_folder='static')

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.PALLETS_INFO)


@bp_page_pallets_info.route(f'/{page_name}', methods=['POST', 'GET'])
def pallets_main():

    return cpages.set_render_page(PAGE_ID.PALLETS_INFO)


@bp_page_pallets_info.route('/pallet_find_info_data_ajax', methods=['POST', 'GET'])
def get_pallet_find_info_data_ajax():

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }
    if request.method == "POST":
        json_ajax = request.get_json()
        dsn_device = json_ajax.get('csn_device')

        if dsn_device and isinstance(dsn_device, str):
            if is_palletsn_valid(dsn_device) and not is_cirylic(dsn_device):
                from page_pallets_info.routes.pallets_common import get_pallet_info_sn_data
                return get_pallet_info_sn_data(dsn_device)
            else:
                response_for_client.update({"error_text": "Вы неверно ввели номер паллета/SN устройства!"})
        else:
            response_for_client.update({"error_text": "Вы неверно ввели номер паллета/SN устройства!"})

    return jsonify(response_for_client)

