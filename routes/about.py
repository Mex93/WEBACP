from __init__ import app, cpages
from engine.pages.enums import PAGE_ID

name = cpages.get_page_template_name_from_page_id(PAGE_ID.ABOUT)


@app.route(f'/{name}')
def about():
    return cpages.set_render_page(PAGE_ID.ABOUT)
