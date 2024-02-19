from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#db.Model is a blueprint of a database
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # getting the userid value from the user table. one-to-many relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    # define what we are going to store in the db
    id = db.Column(db.Integer, primary_key=True)
    # a user cannot register the same email twice and max length is 150 char
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # tell the sqlalchemy to capture the note data for the user
    notes = db.relationship('Note')


