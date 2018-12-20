from flask_script import Manager
from db import db
from app import app
from flask_mail import Message, Mail
from models.DinnerModel import DinnerModel

import time
import datetime

manager = Manager(app)

with app.app_context():
    db.init_app(app)


# def generateMessage(student, dinner):



@manager.command
def hello():
    dinners = DinnerModel.return_all_objects()

    from app import mail
    # First, email the user their list of matches
    for dinner in dinners:
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

    print(time.time())

if __name__ == "__main__":
    manager.run()
