from flask.ext.sqlalchemy import SQLAlchemy
from project_main import db
import json

def to_dictionary(inst, cls):
    """
    dictionarize the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d

class User(db.Model):
    """This is the model for User"""
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(1000))
    zipcode = db.Column(db.Integer)

    def __init__(self, name, content):
        self.name = name
        self.zipcode = content

    @property
    def dictionary(self):
        return to_dictionary(self, self.__class__)

db.create_all()