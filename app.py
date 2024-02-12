from __init__ import app

import routes.index
import routes.account_config
import routes.account_main
import routes.login
import routes.logout
import routes.about
import routes.common


if __name__ == "__main__":
    app.run(debug=True)
