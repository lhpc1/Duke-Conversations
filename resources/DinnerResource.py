# This defines the Dinner Resource that will be used for CRUD operations in the API

# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.DinnerModel import DinnerModel
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

    # GET a particular dinner's information by id
    def get(self,id):
        found = DinnerModel.find_by_id(id)
        if(found):
            return found.json(), {"Access-Control-Allow-Origin":"*"}

        return {"message":"No Dinner could be found with that ID"}, 200, {"Access-Control-Allow-Origin":"*"}

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
        else:
            dinnerOfInterest = DinnerModel(**data)

        dinnerOfInterest.save_to_db()

        return DinnerModel.find_by_id(id).json(), 500, {"Access-Control-Allow-Origin":"*"}

    def delete(self,id):

        if(DinnerModel.find_by_id(id)):
            DinnerModel.find_by_id(id).delete_from_db()
            return {"Message":"Dinner with id " + ID + " deleted."}, 500, {"Access-Control-Allow-Origin":"*"}

        return {"Message":"No dinner with " + id + " found."}, 500, {"Access-Control-Allow-Origin":"*"}

# A resource to return a list of all strains in the db
class DinnerListResource(Resource):

    # Return all strains in a json format
    def get(self):
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

    # Create a new strain, add it to the table
    def post(self):

        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = DinnerRegistrar.parser.parse_args();

        # Create a new ProfessorModel object containing the passed properties.
        newDinner = DinnerModel(**data) ## ** automatically separates dict keywords into arguments

        # Save the new professor to the database.
        newDinner.save_to_db()

        return DinnerModel.return_last_item().json(), 201, {"Access-Control-Allow-Origin":"*"}
