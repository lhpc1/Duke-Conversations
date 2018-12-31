# Importing the db object from the db.py file. The use of this object is what enables Flask-SQLAlchemy to
# made database operations.
from db import db

#The python datetime object lets us store information about a specific datetime in easily encodable and decodable object format.
from datetime import datetime

# This data model represents a student in memory. Information on each student who applies for a dinner is always stored and
# later referenced when a student tries to apply for a new dinner. Each student's memory is stored permanently
class StudentModel(db.Model):

    # Defining the schema for the table to store the db information.
    __tablename__ = "students"

    ##################################################################################################################
    ### MODEL PROPERTIES #############################################################################################
    ##################################################################################################################

    # Every student by default will be referenced by their netID, which will serve as their main unique identifier and
    # consequently the primary key
    netID = db.Column(db.String, primary_key= True)

    # Additionally, we will also be storing each student's unique Duke idea
    uniqueID = db.Column(db.String)

    # Storing the student's first and last names
    firstName = db.Column(db.String)

    lastName = db.Column(db.String)

    # Storing the student's phone number. This will be encoded by the front end into XXX-XXX-XXXX Format
    phoneNumber = db.Column(db.String)

    # The student's major will be stored as an integer on the backend with the frontend decoding each integer to a known
    # value. The use of an integer here is useful as there are only so many discretized majors and it's less memory intensive
    # to store individual numbers on the backend.
    major = db.Column(db.Integer)

    # Each student's gender pronouns will also be stored in the backend as an Integer which will be decoded on the frontend.
    genderPronouns = db.Column(db.Integer)

    # The student's graduation year will be stored with two integers (e.g. class of 2022 will just be 22). The numeric limit
    # will be enforced on the frontend.
    graduationYear = db.Column(db.Integer)

    # Here we store the total number of applications ever, number of selections ever as well as applications and selections in that semester.
    # A chron job will automatically go in and update the list at the end of a term.
    numberApplications = db.Column(db.Integer)

    numberSelections = db.Column(db.Integer)

    numberApplicationsSemester = db.Column(db.Integer)

    numberSelectionsSemester = db.Column(db.Integer)

    blackList = db.Column(db.Boolean)

    # FOREIGN KEY RELATIONSHIPS ######################################################################################

    # Here will be a list of associated applications which are taken by this student
    apps = db.relationship("ApplicationModel", lazy = "dynamic")

    ##################################################################################################################
    ### /MODEL PROPERTIES ############################################################################################
    ##################################################################################################################

    ##################################################################################################################
    ### MODEL METHODS ################################################################################################
    ##################################################################################################################

    # Constructing a new ProfessorModel object using passed properties for the arguments
    def __init__(self, netID, uniqueID, firstName, lastName, phoneNumber, major, genderPronouns, graduationYear):

        self.netID = netID
        self.uniqueID = uniqueID
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.major = major
        self.genderPronouns = genderPronouns
        self.graduationYear = graduationYear

        # By the default, on the creation of a new student, the number of applications and selections will automatically be 0
        self.numberApplications = 0
        self.numberSelections = 0
        self.numberApplicationsSemester = 0
        self.numberSelectionsSemester = 0

        self.blackList = False

    # Return a json representation of the object (note that this returns a dict since Flask automatically converts into json)
    def json(self):
        return {"netID": self.netID, "uniqueID":self.uniqueID, "firstName":self.firstName, "lastName":self.lastName, "phoneNumber": self.phoneNumber,
                "major": self.major, "genderPronouns": self.genderPronouns, "graduationYear": self.graduationYear, "numberApplications": self.numberApplications,
                "numberSelections": self.numberSelections, "numberApplicationsSemester": self.numberApplicationsSemester, "numberSelectionsSemester": self.numberSelectionsSemester}

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
    def find_by_id(cls,netID):
        found = cls.query.filter_by(netID = netID).first() # All ID numbers are unique so this should always return one object
        return found

    @classmethod
    def return_all(cls):
        allStudents = cls.query.all()
        allStudentsJSON = [student.json() for student in allStudents]
        return allStudentsJSON
