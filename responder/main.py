from responder.new_message_handler import NewMessageHandler

def of_user(message):
    pass
def has_data(message):
    pass


def handle_message(message, user_id, session):
    # So currently the message is just a string so there is no way to answer these questions
    if not of_user(last_message) and has_data(last_message):
        MessageFactory(data(last_message)["type"])(data)
    else:
        NewMessageHandler(message).user_id(current_user.id).session(session).message_handler().run()
