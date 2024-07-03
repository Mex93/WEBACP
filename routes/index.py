from __init__ import app
from flask import render_template
from engine.pages.enums import PAGE_ID
from engine.pages.CPages import CPages
from engine.debug.CDebug import CDebug

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)

name = cpages.get_page_route_name_from_page_id(PAGE_ID.INDEX)


@app.route(f'/{name}')
@app.route('/')
@app.route('/home')
def index():
    CURRENT_YEAR = "2024"
    CURRENT_ADMIN_EMAIL = "ryazanov.n@tvkvant.ru"
    CURRENT_TEXT = ('<span class = "header">Панель управления базой данных сборочного производства</span><br><br>'
                    f'По всем интересующим вопросам обращайтесь на почту </span><span class = "email">{CURRENT_ADMIN_EMAIL}</span><br>')

    return cpages.set_render_page(PAGE_ID.ABOUT, year=CURRENT_YEAR, text_main=CURRENT_TEXT)
