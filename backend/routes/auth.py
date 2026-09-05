from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
import bcrypt
from models import AdminUser

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = AdminUser.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid email or password.', 'error')
    return render_template('admin/login.html')


@auth_bp.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
