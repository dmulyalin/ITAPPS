# third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

# local imports
from config import app_config

login_manager = LoginManager()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config['development'])
app.config.from_pyfile('config.py')

Bootstrap(app)

# login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

from .home import home as home_blueprint
app.register_blueprint(home_blueprint)

from .devices import devices as devices_blueprint
app.register_blueprint(devices_blueprint)