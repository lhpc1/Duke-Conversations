# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.UserModel import UserModel
from db import db

class UserResource(Resource):

    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    # GET a particular strain's information by id
    def get(self,id):
        user = UserModel.find_by_id(id)
        if(user):
            return user.json(), {"Access-Control-Allow-Origin":"*"}

        return {"message":"No user could be found with that ID"}, 200, {"Access-Control-Allow-Origin":"*"}

    # # Allow for updates to professors
    # def put(self, uniqueID):
    #
    #     data = ProfessorResource.parser.parse_args()
    #
    #     if(ProfessorModel.find_by_id(uniqueID)):
    #         professorOfInterest = ProfessorModel.find_by_id(uniqueID)
    #         professorOfInterest.firstName = data["firstName"]
    #         professorOfInterest.lastName = data["lastName"]
    #         professorOfInterest.genderPronouns = data["genderPronouns"]
    #         professorOfInterest.department = data["department"]
    #         professorOfInterest.title = data["title"]
    #         professorOfInterest.school = data["school"]
    #         professorOfInterest.email = data["email"]
    #     else:
    #         professorOfInterest = ProfessorModel(**data)
    #
    #     professorOfInterest.save_to_db()
    #
    #     return ProfessorModel.find_by_id(uniqueID).json(),  200, {"Access-Control-Allow-Origin":"*"}
    #
    # def delete(self,uniqueID):
    #
    #     if(ProfessorModel.find_by_id(uniqueID)):
    #         ProfessorModel.find_by_id(uniqueID).delete_from_db()
    #         return {"Message":"Professor with id " + uniqueID + " deleted."}, 200, {"Access-Control-Allow-Origin":"*"}
    #
    #     return {"Message":"No professor with " + uniqueID + " found."}, 200, {"Access-Control-Allow-Origin":"*"}

# A resource to return a list of all strains in the db
class UserListResource(Resource):

    # Return all strains in a json format
    def get(self):
        return UserModel.return_all(), 200, {"Access-Control-Allow-Origin":"*"}
