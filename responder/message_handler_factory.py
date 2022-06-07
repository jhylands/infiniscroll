#!/usr/bin/env python

import logging
import re
import posre
from typing import Callable, Dict, Type
from responder.message_handler_base import (
    MessageHandlerBase,
    LiteralResponder,
    RegexResponder,
    RegexPOSResponder,
    NLPTreeResponder,
    NonMatchingResponder,
)


logger = logging.getLogger(__name__)
# so we want to have some types of matching
# - literal <- The simplest
# - regex <- large lists of these might become complex to manage
# - regex(With POS tagging) <- Might be worth preprocessing the string first for this
# - nlp tree <- I'm still not sure how exactly to build these out

# for longer responses perhaps we should send an indication with the response that we expect there to be some reasoning around


class MessageHandlerFactory:
    """ The factory class for creating executors"""

    literal: Dict[str, LiteralResponder] = {}
    regex: Dict[str, RegexResponder] = {}
    regex_pos: Dict[str, RegexPOSResponder] = {}
    nlp_tree: Dict[str, NLPTreeResponder] = {}

    """ Internal registry for available executors """

    @classmethod
    def register(cls) -> Callable:
        """Class method to register Executor class to the internal registry."""

        def inner_wrapper(wrapped_class: MessageHandlerBase) -> MessageHandlerBase:
            if LiteralResponder in wrapped_class.__mro__:
                if wrapped_class.get_name() in cls.literal:
                    logger.warning("Executor %s already exists. Will replace it", name)
                cls.literal[wrapped_class.get_name()] = wrapped_class
            elif RegexResponder in wrapped_class.__mro__:
                if wrapped_class.get_name() in cls.regex:
                    logger.warning(
                        "Executor %s already exists. Will replace it",
                        wrapped_class.get_name(),
                    )
                cls.regex[wrapped_class.get_name()] = wrapped_class
            elif RegexPOSResponder in wrapped_class.__mro__:
                if wrapped_class.get_name() in cls.regex_pos:
                    logger.warning(
                        "Executor %s already exists. Will replace it",
                        wrapped_class.get_name(),
                    )
                cls.regex_pos[wrapped_class.get_name()] = wrapped_class
            elif NLPTreeResponder in wrapped_class.__mro__:
                if wrapped_class.get_name() in cls.nlp_tree:
                    logger.warning(
                        "Executor %s already exists. Will replace it",
                        wrapped_class.get_name(),
                    )
                cls.nlp_tree[wrapped_class.get_name()] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def match_literal(self, message):
        if message in self.literal:
            return self.literal[message]

    @classmethod
    def match_regex(self, message):
        for regex in self.regex:
            # The returned items should be compiled regex for speed
            match = regex.match(message)
            if match:
                return self.regex[regex]

    @classmethod
    def match_regexPOS(self, message):
        for posgex in self.regex_pos:
            # The returned items should be compiled regex for speed
            match = posgex.match(message)
            if match:
                return self.regex_pos[posgex]

    @classmethod
    def match_NLPTree(self, message):
        pass


def create_handler(
    factory: MessageHandlerFactory, message: str
) -> MessageHandlerBase:
    """Factory command to create the executor.

    This method gets the appropriate Executor class from the registry
    and creates an instance of it, while passing in the parameters
    given in ``kwargs``.
    Args:
        name (str): The name of the executor to create.
    Returns:
        An instance of the executor that is created.
    """
    literal = factory.match_literal(message)
    if literal:
        return literal
    regex = factory.match_regex(message)
    if regex:
        return regex
    regexPOS = factory.match_regexPOS(message)
    if regexPOS:
        return regexPOS
    NLPTree = factory.match_NLPTree(message)
    if NLPTree:
        return NLPTree

    return NonMatchingResponder

def find_handle(factory: MessageHandlerFactory, name: str)-> MessageHandlerBase:
    if name in factory.literal:
        return factory.literal[name]
    if name in factory.regex:
        return factory.regex[name]
    if name in factory.regex_pos:
        return factory.regex_pos[name]
    if name in factory.nlp_tree:
        return factory.nlp_tree[name]
    return NonMatchingResponder
