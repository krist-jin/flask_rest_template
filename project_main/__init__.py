from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from db_credentials import SQLALCHEMY_DATABASE_URI
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
logging.basicConfig(filename='app.log',level=logging.INFO,format='%(asctime)s --- %(message)s')

db = SQLAlchemy(app)
