from __init__ import app, cpages
from engine.pages.enums import PAGE_ID

name = cpages.get_page_template_name_from_page_id(PAGE_ID.ACCOUNT_CONFIG)


@app.route(f'/{name}')
def account_config():
    # if cuser_sessions.is_sessions_start() is False:
    # return cpages.redirect_on_page(PAGE_ID.LOGIN)

    return cpages.set_render_page(PAGE_ID.ACCOUNT_CONFIG)
