from flask import Blueprint, request, url_for, render_template, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required

from backend import db, bcrypt, config
from backend.models import User, Command, ConnectedUser
from pytz import timezone
from datetime import datetime
from random import randint

import uuid as uuid
admin = Blueprint('admin', __name__)


@admin.route('/', methods=['GET', 'POST'])
@admin.route('/command', methods=['GET', 'POST'])
@login_required
def index():
    # Get the current time in the 'Asia/Jakarta' timezone
    jakarta_timezone = timezone(config.TIMEZONE)
    current_time = datetime.now(jakarta_timezone)

    # Retrieve active commands that have not expired yet
    active_commands = Command.query.filter((Command.expired_date > current_time) | (Command.expired_date == None)).all()
    inactive_commands = Command.query.filter((Command.expired_date <= current_time) & (Command.expired_date != None)).all()
    flash(f"Hi {current_user.name}! {config.RANDOM_GREETINGS[randint(0, len(config.RANDOM_GREETINGS) - 1)]}", 'success')
    return render_template('admin/index.html', active_commands=active_commands, inactive_commands=inactive_commands)

@admin.route('/add_command', methods=['GET', 'POST'])
@login_required
def add_command():
    if request.method == 'POST':
        # print(request.form)
        keyword = request.form.get('keyword')
        
        check_single_keyword = len(keyword.split(' ')) == 1
        if not check_single_keyword:
            flash('Keyword cannot contain spaces', 'danger')
            return render_template('admin/add_command.html', keyword=keyword)
        
        message = request.form.get('message')
        expired_date = request.form.get('expired_date')
        code = str(uuid.uuid4())
        
        check = Command.query.filter_by(keyword=keyword).first()
        if check:
            flash(f"Keyword '{keyword}' already exists or expired.", 'danger')
            return render_template('admin/add_command.html', keyword=keyword, message=message, expired_date=expired_date)
        if not expired_date:
            expired_date = None
            
        if len(message) == 0:
            flash('Message cannot be empty', 'danger')
            return render_template('admin/add_command.html', keyword=keyword, message=message, expired_date=expired_date)
        command = Command(code=code, message=message, expired_date=expired_date, keyword=keyword)
        db.session.add(command)
        db.session.commit()
        flash('Command added successfully', 'success')
        return redirect(url_for('admin.add_command'))
    return render_template('admin/add_command.html')

@admin.route("/edit_command/<string:code>", methods=['GET', 'POST'])
@login_required
def edit_command(code):
    command = Command.query.filter_by(code=code).first()
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        message = request.form.get('message')
        expired_date = request.form.get('expired_date')
        if keyword != command.keyword:
            check = Command.query.filter_by(keyword=keyword).first()
            if check:
                flash(f"Keyword '{keyword}' already exists or expired.", 'danger')
                return render_template('admin/edit_command.html', command=command, keyword=keyword, message=message, expired_date=expired_date)
            
        if keyword in config.RESERVED_KEYWORDS:
            expired_date = None
            
        if not expired_date:
            expired_date = None
        command.keyword = keyword
        
        if len(message) == 0:
            flash('Message cannot be empty', 'danger')
            return render_template('admin/edit_command.html', command=command, keyword=keyword, message=message, expired_date=expired_date)
        command.message = message
        command.expired_date = expired_date
        db.session.commit()
        flash('Command edited successfully', 'success')
        return redirect(url_for('admin.edit_command', code=code))
    return render_template('admin/edit_command.html', command=command)

@admin.route("/delete_command", methods=['GET', 'POST'])
@login_required
def delete_command():
    if request.method == 'POST':
        id = request.form.get('id')
        command = Command.query.filter_by(id=id).first()    
        if not command:
            flash('Command is not found.', 'danger')
            return redirect(url_for('admin.index'))
        
        if command.keyword in config.RESERVED_KEYWORDS:
            flash(f"You cannot delete reserved keyword. Keyword '{command.keyword}' must exist!", 'danger')
            return redirect(url_for('admin.index'))
        
        db.session.delete(command)
        db.session.commit()
        flash('Command is deleted successfully', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/delete_command.html', command=command)

@admin.route("/connected_user", methods=['GET', 'POST'])
@login_required
def connected_user():
    connected_users = ConnectedUser.query.all()
    return render_template('admin/connected_user.html', connected_users=connected_users)

@admin.route("/admins", methods=['GET', 'POST'])
@login_required
def admins():
    users = User.query.all()
    return render_template('admin/admins.html', users=users)

@admin.route("/add_admin", methods=['GET', 'POST'])
@login_required
def add_admin():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        check = User.query.filter_by(email=email).first()
        if check:
            flash(f"Email '{email}' already exists.", 'danger')
            return render_template('admin/add_admin.html', name=name, email=email)
        if len(password) == 0:
            flash('Password cannot be empty', 'danger')
            return render_template('admin/add_admin.html', name=name, email=email)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Admin added successfully', 'success')
        return redirect(url_for('admin.add_admin'))
    return render_template('admin/add_admin.html')

@admin.route("/edit_admin/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_admin(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        check = User.query.filter_by(email=email).first()
        if check and check.id != user.id:
            flash(f"Email '{email}' already exists.", 'danger')
            return render_template('admin/edit_admin.html', user=user, name=name, email=email)
        if len(password) == 0:
            flash('Password cannot be empty', 'danger')
            return render_template('admin/edit_admin.html', user=user, name=name, email=email)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.name = name
        user.email = email
        user.password = hashed_password
        db.session.commit()
        flash('Admin edited successfully', 'success')
        return redirect(url_for('admin.edit_admin', id=id))
    return render_template('admin/edit_admin.html', user=user)

@admin.route("/delete_admin", methods=['GET', 'POST'])
@login_required
def delete_admin():
    if request.method == 'POST':
        id = request.form.get('id')
        user = User.query.filter_by(id=id).first()
        if not user:
            flash('User is not found.', 'danger')
            return redirect(url_for('admin.admins'))
        
        if current_user == user:
            flash('You cannot delete yourself.', 'danger')
            return redirect(url_for('admin.admins'))
        db.session.delete(user)
        db.session.commit()
        flash('User is deleted successfully', 'success')
        return redirect(url_for('admin.admins'))

@admin.route('/add_admin', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        check = User.query.filter_by(email=email).first()
        if check:
            flash(f"Email '{email}' already exists.", 'danger')
            return render_template('admin/add_admin.html', name=name, email=email)
        
        if len(password) == 0:
            flash('Password cannot be empty', 'danger')
            return render_template('admin/add_admin.html', name=name, email=email)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Admin added successfully', 'success')
        return redirect(url_for('admin.add_admin'))
    return render_template('admin/add_admin.html')

@admin.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = str(request.form.get('old'))
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm')
        
        if not bcrypt.check_password_hash(current_user.password, old_password):
            flash('Old password is incorrect.', 'danger')
            return render_template('admin/change_password.html')
        if len(new_password) == 0:
            flash('New password cannot be empty', 'danger')
            return render_template('admin/change_password.html')
        if new_password != confirm_password:
            flash('New password and confirm password must be the same', 'danger')
            return render_template('admin/change_password.html')
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Password changed successfully', 'success')
        return redirect(url_for('admin.admins'))
    return render_template('admin/change_password.html')

@admin.route('/about_bot', methods=['GET', 'POST'])
@login_required
def about_bot():
    return render_template('admin/about_bot.html')

@admin.route('/delete_connected_user', methods=['GET', 'POST'])
@login_required
def delete_connected_user():
    if request.method == 'POST':
        id = request.form.get('id')
        connected_user = ConnectedUser.query.filter_by(id=id).first()
        if not connected_user:
            flash('Connected user is not found.', 'danger')
            return redirect(url_for('admin.connected_user'))
        db.session.delete(connected_user)
        db.session.commit()
        flash('Connected user is deleted successfully', 'success')
        return redirect(url_for('admin.connected_user'))
    return render_template('admin/delete_connected_user.html')