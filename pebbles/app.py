import sys
import os as os

from flask import Flask
from flask_migrate import upgrade as flask_upgrade_db_to_head
from flask_migrate import Migrate

from pebbles.models import db, bcrypt
from pebbles.config import BaseConfig, TestConfig

app = Flask(__name__, static_url_path='')
migrate = Migrate(app, db)


# Setup static files to be served by Flask for automated testing
@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


test_run = set(['test', 'covtest']).intersection(set(sys.argv))

if test_run:
    app.dynamic_config = TestConfig()
else:
    app.dynamic_config = BaseConfig()

app.config.from_object(app.dynamic_config)

if app.config['ENABLE_SHIBBOLETH_LOGIN']:
    SSO_ATTRIBUTE_MAP = {
        "HTTP_AJP_SHIB_MAIL": (True, "email_id"),
        "HTTP_AJP_SHIB_EPPN": (False, "eppn"),
        "HTTP_AJP_SHIB_NSACCOUNTLOCK": (False, "accountlock"),
        "HTTP_AJP_SHIB_VPPN": (False, "vppn"),
        "HTTP_AJP_SHIB_AUTHENTICATION_METHOD": (True, "authmethod"),
    }
    app.config.setdefault('SSO_ATTRIBUTE_MAP', SSO_ATTRIBUTE_MAP)
    app.config.setdefault('SSO_LOGIN_URL', '/login')
    app.config.setdefault('PREFERRED_URL_SCHEME', 'https')

bcrypt.init_app(app)
db.init_app(app)


def run_things_in_context(is_test_run):
    # This is only split into a function so we can easily test some of it's
    # behavior.
    with app.app_context():
        # upgrade to the head of the migration path (the default)
        # we might want to pass a particular revision id instead
        # in the future
        if os.environ.get("DB_AUTOMIGRATION", None) and \
           os.environ.get("DB_AUTOMIGRATION", None) not in ["0", 0] and \
           not is_test_run:
            flask_upgrade_db_to_head()


run_things_in_context(test_run)
