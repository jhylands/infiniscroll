from db.message import Message, MessageStatus
from abc import ABCMeta, abstractmethod
from typing import List


class MessageHandlerBase(metaclass=ABCMeta):
    """ Base class for an executor """

    def __init__(self, command: str, handler: "NewMessageHandler"):
        """ Constructor """
        self.command = command
        self.handler = handler

    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @abstractmethod
    def run(self) -> List[dict]:
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

    def run(self) -> List[dict]:
        command = self.command
        handler = self.handler
        return [handler.store_message(command, MessageStatus.USER).as_dict()]
