# This model, utilizing flask-login will enable session based authentitcation.
from db import db
from flask_login import UserMixin

class UserModel(db.Model, UserMixin):
    # The unique ID of the user
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    email = db.Column(db.String(40))

    # 0 = Regular User; 1 = Admin; 2 = Super Admin
    role = db.Column(db.Integer)

    # Here we define the child relationship of the dinner object. As one user could have many dinners, it makes more sense to
    # define them like this.
    dinners = db.relationship("DinnerModel")

    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        if role is not 0 or 1 or 2:
            self.role = 0
        else:
            self.role = role

    # Return a json representation of the object (note that this returns a dict since Flask automatically converts into json)
    def json(self):
        dinnerJSON = [dinner.json() for dinner in self.dinners]
        return {"id":self.id, "username":self.username, "role":self.role, "email": self.email, "dinners":dinnerJSON}

    # Write this particular professor model instance to the DB. Note this also will automatically perform an update as well from a PUT request.
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Delete this profes from the db
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Find a professor via their unique ID. This will automatically return an object in place of a SQL row.
    @classmethod
    def find_by_id(cls,id):
        found = cls.query.filter_by(id = id).first() # All ID numbers are unique so this should always return one object
        return found

    @classmethod
    def find_by_username(cls,username):
        found = cls.query.filter_by(username = username).first() # All ID numbers are unique so this should always return one object
        return found

    @classmethod
    def return_all(cls):
        allStudents = cls.query.all()
        allStudentsJSON = [student.json() for student in allStudents]
        return allStudentsJSON
