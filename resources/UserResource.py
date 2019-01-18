# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.UserModel import UserModel
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity


class UserResource(Resource):

    # Defining a parser that will handle data collection from post requests
    parser = reqparse.RequestParser()

    # GET a particular strain's information by id
    @jwt_required
    def get(self,id):

        user = UserModel.find_by_id(id)

        if not user:
            return {"Message":"No user could be found with that ID"}, 200, {"Access-Control-Allow-Origin":"*"}

        current_user = get_jwt_identity()
        currentUser = UserModel.find_by_username(current_user)
        if user.id == currentUser.id or currentUser.id == 0:
            if(user):
                return user.json(), 200, {"Access-Control-Allow-Origin":"*"}
        else:
            return {"Message":"You cannot view information about other users unless you are a super admin."}, 401,  {"Access-Control-Allow-Origin":"*"}

        return {"Message":"No user could be found with that ID"}, 200, {"Access-Control-Allow-Origin":"*"}

    # Only super admins can delete other users
    @jwt_required
    def delete(self,id):

        current_user = get_jwt_identity()
        user = UserModel.find_by_username(current_user)
        if user.role is not 0:
            return {"Message":"Only super admids may delete users. You lack permissions."}, 401

        if(UserModel.find_by_id(id)):
            UserModel.find_by_id(id).delete_from_db()
            return {"Message":"User with id {} deleted.".format(id)}, 200, {"Access-Control-Allow-Origin":"*"}

        return {"Message":"No user with ID {} found.".format(id)}, 404, {"Access-Control-Allow-Origin":"*"}

# A resource to return a list of all strains in the db
class UserListResource(Resource):

    # Return all strains in a json format
    # @jwt_required
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = UserModel.find_by_username(current_user)
        if user.role is not 0:
            return {"Message":"Only super admins may access the list of all users. You lack permissions."}, 401

        return UserModel.return_all(), 200, {"Access-Control-Allow-Origin":"*"}

class UserRegistrar(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("username",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "username cannot be left blank"
    )

    parser.add_argument("password",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "password cannot be left blank"
    )

    parser.add_argument("email",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "email cannot be left blank"
    )

    parser.add_argument("role",
        type = int,
        required = True, # If there is no price argument, stop.
        help = "role cannot be left blank"
    )

    parser.add_argument("netID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "netID name cannot be left blank"
    )

    parser.add_argument("uniqueID",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "uniqueID name cannot be left blank"
    )

    parser.add_argument("phone",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "phone cannot be left blank"
    )

    parser.add_argument("firstName",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "firstName cannot be left blank"
    )

    parser.add_argument("lastName",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "lastName cannot be left blank"
    )

    parser.add_argument("major",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "major cannot be left blank"
    )

    parser.add_argument("emailText",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "emailText cannot be left blank"
    )

    @jwt_required
    def post(self):

        current_user = get_jwt_identity()
        user = UserModel.find_by_username(current_user)
        if user.role is not 0:
            return {"Message":"Only super admins may create new users. You lack permissions."}, 401

        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = UserRegistrar.parser.parse_args();

        # Create a new StudentModel object containing the passed properties.
        newUser = UserModel(**data) ## ** automatically separates dict keywords into arguments

        # Save the new professor to the database.
        newUser.save_to_db()

        # Return the just posted student
        return newUser.json(), 201, {"Access-Control-Allow-Origin":"*"}
