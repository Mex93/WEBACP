from __init__ import app, cpages
from engine.pages.enums import PAGE_ID

name = cpages.get_page_route_name_from_page_id(PAGE_ID.INDEX)


@app.route(f'/{name}')
@app.route('/')
@app.route('/home')
def index():
    return cpages.set_render_page(PAGE_ID.INDEX)
