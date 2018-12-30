from flask_script import Manager
from db import db
from app import app
from flask_mail import Message, Mail
from models.DinnerModel import DinnerModel
from models.UserModel import UserModel

import time
import datetime

manager = Manager(app)

with app.app_context():
    db.init_app(app)

@manager.command
def gentables():
    db.create_all()
    print('TABLES GENERATED')

# def generateMessage(student, dinner):

@manager.command
def populate():
    a = UserModel("coopedmunds", "pass" , "cooper.edmunds@duke.edu", 2,"ce10", "12345", "Cooper","Edmunds", "123-123-1234",1, "Lorem Ipsum" )
    db.session.add(a)
    db.session.commit()

    allUsers = db.session.query(UserModel).all()
    for user in allUsers:
        print(user.username)

def emailStudents(dinner):

    from app import mail

    dinnerTimeDifference = int(dinner.timeStamp)-time.time()
    print(dinnerTimeDifference)
    print(datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x'))
    # If it is between three and 2 days away
    if dinnerTimeDifference <= 259200 and dinnerTimeDifference >= 172800:
        for application in dinner.applications:
            try:
                dinnerTime = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x')
                msg = Message("Three Day Notification!",
                  sender="yasab27@gmail.com",
                  recipients=["{}@duke.edu".format(application.studentID)]) #entryOfInterest.email
                msg.html = "Don't forget you have a dinner with {} {} on {}. Yay!".format(dinner.professor.firstName, dinner.professor.lastName, dinnerTime)
                mail.send(msg)
            except Exception as e:
                return {"Message": str(e)}
    else:
        for application in dinner.applications:
            try:
                dinnerTime = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x')
                msg = Message("One Day Notification!",
                  sender="yasab27@gmail.com",
                  recipients=["{}@duke.edu".format(application.studentID)]) #entryOfInterest.email
                msg.html = "Don't forget you have a dinner with {} {} on {}. Yay!".format(dinner.professor.firstName, dinner.professor.lastName, dinnerTime)
                mail.send(msg)
            except Exception as e:
                return {"Message": str(e)}

def remindProfessor(dinner):
    from app import mail

    dinnerTimeDifference = int(dinner.timeStamp)-time.time()
    print(dinnerTimeDifference)
    print(datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x'))
    # If it is between three and 2 days away
    if dinnerTimeDifference <= 259200 and dinnerTimeDifference >= 172800:
        try:
            dinnerTime = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x')
            msg = Message("Three Day Reminder!",
              sender="yasab27@gmail.com",
              recipients=[dinner.professor.email]) #entryOfInterest.email
            msg.html = "Don't forget you have a dinner on {}. Yay!".format(dinnerTime)
            mail.send(msg)
        except Exception as e:
            return {"Message": str(e)}
    else:
        try:
            dinnerTime = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x')
            msg = Message("One Day Notification!",
              sender="yasab27@gmail.com",
              recipients=[dinner.professor.email]) #entryOfInterest.email
            msg.html = "Don't forget you have a dinner with on {}. Yay!".format( dinnerTime)
            mail.send(msg)
        except Exception as e:
            return {"Message": str(e)}

def remindUser(dinner):
    from app import mail

    dinnerTimeDifference = int(dinner.timeStamp)-time.time()
    print(dinnerTimeDifference)
    print(datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x'))
    # If it is between three and 2 days away
    if dinnerTimeDifference <= 259200 and dinnerTimeDifference >= 172800:
        try:
            dinnerTime = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x')
            msg = Message("Three Day Reminder!",
              sender="yasab27@gmail.com",
              recipients=[dinner.user.email]) #entryOfInterest.email
            msg.html = "Don't forget you have a dinner on {}. Yay!".format(dinnerTime)
            mail.send(msg)
        except Exception as e:
            return {"Message": str(e)}
    else:
        try:
            dinnerTime = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x')
            msg = Message("One Day Notification!",
              sender="yasab27@gmail.com",
              recipients=[dinner.user.email]) #entryOfInterest.email
            msg.html = "Don't forget you have a dinner with on {}. Yay!".format( dinnerTime)
            mail.send(msg)
        except Exception as e:
            return {"Message": str(e)}


@manager.command
def hello():
    dinners = DinnerModel.return_all_objects()
    # First, email the user their list of matches
    for dinner in dinners:
        emailStudents(dinner)
        remindProfessor(dinner)
    print(time.time())

if __name__ == "__main__":
    manager.run()
