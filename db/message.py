from sqlalchemy import Column, Integer, String, DateTime
from db.base import Base


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user_id = Column(Integer)
    message = Column(String(100))
    timestamp = Column(DateTime())
