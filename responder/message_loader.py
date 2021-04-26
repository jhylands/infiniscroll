from db.message import Message
from sqlalchemy import desc


class MessageLoader:
    def __init__(self, session):
        self.session = session
        self._user_id = None
        self._last_id = None
        self.number_to_load = 10

    def user_id(self, user_id):
        self._user_id = user_id
        return self

    def load(self, number_to_load=10):
        self.number_to_load = number_to_load
        return self

    def last_id(self, last_id):
        self._last_id = last_id
        return self

    def send(self):
        number_to_load = self.number_to_load
        message_query = self.session.query(Message).filter(
            Message.user_id == self._user_id
        )
        if self._last_id:
            message_query = message_query.filter(Message.id < self._last_id)
        messages = message_query.order_by(desc(Message.id)).limit(number_to_load).all()
        return [message.as_dict() for message in messages]
