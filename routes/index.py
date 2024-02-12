from __init__ import app, cpages
from engine.pages.enums import PAGE_ID


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return cpages.set_render_page(PAGE_ID.INDEX)
