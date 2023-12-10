from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import os
from flask import send_file
from werkzeug.utils import secure_filename
from sqlalchemy import text

auth = Blueprint('auth', __name__)
# LFI vuln code
asset_folder = "templates"
@auth.route('/find_secret', methods=['GET', 'POST'])
def get_asset():

    asset_name = request.args.get('file')

    if not asset_name:
        return render_template("find_secret.html",user=current_user)
    return send_file(os.path.join(asset_folder, asset_name))



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = text("SELECT * FROM user WHERE email = '%s' AND password = '%s' "% (email,password))
        results = db.session.execute(query).all()
        if results:
            for result in results:
                flash('Logged in successfully!', category='success')
                user = User.query.filter_by(password=result.password).first()

                login_user(user, remember=True)

                return redirect(url_for('views.home'))
        else:
            flash('Incorrect password, try again.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    # bring the user back to the login page
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)