from db.db import db
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    message = db.Column(db.String(100))
    time = db.Column(db.DateTime())
