from db.message import Message, MessageStatus
from responder.message_handler_factory import MessageHandlerFactory, create_handler
import responder.literal  # noqa: F401
import responder.regex  # noqa: F401
import responder.regex_pos  # noqa: F401
import responder.nlp_tree  # noqa: F401
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
        return create_handler(MessageHandlerFactory, self._message)(self._message, self)

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
