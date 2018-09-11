# Here we create the SQL Alchemy ORM which will allow us to easily read and write to the DB
from flask_sqlalchemy import SQLAlchemy

# SQL Alchemy allows us to directly map objects in python to rows in a database
db = SQLAlchemy()
