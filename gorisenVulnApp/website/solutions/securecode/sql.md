## vuln code:
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



## secure code
## use a parameterized statement for sql alchemy

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = text("SELECT * FROM user WHERE email = :email AND password = :password")
        results = db.session.execute(query,{"email": email, "password": password}).all()

        if results:
                for result in results:

                    flash('Logged in successfully!', category='success')
                    user = User.query.filter_by(password=result.password).first()


                    login_user(user, remember=True)

                    return redirect(url_for('views.home'))
        else:
            flash('Incorrect password, try again.', category='error')


    return render_template("login.html", user=current_user)