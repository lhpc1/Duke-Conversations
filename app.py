# Importing essential dependencies
from flask import Flask, send_file, request, jsonify
from flask_restful import Api
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from flask_cors import CORS

# Configure mail client
from flask_mail import Mail, Message

# Authentication resources
from models.UserModel import UserModel

# Import our resources
from resources.ProfessorResource import ProfessorResource, ProfessorRegistrar, ProfessorListResource
from resources.StudentResource import StudentResource, StudentRegistrar, StudentListResource
from resources.DinnerResource import DinnerResource, DinnerRegistrar, DinnerListResource, DinnerStatusCodeResource, DinnerConfirmer
from resources.ApplicationResource import ApplicationResource, ApplicationRegistrar, ApplicationConfirmer, ApplicationCheckin
from resources.UserResource import UserResource, UserListResource, UserRegistrar
from resources.ReviewResource import StudentReviewResource, StudentReviewListResource, StudentReviewRegistrar

# Initialize our flask application
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuring SQL Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = 'lemon'
app.secret_key = "jose"
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'yasab27@gmail.com',
	MAIL_PASSWORD = "2dfsajfjl;sdfkjl;a"
)

mail = Mail(app)
# Initialize flask_restful Api
api = Api(app)
jwt = JWTManager(app) #/ auth

@app.route('/login', methods=['POST'])
def login():
	if not request.is_json:
		return jsonify({"msg": "Missing JSON in request"}), 400

	username = request.json.get('username', None)
	password = request.json.get('password', None)
	if not username:
		return jsonify({"msg": "Missing username parameter"}), 400
	if not password:
		return jsonify({"msg": "Missing password parameter"}), 400

	# See if there is a user with this particular username
	if UserModel.find_by_username(username) is not None:
		user = UserModel.find_by_username(username)
	else:
		return jsonify({"msg": "No user with username {}".format(username)}), 400

	if password == user.password:
		access_token = create_access_token(identity=username)
	else:
		return jsonify({"msg": "Invalid Password"}), 400

	return jsonify(access_token=access_token), 200

# Setting up a basic route for the homepage without using Flask-RESTful. This enables us to run our angular on the front end
@app.route("/")
def home():
    return send_file("templates/index.html")

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
	# Access the identity of the current user with get_jwt_identity
	current_user = get_jwt_identity()
	user = UserModel.find_by_username(current_user)
	return jsonify(user.json()), 200


# Allow for the creation of standard user objects
api.add_resource(ProfessorRegistrar,"/professor/register")
api.add_resource(ProfessorResource,"/professor/<string:uniqueID>")
api.add_resource(ProfessorListResource,"/professors")
api.add_resource(StudentResource, "/student/<string:netID>")
api.add_resource(StudentRegistrar, "/student/register")
api.add_resource(StudentListResource,"/students")
api.add_resource(DinnerResource, "/dinner/<int:id>")
api.add_resource(DinnerRegistrar, "/dinner/register")
api.add_resource(DinnerStatusCodeResource,"/dinner/selective")
api.add_resource(DinnerListResource, "/dinners")
api.add_resource(DinnerConfirmer, "/dinner/confirm/<int:id>")
api.add_resource(ApplicationConfirmer, "/application/update")
api.add_resource(ApplicationResource,"/application/<int:id>")
api.add_resource(ApplicationRegistrar,"/application/register")
api.add_resource(ApplicationCheckin, "/application/checkin")
api.add_resource(UserResource,"/user/<int:id>")
api.add_resource(UserListResource,"/users")
api.add_resource(UserRegistrar, "/user/register")
api.add_resource(StudentReviewListResource, "/studentreviews")
api.add_resource(StudentReviewRegistrar, "/review/student/register")
api.add_resource(StudentReviewResource, "/review/student/<int:id>")

if __name__ == "__main__":
    # We import SQLAlchemy here from DB alchemy due to the problems with circular importsself.
    # Our models and in turn resources use SQL Alchemy, so we need to import the final version here
    from db import db
    db.init_app(app)
    app.run("localhost", debug=True)
