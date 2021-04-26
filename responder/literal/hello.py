from responder.message_handler_base import LiteralResponder
from responder.message_handler_factory import MessageHandlerFactory


@MessageHandlerFactory.register()
class Hello(LiteralResponder):
    @staticmethod
    def get_name():
        return "hello"
