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

        vars_dict = {
            HTMLFieldsName.tv_field_asr_id: SQL_ASR_FIELDS.asr_fd_tv_asr_id,
            HTMLFieldsName.tv_field_asr_name: SQL_ASR_FIELDS.asr_fd_tv_asr,
            HTMLFieldsName.tv_field_tv_fk: SQL_ASR_FIELDS.asr_fd_tv_fk,
            HTMLFieldsName.tv_field_line_id: SQL_ASR_FIELDS.asr_fd_line_fk,
            HTMLFieldsName.tv_field_wf: SQL_ASR_FIELDS.asr_fd_wifi_module_sn,
            HTMLFieldsName.tv_field_bt: SQL_ASR_FIELDS.asr_fd_bt_module_sn,
            HTMLFieldsName.tv_field_mac: SQL_ASR_FIELDS.asr_fd_ethernet_mac,
            HTMLFieldsName.tv_field_panel: SQL_ASR_FIELDS.asr_fd_lcm_sn,
            HTMLFieldsName.tv_field_oc: SQL_ASR_FIELDS.asr_fd_oc_sn,
            HTMLFieldsName.tv_field_mb: SQL_ASR_FIELDS.asr_fd_mainboard_sn,
            HTMLFieldsName.tv_field_pb: SQL_ASR_FIELDS.asr_fd_powerboard_sn,
            HTMLFieldsName.tv_field_tcon: SQL_ASR_FIELDS.asr_fd_tcon_sn,
            HTMLFieldsName.tv_field_scan_date: SQL_ASR_FIELDS.asr_fd_timestamp_st10,
            HTMLFieldsName.tv_field_ops: SQL_ASR_FIELDS.asr_fd_ops_sn,
            HTMLFieldsName.tv_fild_model_name: SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_name,
            HTMLFieldsName.tv_fild_model_type_name: SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_tv_model_type_name,
            HTMLFieldsName.tv_fild_vendor_code: SQL_TV_MODEL_INFO_FIELDS.tvmi_fd_vendor_code,
        }
        return cpages.set_render_page(PAGE_ID.ASR_FIND, captcha=new_captcha_dict, vars_dict=vars_dict)

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
