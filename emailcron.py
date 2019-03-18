from flask_script import Manager
from db import db
from app import app
from flask_mail import Message, Mail
from models.DinnerModel import DinnerModel
from models.UserModel import UserModel

import time
import datetime

# Getting beautiful soup for parsing html
from bs4 import BeautifulSoup

manager = Manager(app)

with app.app_context():
    db.init_app(app)

@manager.command
def gentables():
    db.create_all()
    print('TABLES GENERATED')

# def generateMessage(student, dinner):

@manager.command
def createSuperAdmin():
    a = UserModel("unclaimed", "pass" , "yasa.baig@gmail.com", 0,"uncl10", "12345", "Unclaimed","User", "123-123-1234",1, "Lorem Ipsum" )
    b = UserModel("superadmin", "pass" , "yasab27@gmail.com", 0,"ce10", "12345", "Super","Admin", "123-123-1234",1, "Lorem Ipsum" )

    db.session.add(a)
    db.session.add(b)
    db.session.commit()

    allUsers = db.session.query(UserModel).all()
    for user in allUsers:
        print("ADMINS: {} {} ROLE: {}".format(user.firstName, user.lastName, user.role))

@manager.command
def testEmail():
    from app import mail

    try:
        msg = Message("Congratulations!",
          sender="dukeconversationsreminders@gmail.com",
          recipients=["yasa.baig@duke.edu"])
          #entryOfInterest.email

        # Read the html from the email template.
        soup = BeautifulSoup(open("email-templates/acceptance.html"),"html.parser")
        print(soup.prettify())
        msg.html = soup.prettify().format("CLORK BROID", "FRIDAY",
                                            "JUNE 20TH", "COOPER EDMUNDS", "GRANT BESNER", "FRIDAY",
                                            "5 WALLABY WAY SYDNEY", "JOMATO FARMING","123-123-1234", "GRANT BESNER")
        mail.send(msg)
    except Exception as e:
        return {"Message": str(e)}

@manager.command
def populate():
    a = UserModel("coopedmunds", "pass" , "cooper.edmunds@duke.edu", 2,"ce10", "12345", "Cooper","Edmunds", "123-123-1234",1, "Lorem Ipsum" )
    b = UserModel("yasab27", "pass" , "yasa.baig@duke.edu", 2,"ymb8", "12345", "Yasa","Baig", "123-123-1234",1, "Lorem Ipsum" )
    c = UserModel("grantbes", "pass" , "grantbesner@duke.edu", 2,"gbe1", "12345", "Grant","Besner", "123-123-1234",1, "Lorem Ipsum" )

    db.session.add(a)
    db.session.add(b)
    db.session.add(c)
    db.session.commit()

    allUsers = db.session.query(UserModel).all()
    for user in allUsers:
        print(user.username)

@manager.command
def populateMega():
    a = UserModel("rcw15","convo434","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("aa377","convo868","aa377@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("gmb33","convo838","gmb33@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("ls301","convo292","ls301@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("aa377","convo404","fyf@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("fyf","convo191","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("kl262","convo929","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("al343","convo010","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("mk377","convo737","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("su30","convo353","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("ksd28","convo232","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("sjk45","convo303","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("al325","convo949","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("acc86","convo383","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("rp161","convo939","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("jk370","convo363","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("aea33","convo848","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("jmc178","convo181","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("lpc23","convo202","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("kah138","convo272","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("adn22","convo939","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("ay103","convo434","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("ahz2","convo505","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    a = UserModel("hlk4","convo121","rwc15@duke.edu", 2, "rwc15", "12345", "Bo","Carlson","7044915888",1, "Lorem Ipsum" )
    db.session.add(a)
    db.session.add(b)
    db.session.add(c)
    db.session.commit()

    allUsers = db.session.query(UserModel).all()
    for user in allUsers:
        print(user.username)

def remindStudents(dinner):

    from app import mail

    dinnerTimeDifference = int(dinner.timeStamp)-time.time()
    print(dinnerTimeDifference)
    print(datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x'))

    if dinnerTimeDifference <= 691200 and dinnerTimeDifference >= 604800:
        emailStudents(dinner, "One Week Reminder")
    elif dinnerTimeDifference <= 518400 and dinnerTimeDifference >= 432000:
        emailStudents(dinner, "5 Day Reminder")
    elif dinnerTimeDifference <= 259200 and dinnerTimeDifference >= 172800:
        emailStudents(dinner, "3 Day Reminder")
    elif dinnerTimeDifference <= 86400 and dinnerTimeDifference >= 0:
        emailStudents(dinner, "1 Day Reminder")

def emailStudents(dinner, time):
    for application in dinner.applications:
        if application.status is 1:
            try:
                dinnerTime = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x')
                msg = Message("{}".format(time),
                  sender="dukeconversationsreminders@gmail.com",
                  recipients=["{}@duke.edu".format(application.studentID)]) #entryOfInterest.email
                msg.html = "Don't forget you have a dinner with {} {} on {}.  !".format(dinner.professor.firstName, dinner.professor.lastName, dinnerTime)
                mail.send(msg)
            except Exception as e:
                return {"Message": str(e)}

def remindProfessor(dinner):
    from app import mail

    dinnerTimeDifference = int(dinner.timeStamp)-time.time()

    print(dinnerTimeDifference)
    print(datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x'))

    dinnerTime = datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x')

    if dinnerTimeDifference <= 691200 and dinnerTimeDifference >= 604800:
        emailProf("One Week Reminder", dinner.professor.email, dinnerTime)
    elif dinnerTimeDifference <= 86400 and dinnerTimeDifference >= 0:
        emailProf("One Day Reminder", dinner.professor.email, dinnerTime)

def emailProf(notificationLine, recipient, dinnerTime):
    try:
        msg = Message(notificationLine,
          sender="dukeconversationsreminders@gmail.com",
          recipients=[recipient]) #entryOfInterest.email
        #TODO
        msg.html = "Don't forget you have a dinner with on {}.  !".format( dinnerTime)
        mail.send(msg)
    except Exception as e:
        return {"Message":str(e)}

def remindUser(dinner):
    from app import mail

    dinnerTimeDifference = int(dinner.timeStamp)-time.time()
    print(dinnerTimeDifference)
    print(datetime.datetime.fromtimestamp(int(dinner.timeStamp)).strftime('%x'))
    # If it is between three and 2 days away
    if dinnerTimeDifference <= 1.21e+6 and dinnerTimeDifference >= 1.123e6:
        emailUser("Two Week Reminder", dinner.user.email, dinnerTime )
    elif dinnerTimeDifference <= 691200 and dinnerTimeDifference >= 604800:
        emailUser("One Week Reminder", dinner.user.email, dinnerTime)
    elif dinnerTimeDifference <= 518400 and dinnerTimeDifference >= 432000:
        emailUser("5 Day Reminder", dinner.user.email, dinnerTime)
    elif dinnerTimeDifference <= 259200 and dinnerTimeDifference >= 172800:
        emailUser("Three Day Reminder", dinner.user.email, dinnerTime)
    elif dinnerTimeDifference <= 86400 and dinnerTimeDifference >= 0:
        emailUser("One Day Reminder", dinner.user.email, dinnerTime)


def emailUser(notificationLine, recipient, dinnerTime):
    try:
        msg = Message(notificationLine,
          sender="dukeconversationsreminders@gmail.com",
          recipients=[recipient]) #entryOfInterest.email
        #TODO
        msg.html = "Don't forget you are hosting a dinner on {}.  !".format( dinnerTime)
        mail.send(msg)
    except Exception as e:
        return {"Message":str(e)}


@manager.command
def hello():
    dinners = DinnerModel.return_all_objects()
    # First, email the user their list of matches
    for dinner in dinners:
        remindStudents(dinner)
        remindProfessor(dinner)
        remindUser(dinner)
    print(time.time())

# Iterate through all of the students in the database whose dinners have already past. If they confirmed
# but where not present, blacklist them.
@manager.command
def blacklist():
    dinners = DinnerModel.return_all_objects()

    for dinner in dinners:
        # if the dinner has past, i.e. if the current timestamp exceeds the dinner timestamp
        if int(float(dinner.timeStamp)) < time.time():
            # Get all of the applications
            applications = dinner.applications

            # Iterate through all of the applications of the dinner, find the users which confirmed
            # but didn't show up, and then blacklist them.
            for app in applications:
                if app.confirmed and not app.present:
                    student = StudentModel.find_by_id(app.studentID)
                    student.blackList = True
                    student.save_to_db()


if __name__ == "__main__":
    manager.run()
