#!/usr/bin/env python

import logging
import re
from typing import Callable, Dict
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
    def register(cls, name: str) -> Callable:
        """Class method to register Executor class to the internal registry."""

        def inner_wrapper(wrapped_class: MessageHandlerBase) -> MessageHandlerBase:
            if isinstance(wrapped_class, LiteralResponder):
                if name in cls.literal:
                    logger.warning("Executor %s already exists. Will replace it", name)
                cls.literal[name] = wrapped_class
            elif isinstance(wrapped_class, RegexResponder):
                if name in cls.regex:
                    logger.warning("Executor %s already exists. Will replace it", name)
                cls.regex[name] = wrapped_class
            elif isinstance(wrapped_class, RegexPOSResponder):
                if name in cls.regex_pos:
                    logger.warning("Executor %s already exists. Will replace it", name)
                cls.regex_pos[name] = wrapped_class
            elif isinstance(wrapped_class, NLPTreeResponder):
                if name in cls.nlp_tree:
                    logger.warning("Executor %s already exists. Will replace it", name)
                cls.nlp_tree[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def create_handler(factory, message: str) -> MessageHandlerBase:
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

    def match_literal(self, message):
        if message in self.literal:
            return self.literal[message]

    def match_regex(self, message):
        for regex in self.regex:
            match = re.match(regex, message)
            if match:
                return self.regex[regex]

    def match_regexPOS(self, message):
        pass

    def match_NLPTree(self, message):
        pass
