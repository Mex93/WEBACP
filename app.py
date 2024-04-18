from __init__ import app, csrf

import routes.index
import routes.about
import routes.common
from captha_main import *

if __name__ == "__main__":
    csrf.init_app(app)
    SIMPLE_CAPTCHA.init_app(app)

    app.run(port=4444, debug=True)
