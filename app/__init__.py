# third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

# databases staff
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# local imports
from config import app_config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config['development'])
app.config.from_pyfile('config.py')

# init flask login
login_manager = LoginManager(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

# databses staff init
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app import models

# add Bootstrap support to app
Bootstrap(app)

from .home import home as home_blueprint
app.register_blueprint(home_blueprint)

from .devices import devices as devices_blueprint
app.register_blueprint(devices_blueprint)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .api import api as api_blueprint
app.register_blueprint(api_blueprint)

from .locations import locations as locations_blueprint
app.register_blueprint(locations_blueprint)