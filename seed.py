from models import db
from app import app

#create all tables - must initialize before being able to add users to DB

db.drop_all()
db.create_all()
