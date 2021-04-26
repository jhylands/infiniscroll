from abc import ABCMeta, abstractmethod


class MessageHandlerBase(metaclass=ABCMeta):
    """ Base class for an executor """

    def __init__(self, handler: "NewMessageHandler", **kwargs):
        """ Constructor """
        self.handler = handler

    @staticmethod
    @abstractmethod
    def get_name():
        pass

    # @abstractmethod
    def run(self, command: str) -> str:
        """ Abstract method to run a command """
        pass


class LiteralResponder(MessageHandlerBase):
    pass


class RegexResponder(MessageHandlerBase):
    pass


class RegexPOSResponder(MessageHandlerBase):
    pass


class NLPTreeResponder(MessageHandlerBase):
    pass


class NonMatchingResponder(MessageHandlerBase):
    @staticmethod
    def get_name():
        return "NonMatchingResponder"
