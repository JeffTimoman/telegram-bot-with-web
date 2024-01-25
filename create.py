import sys
from backend import app, db, bcrypt, config
from time import sleep
# python input password
from getpass import getpass
import re

from backend.models import User
def create_database():
    print("Creating database...")
    sleep(1)
    db.drop_all()
    db.create_all()
    print("Database created.")

def create_superuser():
    email = input("Email: ")
    password = getpass("Password: ")
    password_confirm = getpass("Confirm Password: ")
    name = "admin"

    check_email = User.query.filter_by(email = email).first()
    if check_email is not None:
        print("Email already exists.")
        sys.exit()
    # validate email regex
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email format.")
        sys.exit()
    
    # validate password
    if password != password_confirm:
        print("Password doesn't match.")
        sys.exit()
    
    # validate password length
    if len(password) < 8:
        print("Password must be at least 8 characters.")
        sys.exit()
        
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(name = name, email = email, password = hashed)
    db.session.add(user)
    db.session.commit()
    print("Super user created.")

def create_webvariables():
    print("Creating web variables...")
    sleep(1)
    from backend.models import WebVariables
    # Empty all data from web_variables table
    WebVariables.query.delete()
    db.session.commit()
    # Insert new data
    web_variables = [
        WebVariables(name="BROADCAST_KEY", value=config.BROADCAST_KEY),
    ]
    for variable in web_variables:
        db.session.add(variable)
    db.session.commit()
    
    print("Web variables created.")

def create_commands():
    print("Creating commands...")
    sleep(1)
    from backend.models import Command
    start_check, error_check = db.session.query(Command.keyword).filter(Command.keyword == 'start').first(), db.session.query(Command.keyword).filter(Command.keyword == 'error').first()
    
    
    if start_check is None:
        start = Command(code = 'start', keyword = 'start', message = 'Welcome to Telebot! Please type /help to see available commands.', expired_date = None)
        db.session.add(start)
        
    if error_check is None:
        error = Command(code = 'error', keyword = 'error', message = 'Sorry, I don\'t understand that command. Please type /help to see available commands.', expired_date = None)
        db.session.add(error)
        
    db.session.commit()
    print("Commands created.")
    
def main():
    if len(sys.argv) == 1:
        print("Usage: python create.py [create_database|create_superuser|create_webvariables|create_commands]")
        sys.exit()
    
    function_name = sys.argv[1]
    
    if function_name in globals():
        globals()[function_name]()
    else :
        print("Function doesn't exist.")
        
if __name__ == '__main__':
    with app.app_context():
        main()