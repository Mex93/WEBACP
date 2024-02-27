from __init__ import app
from engine.pages.enums import PAGE_ID
from engine.pages.CPages import CPages
from engine.debug.CDebug import CDebug

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)

name = cpages.get_page_route_name_from_page_id(PAGE_ID.ABOUT)

@app.route(f'/{name}')
def about():
    CURRENT_YEAR = "2024"
    CURRENT_ADMIN_EMAIL = "ryazanov.n@tvkvant.ru"
    CURRENT_TEXT = ('<span class = "header">Сайт для редактирования базы данных сборочного производства.</span><br><br>'
                    '<span class = "text">Все права принадлежат ООО Квант.<br>'
                    'Разработчик: Рязанов НВ<br>'
                    f'По всем интересующим вопросам пишите на почту </span><span class = "email">{CURRENT_ADMIN_EMAIL}</span><br>')

    return cpages.set_render_page(PAGE_ID.ABOUT, year=CURRENT_YEAR, text_main=CURRENT_TEXT)
