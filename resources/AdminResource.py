import sqlite3
from flask_restful import Resource, reqparse
from models.authentication.AdminModel import AdminModel
from db import db


# Since POST methods will be used to add new users to the register, we add it as an endpoint and therefore a resource
# to follow REST API standards
class AdminRegister(Resource):

    # We are going to use a parser to parse the JSON
    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type = str,
        required = True,
        help = "This field cannot be blank"
    )
    parser.add_argument("password",
        type = str,
        required = True,
        help = "This field cannot be blank"
    )

    def post(self):
        # Read the post request and get the username and password fields
        data = UserRegister.parser.parse_args()

        if AdminModel.findByUsername(data["username"]):
            return {"Message" : "This user already exists. Cannot create new user."}, 400

        newUser = AdminModel(**data) # The asterisk will automatically axpand data into individual values
        newUser.save_to_db()

        return {"Message":"Admin created successfully"}
