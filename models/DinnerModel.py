# Importing the db object from the db.py file. The use of this object is what enables Flask-SQLAlchemy to
# made database operations.
from db import db
from models.ProfessorModel import ProfessorModel

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

    # This is a boolean to see if catering was ordered yet.
    catering = db.Column(db.Boolean)

    # This is a boolean to see if transportation was ordered yet.
    transportation = db.Column(db.Boolean)

    # This float holds the cost of the entire dinner. This can be updated later, and is defaulted at 0.
    cost = db.Column(db.Float)

    # The short, one line topic of the dinner
    topic = db.Column(db.String)

    # A longer description of the topic
    description = db.Column(db.String)

    # The absolute max amount of students allowed to attend the dinner. This is specified by the professor
    studentLimit = db.Column(db.Integer)

    # The address of the dinner. Generally the professor's home.
    address = db.Column(db.String)

    # The dietary restrictions of this dinner. By default, this is set to none.
    dietaryRestrictions = db.Column(db.String)

    # TODO: Store path to a static directory to hold pictures of the dinner.

    # TODO: Implement a child relationship for professors.
    # Since the relationship is always one-to-one, the uselist parameter keeps the reference only as one object.
    professorID = db.Column(db.String, db.ForeignKey("professors.uniqueID"))
    professor = db.relationship("ProfessorModel")

    # TODO: Implement child relationship for applications
    applications = db.relationship("ApplicationModel", lazy = "dynamic")

    # TODO: Implement child relationship for student reviews

    # TODO: Implement child relationship for professor reviews


    ##################################################################################################################
    ### /MODEL PROPERTIES ############################################################################################
    ##################################################################################################################

    ##################################################################################################################
    ### MODEL METHODS ################################################################################################
    ##################################################################################################################

    # Constructing a new ProfessorModel object using passed properties for the arguments
    def __init__(self, timeStamp, topic, description, studentLimit, address, dietaryRestrictions, professorID):

        # Instantiating the basic information about the dinner
        self.timeStamp = timeStamp
        self.topic = topic
        self.description = description
        self.studentLimit = studentLimit
        self.address = address
        self.dietaryRestrictions = dietaryRestrictions
        self.professorID = professorID
        # Setting defaults
        self.invitationSentTimeStamp = "Not Sent"
        self.catering = False
        self.transportation = False


    # Return a json representation of the object (note that this returns a dict since Flask automatically converts into json)
    def json(self):
        applicationJSON = [app.json() for app in self.applications]
        return {"id": self.id, "timeStamp": self.timeStamp, "topic": self.topic, "description": self.description, "studentLimit": self.studentLimit,
                "address": self.address, "dietaryRestrictions":self.dietaryRestrictions, "invitationSentTimeStamp": self.invitationSentTimeStamp, "catering": self.catering,
                "transportation": self.transportation, "professorID": self.professorID, "professor":self.professor.json(),  "applications": applicationJSON }

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
    def return_all(cls):
        allDinners = cls.query.all()
        allDinnersJSON = [dinner.json() for dinner in allDinners]
        return allDinnersJSON

    @classmethod
    def return_all_objects(cls):
        allDinners = cls.query.all()
        return allDinners

    @classmethod
    def return_last_item(cls):
        return db.session.query(cls).order_by(cls.id.desc()).first()
