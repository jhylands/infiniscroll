from db.message import Message, MessageStatus
from sqlalchemy import desc
import datetime


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


class NewMessageHandler:
    # in message
    def __init__(self, message):
        self._message = message
        self._user_id = None
        self._session = None

    def user_id(self, user_id):
        self._user_id = user_id
        return self

    def session(self, session):
        self._session = session
        return self

    @staticmethod
    def message_handler(message):
        if message.startswith("/"):
            return "search"

    def send(self):
        new_message = self.store_message(self._message, MessageStatus.USER)
        response = self.message_handler(self._message)
        if response:
            new_response = self.store_message(response, MessageStatus.SERVER)
            return [new_message.as_dict(), new_response.as_dict()]
        else:
            return [new_message.as_dict()]

    def store_message(self, message: str, status: MessageStatus) -> Message:
        now = datetime.datetime.now()
        new_message = Message(
            user_id=self._user_id,
            message=message,
            status=status,
            timestamp=now,
        )
        self._session.add(new_message)
        self._session.commit()
        return new_message
