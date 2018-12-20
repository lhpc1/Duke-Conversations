# Importing essential dependencies
from flask import Flask, send_file, request, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from flask_cors import CORS

# Configure mail client
from flask_mail import Mail, Message

# Import our resources
from resources.ProfessorResource import ProfessorResource, ProfessorRegistrar, ProfessorListResource
from resources.StudentResource import StudentResource, StudentRegistrar, StudentListResource
from resources.DinnerResource import DinnerResource, DinnerRegistrar, DinnerListResource
from resources.ApplicationResource import ApplicationResource, ApplicationRegistrar
from resources.WebhooksTest import WebhooksTest
from resources.AdminResource import AdminRegister
# Initialize our flask application
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuring SQL Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "jose"
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'yasab27@gmail.com',
	MAIL_PASSWORD = "Louieis1_best"
)

mail = Mail(app)
# Initialize flask_restful Api
api = Api(app)

# Configuring token based authentication
jwt = JWT(app, authenticate, identity) #/ auth
#Ask the db to create all the necessary tables before operation
# @app.before_first_request
# def create_tables():
#     db.create_all()
# def options (self):
#     return {'Allow' : 'PUT' }, 200, \
#     { 'Access-Control-Allow-Origin': '*', \
#       'Access-Control-Allow-Methods' : 'PUT,GET' }

# Setting up a basic route for the homepage without using Flask-RESTful. This enables us to run our angular on the front end
@app.route("/")
def home():
    return send_file("templates/index.html")

# Allow for the creation of standard user objects
api.add_resource(ProfessorRegistrar,"/professor/register")
api.add_resource(ProfessorResource,"/professor/<string:uniqueID>")
api.add_resource(ProfessorListResource,"/professors")
api.add_resource(StudentResource, "/student/<string:netID>")
api.add_resource(StudentRegistrar, "/student/register")
api.add_resource(StudentListResource,"/students")
api.add_resource(DinnerResource, "/dinner/<int:id>")
api.add_resource(DinnerRegistrar, "/dinner/register")
api.add_resource(DinnerListResource, "/dinners")
api.add_resource(ApplicationResource,"/application/<int:id>")
api.add_resource(ApplicationRegistrar,"/application/register")
api.add_resource(AdminRegister,"/admin/register")
api.add_resource(WebhooksTest, "/webhooks/test")


if __name__ == "__main__":
    # We import SQLAlchemy here from DB alchemy due to the problems with circular importsself.
    # Our models and in turn resources use SQL Alchemy, so we need to import the final version here
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
