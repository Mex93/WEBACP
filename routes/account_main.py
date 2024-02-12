from __init__ import app, cpages, cuser_sessions
from engine.pages.enums import PAGE_ID

name = cpages.get_page_route_name_from_page_id(PAGE_ID.ACCOUNT_MAIN)


@app.route(f'/{name}')
def account_main():
    if cuser_sessions.is_sessions_start() is False:
        return cpages.redirect_on_page(PAGE_ID.LOGIN)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_MAIN)
