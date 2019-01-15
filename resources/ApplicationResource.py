# This defines the Strain Resource that will be used for CRUD operations in the API

# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.ApplicationModel import ApplicationModel
from models.StudentModel import StudentModel
from models.DinnerModel import DinnerModel
from db import db
from flask_jwt_extended import jwt_required

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
        help = "dinnerID cannot be left blank"
    )

    parser.add_argument("status",
        type = bool,
        required = True, # If there is no price argument, stop.
        help = "status cannot be left blank"
    )

    parser.add_argument("present",
        type = bool,
        required = True, # If there is no price argument, stop.
        help = "present cannot be left blank"
    )

    parser.add_argument("confirmed",
        type = bool,
        required = True, # If there is no price argument, stop.
        help = "confirmed cannot be left blank"
    )

    parser.add_argument("blackList",
        type = bool,
        required = True, # If there is no price argument, stop.
        help = "blackList cannot be left blank"
    )

    # GET a particular strain's information by id
    # @jwt_required
    def get(self,id):
        application = ApplicationModel.find_by_id(id)
        if(application):
            return application.json(), 200,{"Access-Control-Allow-Origin":"*"}

        return {"message":"No application could be found with that ID"}, 404, {"Access-Control-Allow-Origin":"*"}

    # @jwt_required
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
            application.blackList = data["blackList"]
        else:
            return {"Message":"No Application could be found with that ID"},  200, {"Access-Control-Allow-Origin":"*"}

        application.save_to_db()
        return ApplicationModel.find_by_id(id).json(),  200, {"Access-Control-Allow-Origin":"*"}


class ApplicationConfirmer(Resource):


    # Create a new object, add it to the table
    @jwt_required
    def post(self):

        # Acquire the list of applications to update
        content = request.get_json()
        updatedApplications = []
        for applicationNumber,statusUpdate in content.items():

            if ApplicationModel.find_by_id(int(applicationNumber)):

                application = ApplicationModel.find_by_id(int(applicationNumber))
                application.status = statusUpdate

                # If the applicant is being updated to 1, this indicates that the user has been selected, so the
                # number of selections for the student associated to the application needs to be increased by one
                if statusUpdate is 1:
                    student = StudentModel.find_by_id(application.studentID)
                    student.numberSelections += 1
                    student.numberSelectionsSemester += 1
                    student.save_to_db()

                updatedApplications.append(applicationNumber)
                application.save_to_db()

        return {"message":"Updated applications {}".format(str(updatedApplications))}, 200, {"Access-Control-Allow-Origin":"*"}


# class ApplicationCheckin(Resource):
#
#     def options (self):
#         return {'Allow' : 'PUT, POST' }, 200, \
#         { 'Access-Control-Allow-Origin': '*', \
#           'Access-Control-Allow-Methods' : 'PUT,GET, POST', \
#           'Access-Control-Allow-Headers' : "Content-Type"}
#
#     # Create a new strain, add it to the table
#     def post(self):
#
#         # Acquire the list of applications to update
#         content = request.get_json()
#
#         if "present" not in content:
#             return {"Message":"Please include present keyword followed by array of apps to mark present"}, 400, {"Access-Control-Allow-Origin":"*"}
#
#         updatedApplications = []
#         appsToUpdate = content["present"]
#         for app in appsToUpdate:
#             if ApplicationModel.find_by_id(app):
#                 application = ApplicationModel.find_by_id(app)
#                 application.present = True
#                 updatedApplications.append(app)
#                 application.save_to_db()
#
#         return {"message":"Marked present applications {}".format(str(updatedApplications))}, 200, {"Access-Control-Allow-Origin":"*"}

class ApplicationCheckin(Resource):


    # Create a new strain, add it to the table
    @jwt_required
    def post(self):

        # Acquire the list of applications to update
        content = request.get_json()

        for applicationNumber,statusUpdate in content.items():

            # Could not resolve
            couldNotResolve = []

            # applications marked present
            markedPresent = []

            # Marked absent
            markedAbsent = []

            if ApplicationModel.find_by_id(int(applicationNumber)):

                application = ApplicationModel.find_by_id(int(applicationNumber))

                print(application.json())
                print(statusUpdate)

                # If the applicant is being updated to present, this indicates that the user has been selected, so the
                # number of selections for the student associated to the application needs to be increased by one
                if statusUpdate is True:
                    application.present = True
                    application.save_to_db()
                    markedPresent.append(applicationNumber)
                elif statusUpdate is False:
                    application.present = False
                    application.save_to_db()
                    markedAbsent.append(applicationNumber)
                else:
                    couldNotResolve.append(applicationNumber)

            else:
                couldNotResolve.append(applicationNumber)


        return {"message":"Marked applications {} present. Marked {} Absent. Could not resolve applications with numbers {}.".format(str(markedPresent), str(markedAbsent), str(couldNotResolve))}, 200, {"Access-Control-Allow-Origin":"*"}


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
    # @jwt_required
    def post(self):

        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = ApplicationRegistrar.parser.parse_args();

        # Checking to see if a student object even exists with that particular net id
        if not (StudentModel.find_by_id(data["studentID"])):
            return {"ERROR": "No student could be found with that ID"}, 404,{"Access-Control-Allow-Origin":"*"}

        if StudentModel.find_by_id(data["studentID"]).blackList:
            return {"ERROR": "This student has been blacklisted and may not apply"}, 400,{"Access-Control-Allow-Origin":"*"}

        # Checking to see if a dinner object even exists with that particular net id
        if not (DinnerModel.find_by_id(data["dinnerID"])):
            return {"ERROR": "No dinner could be found with that ID"}, 404, {"Access-Control-Allow-Origin":"*"}

        # Create a new Application object containing the passed properties.
        newApp = ApplicationModel(**data) ## ** automatically separates dict keywords into arguments

        # Save the new APPLICATION to the database.
        newApp.save_to_db()

        # Increase the number of applications for the students
        student = StudentModel.find_by_id(data["studentID"])
        student.numberApplications += 1
        student.numberApplicationsSemester += 1

        student.save_to_db();

        return ApplicationModel.return_last_item().json(), 200, {"Access-Control-Allow-Origin":"*"}
