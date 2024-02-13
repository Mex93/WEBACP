from engine.pages.enums import PAGE_ID
from page_account.account import bp_page_account

from engine.pages.CPages import CPages
from engine.users.CUserSessions import CUserSessions
from engine.debug.CDebug import CDebug
from engine.users.CUser import CUser

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)
cuser_sessions = CUserSessions()
cuser = CUser()


def account_main():
    if cuser_sessions.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.LOGIN)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_MAIN)
