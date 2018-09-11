# Importing essential dependencies
from flask import Flask, send_file, request, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required

# Initialize our flask application
app = Flask(__name__)

# Configuring SQL Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize flask_restful Api
api = Api(app)
