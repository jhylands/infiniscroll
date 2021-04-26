from responder.message_handler_factory import MessageHandlerBase


@MessageHandlerFactory.register("hello")
class Greeting(MessageHandlerBase):
    def __init__(self):
        super().__init__("Hello")

    def match():
        pass

    def run(self, command: str) -> (str, str):
        """ Runs the given command using subprocess """
        pass
