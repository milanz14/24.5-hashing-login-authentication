from flask import Flask, flash, redirect, render_template, session
from models import User, db, connect_db
from forms import RegisterForm, LoginForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///loggingdb'
app.config['SECRET_KEY'] = 'development_key'

connect_db(app)

@app.route('/')
def show_register():
    """ redirect the user to the register page """
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def user_registration_route():
    """ route to support user registration """
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        try:
            new_user = User.register(username=username, password=password, email=email, firstname=firstname, lastname=lastname)
            db.session.add(new_user)
            db.session.commit()
        except:
            flash('Something went wrong')
            return redirect('/register')
        session['username'] = username
        flash(f'Welcome, {username}!')
        return redirect('/secret')
    else:
        return render_template('register.html', form=form)

@app.route('/secret')
def show_secret_route():
    """ show the secret route once a user is registered and
    stored in session """
    if 'username' not in session:
        flash('You must be logged in to see this.')
        return redirect('/login')
    else:
        return render_template('secret.html')

@app.route('/login', methods=['GET','POST'])
def login_user():
    """ log user in """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.date
        password = form.password.data
        #authenticate with User model classmethod
        user = User.authenticate(username, password)
        if user:
            session['username'] = username
            flash(f'Welcome back, {username}!')
            return redirect('/secret')
        else:
            form.username.errors = ['Bad password or Incorrect username']
    else:
        return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    """ log out user and redirect to '/' """
    session.pop('username')
    flash('Successfully logged out!')
    return redirect('/')