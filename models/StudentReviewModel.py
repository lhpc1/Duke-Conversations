# Importing the db object from the db.py file. The use of this object is what enables Flask-SQLAlchemy to
# made database operations.
from db import db

#The python datetime object lets us store information about a specific datetime in easily encodable and decodable object format.
from datetime import datetime

# This data model represents a student's review in memory. Information on each student who applies for a dinner is always stored and
# later referenced when a student tries to apply for a new dinner. Each student's memory is stored permanently
class StudentReviewModel(db.Model):

    # Defining the schema for the table to store the db information.
    __tablename__ = "student_reviews"

    ##################################################################################################################
    ### MODEL PROPERTIES #############################################################################################
    ##################################################################################################################

    # To make for easier indexing, each application will be given an associated number to serve as a primary keys
    id = db.Column(db.Integer, primary_key= True)

    # The timestamp records when the application was submitted. It is by default eqaul to the moment of the post request.
    timeStamp =  db.Column(db.DateTime, default=datetime.utcnow)

    # Rating of food out of 5
    foodRating = db.Column(db.Integer)

    # Rating of conversations out of 5
    conversationRating = db.Column(db.Integer)

    # Additional comments from the students
    comments = db.Column(db.String)

    # Every single review should have a student object associated in memory.
    studentID = db.Column(db.String, db.ForeignKey('students.netID'))
    student = db.relationship("StudentModel")

    # Every student object is also the child object of a dinner
    dinnerID = db.Column(db.Integer, db.ForeignKey("dinners.id"))
    dinner = db.relationship("DinnerModel")

    ##################################################################################################################
    ### /MODEL PROPERTIES ############################################################################################
    ##################################################################################################################

    ##################################################################################################################
    ### MODEL METHODS ################################################################################################
    ##################################################################################################################

    # Constructing a new ProfessorModel object using passed properties for the arguments
    def __init__(self, foodRating, conversationRating, comments, studentID, dinnerID):

        self.foodRating = foodRating
        self.conversationRating = conversationRating
        self.comments = comments
        self.studentID = studentID
        self.dinnerID = dinnerID


    # Return a json representation of the object (note that this returns a dict since Flask automatically converts into json)
    def json(self):
        return {"id":self.id, "timeStamp": str(self.timeStamp), "foodRating":self.foodRating, "conversationRating":self.conversationRating,
                "studentID":self.studentID, "dinnerID":self.dinnerID}

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
        objects = cls.query.all()
        allObjectsJSON = [object.json() for object in objects]
        return allObjectsJSON
