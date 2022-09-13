from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user
from .mailgun import sign_up_email

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            flash('Incorrect password, try again.', category='danger')
        else:
            flash('Email does not exist.', category='danger')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    flash('Logged out!', category='success')
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='danger')
            redirect(url_for('auth.login'))
        elif password1 != password2:
            flash('Passwords do not match', category='danger')
        else:
            new_user = User(email=email,
                            first_name=first_name,
                            last_name=last_name,
                            password=generate_password_hash(password1, method="sha256")
                            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            sign_up_email(current_user)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)
