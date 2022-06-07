from db.message import Message, MessageStatus
from responder.message_handler_base import RegexResponder
from responder.message_handler_factory import MessageHandlerFactory

import re


@MessageHandlerFactory.register()
class Hello(RegexResponder):
    @staticmethod
    def get_name():
        return re.compile("(?i)h(i|ello).*")

    def run(self):
        handler = self.handler
        command = self.command
        response = "Hi there!"
        return [
            handler.store_message(command, MessageStatus.USER).as_dict(),
            handler.store_message(response, MessageStatus.SERVER).as_dict(),
        ]
