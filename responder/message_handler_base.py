from abc import ABCMeta, abstractmethod


class MessageHandlerBase(metaclass=ABCMeta):
    """ Base class for an executor """

    def __init__(self, **kwargs):
        """ Constructor """
        pass

    def match(self, message):
        pass

    @abstractmethod
    def run(self, command: str) -> str:
        """ Abstract method to run a command """
        pass


class LiteralResponder(MessageHandlerBase):
    def __init__(self, literal):
        self._literal = literal


class RegexResponder(MessageHandlerBase):
    pass


class RegexPOSResponder(MessageHandlerBase):
    pass


class NLPTreeResponder(MessageHandlerBase):
    pass

class NonMatchingResponder(MessageHandlerBase):
    pass
