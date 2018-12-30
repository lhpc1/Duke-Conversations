# This defines the Dinner Resource that will be used for CRUD operations in the API

# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.DinnerModel import DinnerModel
from models.ProfessorModel import ProfessorModel
from models.UserModel import UserModel
from db import db

class DinnerResource(Resource):
    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    parser.add_argument("timeStamp",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Time Stamp cannot be left blank"
    )

    parser.add_argument("topic",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "topic cannot be left blank"
    )

    parser.add_argument("description",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "description cannot be left blank"
    )

    parser.add_argument("studentLimit",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "Student Limit cannot be left blank"
    )

    parser.add_argument("address",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Address cannot be left blank"
    )

    parser.add_argument("dietaryRestrictions",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Dietary Restrictions cannot be left blank"
    )

    parser.add_argument("invitationSentTimeStamp",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "InvitationSetnTimeStamp cannot be left blank"
    )

    parser.add_argument("professorID",
        type = str,
        required = True,
        help = "Professor ID cannot be left blank. Must be String."
    )

    parser.add_argument("catering",
        type = bool,
        required = True,
        help = "Catering cannot be left blank. Must be Boolean."
    )

    parser.add_argument("transportation",
        type = bool,
        required = True,
        help = "Transportation cannot be left blank. Must be Boolean."
    )

    parser.add_argument("userID",
        type = int,
        required = True,
        help = "userID cannot be left blank. Must be int."
    )

    # GET a particular dinner's information by id
    def get(self,id):
        found = DinnerModel.find_by_id(id)
        if(found):
            return found.json(), 200, {"Access-Control-Allow-Origin":"*"}

        return {"message":"No Dinner could be found with that ID"}, 404, {"Access-Control-Allow-Origin":"*"}

    def options (self):
        return {'Allow' : 'PUT, GET, POST' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET', \
          'Access-Control-Allow-Headers' : "Content-Type"}

    def put(self, id):

        data = DinnerResource.parser.parse_args()

        if(DinnerModel.find_by_id(id)):
            dinnerOfInterest = DinnerModel.find_by_id(id)
            dinnerOfInterest.timeStamp = data["timeStamp"]
            dinnerOfInterest.topic = data["topic"]
            dinnerOfInterest.description = data["description"]
            dinnerOfInterest.studentLimit = data["studentLimit"]
            dinnerOfInterest.address = data["address"]
            dinnerOfInterest.dietaryRestrictions = data["dietaryRestrictions"]
            dinnerOfInterest.professorID = data["professorID"]
            dinnerOfInterest.catering = data["catering"]
            dinnerOfInterest.transportation = data["transportation"]
            dinnerOfInterest.invitationSentTimeStamp = data["invitationSentTimeStamp"]
            dinnerOfInterest.userID = data["userID"]
        else:
            dinnerOfInterest = DinnerModel(**data)

        # If the dinner gains a userID, but is not completely done "not 2", then update the status to 1, which
        # means it is claimed but does not have a user yet.
        if dinnerOfInterest.userID and dinnerOfInterest.status is not 2:
            dinnerOfInterest.status = 1

        dinnerOfInterest.save_to_db()

        # increase the number of dinners for this userID
        user = UserModel.find_by_id(data["userID"])
        user.dinnerCount += 1
        user.semDinnerCount += 1
        user.save_to_db();

        return DinnerModel.find_by_id(id).json(), 200, {"Access-Control-Allow-Origin":"*"}

    def delete(self,id):

        if(DinnerModel.find_by_id(id)):
            DinnerModel.find_by_id(id).delete_from_db()
            return {"Message":"Dinner with id {} deleted.".format(id)}, 200, {"Access-Control-Allow-Origin":"*"}

        return {"Message":"No dinner with id {} found.".format(id)}, 404, {"Access-Control-Allow-Origin":"*"}

# A resource to return a list of all strains in the db
class DinnerListResource(Resource):

    # Return all strains in a json format
    def get(self):
        return DinnerModel.return_all(), 200, {"Access-Control-Allow-Origin":"*"}

class DinnerStatusCodeResource(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("status",type = int, location = "args")

    parser.add_argument("id",type = str, location = "args")

    # Return a dinner by a status code
    def get(self):
        data = DinnerStatusCodeResource.parser.parse_args()

        if data["status"] is None and data["id"]:
            return DinnerModel.return_by_userID(data["id"]), 200, {"Access-Control-Allow-Origin":"*"}
        elif data["status"] and data["id"] is None:
            return DinnerModel.return_all_dinners_by_status(data["status"]), 200, {"Access-Control-Allow-Origin":"*"}
        elif data["status"] and data["id"]:
            return DinnerModel.return_by_status_and_id(data["status"], data["id"]), 200, {"Access-Control-Allow-Origin":"*"}
        else:
            return DinnerModel.return_all(), 200, {"Access-Control-Allow-Origin":"*"}

# A resource to register a new strain
class DinnerRegistrar(Resource):

    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    parser.add_argument("timeStamp",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Time Stamp cannot be left blank"
    )

    parser.add_argument("topic",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "topic cannot be left blank"
    )

    parser.add_argument("description",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "description cannot be left blank"
    )

    parser.add_argument("studentLimit",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "Student Limit cannot be left blank"
    )

    parser.add_argument("address",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Address cannot be left blank"
    )

    parser.add_argument("dietaryRestrictions",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "Dietary Restrictions cannot be left blank"
    )

    parser.add_argument("professorID",
        type = str,
        required = True,
        help = "Professor ID cannot be left blank. Must be integer."
    )

    def options (self):
        return {'Allow' : 'PUT' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET', \
          'Access-Control-Allow-Headers' : "Content-Type"}

    # Create a new strain, add it to the table
    def post(self):
        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = DinnerRegistrar.parser.parse_args();

        if ProfessorModel.find_by_id(data["professorID"]) is None:
            return {"Message":"Dinner could not be created as no such professor could be found with that ID"}

        # Create a new ProfessorModel object containing the passed properties.
        newDinner = DinnerModel(**data) ## ** automatically separates dict keywords into arguments

        # Save the new professor to the database.
        newDinner.save_to_db()

        return DinnerModel.return_last_item().json(), 201, {"Access-Control-Allow-Origin":"*"}
