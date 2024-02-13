from __init__ import app
from flask import render_template
from engine.pages.enums import PAGE_ID
from engine.pages.CPages import CPages
from engine.debug.CDebug import CDebug
from engine.users.CUserSessions import CUserSessions

cdebug = CDebug()
cdebug.debug_system_on(True)

cpages = CPages(cdebug)

name = cpages.get_page_route_name_from_page_id(PAGE_ID.INDEX)


@app.route(f'/{name}')
@app.route('/')
@app.route('/home')
def index():
    session_unit = CUserSessions()

    return render_template("index.html", session_start=session_unit.is_sessions_start())
# cpages.set_render_page(PAGE_ID.INDEX, session_unit=session_unit)