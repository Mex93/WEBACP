from __init__ import app, cpages, cuser_sessions, request

from engine.pages.enums import PAGE_ID
from engine.common import get_checkbox_state
from engine.pages.login import login_actions as login

name = cpages.get_page_route_name_from_page_id(PAGE_ID.LOGIN)


@app.route(f'/{name}', methods=['POST', 'GET'])
def ulogin():
    if cuser_sessions.is_sessions_start() is True:
        return cpages.redirect_on_page(PAGE_ID.ACCOUNT_MAIN)

    if request.method == 'POST':
        # получаем данные от кнопок и полей
        user_name = request.form['user_name']
        user_pass = request.form['user_pass']
        user_save_me = get_checkbox_state(request.form.get('user_save_me'))

        print(user_name)
        print(user_pass)
        print(user_save_me)
        result = login.set_login(user_name, user_pass, bool(user_save_me))
        print(result)
        if isinstance(result, tuple):
            error_text = result[1]
            return cpages.set_render_page(PAGE_ID.LOGIN, errors=error_text)
            # cpages.set_render_page(PAGE_ID.LOGIN, errors=error_text)
            # render_template("login.html", errors=error_text)

    return cpages.set_render_page(PAGE_ID.LOGIN)
