from db.db import db
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user_id = db.Column(db.Integer)
    message = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime())
