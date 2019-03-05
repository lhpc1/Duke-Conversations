# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from models.UserModel import UserModel
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity


class UserResource(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("username",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "username cannot be left blank"
    )

    parser.add_argument("newPassword",type = str, required = False, help = "newPassword cannot be left blank.")

    parser.add_argument("oldPassword",
        type = str,
        required = False, # If there is no price argument, stop.
        help = "oldPassword cannot be left blank"
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


    # GET a particular strain's information by id
    @jwt_required
    def get(self,id):

        user = UserModel.find_by_id(id)

        if not user:
            return {"Message":"No user could be found with that ID"}, 200, {"Access-Control-Allow-Origin":"*"}

        current_user = get_jwt_identity()
        currentUser = UserModel.find_by_username(current_user)
        if user.id == currentUser.id or currentUser.role == 0:
            if(user):
                return user.json(), 200, {"Access-Control-Allow-Origin":"*"}
        else:
            return {"Message":"You cannot view information about other users unless you are a super admin."}, 401,  {"Access-Control-Allow-Origin":"*"}

        return {"Message":"No user could be found with that ID"}, 200, {"Access-Control-Allow-Origin":"*"}


    @jwt_required
    def put(self,id):
        current_user = get_jwt_identity()
        if(UserModel.find_by_username(current_user)):
            currentUser = UserModel.find_by_username(current_user)
        else:
            return {"Message":"JSON token does not match any known user. Please register user first."}

        if currentUser.role != 0:
            if currentUser.id != id:
                return {"Message":"Only super admins and users themselves may modify user information. You lack permissions."}, 401

        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = UserResource.parser.parse_args();

        if(UserModel.find_by_id(id)):
            userToChange = UserModel.find_by_id(id)
            if(data["oldPassword"] is None and currentUser.role != 0):
                return {"Message":"Please enter oldPassword field. Only superadmins may edit without oldPassword."}

            if(userToChange.password != data["oldPassword"] and currentUser.role != 0):
                return {"Messsage":"Old password did not match with this user. Please enter correct password before modifying."},401

            userToChange.username = data["username"]

            if data["newPassword"]:
                userToChange.password = data["newPassword"]

            userToChange.email = data["email"]
            addedMessage = True
            if(currentUser.role == 0):
                addedMessage = False
                userToChange.role = data["role"]

            userToChange.netID = data["netID"]
            userToChange.firstName = data["firstName"]
            userToChange.lastName = data["lastName"]
            userToChange.phone = data["phone"]
            userToChange.major = data["major"]
            userToChange.emailText = data["emailText"]

            userToChange.save_to_db()
            if(addedMessage):
                returnJSON = {}
                returnJSON["user"] = userToChange.json()
                returnJSON["Message"] = "Note: Could not modify role as you do not have superadmin credentials. "
                return returnJSON
            else:
                return userToChange.json()
        else:
            return {"Message":"No user could be found with that id"},404

        return {"Message":"Unexpected error on /User/put"}, 501

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

    parser.add_argument("newPassword",
        type = str,
        required = True, # If there is no price argument, stop.
        help = "newPassword cannot be left blank"
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
            return {"Message":"Only super admins may create new users. You lack permissions."}, 401, {"Access-Control-Allow-Origin":"*"}

        # Acquire all of the data in a dict of each argument defined in the parser above.
        data = UserRegistrar.parser.parse_args();

        # Create a new StudentModel object containing the passed properties.
        dummyPassword = data["newPassword"]
        del data["newPassword"]
        newUser = UserModel(**data, password=dummyPassword) ## ** automatically separates dict keywords into arguments

        # Save the new professor to the database.
        newUser.save_to_db()

        # Return the just posted student
        return newUser.json(), 201, {"Access-Control-Allow-Origin":"*"}
