from __init__ import app, url_for


@app.route('/logo.ico')
def favicon():
    return url_for('static', filename='/static/img/logo.ico')

# @app.errorhandler(404)
# def page_not_found(error_str):
#
#     return cpages.set_render_page(PAGE_ID.PAGE_NOT_FOUND)
