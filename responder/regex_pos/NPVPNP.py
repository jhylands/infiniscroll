
from db.message import Message, MessageStatus
from responder.message_handler_base import RegexPOSResponder
from responder.message_handler_factory import MessageHandlerFactory


@MessageHandlerFactory.register()
class Hello(RegexPOSResponder):
    @staticmethod
    def get_name():
        return "(?i)h(i|ello).*"

    def run(self):
        handler = self.handler
        command = self.command
        response = "Hi there!"
        return [
            handler.store_message(command, MessageStatus.USER).as_dict(),
            handler.store_message(response, MessageStatus.SERVER).as_dict(),
        ]
