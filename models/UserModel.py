# This model, utilizing flask-login will enable session based authentitcation.
from db import db

class UserModel(db.Model):
    # The unique ID of the user
    __tablename__ = "users"

    id = db.Column( db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    email = db.Column(db.String(40))

    # 0 = Regular User; 1 = Admin; 2 = Super Admin
    role = db.Column(db.Integer)

    # Other information
    netID = db.Column(db.String)
    uniqueID = db.Column(db.String)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    phone = db.Column(db.String)
    major = db.Column(db.Integer)
    dinnerCount = db.Column(db.Integer)
    semDinnerCount = db.Column(db.Integer)
    emailText = db.Column(db.String)


    # Here we define the child relationship of the dinner object. As one user could have many dinners, it makes more sense to
    # define them like this.
    dinners = db.relationship("DinnerModel")

    def __init__(self, username, password, email, role, netID, uniqueID, firstName, lastName, phone, major, emailText):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

        # Instantiate non-authentication necessary information about the user
        self.netID = netID
        self.uniqueID = uniqueID
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.major = major
        self.emailText = emailText

        self.semDinnerCount = 0
        self.dinnerCount = 0

    # Return a json representation of the object (note that this returns a dict since Flask automatically converts into json)
    def json(self):
        dinnerJSON = [dinner.json() for dinner in self.dinners]
        return {"id":self.id,  "role":self.role, "email": self.email, "netID":self.netID,
        "uniqueID":self.uniqueID, "firstName":self.firstName, "lastName": self.lastName, "phone": self.phone,
        "major": self.major, "emailText": self.emailText, "semDinnerCount": self.semDinnerCount, "dinnerCount":self.dinnerCount, "dinners":dinnerJSON}

    def infojson(self):
        return {"id":self.id,  "role":self.role, "email": self.email, "netID":self.netID,
        "uniqueID":self.uniqueID, "firstName":self.firstName, "lastName": self.lastName, "phone": self.phone,
        "major": self.major, "emailText": self.emailText, "semDinnerCount": self.semDinnerCount, "dinnerCount":self.dinnerCount}
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
        found = cls.query.filter_by(username = username).first() # All usernames are unique so this should always return one object
        return found

    @classmethod
    def return_all(cls):
        allStudents = cls.query.all()
        allStudentsJSON = [student.json() for student in allStudents]
        return allStudentsJSON
