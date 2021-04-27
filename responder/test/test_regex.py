from responder.new_message_handler import NewMessageHandler
from responder.message_handler_base import NonMatchingResponder
from responder.regex.subscribe import Subscribe
import re
import pytest


@pytest.mark.parametrize(
    "url, valid",
    [
        ("sub http://feeds.bbci.co.uk/news/rss.xml", True),
        ("subscribe http://feeds.bbci.co.uk/news/rss.xml", True),
        ("sub https://feeds.bbci.co.uk/news/rss.xml", True),
        ("sub https://feeds.bbci.co.uk/news/rss", True),
        ("sub https://bbc.co.uk", True),
        ("sub http://bbc.co.uk:80/news/rss.xml?valid=true#title", True),
        ("sub", False),
        ("subscribe", False),
        ("http://feeds.bbci.co.uk/news/rss.xml", False),
        ("http://bbc.co.uk/news/rss.xml", False),
    ],
)
def test_url_regex_query(url, valid):
    assert bool(re.match(Subscribe.get_name(), url)) == valid


def test_regex():
    handler = NewMessageHandler(
        "subscribe http://feeds.bbci.co.uk/news/rss.xml"
    ).message_handler()
    assert not isinstance(handler, NonMatchingResponder)
    assert isinstance(handler, Subscribe)
