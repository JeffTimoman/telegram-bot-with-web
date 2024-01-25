from backend import db, bcrypt, config
from backend import login_manager
from flask_login import UserMixin
from pytz import timezone
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    last_ip = db.Column(db.String(100))
class Command(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(100), unique = True, nullable = False)
    keyword = db.Column(db.String(100), nullable = False, unique = True)
    message = db.Column(db.String(1000), nullable = False)
    expired_date = db.Column(db.Date)
    
    def __repr__(self):
        return f"Command('{self.message}', '{self.expired_date}')"
    
class ConnectedUser(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    chat_id = db.Column(db.String(100), nullable = False, unique = True)
    username = db.Column(db.String(100))
    date_connected = db.Column(db.DateTime, default = datetime.now(timezone(config.TIMEZONE)))
    
    def __repr__(self):
        return f"ConnectedUser('{self.user_id}', '{self.chat_id}')"

class WebVariables(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.String(1000))
