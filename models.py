from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User model for registration purposes """
    __tablename__ = 'users'
    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, pwd):
        """ Register user with hashed password & return user """
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode('utf8')

        # return instance of user w username and hashed pwd
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """ check if the user requesting authentication is valid
        Return user if valid; else return false """

        #find the user in the database
        u = User.query.filter_by(username=username).first()

        #if the user exists and the password hash check passes:
        # compares database password and hash result of passed in password
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
