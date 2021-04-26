from responder.new_message_handler import NewMessageHandler
from responder.message_handler_base import NonMatchingResponder



def test_hello():
    print("starting test")
    handler = NewMessageHandler("hello").message_handler()
    assert not isinstance(handler, NonMatchingResponder)
    from responder.literal.hello import Hello
    assert isinstance(handler, Hello)
