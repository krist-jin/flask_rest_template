from flask import Flask
from models import db
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ebay'
 
logging.basicConfig(level=logging.INFO,format='%(asctime)s --- %(message)s')
db.init_app(app)