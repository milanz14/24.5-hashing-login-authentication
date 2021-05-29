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
        return redirect('/users')
    else:
        return render_template('register.html', form=form)

@app.route('/users/<username>')
def show_secret_route(username):
    """ show the secret route once a user is registered and
    stored in session """
    user = User.query.filter_by(username=username).first()
    # need to add the Feedback query here to find feedback tied to the logged in user
    if 'username' not in session:
        flash('You must be logged in to see this.')
        return redirect('/login')
    else:
        return render_template('userinfo.html', user=user)

@app.route('/users/<username>/feedback/add')
def show_activer_user_feedback(username):
    user = User.query.filter_by(username=username).first()
    if 'username' not in session:
        flash('You must be logged in to perform this action.')
        return redirect('/login')
    else:
        return render_template('addfeedback.html', user=user)

@app.route('/users/<username>/delete', methods=['DELETE'])
def delete_user(username):
    """ delete the user and the feedback tied to the user """
    pass

@app.route('/feedback/<int:feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    """ GET feedback form if it's the logged in user
    and UPDATE via POST if the logged in user wrote the feedback """
    pass

@app.route('/feedback/<int:feedback_id>/delete', methods=['DELETE'])
def delete_specific_feedback(feedback_id):
    """ delete a specific piece of feedback if logged in user wrote it """
    pass


@app.route('/login', methods=['GET','POST'])
def login_user():
    """ log user in """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        #authenticate with User model classmethod
        user = User.authenticate(username, password)
        if user:
            session['username'] = username
            flash(f'Welcome back, {username}!')
            return redirect(f'/users/{username}')
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