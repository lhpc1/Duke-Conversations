# Importing essential dependencies
from flask import Flask, send_file, request, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

# Import our resources
from resources.ProfessorResource import ProfessorResource, ProfessorRegistrar, ProfessorListResource

# Initialize our flask application
app = Flask(__name__)

# Configuring SQL Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "jose"

# Initialize flask_restful Api
api = Api(app)

# Configuring token based authentication
jwt = JWT(app, authenticate, identity) #/ auth

# first request is created unless they exist already. Pretty helpful. Will also automatically create data.db
@app.before_first_request
def create_tables():
    db.create_all()

# Allow for the creation of standard user objects
api.add_resource(ProfessorRegistrar,"/professor/register")
api.add_resource(ProfessorResource,"/professors/<string:uniqueID>")
api.add_resource(ProfessorListResource,"/professors")



if __name__ == "__main__":
    # We import SQLAlchemy here from DB alchemy due to the problems with circular importsself.
    # Our models and in turn resources use SQL Alchemy, so we need to import the final version here
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
