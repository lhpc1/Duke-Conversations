# Importing necessary dependencies
from flask import Flask, request
from flask_restful import Resource, reqparse
from db import db

class PronounsResource(Resource):

    def options (self):
        return {'Allow' : 'PUT' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET', \
          'Access-Control-Allow-Headers' : "Content-Type"}

    # GET a JSON dictionary of each Pronoun number correspondance
    def get(self,netID):
        student = StudentModel.find_by_id(netID)
        if(student):
            return student.json(), 200, {"Access-Control-Allow-Origin":"*"}

        return {"message":"No student could be found with that ID"}, 500, {"Access-Control-Allow-Origin":"*"}
