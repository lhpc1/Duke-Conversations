
# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.ApplicationModel import ApplicationModel
from models.StudentModel import StudentModel
from models.DinnerModel import DinnerModel
from db import db

# A resource to register a new student
class WebhooksTest(Resource):

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
        return {'Allow' : 'PUT, POST' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET', \
          'Access-Control-Allow-Headers' : "Content-Type"}

    # Create a new strain, add it to the table
    def post(self):

        # # Acquire all of the data in a dict of each argument defined in the parser above.
        # data = StudentRegistrar.parser.parse_args();
        #
        # # Error trapping to see if a professor already exists with that particular idea
        # if(StudentModel.find_by_id(data.netID)):
        #     return {"Error":"A student with that net ID already exists"}, 400, {"Access-Control-Allow-Origin":"*"}
        #
        # # Create a new StudentModel object containing the passed properties.
        # netStudent = StudentModel(**data) ## ** automatically separates dict keywords into arguments
        #
        # # Save the new professor to the database.
        # netStudent.save_to_db()

        # Return the just posted student
        return {"message": "Data successfully posted <3"}, 200, {"Access-Control-Allow-Origin":"*"}
