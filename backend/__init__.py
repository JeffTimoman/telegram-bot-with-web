from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from backend.config import Config

config = Config()
app = Flask(__name__)
app.config.from_object(Config())

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.login_view = 'main.index'
login_manager.login_message_category = 'info'
login_manager.init_app(app)


from backend.main.routes import main
from backend.admin.routes import admin
from backend.api.routes import api
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')