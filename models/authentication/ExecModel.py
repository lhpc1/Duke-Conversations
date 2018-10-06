import sqlite3
from db import db

# Note we define database operations under the User class
class ExecModel(db.Model):
    # Defining the table used by SQLAlchemy
    __tablename__ = "executives"

    # Defining the columns -- properties -- of the table
    # SQL Alchemy will only look for these three properties when it saves to the db. They must match.
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80)) # The size of the username is limited to 80 characters maximum
    password = db.Column(db.String(80))


    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {"username":self.username, "password":self.password}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Retrieve a user object from the database via username
    @classmethod
    def findByUsername(cls, username):
        return cls.query.filter_by(username=username).first()

    # Return a user object from the db via the id
    @classmethod
    def findById(cls, _id):
        return cls.query.filter_by(id = _id).first()
