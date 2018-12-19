from flask_script import Manager
from db import db
from app import app
from flask_mail import Message, Mail
from models.DinnerModel import DinnerModel


manager = Manager(app)

with app.app_context():
    db.init_app(app)

@manager.command
def hello():
    dinners = DinnerModel.return_all_objects()
    for dinner in dinners:
        for application in dinner.applications:
            print(application.json())



if __name__ == "__main__":
    manager.run()
