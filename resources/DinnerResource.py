# This defines the Dinner Resource that will be used for CRUD operations in the API

# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.DinnerModel import DinnerModel
from db import db

class DinnerResource(Resource):

    # GET a particular dinner's information by id
    def get(self,id):
        found = DinnerModel.find_by_id(id)
        if(found):
            return found.json()

        return {"message":"No Dinner could be found with that ID"}

# A resource to return a list of all strains in the db
class DinnerListResource(Resource):

    # Return all strains in a json format
    def get(self):
        return DinnerModel.return_all()

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


    # Create a new strain, add it to the table
    def post(self):

        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = DinnerRegistrar.parser.parse_args();

        # Create a new ProfessorModel object containing the passed properties.
        newDinner = DinnerModel(**data) ## ** automatically separates dict keywords into arguments

        # Save the new professor to the database.
        newDinner.save_to_db()

        return DinnerModel.return_last_item().json()
