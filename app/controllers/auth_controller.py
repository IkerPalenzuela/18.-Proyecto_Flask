from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.services.user_service import UserService
from app.forms.login_form import LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('navigation.inicio'))
    form = LoginForm()

    if form.validate_on_submit():
        user = UserService.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user)
            return redirect(url_for('navigation.inicio'))
        
    return render_template('componentes/login_form.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('navigation.inicio'))