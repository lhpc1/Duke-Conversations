# Importing essential dependencies
from flask import Flask, send_file, request, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
# from security import authenticate, identity
from flask_cors import CORS

# Configure mail client
from flask_mail import Mail, Message

# Authentication resources
from models.UserModel import UserModel

# Import our resources
from resources.ProfessorResource import ProfessorResource, ProfessorRegistrar, ProfessorListResource
from resources.StudentResource import StudentResource, StudentRegistrar, StudentListResource
from resources.DinnerResource import DinnerResource, DinnerRegistrar, DinnerListResource, DinnerStatusCodeResource, DinnerConfirmer
from resources.ApplicationResource import ApplicationResource, ApplicationRegistrar, ApplicationConfirmer
from resources.UserResource import UserResource, UserListResource

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
	MAIL_PASSWORD = "2dfsajfjl;sdfkjl;a"
)

mail = Mail(app)
# Initialize flask_restful Api
api = Api(app)

################################
### MANAGING AUTHENTICATION ####
################################
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)

@app.route("/login", methods = ["POST", "GET"])
def login():
	if request.method == 'POST':
		content = request.get_json()
		if "username" and "password" in content:
			if UserModel.find_by_username(content["username"]):
				user = UserModel.find_by_username(content["username"])
				if content["password"] == user.password:
					login_user(user)
				else:
					return jsonify({"Message":"Incorrect username or password"})

				return jsonify({'Message':"Logged in User with username {} and id {}".format(user.username, user.id)})
			else:
				return jsonify({"Message":"No user could be found with that username"})
		else:
			return jsonify({"Message":"Login requests must have username and password fields"})

    # user = UserModel.query.get(1)
	return jsonify({"Message":"error"})

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out"

@app.route("/userinfo")
@login_required
def userinfo():
	return jsonify({"Message":"Current user role: {}".format(current_user.role)})

################################
### /MANAGING AUTHENTICATION ###
################################

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
api.add_resource(DinnerStatusCodeResource,"/dinner/selective")
api.add_resource(DinnerListResource, "/dinners")
api.add_resource(DinnerConfirmer, "/dinner/confirm/<int:id>")
api.add_resource(ApplicationConfirmer, "/application/update")
api.add_resource(ApplicationResource,"/application/<int:id>")
api.add_resource(ApplicationRegistrar,"/application/register")
api.add_resource(UserResource,"/user/<int:id>")
api.add_resource(UserListResource,"/users")

if __name__ == "__main__":
    # We import SQLAlchemy here from DB alchemy due to the problems with circular importsself.
    # Our models and in turn resources use SQL Alchemy, so we need to import the final version here
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
