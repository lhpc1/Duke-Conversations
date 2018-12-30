# This defines the Strain Resource that will be used for CRUD operations in the API

# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.ApplicationModel import ApplicationModel
from models.StudentModel import StudentModel
from models.DinnerModel import DinnerModel
from db import db

class ApplicationResource(Resource):

    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    parser.add_argument("interest",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "interest cannot be left blank"
    )

    parser.add_argument("studentID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Student ID cannot be left blank"
    )

    parser.add_argument("dinnerID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Dinner ID cannot be left blank"
    )

    parser.add_argument("status",
        type = bool,
        required = True, # If there is no price argument, stop.
        help = "Dinner ID cannot be left blank"
    )

    parser.add_argument("present",
        type = bool,
        required = True, # If there is no price argument, stop.
        help = "Dinner ID cannot be left blank"
    )

    parser.add_argument("confirmed",
        type = bool,
        required = True, # If there is no price argument, stop.
        help = "Dinner ID cannot be left blank"
    )

    def options (self):
        return {'Allow' : 'PUT, POST' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET, POST', \
          'Access-Control-Allow-Headers' : "Content-Type"}

    # GET a particular strain's information by id
    def get(self,id):
        application = ApplicationModel.find_by_id(id)
        if(application):
            return application.json(), 200,{"Access-Control-Allow-Origin":"*"}

        return {"message":"No application could be found with that ID"}, 404, {"Access-Control-Allow-Origin":"*"}

    def put(self,id):
        # Get the application which needs to be updated
        data = ApplicationResource.parser.parse_args()

        if(ApplicationModel.find_by_id(id)):
            application = ApplicationModel.find_by_id(id)
            #Update the applicaiton
            application.status = data["status"]
            application.interest = data["interest"]
            application.confirmed = data["confirmed"]
            application.present = data["present"]
            application.dinnerID = data["dinnerID"]
            application.studentID = data["studentID"]
        else:
            return {"Message":"No Application could be found with that ID"},  200, {"Access-Control-Allow-Origin":"*"}

        application.save_to_db()
        return ApplicationModel.find_by_id(id).json(),  200, {"Access-Control-Allow-Origin":"*"}


class ApplicationConfirmer(Resource):

    def options (self):
        return {'Allow' : 'PUT, POST' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET, POST', \
          'Access-Control-Allow-Headers' : "Content-Type"}

    # Create a new strain, add it to the table
    def post(self):

        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = ApplicationRegistrar.parser.parse_args();

        # Checking to see if a student object even exists with that particular net id
        if not (StudentModel.find_by_id(data["studentID"])):
            return {"ERROR": "No student could be found with that ID"}, 404,{"Access-Control-Allow-Origin":"*"}

        # Checking to see if a dinner object even exists with that particular net id
        if not (DinnerModel.find_by_id(data["dinnerID"])):
            return {"ERROR": "No dinner could be found with that ID"}, 404, {"Access-Control-Allow-Origin":"*"}

        # Create a new Application object containing the passed properties.
        newApp = ApplicationModel(**data) ## ** automatically separates dict keywords into arguments

        # Save the new APPLICATION to the database.
        newApp.save_to_db()


        return ApplicationModel.return_last_item().json(), 200, {"Access-Control-Allow-Origin":"*"}


# A resource to register a new strain
class ApplicationRegistrar(Resource):

    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    parser.add_argument("interest",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "interest cannot be left blank"
    )

    parser.add_argument("studentID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Student ID cannot be left blank"
    )

    parser.add_argument("dinnerID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Dinner ID cannot be left blank"
    )

    def options (self):
        return {'Allow' : 'PUT, POST' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET, POST', \
          'Access-Control-Allow-Headers' : "Content-Type"}

    # Create a new strain, add it to the table
    def post(self):

        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = ApplicationRegistrar.parser.parse_args();

        # Checking to see if a student object even exists with that particular net id
        if not (StudentModel.find_by_id(data["studentID"])):
            return {"ERROR": "No student could be found with that ID"}, 404,{"Access-Control-Allow-Origin":"*"}

        # Checking to see if a dinner object even exists with that particular net id
        if not (DinnerModel.find_by_id(data["dinnerID"])):
            return {"ERROR": "No dinner could be found with that ID"}, 404, {"Access-Control-Allow-Origin":"*"}

        # Create a new Application object containing the passed properties.
        newApp = ApplicationModel(**data) ## ** automatically separates dict keywords into arguments

        # Save the new APPLICATION to the database.
        newApp.save_to_db()


        return ApplicationModel.return_last_item().json(), 200, {"Access-Control-Allow-Origin":"*"}
