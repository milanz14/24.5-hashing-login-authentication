from flask import Flask, flash, redirect, render_template
from models import User, db, connect_db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///loggingdb'
app.config['SECRET_KEY'] = 'development_key'

connect_db(app)

@app.route('/')
def show_register():
    """ redirect the user to the register page """
    return render_template('register.html')