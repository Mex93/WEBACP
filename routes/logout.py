from __init__ import app, cpages, cuser_sessions, request

from engine.pages.enums import PAGE_ID

name = cpages.get_page_template_name_from_page_id(PAGE_ID.LOGOUT)


@app.route(f'/{name}')
def logout():
    # if cuser_sessions.is_sessions_start() is False:
    #     return cpages.redirect_on_page(PAGE_ID.LOGIN)

    return cpages.set_render_page(PAGE_ID.LOGOUT)
