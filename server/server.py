from flask import Flask, render_template, request, jsonify, make_response, send_from_directory, g
from flask_login import LoginManager, login_required, current_user
from sqlalchemy import desc
from auth import auth as auth_blueprint
from db.user import User
from db.message import Message, MessageStatus
from db.db import Session

import datetime

from item_manager import ItemManager

app = Flask(__name__)


@app.route("/")
@login_required
def index():
    """ Route to render the HTML """
    return send_from_directory('../dist', "index.html")


@app.route("/main.js")
def js():
    """ Route to render the HTML """
    return send_from_directory('../dist', "main.js")


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('../dist', path)


@app.route("/load", methods=['POST'])
@login_required
def load():
    """ Route to return the posts """
    item_manager = ItemManager(current_user.id)
    items = [item.to_jsonable() for item in item_manager.get_items(20)]
    return jsonify(items)


@app.route('/whoami/')
@login_required
def whoami():
    return jsonify({"current user": current_user.id})


@app.route('/previous_messages/', methods=['POST'])
@login_required
def get_previous_messages_unknown_number():
    session = g.session
    number_to_load = 10
    messages = (
        session
        .query(Message)
        .filter(Message.user_id == current_user.id)
        .order_by(desc(Message.id))
        .limit(number_to_load)
        .all())
    acc = [message.as_dict() for message in messages]
    return jsonify(acc)


@app.route('/previous_messages/<int:last_id>', methods=['POST'])
@login_required
def get_previous_messages(last_id):
    # init SQLAlchemy so we can use it later in our models
    session = g.session
    number_to_load = 10
    messages = (
        session
        .query(Message)
        .filter(Message.user_id == current_user.id)
        .filter(Message.id < last_id)
        .order_by(desc(Message.id))
        .limit(number_to_load)
        .all())
    acc = [message.as_dict() for message in messages]
    return jsonify(acc)


class NewMessageHandler:
    # in message
    def __init__(self, message):
        self.message = message

    @staticmethod
    def message_handler(message):
        if message.startswith("/"):
            return "search"

    def do(self, session):
        new_message = self.store_message(session, self.message)
        response = self.message_handler(self.message)
        if response:
            new_response = self.store_message(session, response, MessageStatus.SERVER)
            return [new_message.as_dict(), new_response.as_dict()]
        else:
            return [new_message.as_dict()]
        

    @staticmethod
    def store_message(session: Session, message: str, status: MessageStatus =MessageStatus.USER)->Message:
        now = datetime.datetime.now()
        new_message = Message(
            user_id=current_user.id,
            message=message,
            status=status,
            timestamp=now)
        session.add(new_message)
        session.commit()
        return new_message


@app.route('/store_message', methods=['POST'])
@login_required
def store_message():
    # init SQLAlchemy so we can use it later in our models
    session = g.session
    message = request.json.get("message")
    return jsonify(NewMessageHandler(message).do(session))

@app.before_request
def attachdb():
    g.session = Session()

@app.teardown_request
def teardown_request(exception):
    g.session.close()
    Session.remove()

@app.after_request
def closedb(request):
    g.session.close()
    Session.remove()
    return request

if __name__ == "__main__":
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        session = g.session
        # since the user_id is just the primary key of our user table, use it in the query for the user
        user =  session.query(User).filter(User.id==int(user_id)).one()
        print(user.id)
        return user

    app.register_blueprint(auth_blueprint)
    app.run(port=8008, host="0.0.0.0")
