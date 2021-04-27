from db.message import Message, MessageStatus
import feedparser
from responder.message_handler_base import RegexResponder
from responder.message_handler_factory import MessageHandlerFactory
from neo.functions import get_user, subscribe, add_feed
import re


@MessageHandlerFactory.register()
class Subscribe(RegexResponder):
    @staticmethod
    def get_name():
        # It would be nice to use a library like urlextract
        # here but we need the name to remain a regex to fit the
        # pattern.
        subscribe = r"(?:sub(?:scribe)?)"
        protocol = r"(?:https?)"
        domain = r"(?:(?:\w+|\.)+)"
        port = r"(?:\:\d+)"
        path = r"(?:(?:\/|\w|.])+)"
        query = r"(?:\?\w+=\w+)"
        fragment = r"(?:#\w+)"
        return f"(?i){subscribe}\s+({protocol}://{domain}{port}?{path}?{query}?{fragment}?)"

    def run(self):
        handler = self.handler
        command = self.command
        match = re.match(self.get_name(), command)
        url = match.group(1)
        print("url", url)
        parsed_feed = feedparser.parse(url)
        title = parsed_feed.feed.title

        # Shouldn't really be accessing the private
        # property here
        # I relly don't think having the user wait for the response calculation is a good idea
        user = get_user(handler._user_id)
        feed = add_feed(title, url)
        subscribe(user, feed)
        response = "Subscribed to {}".format(title)
        return [
            handler.store_message(command, MessageStatus.USER).as_dict(),
            handler.store_message(response, MessageStatus.SERVER).as_dict(),
        ]