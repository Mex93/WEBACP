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

bp_page_asr = Blueprint('asr', __name__, template_folder='templates', static_folder='static')

cdebug = CDebug()
cdebug.debug_system_on(True)

cuser = CUser()
cuser_access = CUserAccess()
cpages = CPages(cdebug)

page_name = cpages.get_page_template_name_from_page_id(PAGE_ID.ASR_FIND)


@bp_page_asr.route(f'/{page_name}', methods=['POST', 'GET'])
def asr_find():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.ASR) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == 'GET':
        new_captcha_dict = SIMPLE_CAPTCHA.create()

        return cpages.set_render_page(PAGE_ID.ASR_FIND, captcha=new_captcha_dict)

    return cpages.set_render_page(PAGE_ID.ASR_FIND)


########################################
@bp_page_asr.route('/asr_find_ajax', methods=['POST', 'GET'])
def asr_find_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.ASR) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        json_ajax = request.get_json()
        asr_name = json_ajax.get('casrname')

        c_hash = json_ajax.get('captcha_hash')
        c_text = json_ajax.get('captcha_text')

        if c_hash and c_text:
            if SIMPLE_CAPTCHA.verify(c_text, c_hash) is False:  # не забыть поправить на true
                if asr_name:
                    if isinstance(asr_name, str):
                        if CASR.check_asr_text(asr_name):
                            from page_asr.routes.find import asr_find_ajax
                            return asr_find_ajax(asr_name)
                        else:
                            response_for_client.update({"error_text": "Ошибка в названии ASR"})
            else:
                response_for_client.update({"error_text": "Вы неверно ввели капчу!"})
                new_captcha_dict = SIMPLE_CAPTCHA.create()

                response_for_client.update({"new_captha": SIMPLE_CAPTCHA.captcha_html(new_captcha_dict)})
        else:
            response_for_client.update({"error_text": "Вы не ввели капчу!"})

    return jsonify(response_for_client)


@bp_page_asr.route('/asr_del_ajax', methods=['POST', 'GET'])
def asr_del_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.ASR) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_ASR_DELETE) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        json_ajax = request.get_json()
        asr_name = json_ajax.get('casrname')
        asr_id = json_ajax.get('cassyid')

        if asr_name and asr_id:
            if isinstance(asr_name, str):
                if CASR.check_asr_text(asr_name):
                    from page_asr.routes.find import asr_del_ajax
                    return asr_del_ajax(asr_name, asr_id)
                else:
                    response_for_client.update({"error_text": "Ошибка в названии ASR"})

    return jsonify(response_for_client)

@bp_page_asr.route('/asr_load_assoc_ajax', methods=['POST', 'GET'])
def asr_load_assoc_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.ASR) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        asr_unit = CASRFields()
        assoc_tup = asr_unit.get_assoc_tuple()
        response_for_client.update({"assoc_tup": assoc_tup})
        response_for_client.update({"result": True})

    return jsonify(response_for_client)


@bp_page_asr.route('/asr_replace_ajax', methods=['POST', 'GET'])
def asr_replace_ajax():
    if cuser_access.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)

    if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.ASR) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if cuser_access.is_access_for_panel(USER_SECTIONS_TYPE.ACCESS_ASR_EDIT) is False:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    response_for_client = {
        "error_text": "Error query Type",
        "result": False
    }

    if request.method == "POST":
        json_ajax = request.get_json()
        asr_name = json_ajax.get('casrname')
        asr_id = json_ajax.get('cassyid')
        edit_list = json_ajax.get('editarray')
        # edit_dict
        if asr_name and asr_id and edit_list:
            if isinstance(asr_name, str) and isinstance(edit_list, list):
                if CASR.check_asr_text(asr_name):
                    from page_asr.routes.find import asr_replace_ajax
                    # response_for_client.update({"result": True})
                    # response_for_client.update({"error_text": "Заебись"})
                    # return jsonify(response_for_client)
                    return asr_replace_ajax(asr_name, asr_id, edit_list)
                else:
                    response_for_client.update({"error_text": "Ошибка в названии ASR"})
            else:
                response_for_client.update({"error_text": "Ошибка в параметрах ASR"})

    return jsonify(response_for_client)
