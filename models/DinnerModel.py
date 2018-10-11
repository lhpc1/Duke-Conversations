# Importing the db object from the db.py file. The use of this object is what enables Flask-SQLAlchemy to
# made database operations.
from db import db

#The python datetime object lets us store information about a specific datetime in easily encodable and decodable object format.
from datetime import datetime

# The DinnerModel is the most complex object in memory, from which all dinners are coordinated and managed. Every dinner has an associated
# professor as a child, as well as a list of applications as foreign-key children. Each application is additionally linked to a student
# in a 1-to-1 relationship. Through this, the dinner object essentially coordinates all other objects. Each dinner also has a child review
# objects.
class DinnerModel(db.Model):

    # Defining the schema for the table to store the db information.
    __tablename__ = "dinners"

    ##################################################################################################################
    ### MODEL PROPERTIES #############################################################################################
    ##################################################################################################################

    # Every dinner will have a unique id which will serve as its primary key.
    id = db.Column(db.Integer, primary_key = True)

    # This will store when the dinner will take place. This is currently being stored in a String for testing purposes,
    # but in the future, this will be translated into a python DateTime object. # TODO: Create method to auto-convert
    # UNIX to DateTime
    timeStamp = db.Column(db.String)

    # This will record the time when an invitation is sent out for a dinner. It is similarly encoded in a UNIX style timestamp.
    # TODO: Implement automatic datetime conversion. 
    invitationSentTimeStamp = db.Column(db.String)

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
