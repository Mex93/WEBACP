from __init__ import app, csrf

import routes.index
import routes.about


if __name__ == "__main__":
    app.run(debug=True)
    csrf.init_app(app)
