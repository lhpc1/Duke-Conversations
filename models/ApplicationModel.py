# Importing the db object from the db.py file. The use of this object is what enables Flask-SQLAlchemy to
# made database operations.
from db import db
#The python datetime object lets us store information about a specific datetime in easily encodable and decodable object format.
from datetime import datetime

# This data model represents one application for a particular dinner in memory. Every application object is the subobject of a dinner object
# in memory in a one-to-many relationship. Each application is also associated with a student in a one-to-one relationship.
class ApplicationModel(db.Model):

    # Defining the schema for the table to store the db information.
    __tablename__ = "applications"

    ##################################################################################################################
    ### MODEL PROPERTIES #############################################################################################
    ##################################################################################################################

    # To make for easier indexing, each application will be given an associated number to serve as a primary keys
    id = db.Column(db.Integer, primary_key= True)

    # The timestamp records when the application was submitted. It is by default eqaul to the moment of the post request.
    timeStamp =  db.Column(db.DateTime, default=datetime.utcnow)

    # The status stores in memory the current state of the application. 0 means it is pending, 1 indicates it was accepted,
    # 2 means denied, and 3 means waitlisted.
    status = db.Column(db.Integer)

    # The interest is a 100 word limited string where the applicant expresses their interest in coming to this particular dinner.
    # The word count is enforced on the frontend.
    interest = db.Column(db.String)

    # The "confirmed" status is a boolean indicating whether the applicant, after being accepted, confirmed they were coming to the
    # dinners
    confirmed = db.Column(db.Boolean)

    # The "present" status a boolean indicating whether the applicant actually showed up at the dinner. Its value is automatically
    # set to false and is updated by a Duke Convos staff member at the time of the dinner.
    present = db.Column(db.Boolean)

    # Every single application should have a student object associated in memory.
    studentID = db.Column(db.String, db.ForeignKey('students.netID'))
    student = db.relationship("StudentModel")

    # Every student object is also the child object of a dinner
    dinnerID = db.Column(db.String, db.ForeignKey("dinners.id"))
    dinner = db.relationship("DinnerModel")

    ##################################################################################################################
    ### /MODEL PROPERTIES ############################################################################################
    ##################################################################################################################

    ##################################################################################################################
    ### MODEL METHODS ################################################################################################
    ##################################################################################################################

    # Constructing a new ProfessorModel object using passed properties for the arguments
    def __init__(self, interest, studentID, dinnerID):

        # By default, the status is initially set on creation to be pending. The student is also not automatically confirmed or
        # marked present for similar reasons.
        self.status = 0
        self.interest = False
        self.present = False
        self.confirmed = False

        # The interst value is dynamically given by the user
        self.interest = interest
        self.studentID = studentID
        self.dinnerID = dinnerID

    # Return a json representation of the object (note that this returns a dict since Flask automatically converts into json)
    def json(self):
        return {"id":self.id, "timeStamp": str(self.timeStamp), "status":self.status, "interest":self.interest, "confirmed":self.confirmed, "present":self.present, "studentID": self.studentID, "student":self.student.json(),
        "dinnerID": self.dinnerID}

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
    def return_last_item(cls):
        return db.session.query(cls).order_by(cls.id.desc()).first()
