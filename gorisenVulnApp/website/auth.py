import subprocess

from flask import Blueprint, render_template, request, flash, redirect, url_for, render_template_string
from .models import User
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import os
from flask import send_file
from sqlalchemy import text
import glob, random

auth = Blueprint('auth', __name__)
# LFI vuln code
asset_folder = "templates"



@auth.route('/find_secret', methods=['GET', 'POST'])
def get_asset():

    asset_name = request.args.get('file')

    if not asset_name:
        return render_template("find_secret.html",user=current_user)
    try:
        return send_file(os.path.join(asset_folder, asset_name))
    except:
        return render_template_string("""
    <h2 style="background-color:powderblue;">
    404 page not found: 
    </h2> 
  <h3>
  the 
   '""" + asset_name + """' resource does not exist! 
  </h3>""", user=current_user), 404


@auth.route("/ping", methods=['GET', 'POST'])
def page():
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        cmd = 'ping ' + hostname
        return subprocess.check_output(cmd, shell=True)
    else:
        return render_template("ping.html", user=current_user)



def chooseRandomImage(directory="website/static"):
    imgExtension = ["png", "jpeg", "jpg"]  # Image Extensions to be chosen from
    allImages = list()

    for img in os.listdir(directory): #Lists all files
        ext = img.split(".")[len(img.split(".")) - 1]
        if (ext in imgExtension):
            allImages.append(img)
    choice = random.randint(0, len(allImages) - 1)
    chosenImage = allImages[choice] #Do Whatever you want with the image file
    return chosenImage
@auth.route("/pickPartner", methods=['GET', 'POST'])

def partner():
    random_image = chooseRandomImage()
    print(random_image)
    if request.method == 'POST':
        buddy = request.form.get('buddy')
        return render_template("pickPartner.html",user=current_user, buddy=buddy, random_image=random_image)
    else:
        buddy = request.args.get('buddy')
        return render_template("pickPartner.html",user=current_user, buddy=buddy, random_image=random_image)






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