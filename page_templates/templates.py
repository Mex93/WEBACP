from flask import Blueprint, request, jsonify

from captha_main import SIMPLE_CAPTCHA

from engine.debug.CDebug import CDebug
from engine.pages.CPages import CPages
from engine.pages.enums import PAGE_ID
from engine.users.CUser import CUser
from engine.users.CUserAccess import CUserAccess
from engine.common import get_checkbox_state
from engine.users.enums import USER_SECTIONS_TYPE, USER_SECTION_ACCESS_TYPE
from engine.users.enums import USER_ALEVEL
from engine.asr.CASR import CASR
from engine.sql.sql_data import SQL_ASR_FIELDS, SQL_TV_MODEL_INFO_FIELDS

from engine.asr.HTMLFieldsName import HTMLFieldsName
from engine.asr.enums import ASRFieldsType
from engine.asr.CASRFields import CASRFields, ASRFieldsType

bp_page_templates = Blueprint('templates', __name__, template_folder='templates', static_folder='static')

cdebug = CDebug()
cdebug.debug_system_on(True)

cuser = CUser()
cuser_access = CUserAccess()
cpages = CPages(cdebug)

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.TEMPLATES_FIND)


@bp_page_templates.route(f'/{page_name}', methods=['POST', 'GET'])
def asr_find():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.SCAN_TEMPLATES) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_SCAN_EDIT) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    return cpages.set_render_page(PAGE_ID.TEMPLATES_FIND)


@bp_page_templates.route('/templates_get_models_list_ajax', methods=['POST', 'GET'])
def get_tv_models_list():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.SCAN_TEMPLATES) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == "POST":
        from page_templates.routes.find import templates_get_models_list_ajax
        return templates_get_models_list_ajax()

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }
    return jsonify(response_for_client)


@bp_page_templates.route('/templates_edit_mask_ajax', methods=['POST', 'GET'])
def get_scan_model_params():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.SCAN_TEMPLATES) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_SCAN_EDIT) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == "POST":

        json_ajax = request.get_json()
        scan_fk = json_ajax.get('scan_fk', None)
        model_id = json_ajax.get('model_id', None)
        model_name = json_ajax.get('model_name', None)

        if None not in (scan_fk, model_id, model_name):
            if isinstance(scan_fk, int) and isinstance(model_id, int) and isinstance(model_name, str):
                from page_templates.routes.find import templates_get_edit_mask_ajax
                return templates_get_edit_mask_ajax(scan_fk, model_id, model_name)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }
    return jsonify(response_for_client)


@bp_page_templates.route('/templates_delete_model_ajax', methods=['POST', 'GET'])
def templates_delete_model():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.SCAN_TEMPLATES) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_SCAN_DELETE) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == "POST":

        json_ajax = request.get_json()
        scan_fk = json_ajax.get('scan_fk', None)
        model_id = json_ajax.get('model_id', None)
        model_name = json_ajax.get('model_name', None)

        if None not in (scan_fk, model_id, model_name):
            if isinstance(scan_fk, int) and isinstance(model_id, int) and isinstance(model_name, str):
                from page_templates.routes.find import templates_delete_mask_ajax
                return templates_delete_mask_ajax(scan_fk, model_id, model_name)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }
    return jsonify(response_for_client)