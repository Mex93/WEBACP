from flask import Blueprint, request, jsonify

from engine.debug.CDebug import CDebug
from engine.pages.CPages import CPages
from engine.pages.enums import PAGE_ID
from engine.users.CUser import CUser
from engine.users.CUserAccess import CUserAccess
from engine.users.enums import USER_SECTIONS_TYPE, USER_SECTION_ACCESS_TYPE

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


    return cpages.set_render_page(PAGE_ID.DEVICESN_FIND)

#
# @bp_page_devicesn.route('/templates_get_models_list_ajax', methods=['POST', 'GET'])
# def get_tv_models_list():
#     if cuser_access.is_sessions_start() is False:
#         return cpages.redirect_on_page(PAGE_ID.ACCOUNT_LOGIN)
#
#     if cuser_access.is_avalible_any_access_field(USER_SECTION_ACCESS_TYPE.SCAN_TEMPLATES) is False:
#         return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)
#
#     if request.method == "POST":
#         from page_templates.routes.common import templates_get_models_list_ajax
#         return templates_get_models_list_ajax()
#
#     response_for_client = {
#         "error_text": "Error query Type",
#         "result": False
#     }
#     return jsonify(response_for_client)
