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
    return cpages.set_render_page(PAGE_ID.ABOUT)
