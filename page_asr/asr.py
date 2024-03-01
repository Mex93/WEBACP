from flask import Blueprint, request, jsonify

from captha_main import SIMPLE_CAPTCHA

from engine.debug.CDebug import CDebug
from engine.pages.CPages import CPages
from engine.pages.enums import PAGE_ID
from engine.users.CUser import CUser
from engine.users.CUserAccess import CUserAccess
from engine.common import get_checkbox_state

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
        return cpages.redirect_on_page(PAGE_ID.ASR_FIND)

    if request.method == 'GET':
        new_captcha_dict = SIMPLE_CAPTCHA.create()
        return cpages.set_render_page(PAGE_ID.ASR_FIND, captcha=new_captcha_dict)

    return cpages.set_render_page(PAGE_ID.ASR_FIND)
