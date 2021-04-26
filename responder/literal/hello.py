from db.message import Message, MessageStatus
from responder.message_handler_base import LiteralResponder
from responder.message_handler_factory import MessageHandlerFactory


@MessageHandlerFactory.register()
class Hello(LiteralResponder):
    @staticmethod
    def get_name():
        return "hello"

    def run(self):
        handler = self.handler
        command = self.command
        response = "Hi there!"
        return [
            handler.store_message(command, MessageStatus.USER).as_dict(),
            handler.store_message(response, MessageStatus.SERVER).as_dict(),
        ]
