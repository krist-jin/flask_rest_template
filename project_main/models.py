from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ad(db.Model):
    """This is the model for advertisement"""
    __tablename__ = 'Ad'
    id = db.Column(db.Integer, primary_key = True)
    category_id = db.Column(db.Integer)
    content = db.Column(db.String(1000))
    score = db.Column(db.Integer)

    def __init__(self, category_id, content):
        self.category_id = category_id
        self.content = content
        self.score = 0  # the default score is 0

class Impression(db.Model):
    """This is the model for Impression"""
    __tablename__ = 'Impression'
    id = db.Column(db.Integer, primary_key = True)
    aid = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)  # for the sake of simplicity I use int to represent timestamp

    def __init__(self, aid, timestamp):
        self.aid = aid
        self.timestamp = timestamp

class Click(db.Model):
    """This is the model for Click"""
    __tablename__ = 'Click'
    id = db.Column(db.Integer, primary_key = True)
    aid = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)  # for the sake of simplicity I use int to represent timestamp

    def __init__(self, aid, timestamp):
        self.aid = aid
        self.timestamp = timestamp