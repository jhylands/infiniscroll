class StateMessageHandler:
    def __init__(self, message):
        self._message = message
        self._user_id = None
        self._session = None

    def user_id(self, user_id):
        self._user_id = user_id
        return self

    def session(self, session):
        self._session = session
        return self

    def get_user(self):
        if self._session:
            return self._session.query(User).filter(User.id == self._user_id).one()
        raise Exception("No session attached, can't query for user object")
