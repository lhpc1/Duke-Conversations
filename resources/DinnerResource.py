# This defines the Dinner Resource that will be used for CRUD operations in the API

# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.DinnerModel import DinnerModel
from models.ProfessorModel import ProfessorModel
from models.UserModel import UserModel
from db import db
from flask_jwt_extended import jwt_required

import time
import datetime

from bs4 import BeautifulSoup

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
        required = False,
        help = "userID cannot be left blank. Must be int."
    )

    # GET a particular dinner's information by id
    # @jwt_required
    def get(self,id):
        found = DinnerModel.find_by_id(id)
        if(found):
            return found.json(), 200, {"Access-Control-Allow-Origin":"*"}

        return {"Message":"No Dinner could be found with id {}".format(id)}, 404, {"Access-Control-Allow-Origin":"*"}

    # @jwt_required
    def put(self, id):

        data = DinnerResource.parser.parse_args()

        if(DinnerModel.find_by_id(id)):
            dinnerOfInterest = DinnerModel.find_by_id(id)

            if not ProfessorModel.find_by_id(data["professorID"]):
                return {"Message":"There is no professor in the database with that ID"}, 404, {"Access-Control-Allow-Origin":"*"}

            if data["userID"]:
                if data["userID"] == -1:
                    pass
                elif not UserModel.find_by_id(data["userID"]):
                    return {"Message":"There is no user in the database with that ID"}, 404, {"Access-Control-Allow-Origin":"*"}

            dinnerOfInterest.timeStamp = data["timeStamp"]
            dinnerOfInterest.topic = data["topic"]
            dinnerOfInterest.description = data["description"]
            dinnerOfInterest.studentLimit = data["studentLimit"]
            dinnerOfInterest.address = data["address"]
            dinnerOfInterest.dietaryRestrictions = data["dietaryRestrictions"]

            if ProfessorModel.find_by_id(dinnerOfInterest.professorID):
                professor = ProfessorModel.find_by_id(dinnerOfInterest.professorID)
                professor.dinnerCount -= 1
                professor.save_to_db();

            dinnerOfInterest.professorID = data["professorID"]
            dinnerOfInterest.catering = data["catering"]
            dinnerOfInterest.transportation = data["transportation"]
            dinnerOfInterest.invitationSentTimeStamp = data["invitationSentTimeStamp"]

            # Assign new userID
            # If there is an older user, subtract their total dinner count by one
            if data["userID"]:
                if UserModel.find_by_id(dinnerOfInterest.userID):
                    user = UserModel.find_by_id(dinnerOfInterest.userID)
                    user.dinnerCount -= 1
                    user.semDinnerCount -= 1
                    user.save_to_db();
                dinnerOfInterest.userID = data["userID"]

        else:

            if not ProfessorModel.find_by_id(data["professorID"]):
                return {"Message":"There is no professor in the database with that ID"}, 404, {"Access-Control-Allow-Origin":"*"}

            if not UserModel.find_by_id(data["userID"]) or data["userID"] != -1:
                return {"Message":"There is no user in the database with that ID"}, 404, {"Access-Control-Allow-Origin":"*"}

            dinnerOfInterest = DinnerModel(id=id,**data)

        # If the dinner gains a userID, but is not completely done "not 2", then update the status to 1, which
        # means it is claimed but does not have a user yet.
        if dinnerOfInterest.userID and dinnerOfInterest.status is not 2:
            dinnerOfInterest.status = 1

        dinnerOfInterest.save_to_db()

        # increase the number of dinners for this new userID
        if data["userID"] and UserModel.find_by_id(data["userID"]):
            user = UserModel.find_by_id(data["userID"])
            user.dinnerCount += 1
            user.semDinnerCount += 1
            user.save_to_db();

        professor = ProfessorModel.find_by_id(data["professorID"])
        professor.dinnerCount += 1
        professor.save_to_db();

        return dinnerOfInterest.json(), 200, {"Access-Control-Allow-Origin":"*"}

    @jwt_required
    def delete(self,id):

        if(DinnerModel.find_by_id(id)):
            dinner = DinnerModel.find_by_id(id)
            dinner.delete_from_db()
            return {"Message":"Dinner with id {} deleted.".format(id)}, 200, {"Access-Control-Allow-Origin":"*"}

        return {"Message":"No dinner with id {} found.".format(id)}, 404, {"Access-Control-Allow-Origin":"*"}

# A resource to return a list of all strains in the db
class DinnerListResource(Resource):

    # Return all strains in a json format
    # @jwt_required
    def get(self):
        return DinnerModel.return_all(), 200, {"Access-Control-Allow-Origin":"*"}

class DinnerStatusCodeResource(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("status",type = int, location = "args")

    parser.add_argument("id",type = str, location = "args")

    # Return a dinner by a status code
    @jwt_required
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

# Get a dinner by and classify it as complete
class DinnerConfirmer(Resource):

    @jwt_required
    def get(self, id):
        # Get the dinner, change status, and then email everyone it is complete
        if DinnerModel.find_by_id(id):
            dinnerToConfirm = DinnerModel.find_by_id(id)
        else:
            return {"Message":"No dinner could be found with id  {}".format(id)}, 404, {"Access-Control-Allow-Origin":"*"}

        if not UserModel.find_by_id(dinnerToConfirm.userID):
            return {"Message":"This dinner is unclaimed and cannot be published"}, 400, {"Access-Control-Allow-Origin":"*"}

        dinnerToConfirm.status = 2
        dinnerToConfirm.save_to_db()

        # Designate all pending applications who are not waitlisted as rejected
        for application in dinnerToConfirm.applications:
            if application.status == 0:
                application.status = 2
                application.save_to_db()

        DinnerConfirmer.notifyRecipients(id)

        dinnerToConfirm.invitationSentTimeStamp = str(time.time())

        return {"Message":"Dinner with id {} is confirmed. All accepted applicants have been emailed. Confirmation email sent to  {} {}:{}".format(id, dinnerToConfirm.user.firstName, dinnerToConfirm.user.lastName, dinnerToConfirm.user.email)}, 200, {"Access-Control-Allow-Origin":"*"}

    # Email every applicant with a confirmed status upon
    @classmethod
    def notifyRecipients(cls, id):

        from app import mail
        from flask_mail import Message

        dinner = DinnerModel.find_by_id(id)

        # Send a confirmation email to the user
        try:
            dinnerTime = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x')
            msg = Message("Dinner Confirmed",
              sender="dukeconversationsreminders@gmail.com",
              recipients=["{}@duke.edu".format(dinner.user.email)]) #entryOfInterest.email
            msg.html = "You've published the dinner hosted by {} {}. It is on {}. Yay!".format(dinner.professor.firstName, dinner.professor.lastName, dinnerTime)
            mail.send(msg)
        except Exception as e:
            return {"Message": str(e)}

        # Email all accepted and waitlisted applicants
        for application in dinner.applications:
            print("Applications Status {}".format(application.status))
            if application.status == 1:
                try:
                    dinnerTime = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x')
                    dinnerDay = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime("%A")

                    msg = Message("Accepted",
                      sender="dukeconversationsreminders@gmail.com",
                      recipients=["{}@duke.edu".format(application.studentID)]) #entryOfInterest.email
                    print("{}@duke.edu".format(application.studentID))

                    # Read the html from the email template.
                    soup = BeautifulSoup(open("email-templates/acceptance.html"),"html.parser")

                    msg.html = soup.prettify().format(dinner.professor.firstName + " " + dinner.professor.lastName, dinnerDay,
                                                        dinnerTime, application.student.firstName +  " " + application.student.lastName, dinner.user.firstName + " " + dinner.user.lastName,
                                                        dinnerDay, dinner.address, dinner.topic,dinner.user.phone, dinner.user.firstName + ' ' + dinner.user.lastName)
                    # msg.html = "<h1> KILL ME </h1>"

                    # print(msg.html)
                    mail.send(msg)
                except Exception as e:
                    return {"Message": str(e)}

            if application.status == 3:
                try:
                    dinnerTime = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x')
                    msg = Message("Accepted",
                      sender="dukeconversationsreminders@gmail.com",
                      recipients=["{}@duke.edu".format(application.studentID)]) #entryOfInterest.email
                    msg.html = "You've been waitlisted to the dinner hosted by {} {}. It is on {}. Please contact us if you'd like to be removed from the waitlist.".format(dinner.professor.firstName, dinner.professor.lastName, dinnerTime)
                    mail.send(msg)
                except Exception as e:
                    return {"Message": str(e)}

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

    parser.add_argument("userID",
        type = int,
        required = False,
        help = "Professor ID cannot be left blank. Must be integer."
    )


    # Create a new strain, add it to the table
    @jwt_required
    def post(self):
        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = DinnerRegistrar.parser.parse_args();

        if ProfessorModel.find_by_id(data["professorID"]) is None:
            return {"Message":"Dinner could not be created as no such professor could be found with id {}.".format(data["professorID"])}, 404, {"Access-Control-Allow-Origin":"*"}

        if data["userID"]:
            if data["userID"] == -1:
                # Create a new ProfessorModel object containing the passed properties.
                newDinner = DinnerModel(**(data.pop("userID"))) ## ** automatically separates dict keywords into arguments

                # Iterate the amount of dinners for this professor by one
                associatedProfessor = ProfessorModel.find_by_id(data["professorID"])
                associatedProfessor.dinnerCount += 1
                associatedProfessor.save_to_db()

                # Save the new professor to the database.
                newDinner.save_to_db()

                return newDinner.json(), 201, {"Access-Control-Allow-Origin":"*"}

            elif not UserModel.find_by_id(data["userID"]):
                return {"Message":"There is no user in the database with that ID. Could not create dinner"}, 404, {"Access-Control-Allow-Origin":"*"}
            else:
                user = UserModel.find_by_id(data["userID"])
                user.dinnerCount += 1
                user.semDinnerCount += 1
                user.save_to_db()

        # Create a new ProfessorModel object containing the passed properties.
        newDinner = DinnerModel(**data) ## ** automatically separates dict keywords into arguments

        # Iterate the amount of dinners for this professor by one
        associatedProfessor = ProfessorModel.find_by_id(data["professorID"])
        associatedProfessor.dinnerCount += 1
        associatedProfessor.save_to_db()

        # Save the new professor to the database.
        newDinner.save_to_db()

        return newDinner.json(), 201, {"Access-Control-Allow-Origin":"*"}
