# Importing essential dependencies
from flask import Flask, send_file, request, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

# Import our resources
from resources.ProfessorResource import ProfessorResource, ProfessorRegistrar, ProfessorListResource
from resources.StudentResource import StudentResource, StudentRegistrar, StudentListResource
from resources.DinnerResource import DinnerResource, DinnerRegistrar, DinnerListResource
from resources.ApplicationResource import ApplicationResource, ApplicationRegistrar

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


# Allow for the creation of standard user objects
api.add_resource(ProfessorRegistrar,"/professor/register")
api.add_resource(ProfessorResource,"/professors/<string:uniqueID>")
api.add_resource(ProfessorListResource,"/professors")
api.add_resource(StudentResource, "/student/<string:netID>")
api.add_resource(StudentRegistrar, "/student/register")
api.add_resource(StudentListResource,"/students")
api.add_resource(DinnerResource, "/dinner/<int:id>")
api.add_resource(DinnerRegistrar, "/dinner/register")
api.add_resource(DinnerListResource, "/dinners")
api.add_resource(ApplicationResource,"/applicaiton/<int:id>")
api.add_resource(ApplicationRegistrar,"/application/register")


if __name__ == "__main__":
    # We import SQLAlchemy here from DB alchemy due to the problems with circular importsself.
    # Our models and in turn resources use SQL Alchemy, so we need to import the final version here
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
