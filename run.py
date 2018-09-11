from app import app
from db import db

# Ask the db to create all the necessary tables before operation
@app.before_first_request
def create_tables():
    db.create_all()

db.init_app(app)
