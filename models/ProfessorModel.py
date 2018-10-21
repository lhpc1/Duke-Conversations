# Importing the db object from the db.py file. The use of this object is what enables Flask-SQLAlchemy to
# made database operations.
from db import db
#The python datetime object lets us store information about a specific datetime in easily encodable and decodable object format.
from datetime import datetime

# This data model represents one professor in memory including attributes such as gender pronouns, name, department, etc.
# Every Dinner in memory will have an associated Professor object as a foreign key.
class ProfessorModel(db.Model):

    # Defining the schema for the table to store the db information.
    __tablename__ = "professors"

    ##################################################################################################################
    ### MODEL PROPERTIES #############################################################################################
    ##################################################################################################################

    # id = db.Column(db.Integer, primary_key = True)
    # The uniqueID corresponds to each professor's uniqueID in the Duke OIT System and serves as the primary identification key.
    # This uniqueID will also serve as the foreign key to reference specific professors in the Dinner object.
    uniqueID = db.Column(db.String, primary_key = True)

    # The professor's first name
    firstName = db.Column(db.String)

    # The professor's last name
    lastName = db.Column(db.String)

    # The professor's gender pronouns. Gender pronouns are stored as integers and mapped on the front end
    genderPronouns = db.Column(db.Integer)

    # The professor's department stored as an int. Like gender pronouns, these will be mapped on the frontend into particular strings.
    department = db.Column(db.Integer)

    # Professor's title
    title = db.Column(db.String)

    # The number of dinners a professor has hosted
    dinnerCount = db.Column(db.Integer)

    # The school of the professor. 0 maps t Pratt, 1 maps to Trinity
    school = db.Column(db.Integer)

    # Here we define the child relationship of the dinner object. As one professor could have many dinners, it makes more sense to
    # define them like this.
    dinners = db.relationship("DinnerModel")

    ##################################################################################################################
    ### /MODEL PROPERTIES ############################################################################################
    ##################################################################################################################

    ##################################################################################################################
    ### MODEL METHODS ################################################################################################
    ##################################################################################################################

    # Constructing a new ProfessorModel object using passed properties for the arguments
    def __init__(self, uniqueID, firstName, lastName, genderPronouns, department, title, school):

        # Construcint a professor object using the passed arguments
        self.uniqueID = uniqueID
        self.firstName = firstName
        self.lastName = lastName
        self.genderPronouns = genderPronouns
        self.department = department
        self.title = title
        self.school = school

        # Upon the initilization of a new professor, the starting dinner count should be 0
        self.dinnerCount = 0

    # Return a json representation of the object (note that this returns a dict since Flask automatically converts into json)
    def json(self):
        return {"uniqueID": self.uniqueID, "firstName": self.firstName, "lastName": self.lastName, "genderPronouns": self.genderPronouns,
                "department": self.department, "title": self.title, "school": self.school, "dinnerCount": self.dinnerCount}

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
    def find_by_id(cls,uniqueID):
        foundProfessor = cls.query.filter_by(uniqueID = uniqueID).first() # All ID numbers are unique so this should always return one object
        return foundProfessor

    # A class method to query the profesors table and return all professors. Returns a list of items encoded into json-style dicts
    @classmethod
    def return_all_professors(cls):
        allProfessors = cls.query.all()
        allProfessorsJSON = [professor.json() for professor in allProfessors]
        return allProfessorsJSON

    @classmethod
    def return_last_item(cls):
        return db.session.query(cls).order_by(cls.uniqueID.desc()).first()
