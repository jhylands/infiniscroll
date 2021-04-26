from db.message import Message, MessageStatus
from responder.message_handler_factory import MessageHandlerFactory, create_handler
import datetime


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

    def message_handler(self):
        return create_handler(MessageHandlerFactory, self._message)(self)

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
