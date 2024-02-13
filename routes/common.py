from __init__ import app
from flask import url_for


@app.route('/logo.ico')
def favicon():
    return url_for('static', filename='/img/logo.ico')

@app.route('/config_db.png')
def conf_db_png():
    return url_for('static', filename='/img/config_db.png')

# @app.errorhandler(404)
# def page_not_found(error_str):
#
#     return cpages.set_render_page(PAGE_ID.PAGE_NOT_FOUND)
