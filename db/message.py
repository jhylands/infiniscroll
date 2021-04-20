from sqlalchemy import types, Column, Integer, String, DateTime
import enum
from db.base import Base

class IntEnum(types.TypeDecorator):
    """
    As explained here: https://stackoverflow.com/questions/33612625/how-to-model-enums-backed-by-integers-with-sqlachemy
    This defines an integer enum, normally when using sqlalchemy enums the enum name is stored as a string.
    I wanted them to be stored as their integer value. That is what this allows
    """
    impl = Integer
    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)

class MessageStatus(enum.Enum):
    USER = 0
    SERVER = 1


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user_id = Column(Integer)
    message = Column(String(100))
    status = Column(IntEnum(MessageStatus))
    timestamp = Column(DateTime())

    def as_dict(self):
        print(self.timestamp)
        return {"message": self.message, "id": self.id, "status": self.status.value, "timestamp": self.timestamp.strftime("%Y-%m-%d;%H:%M:%S")}
