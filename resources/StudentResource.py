# This defines the Strain Resource that will be used for CRUD operations in the API

# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.StudentModel import StudentModel
from db import db

from flask_login import login_required


class StudentResource(Resource):

    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    # parser.add_argument("netID",
    #     type = str,
    #     required = True, # If there is no price argument, stop.
    #     help = "netID cannot be left blank"
    # )

    parser.add_argument("uniqueID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "UniqueID cannot be left blank"
    )

    parser.add_argument("firstName",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "First name cannot be left blank"
    )

    parser.add_argument("lastName",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Last Name cannot be left blank"
    )

    parser.add_argument("genderPronouns",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "Gender pronouncs cannot be left blank"
    )

    parser.add_argument("phoneNumber",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Phone Number cannot be left blank"
    )

    parser.add_argument("major",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "major cannot be left blank"
    )

    parser.add_argument("graduationYear",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "Grad year cannot be left blank"
    )

    def options (self):
        return {'Allow' : 'PUT' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET', \
          'Access-Control-Allow-Headers' : "Content-Type"}

    # GET a particular strain's information by id
    def get(self,netID):
        student = StudentModel.find_by_id(netID)
        if(student):
            return student.json(), 200, {"Access-Control-Allow-Origin":"*"}

        return {"message":"No student could be found with that ID"}, 500, {"Access-Control-Allow-Origin":"*"}

    # Allow for updates to professors
    def put(self, netID):

        data = StudentResource.parser.parse_args()

        if(StudentModel.find_by_id(netID)):
            studentOfInterest = StudentModel.find_by_id(netID)
            studentOfInterest.uniqueID = data["uniqueID"]
            studentOfInterest.firstName = data["firstName"]
            studentOfInterest.lastName = data["lastName"]
            studentOfInterest.genderPronouns = data["genderPronouns"]
            studentOfInterest.phoneNumber = data["phoneNumber"]
            studentOfInterest.major = data["major"]
            studentOfInterest.graduationYear = data["graduationYear"]
        else:
            studentOfInterest = StudentModel(**data)

        studentOfInterest.save_to_db()

        return StudentModel.find_by_id(netID).json(), 200, {"Access-Control-Allow-Origin":"*"}

    def delete(self,netID):

        if(StudentModel.find_by_id(netID)):
            StudentModel.find_by_id(netID).delete_from_db()
            return {"Message":"Student with id {} deleted.".format(netID)}, 500, {"Access-Control-Allow-Origin":"*"}

        return {"Message":"No student with {} found.".format(netID)}, 500, {"Access-Control-Allow-Origin":"*"}

# A resource to return all students
class StudentListResource(Resource):

    # Return all students in a json format
    def get(self):
        return StudentModel.return_all(), 200, {"Access-Control-Allow-Origin":"*"}

# A resource to register a new student
class StudentRegistrar(Resource):

    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    parser.add_argument("netID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "UniqueID cannot be left blank"
    )

    parser.add_argument("uniqueID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "UniqueID cannot be left blank"
    )

    parser.add_argument("firstName",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "First name cannot be left blank"
    )

    parser.add_argument("lastName",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Last Name cannot be left blank"
    )

    parser.add_argument("genderPronouns",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "Gender pronouncs cannot be left blank"
    )

    parser.add_argument("phoneNumber",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Phone Number cannot be left blank"
    )

    parser.add_argument("major",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "major cannot be left blank"
    )

    parser.add_argument("graduationYear",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "Grad year cannot be left blank"
    )

    def options (self):
        return {'Allow' : 'PUT' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET', \
          'Access-Control-Allow-Headers' : "Content-Type"}

    # Create a new strain, add it to the table
    def post(self):

        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = StudentRegistrar.parser.parse_args();

        # Error trapping to see if a professor already exists with that particular idea
        if(StudentModel.find_by_id(data.netID)):
            return {"Error":"A student with that net ID already exists"}, 400, {"Access-Control-Allow-Origin":"*"}

        # Create a new StudentModel object containing the passed properties.
        netStudent = StudentModel(**data) ## ** automatically separates dict keywords into arguments

        # Save the new professor to the database.
        netStudent.save_to_db()

        # Return the just posted student
        return StudentModel.find_by_id(data.netID).json(), 201, {"Access-Control-Allow-Origin":"*"}
