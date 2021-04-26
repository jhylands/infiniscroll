from responder.new_message_handler import NewMessageHandler
from responder.message_handler_base import NonMatchingResponder

from responder.literal.hello import Hello


def test_hello():
    print("starting test")
    handler = NewMessageHandler("hello").message_handler()
    assert not isinstance(handler, NonMatchingResponder)
    assert isinstance(handler, Hello)
