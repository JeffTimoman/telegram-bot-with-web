from flask import Blueprint, request, url_for, render_template, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required


from backend import bcrypt, db
# from backend.main.forms import LoginForm
from backend.models import User

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/login', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    
    if request.method == 'POST':
        next = request.args.get('next')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('You have been logged in!', 'success')
            user.last_ip = request.remote_addr
            db.session.commit()
            if next : 
                return redirect(next)
            return redirect(url_for('admin.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('main/index.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('main.index'))




















# @main.route('/dummy_user')
# def ud():
#     hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
#     u = User(name='admin', email="admin@admin.com", password=hashed_password)
#     db.session.add(u)
#     db.session.commit()
#     return 'Dummy user created'