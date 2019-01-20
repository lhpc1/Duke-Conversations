# This defines the Strain Resource that will be used for CRUD operations in the API

# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.StudentReviewModel import StudentReviewModel
from models.StudentModel import StudentModel
from models.DinnerModel import DinnerModel
from db import db

class StudentReviewResource(Resource):

    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    parser.add_argument("foodRating",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "foodRating cannot be left blank"
    )

    parser.add_argument("conversationRating",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "conversationRating cannot be left blank"
    )

    parser.add_argument("comments",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "foodRating cannot be left blank"
    )

    parser.add_argument("studentID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "studentID cannot be left blank"
    )

    parser.add_argument("dinnerID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "dinnerID cannot be left blank"
    )

    # GET a particular strain's information by id
    def get(self,id):
        review = StudentReviewModel.find_by_id(id)
        if(review):
            return review.json(),200, {"Access-Control-Allow-Origin":"*"}

        return {"Message":"No student review could be found with that ID"}, 404, {"Access-Control-Allow-Origin":"*"}

    # Allow for updates to professors
    def put(self, id):

        data = StudentReviewResource.parser.parse_args()

        if(StudentReviewResource.find_by_id(id)):
            reviewOfInterest = StudentReviewModel.find_by_id(id)
            reviewOfInterest.foodRating = data["foodRating"]
            reviewOfInterest.conversationRating = data["conversationRating"]
            reviewOfInterest.comments = data["comments"]

            if StudentModel.find_by_id(data["studentID"]):
                reviewOfInterest.studentID = data["studentID"]
            else:
                return {"Message":"No student with that ID could be found, please enter a valid student ID"}, 404

            if DinnerModel.find_by_id(data["dinnerID"]):
                reviewOfInterest.dinnerID = data["dinnerID"]
            else:
                return {"Message":"No dinner with that ID could be found, please enter a valid dinner ID"}, 404

        else:
            reviewOfInterest = StudentReviewModel(id=id,**data)

        reviewOfInterest.save_to_db()

        return reviewOfInterest.json(),  200, {"Access-Control-Allow-Origin":"*"}

    def delete(self, id):

        if(StudentReviewModel.find_by_id(id)):
            StudentReviewModel.find_by_id(id).delete_from_db()
            return {"Message":"Student reivew with id {} deleted.".format(id)}, 200, {"Access-Control-Allow-Origin":"*"}

        return {"Message":"No student review with id {} found.".format(id)}, 404, {"Access-Control-Allow-Origin":"*"}

# A resource to return a list of all strains in the db
class StudentReviewListResource(Resource):

    # Return all strains in a json format
    def get(self):
        return StudentReviewModel.return_all(), 200, {"Access-Control-Allow-Origin":"*"}

# A resource to register a new strain
class StudentReviewRegistrar(Resource):

    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    parser.add_argument("foodRating",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "foodRating cannot be left blank"
    )

    parser.add_argument("conversationRating",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "conversationRating cannot be left blank"
    )

    parser.add_argument("comments",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "foodRating cannot be left blank"
    )

    parser.add_argument("studentID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "studentID cannot be left blank"
    )

    parser.add_argument("dinnerID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "dinnerID cannot be left blank"
    )

    def options (self):
        return {'Allow' : 'PUT' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET', \
          'Access-Control-Allow-Headers' : "Content-Type"}

    # Create a new strain, add it to the table
    def post(self):

        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = StudentReviewRegistrar.parser.parse_args();

        # Create a new ProfessorModel object containing the passed properties.
        newReview = StudentReviewModel(**data) ## ** automatically separates dict keywords into arguments

        # Save the new professor to the database.
        newReview.save_to_db()

        return newReview.json(), 200, {"Access-Control-Allow-Origin":"*"}
